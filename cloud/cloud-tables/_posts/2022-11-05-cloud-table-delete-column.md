---
title: How do I delete a column from a FeatureBase Cloud table?
---

You may need to delete a column if:
* the data-type is incorrect for incoming data
* the column contains incorrect data

{% include /cloud/cloud-table-create-sql.md %}

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Learn how to create a database](/cloud/cloud-databases/cloud-db-create)
* [Create a table](/cloud/cloud-tables/cloud-table-create)
* [Create a table column](/cloud/cloud-tables/cloud-table-add-column)

## Delete the selected column

WARNING: Deletion is permanent.

* Click **Databases** then the database that contains the table.
* Click **Tables** if it is not already selected.
* Click the table name.
* Click **Columns**.
* {% include /cloud-icons/icon-edit-unicode.md %} on the column > **Delete**.
* Enter "DELETE" in the confirmation dialog.
* Click **Delete**.
