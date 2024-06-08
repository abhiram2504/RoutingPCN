import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

'''
Choosing a path with the max capacities in the channel. 
Ensure that the payment is routed through the most optimal path in terms of capacity, not necessarily 
the shortest path. This would help in avoiding bottelnecks due to insufficient funds.
'''

# Add nodes
nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
G.add_nodes_from(nodes)

# Add edges with varying capacities
edges = [
    ('A', 'B', 50), ('A', 'C', 100), ('A', 'G', 10),
    ('B', 'D', 100), ('B', 'E', 100), ('B', 'G', 10),
    ('C', 'D', 100), ('C', 'F', 100),
    ('D', 'E', 50), ('D', 'F', 100),
    ('E', 'F', 100), ('E', 'G', 100),
    ('F', 'G', 100)
]

G.add_weighted_edges_from(edges)

def send_payment(graph, source, target, amount):
    # Find all paths from source to target
    all_paths = list(nx.all_simple_paths(graph, source, target))
    
    # Find the path with the highest minimum capacity
    max_capacity_path = None
    max_capacity = 0
    
    for path in all_paths:
        # Find the minimum capacity in the path
        min_capacity = min(graph[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
        
        # Update the path with the highest minimum capacity
        if min_capacity >= amount and min_capacity > max_capacity:
            max_capacity = min_capacity
            max_capacity_path = path
    
    if max_capacity_path is None:
        raise ValueError("No path with enough capacity found")
    
    print(f"Sending payment of {amount} from {source} to {target} via path {max_capacity_path}")
    
    # Adjust the weights along the path
    for i in range(len(max_capacity_path) - 1):
        u, v = max_capacity_path[i], max_capacity_path[i + 1]
        graph[u][v]['weight'] -= amount
        # Print the updated weight
        print(f"Edge ({u}, {v}) new capacity: {graph[u][v]['weight']}")

# Send a payment of 20 from A to G
send_payment(G, 'A', 'G', 20)

# Print the updated graph capacities
for u, v, data in G.edges(data=True):
    print(f"Edge ({u}, {v}) capacity: {data['weight']}")

# Draw the updated network
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)

# Draw edge labels with capacities
edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()
