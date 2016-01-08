import urllib2
import urllib
from bs4 import BeautifulSoup
import background
import re
import os
import hashtable
import traceback
import pickle
import random
import threading
import Queue
import time

#INIT GLOBALS
exitFlag = 0
queueLock = threading.Lock()
workq = Queue.Queue()
threads = []
threadID = 1

class scrapeThread(threading.Thread):
    def __init__(self, threadID, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q
    
    def run(self):
        print "Starting thread: {}\n".format(self.threadID)
        process_data(self.threadID, workq)
        print "Exiting thread: {}\n".format(self.threadID)
        
        
def process_data(threadID, q):
    while not exitFlag:
        queueLock.acquire()
        if not q.empty():
            url = q.get()
            queueLock.release()
            #TODO PROCESS DATA
            print "{} {}\n".format(threadID, url )
        else:
            queueLock.release()
        time.sleep(1)
        
        
def extract_links(url):
    hdr = { 'User-Agent' : 'backgrounder by /u/aleksiy' }
	dlist = []
	flist = []
    
    #load page
    #TODO Error handlin 404 etc
    req = urllib2.Request(url, headers=hdr)
	html = urllib2.urlopen(req).read()
	soup = BeautifulSoup(html, "lxml")
    
    #add next page to queue
    next = soup.find('span', attrs={'class' : 'nextprev'})
    queueLock.acquire()
    workq.put(next)
    queueLock.release()
    
    #scrape pic links
	links = soup.findAll('a', attrs={'class' : 'title'})
    
    #sort links into direct and ones that need to be further scraped
    for ele in links:
        link = ele['href']
        if check_file_ext(link):
            link = clean_link(link)
            dlist.append(link)
            print link
            #TODO
            #check if visited
            #if not table.visited(link):
               # dlinklist.append(link)
            #else:
               # print "already visited", link
        else:
            flist.append(link)
            
            
    #further process links in flist
    while flist:
        furl = flinklist.pop(0)
        #ignore random reddit links
        if ("reddit" or "/r/") not in furl:
        
            #fetch data
            req = urllib2.Request(furl, headers=hdr)
            html = urllib2.urlopen(req).read()
            soup = BeautifulSoup(html, "lxml")
            
            #find meta image link
            links = soup.find('meta', attrs={'property' : 'og:image'})
            if links is not None:
                link = clean_link(links['content'])
                dlist.append(link)
                print link
                #TODO Table visited
                #if not table.visited(link):
                    #dlinklist.append(link)
                    #print link
               # else:
                   #print "already visited", link
                   
                   
                  

def clean_link(url):
	if ".jpg" in url:
		return url.split(".jpg")[0] + ".jpg"
	if ".jpeg" in url:
		return url.split(".jpeg")[0] + ".jpeg"
	if ".png" in url:
		return url.split(".png")[0] + ".png"
	if ".bmp" in url:
		return url.split(".bmp")[0] + ".bmp"
	if ".gif" in url:
		return url.split(".gif")[0] + ".gif"
	else:
		return url

def check_file_ext(file):
	#check file extension for pic
	if ".jpg" in file:
		return True
	if ".jpeg" in file:
		return True
	if ".png" in file:
		return True
	if ".bmp" in file:
		return True
	if ".gif" in file:
		return True
	return False        
    
        
def init_threads(nthreads):
    global threadID
    for x in xrange(0, nthreads):
        print "Initializing thread: {}\n ".format(threadID)
        thread = scrapeThread( threadID, workq)
        thread.start()
        threads.append(thread)
        threadID += 1
        
 
        
        
def main():
    global exitFlag
    nthreads = 10
    urllist = ["https://reddit.com/r/futureporn", "https://www.reddit.com/r/imaginarywinterscapes" , "https://www.reddit.com/r/ImaginaryMindscapes" , "https://www.reddit.com/r/ImaginaryWorlds" ]
     
    init_threads(nthreads)
    
    #add urls to queue
    queueLock.acquire()
    for ele in urllist:
        workq.put(ele)
    queueLock.release()
    
    #wait for exit condition
    #TODO change to len(list)
    while not workq.empty():
        pass
    
    #set exit flag notify threads to exit
    exitFlag = 1
    
    #wait for threads to complete
    for t in threads:
        t.join()
    print "Completed all tasks"
 
     

if __name__ == "__main__":
    main()
       
    