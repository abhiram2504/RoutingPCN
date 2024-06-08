import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

# Add nodes
nodes = range(1, 8)
G.add_nodes_from(nodes)

uniform_weight = 25
edges = [
    (1, 2, uniform_weight),
    (1, 3, uniform_weight),
    (2, 3, uniform_weight),
    (2, 4, uniform_weight),
    (3, 5, uniform_weight),
    (4, 5, uniform_weight),
    (4, 6, uniform_weight),
    (5, 6, uniform_weight),
    (5, 7, uniform_weight),
    (6, 7, uniform_weight)
]

G.add_weighted_edges_from(edges)

# Draw the graph
pos = nx.spring_layout(G)  # Layout for visual representation
nx.draw(G, pos, with_labels=True)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()
