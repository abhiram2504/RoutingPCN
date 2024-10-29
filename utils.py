""" Graph type
erdos-renyi
grid
"""
GRAPH_TYPE = 'erdos-renyi'

""" Graph Size """
GRAPH_SIZE = 100
# When using a grid graph
GRID_GRAPH_SIZE = 5

""" Demand matrix
Types of demand:
circular
test
uniform
circular_no_2_cycles

scale the mean 
scale the std_dev
"""

DEMAND_TYPE = 'circular'
MEAN = 0
STD_DEV = 1000
MEAN_AMT = 0 
STD_DEV_AMT = 10

""" Demand Type, valid for uniform or test demand """
DEMAND_AMT = 10

""" Credit matrix
Types:
uniform
random
"""
CREDIT_TYPE = 'uniform'

""" Credit Amount """
CREDIT_AMT = 15

""" Number of rounds """
ROUNDS = GRAPH_SIZE*25

""" Path type
shortest
random
lsst
"""
PATH_TYPE = "lsst"

""" Number of paths(shortest) """
NUM_PATHS_SHORT = 3

""" Epoch Len """
EPOCH_LEN = GRAPH_SIZE
RESET_EPOCH = EPOCH_LEN

""" Number of paths(random) """
NUM_PATHS_SHORT = 3

""" The parameter for erdos renyi """
ERDOS_P_EDGE = 0.2

""" To increase the weight on the edges (Creating Spanning trees)"""
ALPHA = 1.3

""" RAND SEED """
RAND_SEED = 12

"""
This is the parameter for routing the first K paths in the network in lsst path type
"""
K = 0  