import networkx as nx
import matplotlib.pyplot as plt
import random as rand
import numpy as np
import pandas as pd

from utils import * 

# MIN_ALPHA = 0.5  # Minimum value of ALPHA to stop reducing it
DIST_LIST = []
NODE_PAIRS = []


def generate_max_spanning_tree(graph):
    global DIST_LIST

    """Generate a maximum spanning tree using Prim's algorithm (edges with higher weights are prioritized)."""
    max_spanning_tree = nx.minimum_spanning_tree(graph, weight='weight')
    
    return max_spanning_tree

def calculate_strech_of_spanning_tree(max_spanning_tree):
    paths = dict(nx.all_pairs_shortest_path(max_spanning_tree))
    length_dict = {}
    # Calculate lengths
    for i in range(max_spanning_tree.number_of_nodes()):
        for j in range(max_spanning_tree.number_of_nodes()):
            if i != j:
                key = f"{i}->{j}"
                if key not in NODE_PAIRS:
                    NODE_PAIRS.append(key)
                path_len = len(paths[i][j])-1
                if key in length_dict:
                    length_dict[key].append(path_len)                    
                else:
                    length_dict[f"{i}->{j}"] = len(paths[i][j])-1
                
                # Append path length to DIST_LIST
                DIST_LIST.append(len(paths[i][j])-1)
                
    print(length_dict)

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
    all_spanning_tree_edges = set()
    original_edges = set(graph.edges())
    spanning_tree_list = []
    for i in range(len(list(graph.nodes()))):
        T = generate_max_spanning_tree(graph)
        spanning_tree_list.append(T)
        tree_edges = set(T.edges())
        all_spanning_tree_edges.update(tree_edges)

        increase_edge_weights(graph, tree_edges)

        if all_spanning_tree_edges == original_edges:
            print(spanning_tree_list)
            break
    
    return all_spanning_tree_edges, spanning_tree_list

def visualize_spanning_trees(graph, spanning_tree_list):
    # pos = nx.spring_layout(graph)

    # # Prepare subplots
    # num_nodes = len(graph.nodes())
    # fig, axs = plt.subplots(1, num_nodes + 1, figsize=(20, 5))
    # fig.suptitle('Original Graph and Maximum Spanning Trees')

    # # Plot the original graph
    # nx.draw(graph, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=16, font_weight='bold', edge_color='gray', ax=axs[0])
    # edge_labels = nx.get_edge_attributes(graph, 'weight')
    # nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=axs[0])
    # axs[0].set_title('Original Graph')

    # Initialize variables to track the union of spanning tree edges
    all_spanning_tree_edges = set()
    original_edges = set(graph.edges())

    # Generate and plot maximum spanning trees for each node
    for i, node in enumerate(graph.nodes()):
        T = generate_max_spanning_tree(graph)
        
        # Add spanning tree object to the list
        spanning_tree_list.append(T)
        
        # Add spanning tree edges to the union
        tree_edges = set(T.edges())
        all_spanning_tree_edges.update(tree_edges)
          
        # Decrease the weights of the edges used in the current spanning tree
        # decrease_edge_weights(graph, tree_edges)

        # Plot the original graph with reduced opacity
        # nx.draw(graph, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=16, font_weight='bold', edge_color='gray', ax=axs[i], alpha=0.5)
        
        # # Plot the spanning tree on top
        # nx.draw(T, pos, with_labels=True, node_size=700, node_color='orange', edge_color='red', width=2, ax=axs[i])
        
        # edge_labels = nx.get_edge_attributes(graph, 'weight')
        # nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=axs[i])
        # axs[i].set_title(f'Maximum Spanning Tree from Node {node}')

        # Check if all edges are now covered
        if all_spanning_tree_edges == original_edges:
            print(all_spanning_tree_edges)
            break  # Stop as soon as all edges are covered

    
    # Adjust layout and show
    # plt.tight_layout(rect=[0, 0, 1, 0.95])
    # plt.show()



def generate_and_validate_spanning_trees(graph):
    global ALPHA
    original_weights = {(u, v): data['weight'] for u, v, data in graph.edges(data=True)}  # Store original edge weights
    
    # List to store all spanning tree objects
    spanning_tree_list = []

    while True:
        # Generate spanning trees and collect their edges
        all_spanning_tree_edges, spanning_tree_list = spanning_tree_list_compute(graph)
        original_edges = set(graph.edges())
        
        # Calculate missing edges
        missing_edges = original_edges - all_spanning_tree_edges
        
        # Check if all original edges are covered
        if not missing_edges:
            print("Validation successful: All edges of the original graph are covered.")
            return spanning_tree_list  # Return the set of all spanning tree objects
        
        # If some edges are missing
        print(f"Validation failed: {len(missing_edges)} edges are missing. Re-creating trees with ALPHA = {ALPHA}")
        
        # if ALPHA <= MIN_ALPHA:
        #     print(f"Cannot reduce ALPHA further. Missing edges: {missing_edges}")
        #     return False  # Exit if we can't reduce ALPHA further

        # Reset the graph's edge weights to the original values
        reset_edge_weights(graph, original_weights)
        
        # Reduce ALPHA and try again
        ALPHA = round(ALPHA + 0.1, 2)

    """
    If alpha is 0.5 and even then the edges are not being created properly then 
    just add all the edges to the tree
    """


if __name__ == "__main__":
    # Create a random graph
    G = nx.erdos_renyi_graph(5, 0.6)  # A random graph with 5 nodes and 60% probability of edge creation
    for u, v in G.edges():
        G[u][v]['weight'] = 2  # For testing

    # Generate and validate spanning trees
    all_spanning_trees = generate_and_validate_spanning_trees(G)
    if all_spanning_trees:
        print(f"Generated {len(all_spanning_trees)} spanning trees.")

    # Group distances for each node pair (since there are 5 trees)
    grouped_distances = {pair: DIST_LIST[i::20] for i, pair in enumerate(NODE_PAIRS)}

    # Compute the average distance for each node pair
    average_distances = {pair: sum(distances) / len(distances) for pair, distances in grouped_distances.items()}

    # Convert to DataFrame for better visualization
    df_from_list = pd.DataFrame(list(average_distances.items()), columns=['Node Pair', 'Average Distance'])
    df_from_list.set_index('Node Pair', inplace=True)

    #  print(df_from_list)
