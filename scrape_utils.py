from urllib.request import urlopen, Request
import re, Athlete
import networkx as nx

#Uses raw re to extract race data from url.
def process_race(race_url, data_graph):
	req = Request(race_url, headers={'User-Agent': 'Mozilla/5.0'})
	with urlopen(req) as page:
		race_info = str(page.read())
	pattern = re.compile(r'{"Result":[^}]+}') 

	results = pattern.findall(race_info)

	surpassers = []
	for result in results:
		athlete = process_athlete_result(result, data_graph)
		for surpasser in surpassers:
			data_graph.add_edge(athlete, surpasser, 1)
		surpassers.append(athlete)

#processes a single match found by regular expression, adding data to graph.
def process_athlete_result(result_data, data_graph):
	pattern = re.compile(r'(null|true|false)')
	result_data = re.sub(pattern, 'None', result_data)
	result = eval(result_data)  
	a = Athlete.Athlete(result['FirstName'] + ' ' + result['LastName'], result['AthleteID'])
	if a not in data_graph:
		data_graph.add_node(a)
	return a

if __name__ == "__main__":
	race_url = 'https://www.athletic.net/CrossCountry/meet/154540/results/644131'
	g = nx.MultiDiGraph()
	process_race(race_url, g)
	process_race(race_url, g)
	process_race(race_url, g)
	"""for athlete in g:
		print(g.out_degree(athlete, weight='weight'))
		print('\n') """
	a = Athlete.Athlete('asdf', 9126976)
	b = Athlete.Athlete('ffsa', 12401545)
	print(g[b][a])