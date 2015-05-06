import numpy as np
import matplotlib.pyplot as plt

cellMechData = np.loadtxt("SingleCellMechanics.txt")
exertedForce = []
SLen = []
CLen = []

for stepData in cellMechData:
    forceRank = stepData[0]
    stepNum = stepData[1]
    if(stepNum == 199):
        diffLen = stepData[2]
        if(forceRank<10):
            exertedForce.append(forceRank*0.35);
            SLen.append(diffLen);
        else:
            CLen.append(diffLen);

plt.xlabel('force exerted')
plt.ylabel('cell length along force direction')

SLine = plt.plot(exertedForce[1:], SLen[1:], label="stretch")
CLine = plt.plot(exertedForce[1:], CLen[1:], label="compress")
plt.legend(["streching response", "compression response"],loc=2)
plt.show()
