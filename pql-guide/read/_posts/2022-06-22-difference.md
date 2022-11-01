---
id: difference
title: Difference()
sidebar_label: Difference()
---

The `Difference()` query performs a set difference on the [row calls](/pql-guide/pql#row-calls){:target="_blank"} passed as arguments. It returns the set of record IDs / keys in the first [row call](/pql-guide/pql#row-calls){:target="_blank"} and not in any of the subsequent [row calls](/pql-guide/pql#row-calls){:target="_blank"}. 

`Difference()` is a [row call](/pql-guide/pql#row-calls){:target="_blank"}.

## Call Definition

```pql
Difference(ROW_CALL, ...)
```

#### Mandatory Arguments
- `ROW_CALL` : a [row call](/pql-guide/pql#row-calls){:target="_blank"} to difference

#### Optional Arguments
- `...` : Any number of additional [row calls](/pql-guide/pql#row-calls){:target="_blank"} seperated by commas

#### Returns
- list of record IDs or record keys

## Examples
### Data
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
Which users have purchased from brand1 and not brand3?
#### Query
```
[customer]Difference(
  Row(has_purchased = brand1), 
  Row(has_purchased = brand3)
)
```
#### Tabular Response
```
 _id
-----
 0
 4
```
#### HTTP Response
```json
{
  "results": [
    {
      "columns": [
        0,
        4
      ]
    }
  ]
}
```
#### Explanation
`Row(has_purchased = brand1)` returns `[0,1,2,4]` and `Row(has_purchased = brand3)` returns `[1,2]`. The set difference of these two sets is `[0,4]`. These are the customers have bought brand1 and not brand3.

-----------------------------------------------------------------------
### Example 2
Which users have purchased from brand3 and not brand1?
#### Query
```
[customer]Difference(
  Row(has_purchased = brand3),
  Row(has_purchased = brand1)
)
```
#### Tabular Response
```
 _id
-----
```
#### HTTP Response
```json
{
  "results": [
    {
      "columns": []
    }
  ]
}
```
#### Explanation
`Row(has_purchased = brand3)` returns `[1,2]` and `Row(has_purchased = brand1)` returns `[0,1,2,4]`. The set difference of these two sets is `[]`. There are no customers that bought brand3 and not brand1

-----------------------------------------------------------------------
### Example 3
Which customers have purchased from brand1 and not brand2 and not brand4?

#### Query
```
[customer]Difference(
  Row(has_purchased = brand1),
  Row(has_purchased = brand2),
  Row(has_purchased = brand4)
)
```

#### Tabular Response
```
 _id
-----
 1
 2
```

```json
{
  "results": [
    {
      "columns": [
        1,
        2
      ]
    }
  ]
}
```
#### Explanation
`Row(has_purchased = brand1)` returns `[0,1,2,4]`, `Row(has_purchased = brand2)` returns `[0]`, and `Row(has_purchased = brand4)` returns `[4]`. The the difference of these three sets is `[1,2]` - the only customer who has purchased brand1 but not brand2 or brand4.
