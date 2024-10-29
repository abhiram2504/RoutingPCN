import numpy as np
from utils import *
import random as rand
import time

from generate_circulation import circ_demand, demand_dict_to_matrix
from generate_circ_2 import circ_demand_no_2_cycles

def generate_demand_matrix():

    n = GRAPH_SIZE # This is the size of the grph or the number of nodes in teh graph

    if DEMAND_TYPE == "test":
        demand_mat = np.zeros([n, n])
        demand_mat[0, 1] = 6.
        demand_mat[1,2] = 6.
        demand_mat[2,3] = 6.
        demand_mat[3,1] = 7.
        np.fill_diagonal(demand_mat, 0.0)
    elif DEMAND_TYPE == "uniform":
        demand_mat = np.ones([n, n])    
        for i in range(len(demand_mat)):
            for j in range(len(demand_mat[0])):
                demand_mat[i][j] *= rand.randint(0, DEMAND_AMT)
        np.fill_diagonal(demand_mat, 0.0)
    elif DEMAND_TYPE == "circular":
        demand_dict = circ_demand(n, MEAN, STD_DEV)
        demand_mat = demand_dict_to_matrix(demand_dict, n)
        cnt = np.count_nonzero(demand_mat)
    elif DEMAND_TYPE == "circular_no_2_cycles":
        demand_dict = circ_demand_no_2_cycles(n, MEAN, STD_DEV)
        demand_mat = demand_dict_to_matrix(demand_dict, n)
        cnt = np.count_nonzero(demand_mat)
        print("Demand density: ", 100*cnt/(n*n), "%")
    return demand_mat

