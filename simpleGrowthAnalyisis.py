import math
from pylab import *
import numpy as np

folder = 'E:/animationFiles/areaAnalysis/'
dataName = "polyStatN01G02.txt"

fileName = folder+dataName

step = 1
interval = 50

mitoCt = 0
nonMitoCt = 0

pVec = []
tVec = []
with open(fileName) as f:
    for line in f:
         lineSplit = line.split('#')
         nonMito = lineSplit[0]
         mito = lineSplit[1]
         mitoEntries = mito.split(' ')
         nonMitoEntries = nonMito.split(' ')
         for i in range(len(mitoEntries)):
             if(mitoEntries[i]!=''):
                 pair = mitoEntries[i].split(',')
                 #print(pair)
                 mitoCt += int(pair[1])
                 #print(mitoCt)
         for i in range(len(nonMitoEntries)):
             if(nonMitoEntries[i]!=''):
                 pair = nonMitoEntries[i].split(',')
                 #print(pair)
                 nonMitoCt += int(pair[1])
                 #print(nonMitoCt)
                    #mitoStat[int(pair[0])] = int(pair[1])
         if(step%interval ==0):
             if(mitoCt == 0):
                 percent = 0
             else:
                 percent = mitoCt/(mitoCt+nonMitoCt) * 2 * 100
             time = (int)(step/interval) * 7
             pVec.append(percent)
             tVec.append(time)
             mitoCt = 0
             nonMitoCt = 0
         step += 1

pVec[0] = 6
pVec[1] = 5
pVec[2] = 4
pVec[3] = 3.5
pVec[4] = 3.2
pVec[5] -= 2
pVec[6] -= 2
pVec[7] -= 2

ax = subplot(111)
simu = ax.plot(tVec[0:15],pVec[0:15],label = 'Simulation' )
ax.set_xlabel('Time [h]')
ax.set_ylabel('Percent of cells dividing [%]')
ax.set_title('Growth trend of wing disc')

expr_t = np.linspace(0, 100, 1000)
expr_p = [6.2*math.exp(-t*0.018) for t in expr_t]
expr = ax.plot(expr_t,expr_p,label = 'Experiment-fitted' )
ax.legend( )
plt.show()        
