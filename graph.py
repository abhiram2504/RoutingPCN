import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

import generate_demand_matrix as gdm
import cost_matrix as cm

from utils import *

def generate_graph():
    if GRAPH_TYPE == "test":
        graph = nx.Graph()
        credit_mat = cm.generate_credit_matrix()
        #the weight is uniform
        graph.add_edge(0, 1, weight=credit_mat[0][1] + credit_mat[1][0])
        graph.add_edge(1, 2, weight=credit_mat[1][2] + credit_mat[2][1])
        graph.add_edge(2, 3, weight=credit_mat[2][3] + credit_mat[3][2])
        graph.add_edge(3, 0, weight=credit_mat[3][0] + credit_mat[0][0])
        return graph
    elif GRAPH_TYPE == "erdos-renyi":
        G = nx.erdos_renyi_graph(GRAPH_SIZE, ERDOS_P_EDGE, RAND_SEED)
        # Setting the graph weight or the capacties
        if not nx.is_connected(G):
            print("Graph is not connected.")
            exit(0)
        for u, v in G.edges():
            G[u][v]['weight'] = 2 * CREDIT_AMT
        # nx.draw(G, with_labels=True)
        return G
    elif GRAPH_TYPE == "grid":
        G = nx.grid_2d_graph(GRID_GRAPH_SIZE, GRID_GRAPH_SIZE)
        return G

# Function to visualize the graph 
def visualize_graph(graph):
    pos = nx.spring_layout(graph)  
    plt.figure(figsize=(8, 6)) 

    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color='skyblue')
    nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(data=True), width=2)

    labels = {node: str(node) for node in graph.nodes()}
    nx.draw_networkx_labels(graph, pos, labels, font_size=12)

    plt.title("Network Graph")
    plt.show()