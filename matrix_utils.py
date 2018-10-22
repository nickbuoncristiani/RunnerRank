import numpy as np

#Pass in eigenvals/vectors and receive corresponding rankings.
def get_rankings(eig_vals, eig_vectors):
	eig_one_arr = list(map(basically_one, eig_vals))
	assert True in eig_one_arr
	return eig_vectors[:,eig_one_arr.index(True)]

#To handle float precision. Hopefully we don't have to use this garbage.
def basically_one(n):
	return abs(n - 1) < .000000000000001


