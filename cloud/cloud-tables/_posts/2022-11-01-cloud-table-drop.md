---
title: How do I drop a table in FeatureBase Cloud?
---
{% include /cloud/cloud-sql-alternative.md %}

There are a number of reasons why you may choose to drop a table, including:
* incorrect configuration
* incorrect name
* database deletion
* data deletion

## Warnings

* Tables cannot be recovered once deleted
* Deleting tables will affect data-sources and running queries

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Create a database](/cloud/cloud-databases/cloud-db-create)
* [Create a table](/cloud/cloud-tables/cloud-table-create)

## Step 1: View table list

{% include /cloud/cloud-view-table-list.md %}

## Step 2: Drop the selected table

1. {% include /cloud-icons/icon-edit-unicode.md %} > **Drop table**
2. Enter "DELETE" in the confirmation dialog.
3. Click **Drop table**.

## Further information

* [Delete table API reference](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/deletetable)
* [Learn how to create tables](/cloud/cloud-tables/cloud-table-create)
