import Save, scrape_utils, time
from urllib.request import urlopen, Request
from collections import deque
from bs4 import BeautifulSoup as soup

"""Scrapes starting from athlete_ids, updates date_graph and adds all new athletes to athletes set
xc is set to true by default as it is the most interesting application of our work.
We need to upper bound the number of races that can be added to our system lest we run forever!"""
def search_for_races(save, *athlete_ids, num_races_to_add = 50, event = 'xc'):
	queue = deque(athlete_ids)
	if event == 'xc':
		base_url ='https://www.athletic.net/CrossCountry/Athlete.aspx?AID='
	else:
		base_url ='https://www.athletic.net/TrackAndField/Athlete.aspx?AID='

	races_added = 0
	
	while races_added < num_races_to_add and queue:
		curr_id = queue.popleft()
		if curr_id in save.athletes_considered:
			continue
		page_url = base_url + str(curr_id)
		save.consider_athlete(curr_id)

		print('Working on athlete with id: ' + str(curr_id))
		time.sleep(1)
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
			#If we are considering xc we don't care too much about specific events. 
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
			if race in save.race_history:
				continue
			else:
				races_added += 1
				save.add_race(race)
				scrape_utils.process_race(race, save, queue=queue)

if __name__ == "__main__":
	s = Save.Save('xc')
	search_for_races(s, 12421025)
	print(len(s.athletes_by_id))