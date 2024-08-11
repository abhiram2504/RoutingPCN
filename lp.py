import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import generate_demand_matrix as gdm
import routing as rt
import cost_matrix as cm

from utils import *

# def initialize_graph(demand_matrix):
#     G = nx.Graph()
#     num_nodes = len(demand_matrix)
#     for i in range(num_nodes):
#         for j in range(num_nodes):
#             if i != j:
#                 G.add_edge(i, j)  
#     return G


def generate_test_graph():
    graph = nx.Graph()
    credit_mat = cm.generate_credit_matrix()
    #the weight is uniform
    graph.add_edge(0, 1, weight=credit_mat[0][1] + credit_mat[1][0])
    graph.add_edge(1, 2, weight=credit_mat[1][2] + credit_mat[2][1])
    graph.add_edge(2, 3, weight=credit_mat[2][3] + credit_mat[3][2])
    graph.add_edge(3, 0, weight=credit_mat[3][0] + credit_mat[0][0])
    return graph

def calculate_src_dest_pairs(demand_matrix):
    count = 0
    for i in range(len(demand_matrix)):
        for j in range(len(demand_matrix[0])):
            if i != j and demand_matrix[i][j] != 0:  # Exclude self-pairs

                count += 1
    return count

# Function to visualize the graph 
def visualize_graph(graph):
    pos = nx.spring_layout(graph)  
    plt.figure(figsize=(8, 6)) 

    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color='skyblue')
    nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(data=True), width=2)

    labels = {node: str(node) for node in graph.nodes()}
    nx.draw_networkx_labels(graph, pos, labels, font_size=12)

    edge_labels = {(u, v): f'{d["weight"]:.2f}' for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10)

    plt.title("Network Graph")
    plt.show()

# Main function
def main():
    G = generate_test_graph()
    demand_mat = gdm.generate_demand_matrix()
    credit_mat = cm.generate_credit_matrix()
    num_rounds = ROUNDS
    print(f"The number of rounds are: {num_rounds}")
    # Calculate the number of source-destination pairs
    num_pairs = calculate_src_dest_pairs(demand_mat)
    print(f"Number of source-destination pairs: {num_pairs}")

    # Visualize the initial graph
    visualize_graph(G)

    all_success_payments, all_failed_payments = rt.simulate_routing(demand_mat, credit_mat, num_rounds, G)
    # Output final results
    print("Final successful payments:", all_success_payments)
    print("Final failed payments:", all_failed_payments)
    print(f"Throughput: {len(all_success_payments)/(len(all_success_payments)+len(all_failed_payments))}")

if __name__ == '__main__':
    main()
