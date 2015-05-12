import glob
import os

class CellStat:
     def __init__(self,rank, cellProg, membrProg, isBdry, ngbrCt,
                  area, neighbors, intnlCt, membrCt, center):
         self.rank = rank
         self.cellProg = cellProg
         self.membrProg = membrProg
         self.isBdry = isBdry
         self.ngbrCt = ngbrCt
         self.area = area
         self.neighbors = neighbors
         self.intnlCt = intnlCt
         self.membrCt = membrCt
         self.center = center
     def __str__(self):
         return "cell rank = %s\n\
growth progress = %s\n\
membrane progress = %s\n\
is boundary = %s\n\
number of neighbors = %s\n\
cell are = %s\n\
neighbor list = %s\n\
internal node count = %s\n\
membrane node count = %s\n\
center position = %s\n" %(self.rank,
                          self.cellProg,
                          self.membrProg,
                          self.isBdry,
                          self.ngbrCt,
                          self.area,
                          self.neighbors,
                          self.intnlCt,
                          self.membrCt,
                          self.center)

class CellStatsVec:
    def __init__(self,sTime):
         self.stats =[]
         self.time = sTime
    def addStat(self,statNew):
        self.stats.append(statNew);

class SimuStats:
    def __init__(self):
        self.sequence =[]
    def addFrame(self,statNew):
        self.sequence.append(statNew);

def parseTime(fileName,timePerFrame = 1):
     numPart = fileName[-9:-4]
     frameNum = float(numPart)
     print(frameNum)
     return frameNum*timePerFrame

def strToCellStat(strInputArr):
    i = 0
    dataVec = []
    for i in range(10):
        rawData =(strInputArr[i]).split(':')[1]
        data = rawData.replace('\n','')
        dataVec.append(data)
    dataVec[6] = dataVec[6].replace('{ }','').replace('{ ','').replace(' }','')
    dataVec[6] = filter(lambda x: len(x)>0,dataVec[6].split(' '))
    dataVec[9] = dataVec[9].replace('(','').replace(')','').replace(',',' ')
    dataVec[9] = tuple(dataVec[9].split(' '))
    result = CellStat(dataVec[0],dataVec[1],dataVec[2],dataVec[3],dataVec[4],
                      dataVec[5],dataVec[6],dataVec[7],dataVec[8],dataVec[9])
    #print(result)
    return result

def readStatFile(fileName,linePerCell = 11):
    file = open(fileName, 'r')
    i=0
    strArr = []
    sTime = parseTime(fileName)
    result = CellStatsVec(sTime)
    for line in file:
        if(i%linePerCell == 0):
            strArr = []
        if(i%linePerCell == linePerCell-1):
            cellStat = strToCellStat(strArr)
            result.addStat(cellStat)
        strArr.append(line)
        i = i+1
    return result

def readSimuStat(fileDir,simuNameBase,interval = 1):
    stats = SimuStats()
    os.chdir(fileDir)
    for filename in glob.glob(simuNameBase+"*"):
         #print(filename)
         tmpStr = filename.replace(simuNameBase,'');
         tmpStr = tmpStr.replace('.txt','')
         frameRank = int(tmpStr)
         #print(frameRank)
         if(frameRank%interval==0):
              print(filename)
              frameStat = readStatFile(filename)
              stats.addFrame(frameStat)
    return stats

