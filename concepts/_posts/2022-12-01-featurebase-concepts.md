---
title: Conceptualizing FeatureBase
---

This overview provides a conceptual framework to understand FeatureBase products.

## FeatureBase databases

FeatureBase databases can be conceptualized in the same way as those of a traditional RDBMS:
* databases contain tables
* tables contain columns
* columns have data types and constraints
* columns contain fields
* fields contain data
* tables can be queried

There are also differences.

FeatureBase databases are in fact clusters of FeatureBase instances. These instances are also known as **node**s.

FeatureBase tables are actually Roaring Bitmap format indexes which:
* are typically denormalized
* contain fields which group rows into different categories.

FeatureBase fields can:
* map to a single field in a relational table
* represent all possible values of a matching relational field.
* have multiple values per record

### Clusters

A cluster defines:
* how clusters are replicated
* how communication is managed between nodes

### Data handling

Data is broken into shards that are:
* evenly distributed across the cluster via a consistent hash
* operated in parallel

This means any node can respond to queries.

### Shards

The number of records in a shard is governed by `ShardWidth` which:
* defaults to 2^20 (1,048,576) records
* can be modified at compile time
* cannot be modified once data is being ingested

The total number of shards allocated to handle the current records is governed by `MaxShard` which is:
* zero-indexed (e.g., if index contains six shards, MaxShard = 5)
* used to efficiently distribute queries across all nodes

Shards can be replicated (copied) to a different node in the cluster if required, using `cluster.replicas` which
* indicates the number of shard replicas in the cluster
* includes the original shard in the count
* defaults to 1 where no replicas have been made

Replica integrity is maintained by the `anti-entropy` process that compares all shard replicas on the cluster.

## Next step

* [Learn how FeatureBase handles your data](/concepts/data-handling.md)
