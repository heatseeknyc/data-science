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



