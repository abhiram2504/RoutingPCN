import numpy as np 

from utils import *

""" generate circulation demand for 'num_nodes' number of nodes,
with average total demand at a node equal to 'mean', and a 
perturbation of 'std_dev' """
def circ_demand(num_nodes, mean, std_dev):

	np.random.seed(RAND_SEED)

	assert type(mean) is int
	assert type(std_dev) is int

	demand_dict = {}

	""" sum of 'mean' number of random permutation matrices """
	""" note any permutation matrix is a circulation demand """
	for i in range(mean):
		perm = np.random.permutation(num_nodes)
		for j, k in enumerate(perm):
			if (j, k) in demand_dict.keys():
				demand_dict[j, k] += 1
			else:
				demand_dict[j, k] = 1

	""" add 'std_dev' number of additional cycles to the demand """
	for i in range(std_dev):
		cycle_len = np.random.choice(range(1, num_nodes+1))
		cycle = np.random.choice(num_nodes, cycle_len)
		cycle = set(cycle)
		cycle = list(cycle)
		cycle.append(cycle[0])
		for j in range(len(cycle[:-1])):
			if (cycle[j], cycle[j+1]) in demand_dict.keys():
				demand_dict[cycle[j], cycle[j+1]] += 1
			else:
				demand_dict[cycle[j], cycle[j+1]] = 1			

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

    return demand_matrix

if __name__=='__main__':
	np.random.seed(11)
	demand_dict = circ_demand(5, 25, 4)
	demand_matrix = demand_dict_to_matrix(demand_dict, 5)
	print(demand_dict)
	print("Demand Matrix:\n", demand_matrix)
