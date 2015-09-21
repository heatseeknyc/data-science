## Data Analysis and Methodology

### Tools, Techniques and Technologies 

- [Overview](#overview) 
- [Data](#data) 
    - [Open Data Sources](#opendata) 
        - [NYC 311 Data](#nyc311data)
             - [Obtaining the data](#obtainingdata)
    - [APIs](#apis)
        - [Weather Underground](#weatherunderground)
        - [CitySDK](#citysdk)
    - [Scraping Sites](#scraping)
        - [Building Information Numbers - BIN](#BIN)
- [Merging Data](#mergingdata)
- [Data Tools and Techniques: Extract, Transform, Load](#datatools)
    - [Loading and Analyzing Data Using R](#rdata)
        - [R Example #1: Total heating complaint counts by winter seasons](#rexample1)
        - [Verifying the Numbers](#verifying)
        - [R Example #2: Correlations between median income and complaint counts (by zip code)](#rexample2)
            - [Plotting a scatterplot using ggplot](#rscatterplot)
            - [Curve fitting](#rcurvefit)
    - [Cleaning, Massaging and Knowing Your Data](#cleaning)
        - [Using R](#usingr)
        - [awk](#awk)
        - [tail/head](#tail)
        - [sed](#sed)
        - [wc](#wc)
        - [man pages](#man)
    - [Loading and Analyzing Data Using PostgreSQL](#loadingpostgres)
        - [PostgreSQL Example #1: Loading, Querying and Exporting](#postgresex1)
            - [Setting up PostgreSQL for the first time](#postgresfirst)
            - [Creating the Heat Seek Database](#postgresdb)
            - [Creating the complaints table and loading the data](#postgrescomplaints)
            - [Querying and asking questions of the data](#postgresquerying)
            - [Exporting from PostgreSQL](#postgresexporting)
- [Appendix](#appendix)
    - [Useful Command-Line Tools](#usefulcommandlinetools)
    - [Useful PostgreSQL](#postgrescommands)
        - [Helpful Commands](#postgreshelpfulcommands)
    - [Useful Python](#pythoncommands)
    - [Useful R](#rcommands)
        - [Helpful Commands](#rhelpfulcommands)
    - [Other Useful Resources](#resources)
    - [Contact](#contact)
- [Licensing](#licensing)
        
  
<a name="overview"/>
## Overview

At Heat Seek, our aim is to use innovative technology to eradicate the heating epidemic plaguing tens of thousands of New Yorkers in the winter months. To fulfill this mission, we deploy custom sensors to track a tenant's apartment's indoor temperature and then record the number of violations per hour. In addition to the social and hardware aspect of our mission, data plays a major role as well. Our internal datasets are clearly the key to our success and the information we collect is then supplemented by external data. We spend a lot of time collecting and analyzing datasets and there's a lot of information out there.

We have repeatedly asked - and been asked - many questions related to our mission and heating complains throughout the five boroughs, including: 

* How many New Yorkers file heating complaints each winter? 
* Are the number of complaints going up or down each year? 
* In which boroughs and neighborhoods do the most heating complaints come from? 
* What other trends do we see?

We start all of our analyses with questions such as these and often our investigations lead to a lot of other questions. While we dig for answers we also find that there is *a lot* of information out there. How do we navigate this sea of data, discover meaning, spot trends, and ultimately answer our questions? This walkthrough will hopefully help you to understand how exactly we do just these sort of tasks at Heat Seek. Ultimately, at the heart of all of our analyses is data. But not just any sort. We want rich - and useful - datasets.

<a name="data"/>
## Data

Every analysis requires data. Within the last decade, there has been an explosion of Big Data: a substantially sized variety of information, that comes in many forms and structures. While massive datasets are available online, obtaining answers from this data is not trivial. To perform any meaningful analysis, good data are needed and collecting trustworthy data is actually more difficult than many think.

At a high level, there are three ways Heat Seek collects meaningful and useful data:

* Open Data Sources
* APIs
* Scraping Sites

To begin with, we'll start with [open data](https://en.wikipedia.org/wiki/Open_data) sources.

<a name="opendata"/>
###Open Data Sources

In New York City, as in many larger U.S. cities now, residents can file a 311 complaint for non-emergency services. What's more, the city provides this data to the public for free. This dataset has proven to be extremely valuable: city officials, for instance, use the 311 dataset as one of several sources for the measurement of the performance of public services. Additionally, individuals are free to access and analyze the data as well. NYC’s [Open Data](https://nycopendata.socrata.com/) portal - where the 311 dataset is updated daily - is where Heat Seek often starts when attempting to answer a heat-related question, though this dataset is just one source of information we use at Heat Seek. 

<a name="nyc311data"/>
####New York City 311 Data

<a name="obtainingdata"/>
#####Obtaining the data

To obtain the latest NYC 311 dataset, follow these steps. 

*1. Using [NYC Open Data](https://nycopendata.socrata.com/), let's search for '311 Service Requests from 2010-2015'. Or we can simply search for '311.'*

Results should include '311 Service Requests from 2010-2015.' This is a large dataset: five years of complaint data, millions of rows, dozens of columns, and close to two hundred complaint types. At Heat Seek, we are focused on questions around heating within tenant's apartment so it is not necessary to download all the information within this dataset. We can narrow down our scope using filtering. 


*2. We are interested in complaint types that deal with heating, so we can remove a lot of these rows before we download the dataset by filtering down to heat-specific complaints.* 

Using the site’s Filter panel, input the ```'HEAT/HOT WATER'``` and ```'Heating'``` within the Complaint Type filter.

Note that Complaint Types related to heat were originally, in 2010, labelled as ```‘Heating.’``` Later, the complaint type was labelled within the dataset as ```‘HEAT/HOT WATER.’``` This is why we need to include both values when filtering down with the Complaint Type column. 

*3. After filtering down to heat-specific complaints by tenants, we can now download this dataset.* 

On the right-hand side of the site, select the ‘Export’ icon:

The ‘Download’ prompt will come up and we see that a number of formatting options are available:

As you will see in the next section, a database such as PostgreSQL and a language such as R are two great ways in which to explore and start an analysis of data. CSV-formatted data is very easy to import into either and there are also data visualization tools which work well with comma-separated value files. 

*4. Select CSV or CSV for Excel and save the file locally to your computer.* 

The file is large, even with our filtering applied, so it may take some time to download.

*5. Once the file has been downloaded, we can start to explore our data.* 

There are a couple of ways to quickly gain a high-level idea of the dataset using command-line tools.

To check the number of rows, for example, we can use the ```wc -l``` command:

```
> wc -l 311_Service_Requests_from_2010_to_Present.csv                                                                         
> 1165725 
```

Ok, so we see that there are 1,165,725 rows within this dataset. That's a lot. But how many columns are there?

To check the number of columns we can use the ```awk``` command:

```
> awk -F',' '{print NF; exit}' 311_Service_Requests_from_2010_to_Present.csv
> 53
```

Additionally, we can see the overall size of the file using the ls command with certain flags:

```
> ls -lthr *2010_to_Present.csv
> -rw-r-----@ 1 jesse  staff   892M Jul 30 12:03 311_Service_Requests_from_2010_to_Present.csv
```

<a name="apis"/>
###APIs

<a name="weatherunderground"/>
####Weather Underground

In addition to 311 data, Heat Seek uses a number of other datasets to perform analysis. Weather Underground provides an excellent API for retrieving historical weather information. Additionally, the U.S. Census Bureau has recently released an API to access demographic, city-level data using CitySDK. 

Many of the examples below revolve around the 311 dataset. This dataset is available in its complete form on NYC’s Open Data site. While analyzing data - or when asking questions and having to find data - it’s rare that one dataset will have all of the information we need. In these cases we need to merge in other data using R or PostgreSQL. 

One dataset we use and merge with other data is Weather Underground’s historical temperature data. Weather Underground has a number of temperature sensors throughout the city and an API which allows us to retrieve this information. 

Within the examples folder of this repo is a Python module called wunderground.py 

When run with a set of flags, wunderground.py will retrieve the average temperature between a start and end date. That date and temp for that day is then printed to the screen e.g. 

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

<a name="citysdk"/>
####CitySDK

CitySDK is a project developed by the United States Census Bureau that provides a user-friendly “toolbox” for civic hackers to connect local and national public data. Heat Seek utilizes CitySDK to collect demographic data at the city-level and merge it in with our other datasets to gain a better understanding of the city's landscape as it relates to heating. More information on CitySDK can be found out: https://uscensusbureau.github.io/citysdk

<a name="scraping"/>
###Scraping Sites

Another way that Heat Seek obtains data is through web scraping. Python libraries such as Beautiful Soup allow us to collect information from various sites and this data can then be merged in with our other datasets. 

<a name="BIN"/>
#### Building Information Numbers - BIN
One example site that Heat Seek 'scraped' was the 'Geographic Online Address Translator' or [GOAT](http://a030-goat.nyc.gov/goat/Default.aspx). 

This site contains a lot of useful information when a user submits an address through the form. Data such as BIN, district numbers and other building-level information is returned. But this information is not readily available unless the form is submitted. Since information can be submitted through the URL, a Python script - bs_bin.py in the src directory - was created to assist in gathering this information. The BIN data was 'scraped' from each page after an address was entered in the URL by the script.

<a name="mergingdata"/>
###Merging Data

Once we have retrieved the temperatures for a given historical date range, we can then merge this data in with our other data. The date field is the key we use to merge in these average temperatures. In the case of PostgreSQL, a table with the date and temperature is first created and then a SELECT statement can be used to join the complaint data with the average daily temperature for each date. 

For example, if our historical temperature were stored in a table called temps an example SELECT statement would be:
```
SELECT * FROM complaints c, temps t WHERE c.created_date::date = t.date;
```
Note: Casting was done in this example to illustrate the complaints created_at column is a datetime, and the temps date column would most likely be of type date. 

In an [analysis earlier](http://heatseeknyc.tumblr.com/post/122874427185/a-persistent-and-predictable-problem) this summer, we merged complaint count data with weather data and then looked at the peaks and valleys between the two metrics. There was an obvious, inverse relationship but it also seemed that when temperatures dropped rapidly, complaints would also increase rapidly. In the second visualization of this blog post, it’s as though individuals get used to being cold and only call when the temperature drops suddenly again.

There are many ways to merge data and a database such as PostgreSQL is just one. 

<a name="datatools"/>
##Data Tools and Techniques Using ETL (Extract, Transform, Load)

Now that we have our initial dataset we’ll need some tools to start our analysis and answer some questions. Many data organizations do not use any one tool, technique or technology, and Heat Seek is no different. Languages such as R and Python are powerful when analyzing data and a databases such as PostgreSQL can help us quickly load, select and merge datasets. Additionally, we also utilize data visualization tools and libraries. These include Tableau, Spotfire, Adobe Illustrator, and libraries such as D3.js, Python's matplotlib, and R’s ggplot2. In this document we will focus on data; data visualization will be covered separately within the [Data Visualizations](Data Visualizations.md) section of this repository.

To begin with, let’s start with one of the most valuable weapons in data scientist's toolbox: R

<a name="rdata"/>
###Loading and Analyzing Data Using R

R is a language that has been used by statisticians and scientists for decades. With the rise of Big Data and the role of Data Scientist, it is becoming more popular and is considered one of the essential languages to know (along with Python, depending on how you ask). 

To use R, you should first have the [R development environment installed](https://www.r-project.org/). R will work with a variety of operating systems including Windows, OSX and Linux. Also, [R Studio](https://www.rstudio.com/products/rstudio/download/) is a great, supplemental tool for R code development as well. 

R is very simple to set up so once you have it installed you should be able to start following the steps outlined here to reproduce some of Heat Seek's analyses. 

Note: If you are not familiar with R, there are some great tutorials online. Additionally, Coursera offers some classes as well. The [Useful R](#rcommands) section of this tutorial has more information on these resources.

<a name="rexample1"/>
####R Example #1: Total heating complaint counts by winter seasons

*1. Within R, let’s first load the 311 data we downloaded into a dataframe called df:*

```
> df = read.csv("311_Service_Requests_from_2010_to_Present.csv")
```

Note: you may want to first use setwd() to set your working directory. You can also use the absolute path to point directly to the file. 

Additionally, if this is the first time you have set up R you may need to load some libraries as well. There are a lot of great R tutorials online to guide you through loading and using libraries, and basic R functionality. For the purposes of this post, though, we will not be focusing too heavily on R and instead will spend our energy guiding you through Heat Seek’s methodology and how you can reproduce our results. 

*2. Even with our filtering limiting the dataset to heating complaints, the file is large. Depending on your computer’s resources, reading in the may take some time to successfully load.* 

Let’s now look at the total number of rows in the dataset using nrow(df):

```
> nrow(df)
[1] 1165724
```

At the time of this writing, the dataset covered data from 2010 until mid-2015. Over a five year period we have 1,165,724 rows and each row represents a complaint related to heat. Each row also has a ‘Created.Date’ as well, so we know when the complaint was filed initially. 

Now let’s look at our total columns: 

```
> ncol(df)
[1] 53
```

This shows us that there are 53 columns within this dataset. Using the names() function, we can take a look at the column names as well:

```
> names(df)
 [1] "Unique.Key"                     
 [2] "Created.Date"                  
 [3] "Closed.Date"                    
 [4] "Agency"                        
 [5] "Agency.Name"                    
 [6] "Complaint.Type"                
 [7] "Descriptor"                     
 [8] "Location.Type"  
…
```

*3. Many of these columns are not needed and, considering the size of the dataset, the columns may slow us down during our analysis.* 

Let’s choose a relevant subset of columns to work with for our heat complaint analysis:

```
df_subset <- df[,c('Unique.Key','Created.Date','Closed.Date','Agency','Agency.Name','Complaint.Type','Descriptor','Location.Type','Incident.Zip','Incident.Address','Street.Name','Community.Board','Borough')]
```

Now if we check the number of columns within the df_subset dataframe, we should now see 15 columns of data. 

```
> ncol(df_subset)
[1] 13
```

Our row number has not changed: ~1.1 million rows of data spanning a five year period are still within the subset as nrow(df_subset) will confirm. 

We now know a few things about our dataset: the rows are related to heating complaints, the data spans 2010 until 2015, we have about one million rows of data for these five years, and we have limited to only the most ‘essential’ columns (for now). Since we have a general idea of what our data’s constraints are, let’s start to explore what’s in the data itself. 

*4. df_subset is our dataframe subset of 13 columns, and it’s broken out over five years. One of our questions is how many complaints have them been this year compared to the past?* 

Let’s first look at a breakout of counts by year. 

We first create a new column, which contains only the year for the given row:

```
> df_subset$Year <- format(as.Date(df_subset$Created.Date,'%m/%d/%Y'),'%Y')
> unique(df_subset$Year)
[1] "2015" "2014" "2013" "2012" "2011" "2010"
```

Now let’s look at the actual count of rows per each year in this new column:

```
> count(df_subset,"Year")
  Year   freq
1 2010 214218
2 2011 190184
3 2012 182974
4 2013 202896
5 2014 230364
6 2015 145088
```

Ok! We have some counts, broken out by year.

But in reality we want to see counts by winter, not just by year. But when does the winter officially start? We’ll have to do some digging online to find out.

To begin with, and according to this official New York City site, the official “Heat Season” in New York lasts from October 1st until May 31st each year. 

Within R, the Created.Date column is too granular for our needs. So let’s create a date column  we can filter on as well, so we can look at the winter of 2014-2015 according to NYC’s official site:

```
> df_subset$Date <- as.Date(df_subset$Created.Date, format = "%Y-%m-%d")

> sum(df_subset$Date >= "2014-10-01" & df_subset$Date <= "2015-05-31")
[1] 230702

> sum(df_subset$Date >= "2013-10-01" & df_subset$Date <= "2014-05-31")
[1] 212669
```

According to the analysis we’ve built so far, we can see that, between October 1st, 2014 and May 31st, 2015, there were 230,702 complaints related to heat in the city of New York. That’s a lot. We actually wrote about this back in June, and you can check our our entry here. 

<a name="verifying"/>
###Verifying the Numbers

But is this information we have found correct? It turns out that the [NYC Housing Preservation & Development (HPD)](http://www1.nyc.gov/site/hpd/index.page) publishes their [official total counts](http://www1.nyc.gov/site/hpd/renters/important-safety-issues-heat-hot-water.page) on their site. 

For the 2014-2015 winter season, HPD published a heating complaint count of 231,156. Using R and the steps above, we came to a total count of 230,702. For the 2013-2014 winter season, HPD published a heating complaint count of 212,563 and our complaint count is 212,669.

So, our total count - based on the public 311 data - compared to the count of official data is between 99.8 and 99.99% correct. We’re off but this could be due to any number or reasons and, given the number of rows, this is an acceptable margin of error.

Note: In a section below we walkthrough our methodology while using PostgreSQL. Using the database method, we also see the same numbers as we have seen with R. This illustrates that there has not been an issue with our technique or tools, but possibly with the data published on the Open Data site site. It's possible that some rows are missing from our open data source, for instance. Regardless, this margin of error is extremely small and acceptable. For more information on best practices and acceptable margins of error, you can check out Stanford's ["Statistical Perspectives and Recommendations"](http://bps.stanford.edu/?page_id=367) 

We can be confident in our numbers: we’ve just used R to summarize the data to find the total number of heat complaints for the 2014-2015 season, and below we will use PostgreSQL. We’re on the right track, which is great news. Now we can continue and expand to look at counts for previous winters as well.

In fact, in our [June 30th](http://heatseeknyc.com/blog) post we broke down the total number of heating complaints by each year to show how counts have, overall, increased over the last five years. We also illustrated this using a data visualization within the blog posting as well. 

Ok, let's take stock:

 - We have a reliable data source, which we've retrieved from NYC's Open Data portal
 - We then utilized the R language to load and perform a simple analysis of our data
 - Lastly, we have verified that our numbers look correct

Now let’s take a look at a little more complex example using R.


<a name="rexample2"/>
####R Example #2: Correlations between median income and complaint counts (by zip code)

In the example above, we’ve looked at a basic example of loading data, using R, and finding the complaint counts, by winter. Now let’s take a look at a more advanced analysis. 

In this analysis, we’ll be plotting both complaint counts and median income on the x and y axes, respectively. We’ll also briefly touch upon how the data visualization for a scatter plot can be created, but a deeper dive into this topic will be done in the follow-up post.

*1. We first set our working directory and then load in the data:*

```
setwd("/Users/jesse/Desktop")
df <- read.csv("complaint_count_vs_median_income_bronx_and_manhattan.csv")
```

*2. We can do a quick row/col count, just to make sure our dataset looks ok:*

```
> ncol(df)
[1] 7

> nrow(df)
[1] 129025


> head(df)
  Unique.Key Complaint.Type Incident.Zip   Borough          Winters Median.Income
1   30740154 HEAT/HOT WATER        10462     BRONX 2014-2015 Winter         56283
2   30742155 HEAT/HOT WATER        10452     BRONX 2014-2015 Winter         26187
3   30742153 HEAT/HOT WATER        10460     BRONX 2014-2015 Winter         16041
4   30740136 HEAT/HOT WATER        10466     BRONX 2014-2015 Winter         65909
5   30738219 HEAT/HOT WATER        10469     BRONX 2014-2015 Winter         61500
6   30740143 HEAT/HOT WATER        10033 MANHATTAN 2014-2015 Winter         47618
…

> names(df)
[1] "Unique.Key"     "Complaint.Type" "Incident.Zip"   "Borough"       "Winters"       
[6] "Population"     "Median.Income" 
```

*3. Ok, now we have an idea of what our data looks like. Let’s add in our plotting libraries and create a scatter plot to look at median income vs. complaint count.*

First, we pull in our required charting/SVG libs:

```
library(ggplot2)		## charting
library(plyr)		## helps get counts
library(RSvgDevice)	## for clean SVG export
```

*4. Now, let’s take a subset and grab only the data we want for our scatter plot. Then count up the number of rows (i.e. the complaint count per zip):*

```
> df_subset <- df[,c(3,4,7)]
> names(df_subset)
> [1] "Incident.Zip"  "Borough"       "Median.Income"

>
counts <- count(df_subset,c(1,2,3))
```

<a name="rscatterplot"/>
###### Plotting a scatterplot using ggplot 
*5. Now let’s look at a scatter plot using our counts and the subset of our data.* 

```
ggplot(counts,aes(x=Median.Income,y=freq,color=Borough)) +geom_point()
```

Now when we execute this command, we'll see a scatter plot populated. 

<a name="rcurvefit"/>
###### Curve fitting
*6. We can then go one step further, and look at line fitting such as Loess smoothing:*

```
> ggplot(counts,aes(x=Median.Income,y=freq)) +geom_point() +geom_smooth(method = "lm", formula = y ~ poly(x, 2), size = 1)
```

In the second part of this two-part series about methodology, which we will be posting in a couple of weeks, we will do a deeper dive into creating data visualizations.  

<a name="cleaning"/>
###Cleaning, Massaging and Knowing Your Data

If you are using a Mac or Linux, you have some very useful command line tools and methods for processing text and data. These tools are fast and, when mastered, can assist in a variety of ways when 'cleaning' your data. What do we mean by cleaning? Well, data that you have grabbed online will not always fit easily into a database, R or a data visualization tool. There could be bad formatting, for instance.   

With our Heat Seek data, we want only a subset of columns to load into Postgres (which we see at the end of this document). The ```awk``` command allows us to do a lot of selective manipulation, such as retrieving only columns we want from a file and output to a new file. ```awk``` is also very fast and, since many of the files we are analyzing have a large amount of data, this is helpful and much faster than opening in a program such as Excel, searching for and removing certain rows and/or columns, and re-saving the file. 

One useful technique to quickly convert a csv file into a semi-colon delimited file involves R. In fact, R has a number of useful commands for cleaning data and does a great job of handling 'dirty' data as well, but we will talk about that at another point. 

<a name="usingr"/>
####Using R
Using R, first load the entire 311 dataset of heating complaints into R, and then output a new csv file using a semicolon ; as a delimiter:

```
> df = read.csv("311_Service_Requests_from_2010_to_Present.csv")
> write.table(df, file = "test_data.csv",row.names=FALSE, na="N/A",col.names=FALSE, sep=";")
```


Note that we are temporarily using ; as a delimiter. R is helpful in cleaning in data, especially when there are commas within ields that can cause issues when loading and analyzing the data during other steps. 

<a name="awk"/>
####awk

```awk``` is a useful command-line tool and extremely versatile programming language for working on files. Rather than using GUI-based programs to work on files - programs like Excel - ```awk``` can help us quickly and effectively parse out information.

As an example, let's use awk to grab the columns we are going to load into our database:

```
awk -F "\"*;\"*" '{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$24,$25}' OFS="," 311_Service_Requests_from_2010_to_Present.csv > 311_Heat_Seek_Subset.csv
```


<a name="tail"/>
####tail/head

We already removed our header when we did the export from R. If we had not, though, there are ways we can do this from the command line. One method would be to use the ```tail``` command.

```
tail -n +2 311_Heat_Seek_Subset.csv > 311_Heat_Seek_Subset_No_Header.csv
```

tail -n +2 is saying “give me the ‘end’ of the file, starting at the second line.” file.txt is our input and we redirect the output to file.stdout

Additionally, we can use ```tail``` to look at the last n lines of a file. To output the last 10 lines of file.txt, we can run the following in terminal:

```
tail -n 10 file.txt
```

Similiar to ```tail``` is the ```head``` command. With ```head``` we can output starting from the beginning of a file, rather than the end. 

For more information on both of these commands, use ```man tail``` and ```man head``` respectively. 

<a name="sed"/>
####sed

Additionally, we can use sed to remove the first line of the file (i.e. the header). One such example is as follows:

```
sed '1d' 311_Heat_Seek_Subset.csv > 311_Heat_Seek_Subset_No_Header.csv
```

```sed``` - which stands for Stream EDitor - is a Unix utility that parses and transforms text, using a simple, compact programming language. Both ```awk``` and ```sed``` are powerful - and fast - command line tools and we use them often when performing data analysis at Heat Seek. These commands allow us to quickly clean and massage our data so that we can load into a database or application without issues.  

<a name="wc"/>
####wc 

From the command line, we can take a look at the total number of rows (from 2010 until 2015):

```
> wc -l 311_Heat_Seek_Subset.csv                    
 1165724 output.csv
```

```wc``` - while not as powerful and flexible as tools like ```awk``` and ```sed``` - is still useful when working with files. We can quickly check to see whether or not the expected number of rows have been parsed/excluded/included based on previous tools and commands. 

<a name="man"/>
####man pages

This is a small subset of useful tools at the command line and there are many more out there. Even while using a command, though, there are other options which may prove to be useful. We can read the documentation for a command by simply typing

```
man <command>
    
e.g.

man awk
```

The man page for the specific command - the manual - will then come up. 

<a name="loadingpostgres"/>
###Loading and Analyzing Data Using PostgreSQL

<a name="postgresex1"/>
####PostgreSQL Example #1: Loading, Querying and Exporting

As we mentioned before, we use a variety of techniques, tools and technologies to get to the heart of the data, to find answers to our questions. While R is our primary language for analyzing our data, databases such as PostgreSQL are invaluable tools to help us quickly load in and select subsets of data. We can also use PostgreSQL to merge datasets as well, as we’ll show below. 

First, we need data. Follow the steps in The Data section above. 

You will want to first download the 311_Service_Requests_from_2010_to_Present.csv file.

<a name="postgresfirst"/>
#####Setting up PostgreSQL for the first time

PostgreSQL is a type of Relational Database Management System (RDMS) and what we primarily use at Heat Seek to store much of our data. 

If you do not have PostgreSQL installed on your system, follow these simple steps (if on a Mac):

*1. Install PostgreSQL.* 

On a Mac using homebrew, you can simply type the following at a Terminal prompt: ```brew install postgresql```

*2. After you have PostgreSQL installed, download and install the postgres.app application.* 

This app makes it easy to start PostgreSQL. Launch the app and you will see a small elephant in your task tray. Your local instance should now be started.

*3. From terminal type psql.*

You should be logged into your local instance. You now have PostgreSQL installed. 

Note: if you have any issues getting PostgreSQL up and running, there are a number of great resources online. See the [Useful PostgreSQL](#postgrescommands) section for helpful information information.

<a name="postgresdb"/>
#####Creating the Heat Seek Database 

Now that you have PostgreSQL installed, we can create our Heat Seek instance and load in our data. 

*1. If you are at a terminal window, type psql to log into your PostgreSQL instance. Now create the database heatseek:*

```
CREATE DATABASE heatseek
```

*2. Log out using \q and then log into heatseek database:*

```
psql -d heatseek
```

*3. Now let’s revisit the 311_Service_Requests_from_2010_to_Present.csv file.* 

Remove all but the following 13 columns:

```
 id               
 created_date     
 closed_date      
 agency           
 agency_name     
 complaint_type   
 descriptor       
 location_type    
 incident_zip     
 incident_address  
 street_name      
 community_board  
 borough          
```
<a name="postgrescomplaints"/>
#####Creating the complaints table and loading the data

*1. Create the heatseek database and switch to it:*

```
CREATE DATABASE heatseek
USE heatseek
```

*2. Create the complaints table:*

```
CREATE TABLE complaints(
  id INT,
  created_date DATE,
  closed_date DATE,
  agency VARCHAR(10),
  agency_name VARCHAR(255),
  complaint_type VARCHAR(255),
  descriptor VARCHAR(255),
  location_type VARCHAR(30),
  incident_zip VARCHAR(5),
  incident_address VARCHAR(255),
  street_name VARCHAR(255),
  community_board VARCHAR(255),
  borough VARCHAR(20)
  ) 
```  

*2. Import the 3-1-1 data into the complaints table* 

e.g.
  
```
heatseek=# COPY complaints FROM '/Users/jesse/Desktop/311_Heat_Seek_Subset.csv' CSV;
COPY 1165724
```

You will need to change the location of the 311_Heat_Seek_Subset.csv location to match the location of your dataset.

<a name="postgresquerying"/>
#####Querying and asking questions of the data

Ok, if all goes well and the data loads into the table, we can now begin to extract the data and information about it from the psql terminal window. 

*1. Let’s check our total counts to make sure all rows from 2010 until 2015 were loaded:*

```
heatseek=# select count(id) from complaints;
  count
---------
 1165724
```

*2. Now let’s look at the 2014-2015 winter count:*

```
heatseek=# select COUNT(id) FROM complaints WHERE created_date >= '2014-10-01' AND created_date <= '2015-05-31';
 count
--------
 230702
```

As we showed in our blog post earlier this summer, this is the exact count we expect to see. 

*3. We can now use our database to give counts year-over-year, for instance:*

```
SELECT DATE_TRUNC('year', date) as date, 
       COUNT(*)
FROM (
  SELECT created_date as date
  FROM complaints) as foo
GROUP BY 1
ORDER BY 1, 2;

          date          | count
------------------------+--------
 2010-01-01 00:00:00-05 | 214218
 2011-01-01 00:00:00-05 | 190184
 2012-01-01 00:00:00-05 | 182974
 2013-01-01 00:00:00-05 | 202896
 2014-01-01 00:00:00-05 | 230364
 2015-01-01 00:00:00-05 | 145088
```

*4. But what we really need to see is the count over the winter dates, i.e. October 1st through May 31st of each year. One way we can do this is using a combination of UNION statements. *

```
SELECT '2014-2015', count FROM (select COUNT(id) as count FROM complaints WHERE created_date >= '2014-10-01' AND created_date <= '2015-05-31') as winter_2014_2015
UNION
SELECT '2013-2014', count FROM (select COUNT(id) as count FROM complaints WHERE created_date >= '2013-10-01' AND created_date <= '2014-05-31') as winter_2013_2014
UNION
SELECT '2012-2013', count FROM (select COUNT(id) as count FROM complaints WHERE created_date >= '2012-10-01' AND created_date <= '2013-05-31') as winter_2012_2013
UNION
SELECT '2011-2012', count FROM (select COUNT(id) as count FROM complaints WHERE created_date >= '2011-10-01' AND created_date <= '2012-05-31') as winter_2011_2012
UNION
SELECT '2010-2011', count FROM (select COUNT(id) as count FROM complaints WHERE created_date >= '2010-10-01' AND created_date <= '2011-05-31') as winter_2010_2011;

 	year | count
-----------+--------
 2013-2014 | 212669
 2012-2013 | 194122
 2014-2015 | 230702
 2011-2012 | 170488
 2010-2011 | 210522
```

We can see that the numbers match from our post on DATE as well here.

*5. Another question we had was the count by borough. We can easily modify our query to find the result of this information. For example, what were the total counts, by borough, for the 2014-2015 winter can be queried as:*



```
heatseek=# select borough, COUNT(id) FROM complaints WHERE created_date >= '2014-10-01' AND created_date <= '2015-05-31' GROUP BY 1 ORDER BY 2 DESC;


    borough    | count
---------------+-------
 BRONX         | 76501
 BROOKLYN      | 69358
 MANHATTAN     | 52524
 QUEENS        | 30162
 STATEN ISLAND |  2157
```


<a name="postgresexporting"/>
#####Exporting from PostgreSQL

In our next post on methodology and the steps we have taken at Heat Seek in our analyses, we’ll be looking at how we have created visualizations of our data. We often need to export our data from PostgreSQL in order to do that. 

Suppose we want to export all of our columns to a CSV file, focusing only on the 2014-2015 winter. We can do this using a combination of the COPY PostgreSQL command and a SQL statement:

```
heatseek=# COPY (SELECT * FROM complaints WHERE created_date >= '2014-10-01' AND created_date <= '2015-05-31' ORDER BY created_date ASC) To '/Users/jesse/Desktop/2014_2015_complaints.csv' WITH CSV;
COPY 230702
```

If you look on your desktop, you should see a file called 2014_2015_complaints.csv now. 

Another example would be exporting all winter 2014-2015 rows where the complaint was made in Brooklyn:

```
heatseek=# COPY (SELECT * FROM complaints WHERE created_date >= '2014-10-01' AND created_date <= '2015-05-31' AND borough LIKE '%BROOKLYN%') To '/Users/jesse/Desktop/2014_2015_brooklyn_complaints.csv' WITH CSV;
```

<a name="appendix"/>
##Appendix

<a name="usefulcommandlinetools"/>
###Useful Command-Line Tools

As mentioned [above](#cleaning), there are a number of useful command-line tools and utilities for cleaning and massaging data. 

<a name="postgrescommands"/>
###Useful PostgreSQL 

PostgreSQL is an object-relational database management system (ORDBMS) with an emphasis on extensibility and on standards-compliance. As a database server, its primary function is to store data securely, supporting best practices, and to allow for retrieval at the request of other software applications. At Heat Seek, PostgreSQL - or simply Postgres - is the primary database we use to store and retrieve data.

<a name="postgreshelpfulcommands"/>
####Helpful Commands
If you are not familiar with PostgreSQL, here are some useful commands:

List all databases:

```
\l 			
```

Use the ‘heatseek’ database:

```
use heatseek 	
```

List all tables:

```
\d 			
```

List columns in table:

```
\d <table> 
```

e.g. ```\d complaints```

Export database (run from command line, not from within psql):

```
pg_dump -U user -d database > blah.sql 
```

Import a .sql dump:

```
\i foo.sql 
```

Export all rows with created_date > 2015-01-01:

```
COPY (SELECT * FROM complaints WHERE created_date > '2015-01-01' ORDER BY created_date ASC) To '/Users/jesse/Desktop/2015_complaints.csv' WITH CSV;
```



<a name="pythoncommands"/>
###Useful Python 

- [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/) is an excellent library for scraping web pages. 

- [matplotlib](http://matplotlib.org/) is a python 2D plotting library which is useful when visualizating data and quickly prototyping. 

- [pandas](http://pandas.pydata.org/) is a library providing high-performance, easy-to-use data structures and data analysis tools. Highly recommended. Check out [Wes McKinney's tutorial](https://www.youtube.com/watch?v=w26x-z-BdWQ) as well. 


<a name="rcommands"/>
###Useful R 

- [R manuals](https://cran.r-project.org/manuals.html) document and assist with installation and syntax. 

- [R Programming](https://www.coursera.org/course/rprog) is a useful and incredibly informative class offered by Coursera online. Highly recommended for beginners. 

- [R Studio Cheatsheets](https://www.rstudio.com/resources/cheatsheets/) are helpful when using the R Studio application while developing R code. 


<a name="resources"/>
###Other Useful Resources

- [Coursera Data Science Courses](https://www.coursera.org/specializations/jhudatascience) can aid in gaining a complete understanding of data science techniques and tools, including R and exploratory data analysis. 


<a name="contact"/>
###Contact

For more information or if you have any questions, feel free to contact Jesse Fish at jessefish@gmail.com 

## Licensing

This application is MIT Licensed. See [LICENSE](https://github.com/heatseeknyc/data-science/blob/master/LICENSE) for details. 

Additional information on the MIT License is available at https://opensource.org/licenses/MIT
