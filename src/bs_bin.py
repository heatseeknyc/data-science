# bs_bin.py
# Author: Jesse Fish
# 
# Description: Visit NYC 'GOAT' site, using an address within the URL, 
# and grab BIN for each building. Data then merged into dataset for 
# use with GIS/shapefile maps for visualization. 

from bs4 import BeautifulSoup
import urllib
import time

# open list of brooklyn addresses that have made heat complaints in last 5 years
with open('2010_2015_brooklyn_complaints.csv') as in_file:
	for line in in_file:
		try:
			# read in line, split based on , delimiter
			parts = line.split(",") 
			indexEnd = parts[0].index(" ")
			
			# grab address number and street and building URL for GOAT site
			addressNumber = str(parts[0])[0:indexEnd] 
			street= str(parts[0])[indexEnd+1:len(parts[0])].replace(" ","+") 
			url = "&addressNumber=" + addressNumber + "&street=" + street
			
			# load site, scrape using soup; look for label_bin_output to pull BIN
			r = urllib.urlopen('http://a030-goat.nyc.gov/goat/Default.aspx?boro=3&' + url).read()
			soup = BeautifulSoup(r,"lxml")
			bin = soup.find('span', {'id': 'label_bin_output'})
			
			# format output to be: address/zip/count (line) and with BIN appended 
			the_line = line.replace('\n','') + "," + str(bin).replace("</span>","").replace("<span id=\"label_bin_output\">","")
		
			# utf-8 encoding in case anything strange
			print str(the_line).encode('utf-8')
			
		except:
			print "error"
			
		# wait 3 seconds before hitting url again so site is not overloaded
		time.sleep(3)
