from bs4 import BeautifulSoup
import urllib2
import nltk




html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""




#print(soup.get_text())

req = urllib2.Request('http://www.google.com')

response = urllib2.urlopen(req)

the_page = response.read()

htmlData=nltk.clean_html(the_page)

soup = BeautifulSoup(htmlData)

print(soup.get_text())


