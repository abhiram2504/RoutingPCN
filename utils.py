""" Graph type """
GRAPH_TYPE = 'erdos-renyi'

""" Demand matrix """
"""
Types of demand:
circular
test
uniform
"""

DEMAND_TYPE = 'circular'
MEAN = 4
STD_DEV = 4

""" Credit matrix """
CREDIT_TYPE = 'uniform'

""" Credit Amount """
CREDIT_AMT =  1

""" Graph Size """
GRAPH_SIZE = 100

GRID_GRAPH_SIZE = 5

""" Number of rounds """
ROUNDS = 10 * GRAPH_SIZE

""" Path type """
PATH_TYPE = "random"

""" Number of paths(shortest) """
NUM_PATHS_SHORT = 3

""" Epoch Len """
EPOCH_LEN = GRAPH_SIZE**2 - GRAPH_SIZE

""" Demand Type, valid for uniform or test demand """
DEMAND_AMT = 15000

""" The parameter for erdos renyi """
ERDOS_P_EDGE = 0.5

""" To increase the weight on the edges (Creating Spanning trees)"""
ALPHA = 1.2

""" RAND SEED """
RAND_SEED = 12 # This is to create the credit for each node

# impletemnt time to understand how long it takes
# generate circualriotns, so that shortest path would fail in certain scenarios or the random path