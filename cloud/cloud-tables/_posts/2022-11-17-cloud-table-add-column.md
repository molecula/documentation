---
title: How do I add a column to an existing table in FeatureBase Cloud?
---

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Create a database](/cloud/cloud-databases/cloud-db-create)
* [Create a table](/cloud/cloud-tables/cloud-table-create)

## Column data types and constraints

{% include /cloud/cloud-data-type-table.md %}

## Naming standard

{% include /concepts/column-naming-standard.md %}

## Step 1: View all tables

{% include /cloud/cloud-view-table-list.md %}

## Step 2: Add a column to a table

NOTE: Table columns cannot be edited once created.

1. Click the table name.
2. Click **Columns** > **Add column**.
3. Enter a name for the column
4. Choose the data type and enter values for the constraints if available.
5. Click **Add column**

## Further information

* [Create table column API reference](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/createTableColumn)
* [Learn how to drop a table column](/cloud/cloud-tables/cloud-table-drop-column)