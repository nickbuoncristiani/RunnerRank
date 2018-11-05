import numpy as np

#Pass in matrix and get list of rankings.
def get_rankings(matrix, accuracy = 10):
	N = len(matrix)
	current_rankings = [1 for athlete in matrix]
	for a in range(accuracy):
		in_progress = current_rankings[:]
		for i in range(len(matrix)):
			new_rank = 0
			for j in range(len(matrix)):
				new_rank += current_rankings[j] * matrix[i][j]
			in_progress[i] = new_rank
		current_rankings = in_progress
	return current_rankings

def get_matrix_from_save(save):
	web = save.athlete_web
	matrix = []
	for i in range(len(save.athlete_indices)):
		id_2 = save.athlete_indices[i]
		matrix.append([])
		for j in range(len(save.athlete_indices)):
			id_1 = save.athlete_indices[j]
			if id_1 != id_2 and id_1 in web and id_2 in web[id_1]:
				matrix[i].append(len(web[id_1][id_2]['losses']) / save[id_1].losses)
			else: 
				matrix[i].append(0)
	return np.array(matrix)

#Prints sum of individual columns
def test_columns(matrix):
	for i in range(len(matrix)):
		sum = 0
		for j in range(len(matrix[0])):
			sum += matrix[j][i]
		print(sum)


