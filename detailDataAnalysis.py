from detailDataProcess import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import math

def plotFreqSeq(freqSeq, lastGen):
    typeCt = len(freqSeq)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    freqCMap = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=typeCt)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=freqCMap)
    #print(scalarMap.get_clim())
    #lastCellCount = freqSeq[:,-1]
    #print(lastCellCount)
    #lastGen = len(freqSeq[0])/float(stepPerGen)
    
    for i in range(typeCt):
        #genSeq = np.linspace(0,lastGen,len(freqSeq[i]))
        genSeq = np.linspace(1,lastGen+2,len(freqSeq[i]))
        colorVal = scalarMap.to_rgba(i)
        colorText = ("polygon class: %s"%(i+4))
        ax.plot(genSeq,freqSeq[i], color=colorVal,
                label=colorText)
    handles,labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='upper left')
    ax.grid()
    #plt.axis([1, lastGen, 0, 0.5])
    plt.axis([1, lastGen+2, 0, 0.5])
    plt.xlabel('Generation')
    plt.ylabel('Percentage')
    plt.show()

pos = {}
fileFolder = 'E:/animationFiles/tmp2/'
fileName = 'deStat_N02G03_'
#statSeq = readSimuStat("./data/dataOutput/detailedStatE*")
statSeq = readSimuStat(fileFolder,fileName,4)
#statSeq = readSimuStat("E:/animationFiles/tmp/detailedStatE*")
sequence = statSeq.sequence
#obtainAreaAll(sequence)
freqSeq = obtainFreqSeq(sequence)
lastGen = obtainLastGen(sequence)
plotFreqSeq(freqSeq,lastGen)
#lastFrame = sequence[-50]
#obtainAreaFrame(lastFrame)
