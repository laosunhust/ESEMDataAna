import math
import matplotlib.pyplot as plt
import numpy as np
from detailDataRead import readSimuStat
from detailGrowthProcess import *

folder = 'E:/animationFiles/areaAnalysis/detailData'
fileName = 'deStat_N01G02_'
interval = 50
#beginFrame = 1093
beginFrame = 0

timeBegin = 0
timeEnd = 80

statSeq = readSimuStat(folder,fileName,interval)
sequence = statSeq.sequence

def plotCellCtSeq(statSeq,interval = 1,shrinkRatio = 0.032):
     tVec = []
     ctVec = []
     i = 0
     for frame in statSeq:
          ctVec.append(len(frame.stats))
          tVec.append(i)
          i = i+interval
     tVec = [t*shrinkRatio for t in tVec]
     ax = plt.subplot(221)
     beginIndx = int(beginFrame/interval)
     #print(beginIndx)
     plt.plot(tVec[beginIndx:],ctVec[beginIndx:],
              label = 'Simulation' )
     plt.title('Number of cells in wing disc')

     expr_t = np.linspace(timeBegin, timeEnd, 1000)
     expr_p = [20*math.exp(6*(1-math.exp(-0.03*t))) for t in expr_t]
     plt.plot(expr_t,expr_p,label = 'Experiment-fitted' )
     plt.yscale('log')
     plt.xlabel('Time [h]')
     plt.ylabel('Cell number')
     plt.title('Trend of cell number in wing disc')
     plt.legend(loc='lower right' )
     
     x1,x2,y1,y2 = plt.axis()
     plt.axis((timeBegin,timeEnd,y1,y2))
     #plt.show()

def plotAreaSeq(statSeq,interval = 1,shrinkRatio = 0.032):
     tVec = []
     aVec = []
     i = 0
     for frame in statSeq:
          area = obtainDiscArea(frame)
          aVec.append(area)
          tVec.append(i)
          i = i+interval
     tVec = [t*shrinkRatio for t in tVec]
     ax = plt.subplot(222)
     beginIndx = int(beginFrame/interval)
     plt.plot(tVec[beginIndx:],aVec[beginIndx:],label = 'Simulation' )
     
     expr_t = np.linspace(timeBegin, timeEnd, 1000)
     expr_p = [20*math.exp(6*(1-math.exp(-0.05*t))) for t in expr_t]
     plt.plot(expr_t,expr_p,label = 'Experiment-fitted' )

     plt.title('Growth of wing disc area')
     plt.yscale('log')
     plt.xlabel('Time [h]')
     plt.ylabel('Wing disc area [um^2]')
     plt.title('Trend of wing disc area')
     
     x1,x2,y1,y2 = plt.axis()
     plt.axis((timeBegin,timeEnd,y1,y2))
     plt.legend(loc='lower right' )

def plotLenSeq(statSeq,interval = 1,shrinkRatio = 0.032):
     tVec = []
     lVec = []
     i = 0
     for frame in statSeq:
          length = obtainmaxLen(frame) 
          lVec.append(length)
          tVec.append(i)
          i = i+interval
     tVec = [t*shrinkRatio for t in tVec]
     ax = plt.subplot(223)
     beginIndx = int(beginFrame/interval)
     plt.plot(tVec[beginIndx:],lVec[beginIndx:],label = 'Simulation' )
     
     expr_t = np.linspace(timeBegin, timeEnd, 1000)
     expr_p = [0.1*math.exp(6*(1-math.exp(-0.05*t))) for t in expr_t]
     plt.plot(expr_t,expr_p,label = 'Experiment-fitted' )

     plt.title('Growth of wing disc length')
     plt.yscale('log')
     plt.xlabel('Time [h]')
     plt.ylabel('Wing disc length [um]')
     plt.title('Trend of wing disc length')
     
     x1,x2,y1,y2 = plt.axis()
     plt.axis((timeBegin,timeEnd,y1,y2))
     plt.legend(loc='lower right' )

def plotDenSeq(statSeq,interval = 1,shrinkRatio = 0.032):
     tVec = []
     dVec = []
     i = 0
     for frame in statSeq:
          area = obtainDiscArea(frame)
          num = len(frame.stats)
          den = num/area/12
          dVec.append(den)
          tVec.append(i)
          i = i+interval
     tVec = [t*shrinkRatio for t in tVec]
     ax = plt.subplot(224)
     beginIndx = int(beginFrame/interval)
     plt.plot(tVec[beginIndx:],dVec[beginIndx:],label = 'Simulation' )
     
     expr_t = np.linspace(timeBegin, timeEnd, 1000)
     expr_p = [0.04*math.log2(0.3*(t+4)) for t in expr_t]
     plt.plot(expr_t,expr_p,label = 'Experiment-fitted')

     plt.title('Change of wing disc density')
     plt.xlabel('Time [h]')
     plt.ylabel('Cell density [1/um^2]')
     plt.title('Trend of wing disc cell density')
     
     x1,x2,y1,y2 = plt.axis()
     plt.axis((timeBegin,timeEnd,y1,y2))
     plt.legend(loc='lower right' )


plotCellCtSeq(sequence,interval = interval)
plotAreaSeq(sequence,interval = interval)
plotLenSeq(sequence,interval = interval)
plotDenSeq(sequence,interval = interval)
plt.show()
