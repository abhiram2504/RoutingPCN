import networkx as nx
import numpy as np
import random
from utils import *
from spanning import generate_and_validate_spanning_trees, visualize_spanning_trees

def low_stretch_spanning_tree(graph):
    """Generate a low-stretch spanning tree of the graph."""
    spanning_trees = []
    for node in graph.nodes:
        spanning_tree = generate_and_validate_spanning_trees(graph, node)
        spanning_trees.append(spanning_tree)

    # Return spanning trees as a dictionary with nodes as keys
    return {node: generate_and_validate_spanning_trees(graph, node) for node in graph.nodes}

# Function to route a single payment for one round
def route_single_payment(graph, demand_matrix, credit_matrix, source, target, path_type="shortest", idle_paths=None):
    success_payments = []  # List to keep track of successful payments
    failed_payments = []  # List to keep track of failed payments

    # Initialize idle_paths if it's None
    if idle_paths is None:
        num_nodes = len(demand_matrix)
        idle_paths = {frozenset([i, j]): 0 for i in range(num_nodes) for j in range(num_nodes) if i != j}

    # Get spanning trees if using LSST
    if path_type == "lsst":
        spanning_trees = low_stretch_spanning_tree(graph)
        tree_order = list(spanning_trees.keys())
        random.shuffle(tree_order)

    # Function to select paths based on the path type
    def select_path(graph, source, target, path_type, used_trees=None):

        if path_type == "shortest":
            # Check if path exists
            if nx.has_path(graph, source, target):
                # Get the shortest path
                path = nx.shortest_path(graph, source=source, target=target)
                return path
            else:
                return None  # Return None if no path exists

        elif path_type == "random":
            # Random path routing
            paths = list(nx.all_simple_paths(graph, source=source, target=target))
            if paths:
                path = random.choice(paths)
                return path
            else:
                return None

        elif path_type == "lsst":
            used_trees = set() if used_trees is None else used_trees
            for tree_key in tree_order:
                if tree_key in used_trees:
                    continue  # Skip trees that have already been used
                tree = spanning_trees[tree_key]
                if target in tree:
                    path = tree[target]
                    path_nodes = list(path)  # Convert path to a list of nodes
                    used_trees.add(tree_key)
                    return np.array(path_nodes), used_trees
            return None, used_trees
        else:
            raise ValueError(f"Invalid path type: {path_type}")

    # Only attempt to route the specific payment for the current (source, target) pair
    if demand_matrix[source, target] > 0:  # Exclude zero demand pairs
        used_trees = set()  # Reset used trees for each payment attempt
        demand_left = demand_matrix[source, target]
        payment_successful = False  # Flag to track if the payment was successful

        # Attempt to route on all spanning trees if using LSST
        while demand_left > 0 and path_type == "lsst":
            path, used_trees = select_path(graph, source, target, path_type, used_trees)

            if path is None:
                break  # No valid path found on any tree

            # Determine the minimum credit available along the path
            min_credit = min(credit_matrix[u][v] for u, v in zip(path[:-1], path[1:]))
            demand = demand_matrix[source, target]

            if min_credit >= demand:
                # Successful payment scenario
                for u, v in zip(path[:-1], path[1:]):
                    credit_matrix[u][v] -= demand
                    credit_matrix[v][u] += demand

                # Record the payment
                success_payments.append((source, target, demand))
                demand_matrix[source, target] = 0  # Update the demand matrix
                payment_successful = True  # Mark payment as successful
                break  # No need to try further trees
            else:
                for u, v in zip(path[:-1], path[1:]):
                    credit_matrix[u][v] -= min_credit
                    credit_matrix[v][u] += min_credit
                demand_matrix[source, target] -= min_credit
                demand_left -= min_credit  # Update remaining demand

        # If the payment wasn't successful after trying all spanning trees
        if not payment_successful and path_type == "lsst" and demand_left > 0:
            failed_payments.append((source, target, demand_left))
            demand_matrix[source, target] = 0  # Set demand to 0 since routing failed

        # If not using LSST or after trying all trees in LSST
        if path_type != "lsst" or not payment_successful:
            path = select_path(graph, source, target, path_type)

            if path is None or len(path) < 2:
                failed_payments.append((source, target, demand_matrix[source, target]))  # Record as failed
                demand_matrix[source, target] = 0  # Set demand to 0
                return success_payments, failed_payments, idle_paths  # Skip further processing

            min_credit = min(credit_matrix[u][v] for u, v in zip(path[:-1], path[1:]))
            demand = demand_matrix[source, target]

            if min_credit >= demand:
                for u, v in zip(path[:-1], path[1:]):
                    credit_matrix[u][v] -= demand
                    credit_matrix[v][u] += demand

                success_payments.append((source, target, demand))
                demand_matrix[source, target] = 0
            else:
                for u, v in zip(path[:-1], path[1:]):
                    credit_matrix[u][v] -= min_credit
                    credit_matrix[v][u] += min_credit
                demand_matrix[source, target] -= min_credit

    else:
        # If no demand, record as unsuccessful payment
        failed_payments.append((source, target, 0))  # Demand is zero
        demand_matrix[source, target] = 0

    # Increment the idle time for all other paths
    for k in range(len(demand_matrix)):
        for l in range(len(demand_matrix)):
            if k != l and (k, l) != (source, target):
                idle_paths[frozenset([k, l])] += 1

    return success_payments, failed_payments, idle_paths

def simulate_routing(demand_matrix, credit_matrix, graph, path_type="shortest"):
    all_success_payments = []  # Track all successful payments
    all_failed_payments = []   # Track all failed payments
    idle_paths = None          # Initialize idle paths

    # Get the total number of src-dest pairs with demand
    demand_pairs = [(i, j) for i in range(len(demand_matrix)) for j in range(len(demand_matrix)) if i != j and demand_matrix[i][j] > 0]
    total_pairs = len(demand_pairs)  # Total number of src-dest pairs

    # Round counter to track the actual rounds where routing happens
    round_num = 0

    path_type = PATH_TYPE

    # Iterate over all valid src-dest pairs
    for source, target in demand_pairs:
        # Route a single payment for this src-dest pair
        success_payments, failed_payments, idle_paths = route_single_payment(
            graph, demand_matrix, credit_matrix, source, target, path_type, idle_paths
        )

        # If successful, increment round counter and track results
        if success_payments or failed_payments:
            round_num += 1  # Count only valid routing attempts
            all_success_payments.extend(success_payments)
            all_failed_payments.extend(failed_payments)

            # Print the results for this round
            print(f"Round {round_num}:")
            print(f"Attempting to route from {source} to {target}")
            print("Successful payments:", success_payments)
            print("Failed payments:", failed_payments)
            print("Updated demand matrix:")
            print(demand_matrix)
            print("Updated credit matrix:")
            print(credit_matrix)

        # Check if all demands have been fulfilled
        if np.all(demand_matrix == 0):
            print(f"All demands fulfilled by round {round_num}")
            break  # Exit the loop if all demands are fulfilled

    return all_success_payments, all_failed_payments

