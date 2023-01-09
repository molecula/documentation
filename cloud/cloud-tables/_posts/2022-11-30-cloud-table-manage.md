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

* [Learn about data types and constraints](/cloud/cloud-data-modeling/data-types)

## Naming standard

{% include /cloud/object-naming-standard.md%}
{% include /cloud/cloud-table-naming-standard.md %}
{% include /cloud/cloud-column-naming-standard.md%}

## Managing tables in FeatureBase Cloud

* Create table
    * [UI](/cloud/cloud-tables/cloud-table-create)
    * [SQL](/sql-preview/sql-create-table)
* Add table columns
    * [UI](/cloud/cloud-tables/cloud-table-add-column)
    * [SQL](/sql-preview/sql-alter-table#add_column)
* Drop table columns
    * [UI](/cloud/cloud-tables/cloud-table-delete-column)
    * [SQL](/sql-preview/sql-alter-table#drop_column)
* Drop table
    * [UI](/cloud/cloud-tables/cloud-table-drop)
    * [SQL](/sql-preview/sql-alter-table#drop_column)

<!--
DROP TABLE SQL PAGE NEEDS TO BE CREATED AND REPLACED ABOVE
-->

## Managing tables using the Cloud API

* [Table API reference](https://api-docs-featurebase-cloud.redoc.ly/v2#tag/Tables)

## Joining tables

Tables that exist in the same database can be joined.

## Next step

* [Learn about setting up data ingestion](/cloud/cloud-data-ingestion/ingest-data-overview)
