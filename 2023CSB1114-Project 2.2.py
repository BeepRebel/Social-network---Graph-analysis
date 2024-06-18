#code for finding out the missing links using matrix method, jaccard method and then comparing results

#importing dictionaries for use
import pandas as pd
import networkx as nx
import numpy as np

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

#matrix method--------------------------------------------------------------------------------
#making adjacency matrix for our network graph
m = nx.adjacency_matrix(G).toarray()

#function for creating missing link matrix using m
def missing_link_matrix(m,threshold):
    #creating dictionary to store if missing link or not
    B={}
    
    #running loop in the matrix for all i,j
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            #deleting row and column from matrix to get A for the formula
            A = np.delete(m, i, axis=0)  
            A = np.delete(A, j, axis=1)  
    
            #for finding b,making vector with column deleted
            b = np.delete(m[i], j, axis=0) 
    
            #using linear algebra least square approximation, finding out coefficients for calculation
            lsa_coeff = np.linalg.lstsq(A, b, rcond=None)[0]  

            #calculating linear combination of column vector with coefficients we found
            P = np.delete(m, i, axis=0)  
            comb = P * lsa_coeff[:, np.newaxis]  
            V = np.sum(comb, axis=0)
            ml = V[j]
    
            #boolean to store missing link
            boole=False
            #change if missing link
            if ml > threshold:
                boole=True
            
            #appending the value of bool to dictionary
            B[(i,j)]=boole
    
    #creating a matrix that has ones only for missing link of the graph
    missing_link_matrix = np.zeros_like(m)  #initiating as zeroes
    #runnning loop for i,j in the graph
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            #if not present in original matrix
            if m[i, j] == 0:
                #if it is missing link
                if B[(i,j)]==True:
                    #append 1 in the matrix
                    missing_link_matrix[i][j] =1
                
    return missing_link_matrix

#function to find missing links in the graph
def missing_links(m, missing_link_matrix, nodes):
    #empty list to store the missing links
    missing_links = []
    
    #runnning loop for i,j in the matrix
    for i in range(missing_link_matrix.shape[0]):
        for j in range(missing_link_matrix.shape[1]):
            
            #append if missing link
            if missing_link_matrix[i, j] == 1:
                missing_links.append((nodes[i], nodes[j]))
                
    return missing_links

#for our graph
nodes = list(G.nodes())
threshold = 0.99

#calling functions for our graph to printing the number of missing links in our network
missing_link_matrix = missing_link_matrix(m, threshold)
missing_links = missing_links(m, missing_link_matrix, nodes)
print("Number of missing links using Matrix Method:", len(missing_links))
print(missing_links[8])

#jaccard coefficient method-------------------------------------------------------------------------
#first creating a threshold value for Jaccard coefficient
threshold_j = 0.134  

#creating empty list to store missing links by this method
missing_links_j = []

#for all the nodes in the graph
for i in G.nodes():
    for j in G.nodes():
        if i != j and not G.has_edge(i, j): #when there is no edge between chosen nodes
            #storing neighbors for both nodes
            neighbors_1 = set(G.neighbors(i))
            neighbors_2 = set(G.neighbors(j))
            #calculating Jaccard coefficient for i,j by definition
            intersection = len(neighbors_1.intersection(neighbors_2))
            union = len(neighbors_1.union(neighbors_2))
            if union != 0: #preventing division by zero
                jaccard_coeff= intersection / union
                #appending to list if coeff exceeds our set threshold
                if jaccard_coeff > threshold_j:
                    missing_links_j.append(((i,j), jaccard_coeff))

#printing number of missing links in network using jaccard coefficient
print("Number of missing links using Jaccard coefficient:", len(missing_links_j))
print(missing_links_j[8])