import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Function to visualize the demand graph
def visualize_demand_graph(demand_matrix):
    G = nx.Graph()  # Create an empty graph
    for i in range(len(demand_matrix)):
        for j in range(len(demand_matrix[0])):
            if i != j:
                G.add_edge(i, j, demand=demand_matrix[i, j])  # Add an edge between nodes i and j with demand
    pos = nx.spring_layout(G)  # Compute node positions using the spring layout algorithm
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='black')
    plt.show()
    return G

def routing(matrix_payment_seq):
    G = visualize_demand_graph(matrix_payment_seq[0])
    paths = []
    for i in range(len(matrix_payment_seq)):
        path = []
        for source in G.nodes():
            for target in G.nodes():
                if source != target:
                    path.append(nx.dijkstra_path(G, source, target, weight='demand'))
        paths.append(path)
    return paths





def route_payment(graph, source, destination, amount):
    try:
        shortest_path = nx.dijkstra_path(graph, source, destination)
        # Check if the path has enough capacity to route the payment
        for i in range(len(shortest_path) - 1):
            capacity = graph[shortest_path[i]][shortest_path[i+1]]['weight']
            if amount > capacity:
                return False  # Insufficient capacity, fail the payment
        # Route the payment and update channel capacities
        for i in range(len(shortest_path) - 1):
            # Deduct payment amount from channel capacity
            graph[shortest_path[i]][shortest_path[i+1]]['weight'] -= amount
        return True  # Payment successfully routed
    except nx.NetworkXNoPath:
        return False  # No path found between source and destination
