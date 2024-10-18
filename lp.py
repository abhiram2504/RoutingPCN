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

    total_demand = sum(sum(demand_mat))


    num_rounds = ROUNDS
    # print(f"The number of rounds are: {num_rounds}")
    # Calculate the number of source-destination pairs
    num_pairs = calculate_src_dest_pairs(demand_mat)
    print(f"Number of source-destination pairs: {num_pairs}")

    # if num_rounds < num_pairs:
    #     print("The demand matrix cannot be satisfied as there are less rounds than the total number of src dest pairs")
    #     exit(0)

    # Visualize the initial graph
    # visualize_graph(G)
    path_type = PATH_TYPE

    start_time = time.time()
    all_success_payments, all_failed_payments, round_num = rt.simulate_routing(demand_mat, credit_mat, G, path_type)
    end_time = time.time()
    

    # Output final results
    # print("Final successful payments:", all_success_payments)
    # print("Final failed payments:", all_failed_payments)

    # # num_failed_payments = len(all_failed_payments)
    # if path_type != "lsst":
    #     # print(f"Total failed demand: {rt.TOTAL_DEMAND_FAILED}")
    #     # print(f"Throughput: {(total_demand - rt.TOTAL_DEMAND_FAILED)/total_demand}")
    #     total_not_routed = sum(sum(demand_mat))
    #     print(f"Total failed demand: {total_not_routed}")
    #     print(f"Throughput: {(total_demand - total_not_routed)/total_demand}")
    # else:

    # We check how much demand is remaining in the demand_mat
    # and then that would we the demand that is not going to to be routed ans the minum number of rounds
    # that we go for lsst if something is not achievale would be TOTAL_ROUNDS
    total_not_routed = sum(sum(demand_mat))
    failed_rounds = len(all_failed_payments)
    
    print(f"Total demand: {total_demand}")
    print(f"Total failed demand: {total_not_routed}")
    print(f"Total successful demand: {total_demand - total_not_routed}")
    print(f"Throughput: {(total_demand - total_not_routed)/total_demand}")
    print(f"Total number of rounds used for routing: {round_num}")
    print(f"Percentage of failed rounds: {failed_rounds/num_rounds}")
    print(f"Total time to simulate the payments: {end_time-start_time}")

if __name__ == '__main__':
    main()
