import networkx as nx
import numpy as np
import random
import sys

from spanning import visualize_spanning_trees

from utils import *

def low_stretch_spanning_tree(graph):
    """Generate a low-stretch spanning tree of the graph."""
    # Placeholder for generating an actual low-stretch spanning tree
    # For now, we'll use the minimum spanning tree as a proxy
    return nx.minimum_spanning_tree(graph)

def shortest_path_trees(graph):
    """Generate shortest path trees rooted at each node.
    It calculates the shortest paths from that node to all other nodes."""
    trees = {}
    for node in graph.nodes:
        # Generate the shortest path tree rooted at this node
        tree = nx.single_source_shortest_path(graph, source=node)
        trees[node] = tree
    print(trees)
    return trees

def route_payment_round(graph, demand_matrix, credit_matrix, path_type="shortest", idle_paths=None):
    num_nodes = len(demand_matrix)  # Number of nodes in the network
    success_payments = []  # List to keep track of successful payments
    failed_payments = []  # List to keep track of failed payments

    # Initialize idle_paths if it's None
    if idle_paths is None:
        idle_paths = {frozenset([i, j]): 0 for i in range(num_nodes) for j in range(num_nodes) if i != j}

    # Get spanning trees if using LSST
    if path_type == "lsst":
        spanning_trees = visualize_spanning_trees(graph)

    # Function to select paths based on the path type
    def select_path(source, target, path_type, used_trees=None):
        print(f"Routing from node {source} to node {target} using {path_type} path.")
        if path_type == "shortest":
            # Shortest path routing
            path = nx.shortest_path(graph, source=source, target=target)
            print(f"Path taken: {path}")
            return path  # Return only the path
                
        elif path_type == "random":
            # Random path routing
            paths = list(nx.all_simple_paths(graph, source=source, target=target))
            if paths:
                path = random.choice(paths)
                print(f"Path taken: {path}")
                return path  # Return only the path
            else:
                print("No paths available.")
                return None

        elif path_type == "lsst":
            used_trees = set() if used_trees is None else used_trees

            # Route using the spanning trees
            for tree in spanning_trees:
                if target in tree:
                    path = tree[target]
                    print(f"Path taken from spanning tree rooted at {tree}: {path}")
                    return path  # Return both the path
            print(f"No path found from node {source} to node {target} in any tree.")
            return None

        else:
            raise ValueError(f"Invalid path type: {path_type}")

    # Iterate over all pairs of nodes
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and demand_matrix[i, j] > 0:  # Exclude self-pairs and zero demand pairs
                used_trees = set()  # Reset used trees for each payment attempt
                demand_left = demand_matrix[i, j]

                # Modify the part where select_path is called:
                if path_type == "lsst":
                    path = select_path(i, j, path_type, used_trees)
                else:
                    path = select_path(i, j, path_type)

                if path is None or len(path) < 2:
                    print(f"No valid path found for nodes {i} -> {j}. Skipping.")
                    continue  # Skip to the next pair if no valid path found

                # Determine the minimum credit available along the path
                min_credit = min(credit_matrix[u][v] for u, v in zip(path[:-1], path[1:]))

                # Calculate how much we can actually send
                demand = demand_matrix[i, j]

                if min_credit >= demand:
                    # Successful or partial payment scenario
                    for u, v in zip(path[:-1], path[1:]):
                        # Deduct the amount from the credit matrix on the forward path
                        credit_matrix[u][v] -= demand
                        # Add the amount to the credit matrix on the reverse path (optional, if undirected)
                        credit_matrix[v][u] += demand

                    # Record the payment
                    if demand == demand_left:
                        success_payments.append((i, j, demand))
                        demand_matrix[i, j] = 0  # Update the demand matrix
                        demand_left = 0

                    # Update the idle times for the path used
                    for u, v in zip(path[:-1], path[1:]):
                        idle_paths[frozenset([u, v])] = 0

                    if path_type == "lsst":
                        print(f"LSST path completed for nodes {i} -> {j}. Moving to the next round.")
                        return success_payments, failed_payments, idle_paths
                else:
                    for u, v in zip(path[:-1], path[1:]):
                        # Deduct the maximum possible amount from the credit matrix on the forward path
                        credit_matrix[u][v] -= min_credit
                        # Add the deducted amount to the credit matrix on the reverse path (optional, if undirected)
                        credit_matrix[v][u] += min_credit
                    # Update the demand matrix to reflect the remaining demand
                    demand_matrix[i, j] -= min_credit

                # Increment the idle time for all other paths
                for k in range(num_nodes):
                    for l in range(num_nodes):
                        if k != l and (k, l) != (i, j):
                            idle_paths[frozenset([k, l])] += 1
            
                # After routing for one pair, stop and return the results
                return success_payments, failed_payments, idle_paths

    # Return results
    return success_payments, failed_payments, idle_paths

# Function to simulate routing over multiple rounds
def simulate_routing(demand_matrix, credit_matrix, num_rounds, graph, path_type="shortest"):
    all_success_payments = []  # List to keep track of all successful payments
    all_failed_payments = []  # List to keep track of all failed payments
    idle_paths = None  # Initialize idle paths

    path_type = PATH_TYPE

    # Iterate over the number of rounds
    for round_num in range(1, num_rounds + 1):
        # Route payments for this round
        success_payments, failed_payments, idle_paths = route_payment_round(
            graph, demand_matrix, credit_matrix, path_type, idle_paths
        )
        # Add this round's payments to the overall lists
        all_success_payments.extend(success_payments)
        all_failed_payments.extend(failed_payments)
        
        # Print the results for this round
        print(f"Round {round_num}:")
        print("Successful payments:", success_payments)
        print("Failed payments:", failed_payments)
        print("Updated demand matrix:")
        print(demand_matrix)
        print("Updated credit matrix:")
        print(credit_matrix)

        # Check if all demands have been fulfilled
        if np.all(demand_matrix == 0):
            print(f"All demands fulfilled at round {round_num}")
            break  # Exit the loop if all demands are fulfilled

    return all_success_payments, all_failed_payments
