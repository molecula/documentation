---
title: How do I delete a database in FeatureBase Cloud?
---

Learn how to delete a FeatureBase Cloud database.

## Warnings

* You must delete database tables **before** deleting a database.
* Databases cannot be recovered once deleted.
* Deletion may take a minute or two

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Create a database](/cloud/cloud-databases/cloud-db-create)
* [Delete tables](/cloud/cloud-data-ingestion/tables#drop-table)

<!-- restore this when the cloud-tables PR is merged
* [delete tables](/cloud/cloud-tables/cloud-table-drop)
-->

## How to delete a database

* Click **Databases**.
* Click &#8942; on the database to delete.
* Click **Delete**.
* Enter "Delete" in the confirmation dialog.
* Click **Delete**.

## Further information

* [Delete database API reference](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/deleteDatabase)
