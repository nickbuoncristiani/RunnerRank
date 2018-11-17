from urllib.request import urlopen, Request
import re, Athlete, Meet
import datetime as Date
import time as t

RESULT_PATTERN = re.compile(r'{"Result":[^}]+}')
DATE_PATTERN = re.compile(r'"MeetDate":\"\d{4}.\d{2}.\d{2}')

#Uses raw re to extract race data from url.
def process_race(race_url):
	print('working on race: ' + race_url)
	t.sleep(5)
	try:
		req = Request(race_url, headers={'User-Agent': 'Mozilla/5.0'})
		with urlopen(req) as page:
			race_info = str(page.read())
	except:
		print("Error handling race: " + race_url)
		t.sleep(120)
		process_race(race_url, save, queue, new_athletes_to_add)

	results = re.findall(RESULT_PATTERN, race_info)
	race_date = re.search(DATE_PATTERN, race_info).group()
	str_date = re.split(':', race_date)[1]
	date = process_date(str_date)

	meet_name = re.search('style="cursor:pointer;">[^<]+<', race_info).group()
	meet_name = re.findall('>[^<]+', meet_name)[0][1:]

	finished_results = {}
	for result, place in zip(results, range(1, len(results) + 1)):
		current_athlete, time = process_athlete_result(result) 
		if not(current_athlete): 
			continue
		finished_results[current_athlete] = (place, time)
		
	new_meet = Meet.Meet(meet_name, date, race_url, finished_results)
	for athlete in new_meet.results:
		athlete.add_race(new_meet)
	return new_meet

#processes a single match found by regular expression, adding data to save
def process_athlete_result(result_data):
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
	return athlete, time

#takes date string and returns appropriate datetime object
def process_date(date_string):
	date_list = re.split(r'\D', date_string)[1:]
	date_ints = list(map(int, date_list))
	year, month, day = date_ints
	race_date = Date.datetime(year, month, day)
	return race_date

if __name__ == "__main__":
	print(5)
