#Code for finding out the top leader in dataset using random walk on network graph

#importing dictionaries for use
import pandas as pd
import networkx as nx
import random

#reading excel file using pandas
dataset=pd.read_excel('C:/Users/nares/OneDrive/Desktop/cs101/project2/dataset simplified.xlsx')

#creating a directed graph for dataset
G=nx.DiGraph()

#making the nodes as per the first column and adding edges from the rows
for i, row in dataset.iterrows():
    node = (row.iloc[0])
    G.add_node(node)
    edges_added = set()  #keeping track of edges to avoid duplicate edges
    for col in range(1, 31):  #columns 1 to 30 for impressions
        edge = (row.iloc[col])
        if pd.notna(edge) and edge != '' and edge != 'nan':  #checking for non-empty cell and not 'nan'
            if (node, edge) not in edges_added:  #checking if edge is already added
                G.add_edge(node, edge)
                edges_added.add((node, edge))  #add edge to the track set

#function for using random walk method to find out the top leader
def random_walk(G):
    nodes = list(G.nodes())
    points = {node: 0 for node in nodes}  #initialize points as dictionary for every node
    r = random.choice(nodes) #randomly dropping points
    points[r] += 1
    out = list(G.out_edges(r))
    
    
    c=0
    while c != 100000:
        if len(out) == 0: #teleportation for exception handling case
            focus = random.choice(nodes)
        else:
            focus= random.choice(out)[1]
            
        points[focus] += 1
        out = list(G.out_edges(focus))
        c += 1
    return points

#function for finding out the pagerank from the graph
def pagerank_order(points):
    sorted_nodes = sorted(points.items(), key=lambda x: x[1], reverse=True)
    return [node for node, _ in sorted_nodes]

#calling functions for our dataset and printing the top leader
points = random_walk(G)
sorted_nodes = pagerank_order(points)
print("TOP LEADER OF THE IMPRESSION NETWORK IS:",sorted_nodes[0])

   