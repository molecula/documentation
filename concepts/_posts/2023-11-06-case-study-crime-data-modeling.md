---
title: Case Study - Data Modeling With Crime Data
---

This case study describes a way to conceptualize data modeling in FeatureBase versus a traditional RDBMS.

## Before you begin

* [Learn about FeatureBase bitmap indexing](https://www.featurebase.com/blog/bitmaps-making-real-time-analytics-real)

## The scenario

As a data professional, you are tasked with helping the city of Boston reduce crime by finding insights in past and current data.

## Task 1: import data to FeatureBase

You've decided to use FeatureBase to help you query and analyze the data.

The first task is to `head` the file and look at the provided schema to get a sense of the columns and, most importantly, what the grain of the data is.

This will ideally lead you to a unique identifier to operate as the primary key (or equivalent).

NOTE: FeatureBase requires a primary key, which is usually denoted as `_id` in the data model.

### Example data

```csv
INCIDENT_NUMBER,OFFENSE_CODE,OFFENSE_CODE_GROUP,OFFENSE_DESCRIPTION,DISTRICT,REPORTING_AREA,SHOOTING,OCCURRED_ON_DATE,YEAR,MONTH,DAY_OF_WEEK,HOUR,UCR_PART,STREET,Lat,Long,Location
I182070945,00619,Larceny,LARCENY ALL OTHERS,D14,808,,2018-09-02 13:00:00,2018,9,Sunday,13,Part One,LINCOLN ST,42.35779134,-71.13937053,"(42.35779134, -71.13937053)"
I182070943,01402,Vandalism,VANDALISM,C11,347,,2018-08-21 00:00:00,2018,8,Tuesday,0,Part Two,HECLA ST,42.30682138,-71.06030035,"(42.30682138, -71.06030035)"
```

* [Download the full Boston Crimes dataset](https://www.kaggle.com/datasets/AnalyzeBoston/crimes-in-boston)

### Identifying the key and cleaning the data

In the above data:
* `INCIDENT_NUMBER` is the perfect candidate for your key.
* `Location` seems unnecessary given “Lat” and “Long” already exist.

### Create the database and table for the data

FeatureBase’s use of bitmaps and bit slice indexing means you don’t have to worry about manually creating indexes on this table to improve city analysts' query performance. All that’s needed is the schema.

#### Example table

|Column Name| Data Type |
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

### Import (ingest) the data

For some databases this is a drag and drop GUI, and in others, like FeatureBase, it’s through a push-based ingestion.

In this example we suggest the use of the [streaming CSV ingestion method](/cloud//cloud-data-ingestion/streaming-https-endpoint/tutorial-streaming-csv).

### Troubleshooting Discrepancies

`INCIDENT_NUMBER` is not as unique as first expected, which creates a discrepancy between the data source and the FeatureBase database. For example:

* 319074 records in the data file
* 282517 records in the FeatureBase table

FeatureBase maintains unique keys and treats all ingest operations as UPSERTs. This means that each time a repeat incident was loaded, all the values in the table were updated for the incident record.

#### Example UPSERTs

|Datatype Being Updated | Behavior | Example |
| ------- | ------------ | ------------ |
| STRING, ID, INT, DECIMAL, TIMESTAMP  | Replace existing value | Existing FeatureBase Value: <br> app_status (STRING): Pending <br>New Value Sent:<br>Approved<br> New FeatureBase Value:<br> app_status (STRING): Approve
| IDSET, STRINGSET  | Add (not delete) new values | Existing FeatureBase Value: <br> app_status (STRINGSET): Pending <br>New Value Sent:<br>Approved<br> New FeatureBase Value:<br> app_status (STRINGSET): Pending, Approve

### Resolving the issue using IDSETS and STRINGSETS

The actual number of unique incidents is correctly represented in your database which means that the same crime won't be counted multiple times.

Looking at your data model, you’ve made a mistake assigning some columns like `OFFENSE_CODE` as integers. These codes are discrete values that should be treated categorically, as they will be used in GROUP BY and WHERE queries and not aggregated on or used in range queries.

Others, like “YEAR”, are appropriate because you might use range queries in addition to GROUP BY statements.

The `ID` type is used for unsigned integers that are more meaningful to represent as discrete values.

And `IDSET` can be used to store multiple ID values for a single column which is a better type for the `OFFENSE_CODE` column.

`STRINGSET` operates similarly and can be used to store multiple STRING values for a single column, such as “OFFENSE_CODE_GROUP”. It would also be appropriate for the `STREET` column if different values were populated with the data.

### A more efficient data model

The following changes to the data model will retain the definition and maintain the true incident count of 282517 unique incidents.

|Column Name| Data Type |
| ------- | ------------ |
| OFFENSE_CODE  | IDSET |
| OFFENSE_CODE_GROUP  | STRINGSET |
| offense_description  | STRINGSET |
| UCR_PART  | STRINGSET |

In addition, there is space savings compared to a traditional database table that writes many records with duplicate values for all the columns, which would result in:
* storing 36557 additional records with new keys for each
* storing records with identical `INCIDENT_NUMBER`s along with duplicate values for all the columns that don’t change (date/time columns (`OCCURRED_ON_DATE`, `MONTH`, etc.), `REPORTING_AREA`, `lat`, `long`, and more)

A traditional database table example:

|PK(_id)| INCIDENT_NUMBER | OFFENSE_CODE| OFFENSE_CODE_GROUP | OCCURRED_ON_DATE |
| ------- | ------------ | ------------ | ------------ | ------------ |
| 1 | **I162097077** | 00735 | Auto Theft Recovery | **2016-11-28T12:00:00Z** |
| 2 | **I162097077** | 01300 | Recovered Stolen Property | **2016-11-28T12:00:00Z** |
| 3 | **I162097077** | 03125 | Warrant Arrests | **2016-11-28T12:00:00Z** |


The data model using the `IDSET` and `STRINGSET` type columns is more efficient because each column only needs one additional bit set for each additional value.

A FeatureBase table example:

|INCIDENT_NUMBER (_id)| OFFENSE_CODE| OFFENSE_CODE_GROUP | OCCURRED_ON_DATE |
| ------- | ------------ | ------------ | ------------ |
| I162097077 | 00735,01300,00735  | Auto Theft Recovery, Warrant Arrests, Recovered Stolen Property | 2016-11-28T12:00:00Z |

## Task 2: long term planning

In the current data, all data is rolled up to one timestamp `OCCURRED_ON_DATE`, which means there's no way to associate when each unique `OFFENSE_CODE` was added to the `IDSET`. This means if different codes occur at different times for a single incident, the city will have no way of knowing.

An example might be a robbery that starts at a certain location, like the bank, which has a specific values for street, lat, long, etc., but then a couple hours later is given a car crash offense code at a different location when the robbers are stopped by the police.

### Using Time Quantums to add granularity without extra records

One solution is to have the attributes of each incident updated with an associated `UPDATE_DATE`. Note: this is a non-existent column in the dataset but something that could be added later on.

Time Quantums allow you to associate a time with each value in `IDSET` and `STRINGSET` columns. Using the Robbery example:

* A new value for `STREET` is added to the incident with an associated time (`UPDATE_DATE`) that corresponds to when the robbers crashed and were stopped by the police

#### Example record using time quantums

|INCIDENT_NUMBER (_id)| OFFENSE_CODE| STREET |
| ------- | ------------ | ------------ |
| I162097077 | 00735 (2016-11-28T12:00:00Z) <br> 01300 (2016-11-28T16:00:00Z) <br>00735 (2016-11-29T11:00:00Z)  | GIBSON ST (2016-11-28T12:00:00Z) <br> BROOKS ST(2016-11-28T16:00:00Z) <br> CENTRAL AVE (2016-11-29T11:00:00Z) |

NOTE: Times can only be used as filters and cannot be extracted or returned with a query result set.

#### The impact of time quantums

Now the city can analyze the data even further, such as seeing how an incident progresses over time (i.e. what streets were visited between two times), without having to create a new record every time there is an update for the incident. This is really powerful because the city can now accurately run queries that give them answers to question like “what crimes were occurring on this street between time A and time B?"

## Conclusion

The data models presented above will allow deeper analysis of data, including:

* a smaller data footprint
* low-latency advantages
* time-based query patterns

## Further information

* [Learn more about IDSETS and STRINGSETS](/sql-preview/data-types/data-types-home#data-types)
* [Learn more about Time Quantums](/concepts/time-quantums)
