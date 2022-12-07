---
title: How do I create a table in FeatureBase Cloud?
---

{% include /concepts/create-table-summary.md %}

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Learn how to create a database](/cloud/cloud-databases/cloud-db-create)
* [Learn how to manage tables](/cloud/cloud-tables/cloud-table-manage)

## Naming standards

{% include /cloud/object-naming-standard.md%}
{% include /cloud/cloud-table-naming-standard.md %}

## Method 1: SQL

### Step 1: view query page

1. Click Query
2. Choose a database
    1. You can redirect any query to a particular database by aliasing/prepending it with “{<database name>}”.

### Step 2: Build DDL query

* [Learn how to create tables with SQL](/sql-preview/sql-create-table)

### Step 3: Run DDL query

1. Enter the query.
2. Click **Run** or run with key combination of “Ctrl + Enter" or Cmd + Enter".

## Method 2: Point & Click

### Step 1: view tables

{% include /cloud/cloud-view-table-list.md %}

### Step 2: create table

1. Click **Create table**.
2. Select the destination database.
3. Enter a table name and an optional description.

### Step 3: choose the primary key

{% include /cloud/cloud-pk-table.md %}

1. Select the ID type.
2. Click **Create**.

## Next step

* [Learn how to add columns to a table](/cloud/cloud-tables/cloud-table-add-column)
* [Learn how to create tables with SQL](/sql-preview/sql-create-table)

## Further information

* [Create table API reference](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/createTable)
