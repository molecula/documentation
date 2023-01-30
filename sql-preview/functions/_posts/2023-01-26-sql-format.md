---
id: sql-format
title: FORMAT
---

`Format()` function takes a format string and a list of values, and returns a string with the values formatted according to the format string.

## Syntax

```
format(str_expr, value1, value2, ...)
```

## Arguments

_str_expr_
The string that contains the format specifiers.

_value1, value2, ..._
The values that will be inserted into the format string.

## Format Specifiers
The FORMAT function supports the following format specifiers:

- `%s`: String value.
- `%d`: Integer value.
- `%f`: Floating-point value.
- `%b`: Boolean value.
- `%x`: Hexadecimal value.
- `%o`: Octal value.
- `%v`:	Value in a default format

## Return Type
`string`

## Return Value
`format()` returns the string `str_expr` with the values formatted.

## Remarks
None

## Examples
A. Format with multiple arguments.

```sql
create table segments
    (_id id, segment string, value int);

insert into segments(_id, segment, value)
    values (1,'white', 16777215);

select _id, format("%s -> #%x", segment, value) as segment from segments;
+-----+-----------------+
| _id | segment         |
+-----+-----------------+
|   1 | white -> #ffffff|
+-----+-----------------+
```

B. Format with default values and sets.
```sql
create table segments
    (_id id, time timestamp timeunit 'ms' epoch '2022-01-01T00:00:00Z', ids idset, strings stringset);

insert into segments(_id, time, ids, strings)
    values (1, '2023-01-01', [6 , 1, 9], ['red', 'blue', 'green']);

select format('id = %d , time = %v , ids = %d, strings = %s', _id, time, ids, strings) as description from segments;
+-------------------------------------------------------------------------------------------+
| description                                                                               |
+-------------------------------------------------------------------------------------------+
| id = 1 , time = 2023-01-01 00:00:00 +0000 UTC , ids = [1 6 9], strings = [blue green red] |
+-------------------------------------------------------------------------------------------+
```
