import numpy as np
from utils import *

def generate_demand_matrix():

    n = GRAPH_SIZE # This is the size of the grph or the number of nodes in teh graph

    if SRC_TYPE == "test":
        demand_mat = np.zeros([n, n])
        demand_mat[0, 1] = 1.
        demand_mat[1, 0] = 1.
        demand_mat[1, 3] = 1.
        demand_mat[3, 1] = 1. 

    elif SRC_TYPE == "uniform":
        pass

    return demand_mat

