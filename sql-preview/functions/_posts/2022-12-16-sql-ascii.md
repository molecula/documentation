---
id: sql-ascii
title: ASCII
---

`Ascii()` function returns the ASCII code value of the string expression.

## Syntax

```
ascii(str_expr)
```

## Arguments

_str_expr_
A string expression of length 1. 
 

## Return Type
`int`

## Return Value
`ascii()` returns the ASCII code value of the string expression `str_expr`. 

## Remarks
None

## Examples
A. ASCII function on a column.

```sql
create table segments
    (_id id, segment string);

insert into segments(_id, segment)
    values (1,'r')

select _id, ascii(segment) as segment from segments;
+-----+----------+
| _id | segment  |
+-----+----------+
|   1 | 114      |
+-----+----------+
```
