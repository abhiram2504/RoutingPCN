""" Graph type
erdos-renyi
grid
"""
GRAPH_TYPE = 'grid'

""" Graph Size """
GRAPH_SIZE = 25 
# When using a grid graph
GRID_GRAPH_SIZE = 5

""" Demand matrix
Types of demand:
circular
test
uniform
"""

DEMAND_TYPE = 'circular'
MEAN = 25
STD_DEV = 5

""" Demand Type, valid for uniform or test demand """
DEMAND_AMT = 10

""" Credit matrix
Types:
uniform
random
"""
CREDIT_TYPE = 'uniform'

""" Credit Amount """
CREDIT_AMT = 10

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

EPOCH_LEN = GRAPH_SIZE*2
RESET_EPOCH = EPOCH_LEN

""" Number of paths(random) """

""" The parameter for erdos renyi """
ERDOS_P_EDGE = 0.5

""" To increase the weight on the edges (Creating Spanning trees)"""
ALPHA = 1.5

""" RAND SEED """
RAND_SEED = 12