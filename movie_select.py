#Python Library Imports
import urllib
import json
import sre
#------------------
print "****************************************"
print "*                                      *"
print "*     Streaming Service Check          *"
print "*                                      *"
print "****************************************"
print "\n"

movie = raw_input("Please enter the movie you wish to search for: ")
movie2 = movie.replace(" ", "%20")
movie_url = "http://www.canistream.it/services/search?movieName=%s" % movie2
print movie
url = urllib.urlopen(movie_url)
HTMLsource1 = url.read()
url.close()
# print HTMLsource
data_j = json.loads(HTMLsource1)
ID = data_j[0]['_id'] 
print ID
# print HTMLsource[0]['_id'] 
movie_url2 = "http://www.canistream.it/services/query?movieId=%s&attributes=1&mediaType=streaming" % ID
url = urllib.urlopen(movie_url2)
HTMLsource2 = url.read()
url.close()

#the line below will check HTMLsource2 variable data for the services found after the 'friendlyName' tag
service = sre.findall('friendlyName":"([^"]+)', HTMLsource2)
print "%s is avaliable on the following services: %s" % (movie,service)


# print HTMLsource2
# data_s = json.loads(HTMLsource2)
# Streaming = data_s[u]['friendlyName']
# jsonkeys = data_s.keys()
# pprint.pprint(data_s)