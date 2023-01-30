---
id: sql-charindex
title: CHARINDEX
---

`Charindex()` function provides the position of the substring in the given string.

## Syntax

```
charindex(substring,expr,position)
```

## Arguments

_substring_
A character or string whose position needs to be identified in the given input string.`substring` can be any expression of type `string`

_expr_ 
The input string where substring needs to be searched. The argument `expr` is any expression of type `string`.

_position_ *(optional)* (Default value : 0)
Position from where search needs to be started in the input string. `position` can be any expression of type `int`. 

## Return Type
`int`

## Return Value
`charindex()` returns the position of the substring in the input string.
## Remarks
None
## Examples
A. Char index of the substring in the string

```sql
create table segments
    (_id id, segment string);

insert into segments(_id,segment)
    values (1,'this is great')

select _id, charindex('is',segment) as charindex from segments;
+-----+----------+
| _id | charindex|
+-----+----------+
|   1 | 2        |
+-----+----------+
```
B. Identify charindex of substring in string starting from position
```sql
create table segments
    (_id id, segment string);

insert into segments(_id,segment)
    values (1,'this is great')

select _id, charindex('is',segment,3) as charindex from segments;
+-----+----------+
| _id | charindex|
+-----+----------+
|   1 | 5        |
+-----+----------+
```