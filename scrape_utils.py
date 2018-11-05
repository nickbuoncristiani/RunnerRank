from urllib.request import urlopen, Request
import re, Athlete, time
import Save
import datetime as Date

#Uses raw re to extract race data from url.
def process_race(race_url, save, queue = None, new_athletes_to_add = 2):
	print('working on race: ' + race_url)
	time.sleep(5)
	try:
		req = Request(race_url, headers={'User-Agent': 'Mozilla/5.0'})
		with urlopen(req) as page:
			race_info = str(page.read())
	except:
		print("freaked out with race: " + race_url)
		return
	
	pattern = re.compile(r'{"Result":[^}]+}')

	results = re.findall(pattern, race_info)

	date_pattern = re.compile(r'"MeetDate":\"\d{4}.\d{2}.\d{2}')
	race_date = date_pattern.findall(race_info)[0] #these two lines feel a little janky - i am going to clean up later
	str_date = re.split(':', race_date)[1]

	date_object = process_date(str_date)

	#Struggling a bit w regex expression
	#name_pattern = re.compile(r'"OwnerID":.+:(".+")')
	#meet_name = re.findall(name_pattern, race_info)
	
	surpassers = []
	count = 0
	for result in results:
		a_ID = process_athlete_result(result, save)
		if count < new_athletes_to_add:
			queue.append(a_ID)
			print('adding ' + save[a_ID].name + ' to queue.')
		if not(a_ID): #just an edgecase for if a meet entry is nontraditional and athlete can't be verified.
			continue
		for surpasser in surpassers:
			save.lose(a_ID, surpasser, date_object, 'MEETNAME')
		surpassers.append(a_ID)
		count += 1

#processes a single match found by regular expression, adding data to save
def process_athlete_result(result_data, save):
	pattern = re.compile(r'(null|true|false)')
	result_data = re.sub(pattern, 'None', result_data)
	result = eval(result_data)
	try:
		a_ID = result['AthleteID']
		name = result['FirstName'] + ' ' + result['LastName']
		save.add_athlete(a_ID, name)
	except TypeError:
		return 0
	return a_ID

#takes date string and returns appropriate datetime object
def process_date(date_string):
	date_list = re.split(r'\D', date_string)
	date_list.pop(0)
	date_ints = list(map(int, date_list))
	year, month, day = date_ints
	race_date = Date.datetime(year, month, day)
	return race_date

if __name__ == "__main__":
	race_url = 'https://www.athletic.net/CrossCountry/meet/117800/results/521489'
	s = Save.Save('xc')
	process_race(race_url, s)
