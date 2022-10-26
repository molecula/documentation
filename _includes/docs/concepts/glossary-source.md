
## A

| Term | Description |
|---|---|
| Anti-entropy | See [Featurebase anti-entropy process reference](/fb-db-ref/shard-anti-entropy-ref.md) |
| Batch ingestion | See [How to import data](/concepts/how-to-import-data.md) |
| Featurebase Bitmap | See [FeatureBase bitmap/row reference](/fb-db-ref/fb-bitmap-row-ref.md) |
| Bit Sliced Indexing (BSI) | See [Featurebase BSI reference](/fb-db-ref/fb-bsi-ref.md)

## C

| Term | Description |
|---|---|
| FeatureBase Cluster | See [FeatureBase cluster reference](/fb-db-ref/fb-cluster-ref.md)

## F-G-H-I

| Term | Description |
|---|---|
| Fact table | Each record in a fact table typically represents an immutable event (e.g. someone clicked a link or made a purchase, a temperature reading was recorded, etc). See [Learn about Fact tables](https://en.wikipedia.org/wiki/Fact_table) |
| Fragment | See [Featurebase Fragment reference](/fb-db-ref/fb-fragment-ref.md)
| FeatureBase Field | See [FeatureBase Field reference](/fb-db-ref/fb-field-ref.md)
| PQL GroupBy | See [PQL Groupby reference](pql-groupby-ref.md)
| Index | See [Featurebase Index reference](/fb-db-ref/fb-index-ref.md) |

## M

| PQL Max | See [PQL Max reference](/pql/pql-max-ref.md)
| MaxShard | See [Shard MaxShard reference](/fb-db-ref/shard-maxshard-ref.md) |
| PQL Min | See [PQL Min ref](/pql/pql-min-ref.md) |
| Mutex field | See [Mutex field reference](/fb-db-ref/mutex-field-ref.md) |

## N

| Term | Description |
|---|---|
| Node | An individual running instance of FeatureBase server which belongs to a cluster.

## P

| Term | Description |
|---|---|
| Pilosa Query Language (PQL) | Implementation of SQL unique to FeatureBase and named after an earlier iteration of the product. |
| [Protobuf](https://developers.google.com/protocol-buffers/) | Protocol Buffers is a binary serialization format which FeatureBase uses for internal messages, and can be used by clients as an alternative to JSON. |

## R

| Term | Description |
|---|---|
| Record | FeatureBase uses "Record" to represent the traditional concept of a database row. |
| Replica | See [Shard Replica reference](/fb-db/shard-replica-ref.md)
| Roaring Bitmap | See See [FeatureBase bitmap/row reference](/fb-db-ref/fb-bitmap-row-ref.md) |
| Row | See [FeatureBase bitmap/row reference](/fb-db-ref/fb-bitmap-row-ref.md) |
| Row (BSI) | See [PQL Row bsi](/pql/pql-row-bsi-ref.md) |
| Row (Ranged) | See [PQL Row ranged](/pql/pql-row-ranged-ref.md) |
| Row (Timestamp) | See [PQL Row bsi](/pql/pql-row-bsi-ref.md) |
| Rows | See [PQL Row bsi](/pql/pql-rows-ref.md) |

## S

| Term | Description |
|---|---|
| Shard | Records are sharded on a preset width. Shards are operated on in parallel and are evenly distributed across the cluster via a consistent hash. |
| ShardWidth | This is the number of records in a shard. ShardWidth defaults to 2^20 or about one million. It can be modified, but only at compile time, and before ingesting any data. |
| Store | A PQL query that saves the bitmap result of a query to the given row in the given field. |
| Sum | A PQL query that returns the sum of integers stored in an integer field. |

## T

| Term | Description |
|---|---|
| Time quantum | See [FeatureBase Time Quantum reference](/fb-db-ref/fb-row-ranged-time-quantum-ref.md )|
| TTL | See [Time To Live](/concepts/time-to-live.md) |
| TOML | The [TOML language](https://github.com/toml-lang/toml) is used for FeatureBase's configuration file. |
| TopN | See [TopN PQL Query](/pql-topn.md) |

## V

| Term | Description |
|---|---|
| View | See [FeatureBase Field Views reference](/fb-db-ref/fb-field-views-ref.md) |
