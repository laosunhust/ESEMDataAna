from pylab import *
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.pyplot as plt

def normalize(array):
    arrSum = 0
    for entry in array:
        arrSum = arrSum + entry
    array = [entry / arrSum for entry in array]
    return array

dataName = "polygonStat.txt"
mitiRes = []
nonMitiRes =[]
with open(dataName) as f:
    for line in f:
        mitiStat = {}
        nonMitiStat = {}
        mitiSplit = line.split('#')
        miti = mitiSplit[0]
        nonMiti = mitiSplit[1]
        mitiEntries = miti.split()
        nonMitiEntries = nonMiti.split()
        for i in range(1,len(mitiEntries)):
            pair = mitiEntries[i].split(',')
            #print(pair)
            mitiStat[int(pair[0])] = int(pair[1])
        for i in range(len(nonMitiEntries)):
            pair = nonMitiEntries[i].split(',')
            #print(pair)
            nonMitiStat[int(pair[0])] = int(pair[1])
        #print(mitiStat)
        #print(nonMitiStat)
        mitiRes.append(dict(mitiStat))
        nonMitiRes.append(dict(nonMitiStat))

Start = 0
End = 240
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
    polyClassMitiIndex[i] = mitiCounting[i]/(mitiCounting[i]+nonMitiCounting[i])

mitiCounting = normalize(mitiCounting)
nonMitiCounting = normalize(nonMitiCounting)

plt.subplot(211)
plt.plot(polyClassList,mitiCounting)
plt.plot(polyClassList,nonMitiCounting)

plt.subplot(212)
plt.bar(polyClassList,polyClassMitiIndex,align='center')
plt.show()

width = 0.35
ind = np.arange(NPolyClass) 
countingStat = [i * 100 for i in nonMitiCounting] 
countingStatExp =  [7, 35, 38, 14, 2, 0.5]
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

##ax.set_xlim(-width,len(ind)+width)
##    ax.set_ylim(0,65)
##    ax.set_ylabel('Percentage in all polygons')
##    ax.set_title('Polygon counting statistics')
##    xTickMarks = ['Side '+str(i) for i in range(M,M+N)]
##    ax.set_xticks(ind+width)
##    xtickNames = ax.set_xticklabels(xTickMarks)
##    plt.setp(xtickNames, rotation=45, fontsize=10)
##    ax.legend( (rects1[0], rects2[0]), ('Simulation', 'Experiments') )

##ax = subplot(111)
##subplots_adjust(left=0.1, bottom=0.2)
##
##M = 4
##N = 5
##countingStat = [0, 0, 0, 0, 0]
##countingStatExp =  [7, 35, 38, 14, 2]
##expValSum =0
##for i in range(0,N):
##    expValSum = expValSum + countingStatExp[i]
##for i in range(0,N):
##    if(countingStatExp[i]!=0):
##        countingStatExp[i] = countingStatExp[i]/expValSum*100
##
##
#### necessary variables
##ind = np.arange(N)                # the x locations for the groups
##width = 0.35                      # the width of the bars
##
### axes and labels
##axcolor = 'lightgoldenrodyellow'
##axfreq = axes([0.1, 0.1, 0.8, 0.03], axisbg=axcolor)
##sTime = Slider(axfreq, 'Timestep', 0, len(res)-1, valinit=0)
##
##
##def updatePlot():
##    
##    rects1 = ax.bar(ind, countingStat, width,
##                color='blue')
##    rects2 = ax.bar(ind+width, countingStatExp, width,
##                    color='red')
##    ax.set_xlim(-width,len(ind)+width)
##    ax.set_ylim(0,65)
##    ax.set_ylabel('Percentage in all polygons')
##    ax.set_title('Polygon counting statistics')
##    xTickMarks = ['Side '+str(i) for i in range(M,M+N)]
##    ax.set_xticks(ind+width)
##    xtickNames = ax.set_xticklabels(xTickMarks)
##    plt.setp(xtickNames, rotation=45, fontsize=10)
##    ax.legend( (rects1[0], rects2[0]), ('Simulation', 'Experiments') )
##    
##
##def updateBarVal(countingStat,step):
##    valSum =0
##    for i in range(0,N):
##        val = res[step].get(i+M)
##        if(val==None):
##            val = 0
##        countingStat[i] = val
##        valSum = valSum + val
##    for i in range(0,N):
##        if(countingStat[i]!=0):
##            countingStat[i] = countingStat[i]/valSum*100
##
##def update(val):
##    ax.cla()
##    step = int(sTime.val)
##    updateBarVal(countingStat,step)
##    updatePlot()
##    draw()
##sTime.on_changed(update)
##
##
##show()
