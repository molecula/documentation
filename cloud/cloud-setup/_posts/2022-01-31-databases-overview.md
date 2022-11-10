---
title: Databases Overview
---

 **⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes.

Databases are clusters of FeatureBase nodes. All of your data will live in tables within FeatureBase. They are dedicated resources for your data that you can load to and query against, and like common databases, you can only join tables that exist in the same database.

## Before you begin

* [Learn about data modeling](/concepts/data-modeling-overview)
* [Contact FeatureBase Support](https://www.featurebase.com/contact-us) for help optimizing  database for your use case.

## Shapes

NOTE: These options may not be available for some organizations. Contact FeatureBase Support for help

### Production shapes

Production database shapes are over-provisioned on disk space and memory to ensure performance, and has data replicated should a node ever go down.

| Database Shape | Database Memory (GB) |
|---|---|
| 16GB | 16 |
| 32GB | 32 |
| 64GB | 64 |
| 128GB | 128 |
| 256GB | 256 |
| 512GB | 512 |
| 1024GB | 1024 |
| 2048GB | 2048 |

### Development shapes

These shapes are intended for development and testing.

| Database Shape | Database Memory (GB) |
| --- | ----------- |
| 8GB-Development | 8 |
| 64GB-Development | 64 |

## Database states

Database states are represented by `status` in the FeatureBase application and API.

|Status | Description  |
| --- | ----------- |
| CREATING |  The state of provisioning the hardware, installing software, and everything else in order to create a FeatureBase database.This will generally transition into RUNNING state. |
| RUNNING |  The healthy state of a database that is ready to use. |
| UPDATING |  The state of a database when an update is being applied. This might occur when hardware is being updated, software is being patched, etc. |
| DELETING |  The state when a database is being deleted and hardware is being spun down. This will generally transition into DELETED state. |
| DELETED |  The state of a database that has been successfully deleted. |
| FAILED |  The state of a database when something goes wrong. This can occur for a variety of reasons. If you see this state and the database is ok to delete, feel free to do so. [Contact FeatureBase Support](https://www.featurebase.com/contact-us) if you have any questions. |

## Further information

* [Learn how to create a Database in Cloud](/cloud/cloud-setup/creating-database)
