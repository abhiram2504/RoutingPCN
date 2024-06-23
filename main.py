import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import generate_demand_matrix as gdm
import routing as rt

# Function to generate a Rényi random graph
def generate_renyi_random_graph_with_weights(n, p, weight=1000):
    G = nx.erdos_renyi_graph(n, p)
    for u, v in G.edges():
        G[u][v]['weight'] = weight
    return G

# Function to generate payments per round using an exponential distribution
def generate_random_payments(demand_matrix, num_rounds):
    payments = np.zeros((num_rounds,) + demand_matrix.shape)
    for r in range(num_rounds):
        for i in range(len(demand_matrix)):
            for j in range(len(demand_matrix[0])):
                if i != j:  # Exclude self-payments
                    demand = demand_matrix[i, j]  # Demand between node i and j
                    if demand < 0:  # Check if demand is valid
                        raise ValueError("Invalid demand value")
                    # Compute the payment probability (p) based on demand
                    if(demand == 0): continue
                    p = min(1.0, 1.0 / demand)  # Ensure p is between 0 and 1
                    payments[r, i, j] = np.random.geometric(p)  # Assign payment to corresponding round, i, and j
    return payments

# Route payments through the network and update capacities
def route_and_update(graph, payments):
    success_payments = []
    failed_payments = []
    for r in range(len(payments)):
        for i in range(len(payments[0])):
            for j in range(len(payments[0][0])):
                if i != j:
                    payment = payments[r, i, j]
                    if rt.route_payment(graph, i, j, payment):
                        success_payments.append((i, j, payment))
                    else:
                        failed_payments.append((i, j, payment))
    return success_payments, failed_payments

# Main function
def main():
    matrix_size = int(input("Enter the matrix size: "))
    p = 0.8  
    G = generate_renyi_random_graph_with_weights(matrix_size, p)

    # Generate a uniform demand matrix
    T = gdm.generate_demand_matrix(G, 1000)

    print("Demand Matrix:")
    print(T)

    num_rounds = int(input("Enter the number of rounds: "))

    # Generate payments based on the demand matrix
    payments = generate_random_payments(T, num_rounds)

    # Route payments through the network and update capacities
    success_payments, failed_payments = route_and_update(G, payments)

    print("Successful Payments:")
    for payment in success_payments:
        print(f"From Node {payment[0]} to Node {payment[1]}: {payment[2]}")

    print(f"The number of successful payments is {len(success_payments)}")

    print("\nFailed Payments:")
    for payment in failed_payments:
        print(f"From Node {payment[0]} to Node {payment[1]}: {payment[2]}")

    print(f"The number of failed payments is {len(failed_payments)}")

    # Calculate and print throughput as a percentage of total demand capacity
    total_successful_payments = sum(payment[2] for payment in success_payments)
    total_demand_capacity = np.sum(T)
    throughput_percentage = (total_successful_payments / total_demand_capacity) * 100
    print(f"Throughput: {throughput_percentage:.2f}% of total demand capacity")

if __name__ == '__main__':
    main()
