---
title: STRING data type
---

## Syntax

```
STRING...
```

## Arguments

| Argument | Description | Further information |
|---|---|---|
| STRING | Used for STRING, CHAR and VARCHAR data. |

## Additional information

STRING data types work best when:
* Looking for discrete values,
* `group by` where cardinality is low

If data has high cardinality:
* performance can decrease
* storage will increase
