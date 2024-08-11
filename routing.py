import networkx as nx
import numpy as np
import random

def low_stretch_spanning_tree(graph):
    """Generate a low-stretch spanning tree of the graph."""
    # https://github.com/danspielman/Laplacians.jl/blob/master/docs/src/LSST.md
    # Using to generate a single MST
    return nx.minimum_spanning_tree(graph)

# Function to route payments for one round
def route_payment_round(graph, demand_matrix, credit_matrix, path_type="shortest", idle_paths=None):
    num_nodes = len(demand_matrix)  # Number of nodes in the network
    success_payments = []  # List to keep track of successful payments
    failed_payments = []  # List to keep track of failed payments

    # Initialize idle_paths if it's None
    if idle_paths is None:
        idle_paths = {frozenset([i, j]): 0 for i in range(num_nodes) for j in range(num_nodes) if i != j}

    # Function to select paths based on the path type
    def select_path(source, target, path_type):
        print(f"Routing from node {source} to node {target} using {path_type} path.")
        if path_type == "shortest":
            # Shortest path routing
            return nx.shortest_path(graph, source=source, target=target)
        elif path_type == "random":
            # Random path routing
            paths = list(nx.all_simple_paths(graph, source=source, target=target))
            return random.choice(paths) if paths else None
        # Has to checked again
        elif path_type == "uniform":
            pass
            # Uniform routing: 
        #     paths = list(nx.all_simple_paths(graph, source=source, target=target))
        #     if not paths:
        #         return None

        #     # Find the path with the maximum idle time
        #     max_idle_time = -1
        #     selected_path = None
        #     for path in paths:
        #         idle_time = min(idle_paths[frozenset([u, v])] for u, v in zip(path[:-1], path[1:]))
        #         if idle_time > max_idle_time:
        #             max_idle_time = idle_time
        #             selected_path = path

        #     return selected_path
        # else:
        #     raise ValueError(f"Invalid path type: {path_type}")

    # Iterate over all pairs of nodes
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and demand_matrix[i, j] > 0:  # Exclude self-pairs and zero demand pairs
                # Select the path based on the routing strategy
                path = select_path(i, j, path_type)
                
                if path is None:
                    continue  # Skip if no path is found

                # Determine the minimum credit available along the path
                min_credit = min(credit_matrix[u][v] for u, v in zip(path[:-1], path[1:]))
                
                # Get the demand for this source-destination pair
                demand = demand_matrix[i, j]

                if min_credit >= demand:
                    # Successful payment scenario
                    for u, v in zip(path[:-1], path[1:]):
                        # Deduct the demand amount from the credit matrix on the forward path
                        credit_matrix[u][v] -= demand
                        # Add the demand amount to the credit matrix on the reverse path (optional, if undirected)
                        credit_matrix[v][u] += demand
                    # Record the successful payment
                    success_payments.append((i, j, demand))
                    # Update the demand matrix to reflect that the demand has been fulfilled
                    demand_matrix[i, j] = 0

                    # Update the idle times for the path used
                    for u, v in zip(path[:-1], path[1:]):
                        idle_paths[frozenset([u, v])] = 0
                else:
                    # Partial payment scenario
                    for u, v in zip(path[:-1], path[1:]):
                        # Deduct the maximum possible amount from the credit matrix on the forward path
                        credit_matrix[u][v] -= min_credit
                        # Add the deducted amount to the credit matrix on the reverse path (optional, if undirected)
                        credit_matrix[v][u] += min_credit
                    # Record the partial payment
                    failed_payments.append((i, j, min_credit))
                    # Update the demand matrix to reflect the remaining demand
                    demand_matrix[i, j] -= min_credit

                    # Update the idle times for the path used
                    for u, v in zip(path[:-1], path[1:]):
                        idle_paths[frozenset([u, v])] = 0

                # Increment the idle time for all other paths
                for k in range(num_nodes):
                    for l in range(num_nodes):
                        if k != l and (k, l) != (i, j):
                            idle_paths[frozenset([k, l])] += 1

                # After routing for one pair, stop and return the results
                return success_payments, failed_payments, idle_paths

    # Return results if no payments were routed in this round
    return success_payments, failed_payments, idle_paths

# Function to simulate routing over multiple rounds
def simulate_routing(demand_matrix, credit_matrix, num_rounds, graph, path_type="shortest"):
    all_success_payments = []  # List to keep track of all successful payments
    all_failed_payments = []  # List to keep track of all failed payments
    idle_paths = None  # Initialize idle paths

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
