import scrape_utils, Athlete, matrix_utils, pickle, importer, time
import numpy as np
import networkx as nx
from pygtrie import StringTrie

class Save:

	def __init__(self, event):
		self.athlete_web = nx.DiGraph() #contains athlete ids as nodes. edges contain matchup data.
		self.athletes_by_name = StringTrie() # maps string to athlete object
		self.athletes_by_id = {} # maps id to athlete object. 
		self.athletes_by_index = [] #So we can associate each athlete with a coordinate in the resultant vector.
		self.race_history = set() #Contains race url's
		self.athletes_considered = set() #Contains id's of nodes in scraping process.
		self.event = event
		self.rankings = [] #List of athletes in decreasing order of rank.

	def add_athlete(self, a_ID, name):
		if a_ID in self.athletes_by_id:
			return 
		new_athlete = Athlete.Athlete(a_ID, name)
		self.athletes_by_id[a_ID] = new_athlete
		self.athletes_by_name[name] = new_athlete
		self.athletes_by_index.append(a_ID)
		self.athlete_web.add_node(a_ID)

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
		with open(filename, 'wb') as file:
			pickle.dump(self, file)

	#updates state to match .bin file
	def load(self, filename = 'my_save.bin'):
		with open(filename, 'rb') as file:
			s = pickle.load(file)
		self.athlete_web = s.athlete_web
		self.athletes_by_name = s.athletes_by_name
		self.athletes_by_id = s.athletes_by_id
		self.athletes_by_index = s.athletes_by_index
		self.race_history = s.race_history
		self.event = s.event
		self.athletes_considered = s.athletes_considered
		self.rankings = s.rankings

	def update_rankings(self, filename = 'my_save.bin'):
		system = nx.to_numpy_array(self.athlete_web)
		rankings_by_index = matrix_utils.get_rankings(system)
		score_pairs = [(self.athlete_at_index(pair[0]), pair[1]) for pair in enumerate(rankings_by_index)] 
		score_pairs.sort(key = lambda x: -1 * x[1])
		self.rankings = list(map(lambda x: x[0], score_pairs))
		with open(filename, 'wb') as file:
			pickle.dump(self, file)

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
	#s = Save('xc')
	#s.import_data(8693591, num_races_to_add = 200, filename = 'high_school2.bin')
	b = Save('xc')
	b.load('high_school2.bin')
	#b.update_rankings('high_school2.bin')
	b.print_rankings()

