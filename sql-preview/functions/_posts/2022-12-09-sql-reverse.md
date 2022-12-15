---
id: sql-reverse
title: REVERSE
---

| | |
|-|-|
| **ℹ️NOTE** | This page contains information that only applies to SQL Preview functionality (more information [here](/sql-preview/sql-preview)). Additionally, this page represents a work in progress that is subject to frequent changes. |

---

## REVERSE()

`Reverse()` function returns the reversed strings from the selected column.

### Syntax

```
reverse(expr)
```

### Arguments

_expr_
The argument `expr` is any expression of type `string`.

### Return Type
`string`

### Return Value
`reverse()` returns the reversed input string
### Remarks
None
### Examples
A. Reversing strings in a column

```sql
create table segments
    (_id id, segment string);

insert into segments(_id,segment)
    values (1,'green')

select _id, reverse(segment) as reversed from segments;
+-----+----------+
| _id | reversed |
+-----+----------+
|   1 | neerg    |
+-----+----------+
```

B. Testing nested reverse function
```sql
create table segments
    (_id id, segment string);

insert into segments(_id,segment)
    values (1,'red')

select _id, reverse(reverse(segment)) as segment from segments;
+-----+----------+
| _id | reversed |
+-----+----------+
|   1 | red      |
+-----+----------+
```