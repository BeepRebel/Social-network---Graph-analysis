#Code for finding top 5 most influential people from the network using combined centrality

#importing dictionaries for use
import pandas as pd
import networkx as nx

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

#function for calculating betweenness centrality of nodes of graph
def calculate_betweenness_centrality(graph):
    betweenness = {}  #initializing dictionary to store value for each node
    for node in graph.nodes(): #loop for nodes in graph
        betweenness[node] = 0  #setting centrality value as zero for all

    for node in graph.nodes():  #loop for source nodes in graph
        for s in graph.nodes():  #loop for target nodes in graph
            if s != node:  #when they are not equal
                try:
                    shortest_paths = nx.all_shortest_paths(graph, source=s, target=node) #calculates shortest path between s and node
                    num_shortest_paths = 0  #initializing variable to keep a count
                    shortest_path_nodes = set()  #creating empty set of paths
                    for path in shortest_paths:  #loop in shortest paths
                        num_shortest_paths += 1  #adds on every iteration
                        shortest_path_nodes.update(path)  #updating set
                        for v in shortest_path_nodes: #loop in updated set
                            if v != s and v != node:  #if v is neither source nor target
                                betweenness[v] += 1 / num_shortest_paths  #values for all such v are added for which shortest paths pass through it
                except nx.NetworkXNoPath:  #when there is no path from source node to target node
                    pass
    return betweenness

#calling function for our graph
betweenness = calculate_betweenness_centrality(G)

#function for calculating closeness centrality for nodes of graph
def calculate_closeness_centrality(graph):
    closeness = {}  #initializing dictionary to store value for each node
    for node in graph.nodes():  #loop for current nodes in graph
        total_distance = 0  #initializing variable to store distance from current node to all reachable nodes
        num_reachable_nodes = 0  #initializing variable to count the number of reachable nodes from the current node
        for target_node in graph.nodes():  #loop for target nodes in graph
            if node != target_node:  #when they are not equal
                try:
                    shortest_path_length = nx.shortest_path_length(graph, source=node, target=target_node) #calculates shortest path length between node and target_node
                    total_distance += shortest_path_length  #adding this length to total distance
                    num_reachable_nodes += 1 #adds on every iteration
                except nx.NetworkXNoPath: #when there is no path from source node to target node
                    pass
        closeness[node] = (num_reachable_nodes - 1) / total_distance if total_distance != 0 else 0  #value of closeness centarlity is calculated as reciprocal of average distance from node to all reachable nodes,1 is subtracted to avoid counting itself, 0 is set to avoid division by zero
    return closeness

#calling function for our graph
closeness = calculate_closeness_centrality(G)

#function for calculating degree centrality for nodes of graph
def calculate_degree_centrality(graph):
    degree = {}  #initializing dictionary to store value for each node
    num_nodes_minus_one = len(graph.nodes()) - 1  #calculating total nodes minus 1 to use for definition
    for node in graph.nodes():  #loop for nodes in graph
        degree[node] = len(graph[node]) / num_nodes_minus_one  #degree of node/num of nodes -1
    return degree

#calling function for our graph
degree = calculate_degree_centrality(G)

#calculating the combined centrality by adding all the three calculated values
all_measures = {node: betweenness.get(node, 0) + closeness.get(node, 0) + degree.get(node, 0) for node in G.nodes()}

#sorting nodes by combined centrality value in descending order
sorted_nodes = sorted(all_measures.items(), key=lambda x: x[1], reverse=True)

#printing top 5 influential spreaders
print("Top 5 influential spreaders:")
for i, (node, centrality) in enumerate(sorted_nodes[:5]):
    print(f"{i+1}. Node: {node}, Combined Centrality: {centrality}")
