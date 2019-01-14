import race_scraper, Athlete

import pickle, os
import numpy as np
import networkx as nx
from pygtrie import CharTrie

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
from tkinter import Widget
from tkinter import Event

SAVE_PATH = str(os.getcwd()) + '/saves'

class Save:

	def __init__(self):
		self.athlete_web = nx.DiGraph() 
		self.athletes_by_name = CharTrie() 
		self.athletes_by_id = {} 
		self.athletes_by_index = [] 
		self.race_history = set() 
		self.athletes_considered = set() 
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

	def get_prefix_matches(self, name, count):
		return list(map(lambda athlete: athlete.name, self.athletes_by_name.values(prefix=name)[:count]))

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

		for persons_defeated in map(lambda item: item[1], self.athlete_web.adj.items()):
			for person_defeated, connection in persons_defeated.items():
				connection['weight'] = connection['count']/self[person_defeated].losses

	#takes athletes as starting points and dives into athletic.net.
	def import_data(self, num_races_to_add, *athlete_ids):
		race_scraper.search_for_races(self, num_races_to_add, *athlete_ids)
		self.update_graph()
		self.update_rankings()

	def update_rankings(self):
		system = nx.to_numpy_array(self.athlete_web)
		rankings_by_index = self.get_rankings(system)
		score_pairs = [(self.athlete_at_index(pair[0]), pair[1]) for pair in enumerate(rankings_by_index)] 
		score_pairs.sort(key = lambda x: -1 * x[1])
		self.rankings = list(map(lambda x: x[0], score_pairs))

	#We also assign an index to individual athletes so we can reclaim them from a vector/matrix.
	def athlete_at_index(self, index):
		return self.athletes_by_index[index]

	def get_rankings(self, matrix, precision = 100):
		current_scores = np.full(len(matrix), 1)
		for _ in range(precision):
			current_scores = np.matmul(matrix, current_scores)
		return current_scores

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

CURRENT_SAVE = None
DROPDOWN_NUM = 5

class RunnerRank(tk.Tk):
 
	def __init__(self):
		super().__init__()
		if not os.path.isdir(str(os.getcwd()) + '/saves'):
			os.mkdir(str(os.getcwd()) + '/saves')

		self.pages = {}
		for page in (StartPage, PageOne):
			new_page = page(self)
			self.pages[page] = new_page
			new_page.pack(expand=False)

		self.set_page(StartPage)

		self.wm_title("Runner Rank")
		self.save = None

	def set_page(self, page):
		self.pages[page].tkraise()
		

class StartPage(tk.Frame):

	def __init__(self, parent):
		super().__init__()
		self.parent = parent
		begin_button = ttk.Button(self, text='Begin', command=lambda: parent.set_page(PageOne))
		begin_button.pack(side='left')
		guide_button = ttk.Button(self, text='Guide', command=self.open_guide)
		guide_button.pack(side='left')

	def open_guide(self):
		info_window = tk.Toplevel(self.parent)
		scrollbar = ttk.Scrollbar(info_window)
		scrollbar.pack(side='right', fill='y')
		
		with open(os.getcwd() + '/README.md', 'r') as info:
			info_text = tk.Text(info_window, font=('Verdana', 12), yscrollcommand=scrollbar.set)
			info_text.insert(tk.END, info.read())
			info_text.pack()

		scrollbar.config(command=info_text.yview)
		
		info_window.mainloop()

class PageOne(tk.Frame):

	def __init__(self, parent):
		super().__init__()
		self.parent = parent
		tk.Label(self, text='Select Option:').pack(side='top')
		new_button = ttk.Button(self, text='Make Rankings', command=lambda: parent.set_page(GatherPage))
		new_button.pack(side='top')
		load_button = ttk.Button(self, text='Load Rankings', command=lambda: parent.set_page(ViewPage))
		load_button.pack(side='top')

def update_matches(self):
	if CURRENT_SAVE:
		self.athlete_search_bar['values'] = \
			CURRENT_SAVE.get_prefix_matches(self.athlete_search_bar.get(), DROPDOWN_NUM)

def load_save(self):
	global CURRENT_SAVE
	filename = fd.askopenfilename(initialdir = SAVE_PATH)
	CURRENT_SAVE = Save.load(str(filename))
	self.rankings = str(CURRENT_SAVE)

def new_save(self):
	global CURRENT_SAVE
	filename = fd.asksaveasfilename(initialdir = SAVE_PATH) 
	s = Save()
	args = self.athlete_search_bar.get()
	args = args.split(', ')
	s.import_data(int(self.num_races_bar.get()), *args)
	s.save(filename)
	CURRENT_SAVE = s
	self.rankings = str(s)
	self.announcement('Done collecting data!')

def create_rankings_window(self):
	rankings_window = tk.Toplevel(self.root)
	
	scrollbar = ttk.Scrollbar(rankings_window)
	scrollbar.pack(side='right', fill='y')

	rankings_list = tk.Text(rankings_window, font=('Verdana', 10), yscrollcommand=scrollbar.set)
	rankings_list.insert(tk.END, self.rankings)
	rankings_list.pack()

	scrollbar.config(command=rankings_list.yview)
	
	rankings_window.mainloop()

def announcement(self, msg):
	window = tk.Tk()
	window.resizable(width=False, height=False)
	window.minsize(width=205, height=50)
	window.wm_title('Announcement')
	label = tk.Label(window, text=msg)
	button = ttk.Button(window, text = 'OK', command=lambda: window.destroy())
	label.pack()
	button.pack()


if __name__ == "__main__":
	app = RunnerRank()
	app.mainloop()
	







