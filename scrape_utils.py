from urllib.request import urlopen, Request
import re, Athlete

#Uses raw re to extract race data from url.
def process_race(race_url, data_graph):
	req = Request(race_url, headers={'User-Agent': 'Mozilla/5.0'})
	with urlopen(req) as page:
		race_info = str(page.read())
	pattern = re.compile(r'{"Result":[^}]+}') 

	results = pattern.findall(race_info)

	for result in results:
		process_athlete_result(result, data_graph)

#processes a single match found by regular expression, adding data to graph.
def process_athlete_result(result_data, data_graph):
	pattern = re.compile(r'(null|true|false)')
	result_data = re.sub(pattern, 'None', result_data)
	result = eval(result_data)
	a = Athlete.Athlete(result['FirstName'] + ' ' + result['LastName'], result['AthleteID'])
	#print(a)
	#print('-----\n')

if __name__ == "__main__":
	race_url = 'https://www.athletic.net/CrossCountry/meet/154540/results/644131'
	process_race(race_url, 'a')