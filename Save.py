import scrape_utils, Athlete, matrix_utils
import networkx as nx
from pygtrie import StringTrie

class Save:

	def __init__(self):
		self.athlete_web = nx.DiGraph() #contains athlete objects as nodes, might make more sense just to have athlete id's.
		self.athletes_by_name = StringTrie() # maps string to athlete object
		self.athletes_by_id = {} # maps id to athlete object. 
		self.athlete_indices = [] #So we can associate each athlete with a coordinate in the resultant vector.
		self.race_history = set() # Contains race url's

	def add_athlete(self, a_ID, name):
		if a_ID in self.athletes_by_id:
			return 
		new_athlete = Athlete.Athlete(a_ID, name)
		self.athletes_by_id[a_ID] = new_athlete
		self.athletes_by_name[name] = new_athlete
		self.athlete_indices.append(a_ID)
		self.athlete_web.add_node(a_ID)

	#takes athletes as starting points and dives into athletic.net.
	def import_data(self, *athlete_ids):
		raise NotImplementedError()

	#updates state to match .bin file
	def load(self, file):
		raise NotImplementedError()

	#returns athletes rank in given event, given their unique id. 
	def get_ranking(self, athlete_id, event = 'xc'):
		return athletes_by_id[athlete_id].rank_map[event]


