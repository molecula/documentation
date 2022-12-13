---
id: sql-substring
title: SUBSTRING
---

| | |
|-|-|
| **ℹ️NOTE** | This page contains information that only applies to SQL Preview functionality (more information [here](/sql-preview/sql-preview)). Additionally, this page represents a work in progress that is subject to frequent changes. |

---

## SUBSTRING()

`Substring()` extracts a substring from the given string, starting at the specified start index and with the specified length.

### Syntax

```
substring(expr,startIndex,length)
```

### Arguments

_expr_ 
The input string from which to extract the substring. The argument `expr` is any expression of type `string`.

_startIndex_
The starting index of the substring in the evaluated expression, starting at zero. `startIndex` can be any expression of type `int`

_length_ *(optional)* (Default: end of evaluated `expr`)
The length of the substring to extract. `length` can be any expression of type `int`. 

### Return Type
`string`

### Return Value
`substring()` returns the extracted substring
### Remarks
None
### Examples
A. Substring of the string in a column

```sql
create table segments
    (_id id, segment string);

insert into segments(_id,segment)
    values (1,'green')

select _id, substring(segment,0,3) as substr from segments;
+-----+----------+
| _id | substr   |
+-----+----------+
|   1 | gre      |
+-----+----------+
```

B. Substring of a reversed string.
```sql
create table segments
    (_id id, segment string);

insert into segments(_id,segment)
    values (1,'red')

select _id, substring(reverse(segment), 1) as substr from segments;
+-----+----------+
| _id | substr   |
+-----+----------+
|   1 | er       |
+-----+----------+
```