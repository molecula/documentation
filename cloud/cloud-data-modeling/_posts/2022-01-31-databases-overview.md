---
title: Databases Overview
---

 **⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes.

Databases are clusters of FeatureBase nodes. All of your data will live in tables within FeatureBase. They are dedicated resources for your data that you can load to and query against, and like common databases, you can only join tables that exist in the same database. Below is a list of database shapes offered:

### Shapes

| Database Shape | Database Memory (GB) | Purpose        |
| ---                    | ----------- | | ----------- |
| 8GB-Development        | 8       | development         |
| 64GB-Development       | 64      | development         |
| 16GB                   | 16      | production        |
| 32GB                   | 32      | production        |
| 64GB                   | 64      | production        |
| 128GB                  | 128     | production        |
| 256GB                  | 256     | production        |
| 512GB                  | 512     | production        |
| 1024GB                 | 1024    | production        |
| 2048GB                 | 2048    | production        |

dev: This database shape is meant for development and testing only
prod: This database shape is ready for production use, is over-provisioned on disk space and memory to ensure performance, and has data replicated should a node ever go down

Please note that all of these options might not be available for all organizations. When signing up, our support team will help you size and identify the right options for your use cases. We will customize your experience so that you only see the options identified best for you. This is to protect your organization from creating unnecessarily large databases that will incur additional costs. Additionally, we can work with you on a custom database option if none of our current options fit your need.

There are a couple of states associated with databases that are important to understand. You will see these states as a “status” in the UI and API. The list of states can be seen below:

### States

|Status | Description  |
| --- | ----------- |
|CREATING           |  The state of provisioning the hardware, installing software, and everything else in order to create a FeatureBase database.This will generally transition into RUNNING state. |
|RUNNING           |  The healthy state of a database that is ready to use. |
|UPDATING           |  The state of a database when an update is being applied. This might occur when hardware is being updated, software is being patched, etc. |
|DELETING           |  The state when a database is being deleted and hardware is being spun down. This will generally transition into DELETED state. |
|DELETED           |  The state of a database that has been successfully deleted. |
|FAILED           |  The state of a database when something goes wrong. This can occur for a variety of reasons. If you see this state and the database is ok to delete, feel free to do so. Otherwise, please contact us.|

## Further information

* [Learn how to create a Database in Cloud](/cloud/cloud-data-ingestion/creating-database)
