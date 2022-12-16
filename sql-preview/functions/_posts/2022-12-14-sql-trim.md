---
id: sql-trim
title: TRIM
---

`TRIM()` function removes the leading and trailing whitespaces from input string from the selected column.

## Syntax

```
trim(expr)
```

## Arguments

_expr_
The argument `expr` is any expression of type `string`

## Return Type
`string`

## Return Value
`trim()` returns the input string after removing leading and trailing whitespaces
## Remarks
None
## Examples
Trimming strings in a column

```sql
create table segments
    (_id id, segment string);

insert into segments(_id,segment)
    values (1,' green ')

select _id, trim(segment) as TrimmedStr from segments;
+-----+------------+
| _id | TrimmedStr |
+-----+------------+
|   1 | green      |
+-----+------------+
```
