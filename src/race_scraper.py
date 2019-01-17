from urllib.request import urlopen, Request
import re, Athlete, Meet
import datetime as Date
import time as t
from bs4 import BeautifulSoup as soup
import json, Save

"""Scrapes starting from athlete_ids, updates date_graph and adds all new athletes to athletes set
xc is set to true by default as it is the most interesting application of our work.
We need to upper bound the number of races that can be added to our system else we will run forever!"""
def search_for_races(save, num_races_to_add, *starting_ids, progress_frame=None):
	BASE_URL ='https://www.athletic.net/CrossCountry/Athlete.aspx?AID='
	ATHLETES_TO_ADD = 2
	
	id_queue = list(starting_ids)
	races_added = 0
	
	while races_added < num_races_to_add and id_queue:
		curr_id = id_queue.pop(0)
		if curr_id in save.athletes_considered:
			continue
		page_url = BASE_URL + str(curr_id)
		save.consider_athlete(curr_id)
		print('Working on athlete with id: ' + str(curr_id))
		
		t.sleep(1)
		try:
			req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
			with urlopen(req) as page:
				athlete_history = soup(page.read(), 'html.parser')
		except Exception as e:
			print('Error handling athlete with id: ' + str(curr_id))
			print(e)
			continue

		recent_season = athlete_history.find('div', {'class' : 'card-block px-2 pt-2 pb-0 collapse in'})
		events = recent_season.findAll('h5')
		event_results = recent_season.findAll('table', {'class' : 'table table-sm table-responsive table-hover'})
		
		events = ['xc' for event in events] 
		base_url_2 = 'https://www.athletic.net/CrossCountry/'
		
		full_results = event_results
		race_urls = []
		for result in full_results:
			trs = result.findAll('tr')
			for tr in trs:
				td = tr.findAll('td')[3]
				race_urls.append(base_url_2 + td.find('a')['href'])

		for race in race_urls:
			if not(Meet.Meet('m', 'd', race, 'd') in save.race_history):
				try:
					meet = process_race(save, race)
				except Exception as e:
					print('Error processing race.')
					print(e)
					save.add_race(Meet.Meet('Invalid', '-', race, []))
					continue
				save.add_race(meet)
				for i in range(ATHLETES_TO_ADD):
					id_queue.append(meet.results[i][0])
				races_added += 1
				if progress_frame:
					progress_frame.update_progress(races_added)

#Uses raw re to extract race data from url.
def process_race(save, race_url):
	print('working on race: ' + race_url)
	try:
		with urlopen(Request(race_url, headers={'User-Agent': 'Mozilla/5.0'})) as page:
			race_info = str(page.read())
	except Exception as e:
		print("Error handling race: " + race_url)
		print("Will try again in two minutes.")
		print(e)
		t.sleep(120)
		process_race(save, race_url)

	parse_data = re.search(r'.constant\("initialData"[^;]+\);', race_info).group()
	parse_data = parse_data[25:len(parse_data)-2]
	meet_data = parse_data
	meet_data = re.sub(r'\"SetupState\".+,\"Settings\":null', r'"KMA":null', meet_data).replace('\\', '\\\\')
	meet_data = re.sub(r'\"entries\":null.+', r'"GF":null}', meet_data)

	meet_data = json.loads(meet_data)
	
	meet_name = meet_data['meet']['Name']
	meet_date = process_date(meet_data['meet']['EndDate'])

	finished_results = []
	for result in meet_data['results']:
		current_athlete, time = process_athlete_result(save, result, meet_name) 
		if current_athlete: 
			finished_results.append((current_athlete, time))

	return Meet.Meet(meet_name, meet_date, race_url, finished_results)

#processes a single match found by regular expression, adding data to save
def process_athlete_result(save, result_data, meet):
	try:
		time = result_data['Result']	
		a_id = result_data['AthleteID']
		name = result_data['FirstName'] + ' ' + result_data['LastName']
		school = result_data['SchoolName']
		assert time is not None and a_id is not None
		athlete = Athlete.Athlete(a_id, name, school)
		athlete.add_race((meet, time, result_data['Place']))
	except:
		return None, None
	save.update_athlete(athlete)
	return athlete.id, time

#takes date string and returns appropriate datetime object
def process_date(date_string):
	date_string = date_string.split('-')
	date_string[2] = date_string[2][:2]
	year, month, day = list(map(int, date_string))
	return Date.datetime(year, month, day)
	
if __name__ == "__main__":
	process_race(Save.Save(), 'https://www.athletic.net/CrossCountry/meet/146284/results/612612')
