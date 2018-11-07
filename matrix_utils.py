import numpy as np
import time

#Pass in matrix and get list of rankings.
def get_rankings(matrix, precision = 10):
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

#Prints sum of individual columns. Should be all close to one.
def test_columns(matrix):
	for i in range(len(matrix)):
		sum = 0
		for j in range(len(matrix[0])):
			sum += matrix[j][i]
		print(sum)


