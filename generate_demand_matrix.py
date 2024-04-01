import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def generate_demand_matrix(G, max_payment=100):
    """
    Generate a demand matrix based on the edges of the given graph.
    """
    n = len(G.nodes())
    demand_matrix = np.zeros((n, n))
    adjacency_matrix = nx.to_numpy_array(G)
    for i in range(n):
        for j in range(n):
            if adjacency_matrix[i, j] != 0 and i != j:  # Edge exists in the graph
                # Assign random demand to the edge
                demand_matrix[i, j] = np.random.randint(1, max_payment) / 100
    return demand_matrix

if __name__ == "__main__":
    pass