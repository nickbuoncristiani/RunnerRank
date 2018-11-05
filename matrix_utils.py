import numpy as np

#Pass in eigenvals/vectors and receive corresponding rankings.
def get_rankings(eig_vals, eig_vectors):
	index = 0
	closest_index = 0
	closest = 2
	eigs = 0
	while index < len(eig_vals):
		if basically_one(eig_vals[index]):
			eigs += 1
		if eig_vals[index] < 1 and abs(eig_vals[index] - 1) <= closest:
			closest = abs(eig_vals[index] - 1)
			closes_index = index
		index += 1
	print(eigs)
	return eig_vectors[closest_index]

def get_matrix_from_save(save):
	web = save.athlete_web
	matrix = []
	for i in range(len(save.athlete_indices)):
		matrix.append([])
		for j in range(len(save.athlete_indices)):
			id_1 = save.athlete_indices[j]
			id_2 = save.athlete_indices[i]
			if id_1 != id_2 and id_1 in web and id_2 in web[id_1]:
				matrix[i].append(len(web[id_1][id_2]['losses']) / save[id_1].losses)
			else:
				matrix[i].append(0)
	matrix[0][0] = 1
	return matrix


#To handle float precision. Hopefully we don't have to use this garbage.
def basically_one(n):
	return abs(n - 1) < .000000001


