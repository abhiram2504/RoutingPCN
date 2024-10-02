import numpy as np

from utils import *

def generate_credit_matrix():
    n = GRAPH_SIZE

    if CREDIT_TYPE == 'uniform':
        credit_mat = np.ones([n, n]) * CREDIT_AMT
    elif CREDIT_TYPE == 'random':
        np.random.seed(RAND_SEED)
        credit_mat = np.triu(np.random.rand(n, n), 1) * 2 * CREDIT_AMT
        credit_mat += credit_mat.transpose()
        
    return credit_mat
