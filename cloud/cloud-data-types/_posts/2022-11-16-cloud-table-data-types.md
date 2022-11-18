---
title: Cloud table data types and constraints
---

Data types and constraints are used to define table columns when creating tables via the Cloud UI or the API.

NOTE: For ease of use, Constraint information is included with the relevant Data type reference.

## Before you begin

* [Create a Cloud database using the UI](/cloud/cloud-databases/cloud-db-create)
* [Create a Cloud database using the API](/cloud/cloud-databases/db-api/cloud-db-create-api)

## Data types

Data types used to define the type of data that a table column can contain. They are modified by Constraints.

### Numeric data types

* [DECIMAL](/cloud/cloud-data-types/cloud-decimal-data-type)
* [INT](/cloud/cloud-data-types/cloud-int-data-type)
* [ID](/cloud/cloud-data-types/cloud-id-data-type)

### String data types

* [STRING](/cloud/cloud-data-types/cloud-string-data-type)

### Date/Time data types

* [TIMESTAMP](/cloud/cloud-data-types/cloud-timestamp-data-type)

### FeatureBase data types

* [IDSET](/cloud/cloud-data-types/cloud-idset-data-type)
* [STRINGSET](/cloud/cloud-data-types/cloud-stringset-data-type)

## Constraints

Constraints are applied to data types to modify and optimize how table data is stored and accessed.

Constraints are applied when a column is created.

| Constraint | Data type |
|---|---|
| MIN, MAX | [INT](/cloud/cloud-data-types/cloud-int-data-type) |
| SCALE | [DECIMAL](/cloud/cloud-data-types/cloud-decimal-data-type) |
| TIMEUNIT | [TIMESTAMP](/cloud/cloud-data-types/cloud-timestamp-data-type) |
| TIMEQUANTUM, TTL | [IDSET](/cloud/cloud-data-types/cloud-idset-data-type) |
| TIMEQUANTUM, TTL | [STRINGSET](/cloud/cloud-data-types/cloud-stringset-data-type) |

## Further information

* [Create a Cloud table](/cloud/cloud-tables/cloud-table-create)
* [Create a Cloud table using the API](/cloud/cloud-databases/db-api/cloud-table-create-api)
