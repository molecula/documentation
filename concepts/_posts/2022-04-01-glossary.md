---
id: glossary
title: Glossary
sidebar_label: Glossary
---


### Anti-entropy
A periodic process that compares each shard and its replicas across the cluster to repair inconsistencies.

### Batch
A group of records that are pre-processed and simultaneously ingested into a FeatureBase index.

### Bitmap
The representation of a Row. Implemented with RBF (Roaring B-tree format), inspired by and evolved from the previous implementation via [Roaring Bitmaps](https://roaringbitmap.org/).

### BSI
Bit-sliced indexing is the method FeatureBase uses to represent multi-bit integers and timestamps. Integer and timestamp values are stored in int fields, and can be used for Range, Min, Max, and Sum queries.

### Cluster
A cluster consists of one or more nodes which share a cluster configuration. The cluster also defines how data is replicated and how internode communication is coordinated. FeatureBase does not have a leader node, all data is evenly distributed, and any node can respond to queries.

### Databases

Databases are clusters of FeatureBase nodes. All of your data will live in tables within FeatureBase. They are dedicated resources for your data that you can load to and query against, and like common databases, you can only join tables that exist in the same database. <!--from /cloud/cloud-databases/cloud-db-manage -->

### Fragment
A Fragment is the intersection of a field and a shard in a FeatureBase index (or a field a shard, and a particular time quantum for time type fields). Each Fragment typically corresponds to a file on disk.

### Field
Fields are used to group rows into different categories. Row IDs are namespaced by field such that the same row ID in a different field refers to a different row. For ranked fields, rows are kept in sorted order within the field. Fields are one of six types: set, int, timestamp, bool, time, and mutex.

<!-- TODO: glossary entries for each field type. section on another page detailing pros and cons of each field type and why you'd choose one over another for a particular data example. UI ingest wizard should automatically suggest an ordered list of 1-3 field types, each one having a tooltip explaining those pros and cons, and linking to that section -->

### GroupBy
A PQL query, with functionality similar to a SQL `GROUP BY` clause, that returns the count of the intersection of every combination of rows taking one row each from the specified Rows calls. GroupBy can be thought of as a multi-dimensional version of the TopN query.

### Index
An Index is a top level container in FeatureBase, roughly analogous to a table in an RDBMS, but typically more denormalized since e.g. set fields can have multiple values per record, they don't need to be represented by multiple tables.

### Max
A PQL query that returns the maximum integer value stored in an integer field or maximum timestamp stored in a timestamp field.

### MaxShard
The total number of shards allocated to handle the current set of records. This value is important for all nodes to efficiently distribute queries. MaxShard is zero-indexed, so if an index contains six shards, its MaxShard will be 5.

### Min
A PQL query that returns the minimum integer value stored in an integer field or the minimum timestamp value stored in a timestamp field.

### Mutex Field
A FeatureBase field type similar to the Set type, in which only a single value can be set at any time. Conceptually similar to an enum type, but implemented on top of Set fields, with a performance cost from the single-value constraint. Not to be confused with the mutex synchronization primitive.

### Node
An individual running instance of FeatureBase server which belongs to a cluster.

### PQL
Pilosa Query Language.

### [Protobuf](https://developers.google.com/protocol-buffers/)
Protocol Buffers is a binary serialization format which FeatureBase uses for internal messages, and can be used by clients as an alternative to JSON.

### Record
Like a row in a relational database. FeatureBase has historically used the word "row" differently, so "record" is used to avoid ambiguity.

### Replica
A copy of a shard on a different node than the original. The `cluster.replicas` configuration parameter determines how many replicas of a shard exist in the cluster. This includes the original, so a value of 1 means no extra copies are made.

### [Roaring Bitmap](https://roaringbitmap.org/)
The compressed bitmap format which inspired FeatureBase's RBF implementation of bitmaps.

### Row
Rows are the fundamental vertical data axis within FeatureBase. They are namespaced to each field within an index. Represented as a Bitmap.

### Row (Ranged)
A PQL query that returns bits based on comparison to timestamps, set according to the time quantum.

### Row (BSI)
A PQL query that returns bits based on comparison to integers stored in BSI fields.

### Row (Timestamp)
A PQL query that returns bits based on comparison to date/time stored in timestamp fields.

### Rows
A PQL query that returns a list of row IDs in the given field which have at least one bit set. The field argument is mandatory, the others are optional. Rows is the primary argument used with the GroupBy query.

### Shard
Records are sharded on a preset width. Shards are operated on in parallel and are evenly distributed across the cluster via a consistent hash.

### ShardWidth
This is the number of records in a shard. ShardWidth defaults to 2^20 or about one million. It can be modified, but only at compile time, and before ingesting any data.

### Store
A PQL query that saves the bitmap result of a query to the given row in the given field.

### Sum
A PQL query that returns the sum of integers stored in an integer field.

### Time quantum
Defines the granularity to be used for ranged Row queries on time fields.

### TTL
 TTL (Time To Live) is an field option for time fields. It holds the duration for the views created by FeatureBase based on the time quantum. Once the TTL duration exprires, those views will be deleted. Time quantum is required for TTL to function.

### TOML
the [language](https://github.com/toml-lang/toml) used for FeatureBase's configuration file.

### TopN
A PQL query that returns a list of values, sorted by the count of records with each value, within a specified field.

### View
Views separate the different data layouts within a Field. The primary view is standard, which represents the typical base data. Time based field views are automatically generated for each time quantum. Views are internally managed by FeatureBase, and never exposed directly via the API. This simplifies the functional interface by separating it from the physical data representation.
