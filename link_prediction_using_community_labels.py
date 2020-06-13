import networkx as nx
import random
import math
import numpy as np

from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community import asyn_lpa_communities
from networkx.algorithms.community import label_propagation_communities
from networkx.algorithms.community import asyn_fluidc


Graph=nx.read_gml('datasets/dolphins.gml',label='id')
# Graph=nx.karate_club_graph()
N=len(Graph)
community_list_gmc=list(greedy_modularity_communities(Graph))
community_labels={}
for i in range(len(community_list_gmc)):
    for j in community_list_gmc[i]:
        community_labels[j]=i+1

print(community_list_gmc)
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

print(len(Graph.edges()))
print(list(greedy_modularity_communities(Graph)))
community_list_gmc2=list(greedy_modularity_communities(Graph))
community_labels2={}
for i in range(len(community_list_gmc2)):
    for j in community_list_gmc2[i]:
        community_labels2[j]=i+1



# Computing LP scores for all non observed edges
for i in range(N):
    for j in range(N):
        if community_labels2[i]!=community_labels2[j]:
            
