---
title: Ingestion ID example
---

This page provides examples of how to identify record IDs which are required to successfully import data to FeatureBase.

## ID methods

| Method | Description | Limitation |Example |
|---|---|---|---|
| `primary-key-fields` | Creates unique record IDs by concatenating one or more fields to strings using `/` as delimiter. Recommended for use where `id-field` is not possible. | Single fields are not indexed |  |
| `id-field` | Use when there is an existing key that consists of contiguous positive integers | Auto-incremented ID field from a relational database |
| `external-generate` | Generate unique record IDs using the FeatureBase ID allocator, optionally including `offset-mode`. |  |
| `auto-generate` | Generate unique record IDs suitable for testing.  |  |

When only a single field is used for this, it will *not* be indexed as a field in FeatureBase. When multiple source fields are used, each individual field will be indexed in FeatureBase, in addition to being used for the record ID.

## Example data source

| school | studentID | UUID | age | grade | ... |
|---|---|---|---|---|---|
| (string) | (int) | (string) | (int) | (int) |  |
| Anderson | 0 | 63a8 | 14 | 9 |  |
| Anderson | 1 | 98e9 | 16 | 11 |  |
| Anderson | 2 | 9ccb | 16 | 11 |  |
| Anderson | 3 | 7325 | 15 | 10 |  |
| Bowie    | 0 | 6ed3 | 17 | 12 |  |
| Bowie    | 1 | 62a5 | 16 | 11 |  |
| Bowie    | 2 | bd6c | 15 | 10 |  |
| Bowie    | 3 | 5651 | 16 | 10 |  |

## id-field method

The id-field method is used where there is a clearly defined Primary Key column. For example:

```
--id-field=studentID
```

This results in
* a FeatureBase record ID that matches the `studentID` key
* other columns represented as FeatureBase fields.

## primary-key method

This is used to ingest multiple files without ID conflicts.

In this example one column is identified as the primary key and can be used to create a unique record ID. For example:

```
--primary-key-fields=UUID
```

This results in:
* a FeatureBase record ID that matches the `UUID` key
* other columns represented as FeatureBase fields.

## primary-key composite ID

A composite ID is required where there is no clear unique identifier in the table or the data set is designed to use a composite key.

In this example, two columns can be combined to produce a unique composite identifier. For example:

```
--primary-key-fields=school,studentID
```

This results in a composite key delimited by `/`.

This method can potentially result in **every** column used as a FeatureBase field, including those used for the primary key.

## auto-generate

This method uses the FeatureBase ID generation feature to create auto-incrementing integer IDs.

auto-generate is recommended for:
* test data
* ingesting from a CSV

auto-generate does not support:
* multiple ingestion processes
* stopping and restarting an ingestion process

## External generate

External generate uses the FeatureBase ID generation feature to create auto-incrementing integer IDs.

It can be used with the Kafka ingestion process with `offset-mode`
