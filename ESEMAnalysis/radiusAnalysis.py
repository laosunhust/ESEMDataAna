import numpy as np
import matplotlib.pyplot as plt

cellEquData = np.loadtxt("SingleCellEqu.txt")
meaningfulCount = 200

cellEquData
timeSeq = []
minVal = []
maxVal = []

for stepData in cellEquData:
    timeSeq.append(stepData[0]) 
    minVal.append(stepData[1])
    maxVal.append(stepData[2])

plt.xlabel('time step')
plt.ylabel('distance to center')

minLine = plt.plot(timeSeq[:meaningfulCount], minVal[:meaningfulCount], label="minimum radius")
maxLine = plt.plot(timeSeq[:meaningfulCount], maxVal[:meaningfulCount])
plt.legend(["minumum distance", "maximum distance"])
plt.show()
