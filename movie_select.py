#Python Library Imports
import os, sys, sre, json, urllib
#------------------
print "****************************************"
print "*                                      *"
print "*     Streaming Service Check          *"
print "*                                      *"
print "****************************************"
print "\n"

def get_movie_data():
	global directories
	directories = [os.path.abspath(name) 
		for name in os.listdir('.') if os.path.isdir(name)]
	directories.remove('M:\\$RECYCLE.BIN')
	for dir_ in directories:
		global movie
		movie = (dir_)
		movie = movie[3:]
		movie2 = movie.replace(" ", "%20")
		

	movie_url = "http://www.canistream.it/services/search?movieName=%s" % movie2
	url = urllib.urlopen(movie_url)
	HTMLsource1 = url.read()
	url.close()
	data_j = json.loads(HTMLsource1)
	ID = data_j[0]['_id'] 
	

	movie_url2 = "http://www.canistream.it/services/query?movieId=%s&attributes=1&mediaType=streaming" % ID
	url = urllib.urlopen(movie_url2)
	global HTMLsource2
	HTMLsource2 = url.read()
	url.close()
	
get_movie_data()

#the line below will check HTMLsource2 global variable data for the services found after the 'friendlyName' tag
service = sre.findall('friendlyName":"([^"]+)', HTMLsource2)
print "%s is available on the following services: %s" % (movie,service)
yes = set(['yes','y', 'ye', ''])
no = set(['no','n'])
if "Netflix Instant" not in service:
	print "Moving to next item in the Movies directory."
	# This should go to the next item in for loop
else:
	choice = raw_input("Netflix Streaming is available for %s. Do you wish to delete this movie from your media server?").lower() % movie
	if choice in yes:
		user_delete = 1
	elif choice in no:
		user_delete = 0
	else:
		sys.stdout.write("Please respond with 'yes' or 'no'")




# print HTMLsource2
# data_s = json.loads(HTMLsource2)
# Streaming = data_s[u]['friendlyName']
# jsonkeys = data_s.keys()
# pprint.pprint(data_s)