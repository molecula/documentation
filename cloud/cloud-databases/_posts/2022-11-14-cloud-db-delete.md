---
title: How do I delete a database in FeatureBase Cloud?
---

Learn how to delete a FeatureBase Cloud database.

## Warnings

* You must drop database tables **before** deleting a database.
* Databases cannot be recovered once deleted.
* Deletion may take a minute or two

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Create a database](/cloud/cloud-databases/cloud-db-create)
* [Delete tables](/cloud/cloud-setup/cloud-quickstart-guide#spinning-down-a-database)

<!-- restore this when the cloud-tables PR is merged
* [Drop tables](/cloud/cloud-tables/cloud-table-drop)
-->

## How to delete a database

1. Click **Databases**.
2. Click &#8942; on the database to delete.
3. Click **Delete**.
4. Enter "Delete" in the confirmation dialog.
5. Click **Delete**.

## Further information

* [Delete database API reference](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/deleteDatabase)
