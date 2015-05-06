from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
import os
import math

from skimage import io
from skimage import morphology
from skimage import data
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage import measure
from skimage.morphology import watershed
from skimage.feature import peak_local_max

def calBdryLen(imgData):
    size1 = len(imgData)
    size2 = len(imgData[0])
    bdryPosVec = []
    for i in range(size1):
        for j in range(size2):
            if (imgData[i][j] == True):
                # logic is strange here, but necessary to avoid bugs
                if(i==0 or i==size1-1):
                    bdryPosVec.append((i,j))
                else:
                    left = i-1
                    right = i+1
                    if(imgData[left][j] == False or
                       imgData[right][j] == False):
                        bdryPosVec.append((i,j))
                if(j==0 or j==size2-1):
                    bdryPosVec.append((i,j))
                else:
                    up = j-1
                    down = j+1
                    if(imgData[i][up] == False or
                       imgData[i][down] == False):
                        bdryPosVec.append((i,j))
    xList = []
    yList = []
    for pos in bdryPosVec:
        xList.append(pos[0])
        yList.append(pos[1])
    aveX = sum(xList) / float(len(xList))
    aveY = sum(yList) / float(len(yList))
    # find long axis
    xDiffVec = []
    yDiffVec = []
    xDiffUnit = []
    yDiffUnit = []
    for x,y in zip(xList,yList):
        diffX = x-aveX
        diffY = y-aveY
        xDiffVec.append(diffX)
        yDiffVec.append(diffY)
        vecPro = math.sqrt(diffX*diffX + diffY*diffY)
        if(diffX == 0 and diffY == 0):
            vecPro = 1.0  #to prevent divide by 0 error
        xDiffUnit.append(diffX/vecPro)
        yDiffUnit.append(diffY/vecPro)
    maxLen = 0
    maxDirX = 0
    maxDirY = 0
    for xDir, yDir in zip(xDiffUnit,yDiffUnit):
        tmpVec = []
        for xDiff,yDiff in zip(xDiffVec,yDiffVec):
            tmpVecPro = xDir*xDiff + yDir*yDiff
            tmpVec.append(tmpVecPro)
        tmpLen = (max(tmpVec) - min(tmpVec))/2
        if(tmpLen>maxLen):
            maxLen = tmpLen
            maxDirX = xDir
            maxDirY = yDir
    minLen = 0
    minDirX = maxDirY
    minDirY = -maxDirX
    tmpVec = []
    for xDiff,yDiff in zip(xDiffVec,yDiffVec):
        tmpVecPro = minDirX*xDiff + minDirY*yDiff
        tmpVec.append(tmpVecPro)
    minLen = (max(tmpVec) - min(tmpVec))/2
    maxLen += 0.5
    #minLen += 0.5
    # there is no formula for ellipse perimeter in simple form.
    # this formula is a relatively accurate approximation.
    perimeter = np.pi*(1.5*(maxLen+minLen)-math.sqrt(maxLen*minLen))
    return perimeter

def obtainSubImg(labels_ws, label):
    size1 = len(labels_ws)
    size2 = len(labels_ws[0])
    xList = []
    yList = []
    for i in range(size1):
        for j in range(size2):
            if(labels_ws[i][j] == label):
                xList.append(i)
                yList.append(j)
    x_Low = min(xList)
    x_High = max(xList)
    y_Low = min(yList)
    y_High = max(yList)
    res = labels_ws[x_Low:x_High+1,y_Low:y_High+1]
    res = res == label
    return res

def writeArrToFile(filename,arr,append = True):
    if(append):
        f = open(filename, "a")
        f.write(" ".join(str(elem) for elem in arr) + "\n")
        f.close()
    else:
        f = open(filename, "w")
        f.write(" ".join(str(elem) for elem in arr) + "\n")
        f.close()

def readArrFromFile(fname,delimiter = ' '):
    resArrs = []
    with open(fname) as f:
        for line in f:
            numStrs = line.split(delimiter)
            #print(numStrs)
            nums = []
            for numStr in numStrs:
                nums.append(float(numStr))
            resArrs.append(nums)
    return resArrs

def appendArrFromFile(resArrs,fname,delimiter = ' '):
    i=0
    with open(fname) as f:
        for line in f:
            numStrs = line.split(delimiter)
            #print(numStrs)
            nums = []
            for numStr in numStrs:
                resArrs[i].append(float(numStr))
            i += 1
    return resArrs

def calRoundness(imgFile,posVec,posExclude = [],showPic = True,
                 minPixelCt=50,greyThreshold = -1, bkgdFlip = True,
                 dataFileName = "roundness.txt",rewriteData = True):
    """ segment image first, then return the average roundness
        of normal objects, followed by average roundness of
        special objects, which are identified by input posVec.
        roundness is calculated as following:
        roundness = 4*PI*area/perimeter^2   """
    
    imgData = io.imread(imgFile)
    img_grey = rgb2gray(imgData)
    
    threshold = greyThreshold
    if(greyThreshold == -1):
            threshold = threshold_otsu(img_grey)
            #print("enter 1")
    #print(threshold)
    #print(img_grey)
    if(bkgdFlip):
            img = img_grey <= threshold
            #print("enter 3")
    else:
            img = img_grey >= threshold
            #print("enter 4")
    if(showPic):
            plt.imshow(img,cmap='gray')
            plt.show()
    # by default, the ndimage lib give background label 0
    bkgdLabel = 0
    labels_ws, nb_labels = ndimage.label(img)
    backMask = labels_ws == bkgdLabel
    labels_wsp = labels_ws % 30
    labels_wsp = labels_wsp + 1
    for i in range(len(labels_wsp)):
            for j in range(len(labels_wsp[0])):
                    if( backMask[i][j]):
                            labels_wsp[i][j] =  0
    ## show segmentated image
    if(showPic):
            plt.imshow(labels_wsp)
            plt.show()
    maxLabel = np.max(labels_ws)
    specialLabels = set()
    bdryLabels = set()
    specialRoundness = []
    normalRoundness = []
    specialArea = []
    normalArea = []
    for coord in posVec:
        # notice the switch of coord order
        xCoord = int(coord[1])
        yCoord = int(coord[0])  
        label = labels_ws[xCoord][yCoord]
        specialLabels.add(label)
        imgCell = obtainSubImg(labels_ws,label)
        #pixelCt is number of pixels. Used as area.
        pixelCt = np.sum(imgCell)
        specialArea.append(pixelCt)
        bdryLen = calBdryLen(imgCell)
        r = 4.0*np.pi*pixelCt/bdryLen/bdryLen
        specialRoundness.append(r)
        print(r,"special")
        if(showPic):
                plt.imshow(imgCell)
                plt.show()
    for coord in posExclude:
        xCoord = int(coord[1])
        yCoord = int(coord[0])  
        label = labels_ws[xCoord][yCoord]
        bdryLabels.add(label)
    size1 = len(labels_ws)
    size2 = len(labels_ws[0])
    for i in range(size1):
        bdryLabel1 = labels_ws[i][0]
        bdryLabel2 = labels_ws[i][size2-1]
        bdryLabels.add(bdryLabel1)
        bdryLabels.add(bdryLabel2)
    for i in range(size2):
        bdryLabel1 = labels_ws[0][i]
        bdryLabel2 = labels_ws[size1-1][i]
        bdryLabels.add(bdryLabel1)
        bdryLabels.add(bdryLabel2)
    if(not rewriteData):
        return
    for i in range(1,maxLabel):
        if(i not in specialLabels and i not in bdryLabels):
            imgCell = obtainSubImg(labels_ws,i)
            #pixelCt is number of pixels. Used as area.
            pixelCt = np.sum(imgCell)
            if(pixelCt<minPixelCt):
                continue
            normalArea.append(pixelCt)
            bdryLen = calBdryLen(imgCell)
            r = 4.0*np.pi*pixelCt/bdryLen/bdryLen
            print(r,"normal")
            #if(showPic):
            #    plt.imshow(imgCell)
            #    plt.show()
            normalRoundness.append(r)
    aveNormal = sum(normalRoundness) / float(len(normalRoundness))
    aveSpecial = sum(specialRoundness) / float(len(specialRoundness))
    print(aveNormal,aveSpecial)

    aveAreaSpecial = sum(specialArea) / float(len(specialArea))
    for i in range(len(normalArea)):
        normalArea[i] = normalArea[i] / aveAreaSpecial
    for i in range(len(specialArea)):
        specialArea[i] = 1
    writeArrToFile(dataFileName,normalRoundness,append = False)
    writeArrToFile(dataFileName,specialRoundness)
    writeArrToFile(dataFileName,normalArea)
    writeArrToFile(dataFileName,specialArea)
    #return (normalRoundness,specialRoundness,normalArea,specialArea)

##def calRoundness(imgFile,posVec,minPixelCt=50):
##    """ segment image first, then return the average roundness
##        of normal objects, followed by average roundness of
##        special objects, which are identified by input posVec.
##        roundness is calculated as following:
##        roundness = 4*PI*area/perimeter^2   """
##    imgData = io.imread(imgFile)
##    img_grey = rgb2gray(imgData)
##    threshold = threshold_otsu(img_grey)
##    #in case otsu doesn't work
##    #threshold = 0.35
##    img = img_grey <= threshold
##    plt.imshow(img,cmap='gray')
##    plt.show()
##    distance = ndimage.distance_transform_edt(img)
##    local_maxi = peak_local_max(distance, indices=False,
##                                footprint=np.ones((15,15)),labels=img)
##    markers = measure.label(local_maxi)
##    #labels_ws = watershed(-distance, markers, mask=img)
##    bkgdLabel = 0
##    labels_ws, nb_labels = ndimage.label(img)
##    #labels_ws = measure.label(img,background=bkgdLabel)
##    backMask = labels_ws == bkgdLabel
##    #print(background)
##    print(backMask)
##    labels_wsp = labels_ws % 30
##    labels_wsp = labels_wsp + 2
##    for i in range(len(labels_wsp)):
##            for j in range(len(labels_wsp[0])):
##                    if( backMask[i][j]):
##                            labels_wsp[i][j] =  0 
##    plt.imshow(labels_wsp)
##    ## show segmentated image
##    plt.show()
##    ##  maxLabel = np.max(labels_ws)
##    specialLabels = set()
##    specialRoundness = []
##    normalRoundness = []
##    for coord in posVec:
##        # notice the switch of coord order
##        xCoord = int(coord[1])
##        yCoord = int(coord[0])  
##        label = labels_ws[xCoord][yCoord]
##        specialLabels.add(label)
##        imgCell = obtainSubImg(labels_ws,label)
##        pixelCt = np.sum(imgCell)
##        bdPixCt = calBdryLen(imgCell)
##        r = 4.0*np.pi*pixelCt/bdPixCt/bdPixCt
##        specialRoundness.append(r)
##        print(r,"special")
##        plt.imshow(imgCell)
##        plt.show()
##    for i in range(1,maxLabel):
##        if i not in specialLabels:
##            #imgCell = labels_ws == i
##            imgCell = obtainSubImg(labels_ws,i)
##            pixelCt = np.sum(imgCell)
##            bdPixCt = calBdryLen(imgCell)
##            if(pixelCt<minPixelCt):
##                continue
##            r = 4.0*np.pi*pixelCt/bdPixCt/bdPixCt
##            normalRoundness.append(r)
##    aveNormal = sum(normalRoundness) / float(len(normalRoundness))
##    aveSpecial = sum(specialRoundness) / float(len(specialRoundness))
##    print(aveNormal,aveSpecial)
##    return (aveNormal,aveSpecial)
##
