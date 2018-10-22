from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
import re, html5lib

#takes meet url and places all athletes into graph and updates athletes. Right now let's focus on men's races.

###!!!I did not realize that this page format does not include athlete ids. So this code is most likely useless!!!###
def import_meet(url, data_graph_men, data_graph_women):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	page = urlopen(req)
	page = page.read()
	page_soup = soup(page, 'html.parser')
	
	#getting mens' results
	mens_results = page_soup.find('div', {'id' : 'gender_M'})
	mens_races = mens_results.findAll('tbody', {'style' : 'cursor: pointer;'})
	for race in mens_races:
		curr_tag = race.find('tr')
		curr_tag = curr_tag.nextSibling.nextSibling.nextSibling
		while curr_tag:
			if curr_tag.text != 'Provided by Athletic.net':
				print(extract_athlete_data(curr_tag))
			curr_tag = curr_tag.nextSibling
	
	#getting womens' results
	womens_results = page_soup.find('div', {'id' : 'gender_F'})
	womens_races = womens_results.findAll('tbody', {'style' : 'cursor: pointer;'})
	for race in womens_races:
		curr_tag = race.find('tr')
		curr_tag = curr_tag.nextSibling.nextSibling.nextSibling
		while curr_tag:
			if curr_tag.text != 'Provided by Athletic.net':
				print(extract_athlete_data(curr_tag))
			curr_tag = curr_tag.nextSibling
		
#takes an athlete tag and returns (name, place)
def extract_athlete_data(html_block):
	data = html_block.find('td')
	place = data.text
	data = data.nextSibling.nextSibling
	name = data.text
	return place, name

if __name__ == '__main__':
	url = 'https://www.athletic.net/CrossCountry/Results/Meet.aspx?Meet=117561&show=all'
	import_meet(url, 'a', 'b')
