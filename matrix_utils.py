import numpy as np
import time

#Pass in matrix and get list of rankings.
def get_rankings(matrix, precision = 1000):
	N = len(matrix)
	current_scores = np.array([1 for i in range(N)])
	for a in range(precision):
		in_progress = []
		for i in range(N):
			new_rank = np.dot(current_scores, matrix[i])
			in_progress.append(new_rank)
		new_scores = np.array(in_progress)
		current_scores = new_scores
	return current_scores

def get_matrix_from_save(save):
	web = save.athlete_web
	matrix = []
	for i in range(len(save)):
		id_2 = save.athlete_at_index(i)
		matrix.append([])
		for j in range(len(save)):
			id_1 = save.athlete_at_index(j)
			if id_1 != id_2 and id_2 in web[id_1]:
				matrix[i].append(len(web[id_1][id_2]['losses']) / save[id_1].losses)
			else: 
				matrix[i].append(0)
	return np.array(matrix)

#Prints sum of individual columns. Should be all close to one.
def test_columns(matrix):
	for i in range(len(matrix)):
		sum = 0
		for j in range(len(matrix[0])):
			sum += matrix[j][i]
		print(sum)


