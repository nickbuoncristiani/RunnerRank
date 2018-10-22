class Athlete:

	def __init__(self, name, id):
		self.name = name #e.g Cooper Teare
		self.id = id
		self.rank_map = {} #e.g {'xc' : 10, '1600m' : 1} 

	def add_rank(self, event, rank):
		self.rank_map[event] = rank

	def __eq__(self, other):
		return isinstance(other, Athlete) and self.id == other.id

	def __hash__(self):
		return self.id