---
title: FeatureBase ingestion
---

## What is ingestion?



## Ingestion process

This process typically reduces your data footprint by one to two orders of magnitude.
1. Associate records with keys
2. Uncompressed data is imported from the data source
3. Data is translated to the FeatureBase roaring bitmap format
4. Data is written to the target table

## Step 1: Associate records with keys

The ingestion process requires keys to be associated with all records.

* [Learn how to identify the record ID](/concepts/example-ingest-keys)

## Step 2: Import uncompressed data from data source

Records are imported via the selected method and accumulate in a mostly uncompressed format

## Step 3: Translate data

FeatureBase requires Key IDs for all keyed rows and columns in order to compress the records. For example:
* String fields have one ID for each value present in the field
* String-keyed indexes have one ID for a row.

NOTE: FeatureBase generates an ID for any row or column that does not yet exist.

Once a specified number of records are imported, a batch is created then converted to Roaring Bitmap format.

## Step 4: Write translated data to target table


ORIGINAL CONTENT

The ingester acquires a transaction in order to ensure that no other application accesses an incompletely written index, and then copies all of the data into FeatureBase. This step is typically bottlenecked either by the network or the storage device backing the FeatureBase cluster.

## Ingestion process log

The following log messages will be recorded during an ingestion process.

| Stage | Example log message |
|---|---|
| Import |
| Translation | `2020/07/20 14:14:47 translating batch of 10 took: 10.1172ms` |
| Write | `2020/07/20 14:14:47 flushing batch of 10 to fragments took 84.2µs` |



##
