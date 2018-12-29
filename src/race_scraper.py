from urllib.request import urlopen, Request
import re, Athlete, Meet
import datetime as Date
import time as t

RESULT_PATTERN = re.compile(r'{"Result":[^}]+}')
DATE_PATTERN = re.compile(r'"MeetDate":\"\d{4}.\d{2}.\d{2}')

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
	for result, place in zip(results, range(1, len(results) + 1)):
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
