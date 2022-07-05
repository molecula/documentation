---
id: options
title: Options()
sidebar_label: Options()
---

`Options()` can be used to modify any call / query.

## Call Definition
```
Options(<CALL>, shards=[LIST_OF_SHARDS])
```

#### Mandatory Arguments
- `CALL`: Any PQL query

#### Optional Arguments
- `shards`: Run the query using only the data from the given shards. By default, the entire data set (i.e. data from all shards) is used.
  - `LIST_OF_SHARDS`: list of shards (e.g. 0, 5, 10)

#### Returns
- Same result type as `<CALL>`.

## Examples

### Example 1
Run the query `Row(f1=10)` against shards 0 and 2 only:

#### Query
```pql
Options(Row(f1=10), shards=[0, 2])
```
#### HTTP Response
```
{"columns":[100, 2097152]}
```
