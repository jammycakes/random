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