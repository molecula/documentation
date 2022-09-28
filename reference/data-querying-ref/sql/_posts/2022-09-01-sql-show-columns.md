---
title: SHOW COLUMNS
---

| | |
|-|-|
| **ℹ️NOTE** | This page contains information that only applies to SQL Preview functionality (more information [here](/data-querying/sql/sql-overview)). Additionally, this page represents a work in progress that is subject to frequent changes. |

---


### Syntax

```sql
SHOW COLUMNS FROM table;
```

![expr](/img/sql/show_columns.svg)

### Returns

| **Column Name** | **Data Type** | **Description** |
|-----------------|---------------|-----------------|
| name            | string        |                 |
| type            | string        |                 |
| created_at      | timestamp     |                 |
| keys            | bool          |                 |
| cache_type      | string        |                 |
| cache_size      | int           |                 |
| scale           | int           |                 |
| min             | int           |                 |
| max             | int           |                 |
| timeunit        | string        |                 |
| epoch           | int           |                 |
| time_quantum    | string        |                 |
| ttl             | string        |                 |


