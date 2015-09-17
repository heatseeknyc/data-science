import urllib2, json, time, sys
from datetime import date, datetime
from dateutil.rrule import rrule, DAILY
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", dest="fahrenheit", action="store", default=False, type="string", help="Convert to FAHRENHEIT")
parser.add_option("-e", dest="end", action="store", default=False, type="string", help="START date")
parser.add_option("-s", dest="start", action="store", default=False, type="string", help="END date")
parser.add_option("-t", dest="token", action="store", default=False, type="string", help="Weather Underground TOKEN")
(options, args) = parser.parse_args()

if options.token:
    token = options.token
else:
    parser.print_help()
    sys.exit()
	
if options.start:
    start = options.start
else:
    parser.print_help()
    sys.exit()
	
if options.end:
    end = options.end
else:
    parser.print_help()
    sys.exit()
	
if options.fahrenheit:
	fahrenheit = True
else:
	fahrenheit = False
	
start = datetime.strptime(start,'%Y-%m-%d')
end = datetime.strptime(end,'%Y-%m-%d')

url = ""

if end < start:
	print "Error: end date " + str(end) + " occurs before start date " + str(start)
	sys.exit()
	

for dt in rrule(DAILY, dtstart=start, until=end):
	
	total = 0.0
	temp = 0.0
  	count = 0
	
	wunderground_url ="http://api.wunderground.com/api/" + token + "/history_" + dt.strftime("%Y%m%d") +"/q/NY/New_York_City.json"

	try:
		url = urllib2.urlopen(wunderground_url)
		parsed_json = json.loads(url.read())
	except:
		print "Error reading URL " + wunderground_url
		print "Is your token correct?"
		url.close()
		sys.exit()
	
	try:
		for mean in parsed_json['history']['observations']:
			if fahrenheit:
				total += float(mean['tempi'])
			else:
				total += float(mean['tempm'])
  	  		count += 1 
			
		temp = (total / count)	
		print dt.strftime("%Y-%m-%d") + "," + str(temp)
	except:
		print "Error retrieving temperature records for start date " + str(start) + " end date " + str(end)
		url.close()
		
	time.sleep(10)
