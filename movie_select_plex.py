#Python Library Imports
import os, sys, sre, json, urllib, shutil, logging, stat, win32api, win32con, datetime, httplib, urllib
from xml.dom import minidom
#------------------
header = """
****************************************
*                                      *
*     Streaming Service Check          *
*                                      *
****************************************
\n"""

#Log Handler Setup
logger = logging.getLogger('Netflix_check')
logdate = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
hdlr = logging.FileHandler('D:\scripts\logs\Netflix Check\Netflix_Check-' + logdate + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

def movie_data(title):
	global movie1
	global movie
	movie1 = (title)
	movie_paren = movie1.replace('(', '').replace(')', '')
	movie = movie_paren
	movie_url = "http://www.canistream.it/services/search?movieName=%s" % movie
	try:
		url = urllib.urlopen(movie_url)
	except UnicodeError:
		print 'Non-ASCII Characters in title. Skipping.'
		logger.info('Non-ASCII Characters in title of %s' % movie)
		return False
	HTMLsource1 = url.read()
	url.close()
	data_j = json.loads(HTMLsource1)
	try:
		ID = data_j[0]['_id']
	except IndexError:
		print 'Invalid characters in title. Skipping.'
		logger.info('Invalid Search Characters in title of %s' % movie)
		return False
	movie_url2 = "http://www.canistream.it/services/query?movieId=%s&attributes=1&mediaType=streaming" % ID
	url = urllib.urlopen(movie_url2)
	global HTMLsource2
	HTMLsource2 = url.read()
	url.close()
	Netflix()
	
def Netflix():
	service = sre.findall('friendlyName":"([^"]+)', HTMLsource2)
	if 'Netflix Instant' in service:
		return True
	else:
		return False
		
def delete_movie():
		print "%s marked for deletion. Moving on to the next movie." % movie
		logger.info('%s is avalible on Netflix.' % movie)

def pushover():
	if 1 in to_delete:
		conn = httplib.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
		urllib.urlencode({
		"token": "afTHBbHyLBSUFTNNPhBV9oDtBpqCUJ",
		"user": "uU95W9hYqeW3b24uyPaT1skT1SG35N",
		"message": "Netflix/Plex Scan has been run, and found new items to delete. Check the log for new movies to remove from Plex. ",
		}), { "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()
	else:
		conn = httplib.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
		urllib.urlencode({
		"token": "afTHBbHyLBSUFTNNPhBV9oDtBpqCUJ",
		"user": "uU95W9hYqeW3b24uyPaT1skT1SG35N",
		"message": "Netflix/Plex Scan has been run, but found no new movies to delete.",
		}), { "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()

plex_url = 'http://localhost:32400/library/sections/2/all'
root_tree = minidom.parse(urllib.urlopen(plex_url))
video = root_tree.getElementsByTagName('Video')
for t in video:
	title = t.getAttribute('title')
	movie_data(title)
	if Netflix() is True:
		to_delete = '1'
		delete_movie()
	else:
		os.system('cls')
		print header
		print "%s is not available on Netflix. Moving on to next movie." % movie
		continue
pushover()