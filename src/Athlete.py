class Athlete:

	id = 0
	def __init__(self, id, name, school):
		self.name = name
		self.school = school
		self.id = id
		self.losses = 0
		self.races = set()

	def lose(self):
		self.losses += 1

	def merge(self, other):
		assert isinstance(other, Athlete)
		assert self == other
		self.losses += other.losses
		self.races = self.races.union(other.races)
		self.school = other.school if other.school is not 'Unattached' else self.school

	def add_race(self, race):
		self.races.add(race)

	def __eq__(self, other):
		return isinstance(other, Athlete) and self.id == other.id

	def __hash__(self):
		return self.id

	def __repr__(self):
		return self.name
