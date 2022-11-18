---
title: How do I create a Database?
---

This procedure explains how to create a Database in FeatureBase Cloud.

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Learn how to manage databases](/cloud/cloud-databases/cloud-db-manage)
* [Perform data modeling](/concepts/data-modeling-overview) prior to creating databases to avoid issues.
* FeatureBase Trial accounts are limited to one database and development database shapes (8GB or 16GB)

## Cloud database shapes

{% include /concepts/database-shape-summary.md %}

* [Learn about cloud database shapes](/cloud/cloud-databases/cloud-db-shape)

## Naming standards

{% include /concepts/database-naming-standard.md %}

## How do I create a FeatureBase Database?

1. Click **Databases** > **New database**
2. Name your database.
3. Choose the database type:

| Type | Description | Further information |
|---|---|---|
| Start with pre-loaded database sample | 1 million records |  |
| Start with a clean database | Choose from development or production shapes. | [Database shapes](/cloud/cloud-databases/cloud-db-shapes) |

<ol start="4"><!--added because numbering restarts after para break-->
  <li>Click **Create database**.</li>
</ol>
## Next step

* [Learn how to add tables](/cloud/cloud-tables/cloud-table-create)

## Further information

* [Create database API reference](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/createDatabase)
* [Learn how to delete a database](/cloud/cloud-databases/cloud-db-delete)
