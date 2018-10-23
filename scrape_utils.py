from urllib.request import urlopen, Request
import re, Athlete
import Save

#Uses raw re to extract race data from url.
def process_race(race_url, save):
	req = Request(race_url, headers={'User-Agent': 'Mozilla/5.0'})
	with urlopen(req) as page:
		race_info = str(page.read())
	pattern = re.compile(r'{"Result":[^}]+}') 

	results = pattern.findall(race_info)

	surpassers = []
	for result in results:
		a_ID = process_athlete_result(result, save)
		if not(a_ID):
			continue
		for surpasser in surpassers:
			save.lose(a_ID, surpasser, 'date', save)
		surpassers.append(a_ID)

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
	except KeyError:
		return 0
	return a_ID

if __name__ == "__main__":
	race_url = 'https://www.athletic.net/CrossCountry/meet/117800/results/521489'
	s = Save.Save('xc')
	process_race(race_url, s)
	print(s.athletes_by_id)