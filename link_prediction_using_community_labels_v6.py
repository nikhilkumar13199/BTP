import networkx as nx
import random
import math
import numpy as np
import sklearn

from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community import asyn_lpa_communities
from networkx.algorithms.community import label_propagation_communities
from networkx.algorithms.community import asyn_fluidc
# from google.colab import drive
from sklearn.metrics import confusion_matrix
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
def Union(lst1, lst2): 
    final_list = list(set(lst1) | set(lst2)) 
    return final_list
def lps_for_different_community(i,j,negihbour,community_nodes,community_labels2,list_of_lp_score,edge_between_community,edge_in_community):
	lp_score=0.0
	total=len(negihbour[i])+len(negihbour[j])+1
	inter1=len(np.intersect1d(np.asarray(negihbour[i]),np.asarray(community_nodes[j])))
	inter2=len(intersection(negihbour[j],community_nodes[i]))
	total=(inter1+inter2)/total	
	x=edge_between_community[community_labels2[i]][community_labels2[j]]
	y=1
	y=y+edge_in_community[community_labels2[i]]+edge_in_community[community_labels2[j]]
	if y==0:
		total=0
	else:
		x=x/y
	total=total*x
	p=Union(negihbour[i],negihbour[j])
	q=intersection(negihbour[i],negihbour[j])
	if(len(p)==0):
		total=0
	else:
		total=total*((len(q))/len(p))
	list_of_lp_score_different_community.append((total,i,j))
	return 0
def lps_for_same_community(i,j,negihbour,community_labels2,N,vertex,list_of_lp_score_same_community,nodes_in_community):
	nx=negihbour[i]
	ny=negihbour[j]
	c=nodes_in_community[community_labels2[i]]
	m1=len(intersection(intersection(nx,ny),c))
	m2=len(intersection(c,Union(nx,ny)))
	m1=m1/m2
	n1=len(intersection(intersection(nx,ny),list(np.setdiff1d(np.asarray(vertex),np.asarray(c)))))
	n2=len(intersection(Union(nx,ny),list(np.setdiff1d(np.asarray(vertex),np.asarray(c)))))
	if(n2==0):
		n1=1
	else:
		n1=n1/n2
	lps=n1*m1
	list_of_lp_score_same_community.append((lps,i,j))
	return 0
def accuracy_by_jaccard(negihbour,Is_edges_exist,N,deletedEdgesList1):
	lucas_predicted_edge_lps=[]
	for i in range(N):
		for j in range(i+1,N):
			if Is_edges_exist[i][j]==0:
				p=Union(negihbour[i],negihbour[j])
				q=intersection(negihbour[i],negihbour[j])
				total=1
				if(len(p)==0):
					total=0
				else:
					total=total*((len(q))/len(p))
				lucas_predicted_edge_lps.append((total,i,j))
	sorted(lucas_predicted_edge_lps,reverse=True)
	lucas_predicted_edge=[]
	phi=len(deletedEdgesList1)/(len(lucas_predicted_edge_lps))
	for i in range(len(deletedEdgesList1)):
		lucas_predicted_edge.append((lucas_predicted_edge_lps[i][1],lucas_predicted_edge_lps[i][2]))
	print(len(lucas_predicted_edge))
	cnt=len(intersection(deletedEdgesList1,lucas_predicted_edge))
	accuracyj=(cnt/len(deletedEdgesList1))*100
	print("(absolute_accuracy*100) of by jaccard coficient ",accuracyj)

def accuracy_by_adamic_adar(negihbour,N,Is_edges_exist,deletedEdgesList1):
	adamic_adar_predicted_edge_lps=[]
	for i in range(N):
		for j in range(i+1,N):
			if Is_edges_exist[i][j]==0:
				p=intersection(negihbour[i],negihbour[j])
				x=0
				for k in p:
					temp=math.log(len(negihbour[k]),2)
					if(temp<=0):
						x=x
					else:
						x=x+1/temp
				adamic_adar_predicted_edge_lps.append((x,i,j))
	sorted(adamic_adar_predicted_edge_lps,reverse=True)
	adamic_adar_predict_edge=[]
	phi=len(deletedEdgesList1)/(len(adamic_adar_predicted_edge_lps))
	for i in range(int(math.ceil(len(adamic_adar_predicted_edge_lps)*phi))):
		adamic_adar_predict_edge.append((adamic_adar_predicted_edge_lps[i][1],adamic_adar_predicted_edge_lps[i][2]))
	cnt1=len(intersection(deletedEdgesList1,adamic_adar_predict_edge))
	accuracy_aa=(cnt1/len(deletedEdgesList1))*100
	print("(absolute_accuracy*100) of by adamic adar coficient ",accuracy_aa)
def accuracy_by_preferential_attach(negihbour,N,Is_edges_exist,deletedEdgesList1):
	preferential_attach_predicted_edge_lps=[]
	for i in range(N):
		for j in range(i+1,N):
			if Is_edges_exist[i][j]==0:
				preferential_attach_predicted_edge_lps.append((0,i,j))
	sorted(preferential_attach_predicted_edge_lps,reverse=True)
	preferential_attach_predicted_edge=[]
	phi=len(deletedEdgesList1)/(len(preferential_attach_predicted_edge_lps))
	for i in range(int(math.ceil(len(preferential_attach_predicted_edge_lps)*phi))):
		preferential_attach_predicted_edge.append((preferential_attach_predicted_edge_lps[i][1],preferential_attach_predicted_edge_lps[i][2]))
	cnt=len(intersection(deletedEdgesList1,preferential_attach_predicted_edge))
	accuracy_pa=(cnt/len(deletedEdgesList1))*100
	print("(absolute_accuracy*100) of by preferential attach coficient ",accuracy_pa)

# drive.mount('/content/drive')
Graph=nx.read_gml('netscience.gml',label='id')
# Graph=nx.karate_club_graph()
# Graph=nx.read_gml('dolphins.gml',label='id')
# Graph=nx.read_gml('netscience.gml',label='id')
N=len(Graph)
print(N)
community_list_gmc=list(greedy_modularity_communities(Graph))
community_labels={}
for i in range(len(community_list_gmc)):
    for j in community_list_gmc[i]:
        community_labels[j]=i+1

# # print(community_labels)
# print(nx.info(Graph))
# # Preparing test and train data in 20-80 ratio respectively by deleting 20% of edges
# # print(Graph.edges())
edgesCount=len(Graph.edges())
listOfEdges=np.asarray(Graph.edges())
numberedList=[]
for i in range(edgesCount):
    numberedList.append(i)
# print(edgesCount)
deletedEdgesIdx=np.random.choice(numberedList,size=int(0.2*edgesCount),replace=False)
deletedEdgesIdx.sort()
# # print(deletedEdgesIdx)
deletedEdgesList=[]
for i in deletedEdgesIdx:
    deletedEdgesList.append(listOfEdges[i])
for i in deletedEdgesList:
    Graph.remove_edge(i[0],i[1])
deletedEdgesList1=[]
for i in deletedEdgesList:
	sorted(i)
	deletedEdgesList1.append((i[0],i[1]))

listOfEdges1=np.asarray(Graph.edges())
Is_edges_exist=[]
for i in range(N+10):
	a=[]
	for j in range(N+10):
		a.append(0)
	Is_edges_exist.append(a)
for i in listOfEdges1:
	Is_edges_exist[i[0]][i[1]]=1
	Is_edges_exist[i[1]][i[0]]=1
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
# list that contain total vertex
vertex=[]
for i in range(N):
	vertex.append(i)
#community formed after we delete 20% edeges
community_list_gmc2=list(greedy_modularity_communities(Graph))
# community_nodes contain node which lies in community of each node i
# print(len(community_list_gmc2))
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
# it contain comunity i,j have how many commen edges
edge_between_community=[]
no_of_community=len(community_list_gmc2)
print(no_of_community)
for i in range(no_of_community+10):
	a=[]
	for j in range(no_of_community+10):
		a.append(0)
	edge_between_community.append(a)
# these list contain lps when same community or different community
# it contain number of edge in a community
edge_in_community=[]
for i in range(no_of_community+10):
	edge_in_community.append(0)
for i in listOfEdges1:
	x=community_labels2[i[0]]
	y=community_labels2[i[1]]
	if(x==y):
		edge_in_community[x]+=1
		edge_between_community[x][x]+=1
	else:
		edge_between_community[x][y]+=1
		edge_between_community[y][x]+=1
list_of_lp_score_different_community=[]
list_of_lp_score_same_community=[]
nodes_in_community=[]
for i in range(no_of_community+10):
	nodes_in_community.append([])
for i in range(N):
	x=community_labels2[i]
	nodes_in_community[x].append(i)
for i in range(N):
	for j in range(i+1,N):
		if Is_edges_exist[i][j]==0 and Is_edges_exist[j][i]==0 and community_labels2[i]!=community_labels2[j]:
			lps_for_different_community(i,j,negihbour,community_nodes,community_labels2,list_of_lp_score_different_community,edge_between_community,edge_in_community)
		if Is_edges_exist[i][j]==0 and Is_edges_exist[j][i]==0 and community_labels2[i]==community_labels2[j]:
			lps_for_same_community(i,j,negihbour,community_labels2,N,vertex,list_of_lp_score_same_community,nodes_in_community)
sorted(list_of_lp_score_different_community,reverse=True)
sorted(list_of_lp_score_same_community,reverse=True)
phi=len(deletedEdgesList1)/(len(list_of_lp_score_same_community)+len(list_of_lp_score_different_community))
print("phi ",phi)
x=math.ceil(len(list_of_lp_score_different_community)*phi)
y=math.ceil(len(list_of_lp_score_same_community)*phi)
predicted_edge=[]
for i in range(int(x)):
	predicted_edge.append((list_of_lp_score_different_community[i][1],list_of_lp_score_different_community[i][2]))
for i in range(int(y)):
	predicted_edge.append((list_of_lp_score_same_community[i][1],list_of_lp_score_same_community[i][2]))
total_delete_edge=len(deletedEdgesList1)
total_number_of_possible_edges=(N*(N-1))/2
cnt=0
cnt=len(intersection(deletedEdgesList1,predicted_edge))
print("total number of deleted edges----->",len(deletedEdgesList1))
print("total number of lps scores-------->",len(list_of_lp_score_different_community)+len(list_of_lp_score_same_community))
print("total number of predicted edges--->",len(predicted_edge))
print("total number of correct pred------>",cnt)
random_accuracy=total_delete_edge/(total_number_of_possible_edges-edgesCount+total_delete_edge)
print("random pred accuracy-------------->",random_accuracy)
accuracy=((cnt)/total_delete_edge)*100
print("absolute accuracy----------------->",accuracy)

accuracy_by_jaccard(negihbour,Is_edges_exist,N,deletedEdgesList1)
accuracy_by_adamic_adar(negihbour,N,Is_edges_exist,deletedEdgesList1)
accuracy_by_preferential_attach(negihbour,N,Is_edges_exist,deletedEdgesList1)
print("factor improvement over random---->",accuracy/random_accuracy)