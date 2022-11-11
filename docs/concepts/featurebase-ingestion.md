---
title: Learn about importing data to FeatureBase
---

This page provides a high-level overview of importing data to FeatureBase

## Before you begin

* [Learn how FeatureBase databases work](/docs/concepts/featurebase-databases)

## Ingestion vs Import

FeatureBase uses the term **ingestion** to describe the three-step process that imports data to the FeatureBase database cluster.

### Step 1: collect

Collection is a batch process performed when a specified number of records are accumulated in an uncompressed format from the data-source.

Using large batches reduces the processing overhead.

### Step 2: translate

Translation involves compressing and translating data to the Roaring Bitmap format that FeatureBase uses.

The system collects **Key IDs** for keyed rows and columns, for example:

* String fields have one ID for each string value present in the field
* String-keyed indexes have one ID for each row.

NOTE: FeatureBase generates an ID if the specified row/column did not previously exist.

Once all IDs are mapped, the batch is converted into the Roaring Bitmap format

### Step 3: copy

In the final part of the process, the ingestion system:
* obtains a transaction to prevent other applications accessing the incompletely written index
* copies the batched data to FeatureBase.

The copy speed can be affected by
* network processes between the cluster and the data source
* the destination storage device where the FeatureBase cluster is saved

## Further information



## Get support

{% include /docs/get-support-source.md %}

## SOURCES (DELETE WHEN READY)
* https://docs.featurebase.com/data-ingestion/enterprise/ingesters
* https://docs.featurebase.com/reference/data-ingestion/ingester-configuration
