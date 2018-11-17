class Athlete:

	def __init__(self, id, name):
		self.name = name #e.g Cooper Teare
		self.id = id
		self.losses = 0
		self.outgoing_points = 0
		self.races = set()

	def lose(self, outgoing_points):
		self.losses += 1
		self.outgoing_points += outgoing_points

	def merge(self, other):
		assert isinstance(other, Athlete)
		assert self == other
		self.losses += other.losses
		self.outgoing_points += other.outgoing_points
		self.races = self.races.union(other.races)

	def add_race(self, race):
		self.races.add(race)

	def __eq__(self, other):
		return isinstance(other, Athlete) and self.id == other.id

	def __hash__(self):
		return self.id

	def __repr__(self):
		return self.name
