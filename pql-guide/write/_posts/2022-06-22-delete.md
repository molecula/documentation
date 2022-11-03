---
id: delete
title: Delete()
sidebar_label: Delete()
---

The `Delete()` call removes entire records. A [row call](/pql-guide/pql-introduction#row-calls){:target="_blank"} is used to determine which records will be deleted.

It is potentially a very heavy operation. It iterates over all fields and views in a set of records, removing the records. It also removes  all data from fields, existence bits, and key translation for the provided columns for all replicas in the cluster.

`Delete()` does not support deleting specific fields, only full records based on `ROW_CALL`. It doesn’t support deletes from Kafka Delete Consumer or two separate clusters.

Note: while you could delete all records in an index using `Delete(All())`, this is not recommended, as [dropping an index](/community/community-api/grpc-api#deleteindex) would be a much more performant way of deleting all records in an index.

## Call Definition
```
Delete(ROW_CALL)
```

#### Mandatory Arguments
- `ROW_CALL` : the [row call](/pql-guide/pql-introduction#row-calls){:target="_blank"} used to determine which records to delete -- i.e. records returned by `ROW_CALL` will be deleted.

#### Optional Arguments

#### Returns
 - boolean
    - true indicates that the columns to delete were found AND deleted.
    - false indicates that the columns to delete were NOT found OR that they WERE found but not deleted.

## Examples

### Example 1
Delete customers who's last purchase was before 2021.

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
[customer]Delete(Row(last_purchase < "2021-01-01T00:00:00Z"))
```
#### Tabular Response
```
 result
--------
 true
```
#### Data Post-Query
```
 _id | age (Int) | has_purchased (Set) | last_purchase (Timestamp)
-----+-----------+---------------------+---------------------------
 0   |    23     | ["brand1","brand2"] | 2021-01-05T08:30:00Z
 2   |    28     | ["brand1","brand3"] | 2021-08-06T16:15:00Z
 3   |    19     | []                  | null
 4   |    25     | ["brand1","brand4"] | 2021-10-01T20:45:00Z
 5   |    40     | ["brand4"]          | 2022-01-13T11:00:00Z
```
