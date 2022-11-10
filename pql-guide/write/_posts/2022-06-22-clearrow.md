---
id: clearrow
title: ClearRow()
sidebar_label: ClearRow()
---

The `ClearRow()` call disassociates or unassigns a value from all record in a specified field -- i.e. any record with the value `FIELD_VALUE` in `FIELD` will not have it after running `ClearRow(FIELD=FIELD_VALUE)`.

## Call Definition
```
ClearRow(FIELD=FIELD_VALUE)
```

#### Mandatory Arguments
- `FIELD` : the name of a Set, Mutex or Time field in the index being written to
- `FIELD_VALUE` : a value in FIELD -- record in the index with this value will no longer have it

#### Optional Arguments

#### Returns
- boolean:
  - true indicates that `FIELD_VALUE` was removed or disassociated with at least one record
  - false indicates that no records in the index had or were associated with `FIELD_VALUE` in `FIELD`

## Examples

### Example 1
We no longer want to store data on brand1. We'd like to remove it from the has_purchased field.

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
[customer]ClearRow(has_purchased=brand1)
```
#### Tabular Response
```
 result
--------
 true
```
#### Data Post-Query
```
 _id | age | has_purchased |    last_purchase
-----+-----+---------------+----------------------
 0   | 23  | ["brand2"]    | 2021-01-05T08:30:00Z
 1   | 31  | ["brand3"]    | 2020-09-12T12:30:00Z
 2   | 28  | ["brand3"]    | 2021-08-06T16:15:00Z
 3   | 19  | []            | null
 4   | 25  | ["brand4"]    | 2021-10-01T20:45:00Z
 5   | 40  | ["brand4"]    | 2022-01-13T11:00:00Z
```
