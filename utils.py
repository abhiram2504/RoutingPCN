""" 
Graph types:
1. test
2. erdos-renyi
3. grid
"""
GRAPH_TYPE = 'grid'

""" Graph Size """
GRAPH_SIZE = 100
GRID_GRAPH_SIZE = 10

""" Demand matrix
Types of demand:
1. circular
2. test
3. uniform
4. circular_no_2_cycles
"""

DEMAND_TYPE = 'circular_no_2_cycles'
MEAN = 20
STD_DEV = 1
MEAN_AMT = 10
STD_DEV_AMT = 1

""" Demand Type, valid for uniform or test demand """
DEMAND_AMT = 60

""" Credit matrix
Types: 
1. uniform  
2. random
"""

CREDIT_TYPE = 'uniform'

""" Credit Amount """
CREDIT_AMT = 50

""" Number of rounds """
ROUNDS = GRAPH_SIZE*100

""" 
Path type:
1. shortest
2. random
3. lsst
"""
PATH_TYPE = "shortest"

""" Epoch Len """
EPOCH_LEN = GRAPH_SIZE*100
RESET_EPOCH = EPOCH_LEN

""" Number of paths(random) """
NUM_PATHS_SHORT = 3

""" The parameter for erdos renyi """
ERDOS_P_EDGE = 0.1

""" To increase the weight on the edges (Creating Spanning trees)"""
ALPHA = 1.3 

""" RAND SEED """
RAND_SEED = 1
