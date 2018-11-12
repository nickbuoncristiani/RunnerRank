class Athlete:

	def __init__(self, id, name):
		self.name = name #e.g Cooper Teare
		self.id = id
		self.results = {} 
		self.losses = 0
		self.wins = 0
		self.outgoing_points = 0

	def add_result(self, meet_name, time):
		self.results[meet_name] = time

	def lose(self, outgoing_points):
		self.losses += 1
		self.outgoing_points += outgoing_points

	def win(self):
		self.wins += 1

	def __eq__(self, other):
		return isinstance(other, Athlete) and self.id == other.id

	def __hash__(self):
		return self.id

	def __repr__(self):
		return self.name
