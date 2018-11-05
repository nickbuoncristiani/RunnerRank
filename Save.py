import scrape_utils, Athlete, matrix_utils, pickle, importer
import networkx as nx
from pygtrie import StringTrie

class Save:

	def __init__(self, *events_considering):
		self.athlete_web = nx.DiGraph() #contains athlete ids as nodes. edges contain matchup data.
		self.athletes_by_name = StringTrie() # maps string to athlete object
		self.athletes_by_id = {} # maps id to athlete object. 
		self.athletes_by_index = [] #So we can associate each athlete with a coordinate in the resultant vector.
		self.race_history = set() #Contains race url's
		self.athletes_considered = set() #Contains id's of nodes in scraping process.
		self.events_considering = events_considering

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
	def import_data(self, *athlete_ids, filename = 'my_save.bin'):
		if 'xc' in self.events_considering:
			importer.import_all(self, *athlete_ids)
		else:
			importer.import_all(self, *athlete_ids, *self.events_considering)
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
		self.events_considering = s.events_considering
		self.athletes_considered = s.athletes_considered

	#returns athletes rank in given event, given their unique id. 
	def get_ranking(self, athlete_id, event = 'xc'):
		return self[athlete_id].rank_map[event]

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
		return len(athletes_by_index)

	def __repr__(self):
		s1 = 'This save contains ' + len(self) + ' athles.'
		s2 = 'Top five runners are: '
		return s1 + s2


if __name__ == "__main__":
	#s = Save('xc')
	#s.import_data(8710974, filename = 'high_school.bin')
	#print(s.race_history)
	
	


