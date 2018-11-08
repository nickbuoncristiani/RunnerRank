import scrape_utils, Athlete, matrix_utils, pickle, importer, time
import numpy as np
import networkx as nx
from pygtrie import StringTrie

class Save:

	def __init__(self, event = 'xc'):
		self.athlete_web = nx.DiGraph() 
		self.athletes_by_name = StringTrie() 
		self.athletes_by_id = {} 
		self.athletes_by_index = [] 
		self.race_history = set() 
		self.athletes_considered = set() 
		self.event = event
		self.rankings = []

	#Returns new Save from source file. 
	def load(self, filename = 'my_save.bin'):
		with open(filename, 'rb') as file:
			s = pickle.load(file)
		return s

	def save(self, filename = 'my_save.bin'):
		with open(filename, 'wb') as file:
			pickle.dump(self, file)

	def add_athlete(self, a_ID, name):
		if a_ID in self.athletes_by_id:
			return 
		new_athlete = Athlete.Athlete(a_ID, name)
		self.athletes_by_id[a_ID] = new_athlete
		self.athletes_by_name[name] = new_athlete
		self.athletes_by_index.append(a_ID)
		self.athlete_web.add_node(a_ID)

	def consider_athlete(self, a_ID):
		self.athletes_considered.add(a_ID)

	def add_race(self, race_url):
		self.race_history.add(race_url)

	def lose(self, won_id, lost_id):
		self[won_id].win()
		self[lost_id].lose()
		if won_id in self and lost_id in self.athlete_web[won_id]:
			self.athlete_web[won_id][lost_id]['count'] += 1
		else:
			self.athlete_web.add_edge(won_id, lost_id, count = 1)
		count = self.athlete_web[won_id][lost_id]['count']
		self.athlete_web.add_edge(won_id, lost_id, weight = count / self[lost_id].losses)

	#takes athletes as starting points and dives into athletic.net.
	def import_data(self, *athlete_ids, num_races_to_add = 20, filename = 'my_save.bin'):
		importer.search_for_races(self, *athlete_ids, num_races_to_add = num_races_to_add, event = self.event)
		self.save(filename)

	def update_rankings(self, filename = 'my_save.bin'):
		system = nx.to_numpy_array(self.athlete_web)
		rankings_by_index = matrix_utils.get_rankings(system)
		score_pairs = [(self.athlete_at_index(pair[0]), pair[1]) for pair in enumerate(rankings_by_index)] 
		score_pairs.sort(key = lambda x: -1 * x[1])
		self.rankings = list(map(lambda x: x[0], score_pairs))
		self.save(filename)
	
	#We also assign an index to individual athletes so we can reclaim them from a vector/matrix.
	def athlete_at_index(self, index):
		return self.athletes_by_index[index]

	#can subscript Save object using either athlete or athlete id for the same result.
	def __getitem__(self, request):
		if type(request) == int:
			return self.athletes_by_id[request]
		return self.athletes_by_name[request]

	def __contains__(self, request):
		if type(request) == int:
			return request in self.athletes_by_id
		return request in self.athletes_by_name

	def __len__(self):
		return len(self.athletes_by_index)

	def __repr__(self):
		return 'Save object containing ' + str(len(self)) + ' athletes.'

	def print_rankings(self):
		for place, athlete in list(enumerate(self.rankings))[:100][::-1]:
			print(place, self[athlete])

if __name__ == "__main__":
	s = Save('xc')
	s.import_data(8693591, num_races_to_add = 1)
	#b = load('high_school2.bin')
	s.update_rankings()
	s.print_rankings()

