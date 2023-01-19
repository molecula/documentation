---
id: sql-replicate
title: REPLICATE
---

`Replicate()` function splits a string into multiple substrings based on a specified separator.

## Syntax

```
replicate(expr,numoftimes)
```

## Arguments

_expr_ 
The input string to replicate. The argument `expr` is any expression of type `string`.

_numoftimes_
Number of times input string needs to be replicated. `numoftimes` can be any expression of type `int`. 

## Return Type
`string`

## Return Value
`replicate()` returns the string with input string repeated specified number of times.
## Remarks
None
## Examples
A. Replicate function on a column.

```sql
create table segments
    (_id id, segment string);

insert into segments(_id,segment)
    values (1,'green')

select _id, replicate(segment,2) as RepeatedStr from segments;
+-----+------------+
| _id | RepeatedStr|
+-----+------------+
|   1 | greengreen |
+-----+------------+
```
