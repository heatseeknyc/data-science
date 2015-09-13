# data-science

Repository for all-things-data at Heat Seek. This includes our methodologies, datasets, and information on the data visualization tools and techniques we utilize when performing data analysis. 


# Data Analysis and Methodology - Tools, Techniques and Technologies - Part I


## Overview

At Heat Seek, our aim is to use innovative technology and data to eradicate the heating epidemic plaguing tens of thousands of New York’s in the winter months. To fulfill this mission, data obviously plays a major role and we have repeatedly asked - and been asked - a lot of questions: just how bad is the heating situation for New Yorkers? Is this an ongoing problem? Which areas does this heating crisis effect the most? What boroughs submit the most heating complaints? How has the heating situation changed from year-to-year? Are there any other trends we see?

We start all of our analyses with a question and this often leads to a lot of other questions. When we have compiled a list and a simple Google search doesn’t suffice, then we start to dig in. With our questions comes the need for data and, oftentimes, even more data on top of that. Of course, at the heart of all of our analyses is data. 


## Data

At the heart of every analysis - whether it’s a Heat Seek’s or a university or a Fortune 500 company - obtaining data is key. A decade ago, one anecdote comments, someone remarked that ‘data is the new oil.’ More recently, another individual laughed at that statement. ‘Data is the new soil,’ he countered. Data is essential for answering questions and the world is drowning in it. We know we need data to answer our questions, but how do we find the right data? 

In New York City, as in many larger U.S. cities now, residents can file a 311 complaint for non-emergency services. Heating complaints are filed in this way. Thankfully, in NYC this dataset is available to the public and is used by city officials as one of several sources for the measurement of the performance of city services. Since heating complaints for residents of New York are accessible and formatted in a way that makes it very easy for us to start our analysis, NYC’s Open Data portal is where we often start. Specifically, the 311 dataset is key to many of our questions. 

Obviously, data is key when trying to get to the heart of a problem or answering questions. At Heat Seek, there are three main ways that we collect data: 

*Open Source data
*APIs
*Scraping web sites


Here we will talk about each data collection method and give examples of how we proceeded on each. 

###Open Data Portals

####New York City 311 Data

*1. Using NYC Open Data, we first search for "311 Service Requests from 2010-2015."*

A result should be returned. Selecting it shows that this is a large dataset: five years of complaint data, millions of rows, dozens of columns, and close to two hundred complaint types. Since our initial questions do not require every bit of information within this dataset, we can narrow down our scope. Before downloading this data, the Open Data portal allows us to filter by a specific column; for example, Complaint Type:


*2. We are interested in complaint types that deal with heating, so we can remove a lot of these rows before we download the dataset by filtering down to heat-specific complaints.* 

Using the site’s Filter panel, input the following:

Note that Complaint Types related to heat were originally, in 2010, labelled as ‘Heating.’ Later, the complaint type was labelled within the dataset as ‘HEAT/HOT WATER.’ This is why we need to include both values when filtering down with the Complaint Type column. 

*3. After filtering down to heat-specific complaints by tenants, we can now download this dataset.* 

On the right-hand side of the site, select the ‘Export’ icon:

The ‘Download’ prompt will come up and we see that a number of formatting options are available:

As you will see in the next section, a database such as PostgreSQL and a language such as R are two great ways in which explore and start an analysis of data. CSV-formatted data is very easy to import data into either and there are also data visualization tools which work well with comma-separated value files. 

*4. Select CSV or CSV for Excel and save the file locally to your computer.* 

The file is large, even with our filtering done, so it may take some time to download.

*5. Once the file has been downloaded, we can start to explore our data.* 

There are a couple of ways to quickly gain a high-level idea of the dataset using command-line tools.

To check the number of rows, for example, we can use the ```wc -l``` command:

```
> wc -l 311_Service_Requests_from_2010_to_Present.csv                                                                         
> 1165725 
```

Ok, so there are 1,165,725 rows within this dataset. That's a lot. But how many columns are there?

To check the number of columns we can use the incredibly useful ```awk``` command:

```
> awk -F',' '{print NF; exit}' 311_Service_Requests_from_2010_to_Present.csv
> 53
```

Additionally, we can see the overall size of the file using the ls command with certain flags:

```
> ls -lthr *2010_to_Present.csv
> -rw-r-----@ 1 jesse  staff   892M Jul 30 12:03 311_Service_Requests_from_2010_to_Present.csv
```

###APIs

####Weather Underground

In addition to 311 data, Heat Seek uses a number of other datasets to perform analysis. Weather Underground provides an excellent API for retrieving historical weather information. Additionally, the U.S. Census Bureau has recently released an API to access demographic, city-level data using CitySDK. 

Many of the examples below revolve around the 311 dataset. This dataset is available in its complete form on NYC’s Open Data site. While analyzing data - or when asking questions and having to find data - it’s rare that one dataset will have all of the information we need. In these cases we need to merge in other data using R or PostgreSQL. 

One dataset we use and merge with other data is Weather Underground’s historical temperature data. Weather Underground has a number of temperature sensors throughout the city and an API which allows us to retrieve this information. 

Within the our Github data-science repo and in the examples folder is a Python module called wunderground.py 

When run, wunderground.py will retrieve the average temperature - in fahrenheit - between a start and end date. That date and temp for that day is then printed to the screen e.g. 

```
2015-09-05,72.6407407407
2015-09-06,74.6583333333
2015-09-07,79.536
2015-09-08,84.6315789474
```
 
This example Python program can be run in the following way:

```
python wunderground.py -t <TOKEN> -s ‘2015-09-05’ -e ‘2015-09-08’ -f True
```

If we would rather have the temperatures in Celsius, we can leave the -f flag off entirely:

```
python wunderground.py -t <TOKEN> -s ‘2015-09-05’ -e ‘2015-09-08’
```

Note: in order to make calls to the API and retrieve historical temperatures you will need a Weather Underground API token. 

####CitySDK
