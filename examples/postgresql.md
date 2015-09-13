
#### Create 'heatseek' database and 'complaints' table

```
CREATE DATABASE heatseek;

USE heatseek;

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
  ); 
  
 ```
 
#### Load 311 data into 'complaints' table

```
heatseek=# COPY complaints FROM '/Users/jesse/Desktop/311_Heat_Seek_Subset.csv' CSV;
COPY 1165724
```

#### Querying complaint counts

##### 2014-2015 winter - total complaint count

```
heatseek=# select COUNT(id) FROM complaints WHERE created_date >= '2014-10-01' AND created_date <= '2015-05-31';


 count
--------
 230702
```

##### Year-over-year counts

```
SELECT '2014-2015' as year, count FROM (select COUNT(id) as count FROM complaints WHERE created_date >= '2014-10-01' AND created_date <= '2015-05-31') as winter_2014_2015
UNION
SELECT '2013-2014' as year, count FROM (select COUNT(id) as count FROM complaints WHERE created_date >= '2013-10-01' AND created_date <= '2014-05-31') as winter_2013_2014
UNION
SELECT '2012-2013' as year, count FROM (select COUNT(id) as count FROM complaints WHERE created_date >= '2012-10-01' AND created_date <= '2013-05-31') as winter_2012_2013
UNION
SELECT '2011-2012' as year, count FROM (select COUNT(id) as count FROM complaints WHERE created_date >= '2011-10-01' AND created_date <= '2012-05-31') as winter_2011_2012
UNION
SELECT '2010-2011' as year, count FROM (select COUNT(id) as count FROM complaints WHERE created_date >= '2010-10-01' AND created_date <= '2011-05-31') as winter_2010_2011;


     year  | count
-----------+--------
 2013-2014 | 212669
 2012-2013 | 194122
 2014-2015 | 230702
 2011-2012 | 170488
 2010-2011 | 210522
 ```
