import math
import matplotlib.pyplot as plt
from pylab import * 
import numpy as np
from detailDataRead import readSimuStat
from detailGrowthProcess import *

folder = 'J:/aniFiles/txt/'
fileName = 'deStat_N01G02_'
interval = 50
#beginFrame = 1093
beginFrame = 0

timeBegin = 0
timeEnd = 80
seqVec = [500,1000,2000]

statSeq = readSimuStat(folder,fileName,interval)
sequence = statSeq.sequence

def plotFrameAreaRelation(frame):
     memVec,areaVec = obtainMemLenVec(frame)
     plt.scatter(areaVec,memVec)
     fit = polyfit(areaVec,memVec,1)
     fit_fn = poly1d(fit)
     plt.plot(areaVec,fit_fn(areaVec),label = 'linear fitting',
              color='green')
     plt.axis((0,1.1,0,200))
     plt.xticks(fontsize = 20)
     plt.yticks(fontsize = 20)
     plt.title('Change of wing disc density')
     plt.xlabel('Cell area (um^2)')
     plt.ylabel('number of membrane elements')
     #plt.title('')
     plt.legend(loc='lower right' )
     plt.show()

def plotFrameSeqArea(statSeq,interval = 1,seqVec = []):
     for seq in seqVec:
          seq_m = int(seq/interval)
          frame = statSeq[seq_m]
          plotFrameAreaRelation(frame)

plotFrameSeqArea(sequence,interval = interval,seqVec =seqVec)
