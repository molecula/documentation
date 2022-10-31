---
title:  CREATE TABLE
---

| | |
|-|-|
| **ℹ️NOTE** | This page contains information that only applies to SQL Preview functionality (more information [here](/sql-guide/sql-preview)). Additionally, this page represents a work in progress that is subject to frequent changes. |

---


Creates a FeatureBase table. The the table already exists and `IF NOT EXISTS` is not specified the statement will not be successful. The identifier for the table must conform to the rules of FeatureBase identifiers.

### Syntax

![expr](/img/sql/create_table_stmt.svg)

#### column_def

![expr](/img/sql/column_def.svg)

You must specify an `_id` column for `CREATE TABLE` to be successful. The type for the `_id` column can be `id` for a non-keyed table or `string` for a keyed table. No column constraints are permitted for the `_id` column.
The identifier for each column must conform to the rules of FeatureBase identifiers. Valid type names are specified in [Data Types](/sql-guide/sql-datatypes). `decimal` types require a scale to be specified.



#### type_name

![expr](/img/sql/type_name.svg)

See also [Data Types](/sql-guide/sql-datatypes).

#### column_constraint
Column constraints are optional for columns.

![expr](/img/sql/column_constraint.svg)

| **Constraint Type**                                    | **Applies to**               | **Comment**                                                                                                                                                                                                                                                          |
|--------------------------------------------------------|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TIMEQUANTUM<br>optional: TTL                               | IDSET, STRINGSET             | Input:<br>timequantum:<br>YMD ,YM,Y<br>ttl:<br>&lt;integer&gt;+ h, m, s, ms, us, ns<br>Defaults:<br>timequantum:<br>Not set by default<br>ttl:<br>0s                                                                                                                                                     |
| CACHETYPE (type and size)                              | IDSET, STRINGSET, ID, STRING | Input:<br>type:ranked, none<br>size:<br>Integer? boundary?<br>Defaults:<br>type:ranked<br>size:50000                                                                                                                                                                                        |
| MIN, MAX                                               | INT                          | Input:<br>Integer values only<br>Defaults:<br>Min Defaults to -2^63<br>Max Defaults to 2^63 - 1                                                                                                                                                                                      |
| TIMEUNIT                                               | TIMESTAMP                    | Input:<br>"s", "ms", "us", "ns" (basically go Duration)<br>Defaults:<br> "s"                                                                                                                                                                                                     |
| EPOCH                                                  | TIMESTAMP                    | Input:<br>RFC339 time stamp string<br>The epoch which timestamps should be relative to. The value may specify a timezone, for example 1980-11-30T14:20:28.000+07:00, or use zulu time (i.e. +00:00) 1980-11-30T14:20:28.000Z.<br>Defaults:<br>The Unix epoch (1970-01-01T00:00:00Z) |


#### table_options

![expr](/img/sql/table_options.svg)

| **Table Option** | **Comment**                                                           |
|------------------|-----------------------------------------------------------------------|
| KEYPARTITIONS    | integer literal; between 1-10000                                      |
| SHARDWIDTH       | integer literal; must be a power of two greater than or equal to 2^16 |


#### Example

```sql
create table allcoltypes (
	_id id,
	intcol int min 0 max 10000, 
	boolcol bool, 
	timestampcol timestamp timeunit 'ms' epoch '2022-01-01T00:00:00Z', 
	decimalcol decimal(2), 
	stringcol string cachetype ranked size 1000, 
	stringsetcol stringset cachetype lru size 1000, 
	stringsetcolq stringset cachetype lru size 1000 timequantum 'ymd' ttl '24h', 
	idcol id cachetype ranked size 1000, 
    idsetcol idset cachetype lru size 1000,
	idsetcolq idset cachetype lru size 1000 timequantum 'ymd' ttl '24h'
) keypartitions 12 shardwidth 65536
```
