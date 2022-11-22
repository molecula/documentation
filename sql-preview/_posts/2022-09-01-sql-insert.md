---
title: INSERT
---

| | |
|-|-|
| **ℹ️NOTE** | This page contains information that only applies to SQL Preview functionality (more information [here](/sql-preview/sql-preview)). Additionally, this page represents a work in progress that is subject to frequent changes. |

---


Inserts data into a FeatureBase table. Using insert you can insert multiple rows of data.

FeatureBase insert uses an update/insert semantic. If the row exists, the values in each column will be updated to the new values.

Here is an example of an insert statement:

```sql
insert into test_table (_id, column1, column2) values (1, 10, 'data10'), (2, 10, 'data10'); 
```

### Syntax

![expr](/img/sql/insert_stmt.svg)

#### column_list

![expr](/img/sql/column_list.svg)

_column_list_ is the target list of columns to be inserted into. They must be valid columns for the specified table _table_name_, and one of the columns must be the `_id` column. If no _column_list_ is specified, a column list consisting of all columns in the table is assumed.

#### value_list

![expr](/img/sql/value_list.svg)

_value_list_ is the list of expressions to be inserted. The length of the _value_list_ must match the length of the _column_list_.


