import race_scraper, Athlete, matrix_utils

import pickle, os
import numpy as np
import networkx as nx
from pygtrie import StringTrie

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd

SAVE_PATH = str(os.getcwd()) + '/saves'

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

	@classmethod
	def load(self, filename = 'my_save.bin'):
		with open(filename, 'rb') as file:
			s = pickle.load(file)
		return s

	def save(self, filename = 'my_save.bin'):
		with open(filename, 'wb') as file:
			pickle.dump(self, file)

	def update_athlete(self, athlete):
		if athlete.id in self:
			self[athlete.id].merge(athlete)
			return 
		self.athletes_by_id[athlete.id] = athlete
		self.athletes_by_name[athlete.name] = athlete
		self.athletes_by_index.append(athlete.id)
		self.athlete_web.add_node(athlete.id)

	def consider_athlete(self, a_ID):
		self.athletes_considered.add(a_ID)

	def add_race(self, race_url):
		self.race_history.add(race_url)

	def update_graph(self):
		for race in self.race_history:
			surpassers = []
			for runner_id in map(lambda x: x[0], race.results):
				for surpasser_id in surpassers:
					self[runner_id].lose()
					if self.athlete_web.has_edge(surpasser_id, runner_id):
						self.athlete_web[surpasser_id][runner_id]['count'] += 1
					else:
						self.athlete_web.add_edge(surpasser_id, runner_id, count = 1)
						surpassers.append(runner_id)

		for persons_defeated in self.athlete_web.adj.items():
			for person_defeated, connection in persons_defeated.items():
				connection['weight'] = connection['count']/self[person_defeated].losses

	#takes athletes as starting points and dives into athletic.net.
	def import_data(self, num_races_to_add, *athlete_ids):
		race_scraper.search_for_races(self, *athlete_ids, num_races_to_add = num_races_to_add, event = self.event)
		self.update_graph()
		self.update_rankings()

	def update_rankings(self):
		system = nx.to_numpy_array(self.athlete_web)
		rankings_by_index = matrix_utils.get_rankings(system)
		score_pairs = [(self.athlete_at_index(pair[0]), pair[1]) for pair in enumerate(rankings_by_index)] 
		score_pairs.sort(key = lambda x: -1 * x[1])
		self.rankings = list(map(lambda x: x[0], score_pairs))

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

	def __str__(self):
		return ''.join([str(a[0] + 1) + '. ' + str(self.athletes_by_id[a[1]]) + '\n' for \
			a in enumerate(self.rankings)])

class RunnerRank(tk.Tk):
 
	def __init__(self):
		super().__init__()
		if not os.path.isdir(str(os.getcwd()) + '/saves'):
			os.mkdir(str(os.getcwd()) + '/saves')

		MainFrame(self).pack(expand=True)

		self.wm_title("Runner Rank")

class MainFrame(tk.Frame):

	def __init__(self, root):
		super().__init__(root)
		
		self.rankings = "Please load a save!"
		self.current = None
		self.root = root
		tk.Label(self, text="Athletes:").grid(row=0, column=0, sticky='E')
		tk.Label(self, text='Races to add:').grid(row=1, column=0, sticky='E')
		
		self.athlete_search_bar = tk.Entry(self)
		self.athlete_search_bar.insert(0, "12421023, 12421047")
		self.athlete_search_bar.grid(row=0, column=1)
		
		self.num_races_bar = tk.Entry(self)
		self.num_races_bar.insert(0, '20')
		self.num_races_bar.grid(row=1, column=1)

		new_button = tk.Button(self, text="New", command=self.new_save)
		new_button.grid(row=2, column=0)

		load_button = tk.Button(self, text="Load", command=self.load_save)
		load_button.grid(row=2, column=1)

		rankings_button = tk.Button(self, text="Show Current Rankings", \
			command=self.create_rankings_window)
		rankings_button.grid(row=3, columnspan=2)

	def load_save(self):
		filename = fd.askopenfilename(initialdir = SAVE_PATH)
		self.current = Save.load(str(filename))
		self.rankings = str(self.current)

	def new_save(self):
		filename = fd.asksaveasfilename(initialdir = SAVE_PATH) 
		s = Save()
		args = self.athlete_search_bar.get()
		args = args.split(', ')
		s.import_data(int(self.num_races_bar.get()), *args)
		s.save(filename)
		self.current = s
		self.rankings = str(s)
		self.announcement('Done collecting data!')

	def create_rankings_window(self):
		rankings_window = tk.Toplevel(self.root)

		rankings_list = tk.Text(rankings_window, font=('Verdana', 10))
		rankings_list.pack()

		rankings_list.insert(tk.END, self.rankings)
		rankings_window.mainloop()

	def announcement(self, msg):
		window = tk.Tk()
		window.wm_title('Announcement')
		label = tk.Label(window, text=msg)
		button = ttk.Button(window, text = 'OK', command=lambda: window.destroy())
		label.pack()
		button.pack()


if __name__ == "__main__":
	app = RunnerRank()
	app.mainloop()







