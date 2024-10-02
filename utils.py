""" Graph type """
GRAPH_TYPE = 'erdos-renyi'

""" Demand matrix """
DEMAND_TYPE = 'circular'

""" Credit matrix """
CREDIT_TYPE = 'uniform'

""" Credit Amount """
CREDIT_AMT = 10

""" Graph Size """
GRAPH_SIZE = 5

""" Number of rounds """
ROUNDS = GRAPH_SIZE**3

""" Path type """
PATH_TYPE = "shortest"

""" Epoch Len """
EPOCH_LEN = GRAPH_SIZE**2 - GRAPH_SIZE

""" Demand Type """
DEMAND_AMT = 15

""" The parameter for erdos renyi """
ERDOS_P_EDGE = 0.5

""" To reduce the weight on the edges (Creating Spanning trees)"""
ALPHA = 1.2

""" RAND SEED """
RAND_SEED = 11 # This is to create the credit for each node

# impletemnt time to understand how long it takes
# generate circualriotns, so that shortest path would fail in certain scenarios or the random path