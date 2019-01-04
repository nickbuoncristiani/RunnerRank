from urllib.request import urlopen, Request
import re, Athlete, Meet
import datetime as Date
import time as t
from collections import deque

RESULT_PATTERN = re.compile(r'{"Result":[^}]+}')
DATE_PATTERN = re.compile(r'"MeetDate":\"\d{4}.\d{2}.\d{2}')

"""Scrapes starting from athlete_ids, updates date_graph and adds all new athletes to athletes set
xc is set to true by default as it is the most interesting application of our work.
We need to upper bound the number of races that can be added to our system else we will run forever!"""
def search_for_races(save, *starting_ids, num_races_to_add = 50, event = 'xc'):
	queue = deque(starting_ids)
	if event == 'xc':
		base_url ='https://www.athletic.net/CrossCountry/Athlete.aspx?AID='
	else:
		base_url ='https://www.athletic.net/TrackAndField/Athlete.aspx?AID='

	races_added = 0
	ATHLETES_TO_ADD = 2
	
	while races_added < num_races_to_add and queue:
		curr_id = queue.popleft()
		if curr_id in save.athletes_considered:
			continue
		page_url = base_url + str(curr_id)
		print(page_url)
		save.consider_athlete(curr_id)

		print('Working on athlete with id: ' + str(curr_id))
		t.sleep(1)
		try:
			req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
			with urlopen(req) as page:
				athlete_history = soup(page.read(), 'html.parser')
		except:
			print('Error handling athlete with id: ' + str(curr_id))
			continue

		recent_season = athlete_history.find('div', {'class' : 'card-block px-2 pt-2 pb-0 collapse in'})
		events = recent_season.findAll('h5')
		event_results = recent_season.findAll('table', {'class' : 'table table-sm table-responsive table-hover'})
		
		if event == 'xc':
			events = ['xc' for event in events]
			base_url_2 = 'https://www.athletic.net/CrossCountry/'
		else:
			base_url_2 = 'https://www.athletic.net/TrackAndField/'
		
		full_results = zip(events, event_results)
		race_urls = []
		for result in full_results:
			if result[0] != event:
				continue
			else:
				trs = result[1].findAll('tr')
				for tr in trs:
					td = tr.findAll('td')[3]
					race_urls.append(base_url_2 + td.find('a')['href'])

		for race in race_urls:
			if Meet.Meet('m', 'd', race, 'd') in save.race_history:
				continue
			else:
				meet = process_race(save, race)
				for i in range(ATHLETES_TO_ADD):
					queue.append(meet.results[i][0])
				save.add_race(meet)
				races_added += 1

#Uses raw re to extract race data from url.
def process_race(save, race_url):
	print('working on race: ' + race_url)
	t.sleep(5)
	try:
		req = Request(race_url, headers={'User-Agent': 'Mozilla/5.0'})
		with urlopen(req) as page:
			race_info = str(page.read())
	except:
		print("Error handling race: " + race_url)
		t.sleep(120)
		process_race(save, race_url)

	results = re.findall(RESULT_PATTERN, race_info)
	race_date = re.search(DATE_PATTERN, race_info).group()
	str_date = re.split(':', race_date)[1]
	date = process_date(str_date)

	meet_name = re.search('style="cursor:pointer;">[^<]+<', race_info).group()
	meet_name = re.findall('>[^<]+', meet_name)[0][1:]

	finished_results = []
	for result in results:
		current_athlete, time = process_athlete_result(save, result) 
		if not(current_athlete): 
			continue
		finished_results.append((current_athlete, time))
		
	new_meet = Meet.Meet(meet_name, date, race_url, finished_results)
	return new_meet

#processes a single match found by regular expression, adding data to save
def process_athlete_result(save, result_data):
	pattern = re.compile(r'(null|true|false)')
	result_data = re.sub(pattern, 'None', result_data) 
	try:
		result = eval(result_data)
		time = result['SortValue']
		a_id = result['AthleteID']
		name = result['FirstName'] + ' ' + result['LastName']
		assert time is not None and a_id is not None
		athlete = Athlete.Athlete(a_id, name)
	except:
		return None, None
	save.update_athlete(athlete)
	return athlete.id, time

#takes date string and returns appropriate datetime object
def process_date(date_string):
	date_list = re.split(r'\D', date_string)[1:]
	date_ints = list(map(int, date_list))
	year, month, day = date_ints
	race_date = Date.datetime(year, month, day)
	return race_date
