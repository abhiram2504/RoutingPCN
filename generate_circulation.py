import numpy as np  # type: ignore

from utils import *

""" generate circulation demand for 'num_nodes' number of nodes,
with average total demand at a node equal to 'mean', and a 
perturbation of 'std_dev' """
def circ_demand(num_nodes, mean, std_dev):

	np.random.seed(RAND_SEED)

	assert type(mean) is int
	assert type(std_dev) is int

	demand_dict = {}

	""" sum of 'mean' number of random permutation
 matrices """
	""" note any permutation matrix is a circulation demand """
	for i in range(mean):
		perm = np.random.permutation(num_nodes)
		for j, k in enumerate(perm):
			if (j, k) in demand_dict.keys():
				demand_dict[j, k] += MEAN_AMT
			else:
				demand_dict[j, k] = MEAN_AMT

	""" add 'std_dev' number of additional cycles to the demand """
	for i in range(std_dev):
		# cycle_len = np.random.choice(range(1, num_nodes+1))
		cycle_len = 3
		cycle = np.random.choice(num_nodes, cycle_len)
		cycle = set(cycle)
		cycle = list(cycle)
		cycle.append(cycle[0])
		for j in range(len(cycle[:-1])):
			if (cycle[j], cycle[j+1]) in demand_dict.keys():
				demand_dict[cycle[j], cycle[j+1]] += STD_DEV_AMT
			else:
				demand_dict[cycle[j], cycle[j+1]] = STD_DEV_AMT		

	""" remove diagonal entries of demand matrix """
	for (i, j) in demand_dict.keys():
		if i == j:
			# print(f"i:{i}, j:{j}, demand:{demand_dict[i, j]}") 
			demand_dict[i, j] = 0
	return demand_dict

def demand_dict_to_matrix(demand_dict, num_nodes):
    demand_matrix = np.zeros((num_nodes, num_nodes), dtype=int)

    # Iterate through demand_dict and populate the matrix
    for (i, j), value in demand_dict.items():
        demand_matrix[i][j] = value
        
    scaled_mat = scale_demand_matrix(demand_matrix, TARGET_SUM)

    return scaled_mat

def scale_demand_matrix(demand_matrix, target_sum):
	sum_demand = np.sum(demand_matrix)
	scale_factor = target_sum / sum_demand
	scaled_matrix = np.round(demand_matrix * scale_factor).astype(int)
	return scaled_matrix


	
