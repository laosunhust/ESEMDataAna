import math
import matplotlib.pyplot as plt
from pylab import * 
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
seqVec = [1000,1500,2000]

statSeq = readSimuStat(folder,fileName,interval)
sequence = statSeq.sequence

def plotFrameAreaRelation(frame):
     lenVec,areaVec = obtainLenVec(frame)
     plt.scatter(lenVec,areaVec)
     fit = polyfit(lenVec,areaVec,1)
     fit_fn = poly1d(fit)
     plt.plot(lenVec,fit_fn(lenVec),label = 'linear fitting',
              color='green')
     plt.axis((0,1,0,10))
     plt.xticks(fontsize = 20)
     plt.yticks(fontsize = 20)
     plt.title('Change of wing disc cell area')
     plt.xlabel('Relative distance from center')
     plt.ylabel('Cell area (um^2)')
     #plt.title('')
     plt.legend(loc='lower right' )
     plt.show()

def plotFrameSeqArea(statSeq,interval = 1,seqVec = []):
     for seq in seqVec:
          seq_m = int(seq/interval)
          frame = statSeq[seq_m]
          plotFrameAreaRelation(frame)

plotFrameSeqArea(sequence,interval = interval,seqVec =seqVec)
