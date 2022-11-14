---
title: database states reference
---

Database states are represented by `status` in the FeatureBase application and API.

## Before you begin

{% include /cloud/cloud-before-begin.md %}

## Database states

| Status | Description | Further information |
|---|---|---|
| CREATING |  Provisioning hardware, installing software, and other tasks to create the database. | [Create a cloud database](/cloud/cloud-databases/cloud-db-create) |
| RUNNING |  Post-creation state of the database which indicates it is ready for use. |  |
| UPDATING |  Updates may occur due to hardware changes or software patches. |  |
| DELETING |  Occurs when a database is deleted and hardware is being spun down. | [Delete a cloud database](/cloud/cloud-databases/cloud-db-delete) |
| DELETED |  Post deletion state that indicates successful deletion. |
| FAILED |  An issue has occurred on the database that requires attention. |

## Further information

* [Learn how to query the database status via SSH](/cloud//query-cloud-data/cloud-query-db-status-ssh)
