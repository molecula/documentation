---
title: part 1 - perform data mapping on source data
---

{% include /concepts/data-modeling-overview.md %}

{% include /concepts/data-mapping-summary.md%}

## Before you begin

* [Learn about data modeling](https://en.wikipedia.org/wiki/Data_modeling)
* [Establish your use case and find your data](/concepts/part1-use-case-find-data)
* [Learn about data cardinality](https://en.wikipedia.org/wiki/Cardinality_(data_modeling))

## Mapping data based on query types

| Query type | Column data | FeatureBase data type | Further information |
|---|---|---|---|
| Aggregate and range queries | Numeric with two or more decimal points | DECIMAL | [Decimal data type]() |
| Discrete values or grouping by when cardinality is low | Unsigned integers between `1` and `2^63 -1` | ID  | [ID]() |
| Aggregate queries and range queries using `<` or `>` | Integer data between `-2^63` and `2^63 -1` | INT | [INT data type]() |
| Discrete values or grouping by when cardinality is low | String, char, and varchar data | STRING | [STRING data type]() |
|  | Date and time data | TIMESTAMP | [TIMESTAMP data type]() |

## FeatureBase

Additionally, the following data types offer unique properties for FeatureBase queries:

| Query type | FeatureBase data type | Description | Further information |
|---|---|---|---|
| Simple query filtering | BOOL | Stores boolean `1` or `0` depending on the data imported. | [BOOL data type]() |

| Query type | FeatureBase data type | Description | Further information |
|---|---|---|---|
| Grouping by or searching for discrete values | IDSET | Creates an index on integer data to represent multiple values which can then be queried. | [IDSET]() |
| Grouping by or searching for discrete values | STRINGSET | Creates an index on string data to represent multiple values which can then be queried. | [STRINGSET]() |

## Next step

* [Part 2: create destination database and tables](/concepts/part2-create-db-tables)
