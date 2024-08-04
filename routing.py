import networkx as nx
import numpy as np

# Function to route payments for one round
def route_payment_round(graph, demand_matrix, credit_matrix):
    num_nodes = len(demand_matrix)  # Number of nodes in the network
    success_payments = []  # List to keep track of successful payments
    failed_payments = []  # List to keep track of failed payments

    # Iterate over all pairs of nodes
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and demand_matrix[i, j] > 0:  # Exclude self-pairs and zero demand pairs
                # Find the shortest path between source i and target j
                path = nx.shortest_path(graph, source=i, target=j)
                
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

                # After routing for one pair, stop and return the results
                return success_payments, failed_payments

    # Return results if no payments were routed in this round
    return success_payments, failed_payments

# Function to simulate routing over multiple rounds
def simulate_routing(demand_matrix, credit_matrix, num_rounds, graph):
    all_success_payments = []  # List to keep track of all successful payments
    all_failed_payments = []  # List to keep track of all failed payments

    # Iterate over the number of rounds
    for round_num in range(1, num_rounds + 1):
        # Route payments for this round
        success_payments, failed_payments = route_payment_round(graph, demand_matrix, credit_matrix)
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
