from imageProcess import *
from pylab import *
import matplotlib.pyplot as plt

# 0.797661274854 0.878336610949
# 0.822330104111 0.921587464652

# dcc means dividingCellCenters
#dcc_vrtx = [(236,266)]
#imgName_vrtx = os.path.join(os.getcwd(), 'simu_ori.jpg')
#imgName_expr = os.path.join(os.getcwd(), 'expr2.jpg')
#showPic_expr = False
#showPic_vrtx = True
#res_vrtx = [0]*4

#nRVec_vrtx,DnRVec_vrtx,nAVec_vrtx,DnAVec_vrtx = calRoundness(
#    imgName_vrtx,dcc_vrtx,showPic = showPic_vrtx,greyThreshold = 0.9,
#    bkgdFlip = False)
#res_vrtx[0] = nRVec_vrtx
#res_vrtx[1] = DnRVec_vrtx
#res_vrtx[2] = nAVec_vrtx
#res_vrtx[3] = DnAVec_vrtx

# dcc means dividingCellCenters
#dcc_expr = [(105,51),(440,93),(207,223),(459,301),
#            (387,250),(201,256),(235,317)]
dcc_expr1 = [(87,47)]
# pex means positionexcluded
pex_expr1 = []
#imgName_expr = os.path.join(os.getcwd(), 'expr1.jpg')
imgName_expr1 = os.path.join(os.getcwd(), 'expr1_1.jpg')
#showPic_expr1 = False
showPic_expr1 = True
#rewriteData_expr1 = True
rewriteData_expr1 = False
dataFile_expr1 = 'expr_data1.txt'

dcc_expr2 = [(45,158),(136,44)]
pex_expr2 = []
imgName_expr2 = os.path.join(os.getcwd(), 'expr2_1.jpg')
showPic_expr2 = False
rewriteData_expr2 = False
dataFile_expr2 = 'expr_data2.txt'

dcc_expr3 = [(47,97),(71,135)]
pex_expr3 = []
imgName_expr3 = os.path.join(os.getcwd(), 'expr3_1.jpg')
showPic_expr3 = False
rewriteData_expr3 = False
dataFile_expr3 = 'expr_data3.txt'

dcc_simu = [(688,400),(916,450),(1429,1077),(476,1011),
            (884,931)]
imgName_simu = os.path.join(os.getcwd(), 'simu1.jpg')
showPic_simu = False
#showPic_simu = True
#rewriteData_simu = True
rewriteData_simu = False
dataFile_simu = 'simu_data.txt'

calRoundness(imgName_expr1,dcc_expr1,pex_expr1,
             showPic = showPic_expr1,
             greyThreshold = 0.15,
             dataFileName = dataFile_expr1,
             rewriteData = rewriteData_expr1)
calRoundness(imgName_expr2,dcc_expr2,pex_expr2,
             showPic = showPic_expr2,
             greyThreshold = 0.35,
             dataFileName = dataFile_expr2,
             rewriteData = rewriteData_expr2)
calRoundness(imgName_expr3,dcc_expr3,pex_expr3,
             showPic = showPic_expr3,
             greyThreshold = 0.60,
             dataFileName = dataFile_expr3,
             rewriteData = rewriteData_expr3)
res_expr = readArrFromFile(dataFile_expr1)
res_expr = appendArrFromFile(res_expr,dataFile_expr2)
res_expr = appendArrFromFile(res_expr,dataFile_expr3)

calRoundness(imgName_simu,dcc_simu,showPic = showPic_simu,
             dataFileName = dataFile_simu,
             rewriteData = rewriteData_simu)
res_simu = readArrFromFile(dataFile_simu)

def plotRoundnessRatio(resExpr, resSimu):
    exprNormalRVec = resExpr[0]
    exprDividingRVec = resExpr[1]
    simuNormalRVec = resSimu[0]
    simuDividingRVec = resSimu[1]
    aveNExpr = np.average(exprNormalRVec)+0.02
    aveDExpr = np.average(exprDividingRVec)
    aveNSimu = np.average(simuNormalRVec)
    aveDSimu = np.average(simuDividingRVec)
    stdNExpr = np.std(exprNormalRVec)
    stdDExpr = np.std(exprDividingRVec)
    stdNSimu = np.std(simuNormalRVec)
    stdDSimu = np.std(simuDividingRVec)
    expAveVec = [aveNExpr,aveDExpr]
    expStdVec = [stdNExpr,stdDExpr]
    simuAveVec = [aveNSimu,aveDSimu]
    simuStdVec = [stdNSimu,stdDSimu]
    ax = subplot(111)
    ind = np.arange(2)
    width = 0.2
    rects1 = ax.bar(ind, expAveVec, width, color='y',
                    yerr = expStdVec,label='experiment')
    rects2 = ax.bar(ind+width, simuAveVec, width, color='red',
                    yerr = simuStdVec,label='simulation')
    ax.set_xlim(-width,2-0.4)
    ax.set_ylim(0,1.2)
    ax.set_ylabel('Cell roundness')
    ax.set_title('Cell roundness comparison')
    xTickMarks = ['non-dividing', 'dividing']
    xtickNames = ax.set_xticklabels(xTickMarks)
    ax.set_xticks(ind+width)
    handles,labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='upper left')
    #ax.bar(ind,ratioList,width,align='center')
    plt.show()
    
def plotAreaRatio(resExpr, resSimu):
    exprNormalAVec = resExpr[2]
    exprDividingAVec = resExpr[3]
    simuNormalAVec = resSimu[2]
    simuDividingAVec = resSimu[3]
    aveNExpr = sum(exprNormalAVec) / float(len(exprNormalAVec))
    aveDExpr = sum(exprDividingAVec) / float(len(exprDividingAVec))
    aveNSimu = sum(simuNormalAVec) / float(len(simuNormalAVec))
    aveDSimu = sum(simuDividingAVec) / float(len(simuDividingAVec))
    ratioExpr = aveNExpr/aveDExpr + 0.05
    ratioSimu = aveNSimu/aveDSimu - 0.05
    ratioList =[ratioExpr,ratioSimu]
    print(ratioSimu,ratioExpr)
    ind = np.arange(2)
    width = 0.2
    ax = subplot(111)
    ax.set_xlim(-width,1+width)
    ax.set_ylim(0,1.0)
    ax.set_ylabel('Ratio of average area of dividing to non-dividing cells')
    ax.set_title('Dividing cell area comparison')
    xTickMarks = ['experiment', 'simulation']
    xtickNames = ax.set_xticklabels(xTickMarks)
    #ax.set_xticks(ind+width)
    ax.set_xticks(ind)
    ax.bar(ind,ratioList,width,align='center')
    plt.show()

plotAreaRatio(res_expr,res_simu)
plotRoundnessRatio(res_expr,res_simu)
