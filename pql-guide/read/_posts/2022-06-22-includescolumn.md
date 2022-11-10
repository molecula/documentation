---
id: includescolumn
title: IncludesColumn()
sidebar_label: IncludesColumn()
---

`IncludesColumn()` returns true if some record ID / record key is in a specified set of record IDs / record keys - i.e. if the specified record was returned by a specified [row call](/pql-guide/pql-introduction#row-calls){:target="_blank"} or not.

## Call Definition

```
IncludesColumn(ROW_CALL, column=UINT_OR_STRING)
```
#### Mandatory Arguments
 - `ROW_CALL`: the [row call](/pql-guide/pql-introduction#row-calls){:target="_blank"} to compare against
 - `column`: the record ID or record key we want to check is in or not in the result of `ROW_CALL`
   - `UINT_OR_STRING`: unsigned integer for non keyed records or a string for keyed records

#### Optional Arguments

#### Returns
- a boolean: true if UINT_OR_STRING is in the set of record IDs / keys returned by `ROW_CALL` -- false otherwise.


## Examples

### Data:
```
Index: customer (non keyed index)

 _id | age (Int) | has_purchased (Set) | last_purchase (Timestamp)
-----+-----------+---------------------+---------------------------
 0   |    23     | ["brand1","brand2"] | 2021-01-05T08:30:00Z
 1   |    31     | ["brand1","brand3"] | 2020-09-12T12:30:00Z
 2   |    28     | ["brand1","brand3"] | 2021-08-06T16:15:00Z
 3   |    19     | []                  | null
 4   |    25     | ["brand1","brand4"] | 2021-10-01T20:45:00Z
 5   |    40     | ["brand4"]          | 2022-01-13T11:00:00Z
```

-----------------------------------------------------------------------
### Example 1
Question: Has the customer with ID 0 bought from brand1?

#### Query
```
[customer]IncludesColumn(
  Row(has_purchased = brand1),
  column = 0
)
```
#### Tabular Response
```
 result
--------
 true
```
#### HTTP Response
```json
{
  "results": [
    true
  ]
}
```

#### Explanation
`Row(has_purchased = brand1)` returns `[0,1,2,4]`. `IncludesColumn()` returns true because the record with ID 0 is in that set.
