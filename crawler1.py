import urllib
import re
import mechanize
from bs4 import BeautifulSoup
#import BeautifulSoup
import urlparse

url = ["http://www.adbnews.com/area51/", "http://sheldonbrown.com/web_sample1.html","http://www.unipune.ac.in"]

visited = [url]


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

    print "\n\n\n\nImage links and alt for "+b1+":\n\n"

    #get BeautifulSoup image Links & alt content
    for il,ia in zip(imageLinks,imageAlt):
        print il,"\n",ia,"\n"

    i+=1
