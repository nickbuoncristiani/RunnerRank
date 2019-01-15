import race_scraper, Athlete, time

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
		else: 
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
	def import_data(self, num_races_to_add, athlete_id, progress_frame=None):
		race_scraper.search_for_races(self, num_races_to_add, athlete_id, progress_frame=progress_frame)
		self.update_graph()
		self.update_rankings()

	def update_rankings(self):
		system = nx.to_numpy_array(self.athlete_web)
		rankings_by_index = self.get_rankings(system)
		score_pairs = [(self.athlete_at_index(pair[0]), pair[1]) for pair in enumerate(rankings_by_index)] 
		score_pairs.sort(key=lambda x: -1 * x[1])
		self.rankings = list(map(lambda x: x[0], score_pairs))

	#We also assign an index elf.get_rankings(system)l athletes so we can reclaim them from a vector/matrix.
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
RANKINGS = 'Please load a save or create a new one.'

class RunnerRank(tk.Tk):
 
	def __init__(self):
		super().__init__()
		if not os.path.isdir(str(os.getcwd()) + '/saves'):
			os.mkdir(str(os.getcwd()) + '/saves')

		self.pages = {}
		for page in (StartPage, PageOne, GatherPage, ViewPage, LoadingFrame):
			new_page = page(self)
			self.pages[page] = new_page
			new_page.grid(row=0, column=0, sticky='nsew')

		self.set_page(StartPage)

		self.wm_title("Runner Rank")
		self.save = None

	def set_page(self, page):
		self.pages[page].tkraise()

	def announcement(self, frame, msg):
		def ok_button():
			self.set_state(frame, 'normal')
			window.destroy()
		
		self.set_state(frame, 'disabled')
		window = tk.Tk()
		window.resizable(width=False, height=False)
		window.minsize(width=205, height=50)
		window.wm_title('Announcement')
		label = tk.Label(window, text=msg)
		button = ttk.Button(window, text = 'OK', command=ok_button)
		label.pack()
		button.pack()

	def set_state(self, frame, state):
		state = state if state in ('disabled', 'normal') else 'normal'
		for widget in self.pages[frame].grid_slaves():
			widget.configure(state=state)
		

class StartPage(tk.Frame):

	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		begin_button = ttk.Button(self, text='Begin', command=lambda: parent.set_page(PageOne))
		begin_button.pack(side='top', expand=True)
		guide_button = ttk.Button(self, text='Guide', command=self.open_guide)
		guide_button.pack(side='top', expand=True)

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
		tk.Frame.__init__(self, parent)
		self.parent = parent
		tk.Label(self, text='Select Option:').pack(side='top')
		new_button = ttk.Button(self, text='Make Rankings', command=lambda: parent.set_page(GatherPage))
		new_button.pack(side='top')
		load_button = ttk.Button(self, text='Load Rankings', command=self.load_save)
		load_button.pack(side='top', expand=True)
		back_button = ttk.Button(self, text='Back', command = lambda: parent.set_page(StartPage))
		back_button.pack(side='top', expand=True)

	def load_save(self):
		global CURRENT_SAVE, RANKINGS
		filename = fd.askopenfilename(initialdir = SAVE_PATH)
		CURRENT_SAVE = Save.load(str(filename))
		RANKINGS = str(CURRENT_SAVE)
		self.parent.set_page(ViewPage)

class GatherPage(tk.Frame):

	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		tk.Label(self, text='Athlete:').grid(row=0, column=0, sticky='e')
		self.search_bar = ttk.Combobox(self)
		self.search_bar.grid(row=0, column=1, pady=2, sticky='w')

		tk.Label(self, text='Races to add:').grid(row=1, column=0, sticky='e')
		self.num_races_bar = ttk.Entry(self)
		self.num_races_bar.grid(row=1,column=1, sticky='w')

		self.generate_button = ttk.Button(self, text='Generate', command=self.new_save)
		self.generate_button.grid(row=2, column=0, pady=2, sticky='e')

		back_button = ttk.Button(self, text='Back', command = lambda: parent.set_page(PageOne))
		back_button.grid(row=3, column=0, pady=2, sticky='e')

	def new_save(self):
		global CURRENT_SAVE, RANKINGS
		
		filename = fd.asksaveasfilename(initialdir=SAVE_PATH) 
		athlete = int(self.search_bar.get())
		num_races = int(self.num_races_bar.get())
		s = Save()
		
		loading = self.parent.pages[LoadingFrame]
		loading.set_max(num_races)
		self.parent.set_page(LoadingFrame)
		self.parent.update()

		s.import_data(num_races, athlete, progress_frame=loading)
		s.save(filename)

		RANKINGS = str(s)
		CURRENT_SAVE = s

		self.parent.announcement(ViewPage, 'Done Collecting Data.')
		self.parent.set_page(ViewPage)
		

class LoadingFrame(tk.Frame):
	
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		self.bar = ttk.Progressbar(self, orient='horizontal', length=275, value=0)
		self.bar.pack(side='top', pady=3)
		tk.Label(self, text='Generating Rankings...').pack(side='top')

	def set_max(self, max):
		self.bar['max'] = max

	def update_progress(self, value):
		self.bar['value'] = value
		self.parent.update()

class ViewPage(tk.Frame):
	
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		tk.Label(self, text='Search:').grid(row=0, column=0, sticky='e')
		self.search_bar = ttk.Combobox(self)
		self.search_bar.grid(row=0, column=1)
		self.view_button = ttk.Button(self, text='View All Rankings', command=self.view_rankings)
		self.view_button.grid(row=1, column=0, sticky='e')
		back_button = ttk.Button(self, text='Back', command = lambda: parent.set_page(PageOne))
		back_button.grid(row=2, column=0, sticky='e')

	def view_rankings(self):
		rankings_window = tk.Toplevel(self.parent)
	
		scrollbar = ttk.Scrollbar(rankings_window)
		scrollbar.pack(side='right', fill='y')

		rankings_list = tk.Text(rankings_window, font=('Verdana', 10), yscrollcommand=scrollbar.set)
		rankings_list.insert(tk.END, RANKINGS)
		rankings_list.pack()
		rankings_list.config(state='disabled')

		scrollbar.config(command=rankings_list.yview)
		
		rankings_window.mainloop()

def update_matches(self):
	if CURRENT_SAVE:
		self.athlete_search_bar['values'] = \
			CURRENT_SAVE.get_prefix_matches(self.athlete_search_bar.get(), DROPDOWN_NUM)
	

if __name__ == "__main__":
	app = RunnerRank()
	app.mainloop()
	







