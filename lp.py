import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import generate_demand_matrix as gdm
import cost_matrix as cm

import routing as rt

from graph import generate_graph, visualize_graph
from utils import *

def calculate_src_dest_pairs(demand_matrix):
    count = 0
    for i in range(len(demand_matrix)):
        for j in range(len(demand_matrix[0])):
            if i != j and demand_matrix[i][j] != 0:  # Exclude self-pairs

                count += 1
    return count

# Main function
def main():
    G = generate_graph()
    demand_mat = gdm.generate_demand_matrix()
    credit_mat = cm.generate_credit_matrix()
    print(demand_mat)
    print(credit_mat)

    # sleep(7)

    num_rounds = ROUNDS
    print(f"The number of rounds are: {num_rounds}")
    # Calculate the number of source-destination pairs
    num_pairs = calculate_src_dest_pairs(demand_mat)
    print(f"Number of source-destination pairs: {num_pairs}")


    if num_rounds < num_pairs:
        print("The demand matrix cannot be satisfied as there are less rounds than the total number of src dest pairs")
        exit(0)

    # Visualize the initial graph
    visualize_graph(G)
    path_type = PATH_TYPE

    start_time = time.time()
    all_success_payments, all_failed_payments = rt.simulate_routing(demand_mat, credit_mat, G, path_type)
    end_time = time.time()

    
    # Output final results
    print("Final successful payments:", all_success_payments)
    print("Final failed payments:", all_failed_payments)

    num_failed_payments = len(all_failed_payments)

    print(f"Throughput: {(num_pairs-num_failed_payments)/num_pairs}")

    print(f"Total time to simulate the payments: {end_time-start_time}")

if __name__ == '__main__':
    main()

