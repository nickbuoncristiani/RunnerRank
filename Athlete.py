class Athlete:

	def __init__(self, name, id):
		self.name = name #e.g Cooper Teare
		self.id = id
		self.rank_map = {} #e.g {'xc' : 10, '1600m' : 1, ...}
		self.losses = 0

	def add_rank(self, event, rank):
		self.rank_map[event] = rank

	def lose(self, other, graph):
		self.losses += 1
		if self in graph and other in graph.adj[self]:
			graph[self][other]['weight'] += 1
		else:			
			graph.add_edge(self, other, weight = 1)

	def __eq__(self, other):
		return isinstance(other, Athlete) and self.id == other.id

	def __hash__(self):
		return self.id

	def __repr__(self):
		return str(self.id)

	def __str__(self):
		return self.name + '\n' + str(self.id) + '\n' + str(self.rank_map)