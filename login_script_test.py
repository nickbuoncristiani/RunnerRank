"""I noticed that robobrowser wasn't able to locate the form on the athletic.net login page so I'm trying to use 
beautiful soup here to find it and it seems to be missing. This is probably why robobrowser can't find the form as robo-
browser uses beautiful soup. This is a temporary file for experimenting with ways to login to athletic.net."""

import html5lib
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup

if __name__ == '__main__':
	url = 'https://www.athletic.net/CrossCountry/meet/154540/results/644131'
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	with urlopen(req) as site:
		page = site.read()
	page_soup = soup(page, 'html.parser')
	print(page_soup.prettify())
