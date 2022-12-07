---
title: SHOW CREATE TABLE
---

| | |
|-|-|
| **ℹ️NOTE** | This page contains information that only applies to SQL Preview functionality (more information [here](/sql-preview/sql-preview)). Additionally, this page represents a work in progress that is subject to frequent changes. |

---


Shows the data definition language (DDL) statement for a FeatureBase table.

### Syntax

```sql
SHOW CREATE TABLE table_name;
```

![expr](/img/sql/show_create_table.svg)

### Returns

| **Column Name** | **Data Type** | **Description**   |
|-----------------|---------------|-------------------|
| ddl             | string        | DDL of the table  |


