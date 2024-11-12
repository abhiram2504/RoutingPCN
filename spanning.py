import networkx as nx # type: ignore
import matplotlib.pyplot as plt # type: ignore
import random as rand
import numpy as np # type: ignore
import pandas as pd # type: ignore

from utils import * 
from graph import visualize_graph
from collections import Counter

NODE_PAIRS = []

# rand.seed(RAND_SEED)

def generate_min_spanning_tree(graph):
    mix_spanning_tree = nx.minimum_spanning_tree(graph, weight='weight')
    return mix_spanning_tree

def calulate_matrix_distance(tree):
    n = tree.number_of_nodes()
    distance_matrix = np.zeros((n, n), dtype=int)
    paths_lengths = dict(nx.all_pairs_shortest_path_length(tree))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = paths_lengths[i][j]
    
    return distance_matrix

def increase_edge_weights(graph, edges_used):
    """Increase the weights of edges used in a spanning tree."""
    for u, v in edges_used:
        if 'weight' in graph[u][v]:
            graph[u][v]['weight'] = round(graph[u][v]['weight'] * ALPHA, 2)  # Incraese the weight by alpha

def reset_edge_weights(graph, original_weights):
    """Reset edge weights to their original values."""
    for (u, v), weight in original_weights.items():
        graph[u][v]['weight'] = weight

def spanning_tree_list_compute(graph):
    global ALPHA
    all_spanning_tree_edges = set()
    original_edges = set(graph.edges())
    spanning_tree_list = []
    for i in range(len(graph.nodes())):
        T = generate_min_spanning_tree(graph)
        spanning_tree_list.append(T)
        tree_edges = set(T.edges())
        all_spanning_tree_edges.update(tree_edges)

        increase_edge_weights(graph, tree_edges)

    return all_spanning_tree_edges, spanning_tree_list

def generate_and_validate_spanning_trees(graph):
    global ALPHA
    original_weights = {(u, v): data['weight'] for u, v, data in graph.edges(data=True)}  # Store original edge weights
    
    spanning_tree_list = []

    while True:
        all_spanning_tree_edges, spanning_tree_list = spanning_tree_list_compute(graph)
        original_edges = set(graph.edges())
        
        missing_edges = original_edges - all_spanning_tree_edges
        
        if not missing_edges:
            print("Validation successful: All edges of the original graph are covered.")
            return spanning_tree_list  # Return the set of all spanning tree objects
        else:
            # If some edges are missing
            print(f"Validation failed: {len(missing_edges)} edges are missing. Re-creating trees with ALPHA = {ALPHA}")
            reset_edge_weights(graph, original_weights)
            ALPHA = round(ALPHA + 0.1, 2)
            spanning_tree_list_compute(graph)

def calculate_normalized_distance_matrix(G):
    spanning_trees = generate_and_validate_spanning_trees(G)
    
    graph_distance_matrix = calulate_matrix_distance(G)
    
    sp_distance_matrixs = []
    for tree in spanning_trees:
        sp_distance_matrixs.append(calulate_matrix_distance(tree))
        
    
    mean_sp_distance_matrix = np.mean(sp_distance_matrixs, axis=0)
    
    epsilon = 1e-10  
    result_matrix = np.divide(mean_sp_distance_matrix, graph_distance_matrix + epsilon)
    
    return result_matrix
        
if __name__ == "__main__":
    G = nx.erdos_renyi_graph(GRAPH_SIZE, ERDOS_P_EDGE, RAND_SEED)
    if not nx.is_connected(G):
        print("Graph is not connected.")
        exit(0)
    for u, v in G.edges():
        G[u][v]['weight'] = 2 * CREDIT_AMT

    spanning_trees = generate_and_validate_spanning_trees(G)
    result_matrix = calculate_normalized_distance_matrix(G)
    print(result_matrix)
    

