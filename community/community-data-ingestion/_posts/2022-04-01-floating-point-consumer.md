---
id: floating-point-consumer
title: Floating Point / DataFrame Consumer
sidebar_label: Floating Point / DataFrame Consumer
---

## Overview

FeatureBase's native data format (the bitmap) is designed for high speed filtering and summation of integer and fixed point numbers (`Int` and `Decimal` field types). However, when you need to do more general purpose calculation such as multiplication, division, or transcendental functions, the `float64` and `int64` data types should be used. Currently, the best way to get data into FeatureBase using those types is the consumer documented here.

If you have a numeric field that you only want to compute sum, average, min, or max over, you do **not** need this consumer or the `float64` or `int64` field types. For these calculations, you can use the native `Int` or `Decimal` field types. 

Here are some examples of when to use the `float64` and `int64` field types:
- You want to return the output of values in the database after some unary operator has been applied to all / some of the values (e.g. return 10 percent of the `salary` field) 
- You want to return the product (or some other binary operator) of two fields for all records returned (e.g. return the product of `price` and `quantity` for all records)
- You want to return a complex aggregate statistic over some subset of records (e.g. return the standard deviation of the `age` field for people that use the Linux operating system)
- You want to return the output of a calculation that occurs accross records (e.g. return the euclidean distance between two records in the data set)

This is a small subset of the things you can do with the `float64` and `int64` field types. If you want to explore this functionality and the types of queries you can run, visit the documentation for [Apply()](/pql-guide/read/apply) and [Arrow()](/pql-guide/read/arrow).

## Considerations
Below are some things to consider when using this consumer:
- This consumer ingests data from a single CSV file (pointed to by the `-csv` flag)
- This consumer only ingest data to keyed indexes in FeatureBase
- In order to map data between bitmap fields and `float64`/`int64` fields, the first column in the CSV file should correspond the the record keys used for records with bitmap data.
- The first line in the CSV file must define the column name (which will be used to refer to the data in queries) and the column's field type. The format for each column must be `<column_name>__<column_type>` where `<column_type>` can take the value `F` for `float64` and `I` for `int64` data.

## Usage

Let's assume I have the following data currently stored in FeatureBase (in bitmaps).

```
+---------------------+-------------------+-------------------+
| _id                 | event (keyed set) | day (keyed set)   |
+---------------------+-------------------+-------------------+
| 2022-01-04 00:00:00 | [cloudy rain]     | [Tue]             |
| 2022-01-03 00:00:00 | [sunny]           | [Mon]             |
| 2022-01-01 00:00:00 | [cloudy]          | [Sat]             |
| 2022-01-02 00:00:00 | [cloudy rain]     | [Sun]             |
+---------------------+-------------------+-------------------+
```

Now, we want to add some `float64` and `int64` data to this index. Here is what the CSV file looks like (note the header has already been modified to define the name and type of fields).

```
date,min_temp__F,max_temp__F,rainfall__F,day_of_week__I
2022-01-01 00:00:00,14.0,26.9,3.6,6
2022-01-02 00:00:00,14.0,26.9,3.6,7
2022-01-03 00:00:00,13.7,23.4,0.0,1
2022-01-04 00:00:00,13.3,15.5,2.9,2
```

Using the consumer as part of the `featurebase` binary, we can run:

```
featurebase dataframe-csv-loader -csv weather.csv -index weather -featurebase-host localhost:10101
```

You can confirm the schema using the [HTTP API](/community/community-api/http-api#dataframe-endpoints). You can confirm / return the data using the [Arrow()](/pql-guide/read/arrow) PQL query. You can run analytical queries against the data using the [Apply()](/pql-guide/read/apply) PQL query.
