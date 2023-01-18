---
title: What states can my Database have?
---

{% include /concepts/db-states-summary.md %}

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Manage databases](/cloud/cloud-databases/cloud-db-manage)

## Database states

| Status | Description | Further information |
|---|---|---|
| CREATING |  Provisioning hardware, installing software, and other tasks to create the database. | [Create a cloud database](/cloud/cloud-databases/cloud-db-create) |
| RUNNING |  Post-creation state of the database which indicates it is ready for use. |  |
| UPDATING |  Updates may occur due to hardware changes or software patches. |  |
| DELETING |  Occurs when a database is deleted and hardware is being spun down. | [Delete a cloud database](/cloud/cloud-databases/cloud-db-delete) |
| DELETED |  Post deletion state that indicates successful deletion. |
| FAILED |  [Contact FeatureBase support](https://www.featurebase.com/contact-us) to help with this issue. |

## Further information

* [Query the database state via the API](https://api-docs-featurebase-cloud.redoc.ly/latest#operation/getDatabase)
