# Scripts and Source Code

This folder contains scripts and source code used by Heat Seek for collecting and analyzing data. 

## wunderground.py

This Python script is used to pull the average daily temperature for New York City for a given time range. To execute this script, the following can be run at the command line:

python wunderground.py -t <TOKEN> -s <START_DATE> -e <END_DATE> -f True

Where -t is your WUnderground API token, -s is the start date for the range, -e is the end date for the range, and -f is an option flag for outputting in either Fahrenheit or Celsius. 

Dates should be written in the format of 'YYYY-MM-DD' e.g. '2015-09-15'

