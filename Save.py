import scrape_utils.py, Athlete.py, matrix_utils.py
import networkx as nx
from pygtrie import StringTrie

class Save:

	def __init__(self):
		self.athlete_web = nx.DiGraph() #contains athlete objects as nodes, might make more sense just to have athlete id's.
		self.athletes_by_name = StringTrie() # maps string to athlete object
		self.athletes_by_id = {} # maps id to athlete object. 
		self.race_history = set() # Contains race url's

	#takes athletes as starting points and dives into athletic.net.
	def import_data(self, *athlete_ids):
		raise NotImplementedError()

	#updates state to match .bin file
	def load(self, file):
		raise NotImplementedError()

	#returns athletes rank in given event, given their unique id. 
	def get_ranking(self, athlete_id, event = 'xc'):
		return athletes_by_id[athlete_id].rank_map[event]


