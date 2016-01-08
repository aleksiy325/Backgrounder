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
       
    