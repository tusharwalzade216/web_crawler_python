import couchdb
couch = couchdb.Server()
#x = raw_input('enter the url\n')
#print x
#del couch[x]
#db = couch.create(x) # newly created
#db = couch['test1'] # existing


visited = raw_input('enter url')
data = raw_input('enter the data')
#try:
db = couch.create('issc')
doc_id1, doc_rev1 = db.save({'_id':visited,'link':data})
   # doc_id2, doc_rev2 = db.save({'_id':'unvisited','link':[]})

#except Exception:
#   db = server['test']

#doc1 = {"text": "Sandeep","rating": 113} #To insert new record
#db.save(doc1) #To save document

#for id in db:
#    print id





#s=db.get('text')
#print s


