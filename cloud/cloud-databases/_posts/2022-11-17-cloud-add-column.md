---
title: How do I add a column to an existing table in FeatureBase Cloud?
---

You can add a column to a FeatureBase table.

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Learn how to create a database](/cloud/cloud-databases/cloud-db-manage)
* [Learn how to create tables](/cloud/cloud-databases/cloud-table-manage)
* Table columns cannot be edited once created.

## Table column data types and constraints

You can choose from the following data types and their constraints

| Data type | Optional constraints | Further information |
|---|---|---|
| bool (boolean) | none |  |
| decimal | SCALE | [DECIMAL data type](/cloud/cloud-databases/cloud-decimal-data-type) |
| id | none | [ID data type](/cloud/cloud-databases/cloud-id-data-type) |
| idset | Time Quantum, TTL (Time to live) | [IDSET data type](/cloud/cloud-databases/cloud-idset-data-type) |
| int | min, max | [INT data type](/cloud/cloud-databases/cloud-int-data-type) |
| string | none | [STRING data type](/cloud/cloud-databases/cloud-string-data-type) |
| stringset | Time Quantum, TTL (Time to live) | [STRINGSET data type](/cloud/cloud-databases/cloud-stringset-data-type) |
| timestamp | Time unit | [TIMESTAMP data type](/cloud/cloud-databases/cloud-timestamp-data-type) |

## Step 1: View all tables

{% include /cloud/cloud-view-table-list.md %}

## Step 2: Add a column to a table

1. Click the table name.
2. Click **Columns**.
3. Click **Add column**.
4. Enter a name for the column
5. Choose the data type and enter values for the constraints if available.
6. Click **Add column**

## Further information

* [Learn how to drop a table column](/cloud/cloud-databases/cloud-table-drop-column)
