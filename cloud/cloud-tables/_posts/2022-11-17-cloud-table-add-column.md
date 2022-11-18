---
title: How do I add a column to an existing table in FeatureBase Cloud?
---

You can add a column to a FeatureBase table.

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Learn how to create a database](/cloud/cloud-databases/cloud-db-manage)
* [Learn how to create tables](/cloud/cloud-tables/cloud-table-manage)
* Table columns cannot be edited once created.

## Column data types and constraints

You can choose from the following data types and their constraints:

{% include /cloud/cloud-data-type-table.md%}

## Naming standard

{% include /concepts/column-naming-standard.md %}

## Step 1: View all tables

{% include /cloud/cloud-view-table-list.md %}

## Step 2: Add a column to a table

1. Click the table name.
2. Click **Columns**.
3. Click **Add column**.
4. Enter a name for the column
5. Choose the data type and enter values for the constraints if available.
6. Click **Add column**

## Further information

* [Create table column API reference](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/createTableColumn)
* [Learn how to drop a table column](/cloud/cloud-tables/cloud-table-drop-column)
