import numpy as np
from utils import *
import random as rand

def generate_demand_matrix():

    n = GRAPH_SIZE # This is the size of the grph or the number of nodes in teh graph

    if SRC_TYPE == "test":
        demand_mat = np.zeros([n, n])
        demand_mat[0, 1] = 2.
        demand_mat[1, 2] = 3.

    elif SRC_TYPE == "uniform":
        demand_mat = np.ones([n, n])
        np.fill_diagonal(demand_mat, 0.0)       
        demand_mat = demand_mat * rand.randint(0, CREDIT_AMT) 


    return demand_mat

