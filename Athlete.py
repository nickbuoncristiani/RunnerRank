class Athlete:

	def __init__(self, name, id):
		self.name = name #e.g Cooper Teare
		self.id = id
		self.rank_map = {} #e.g {'xc' : 10, '1600m' : 1, ...}
		self.losses = 0

	def add_rank(self, event, rank):
		self.rank_map[event] = rank

	def lose(self, other_ID, date, save):
		self.losses += 1
		if self.id in save.athletes_by_id and other_ID in save.athlete_web.adj[self.id]:
			save.athlete_web[self.id][other_ID]['dates_of_losses'].append(date)
		else:
			save.athlete_web.add_edge(self.id, other_ID, dates_of_losses = [date])

	def __eq__(self, other):
		return isinstance(other, Athlete) and self.id == other.id

	def __hash__(self):
		return self.id

	def __repr__(self):
		return str(self.id)

	def __str__(self):
		return self.name + '\n' + str(self.id) + '\n' + str(self.rank_map)
