---
title: SHOW TABLES
---

| | |
|-|-|
| **ℹ️NOTE** | This page contains information that only applies to SQL Preview functionality (more information [here](/sql-guide/sql-preview)). Additionally, this page represents a work in progress that is subject to frequent changes. |

---


Shows the list of FeatureBase tables that exist on the server.

### Syntax

```sql
SHOW TABLES;
```

![expr](/img/sql/show_tables.svg)

### Returns

| **Column Name** | **Data Type** | **Description**   |
|-----------------|---------------|-------------------|
| name            | string        | Name of the table |
| created_at      | timestamp     |                   |
| track_existence | bool          |                   |
| keys            | bool          |                   |
| shard_width     | int           |                   |


