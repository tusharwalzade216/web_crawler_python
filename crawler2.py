import urllib
import re
import mechanize
from bs4 import BeautifulSoup
import urlparse
import couchdb



def singalurl(url):


    htmlcantent = urllib.urlopen(url)
    sop=BeautifulSoup(htmlcantent)
    a=sop.findAll('a')
    ankar = []
    for h in a:
        ankar+=[urlparse.urljoin(str(url),(str(h.get('href'))))]
    
        lst=[]
        for t in ankar:
            if('#' not in t  and '?' not in t and '=' not in t):
                lst.append(t)

        link=[]
        for i in lst:
             if(i not in link and i != url):
                 link.append(i)

    return link


link=[] 
def multiurl(urls):
       for ur in urls:
#url='http://fb.com'
                       htmlcantent = urllib.urlopen(ur)
                       sop=BeautifulSoup(htmlcantent)
                       a=sop.findAll('a')
                       ankar = []
                       for h in a:
                           ankar+=[urlparse.urljoin(str(ur),(str(h.get('href'))))]
    
                           lst=[]
                           for t in ankar:
                               if('#' not in t  and '?' not in t and '=' not in t and '\xe3' not in t):
                                   lst.append(t)

                           #link=[]
                           for i in lst:
                               if(i not in link and i != ur):
                                   link.append(i)
       return link


x=[]
xy= []
def recartion(m,x):
    lent1=len(m)
    for l in m:
        if l in x:
            xy.append(l)
    x=m
    lent=len(xy)
    if lent==lent1:
        multiurl([])
        
    else:
        #x=m
        m=multiurl(m)
        print m
        recartion(m,x)
    
urls = singalurl('https://www.google.com')
#urls = singalurl('https://www.facebook.com')
#s = multiurl(['https://www.facebook.com/directory/places/'])
#multiurl(s)
#print s
print urls
#m = multiurl(['https://www.fb.com/', 'https://www.facebook.com/recover/initiate', 'https://www.fb.com/legal/terms', 'https://www.fb.com/about/privacy', 'https://www.fb.com/help/cookies', 'https://www.fb.com/pages/create/', 'https://www.facebook.com/', 'https://www.facebook.com/directory/people/', 'https://www.facebook.com/directory/pages/', 'https://www.facebook.com/facebook', 'https://www.facebook.com/privacy/explanation', 'https://www.facebook.com/directory/places/']) 
m = multiurl(urls)
#n = multiurl(m)
print m
#print n
#m=['http://www.fb.com','http://www.google.com']
#m=['http://www.google.com','http://www.fb.com']
recartion(m,x)
