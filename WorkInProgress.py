
#Good vs Bad Centrality
#For each of the nodes in the dataset, calculate degree centrality and eigenvector centrality.

import os
import networkx as nx
import matplotlib.pyplot as plt
from pandas import DataFrame
import pandas as pd
import webbrowser

os.chdir('C:\\Users\\TRADE\\Documents\\GitHub\\DATA620-Project1\\')
pickled_graph_file = 'SW_affiliations.gpickle' #get Bonnie's pickled graph file of Force Alignment
G = nx.read_gpickle(pickled_graph_file)
G.nodes['Han_Solo'] # alignment (sith/jedi)  {'score': 0.05, 'alignment': 'good'}
f = nx.get_node_attributes(G, 'score')  #extract the Sith/Jedi alignment scores from the nodes' first  attribute

#CONNECTEDNESS  calculate the number of connections each character has to other characters in the graph
lConnections = sorted(G.degree, key=lambda x: x[1], reverse=True) ##create a sorted list of characters by number of connections   #type(H) #<class 'list'>
d = nx.degree(G) #object needed to combine in table below

#CLOSENESS  calculate characters' closeness to each other
c=nx.closeness_centrality(G) #creates a dict of tuples, a=character, b=closeness   type(c) # <class 'dict'>
lCloseness = [(k,v) for k,v in c.items()]  #characters and closeness as a list!  <class 'list'>  [('1151', 0.2831842473296037), ('Crasher', 0.21856644313469864), 
lCloseness.sort(key=lambda x: x[1], reverse=True) #sort the list by the 2nd column

#BETWEENNESS  determine which characters are information brokers
b = nx.betweenness_centrality(G) #<class 'dict'>
lBetween =  [(k,v) for k,v in b.items()]
lBetween.sort(key=lambda x: x[1], reverse=True)

#EIGENVECTOR CENTRALITY
e = nx.eigenvector_centrality(G)
lEigen =  [(k,v) for k,v in e.items()]
lEigen.sort(key=lambda x: x[1], reverse=True)

#Bring all together (from textbook)
names1=[x[0] for x in lConnections[:10]] #get first column (character name) of first 11 records in the list
names2=[x[0] for x in lCloseness[:10]]
names3=[x[0] for x in lBetween[:10]]
names4=[x[0] for x in lEigen[:10]]
names = list(set(names1) | set(names2) | set(names3) | set(names4))  #make a list of distinct names from the 3 lists 
table=[[name,d[name],c[name],b[name], e[name], f[name]] for name in names]
type(table)

#display the table in a web-browser (just for fun)
df = pd.DataFrame(table)
df.columns = ['Name','Degree Centrality','Closeness','Betweenness','Eigen Centrality', 'Sith/Jedi Alignment']
filename = 'C:\\Users\\TRADE\\Documents\\GitHub\\DATA620-Project1\\table.html'
with open(filename,'w') as f:
    df.to_html(f)
webbrowser.open_new_tab(filename)




