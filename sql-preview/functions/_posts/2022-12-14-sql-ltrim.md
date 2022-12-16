---
id: sql-ltrim
tittle: LTRIM
---

`LTRIM()` function removes the leading whitespaces from input string from the selected column.

## Syntax

```
ltrim(expr)
```

## Arguments

_expr_
The argument `expr` is any expression of type `string`

## Return Type
`string`

## Return Value
`ltrim()` returns the input string after removing leading whitespaces
## Remarks
None
## Examples
Trimming strings in a column

```sql
create table segments
    (_id id, segment string);

insert into segments(_id,segment)
    values (1,'    green    ')

select _id, ltrim(segment) as TrimmedStr from segments;
+-----+------------+
| _id | TrimmedStr |
+-----+------------+
|   1 | green      |
+-----+------------+
```
