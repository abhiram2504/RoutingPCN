import networkx as nx # type: ignore
import numpy as np # type: ignore
import random, time
from collections import Counter
from utils import *

from spanning import generate_and_validate_spanning_trees
from graph import visualize_graph

TOTAL_DEMAND_FAILED = 0
    
# Function to route a single payment for one round
def route_single_payment(graph, demand_matrix, credit_matrix, source, target, path_type, tree = None):
    global TOTAL_DEMAND_FAILED
    success_payments = []  
    failed_payments = []  

    routing_tree = tree

    # Function to select paths based on the path type
    def select_path(graph, source, target, path_type, tree = routing_tree):
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
            paths = list(nx.all_simple_paths(graph, source=source, target=target, cutoff=NUM_PATHS_SHORT))
            if paths:
                path = random.choice(paths)
                return path
            else:
                return None

        elif path_type == "lsst":
            # visualize_graph(tree)
            if nx.has_path(tree, source, target):
                # Get the shortest path
                path = nx.shortest_path(tree, source=source, target=target)
                return path
            else:
                print(f"There spans no path from {source} to {target}")
                return None
        else:
            raise ValueError(f"Invalid path type: {path_type}")

    demand = demand_matrix[source, target]
    # Only attempt to route the specific payment for the current (source, target) pair
    # demand = 1

    if demand > 0:  # Exclude zero demand pairs
        # Attempt to route on all spanning trees if using LSST
        if path_type == "lsst":
            path = select_path(graph, source, target, path_type, tree=routing_tree)
            print(path)

            # Determine the minimum credit available along the path
            min_credit = min(credit_matrix[u][v] for u, v in zip(path[:-1], path[1:]))
            print(f"Source: {source}, destination: {target}.")
            print(f"min_credit: {min_credit}, demand: {demand}.")

            if min_credit >= demand:
                # Successful payment scenario
                for u, v in zip(path[:-1], path[1:]):
                    credit_matrix[u][v] -= demand
                    credit_matrix[v][u] += demand
                    # credit_matrix[u][v] -= 1
                    # credit_matrix[v][u] += 1
                success_payments.append((source, target, demand))
                # demand_matrix[source, target] -= 1  # Update the demand matrix
                demand_matrix[source, target] -= demand
            elif min_credit == 0:
                # print(f"Payment failed: {source} -> {target}")
                # exit(0)
                failed_payments.append((source, target, demand_matrix[source, target]))
                return success_payments, failed_payments
            else:
                for u, v in zip(path[:-1], path[1:]):
                    credit_matrix[u][v] -= min_credit
                    credit_matrix[v][u] += min_credit
                    # credit_matrix[u][v] -= 1
                    # credit_matrix[v][u] += 1
                demand_matrix[source, target] -= min_credit
                # demand_matrix[source, target] -= 1
                success_payments.append((source, target, min_credit))
        # If not using LSST
        else:
            path = select_path(graph, source, target, path_type)
            # It would not happen as I already test if a graph is connected or not adn there is always a path between two nodes in a connected graph
            if path is None:
                failed_payments.append((source, target, demand))
                TOTAL_DEMAND_FAILED += demand_matrix[source, target]    
                # demand_matrix[source, target] = 0
                return success_payments, failed_payments  # Skip further processing
            else:
                min_credit = min(credit_matrix[u][v] for u, v in zip(path[:-1], path[1:]))
                demand = demand_matrix[source, target]
                #demand = 1

                if min_credit >= demand:
                    for u, v in zip(path[:-1], path[1:]):
                        credit_matrix[u][v] -= demand
                        credit_matrix[v][u] += demand
                        # credit_matrix[u][v] -= 1
                        # credit_matrix[v][u] += 1
                    success_payments.append((source, target, demand))
                    demand_matrix[source, target] -= demand
                    # demand_matrix[source, target] -= 1  # Update the demand matrix
                elif min_credit == 0:
                    failed_payments.append((source, target, demand_matrix[source, target]))
                    TOTAL_DEMAND_FAILED += demand_matrix[source, target]    
                    # demand_matrix[source, target] = 0
                    return success_payments, failed_payments
                else:
                    for u, v in zip(path[:-1], path[1:]):
                        credit_matrix[u][v] -= min_credit
                        credit_matrix[v][u] += min_credit
                        # credit_matrix[u][v] -= 1
                        # credit_matrix[v][u] += 1
                    demand_matrix[source, target] -= min_credit
                    # demand_matrix[source, target] -= 1
                    success_payments.append((source, target, min_credit))

    return success_payments, failed_payments


def simulate_routing(demand_matrix, credit_matrix, graph, path_type=PATH_TYPE):
    global EPOCH_LEN

    all_success_payments = []  # Track all successful payments
    all_failed_payments = []   # Track all failed payments

    used_trees = set()

    # Initialize a round counter
    round_num = 0

    if path_type != "lsst":
        # Continue looping until the demand matrix is zero or until a set number of rounds are executed

        while round_num < ROUNDS and not np.all(demand_matrix == 0):
            # Create demand pairs based on the current demand matrix
            demand_pairs = [(i, j) for i in range(len(demand_matrix)) for j in range(len(demand_matrix)) if i != j and demand_matrix[i][j] > 0]
            
            # Check if there are any demand pairs to route
            if not demand_pairs:
                print("No more valid demand pairs to route.")
                break
            
            demand_pairs = random.sample(demand_pairs, len(demand_pairs))

            # Iterate over all valid src-dest pairs
            for source, target in demand_pairs:
                # Route a single payment for this src-dest pair
                success_payments, failed_payments = route_single_payment(
                    graph, demand_matrix, credit_matrix, source, target, path_type, tree=None
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

                # Check if all demands have been fulfilled after each attempt
                if np.all(demand_matrix == 0):
                    print(f"All demands fulfilled by round {round_num}")
                    break  

                if round_num >= ROUNDS: break
                

        return all_success_payments, all_failed_payments, round_num
    else:
        spanning_trees = generate_and_validate_spanning_trees(graph)
        # Continue looping until the demand matrix is zero or until a set number of rounds are executed
        while round_num < ROUNDS and not np.all(demand_matrix == 0):
            demand_pairs = [(i, j) for i in range(len(demand_matrix)) for j in range(len(demand_matrix)) if i != j and demand_matrix[i][j] > 0]

            demand_pairs = random.sample(demand_pairs, len(demand_pairs))

            # choosing a random tree and adding it to the set
            tree = random.choice(spanning_trees)
            used_trees.add(tree)

            if len(used_trees) == len(spanning_trees):
                used_trees.clear()
                tree = random.choice(spanning_trees)
                used_trees.add(tree)


            if EPOCH_LEN<0:
                spanning_tree_set = set(spanning_trees)
                intersection = spanning_tree_set.intersection(used_trees)
                tree = random.choice(list(intersection))
                EPOCH_LEN = RESET_EPOCH

            # Check if there are any demand pairs to route
            if not demand_pairs:
                print("No more valid demand pairs to route.")
                return all_success_payments, all_failed_payments

            print(f"Round:{round_num}, Total rounds: {ROUNDS}")
            
            # Iterate over all valid src-dest pairs
            for source, target in demand_pairs:
                # Route a single payment for this src-dest pair
                success_payments, failed_payments = route_single_payment(
                    graph, demand_matrix, credit_matrix, source, target, path_type, tree=tree
                )

                round_num += 1  # Count only valid routing attempts
                EPOCH_LEN -= 1
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

                # Check if all demands have been fulfilled after each attempt
                if np.all(demand_matrix == 0):
                    # print(f"All demands fulfilled by round {round_num}")
                    break  # Exit the loop if all demands are fulfilled

                if round_num >= ROUNDS: break

                if EPOCH_LEN<0:
                    spanning_tree_set = set(spanning_trees)
                    intersection = spanning_tree_set.intersection(used_trees)
                    tree = random.choice(list(intersection))
                    EPOCH_LEN = RESET_EPOCH
                    # visualize_graph(tree)
                    
        return all_success_payments, all_failed_payments, round_num


