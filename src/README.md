# Scripts and Source Code

This folder contains scripts and source code used by Heat Seek for collecting and analyzing data using APIs and/or web scraping.

## wunderground.py

This Python script is used to pull the average daily temperature for New York City for a given time range. 

###Usage

To execute this script, the following can be run at the command line:

```
python wunderground.py -t <TOKEN> -s <START_DATE> -e <END_DATE> -f True
```

Where ```-t``` is your WUnderground API token, ```-s``` is the start date for the range, ```-e``` is the end date for the range, and ```-f``` is an option flag for outputting in either Fahrenheit or Celsius. 

Dates should be written in the format of ``'YYYY-MM-DD'``` e.g. ```'2015-09-15'```

## bs_bin.py

This Python script is used to 'scrape' BIN information from NYC 'GOAT' site (http://a030-goat.nyc.gov/goat/Default.aspx). The retrieved BIN information is then merged in with building addresses and used with GIS/shapefile datasets to visualize data at the building level. 

###Usage

To execute this script, the following can be run at the command line:

```
python -u bs_bin.py > output_bk_2010_2015.csv
```

This will output all information to a file named ```output_bk_2010_2015.csv```

## bryan.ipynb

dirty_data(dirty_readings, start_date = None, end_date = None) takes a set of readings and returns a list of sensors that have weird readings. That's hard coded at > 90 outside temperature, < 40 inside temperature, and cases where the outside temperature is > than the inside temperature.

clean_data(dirty_readings) returns the subset of readings that don't include the ones above

sensor_down_complete takes a bunch of readings, a date range, and a sensor id, and returns the tenant's first and last name, the sensor id, the tenant id, the % of time each sensor was up in the entire date range, as well as the % of time they were up between each sensor's idiosyncratic first and last reading.

sensor_down is the same, just modified to produce a simple csv that will work with Emily's visualization.

generate_report takes a range of dates and runs the sensor_down function on all the sensors, and returns a dataframe with the information for all the sensors

simulate_data does what it says and generates a dataframe of fake readings that I used to test the other functions

violation_percentages is the thing I'm working on right now, and it's basically a measure of how severe a tenant's heating problem was. Right now I'm running with % of violation hours over total hours it was possible to get a violation.

