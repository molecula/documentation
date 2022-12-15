---
id: sql-replaceall
title: REPLACEALL
---

`ReplaceAll()` function replaces all occurrences of the expression `exprOld` in the evaluated expression `expr` with a new expression `exprNew`.

## Syntax

```
replaceall(expr,exprOld,exprNew)
```

## Arguments

_expr_ 
The evaluated expression in which all occurrences of `exprOld` should be replaced with `exprNew`. `expr` can be any expression of type `string`

_exprOld_
The substring that should be replaced. `exprOld` can be any expression of type `string`

_exprNew_ 
The substring that should be used as a replacement for `exprOld`. `exprNew` can be any expression of type `string`

## Return Type
`string`

## Return Value
`replaceall()` returns a string that is the result of replacing all occurrences of `exprOld` in `expr` with `exprNew`.
## Remarks
None
## Examples
A. Replacing all the occurances

```sql
create table segments
    (_id id, segment string);

insert into segments(_id,segment)
    values (1,'hello world!')

select _id, segment ,replaceall(segment, 'world','universe') as replaced from segments;
+-----+--------------+-----------------+
| _id | segment      | replaced        |
+-----+--------------+-----------------+
|   1 | hello world! | hello universe! |
+-----+--------------+-----------------+
```

B. Replace all with reversed string.
```sql
create table segments
    (_id id, segment string, rev string);

insert into segments(_id,segment)
    values (1,'tic tac', 'cot')

select _id, segment, replaceall(segment, 'tac', reverse(rev)) as replaced from segments;
+-----+--------------+-----------------+
| _id | segment      | replaced        |
+-----+--------------+-----------------+
|   1 | tic tac      | tic toc         |
+-----+--------------+-----------------+
```
