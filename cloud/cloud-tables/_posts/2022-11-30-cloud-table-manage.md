---
title: How do I manage tables in FeatureBase Cloud?
---

This page provides an overview of FeatureBase tables and links to guide you through creating, altering and dropping tables.

{% include /concepts/create-table-summary.md %}

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Learn how to manage Cloud databases](/cloud/cloud-databases/cloud-db-manage)

## Data modeling

{% include /concepts/data-modeling-overview.md %}

IMPORTANT: Perform data modeling **before** creating tables to avoid issues.

* [Learn about data modeling](/concepts/data-modeling-overview)

## Table primary key

{% include /cloud/cloud-pk-table.md %}

## Column data types and constraints

* [Learn about data types and constraints](/sql-preview/data-types/data-types-home)

## Naming standard

{% include /cloud/object-naming-standard.md%}
{% include /cloud/cloud-table-naming-standard.md %}
{% include /cloud/cloud-column-naming-standard.md%}

## Manage tables

Manage tables with FeatureBase Cloud
* [Create a table](/cloud/cloud-tables/cloud-table-create)
* [Delete a table](/cloud/cloud-tables/cloud-table-drop)

Manage tables with SQL statements
* [CREATE TABLE statement](/sql-preview/sql-create-table)
* [DROP TABLE statement](/sql-preview/sql-drop-table)

## Manage table columns

Manage table columns with FeatureBase Cloud
* [Add table column](/cloud/cloud-tables/cloud-table-add-column)
* [Delete table column](/cloud/cloud-tables/cloud-table-delete-column)

Manage table columns with the ALTER TABLE statement
* [ALTER TABLE statement with ADD COLUMN argument](/sql-preview/sql-alter-table#add_column)
* [ALTER TABLE statement with DROP COLUMN argument](/sql-preview/sql-alter-table#drop_column)

## Next step

* [Learn about setting up data ingestion](/cloud/cloud-data-ingestion/ingest-data-overview)

## Further information

Additional SQL statements are available for use:
* [SHOW TABLES statement](/sql-preview/sql-show-tables)
* [SHOW COLUMNS statement](/sql-preview/sql-show-columns)
* [SHOW CREATE TABLE statement](/sql-preview/sql-show-create-table)
