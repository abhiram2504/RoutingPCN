""" Graph type """
GRAPH_TYPE = 'erdos-renyi'

""" Graph Size """
GRAPH_SIZE = 8
# When using a grid graph
GRID_GRAPH_SIZE = 5

""" Demand matrix
Types of demand:
circular
test
uniform
"""
DEMAND_TYPE = 'uniform'
MEAN = 10
STD_DEV = 1

""" Demand Type, valid for uniform or test demand """
DEMAND_AMT = 100

""" Credit matrix
Types:
uniform
random
"""
CREDIT_TYPE = 'uniform'

""" Credit Amount """
CREDIT_AMT =  50

""" Number of rounds """
ROUNDS = GRAPH_SIZE*1

""" Path type
shortest
random
lsst
"""
PATH_TYPE = "shortest"

""" Number of paths(shortest) """
NUM_PATHS_SHORT = 3

""" Epoch Len """
EPOCH_LEN = GRAPH_SIZE
RESET_EPOCH = EPOCH_LEN

""" Number of paths(random) """

""" The parameter for erdos renyi """
ERDOS_P_EDGE = 0.3

""" To increase the weight on the edges (Creating Spanning trees)"""
ALPHA = 1.5

""" RAND SEED """
RAND_SEED = 12 # This is to create the credit for each node

# impletemnt time to understand how long it takes
# generate circualriotns, so that shortest path would fail in certain scenarios or the random path