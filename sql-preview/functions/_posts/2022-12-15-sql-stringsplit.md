---
id: sql-stringsplit
title: STRINGSPLIT
---

| | |
|-|-|
| **ℹ️NOTE** | This page contains information that only applies to SQL Preview functionality (more information [here](/sql-preview/sql-preview)). Additionally, this page represents a work in progress that is subject to frequent changes. |

---

## STRINGSPLIT()

`Stringsplit()` function splits a string into multiple substrings based on a specified separator.

### Syntax

```
stringsplit(expr,seperator,position)
```

### Arguments

_expr_ 
The input string to split. The argument `expr` is any expression of type `string`.

_seperator_
A character or string that will be used to split the evaluated expression `expr`. `seperator` can be any expression of type `string`

_position_ *(optional)* (Default value : 0)
Substring to retrive from the resulting array of substrings. `position` can be any expression of type `int`. 

### Return Type
`string`

### Return Value
`stringsplit()` returns the substring at the position, from the resulting array of substrings.
### Remarks
None
### Examples
A. Split strings and return second substring

```sql
create table segments
    (_id id, segment string);

insert into segments(_id,segment)
    values (1,'red,blue,green')

select _id, stringsplit(segment,',',1) as segment from segments;
+-----+----------+
| _id | segment  |
+-----+----------+
|   1 | blue     |
+-----+----------+
```

B. Split with a column as seperator.
```sql
create table segments
    (_id id, segment string, seperator);

insert into segments(_id, segment, seperator)
    values (1,'red,blue', ',')

insert into segments(_id, segment, seperator)
    values (2,'green:yellow', ':')

select _id, stringsplit(segment, seperator, 0) as segment from segments;
+-----+----------+
| _id | segment  |
+-----+----------+
|   1 | red      |
|   2 | green    |
+-----+----------+
```