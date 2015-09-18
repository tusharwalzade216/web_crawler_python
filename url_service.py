import socket, select, sys
import sys
from BeautifulSoup import BeautifulSoup
import urllib
import re
import urlparse
import couchdb

#connecting to the couchdb server of local machine
server = couchdb.Server()
try:
    db = server.create('url_service')
    doc_id1, doc_rev1 = db.save({'_id':'visited','link':[]})
    doc_id2, doc_rev2 = db.save({'_id':'unvisited','link':[]})

except Exception:
    db = server['url_service']

#crawling a link given while starting the whole multi crawling(url_service) program
def crawler(link):
    url2 = urllib.urlopen(link)
    soup=BeautifulSoup(url2)
    fall=soup.findAll('a')
    urllist = []
    for h in fall:
        urllist+=[urlparse.urljoin(str(link),(str(h.get('href'))))]
    
    lst=[]
    for t in urllist:
	if('#' not in t):
	   lst.append(t)

    links1=[]
    for i in lst:
	if(i not in links1 and i != link):
            links1.append(i)
    
    u = db.get('unvisited')
    v = db.get('visited')
    doc_u = {'_id':u['_id'],'_rev':u['_rev'],'link':(u['link']+links1)}
    db.save(doc_u)
    doc_v = {'_id':v['_id'],'_rev':v['_rev'],'link':(v['link']+[link])}
    db.save(doc_v)


#for url service - taking 1 from 'unvisited',putting it into 'visited'  
#and giving it back to the idle client for new crawling
def url_db():
    u = db.get('unvisited')
    if(len(u['link']) == 0):
        return ''
    else:
        lk = u['link'][0]    			
        doc_u = {'_id':u['_id'],'_rev':u['_rev'],'link':u['link'][1:]}
        db.save(doc_u)
        v = db.get('visited')
        if(lk not in v['link']):
            tempLst = [lk] + v['link']			
            doc_v = {'_id':v['_id'],'_rev':v['_rev'],'link':tempLst}
            db.save(doc_v)
            return lk
        else:
            return url_db()
        

 
if __name__ == "__main__":
     
    
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    CLIENT_ADDR_LIST = []
    RECV_BUFFER = 999999 
    PORT = 5000
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
    crawler(sys.argv[2])
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                CLIENT_ADDR_LIST.append(addr)
		sockfd.sendto(url_db(),sockfd.getpeername())
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        sender=sock.getpeername()
                        print data
			k = url_db()
			if(len(k) != 0):   
                           sock.sendto(k,sock.getpeername())
			else:
			   server_socket.close()
				
                        
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()
