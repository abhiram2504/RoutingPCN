import networkx as nx
import matplotlib.pyplot as plt
import random as rand
import numpy as np
import pandas as pd

from utils import * 

MIN_ALPHA = 0.5  # Minimum value of ALPHA to stop reducing it
DIST_LIST = []
NODE_PAIRS = []


def generate_max_spanning_tree(graph):
    global DIST_LIST

    """Generate a maximum spanning tree using Prim's algorithm (edges with higher weights are prioritized)."""
    max_spanning_tree = nx.maximum_spanning_tree(graph, weight='weight')
    paths = dict(nx.all_pairs_shortest_path(max_spanning_tree))

    length_dict = {}
    

    #calculate lengths
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
                
                #0 in the first list, 1 ist in the second .... max of i lists each having i elemetns
                    DIST_LIST.append(len(paths[i][j])-1)
                
    print(length_dict)

    #print(paths)

    return max_spanning_tree

def decrease_edge_weights(graph, edges_used):
    """Decrease the weights of edges used in a spanning tree."""
    for u, v in edges_used:
        if 'weight' in graph[u][v]:
            graph[u][v]['weight'] = round(graph[u][v]['weight'] * ALPHA, 2)  # Decrease weight by ALPHA factor

def reset_edge_weights(graph, original_weights):
    """Reset edge weights to their original values."""
    for (u, v), weight in original_weights.items():
        graph[u][v]['weight'] = weight

def visualize_spanning_trees(graph):
    pos = nx.spring_layout(graph)

    # Prepare subplots
    num_nodes = len(graph.nodes())
    fig, axs = plt.subplots(1, num_nodes + 1, figsize=(20, 5))
    fig.suptitle('Original Graph and Maximum Spanning Trees')

    # Plot the original graph
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=16, font_weight='bold', edge_color='gray', ax=axs[0])
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=axs[0])
    axs[0].set_title('Original Graph')

    # Initialize variables to track the union of spanning tree edges
    all_spanning_tree_edges = set()

    # Generate and plot maximum spanning trees for each node
    for i, node in enumerate(graph.nodes(), start=1):
        T = generate_max_spanning_tree(graph)
        
        # Add spanning tree edges to the union
        tree_edges = set(T.edges())
        all_spanning_tree_edges.update(tree_edges)
        
        # Decrease the weights of the edges used in the current spanning tree
        decrease_edge_weights(graph, tree_edges)
        
        # Plot the original graph with reduced opacity
        nx.draw(graph, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=16, font_weight='bold', edge_color='gray', ax=axs[i], alpha=0.5)
        
        # Plot the spanning tree on top
        nx.draw(T, pos, with_labels=True, node_size=700, node_color='orange', edge_color='red', width=2, ax=axs[i])
        
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=axs[i])
        axs[i].set_title(f'Maximum Spanning Tree from Node {node}')
    
    # Adjust layout and show
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

    return all_spanning_tree_edges

def generate_and_validate_spanning_trees(graph):
    global ALPHA
    original_weights = {(u, v): data['weight'] for u, v, data in graph.edges(data=True)}  # Store original edge weights
    
    while True:
        all_spanning_tree_edges = visualize_spanning_trees(graph)
        original_edges = set(graph.edges())
        missing_edges = original_edges - all_spanning_tree_edges
        print(graph.edges())

        if not missing_edges:
            print("Validation successful: All edges of the original graph are covered.")
            return True
        else:
            print(f"Validation failed: {len(missing_edges)} edges are missing. Re-creating trees with ALPHA = {ALPHA}")
            if ALPHA <= MIN_ALPHA:
                print(f"Cannot reduce ALPHA further. Missing edges: {missing_edges}")
                return False


            # Reset the graph's edge weights to the original values
            reset_edge_weights(graph, original_weights)
            
            # Reduce ALPHA and try again
            ALPHA = round(ALPHA - 0.1, 2)

if __name__ == "__main__":
    # Create a random graph
    G = nx.erdos_renyi_graph(5, 0.6)  # A random graph with 5 nodes and 60% probability of edge creation
    for u, v in G.edges():

        # G[u][v]['weight'] = round(1 + (rand.random() * 9), 2)  # Initialize random edge weights between 1 and 10
        # For testing:
        G[u][v]['weight'] = 2

    # Generate and validate spanning trees
    validation = generate_and_validate_spanning_trees(G)

    # Group distances for each node pair (since there are 5 trees)
    grouped_distances = {pair: DIST_LIST[i::20] for i, pair in enumerate(NODE_PAIRS)}

    # Compute the average distance for each node pair
    average_distances = {pair: sum(distances) / len(distances) for pair, distances in grouped_distances.items()}

    # Convert to DataFrame for better visualization
    df_from_list = pd.DataFrame(list(average_distances.items()), columns=['Node Pair', 'Average Distance'])
    df_from_list.set_index('Node Pair', inplace=True)

    print(df_from_list)




