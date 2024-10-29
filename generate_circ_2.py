import numpy as np # type: ignore
from utils import *

def circ_demand_no_2_cycles(num_nodes, mean, std_dev):

	assert type(mean) is int
	assert type(std_dev) is int

	demand_dict = {}

	""" sum of 'mean' number of random permutation matrices """
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
		cycle_len = np.random.choice(range(1, num_nodes+1))
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
			demand_dict[i, j] = 0

	""" create demand matrix """
	demand_mat = np.zeros([num_nodes, num_nodes])
	for (i, j) in demand_dict.keys(): 
		demand_mat[i, j] = demand_dict[i, j]

	""" remove 2-cycles from the demand matrix """
	for (i, j) in demand_dict.keys(): 
		if demand_mat[j, i] > 0:
			x = min(demand_mat[i, j], demand_mat[j, i])
			demand_mat[i, j] -= x 
			demand_mat[j, i] -= x 

	return demand_mat

def main(): 
	np.random.seed(11)
	n = 100
	mean = 200
	std_dev = 20 

	demand_mat = circ_demand_no_2_cycles(n, mean, std_dev)

	print("Demand density: ", 100*np.sum(demand_mat > 0)/(n*n), "%")
	print(demand_mat)			

if __name__=='__main__':
	main() 