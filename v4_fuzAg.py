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

# Graph=nx.karate_club_graph()
# Graph=nx.read_gml('datasets/dolphins.gml',label='id')
Graph=nx.fast_gnp_random_graph(25,0.7)
# Graph=nx.windmill_graph(8,4)

# sizes = [5, 5, 10]
# probs = [[0.05, 0.05, 0.02],
#          [0.05, 0.15, 0.07],
#          [0.02, 0.07, 0.04]]
# Graph = nx.stochastic_block_model(sizes, probs, seed=0)

gmc = list(greedy_modularity_communities(Graph))
alc=list(asyn_lpa_communities(Graph))
lpac=list(label_propagation_communities(Graph))
asfl=list(asyn_fluidc(Graph,3))
girvanNewmanCommunities=list(girvan_newman(Graph))
W2=np.zeros((len(Graph),len(Graph)))
for i in Graph:
	for j in nx.neighbors(Graph,i):
		W2[i][j]=1;
		W2[j][i]=1;
for i in range(len(Graph)):
	print(i,end="->")
	for j in range(len(Graph)):
		if(W2[i][j]==1):
			print(j,end=" ")
	print()
W=W2

# threshold value for acquiring membership of a particular community
phi=0.25

# maximum number of iterations
itermax=15

# Total Number of Nodes
N=len(Graph)

# Current Number of Communities
K=1

# adjacency matrix Wij, weight of edge connecting node i and j
# N=30
# W=np.zeros((N,N))
# # src=np.random.choice(N,5,replace=False)
# # dest=np.random.choice(N,5,replace=False)
# for i in range(N):
# 	dest=np.random.choice(N,2)
# 	for j in dest:
# 		if i!=j:
# 			W[i][j]=1
# 			W[j][i]=W[i][j];

# print(W)
for i in range(N):
	print("Nodes adjacent to",i,"are: ",end="")
	for j in range(N):
		if(W[i][j]>0):
			print(j,W[i][j],end="; ")
	print()

# Partitioning Matrix (Python Dictionary)
U={}

U[N+1]=np.zeros(N)

# anchorList
anchorList=set({})


# Returns a random vertex as the first anchor
def randomFirstAnchor(numberOfNodes):
	randomVertex=random.randrange(0,numberOfNodes,1)
	# anchorList.add(randomVertex)
	addAnchor(randomVertex)

# Returns set of adjacent nodes for a node
def adjacentNodes(node):
	adjacentNodesList=[]
	# print(node)
	for i in range(0,len(W[node])):
		if(W[node][i]>0):
			adjacentNodesList.append(i)
	return np.asarray(adjacentNodesList)

# returns sum of membership degree with remaining anchors
def sumOfMembershipWithRemainingCommunities(currentNode,anchorNode):
	# print("Calculating Sum of Membership with remaining communities excpet Anchor ",anchorNode)
	val=0
	# print(U)
	for i in U:
		if(i!=anchorNode and i!=N+1):
			# print("AnchorNode-> ",i," CurrentNode-> ",currentNode)
			val+=U[i][currentNode]
	return val


# return list of vital nodes for a community
def vitalNodes(anchorNode):
	vitalNodesList=adjacentNodes(anchorNode)
	# print("Adjacent Nodes of AnchorNode",anchorNode,": ",vitalNodesList)
	for i in range(0,N):
		if i not in vitalNodesList and i!=anchorNode:
			if(U[anchorNode][i]>=sumOfMembershipWithRemainingCommunities(i,anchorNode)):
				# vitalNodesList.append(i)
				np.concatenate([vitalNodesList,[i]])
	return np.asarray(vitalNodesList)


# return list of nodes common between vitalnodes and adjacent nodes of a given node
def commonVitalAdjacentNodes(givenNode,anchorNode):
	neighbours=adjacentNodes(givenNode)
	currentVitalNodes=vitalNodes(anchorNode)
	return np.intersect1d(neighbours,currentVitalNodes)



# Calculate all membership values of nodes with respect to the current anchors
def calculateMembership(node,community):
	numr=0
	for i in commonVitalAdjacentNodes(node,community):
		numr+=(W[i][node])
	denmr=0
	# print(node," -> ",adjacentNodes(node))
	for j in adjacentNodes(node):
		denmr+=(W[j][node])
	if(denmr==0):
		return 0
	return numr/denmr

# return list of all independent nodes
def independentNodes():
	listOfAllNodes=[i for i in range(0,N)]
	npArrayOfAllNodes=np.array(listOfAllNodes)
	npArrayOfAllVitalNodes=allVitalNodes()
	ret=np.setdiff1d(npArrayOfAllNodes,np.intersect1d(npArrayOfAllNodes,npArrayOfAllVitalNodes))
	# print("independentNodes",ret)
	return ret


# calculate self membership
def selfMembership(node):
	numr=0
	allIndependentNodes=independentNodes()
	neighbours=adjacentNodes(node)
	commonNodes=np.intersect1d(allIndependentNodes,neighbours)
	for i in commonNodes:
		numr+=(W[i][node])
	denmr=0

	for j in adjacentNodes(node):
		denmr+=(W[j][node])
	if(denmr==0):
		return 0
	return numr/denmr

# identify new anchors
def newAnchors():
	listOfNewAnchors=[]
	oldAnchorList=[]
	for i in anchorList:
		oldAnchorList.append(i)
	# print("oldAnchorList-> ",oldAnchorList)
	for i in range(N):
		sumOfMembershipWithAllCommunties=0
		for j in oldAnchorList:
			# print("oldAnchor-> ",j)
			sumOfMembershipWithAllCommunties+=U[j][i]
		# print("Node-> ",i," Self membership-> ",U[N+1][i],"Membership at others",sumOfMembershipWithAllCommunties)
		if(U[N+1][i]>=sumOfMembershipWithAllCommunties):
			listOfNewAnchors.append(i)
			anchorList.add(i)
	return np.asarray(listOfNewAnchors)

# list of all Vital Nodes of any anchor
def allVitalNodes():
	setOfAllVitalNodes=set({})
	for i in anchorList:
		for j in vitalNodes(i):
			setOfAllVitalNodes.add(j)
	return np.asarray(list(setOfAllVitalNodes))

# set of all vital nodes of all anchors except this anchors
def allVitalNodesMinusThisAnchor(anchor):
	setOfAllVitalNodesExceptThisAnchor=set({})
	# print("anchor",anchor)
	for i in anchorList:
		if i!=anchor:
			for j in vitalNodes(i):
				setOfAllVitalNodesExceptThisAnchor.add(j)
	return list(setOfAllVitalNodesExceptThisAnchor)


# identify redundant anchor
def identifyRedundantAnchor(anchorNode):
	listOfVitalNodes=vitalNodes(anchorNode)
	flag=0
	setOfAllVitalNodes=np.array(allVitalNodesMinusThisAnchor(anchorNode))
	# print("All vital Nodes except ",anchorNode, " Node",setOfAllVitalNodes)
	# print("List of All Vital Nodes of ",anchorNode," -> ",listOfVitalNodes)
	intersection=np.intersect1d(listOfVitalNodes,setOfAllVitalNodes)
	if(len(intersection)<len(listOfVitalNodes)):
		# not redundant anchor
		return False
	else:
		# redundant anchor identified
		# print("Identified redundant anchor-> ",anchorNode)
		return True

# identify false anchor
def identifyFalseAnchor(anchorNode):
	flag=0
	for i in U[anchorNode]:
		if i>=phi:
			flag=1
			break
	if(flag==1):
		# not False Anchor
		return False
	else:
		# False Anchor Identified
		# print("Identified False Anchor-> ",anchorNode)
		return True

# remove Anchor
def removeAnchor(anchor):
	anchorList.remove(anchor)
	del U[anchor]

# add Anchor
def addAnchor(anchor):
	anchorList.add(anchor)
	U[anchor]=np.zeros(N)
	# membershipOfNodes=[]
	# for i in range(N):
	# 	membershipOfNodes.append(calculateMembership(i,anchor))
	# U[anchor]=np.array(membershipOfNodes)

# normalize the U
def normalize():
	for i in range(N):
		tsum=0
		for j in U:
			tsum+=U[j][i]
		if tsum==0:
			continue
		for j in U:
			U[j][i]=U[j][i]/tsum


# main working Loop
randomFirstAnchor(N)
# addAnchor(4)
# for i in range(N):
# 	U[N+1][i]=selfMembership(i)
# print(U)
rflag=1
aflag=1
iterVal=0
while(1):
	print("ITERATION:",iterVal)
	iterVal+=1
	trflag=0
	taflag=0
	for i in range(N):
		U[N+1][i]=selfMembership(i)
	for i in range(N):
		for j in anchorList:
			U[j][i]=calculateMembership(i,j)
	normalize()
	# print(U)
	anchorsToBeRemoved=[]
	for i in anchorList:
		if identifyFalseAnchor(i) or identifyRedundantAnchor(i):
			# removeAnchor(i)
			anchorsToBeRemoved.append(i)
			trflag=1
	for i in anchorsToBeRemoved:
		# print("Removing Anchor-> ",i)
		removeAnchor(i)
	# print(U)
	if(trflag==1):
		for i in anchorList:
			tmpList=[]
			for j in range(N):
				tmpList.append(calculateMembership(j,i))
			U[i]=np.array(tmpList)
		# for i in range(N):
		# 	tmpList=[]
		# 	for j in anchorList:
		# 		tmpList.append(calculateMembership(i,j))
		# 	U[j]=np.array(tmpList)
		for i in range(N):
			U[N+1][i]=selfMembership(i)
		for i in range(N):
			for j in anchorList:
				U[j][i]=calculateMembership(i,j)
		normalize()
		# print(U)
		rflag=1
	else:
		rflag=0

	listOfNewAnchors=newAnchors()
	print("Adding Anchors->",listOfNewAnchors)
	if(len(listOfNewAnchors)>0):
		aflag=1
	else:
		aflag=0
	for i in listOfNewAnchors:
		addAnchor(i)
	for i in range(N):
		U[N+1][i]=selfMembership(i)
	for i in range(N):
		for j in anchorList:
			U[j][i]=calculateMembership(i,j)
	normalize()
	if(iterVal>=itermax):
		break
	if(aflag==0 and rflag==0):
		break

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


print()
print("gmc",gmc)
print("alc",alc)
print("lpac",lpac)
print("async_fluidc",asfl)
# print("girvan_newman",girvanNewmanCommunities)
print("FuzAg Communties")
for i in finalCommunities:
	print(i,end="-> ")
	for j in finalCommunities[i]:
		print(j,end=" ")
	print()

listOfFinalCommunties=[]
for i in finalCommunities:
	listOfFinalCommunties.append(finalCommunities[i])
coverageOfFuzAg=coverage(Graph,listOfFinalCommunties)
print("coverage Of FuzAg",coverageOfFuzAg)
print("coverage of greedy_modularity_communities",coverage(Graph,gmc))
print("coverage of async_lpa_communities",coverage(Graph,alc))
print("coverage of label_propagation_communities",coverage(Graph,lpac))
print("coverage of Async Fluid Communties",coverage(Graph,asfl))

performanceOfFuzAg=performance(Graph,listOfFinalCommunties)
print("performance Of FuzAg",performanceOfFuzAg)
print("performance of greedy_modularity_communities",performance(Graph,gmc))
print("performance of async_lpa_communities",performance(Graph,alc))
print("performance of label_propagation_communities",performance(Graph,lpac))
print("performance of Async Fluid Communties",performance(Graph,asfl))
