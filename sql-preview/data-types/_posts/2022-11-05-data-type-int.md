---
title: INT data type
---

Int is a numeric datatype used with the `min` and `max` constraints.

## Syntax

```
INT MIN [MIN VALUE] MAX [MAX VALUE]
```

## Arguments

| Argument | Description |
|---|---|
| INT | Used for integer data that spans a large range of values intended for aggregate queries |
| MIN | Minimum value constraint defaults to -2^63 |
| MAX | Maximum value constraint defaults to 2^63 -1 |

## Additional information

INT is not suitable for queries that
* group by
* include data sets with low cardinality

Instead, use the [ID data type](/sql-preview/data-types/data-type-id).
