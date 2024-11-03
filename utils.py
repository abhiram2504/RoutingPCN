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
MEAN = 100
STD_DEV = 1
MEAN_AMT = 1
STD_DEV_AMT = 1

""" Demand Type, valid for uniform or test demand """
DEMAND_AMT = 100

""" Credit matrix
Types: 
uniform
random
"""
CREDIT_TYPE = 'uniform'

""" Credit Amount """
CREDIT_AMT = 50

""" Number of rounds """
ROUNDS = GRAPH_SIZE*500

""" Path type
shortest
random
lsst
"""
PATH_TYPE = "lsst"

""" Number of paths(shortest) """
NUM_PATHS_SHORT = 3

""" Epoch Len """
EPOCH_LEN = GRAPH_SIZE*2
RESET_EPOCH = EPOCH_LEN

""" Number of paths(random) """
NUM_PATHS_SHORT = 3

""" The parameter for erdos renyi """
ERDOS_P_EDGE = 0.1

""" To increase the weight on the edges (Creating Spanning trees)"""
ALPHA = 1.3

""" RAND SEED """
RAND_SEED = 12
