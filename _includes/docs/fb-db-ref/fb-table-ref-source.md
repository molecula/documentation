## Potential sources of information

* /data-ingestion/cloud/_posts/2022-04-03-tables.md
* /reference/data-querying-ref/sql/_posts/2022-09-10-sql-alter-table.md
* /reference/data-querying-ref/sql/_posts/2022-09-10-sql-create-table.md

## Description

A FeatureBase table is analogous to a table found in a traditional RDBMS. Tables contain:

* Data
* a schema that details the structure of the data
* an optional description defined when the table is created

## Syntax


## Arguments

| Argument | Description |
|---|---|
| TableName | unique identifier that cannot be edited. |
|  | Optional description for the table to help with identification. |
| _id | Primary key that can be a unique number (positive integer) or unique string passed as a single column or concatenation of multiple columns. |


## Additional information

* Tables cannot be altered once created.
* You must create a table before you can setup FeatureBase to ingest data from an external database.
* Table names start with an alphabetic character and contain lowercase alphanumeric characters, dashes (-), and underscores (_).
* _id acts as the primary key of your table and must uniquely represent a record in your table.

## Examples


## Further information

* [Immutable objects](https://en.wikipedia.org/wiki/Immutable_object)
* [FeatureBase row reference]()
* [Roaring Bitmaps](https://roaringbitmap.org/).
