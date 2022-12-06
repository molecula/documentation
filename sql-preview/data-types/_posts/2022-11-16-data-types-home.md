---
title: Cloud table data types and constraints
---

Data types and constraints are used to define table columns when creating tables via the Cloud UI or the API.

NOTE: For ease of use, Constraint information is included with the relevant Data type reference.

## Before you begin

* [Create a Cloud database using the UI](/cloud/cloud-databases/cloud-db-create), OR
* [Create a Cloud database using the API](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/createDatabase)

## Data types

Data types used to define the type of data that a table column can contain. They are modified by Constraints.

### Numeric data types

* [BOOL](/sql-preview/data-types/cloud-bool-data-type)
* [DECIMAL](/sql-preview/data-types/cloud-decimal-data-type)
* [INT](/sql-preview/data-types/cloud-int-data-type)
* [ID](/sql-preview/data-types/cloud-id-data-type)

### String data types

* [STRING](/sql-preview/data-types/cloud-string-data-type)

### Date/Time data types

* [TIMESTAMP](/sql-preview/data-types/cloud-timestamp-data-type)

### FeatureBase data types

* [IDSET](/sql-preview/data-types/cloud-idset-data-type)
* [STRINGSET](/sql-preview/data-types/cloud-stringset-data-type)

## Constraints

Constraints are applied to data types to modify and optimize how table data is stored and accessed.

Constraints are applied when a column is created.

| Constraint | Data type |
|---|---|
| MIN, MAX | [INT](/sql-preview/data-types/cloud-int-data-type) |
| SCALE | [DECIMAL](/sql-preview/data-types/cloud-decimal-data-type) |
| TIMEUNIT | [TIMESTAMP](/sql-preview/data-types/cloud-timestamp-data-type) |
| TIMEQUANTUM, TTL | [IDSET](/sql-preview/data-types/cloud-idset-data-type) |
| TIMEQUANTUM, TTL | [STRINGSET](/sql-preview/data-types/cloud-stringset-data-type) |

## Further information

* [Create a Cloud table](/cloud/cloud-tables/cloud-table-create)
* [Create a Cloud table using the API](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/createTable)
