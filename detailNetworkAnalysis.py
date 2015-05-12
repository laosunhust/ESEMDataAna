from detailDataProcess import *

def obtainNonBdryNodeList(gr):
    nodeVec = []
    degrVec = []
    for n,d in gr.nodes_iter(data=True):
        if(d['bdry'] == False):
            nodeVec.append(n)
            degrVec.append(d['ngbr'])
    return (nodeVec,degrVec)

statSeq = readSimuStat("./data/dataOutput/detailedStatE*")
sequence = statSeq.sequence
lastFrame = sequence[-1].stats         
Gr = fetchNetwork(lastFrame)
pos=nx.get_node_attributes(Gr,'pos')
ngbrCtVec = nx.get_node_attributes(Gr,'ngbr')
ngbrDegrees = list(map(int, ngbrCtVec.values()))
nodelistVec = nx.get_node_attributes(Gr,'bdry')
nodeList = list(map(bool, nodelistVec.values()))
print(nodelistVec)
print(ngbrDegrees)
nonBdryList = []
for i in range(len(nodeList)):
    if(nodeList[i] == True):
        nonBdryList.append(i+1)
print(nonBdryList)
#nonBdryList = obtainNonBdryNodeList(Gr)
nodeVec,degrVec = obtainNonBdryNodeList(Gr)
#print(theList)
#nx.draw(Gr,pos,node_color=ngbrDegrees,
#        node_cmap=plt.get_cmap('jet'),
#        nodelist = nonBdryList,
#        with_labels=True)
nx.draw(Gr,pos,nodelist = nodeVec,
        node_color=degrVec,
        node_cmap=plt.get_cmap('jet'),
        with_labels=True)
plt.show()
