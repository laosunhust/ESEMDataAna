from detailDataRead import *
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
import math


def degreeToColor(degree):
    pass 

def fetchNetwork(frameData):
    G=nx.Graph()
    curCt = 0
    for cellStat in frameData:
        neighbors = cellStat.neighbors
        ngbrCt = int(cellStat.ngbrCt)
        cellRank = int(cellStat.rank)
        notBdry = not int(cellStat.isBdry)
        G.add_node(cellRank,pos=(float(cellStat.center[0]),
                                 float(cellStat.center[1])),
                   bdry = not notBdry,
                   ngbr = ngbrCt,
                   )
        if(notBdry):
            for neighbor in neighbors:
                G.add_edge(cellRank,int(neighbor))
    return G

def obtainAreaFrame(frameData,polyStart = 4,polyTypeCt = 6):
    areaSum = 0.0
    d = defaultdict(int)
    areaSumDict = defaultdict(float)
    for cellStat in frameData.stats:
        notBdry = not int(cellStat.isBdry)
        neighborCt = int(cellStat.ngbrCt)
        if(notBdry and neighborCt>=polyStart and neighborCt<polyStart+polyTypeCt):
            d[neighborCt] += 1
            areaSumDict[neighborCt] += float(cellStat.area)
    return (d,areaSumDict)

def obtainAreaAll(statSeq,startStep = 1500,polyStart = 4,polyTypeCt = 6):
    countAll = defaultdict(int)
    areaSumAll = defaultdict(float)
    step = 0
    for frame in statSeq:
        if step > startStep:
            polyCt,areaSum = obtainAreaFrame(frame,polyStart,polyTypeCt)
            for key in polyCt.keys():
                countAll[key] +=  polyCt[key]
                areaSumAll[key] += areaSum[key]
        step += 1
    areaAll = 0
    count_all = 0
    for key in areaSumAll:
        areaAll += areaSumAll[key]
        count_all +=countAll[key]
    areaAll = areaAll/count_all
    for key in areaSumAll:
        areaSumAll[key] = areaSumAll[key]/countAll[key]/areaAll
    print(areaSumAll)

def obtainFreqFrame(frameData,polyStart = 4,polyTypeCt = 6):
    result = [0.0]*polyTypeCt
    d = defaultdict(int)
    for cellStat in frameData.stats:
        notBdry = not int(cellStat.isBdry)
        neighborCt = int(cellStat.ngbrCt)
        #print(neighborCt)
        if(notBdry):
            d[neighborCt] += 1
    valueSum = float(sum(d.values()))
    if valueSum>0:
        for polyClass in range(polyStart,polyStart+polyTypeCt):
            result[polyClass-polyStart] = d[polyClass]/valueSum
    return result

def obtainFreqSeq(statSeq,polyStart = 4,polyTypeCt = 6):
    dataSize = len(statSeq)
    print(dataSize)
    freqSeq = np.zeros((polyTypeCt,dataSize))
    i = 0
    for frame in statSeq:
        print(i)
        frameFreq = obtainFreqFrame(frame,polyStart,polyTypeCt)
        for j in range(polyTypeCt):
            freqSeq[j][i] = frameFreq[j]
        i += 1
    return freqSeq

def obtainFrameCellCt(frameData):
    cellCt = 0
    for cellStat in frameData.stats:
        notBdry = not int(cellStat.isBdry)
        if(notBdry):
            cellCt += 1
    return cellCt

def obtainLastGen(statSeq,initalCellCt = 7):
    lastFrame = statSeq[-1]
    lastCellCt = obtainFrameCellCt(lastFrame)
    return math.log2(lastCellCt/float(initalCellCt))
    
    
#fileFolder = './data/dataOutput/'
#fileName = 'detailedStatE'
#statSeq = readSimuStat("detailedStatE*")
#statSeq = readSimuStat(fileFolder,fileName,4)
