
import urllib2
import json


searchkey="https://www.googleapis.com/customsearch/v1?key=AIzaSyA4JLIQy1RNDH_n5UNZcmc1xPGOiV2EiiM&cx=008405862994369354446:bveyst4i9v0&q="
query="vishnu"
response = urllib2.urlopen(searchkey+query)
html = response.read()
data = json.loads(html)
for x in data["items"]:
  print x["formattedUrl"]



#print html["items"]





