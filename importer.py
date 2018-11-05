import Save, scrape_utils
from urllib.request import urlopen, Request
from collections import deque
from bs4 import BeautifulSoup as soup

#Scrapes starting from athlete_ids, updates date_graph and adds all new athletes to athletes set
def import_all(save, *athlete_ids, xc = True):
	queue = deque(athlete_ids)
	if xc:
		base_url ='https://www.athletic.net/CrossCountry/Athlete.aspx?AID='
	else:
		base_url ='https://www.athletic.net/TrackAndField/Athlete.aspx?AID='
	
	while queue:
		curr_id = queue.popleft()
		page_url = base_url + str(curr_id)
		req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
		with urlopen(req) as page:
			athlete_history = soup(page.read(), 'html.parser')
		
		recent_season = athlete_history.find('div', {'class' : 'card-block px-2 pt-2 pb-0 collapse in'})
		events = recent_season.findAll('h5')
		event_results = recent_season.findAll('table', {'class' : 'table table-sm table-responsive table-hover'})
		
		if xc:
			#If we are considering xc we don't care too much about specific events. 
			events = ['xc' for event in events]
			base_url_2 = 'https://www.athletic.net/CrossCountry/'
		else:
			base_url_2 = 'https://www.athletic.net/TrackAndField/'
		
		full_results = zip(events, event_results)
		race_urls = []
		for result in full_results:
			if result[0] not in save.events_considering:
				continue
			trs = result[1].findAll('tr')
			for tr in trs:
				td = tr.findAll('td')[3]
				race_urls.append(base_url_2 + td.find('a')['href'])

		for race in race_urls:
			if race in save.race_history:
				continue
			save.race_history.add(race)
			scrape_utils.process_race(race, save)


if __name__ == "__main__":
	s = Save.Save('xc')
	import_all(s, 12421025)
	print(len(s.athletes_by_id))