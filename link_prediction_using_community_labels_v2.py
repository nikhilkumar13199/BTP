import networkx as nx
import random
import math
import numpy as np

from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community import asyn_lpa_communities
from networkx.algorithms.community import label_propagation_communities
from networkx.algorithms.community import asyn_fluidc


Graph=nx.read_gml('dolphins.gml',label='id')
# Graph=nx.karate_club_graph()
N=len(Graph)
print(N)
community_list_gmc=list(greedy_modularity_communities(Graph))
community_labels={}
for i in range(len(community_list_gmc)):
    for j in community_list_gmc[i]:
        community_labels[j]=i+1
# print(community_labels)
print(nx.info(Graph))
# Preparing test and train data in 20-80 ratio respectively by deleting 20% of edges
# print(Graph.edges())
edgesCount=len(Graph.edges())
listOfEdges=np.asarray(Graph.edges())
numberedList=[]
for i in range(edgesCount):
    numberedList.append(i)
# print(edgesCount)
deletedEdgesIdx=np.random.choice(numberedList,size=int(0.2*edgesCount),replace=False)
deletedEdgesIdx.sort()
# print(deletedEdgesIdx)
deletedEdgesList=[]
for i in deletedEdgesIdx:
    deletedEdgesList.append(listOfEdges[i])
for i in deletedEdgesList:
    Graph.remove_edge(i[0],i[1])

listOfEdges1=np.asarray(Graph.edges())
Is_edges_exist={}
for i in listOfEdges1:
	Is_edges_exist[(i[0],i[1])]=1
	Is_edges_exist[(i[1],i[0])]=1
negihbour={}
for i in listOfEdges1:
	if i[1] not in negihbour.keys():
	 	negihbour[i[1]]=[]
	 	negihbour[i[1]].append(i[0])
	else:
		negihbour[i[1]].append(i[0])
	if i[0] not in negihbour.keys():
		negihbour[i[0]]=[]
		negihbour[i[0]].append(i[1])
	else:
	 	negihbour[i[0]].append(i[1])
for i in range(N):
	if i not in negihbour.keys():
		negihbour[i]=[]
community_list_gmc2=list(greedy_modularity_communities(Graph))
community_nodes={}
for i in community_list_gmc2:
	for j in i:
		for k in i:
			if k!=j:
				if j not in community_nodes.keys():
					community_nodes[j]=[]
				community_nodes[j].append(k)
for i in range(N):
	if i not in community_nodes.keys():
		community_nodes[i]=[]
community_labels2={}
for i in range(len(community_list_gmc2)):
    for j in community_list_gmc2[i]:
        community_labels2[j]=i+1
list_of_lp_score=[]
for i in range(N):
	for j in range(i+1,N):
		if (i,j) not in Is_edges_exist.keys() and (j,i) not in Is_edges_exist.keys() and community_labels2[i]!=community_labels2[j]:
			lp_score=0.0
			total=len(negihbour[i])+len(negihbour[j])+1
			nx=np.asarray(negihbour[i])
			cj=np.asarray(community_nodes[j]);
			inter1=len(np.intersect1d(nx,cj))
			ny=np.asarray(negihbour[j])
			ci=np.asarray(community_nodes[i])
			inter2=len(np.intersect1d(ny,ci))
			total=(inter1+inter2)/total
			x=0
			y=1
			for k in listOfEdges1:
				if (community_labels2[k[0]]==community_labels2[i] and community_labels2[k[1]]==community_labels2[j]) or (community_labels2[k[1]]==community_labels2[i] and community_labels2[k[0]]==community_labels2[j]):
					x=x+1
				if (community_labels2[k[0]]==community_labels2[i] and community_labels2[k[1]]==community_labels2[i]) or (community_labels2[k[1]]==community_labels2[j] and community_labels2[k[0]]==community_labels2[j]):
					y=y+1
			if y==0:
				total=0
			else:
				x=x/y
			total=total*x
			p=np.union1d(nx,ny)
			q=np.intersect1d(nx,ny)
			if(len(p)==0):
				total=0
			else:
				total=total*((len(q))/len(p))
			list_of_lp_score.append([total,i,j])
			






