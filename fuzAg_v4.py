# https://colab.research.google.com/drive/1M_iVpeNAqTlRQGy4gpWjojXpaCLjHHwq#scrollTo=1nIoXo4k-HI5

import networkx as nx
import matplotlib.pyplot as plt
import random
from random import shuffle
import math
import numpy as np
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community import asyn_lpa_communities
from networkx.algorithms.community import label_propagation_communities
from networkx.algorithms.community import asyn_fluidc
from networkx.algorithms.community.quality import coverage
from networkx.algorithms.community.quality import performance
from networkx.algorithms.community.centrality import girvan_newman


# preparing data
g=nx.read_gml('datasets/dolphins.gml',label='id')
# g=nx.karate_club_graph()
# g=nx.fast_gnp_random_graph(8,0.7)
# g=nx.windmill_graph(8,4)
N=len(g)
W=np.zeros((N,N))
for i in g:
    print(i,end="-> ")
    for j in nx.neighbors(g,i):
        print(j,end=" ")
        W[i][j]=1
        W[j][i]=1
    print()

# networkx community detection

gmc = list(greedy_modularity_communities(g))
alc=list(asyn_lpa_communities(g))
lpac=list(label_propagation_communities(g))
asfl=list(asyn_fluidc(g,3))


# inititalization
anchorList=set([])
U={}
U[N]=np.zeros(N)
randomFirstAnchor=random.randint(0,N-1)
anchorList.add(randomFirstAnchor)
U[randomFirstAnchor]=np.zeros(N)
phi=0.25
itermax=15
K=1
adjacentNodes={}
for i in range(N):
    tmp=[]
    for j in range(N):
        if W[i][j]==1:
            tmp.append(j)
    adjacentNodes[i]=np.array(tmp)

# data storage for each iteration
membershipOfAllNodesWithAllAnchors=np.zeros(N)
VN={}
setOfAllVitalNodes=set([])

def fixSetOfAllVitalNodes():
    tmp=set([])
    for i in anchorList:
        for j in VN[i]:
            tmp.add(j)
    for i in tmp:
        setOfAllVitalNodes.add(i)
    # print("setOfAllVitalNodes",setOfAllVitalNodes)

def sumOfMembershipWithAllCommunties(node):
    ret=0
    for i in anchorList:
        ret+=U[i][node]
    membershipOfAllNodesWithAllAnchors[node]=ret

def vitalNodes(anchor):
    ret=[]
    for i in range(N):
        if W[anchor][i]>0:
            ret.append(i)
            continue
        if U[anchor][i]>membershipOfAllNodesWithAllAnchors[i]-U[anchor][i]:
            ret.append(i)
    VN[anchor]=np.array(ret)

def calculateMembership(node,anchor):
    nieghborsOfThisNode=adjacentNodes[node]
    vitalNodesOfThisAnchor=VN[anchor]
    commonNodes=np.intersect1d(nieghborsOfThisNode,vitalNodesOfThisAnchor)
    numr=0
    for i in commonNodes:
        numr+=W[i][node]
    denmr=0
    for i in nieghborsOfThisNode:
        denmr+=W[i][node]
    if denmr==0:
        return 0
    else:
        return (numr/denmr)

# calculate self membership
def selfMembership(node):
    # print("setOfAllVitalNodes",setOfAllVitalNodes)

    numr=0
    allNodes=[i for i in range(0,N)]
    allNodes=np.array(allNodes)
    # independentNodes=np.array(np.setdiff1d(allNodes,setOfAllVitalNodes))
    independentNodes=[]
    for i in allNodes:
        if i not in setOfAllVitalNodes:
            independentNodes.append(i)
    # print("independent",independentNodes)
    # print("setOfAllVitalNodes",setOfAllVitalNodes)
    neighbours=adjacentNodes[node]
    commonNodes=np.intersect1d(independentNodes,neighbours)
    for i in commonNodes:
	       numr+=(W[i][node])
    denmr=0
    for j in adjacentNodes[node]:
        denmr+=(W[j][node])
    if(denmr==0):
        return 0
    return numr/denmr

# new anchors to be added
def newAnchors():
    ret=[]
    for i in range(N):
        if i not in anchorList:
            if U[N][i]>=membershipOfAllNodesWithAllAnchors[i]:
                ret.append(i)
    return np.array(ret)

def addAnchor(anchor):
    anchorList.add(anchor)
    U[anchor]=np.zeros(N)

def removeAnchor(anchor):
    anchorList.remove(anchor)
    del U[anchor]

def identifyFalseAnchor(anchor):
    flag=0
    for i in U[anchor]:
        if i>=phi:
            flag=1
            break
    if flag==1:
        return False
    else:
        print("false anchor",anchor,end=" ")
        return True

def identifyRedundantAnchor(anchor):
    setOfAllVitalNodesExceptThisAnchor=set([])
    for i in anchorList:
        if i!=anchor:
            for j in VN[i]:
                setOfAllVitalNodesExceptThisAnchor.add(j)
    setOfAllVitalNodesExceptThisAnchor=list(setOfAllVitalNodesExceptThisAnchor)
    intersection=np.intersect1d(VN[anchor],setOfAllVitalNodesExceptThisAnchor)
    if len(intersection)==len(VN[anchor]):
        print("redundant anchor",anchor,end=" ")
        return True
    else:
        return False

def normalize():
    for i in range(N):
        tsum=0
        for j in U:
            tsum+=U[j][i]
        if tsum==0:
            continue
        for j in U:
            U[j][i]=U[j][i]/tsum

def evalauteMatrix():
    for i in anchorList:
        for j in range(N):
            U[i][j]=calculateMembership(j,i)
    for i in range(N):
        U[N][i]=selfMembership(i)
    normalize()

def precompute():
    # precomputation of data
    for i in anchorList:
        vitalNodes(i)
    fixSetOfAllVitalNodes()
    for i in range(N):
        sumOfMembershipWithAllCommunties(i)
        print(membershipOfAllNodesWithAllAnchors[i],end=" ")
    print("VN")
    print(VN)

# main working Loop
rflag=1
aflag=1
iterVal=0
while(1):
    iterVal+=1
    print("ITERATION:",iterVal)
    trflag=0
    taflag=0

    precompute()

    evalauteMatrix()
    precompute()
    print(U)
    if iterVal>=itermax:
        break
    if aflag==0 and flag==0:
        break
    anchorsToBeRemoved=[]
    for i in anchorList:
        if identifyFalseAnchor(i) or identifyRedundantAnchor(i):
            anchorsToBeRemoved.append(i)
    print("removing anchors->",anchorsToBeRemoved)
    if len(anchorsToBeRemoved)>0:
        for i in anchorsToBeRemoved:
            removeAnchor(i)

        evalauteMatrix()
        precompute()
        rflag=1
    else:
        rflag=0

    anchorsToBeAdded=newAnchors()
    print("adding anchors->",anchorsToBeAdded)
    if len(anchorsToBeAdded)>0:
        aflag=1
        for i in anchorsToBeAdded:
            addAnchor(i)
    # print(U)





finalCommunities={}
for i in U:
	print(i,U[i])

for i in range(N):
	mx=0
	for j in anchorList:
		mx=max(mx,U[j][i])
	probableCommunities=[]
	for j in anchorList:
		if(U[j][i]==mx):
			probableCommunities.append(j)
	selectedAnchorIndex=random.randint(0,len(probableCommunities)-1)
	selectedAnchor=probableCommunities[selectedAnchorIndex]
	if selectedAnchor not in finalCommunities:
		finalCommunities[selectedAnchor]=[i]
	else:
		finalCommunities[selectedAnchor].append(i)
print("gmc",gmc)
print("alc",alc)
print("lpac",lpac)
print("async_fluidc",asfl)
print("FuzAg Communties")
for i in finalCommunities:
    for j in finalCommunities[i]:
        print(j,end=" ")
    print()
listOfFinalCommunties=[]
for i in finalCommunities:
	listOfFinalCommunties.append(finalCommunities[i])

coverageOfFuzAg=coverage(g,listOfFinalCommunties)
print("coverage Of FuzAg",coverageOfFuzAg)
print("coverage of greedy_modularity_communities",coverage(g,gmc))
print("coverage of async_lpa_communities",coverage(g,alc))
print("coverage of label_propagation_communities",coverage(g,lpac))
print("coverage of Async Fluid Communties",coverage(g,asfl))
