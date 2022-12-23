---
title: How do I delete a column from a FeatureBase Cloud table?
---
{% include /cloud/cloud-sql-alternative.md %}

You may need to delete a column if:
* the data-type is incorrect for incoming data
* the column contains incorrect data

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Learn how to create a database](/cloud/cloud-databases/cloud-db-create)
* [Create a table](/cloud/cloud-tables/cloud-table-create)
* [Create a table column](/cloud/cloud-tables/cloud-table-add-column)

## Step 1: View all tables

{% include /cloud/cloud-view-table-list.md %}

## Step 2: Delete the selected column

WARNING: Deletion is permanent.

1. Click the table name.
2. Click **Columns**.
3. {% include /cloud/icon-edit-unicode.md %} on the column > **Delete**.
5. Enter "DELETE" in the confirmation dialog.
6. Click **Delete**.

## Further information

* [Delete table column API reference](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/deletetableColumn)
