
from bs4 import BeautifulSoup
import urllib2
import nltk
from nltk.stem import WordNetLemmatizer
import operator
import random
from nltk.corpus import stopwords
import json
import re

class uTaboo:

    def __init__(self):
        pass

    def pickWord(file1='en-US.dic'):
        dictionary = open('en-US.dic')
        newlist=[]
        for line in dictionary:
            newlist.append(line)
        choice1=random.choice(newlist)
        return choice1
        

    def getGoogledURLS(self,pickedWord):
    	urls=[]
    	searchkey="https://www.googleapis.com/customsearch/v1?key=AIzaSyA4JLIQy1RNDH_n5UNZcmc1xPGOiV2EiiM&cx=008405862994369354446:bveyst4i9v0&q="
    	query=pickedWord
    	response = urllib2.urlopen(searchkey+query)

    	html = response.read()
    	data = json.loads(html)
    	for x in data["items"]:
    		urls.append(x["link"])
    	return urls
    	pass
        
        
    def fetchHTML(self,url):

    	print url
    	req = urllib2.Request(url)
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
        
        
    def html2Text(self,htmlData):
    	soup = BeautifulSoup(htmlData)
        return soup.get_text()
        pass

    def getUnprocessed(self,pickedWord):
    	myUrls = self.getGoogledURLS(pickedWord)
    	textData=""
    	print myUrls
    	for myUrl in myUrls:
    		if myUrl.find(".pdf")==-1:
    			print "\nopen.."
	    		rawHtml = self.fetchHTML(myUrl)
	    		neathtml=self.stripScript(rawHtml)
	    		#print neathtml
	    		textData=textData+" " + self.html2Text(neathtml)

        return textData

    # Second Module
    def sanitizeWords(self,listOfWords):   # takes input text. output: split sanitized words
    	lemmatizer = WordNetLemmatizer()
    	sanitized=re.sub(r'[^\w]', ' ', listOfWords)
    	sanitized=[y.lower() for y in sanitized.split()]
    	sanitized=[lemmatizer.lemmatize(y) for y in sanitized]   #Lemmatazation 
    	return sanitized
    	pass
   

    def filterExtraWords(self,word1,listOfWords1):
        x = [word for word in listOfWords1 if word not in stopwords.words('english')]
        word1=word1[0:len(word1)-1]
        otherWords=[word1,word1+'s']
        x = [word for word in x if word not in otherWords]
        return x


        
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
        return tabooWords[0:6]
        
    def getTabooWords(self,word,listOfWords):
        filteredListofWords=self.filterExtraWords(word,listOfWords)
        rankedListOfWords=self.getRankedList(filteredListofWords)
        tabooWords=self.fetchTop6(rankedListOfWords)
        return tabooWords

       

x = uTaboo()
word1=x.pickWord()
print word1
unProText=x.getUnprocessed(word1)
sanitizedWords=x.sanitizeWords(unProText)
print x.getTabooWords(word1,sanitizedWords)

#print x.getRankedList(['hello','shinoy','smrithi','vishnu' , 'shinoy','radhika', 'shinoy','vishnu','vishnu'])