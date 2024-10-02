import networkx as nx
import random

# Initialize the graph
G = nx.complete_graph(5, weights=2)

# Add edges with weights (all weights initially 1)
edges = [('A', 'B', 1), ('A', 'C', 1), ('B', 'C', 1), ('B', 'D', 1), 
         ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]

G.add_weighted_edges_from(edges)

# Function to generate low-stretch spanning trees
def generate_low_stretch_spanning_trees(graph):
    # Dictionary to track weights
    weights = {(u, v): d['weight'] for u, v, d in graph.edges(data=True)}
    spanning_trees = []
    covered_edges = set()

    while len(covered_edges) < len(graph.edges):
        # Create a new spanning tree by prioritizing high-weight edges
        tree = create_spanning_tree(graph, weights)
        spanning_trees.append(tree)

        # Update weights and track covered edges
        for u, v in tree.edges:
            weights[(u, v)] *= 0.85  # Reduce weight after use
            covered_edges.add((u, v))

    return spanning_trees

# Function to create a spanning tree using Kruskal's algorithm
def create_spanning_tree(graph, weights):
    # Sort edges by weight, prioritize higher weights first
    sorted_edges = sorted(graph.edges(data=True), key=lambda x: weights[(x[0], x[1])], reverse=True)
    
    # Create a spanning tree using Kruskal's algorithm
    T = nx.Graph()
    for u, v, _ in sorted_edges:
        T.add_edge(u, v)
        if nx.is_tree(T) and len(T.edges) == len(graph.nodes) - 1:
            break
    
    return T

# Generate the spanning trees
spanning_trees = generate_low_stretch_spanning_trees(G)

# Display the generated spanning trees
for i, tree in enumerate(spanning_trees):
    print(f"Spanning Tree {i + 1}:")
    print(list(tree.edges))
