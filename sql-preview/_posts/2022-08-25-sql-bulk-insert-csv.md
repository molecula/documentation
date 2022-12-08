---
title: How do I Bulk Insert A CSV File?
---

## Before you begin
{% include /sql-preview/before_ingest.md %}

## Step 0: learn about the data

1. Learn a little bit about the [age dataset](https://www.kaggle.com/datasets/imoore/age-dataset?resource=download)

## Step 2: create table

```sql
CREATE TABLE age (
    _id STRING,
    name STRING cachetype ranked size 1000,
    description STRING cachetype ranked size 1000,
    gender STRING cachetype ranked size 1000,
    country STRING cachetype ranked size 1000,
    occupation STRING cachetype ranked size 1000,
    birth_year INT min -32767 max 32767,
    death_year INT min -32767 max 32767,
    death_manner STRING cachetype ranked size 1000,
    birth_age INT min -32767 max 32767
) keypartitions 12 shardwidth 65536;
```

## Step 3: ingest data

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

## Step 4: query the data

```sql
SELECT COUNT(*) FROM age;
```
```sql
SELECT TOP(10) * FROM age;
```

## Further information

* [Bulk Insert](/sql-preview/sql-bulk-insert)