---
title: INT data type
---

Used with integers between `-2^63` and `2^63 -1`.

## Syntax

```
syntax goes here

INT [MIN | MAX]
```

## Arguments

| Argument | Description | Further information |
|---|---|---|
| INT | Used for integer data that spans a large range of values intended for aggregate queries |  |
| MIN | Minimum value constraint defaults to -2^63 |  |
| MAX | Maximum value constraint defaults to 2^63 -1 |  |

## Additional information

INT is not suitable for queries that
* group by
* look for discrete values
* include data sets with low cardinality

Instead, use the [ID data type](/sql-preview/data-typescloud-id-data-type).

## Examples
