#!/usr/bin/env python


from bs4 import BeautifulSoup
import urllib2
import nltk
from nltk.stem import WordNetLemmatizer
import operator
import random
from nltk.corpus import stopwords
import json
import re
import sys

class uTaboo:

    def __init__(self):
        pass

    # This function picks a word from the english dictionary or as arguments
    # while executing the program.
    def pickWord(file1='Fruits.txt'):
        if len(sys.argv) > 1:
            return sys.argv[1]
        dictionary = open('Fruits.txt')
        newlist = []
        for line in dictionary:
            newlist.append(line)
        return newlist

    # Returns url's of webpages for the query word from pickWord function.
    def getGoogledURLS(self, pickedWord):
        urls = []
        print pickedWord
        searchkey = "https://www.googleapis.com/customsearch/v1?key=AIzaSyA4JLIQy1RNDH_n5UNZcmc1xPGOiV2EiiM&cx=008405862994369354446:bveyst4i9v0&q="
        query = str(pickedWord)
        response = urllib2.urlopen(url = searchkey+query)
        print response

        #urllib2.urlopen(url[, data[, timeout[, cafile[, capath[, cadefault[, context]]]]])
        
        html = response.read()
        data = json.loads(html)
        for x in data["items"]:
            urls.append(x["link"])
        return urls
        pass

    # Returns rawHTML of the url's returned from getGoogledURLS for processing.
    def fetchHTML(self, url):

        print url
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        rawHtml = response.read()
        return rawHtml
        pass

    # Removes HTML markup
    def stripScript(self, rawHtml):
        soup = BeautifulSoup(rawHtml,"lxml")
        cleanedHtml = soup.get_text()
        return cleanedHtml
        pass

    # Cleans HTML to obtain just text
    def html2Text(self, htmlData):
        soup = BeautifulSoup(htmlData,"lxml")
        return soup.get_text()
        pass

    # Gets text data by opening URL's and cleaning the html data to get just
    # text.
    def getUnprocessed(self, pickedWord):
        print pickedWord
        myUrls = self.getGoogledURLS(pickedWord)
        textData = ""
        print myUrls
        for myUrl in myUrls:
            if myUrl.find(".pdf") == -1:
                print "\nopen.."
                while True:
                    try:
                        rawHtml = self.fetchHTML(myUrl)
                        neathtml = self.stripScript(rawHtml)
                        break
                    except urllib2.HTTPError, e:
                        break


                
                # print neathtml
                textData = textData + " " + self.html2Text(neathtml)

        return textData

    # Second Module 
    # Split words based on sentences or words that makes sense. Cleans digits.
    def sanitizeWords(self, listOfWords):
        lemmatizer = WordNetLemmatizer()
        sanitized = re.sub(r'[^\w]', ' ', listOfWords)
        # put to lower case, remove complete numbers
        sanitized = [y.lower()
                     for y in sanitized.split() if y.isdigit() != True]
        sanitized = [lemmatizer.lemmatize(y)
                     for y in sanitized]  # Lemmatazation
        return sanitized
        pass

    # Remove stopwords from data such as and, the, is, was etc.
    def filterExtraWords(self, word1, listOfWords1):
        x = [
            word for word in listOfWords1 if word not in stopwords.words('english')]
        word1 = word1[0:len(word1) - 1]
        otherWords = [word1, word1 + 's']
        x = [word for word in x if word not in otherWords]
        return x

    # Rank words depending upon the frequency of occurance of the words.
    def getRankedList(self, filteredListofWords):
        rankedListOfWords = {}
        for i in filteredListofWords:
            rankedListOfWords[i] = 0
        for i in filteredListofWords:
            rankedListOfWords[i] = rankedListOfWords[i] + 1
        return rankedListOfWords

    # Get the top 6 words from the list of rankedListOfWords
    def fetchTop6(self, rankedListOfWords):
        ranked = sorted(
            rankedListOfWords.iteritems(),
            key=operator.itemgetter(1),
            reverse=True)
        tabooWords = [x for (x, y) in ranked]
        return tabooWords[0:6]

    # Get taboo words which calls all the functions.
    def getTabooWords(self, word, listOfWords):
        filteredListofWords = self.filterExtraWords(word, listOfWords)
        rankedListOfWords = self.getRankedList(filteredListofWords)
        tabooWords = self.fetchTop6(rankedListOfWords)
        return tabooWords

x = uTaboo()
word1 = x.pickWord()
print word1

count = 0
dic = {}
for i in word1:
    count += 1
    if count > 4:
        break
    unProText = x.getUnprocessed(i)
    sanitizedWords = x.sanitizeWords(unProText)
    finalWords = x.getTabooWords(i, sanitizedWords)
    Super_Words = []
    for k in finalWords:
        Super_Words.append(k)
    print Super_Words   

    dic[i] = Super_Words


jsonData = json.dumps(dic, sort_keys = True, indent = 4 ,separators= (',',':'))
print(jsonData)
with open('test.json', 'w') as f:
    json.dump(jsonData, f)


