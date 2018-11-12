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
		print("Error handling race: " + race_url)
		time.sleep(120)
		process_race(race_url, save, queue, new_athletes_to_add)
	
	result_pattern = re.compile(r'{"Result":[^}]+}')

	results = re.findall(result_pattern, race_info)

	#We might want to use this later.
	"""
	date_pattern = re.compile(r'"MeetDate":\"\d{4}.\d{2}.\d{2}')
	race_date = date_pattern.findall(race_info)[0] #these two lines feel a little janky - i am going to clean up later
	str_date = re.split(':', race_date)[1]

	date_object = process_date(str_date)

	name_pattern = re.compile(r'"OwnerID":.+:(".+")')
	meet_name = re.findall(name_pattern, race_info)
	"""

	meet_name = re.search('style="cursor:pointer;">[^<]+<', race_info).group()
	meet_name = re.findall('>[^<]+', meet_name)[0][1:]
	
	surpassers = []
	added_to_queue = 0 
	for result in results:
		a_ID = process_athlete_result(result, meet_name, save)
		if added_to_queue < new_athletes_to_add and queue is not None:
			queue.append(a_ID)
			print('adding ' + save[a_ID].name + ' to queue.')
		if not(a_ID): #just an edgecase for if a meet entry is nontraditional and athlete can't be verified.
			continue
		for surpasser in surpassers:
			save.lose(surpasser, a_ID, margin = save[a_ID].results[meet_name] - save[surpasser].results[meet_name] + .01)
		surpassers.append(a_ID)
		added_to_queue += 1

#processes a single match found by regular expression, adding data to save
def process_athlete_result(result_data, meet_name, save):
	pattern = re.compile(r'(null|true|false)')
	result_data = re.sub(pattern, 'None', result_data)
	try:
		result = eval(result_data)
		time = result['SortValue']
		a_ID = result['AthleteID']
		name = result['FirstName'] + ' ' + result['LastName']
		assert(time is not None and a_id is not None)
		save.update_athlete(a_ID, name, meet_name, time)
	except:
		return 0
	return a_ID

"""Converts a time in 'xx:xx' format to double format"""
def getSeconds(time):
    if ':' in time:
        minutes = float('0' + time[0 : self.time.find(':')]) 
        seconds = float(self.time[self.time.find(':') + 1:])
        return minutes * 60 + seconds
    return float(self.time)

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
	s = Save.Save()
	process_race(race_url, s)
