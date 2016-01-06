import ctypes
import time
import os
from PIL import Image
import scrape



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
		
		
def check_size(path, dXres,  dYres):


	
	try:
		image = Image.open(path)
	except Exception:
		print "Error:" , path
		return False
		
	x, y  = image.size 
	
	#x y difference
	xdiff = float(x) /dXres
	ydiff = float(y) /dYres
	
	
	
	#aspect ratio
	dar = float(dXres) / dYres
	par = float(x) / y
	rdiff = abs((dar - par) / dar)
	
	
	
	print rdiff, x, y, par
	# false if aspect ratio is more than 40% diff or pic x or y is below 0.5 
	#REJECTION SETTINGS
	return rdiff < 0.5 and xdiff > 0.75 and ydiff > 0.75
	
	
	

def populate_image_list( pathlist ):
	#DESKTOP RES
	xres = ctypes.windll.user32.GetSystemMetrics(0)
	yres = ctypes.windll.user32.GetSystemMetrics(1)
	
	
	
	rejected = 0

	picslist = []
	#loop through all dirs
	for path in pathlist:
		#loop through contents and add to list if pic
		for ele in os.listdir(path):
			#check if pics and add
			if check_file_ext(ele):
				if check_size(path + "\\" + ele, xres,  yres):
					picslist.append(path + "\\" + ele)
				else:
					#delete
					os.remove(path + "\\" + ele)
					rejected += 1
					
	

	print rejected, "rejected"
	
	return len(picslist)