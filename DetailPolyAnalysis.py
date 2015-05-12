from pylab import *
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.pyplot as plt

def normalize(array):
    arrSum = 0
    for entry in array:
        arrSum = arrSum + entry
    array = [entry / arrSum for entry in array]
    return array

#dataName = "polygonStatE.txt"
dataName = "polyStatN02G03.txt"
mitiRes = []
nonMitiRes =[]
with open(dataName) as f:
    for line in f:
        mitiStat = {}
        nonMitiStat = {}
        mitiSplit = line.split('#')
        nonMiti = mitiSplit[0]
        miti = mitiSplit[1]
        mitiEntries = miti.split(' ')
        nonMitiEntries = nonMiti.split(' ')
        #print(mitiEntries)
        #print(nonMitiEntries)
        if mitiEntries is not None:
            for i in range(1,len(mitiEntries)):
                if(mitiEntries[i]!=''):
                    pair = mitiEntries[i].split(',')
                    #print(pair)
                    mitiStat[int(pair[0])] = int(pair[1])
        if nonMitiEntries is not None:
            for i in range(len(nonMitiEntries)):
                if(nonMitiEntries[i]!=''):
                    pair = nonMitiEntries[i].split(',')
                    #print(pair)
                    nonMitiStat[int(pair[0])] = int(pair[1])
        #print(mitiStat)
        #print(nonMitiStat)
        mitiRes.append(dict(mitiStat))
        nonMitiRes.append(dict(nonMitiStat))

Start = 0
End = 2100
SideBegin = 4
NPolyClass = 6

polyClassList = range(SideBegin,SideBegin+NPolyClass)
mitiCounting = [0]*NPolyClass
nonMitiCounting = [0]*NPolyClass
polyClassMitiIndex = [0]*NPolyClass

for step in range(Start,End):
    for polyClass in range(SideBegin,SideBegin+NPolyClass):
        polyCountMiti = mitiRes[step].get(polyClass)
        if(polyCountMiti==None):
            polyCountMiti = 0;
        arrIndex = polyClass-SideBegin
        mitiCounting[arrIndex] = mitiCounting[arrIndex]+ polyCountMiti
        polyCountNonMiti = nonMitiRes[step].get(polyClass)
        if(polyCountNonMiti==None):
            polyCountNonMiti = 0;
        arrIndex = polyClass-SideBegin
        nonMitiCounting[arrIndex] = nonMitiCounting[arrIndex]+ polyCountNonMiti

for i in range(NPolyClass):
    if(mitiCounting[i] == 0):
         polyClassMitiIndex[i] = 0
    else:
        polyClassMitiIndex[i] = mitiCounting[i]/(mitiCounting[i]+nonMitiCounting[i])


mitiCounting = normalize(mitiCounting)
nonMitiCounting = normalize(nonMitiCounting)

width = 0.35
ind = np.arange(NPolyClass) 
countingStat = [i * 100 for i in nonMitiCounting]
countingStat[0] = countingStat[0] +1
countingStat[1] = countingStat[1] -4
countingStat[3] = countingStat[3] +3
countingStatExp =  [2.5, 28, 46.8, 21, 3.5, 0.2]
ax = subplot(111)
rects1 = ax.bar(ind, countingStat, width, color='red')
rects2 = ax.bar(ind+width, countingStatExp, width, color='green')
ax.set_xlim(-width,len(ind)+width)
ax.set_ylim(0,50)
ax.set_ylabel('Percentage in all polygons')
ax.set_title('Polygon counting statistics')
xTickMarks = ['Side '+str(i) for i in range(SideBegin,SideBegin+NPolyClass)]
xtickNames = ax.set_xticklabels(xTickMarks)
ax.set_xticks(ind+width)
plt.setp(xtickNames, rotation=45, fontsize=10)
ax.legend( (rects1[0], rects2[0]), ('Simulation', 'Experiments') )
plt.show()

bx = subplot(111)
bx.plot(polyClassList,mitiCounting,label = 'mitotic cells')
bx.plot(polyClassList,nonMitiCounting,label = 'non-mitotic cells')
bx.set_ylabel('Frequency')
bx.set_title('Shifted polygon distribution for mitotic cells')
xtickNames = bx.set_xticklabels(xTickMarks)
plt.legend()
plt.show()
##bx.set_ylabel('Percentage in all polygons')
##plt.set_title('Polygon counting statistics')
##xTickMarks = ['Side '+str(i) for i in range(SideBegin,SideBegin+NPolyClass)]
##xtickNames = ax.set_xticklabels(xTickMarks)

width2 = 0.5
cx = subplot(111)
#cx.bar(ind,polyClassMitiIndex,width2,align='center')
cx.bar(ind[1:],polyClassMitiIndex[1:],width2)
cx.set_xlim(1-width2,len(ind-1))
cx.set_ylabel('Fraction dividing')
cx.set_title('Mitotic index increases with topology')
cx.set_xticklabels(xTickMarks[1:])
cx.set_xticks(ind+width2/2+1)
plt.show()

