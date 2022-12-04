---
id: floating-point-consumer
title: Floating Point Consumer
sidebar_label: Floating Point Consumer
---

### Overview

FeatureBase's native data format (the bitmap) is designed for high speed filtering and summation of integers and fixed point numbers (Int and Decimal field types). However, when you need more general purpose calculation such as multiplication, division, or transcendental functions, the float64 and int64 data types should be used. Currently, the best way to get data into FeatureBase using those types is the consumer documented here.

If you have a numeric value that you only want to compute `Sum()`, `Average()`, `Min()`, or `Max()` over, you should **not** use this consumer or the `float64` or `int64` field types. For these calculations, you should use the native Int or Decimal field types. 

Here are some examples when to use the `float64` and `int64` field types:
- You want to return the output of values in the database after some unary operator has been applied to all / some of the values (e.g. return 10 percent of the `salary` field) 
- You want to return the product (or some other binary operator) of two fields for all records returned (e.g. return the product of `price` and `quantity` for all records)
- You want to return a complex aggregate statistic over some subset of records (e.g. return the standard deviation of the `age` field for people that use the Linux operating system)
- You want to return the output of a calculation that occurs accross records (e.g. return the euclidean distance between two records in the data set)

This is a small subset of the things you can do with the `float64` and `int64` field types. If you want to explore this functionality and the types of queries you can run, visit the documentation for [Apply()](TODO) and [Arrow()](TODO).

## Considerations
Below are some things to consider when using this consumer:
- This consumer ingests data from CSV files
- This consumer only ingest data to keyed indexes in FeatureBase.
- In order to map data between bitmap fields and `float64`/`int64` fields, the first column in the CSV file should correspond the the record keys used for records with bitmap data.
- The first line in the CSV file must define the column name (which will be used to refer to the data in queries) and the column's field type. The format 

## Usage

Let's assume I have the following data currently stored in FeatureBase (in bitmaps).

