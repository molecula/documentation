---
title: Data types and constraints
---

Data types and constraints are used to define table columns when creating tables via SQL.

NOTE: For ease of use, Constraint information is included with the relevant Data type reference.

## Before you begin

* [Create a Cloud database using the UI](/cloud/cloud-databases/cloud-db-create), OR
* [Create a Cloud database using the API](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/createDatabase)

## Data types

Data types used to define the type of data that a table column can contain. They are modified by Constraints.

### Mapping data types

| SQL Data Type | FeatureBase Data Type |
|---------------|---|
| int | int |
| bool | bool |
| timestamp | timestamp |
| decimal | decimal |
| string | keyed mutex |
| stringset | keyed set |
| id | mutex |
| idset | set |

### Numeric data types

* [BOOL](/sql-preview/data-types/data-type-bool)
* [DECIMAL](/sql-preview/data-types/data-type-decimal)
* [ID](/sql-preview/data-types/data-type-id)
* [INT](/sql-preview/data-types/data-type-int)

### String data types

* [STRING](/sql-preview/data-types/data-type-string)

### Date/Time data types

* [TIMESTAMP](/sql-preview/data-types/data-type-timestamp)

### FeatureBase data types

* [IDSET](/sql-preview/data-types/data-type-idset)
* [STRINGSET](/sql-preview/data-types/data-type-stringset)

## Constraints

Constraints are applied to data types to modify and optimize how table data is stored and accessed.

Constraints are applied when a column is created.

| Constraint | Data type |
|---|---|
| EPOCH | [TIMESTAMP](/sql-preview/data-types/data-type-timestamp)
| MIN, MAX | [INT](/sql-preview/data-types/data-type-int) |
| SCALE | [DECIMAL](/sql-preview/data-types/data-type-decimal) |
| TIMEQUANTUM, TTL | [IDSET](/sql-preview/data-types/data-type-idset)<br/> [STRINGSET](/sql-preview/data-types/data-type-stringset) |
| TIMEUNIT | [TIMESTAMP](/sql-preview/data-types/data-type-timestamp) |

<!--
removed from functionality but keeping in a comment if later available:
| Cachetype | [ID](/sql-preview/data-types/data-type-id)<br/> [STRING](/sql-preview/data-types/data-type-string)<br/> [IDSET](/sql-preview/data-types/data-type-idset)<br/> [STRINGSET](/sql-preview/data-types/data-type-stringset) |
-->

## Further information

* [Create a Cloud table](/cloud/cloud-tables/cloud-table-create)
* [Create a Cloud table using the API](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/createTable)
