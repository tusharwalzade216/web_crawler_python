import urllib
import re
import mechanize
from bs4 import BeautifulSoup
import urlparse
import couchdb #importing couchdb

str1=raw_input('Enter word to search : ')


couch = couchdb.Server()
db = couch['test']

for id in db:
   #print id.find(str1)
   if id.find(str1)>=0:
      u = db.get(id)
      doc_u = u['link']
      print doc_u
