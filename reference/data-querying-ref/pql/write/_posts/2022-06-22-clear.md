---
id: clear
title: Clear()
sidebar_label: Clear()
---

The `Clear()` call disassociates or unassigns a value from a record in a specified field. 

For Set, Mutex, and Time fields, you can disassociate one value from one record at a time.

For Int, Decimal, and Timestamp fields, you can set the value for a given record to null by using any value for `FIELD_VALUE` -- see example 2 below.

## Call Definition
```
Clear(UINT_OR_STRING, FIELD=FIELD_VALUE)
```

#### Mandatory Arguments
- `UINT_OR_STRING`: the record we'd like to operate on -- UNIT or unsigned integer for non-keyed indexes and string for keyed indexes.
- `FIELD` : the name of the field that contains the value we want to disassociate with the record
- `FIELD_VALUE` : the value we want to disassociate with the record - use the value of `null` for Int, Decimal, and Timestamp fields if you want to clear a value - i.e. set the value to *null*.

#### Optional Arguments

#### Returns
- boolean
  - true indicates the write was successful
  - false indicates the write was unsuccessful or nothing changed

## Examples

### Example 1
Customer 5 as decided they don't want the company to store their purchase data - remove it with `Clear()`.

#### Data Pre-Query
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

#### Query
```
[customer]Clear(5, has_purchased=brand4)
```
#### Tabular Response
```
 result
--------
 true
```
#### Data Post-Query
```
 _id | age |    has_purchased    |    last_purchase
-----+-----+---------------------+----------------------
 0   | 23  | ["brand1","brand2"] | 2021-01-05T08:30:00Z
 1   | 31  | ["brand1","brand3"] | 2020-09-12T12:30:00Z
 2   | 28  | ["brand1","brand3"] | 2021-08-06T16:15:00Z
 3   | 19  | []                  | null
 4   | 25  | ["brand1","brand4"] | 2021-10-01T20:45:00Z
 5   | 40  | []                  | 2022-01-13T11:00:00Z
```
<hr>

### Example 2
Customer 5 also doesn't want the company to store their `last_purchase` data - remove it with `Clear()`.

#### Data Pre-Query
```
 _id | age |    has_purchased    |    last_purchase
-----+-----+---------------------+----------------------
 0   | 23  | ["brand1","brand2"] | 2021-01-05T08:30:00Z
 1   | 31  | ["brand1","brand3"] | 2020-09-12T12:30:00Z
 2   | 28  | ["brand1","brand3"] | 2021-08-06T16:15:00Z
 3   | 19  | []                  | null
 4   | 25  | ["brand1","brand4"] | 2021-10-01T20:45:00Z
 5   | 40  | []                  | 2022-01-13T11:00:00Z
```

#### Query
```
[customer]Clear(5, last_purchase=null)
```

#### Tabular Response
```
 result
--------
 true
```

#### Data Post-Query 
```
 _id | age |    has_purchased    |    last_purchase
-----+-----+---------------------+----------------------
 0   | 23  | ["brand1","brand2"] | 2021-01-05T08:30:00Z
 1   | 31  | ["brand1","brand3"] | 2020-09-12T12:30:00Z
 2   | 28  | ["brand1","brand3"] | 2021-08-06T16:15:00Z
 3   | 19  | []                  | null
 4   | 25  | ["brand1","brand4"] | 2021-10-01T20:45:00Z
 5   | 40  | []                  | null
```
