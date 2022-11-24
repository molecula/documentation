---
title: Fact and dimension data queries
---

<!--source /concepts/2022-11-24-data-modeling-overview.md -->

In a standard relational model, there are often "fact" and "dimension tables" which are split to avoid duplicating data.

FeatureBase can DO SOME BENEFIT

These use cases are provided with the following caveats:
* Database space is not at a premium
* data can be stored in the same FeatureBase table
* there is a requirement for low latency queries

## Before you begin

* [Learn about data modeling](/concepts/data-modeling-overview)
* [Learn about fact tables](https://en.wikipedia.org/wiki/Fact_table)
* [Learn about dimension tables](https://en.wikipedia.org/wiki/Dimension_(data_warehouse\)#Dimension_table)
* FeatureBase uses **Record** to identify the data in a table cell.

## Example tables

This is a simple representation of users and blog posts.

Fact table

|  | col1 | col2 | etc |
| data types |


Dimension table

DEFINITION PLUS DATA

## Query users and blog posts

Users and blog posts belong in the FACT table, and other information is found in the DIMENSIONS table.

* How many users visited a specific blog post?
* How many users visited a page within the past month?

### RDBMS approach

An RDBMS query would involve:
* joining the tables
* a more complex and time-consuming query

### FeatureBase approach

1. Merge the tables in FeatureBase
2. Create table column with the STRINGSET data type which can hold multiple values for the same data
3. Map the STRINGSET column to USER

The STRINGSET data type can then track multiple pages visited per user without additional overhead.

## Query site visits

* How many times was the blog visited?

## RDBMS approach

An RDBMS query would involve:
* joining the tables
* a more complex and time-consuming query

### FeatureBase approach

Use a "time" column data type to associate a monthly, daily or hourly timestamp with every user-page association

FeatureBase lets you query across arbitrary time ranges.
