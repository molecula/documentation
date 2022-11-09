---
title: Case Study - Data Modeling and Time Quantums
---

This case study describes a way to conceptualise data modeling in FeatureBase versus a traditional RDBMS.

## Before you begin

* [Learn about FeatureBase bitmap indexing](https://www.featurebase.com/blog/bitmaps-making-real-time-analytics-real)

## The scenario

As a data professional, you are tasked with helping the city of Boston reduce crime by finding insights in past and current data.

## Task 1: import data to FeatureBase

You've decided to use FeatureBase to help you query and analyse the data.

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

### Updated data model

The data model will retain the definition and maintain the true incident count of 282517 unique incidents.

|Data Type| Description |
| ------- | ------------ |
| OFFENSE_CODE  | IDSET |
| OFFENSE_CODE_GROUP  | STRINGSET |
| offense_description  | STRINGSET |
| UCR_PART  | STRINGSET |

In addition, there is a space saving compared to a traditional database which writes many records with duplicate values for all the columns , which would result in:
* storing 36557 additional records
* storing an identical `INCIDENT_NUMBER` multiple times
* New keys for each record, e.g., all data/time columns such as  `OCCURRED_ON_DATE`, “REPORTING_AREA”, `lat`, `long`, etc.

For example:

|PK(_id)| INCIDENT_NUMBER | OFFENSE_CODE| OFFENSE_CODE_GROUP | OCCURRED_ON_DATE |
| ------- | ------------ | ------------ | ------------ | ------------ |
| 1 | *I162097077* | 00735 | Auto Theft Recovery | *2016-11-28T12:00:00Z* |
| 2 | *I162097077* | 01300 | Recovered Stolen Property | *2016-11-28T12:00:00Z* |
| 3 | *I162097077* | 03125 | Warrant Arrests | *2016-11-28T12:00:00Z* |

### A more efficient data model

This data model is more efficient and only needs an additional bit tracked for each additional value in the `IDSET` and `STRINGSET` type columns.

|INCIDENT_NUMBER (_id)| OFFENSE_CODE| OFFENSE_CODE_GROUP | OCCURRED_ON_DATE |
| ------- | ------------ | ------------ | ------------ |
| I162097077 | 00735,01300,00735  | Auto Theft Recovery, Warrant Arrests, Recovered Stolen Property | 2016-11-28T12:00:00Z |

## Task 2: long term planning

In the current data, all data is rolled up to one timestamp `OCCURRED_ON_DATE` which means there's no way to identify when each unique `OFFENCE_CODE` was added. This means that related crimes are recorded as separate incidents.

### Using Time Quantums to add granularity without extra records

A solution is to have the attributes of each incident updated at an `UPDATE_DATE`.

Time Quantums allow you to associate a time with each value in `IDSET` and `STRINGSET` columns. For example:

* An incident occurs at a specified `STREET`
* A new value for `STREET` is added to represent a related incident, which is associated with an `UPDATE_DATE` column

NOTE: Times can only be used as filters and cannot be extracted or returned with a query result set.

#### Example data model

|INCIDENT_NUMBER (_id)| OFFENSE_CODE| STREET |
| ------- | ------------ | ------------ |
| I162097077 | 00735 (2016-11-28T12:00:00Z) <br> 01300 (2016-11-28T16:00:00Z) <br>00735 (2016-11-29T11:00:00Z)  | GIBSON ST (2016-11-28T12:00:00Z) <br> BROOKS ST(2016-11-28T16:00:00Z) <br> CENTRAL AVE (2016-11-29T11:00:00Z) |

## Conclusion

The data models presented above will allow deeper analysis of data, including:

* querying related incidents within the same record
* a smaller data footprint
* low-latency advantages

## Further information

* [Learn more about IDSETS and STRINGSETS](/cloud/cloud-data-modeling/data-types#data-types)
* [Learn more about Time Quantums](/concepts/time-quantums)
