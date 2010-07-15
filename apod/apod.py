'''
A script to screen-scrape Astronomy Picture of the Day and come up with a
league table of "Tomorrow's picture" teasers.

APOD (http://apod.nasa.gov/) gives a teaser every day for the next day's
picture. I noticed that they seemed to be using "pixels in space" or
"open space" for this almost every other day, and wanted to see exactly how
stuck in a rut they were.
'''

from httplib import HTTPConnection
import re

connection = HTTPConnection('apod.nasa.gov')

def wget(url):
	connection.request('GET', url)
	resp = connection.getresponse()
	data = resp.read()
	return (resp.status, resp.reason, data)

teasers = {}

try:
	connection.connect()
	home = wget('/apod/archivepix.html')
	links = re.findall(r'<a href="(ap[0-9]+\.html)">', str(home[2]))
	for link in links:
		url = '/apod/' + str(link)
		page = wget(url)
		text = re.findall(r'Tomorrow\'s picture:.*<a href=.*?>(.*?)</a>', str(page[2]))
		if text:
			teaser = str(text[0]).strip()
			if teasers.has_key(teaser):
				teasers[teaser] += 1
			else:
				teasers[teaser] = 1
			print url + ': ' + teaser
finally:
	connection.close()

teasertexts = list(teasers.items())
teasertexts.sort(key = lambda v: -v[1])

print
print 'League table:'
print

for t in teasertexts:
	print t