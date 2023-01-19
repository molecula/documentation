---
title: How do I drop a table in FeatureBase Cloud?
---

There are a number of reasons why you may choose to drop a table, including:
* incorrect configuration
* incorrect name
* database deletion
* data deletion

## Warnings

* Tables cannot be recovered once deleted
* Deleting tables will affect running queries

{% include /cloud/cloud-table-create-sql.md %}

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Create a database](/cloud/cloud-databases/cloud-db-create)
* [Create a table](/cloud/cloud-tables/cloud-table-create)

## Drop the selected table

* Click Databases then the database that contains the table.
* Click **Tables** if it is not already selected.
* {% include /cloud-icons/icon-edit-unicode.md %} > **Drop table**
* Enter "DELETE" in the confirmation dialog.
* Click **Drop table**.
