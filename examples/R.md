
#### Load 311_Service_Requests_from_2010_to_Present.csv and create df_subset

```
df = read.csv("311_Service_Requests_from_2010_to_Present.csv")

df_subset <- df[,c('Unique.Key','Created.Date','Closed.Date','Agency','Agency.Name','Complaint.Type','Descriptor','Location.Type','Incident.Zip','Incident.Address','Street.Name','Community.Board','Borough')]
```

#### Create new 'Year' column and sume complaints by year
```
df_subset$Year <- format(as.Date(df_subset$Created.Date,'%m/%d/%Y'),'%Y')
> unique(df_subset$Year)
[1] "2015" "2014" "2013" "2012" "2011" "2010"

> count(df_subset,"Year")
  Year   freq
1 2010 214218
2 2011 190184
3 2012 182974
4 2013 202896
5 2014 230364
6 2015 145088
```

#### Create 'Date' column and sum rows for particular winter

```
> df_subset$Date <- as.Date(df_subset$Created.Date, format = "%Y-%m-%d")

> sum(df_subset$Date >= "2014-10-01" & df_subset$Date <= "2015-05-31")
[1] 230702
```


