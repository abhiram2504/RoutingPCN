import numpy as np

from utils import *

def generate_credit_matrix():
    n = GRAPH_SIZE

    if CREDIT_TYPE == 'uniform':
        credit_mat = np.ones([n, n]) * CREDIT_AMT

    print(credit_mat)
    return credit_mat
