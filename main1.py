import urllib
import re
import mechanize
from bs4 import BeautifulSoup
import urlparse
import couchdb #importing couchdb

#url = raw_input('Enter Url \n') 
url = ["http://cs.unipune.ac.in"]

visited = [url]

couch = couchdb.Server()  #connection with server
del couch['test'] #deleting existing database
db = couch.create('test') # newly created

i=0

while i<len(url):

    #Mechanize
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]
    br.open(url[i])

    #BeautifulSoup
    htmlcontent = urllib.urlopen(url[i])
    soup = BeautifulSoup(htmlcontent)

    levelLinks = []
    linkText = [] 
    imageLinks = []
    imageAlt = []

    for link in br.links(text_regex=re.compile('^((?!IMG).)*$')):
        newurl = urlparse.urljoin(link.base_url, link.url)
        b1 = urlparse.urlparse(newurl).hostname
        b2 = urlparse.urlparse(newurl).path
        wholeLink = "http://"+b1+b2
        linkTxt = link.text
        linkText.append(linkTxt)
        levelLinks.append(wholeLink)

    for linkwimg in soup.find_all('a'):
        imgSource = linkwimg.find('img')
        if linkwimg.find('img',alt=True):
            imgLink = linkwimg['href']
            imageLinks.append(imgLink)
            imgAlt = linkwimg.img['alt']
            imageAlt.append(imgAlt)
        elif linkwimg.find('img',alt=False):
            imgLink = linkwimg['href']
            imageLinks.append(imgLink)
            imgAlt = ['No Alt']
            imageAlt.append(imgAlt)

    print "\n\n\n\nLinks and Text for "+b1+":\n\n"

    #get Mechanize Links
    for l,lt in zip(levelLinks,linkText):
        print l,"\n",lt,"\n"
        doc = {'_id': lt,'link': l} #To insert new record
        db.save(doc) #To save document

    print "\n\n\n\nImage links and alt for "+b1+":\n\n"

    #get BeautifulSoup image Links & alt content
    for il,ia in zip(imageLinks,imageAlt):
        print il,"\n",ia,"\n"

    i+=1
