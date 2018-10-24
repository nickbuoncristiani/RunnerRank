import scrape_utils, Athlete, matrix_utils, pickle, importer
import networkx as nx
from pygtrie import StringTrie

class Save:

	def __init__(self, *events_considering):
		self.athlete_web = nx.DiGraph() #contains athlete objects as nodes, might make more sense just to have athlete id's.
		self.athletes_by_name = StringTrie() # maps string to athlete object
		self.athletes_by_id = {} # maps id to athlete object. 
		self.athlete_indices = [] #So we can associate each athlete with a coordinate in the resultant vector.
		self.race_history = set() # Contains race url's
		self.events_considering = events_considering

	def add_athlete(self, a_ID, name):
		if a_ID in self.athletes_by_id:
			return 
		new_athlete = Athlete.Athlete(a_ID, name)
		self.athletes_by_id[a_ID] = new_athlete
		self.athletes_by_name[name] = new_athlete
		self.athlete_indices.append(a_ID)
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
			save = pickle.load(file)
		self.athlete_web = save.athlete_web
		self.athletes_by_name = save.athletes_by_name
		self.athletes_by_id = save.athletes_by_id
		self.athlete_indices = save.athlete_indices
		self.race_history = save.race_history
		self.events_considering = save.events_considering

	#returns athletes rank in given event, given their unique id. 
	def get_ranking(self, athlete_id, event = 'xc'):
		return self[athlete_id].rank_map[event]

	#data is a dictionary of data we want to add to edge.
	def set_edge(self, athlete1_ID, athlete2_ID, date, meet_name):
		if athlete1_ID in self and athlete2_ID in self.athlete_web.adj[athlete1_ID]:
			self.athlete_web[athlete1_ID][athlete2_ID]['losses'].append((meet_name, date))
		else:
			self.athlete_web.add_edge(athlete1_ID, athlete2_ID, losses = [(meet_name, date)])

	def __getitem__(self, id):
		return self.athletes_by_id[id]

	def __contains__(self, id):
		return id in self.athletes_by_id

if __name__ == "__main__":
	s = Save('xc')
	s.import_data(12421025)
	b = Save('xc')
	b.load()


