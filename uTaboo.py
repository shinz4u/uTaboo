
from bs4 import BeautifulSoup
import urllib2
import nltk
import operator
import random
from nltk.corpus import stopwords
import json

class uTaboo:

    def __init__(self):
        pass

    def pickWord(file1='en-US.dic'):
        dictionary = open('en-US.dic')
        newlist=[]
        for line in dictionary:
            newlist.append(line)
        #print newlist
        choice1=random.choice(newlist)
        print choice1
        return choice1
        

    def getGoogledURLS(self,pickedWord):
    	urls=[]
    	searchkey="https://www.googleapis.com/customsearch/v1?key=AIzaSyA4JLIQy1RNDH_n5UNZcmc1xPGOiV2EiiM&cx=008405862994369354446:bveyst4i9v0&q="
    	query=pickedWord
    	response = urllib2.urlopen(searchkey+query)
    	html = response.read()
    	data = json.loads(html)
    	for x in data["items"]:
    		#print x["formattedUrl"]
    		urls.append(x["formattedUrl"])
    	return urls
    	pass
        
        
    def fetchHTML(self,url):
    	req = urllib2.Request('http://www.google.com')
    	response = urllib2.urlopen(req)
    	rawHtml = response.read()
        return rawHtml
        pass

     	#used ntlk to remove for now. Use beautiful soup to do that as well. Details in this link
    	# http://stackoverflow.com/questions/22799990/beatifulsoup4-get-text-still-has-javascript
    def stripScript(self,rawHtml):
     	cleanedHtml=nltk.clean_html(rawHtml)
     	return cleanedHtml
     	pass
        
    def getAllhtmls(self,urls):
        #use fetchHTML(url) to obtain a concatenated list of htmldata
        pass
        
    def html2Text(self,htmlData):
    	soup = BeautifulSoup(htmlData)
        return soup.get_text()
        pass

    def getUnprocessed(self,pickedWord):
    	myUrls = self.getGoogledURLS(pickedWord)
    	textData=""
    	for myUrl in myUrls:
    		rawHtml = self.fetchHTML(myUrl)
    		neathtml=self.stripScript(rawHtml)
    		textData=textData+" " + self.html2Text(neathtml)

        return textData
   
    # Second Module

    def filterStopWords(self,listOfWords):   
        return [ word for word in listOfWords if word not in stopwords.words('english') ]
        
    def getRankedList(self,filteredListofWords):
        rankedListOfWords={}
        for i in filteredListofWords:
            rankedListOfWords[i]=0
        for i in filteredListofWords:
            rankedListOfWords[i]=rankedListOfWords[i]+1
        return rankedListOfWords

    def fetchTop6(self,rankedListOfWords):
        ranked = sorted(rankedListOfWords.iteritems(), key=operator.itemgetter(1),reverse=True)
        tabooWords=[x for (x,y) in ranked]
        return tabooWords
        
        
    def getTabooWords(self,word,listOfWords):
        filteredListofWords=self.filterStopWords(listOfWords)
        rankedListOfWords=self.getRankedList(filteredListofWords)
        tabooWords=self.fetchTop6(rankedListOfWords)

        return tabooWords
        #return a dictionary with word as key and a list of 6 words as value
        pass
       

x = uTaboo()
word1=x.pickWord()
print word1
unProText=x.getUnprocessed(word1)

print x.getTabooWords(word1,unProText)

#print x.getRankedList(['hello','shinoy','smrithi','vishnu' , 'shinoy','radhika', 'shinoy','vishnu','vishnu'])