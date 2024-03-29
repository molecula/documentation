---
title: Tutorial - Ingest a CSV with BULK INSERT
---

## Before you begin
{% include /sql-preview/before_ingest.md %}

[Learn about the age dataset](https://www.kaggle.com/datasets/imoore/age-dataset?resource=download)

## Step 1: create table

```sql
CREATE TABLE age (
    _id STRING,
    name STRING,
    description STRING,
    gender STRING,
    country STRING,
    occupation STRING,
    birth_year INT min -32767 max 32767,
    death_year INT min -32767 max 32767,
    death_manner STRING,
    birth_age INT min -32767 max 32767
);
```

## Step 2: ingest data

```sql
BULK INSERT
INTO age (_id, name, description, gender, country, occupation,
    birth_year, death_year, death_manner, birth_age )
MAP(0 STRING,
1 STRING,
2 STRING,
3 STRING,
4 STRING,
5 STRING,
6 INT,
7 INT,
8 STRING,
9 INT )
FROM
    'https://featurebase-public-data.s3.us-east-2.amazonaws.com/age.csv'
WITH
    BATCHSIZE 100000
    FORMAT 'CSV'
    INPUT 'URL'
    HEADER_ROW;
```

## Step 3: query the data

```sql
SELECT COUNT(*) FROM age;
```
```sql
SELECT TOP(10) * FROM age;
```

## Further information

* [Bulk Insert](/sql-preview/sql-bulk-insert)
