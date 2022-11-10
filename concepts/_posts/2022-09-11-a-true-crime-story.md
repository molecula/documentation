---
title: A True Crime Story
---

Ok, not a crime story, but a data modeling story with true crime… Data! This doc describes the flow of how you, an individual in the data community, might think about modeling data in FeatureBase versus a traditional RDBMS. Many of the differences derive from the fact that FeatureBase is built entirely on bitmaps, which can be read about [here](https://www.featurebase.com/blog/bitmaps-making-real-time-analytics-real). The data referenced in this post is real crime data from Boston and can be referenced [here](https://www.kaggle.com/datasets/AnalyzeBoston/crimes-in-boston) to follow along.

As a data professional, you are tasked with helping the city of Boston reduce crime by finding insights in past and current data. You have just gotten your hands on a flat file with a couple of years of intriguing crime data, so now what? You realize this data is way too big to analyze on your local/virtual workspace (not really… but let’s say it is), so the first thing is getting it into a database in order to analyze and query the data much more easily.. You’ve decided you want to try FeatureBase because of all the great things you’ve heard. The first thing you’ll likely do is `head` the file and look at the provided schema to get a sense of the columns and, most importantly, what the grain of the data is. This ideally leads you to a unique identifier to operate as the primary key (or equivalent) for your table. FeatureBase requires a primary key, which is usually denoted as `_id` in the data model.

```csv
INCIDENT_NUMBER,OFFENSE_CODE,OFFENSE_CODE_GROUP,OFFENSE_DESCRIPTION,DISTRICT,REPORTING_AREA,SHOOTING,OCCURRED_ON_DATE,YEAR,MONTH,DAY_OF_WEEK,HOUR,UCR_PART,STREET,Lat,Long,Location
I182070945,00619,Larceny,LARCENY ALL OTHERS,D14,808,,2018-09-02 13:00:00,2018,9,Sunday,13,Part One,LINCOLN ST,42.35779134,-71.13937053,"(42.35779134, -71.13937053)"
I182070943,01402,Vandalism,VANDALISM,C11,347,,2018-08-21 00:00:00,2018,8,Tuesday,0,Part Two,HECLA ST,42.30682138,-71.06030035,"(42.30682138, -71.06030035)"
```

Quickly looking at the file, you identify “INCIDENT_NUMBER” as the perfect candidate for your key. After jotting down the other columns and their potential types, you also decide “Location” seems unnecessary given “Lat” and “Long” already exist. Now you are off to ingest the data! For most databases, including FeatureBase, this means creating a [table](/cloud/cloud-data-ingestion/tables) and modeling the columns based on what you see in the file. You’ve come up with the following for FeatureBase:

|Data Type| Description |
| ------- | ------------ |
| OFFENSE_CODE  | INT |
| OFFENSE_CODE_GROUP  | STRING |
| offense_description  | STRING |
| DISTRICT  | STRING |
| REPORTING_AREA  | STRING |
| SHOOTING  | STRING |
| OCCURRED_ON_DATE  | TIMESTAMP |
| YEAR  | INT |
| MONTH  | INT |
| DAY_OF_WEEK  | STRING |
| HOUR  | INT |
| UCR_PART  | STRING |
| STREET  | STRING |
| Lat  | DECIMAL |
| Long  | DECIMAL |

FeatureBase’s use of bitmaps and bit slice indexing means you don’t have to worry about manually creating indexes on this table to improve city analysts' query performance. All that’s needed is the schema. This is followed by sending the data to be ingested. For some databases this is a drag and drop GUI, and in others, like FeatureBase, it’s through [push-based ingest](/cloud/cloud-data-ingestion/streaming-https-endpoint/tutorial-streaming-csv).

After some expected back and forth and troubleshooting, you now have a FeatureBase table with 282,517 records! Job well done! Nothing could’ve gone wrong, but because it’s not your first rodeo, you do some simple record count validation to make sure no data was lost. Lo and behold you notice the file had 319,074 records! What is this madness? Well, it’s one of the differences between FeatureBase and other databases. It appears you made a mistake thinking “INCIDENT_NUMBER” was unique. Some databases may have thrown errors here because they would have seen duplicate values attempting to be loaded. Others may have ingested all 319,074 records because the backend implementation doesn’t require (or generates) unique keys. FeatureBase maintains unique keys and treats all ingest operations as UPSERTs. So every time a repeat incident number was loaded, all of the values in your table were updated for that incident’s record. The update behavior of UPSERTs depends on the data type that is being updated:

|Datatype Being Updated| Behavior| Example |
| ------- | ------------ | ------------ |
| STRING, ID, INT, DECIMAL, TIMESTAMP  | Replace existing value | Existing FeatureBase Value: <br> app_status (STRING): Pending <br>New Value Sent:<br>Approved<br> New FeatureBase Value:<br> app_status (STRING): Approve
| IDSET, STRINGSET  | Add (not delete) new values | Existing FeatureBase Value: <br> app_status (STRINGSET): Pending <br>New Value Sent:<br>Approved<br> New FeatureBase Value:<br> app_status (STRINGSET): Pending, Approve

Well now you are conflicted. On the one hand, you know this is the actual number of unique incidents, so counts on this table will reflect actuals (versus needing a count distinct with 319,074 records). This is nice because you know the city’s analysts won’t make mistakes and count the same crime multiple times. However, you have lost some of the definition of your data like offense codes and groups that have multiple values for a single incident. You could create a new unique key for this data, but you find a FeatureBase superpower, [IDSETS & STRINGSETS](/cloud/cloud-data-modeling/data-types#data-types). These datatype gives individual records the ability to store multiple values for a single column.

First, you look into `IDSET` but find you don’t know what the `ID` type is. After going through the docs, you find the `ID` type is for unsigned integers that are more meaningful to represent as discrete values. Looking at your data model, you’ve made a mistake assigning some columns like “OFFENSE_CODE'' as integers. These codes are discrete values that should be treated categorically, as they will be used in `GROUP BY` and `WHERE` queries and not aggregated on or used in range queries. Others, like “YEAR”, are appropriate because you might use range queries in addition to `GROUP BY` statements. Now understanding `ID`, you see `IDSET` can be used to store multiple `ID` values for a single column. This is exactly what columns like “OFFENSE_CODE'' need. Next, you see `STRINGSET` operates similarly and can be used to store multiple `STRING` values for a single column, such as “OFFENSE_CODE_GROUP”. This type would be appropriate for others like “STREET” if different values were populated with the data, which they are not today. You revisit your data model (updated types below) and now consider if this is a good move:

|Data Type| Description |
| ------- | ------------ |
| OFFENSE_CODE  | IDSET |
| OFFENSE_CODE_GROUP  | STRINGSET |
| offense_description  | STRINGSET |
| UCR_PART  | STRINGSET |

With this model, you won’t lose any of your data’s definition and will still maintain the true count of 282,517 unique incidents. What’s more, you see the space savings compared to both implementing a new unique key in FeatureBase and using a traditional database. A new unique key would have meant storing 36,557 additional records, and while these would be stored as efficient bitmaps, they would further grow your data footprint and potentially have an impact over time. You’d also be storing the same “INCIDENT_NUMBER”  multiple times in addition to the new keys for every record. A traditional database would have meant writing many records with duplicate values for all the columns that don’t change (all date/time columns ( i.e "OCCURRED_ON_DATE"), “REPORTING_AREA”, lat/long, et al):

|PK(_id)| INCIDENT_NUMBER | OFFENSE_CODE| OFFENSE_CODE_GROUP | OCCURRED_ON_DATE |
| ------- | ------------ | ------------ | ------------ | ------------ |
| 1 | *I162097077* | 00735 | Auto Theft Recovery | *2016-11-28T12:00:00Z* |
| 2 | *I162097077* | 01300 | Recovered Stolen Property | *2016-11-28T12:00:00Z* |
| 3 | *I162097077* | 03125 | Warrant Arrests | *2016-11-28T12:00:00Z* |


Your new data model is much more efficient and only needs an additional bit tracked for each additional value in the `IDSET` and `STRINGSET` type columns, so you feel good about this call! In fact it’d be a crime not to do this… Ok sorry for that.

|INCIDENT_NUMBER (_id)| OFFENSE_CODE| OFFENSE_CODE_GROUP | OCCURRED_ON_DATE |
| ------- | ------------ | ------------ | ------------ |
| I162097077 | 00735,01300,00735  | Auto Theft Recovery, Warrant Arrests, Recovered Stolen Property | 2016-11-28T12:00:00Z |

Now you start thinking about how Boston could improve their data over time. Today, everything in the data is rolled up to one timestamp, “OCCURRED_ON_DATE”, so there is no way to know when each of the unique offense_codes were added.  However, you have the foresight to know the city would love to track crime much more granularly. It seems like incidents in real life evolve over time, so it would be great to have each incident’s attributes updated at a time you are generically calling “UPDATE_DATE” for now. An example might be a robbery that starts at a certain location, like the bank (street, lat, long, et al), but then a couple hours later is given a car crash offense code at a different location when the robbers are stopped by the police. You want to add this ability but don’t want to add superfluous records for each “UPDATE_DATE”. Luckily, you find FeatureBase has another trick up its sleeve, [time quantums](/concepts/time-quantums). With time quantums, you are able to associate a time with each value in `IDSET` and `STRINGSET` type columns. In the robbery example, you could set a new value for “STREET” and associate the appropriate time this value occurred at with the “UPDATE_DATE”. A record with this data model is represented below, but it's important to note that the times cannot be extracted/returned with your query result set, only to filter by.

|INCIDENT_NUMBER (_id)| OFFENSE_CODE| STREET |
| ------- | ------------ | ------------ |
| I162097077 | 00735 (2016-11-28T12:00:00Z) <br> 01300 (2016-11-28T16:00:00Z) <br>00735 (2016-11-29T11:00:00Z)  | GIBSON ST (2016-11-28T12:00:00Z) <br> BROOKS ST(2016-11-28T16:00:00Z) <br> CENTRAL AVE (2016-11-29T11:00:00Z) |

Now the city can analyze the data even further, such as seeing how an incident progresses over time (i.e. what streets were visited between two times), without having to create a new record every time there is an update for the incident. This is really powerful because the city can now accurately run queries that give them answers to question like “what crimes were occurring on this street between time A and time B?” This, in combination with the smaller data footprint and many low-latency advantages FeatureBase brings, has you feeling pretty good about your proposed data model for Boston. What’s more, you feel much more confident about what you can do with FeatureBase for other data sources in the future.

Interested in following along with this exploration of Boston crime data? [Start your FREE FeatureBase Cloud trial today!](https://cloud.featurebase.com/signup)
