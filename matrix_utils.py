import numpy as np

#Pass in matrix and get list of rankings.
def get_rankings(matrix, precision = 100):
	current_scores = np.full(len(matrix), 1)
	for p in range(precision):
		current_scores = np.matmul(matrix, current_scores)
	return current_scores

#Prints sum of individual columns. Should be all close to one.
def test_columns(matrix):
	for i in range(len(matrix)):
		sum = 0
		for j in range(len(matrix[0])):
			sum += matrix[j][i]
		print(sum)


