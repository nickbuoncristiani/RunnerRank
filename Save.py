import scrape_utils, Athlete, matrix_utils, pickle, importer, time
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

	def lose(self, athlete1_ID, athlete2_ID, date, meet_name):
		self[athlete1_ID].lose()
		self[athlete2_ID].win()
		self.set_edge(athlete1_ID, athlete2_ID, date, meet_name)

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

	#returns athletes rank in given event, given their unique id. 
	def get_ranking(self, athlete_id, event = 'xc'):
		return self[athlete_id].rank_map[event]

	def update_rankings(self):
		t1 = time.clock()
		web_matrix = matrix_utils.get_matrix_from_save(self)
		t2 = time.clock()
		print('generating matrix took ' + str(t2 - t1) + ' seconds')
		t1 = time.clock()
		rankings_by_index = matrix_utils.get_rankings(web_matrix)
		t2 = time.clock()
		print('generating rankings took ' + str(t2 - t1) + ' seconds')
		score_pairs = [(self.athlete_at_index(pair[0]), pair[1]) for pair in enumerate(rankings_by_index)] 
		score_pairs.sort(key = lambda x: -1 * x[1])
		self.rankings = list(map(lambda x: x[0], score_pairs))

	#data is a dictionary of data we want to add to edge.
	def set_edge(self, athlete1_ID, athlete2_ID, date, meet_name):
		if athlete1_ID in self and athlete2_ID in self.athlete_web.adj[athlete1_ID]:
			self.athlete_web[athlete1_ID][athlete2_ID]['losses'].append((meet_name, date))
		else:
			self.athlete_web.add_edge(athlete1_ID, athlete2_ID, losses = [(meet_name, date)])

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

	#Returns number of athletes in Save.
	def __len__(self):
		return len(self.athletes_by_index)

	def __repr__(self):
		return 'Save object containing ' + str(len(self)) + ' athletes.'


if __name__ == "__main__":
	#s = Save('xc')
	#s.import_data(8693591, num_races_to_add = 80, filename = 'high_school2.bin')
	b = Save('xc')
	b.load('high_school2.bin')
	b.update_rankings()
	for athlete_id in b.rankings:
		print(b[athlete_id].name)

	
	


