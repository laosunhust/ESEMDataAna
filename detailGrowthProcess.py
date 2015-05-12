from detailDataRead import *
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import math

def obtainAllCenter(frameData):
     cellCt = len(frameData.stats)
     xSum = 0
     ySum = 0
     for cellStat in frameData.stats:
          xSum += float(cellStat.center[0])
          ySum += float(cellStat.center[1])
     return (xSum/cellCt,ySum/cellCt)

def obtainmaxLen(frameData):
     cellCt = len(frameData.stats)
     discCenter = obtainAllCenter(frameData)
     centerX = float(discCenter[0])
     centerY = float(discCenter[1])
     maxDist = 0
     for cellStat in frameData.stats:
          pos = cellStat.center
          diffX = float(pos[0]) - centerX
          diffY = float(pos[1]) - centerY
          dist = math.sqrt(diffX*diffX+diffY*diffY)
          if(dist>maxDist):
               maxDist = dist
     return maxDist

def obtainDiscArea(frameData):
     discArea = 0.0
     for cellStat in frameData.stats:
          area = float(cellStat.area)
          discArea += area
     return discArea

def obtainAveDensity(frameData):
     cellCt = len(frameData.stats)
     discArea = obtainDiscArea(frameData)
     return (discArea/float(cellCt))

def obtainLenVec(frameData,divThres = 0.93):
     discCenter = obtainAllCenter(frameData)
     maxDist = obtainmaxLen(frameData)
     centerX = float(discCenter[0])
     centerY = float(discCenter[1])
     lenVec = []
     areaVec = []
     for cellStat in frameData.stats:
          prog = float(cellStat.cellProg)
          if(prog>divThres):
               continue
          bdry = int(cellStat.isBdry)
          if(bdry):
               continue
          pos = cellStat.center
          diffX = float(pos[0]) - centerX
          diffY = float(pos[1]) - centerY
          dist = math.sqrt(diffX*diffX+diffY*diffY)
          area = float(cellStat.area) * 12
          lenVec.append(dist/maxDist)
          areaVec.append(area)
     return (lenVec,areaVec)

def obtainMemLenVec(frameData):
     memVec = []
     areaVec = []
     for cellStat in frameData.stats:
          bdry = int(cellStat.isBdry)
          if(bdry):
               continue
          memCt = float(cellStat.membrCt)
          area = float(cellStat.area)
          memVec.append(memCt)
          areaVec.append(area)
     return (memVec,areaVec)
