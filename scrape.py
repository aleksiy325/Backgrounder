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


def extract_pic_links(linklist, table, numberofpics):
	hdr = { 'User-Agent' : 'backgrounder by /u/aleksiy' }
	dlinklist = []
	flinklist = []
	
	while len(dlinklist) < numberofpics:
		url = linklist.pop(0)
		try:
			req = urllib2.Request(url, headers=hdr)
			html = urllib2.urlopen(req).read()
			soup = BeautifulSoup(html, "lxml")
			links = soup.findAll('a', attrs={'class' : 'title'})
			#add next page 
			next = soup.find('span', attrs={'class' : 'nextprev'})
			linklist.append(next.find('a')['href'])
			print "appended:" , next.find('a')['href']
			
			for ele in links:
				link = ele['href']
				if background.check_file_ext(link):
					link = clean_link(link)
					if not table.visited(link):
						dlinklist.append(link)
					else:
						print "already visited", link
				else:
					flinklist.append(link)
			
			
			#further process flinklist
			
			while flinklist:
				furl = flinklist.pop(0)
				#remove random reddit links
				if ("reddit" or "/r/") not in furl:
					req = urllib2.Request(furl, headers=hdr)
					print furl
					html = urllib2.urlopen(req).read()
					soup = BeautifulSoup(html, "lxml")
					links = soup.find('meta', attrs={'property' : 'og:image'})
					if links is not None:
						link = clean_link(links['content'])
						if not table.visited(link):
							dlinklist.append(link)
							print link
						else:
							print "already visited", link
		except Exception, e:
			print e
			traceback.print_exc()
			pass
		
		
		
		
		print "DONE LIST SIZE:" , len(dlinklist)
	return dlinklist

def download_images( urllist, path, table):
	count = 0
	for url in urllist:
		try:
			table.add(url)
			filename = url.split('/')[-1]
			urllib.urlretrieve(url, path + "\\" + filename)
			count += 1
			print "download", filename
		except Exception, e:
			print e
			pass
			
	#write table to file
	pickle.dump(table , open("table.p" , "wb"))		
	return count
 
 
if __name__ == "__main__":
	#PATHS
	BASE_PATH = os.path.dirname(os.path.abspath(__file__))+ "\\"
	PICS_PATH = BASE_PATH + "pics"	
	
	#settings 
	numberofpics = 25
	sources = 4
	
	
	
	#create dirs
	picdirs = [PICS_PATH]
	
	for path in picdirs:
		try: 
			os.makedirs(path)
		except OSError:
			if not os.path.isdir(path):
				raise
		
	
	
	
	if os.path.exists(BASE_PATH + "table.p"):
		table = pickle.load( open( "table.p", "rb" ) )
	else:
		table = hashtable.hashtable(64)
	
	
	url = ["https://reddit.com/r/futureporn", "https://www.reddit.com/r/imaginarywinterscapes" , "https://www.reddit.com/r/ImaginaryMindscapes" , "https://www.reddit.com/r/ImaginaryWorlds" ]
	
	random.shuffle(url)

	count = 0 
	list = []
	
	
	while( count < numberofpics):
		if len(list) < numberofpics - count:
			list = extract_pic_links(url , table , numberofpics * sources )
			random.shuffle(list)
		sublist = []
		for x in xrange(0 , numberofpics - count):
			sublist.append(list.pop(0))
		
		count += download_images(sublist , PICS_PATH, table)
		count -= background.populate_image_list(picdirs)
		print count
	
