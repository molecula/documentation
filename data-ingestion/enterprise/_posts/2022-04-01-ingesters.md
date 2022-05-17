---
id: ingesters
title: Ingesters
sidebar_label: Ingesters
---


## What is an ingester?

The Molecula Ingest Development Kit is a system for efficiently loading large amounts of data into a FeatureBase cluster.
It provides services which convert other data formats to FeatureBase's Roaring data format and load it into FeatureBase.

The ingester has three steps:
1. Collect records from a data source.
2. Translate records into FeatureBase's Roaring Bitmap format.
3. Copy the converted data into FeatureBase.

### 1. Collect records from a data source.

This process operates in large "batches" of records.
The entirety of a single batch is copied into FeatureBase at the same time.
Large batches mean that the per-batch overhead is less significant.
A batch is created once a specified number of records have been pulled.

:::note
When using the Kafka ingester, a smaller batch will be created if Kafka stops supplying records for at least a second.
:::

In Molecula `v2.2` and newer, the ingester has a `--track-progress` CLI option which periodically logs the number of records which have been pulled from a source, as well as the lifetime average record sourcing rate.

### 2. Translate records into FeatureBase's Roaring Bitmap format.

During the first step, the records are accumulated in a mostly uncompressed format. In order to compress them, the ingester needs to acquire "Key IDs" for all keyed rows and columns. In the case of a string field, there is one ID for each string value which can be present in the field. For a string-keyed index, there is one ID for each row. If the specified row/column did not previously exist, FeatureBase will generate an ID in this step.

The process of obtaining these Key IDs is referred to as translation in the ingester's logs:

```text
2020/07/20 14:14:47 translating batch of 10 took: 10.1172ms
```

Once all of the IDs have been mapped, the ingester converts the batch into roughly the format that FeatureBase will store it in.

### 3. Copy the converted data into FeatureBase.

The ingester acquires a transaction in order to ensure that no other application accesses an incompletely written index, and then copies all of the data into FeatureBase. This step is typically bottlenecked either by the network or the storage device backing the FeatureBase cluster.

The process of copying this data into FeatureBase is referred to as "flushing" in the ingester's logs, and typically takes a very small amount of time:

```text
2020/07/20 14:14:47 flushing batch of 10 to fragments took 84.2µs
```


## ID generation

When ingesting into Molecula, each record must be associated with a key. Ingesters support four ways to do this, three suitable for production workloads:

- `primary-key-fields`,
- `id-field`,
- `external-generate`, to use the FeatureBase ID allocator, optionally including `offset-mode`,
- `auto-generate`, suitable for testing.

The `id-field` option should be considered when there is an existing field in the data which uniquely identifies each record and consists of contiguous positive integers. For example, the auto-incremented ID field from a relational database is usually perfect for this.

In most other cases, the `primary-key-fields` option should be used. This uses one or more fields, converted to strings, then concatenated (using `|` as the delimiter), to create unique record IDs. When only a single field is used for this, it will *not* be indexed as a field in Molecula. When multiple source fields are used, each individual field will be indexed in Molecula, in addition to being used for the record ID.

As an example, consider a data set of students across multiple schools, perhaps with a different CSV file for each school:

| school   | studentID | UUID     |   age | grade | ... |
| ---      |       --- | ---      |   --- |   --- | --- |
| (string) |     (int) | (string) | (int) | (int) |     |
| Anderson |         0 | 63a8     |    14 |     9 |     |
| Anderson |         1 | 98e9     |    16 |    11 |     |
| Anderson |         2 | 9ccb     |    16 |    11 |     |
| Anderson |         3 | 7325     |    15 |    10 |     |
| Bowie    |         0 | 6ed3     |    17 |    12 |     |
| Bowie    |         1 | 62a5     |    16 |    11 |     |
| Bowie    |         2 | bd6c     |    15 |    10 |     |
| Bowie    |         3 | 5651     |    16 |    10 |     |

The studentID column, unique within a single school, serves as an identifier. When ingesting a single file corresponding to a single school, an ingest option like `--id-field=studentID` might work well. This will result in an index with `studentID` as Molecula record IDs, and every *other* column potentially represented as a FeatureBase field, including `school`, `UUID`, `age`, and `grade`.

To ingest multiple files without conflicting IDs, a different approach is required. When an appropriate identifier like a UUID is available, that can be used directly, with an option like `--primary-key-fields=UUID`. This will result in an index with `UUID` as FeatureBase record keys, so the index depends on key translation to convert UUID string values to integer record IDs. Every other column would potentially be represented as a FeatureBase field, including `school`, `studentID`, `age`, and `grade`.

Sometimes, an appropriate unique identifier is not directly available, or perhaps a data set is designed to use a composite key as a unique identifier. For example, if the students data set did not include a UUID column. In this case, multiple values can be combined to produce a composite identifier that is unique. One option that would work well here is the pair (school, studentID), which would be specified as `--primary-key-fields=school,studentID`. This would result in an index with this composite key as FeatureBase record keys. The key for the first row in the data set would be "Anderson|0". Again, this index would depend on key translation. This index, in contrast to the previous, could include *every* column as a FeatureBase field, including both `school` and `studentID` as separate fields.

The `auto-generate` option can create auto-incrementing integer IDs, when generating test data, or when ingesting from a CSV source, for example. This option is suitable for quick testing purposes, but does not support using multiple ingest processes or stopping and restarting ingest.

Finally, setting `external-generate` in addition to `auto-generate` uses FeatureBase's ID generation feature. Additionally, `offset-mode` can be set for use with Kafka.

## Kafka Ingester

The Kafka ingester reads Avro-encoded records from a Kafka topic, uses the Confluent schema registry to decode them, and ingests the data into Molecula.

[Full configuration reference](/reference/ingester-configuration#kafka-ingester)


### Schema Registry Behavior

How the Ingester indexes data in FeatureBase can be controlled to some extent via the schema registry. Avro schemas allow arbitrary properties to be associated with any item to implement features like [logical types](https://avro.apache.org/docs/current/spec.html#Logical+Types). 

A "float" or "double" type field in an Avro schema will be ingested into FeatureBase as a decimal field. If the property "scale" is provided, and is an integer, the value will be multiplied by 10^scale before being ingested. FeatureBase also stores the scale internally, so decimal fields will scale their query parameters appropriately, and floating point numbers are accepted as query parameters. A type which uses the logical type "decimal" will also be ingested as a decimal provided that it is 8 bytes or less (64 bit).

A "boolean" type field (or a union of boolean and null), will be ingested according to the "pack-bools" setting on the ingester. By default, boolean fields are packed into two "set" fields in FeatureBase which has a few benefits. It reduces fragmentation internally in FeatureBase, and allows one to perform "TopN" queries on all boolean fields together. The reason there are two fields is to distinguish between true, false, and null. Each row in the "bools" field represents whether the boolean value is true. Each row in the "bools-exists" field represents whether or not the value is null. So, a set bit in the "bools" field always implies the corresponding set bit in the "bools-exists" field, but the lack of a set bit in the "bools" field needs to check "bools-exists" to determine if the value is null or false.

An "enum" type will be ingested into a FeatureBase mutex field by default. Unlike a set field, if a different value comes in for the same record, the existing value will automatically be cleared—that is, each record (FeatureBase column) can only have one value for a mutex field.

A "string" type will be ingested into a FeatureBase set field by default. One can choose to use a mutex field instead by adding the property '"mutex": true' to the schema for that field.

Currently, the ingester supports a limited subset of Avro types. The top level type must be a Record, and nested fields are not supported—meaning that fields must not be of type Record or Map. Unions are only supported if it is a union of a supported type and null. Arrays are supported as long as they contain strings, bytes, fixed or enum types.

Field names must be valid FeatureBase field names, so they must be all lower case, start with a letter, contain only letters, numbers, or dashes, and be 64 characters or less. We're hoping to lift these restrictions in an upcoming release.


## Kafka Delete Ingester

The delete ingester for Kafka works similarly to the Kafka ingester in that it takes Avro-encoded records and uses the schema registry to decode them. It differs, however, in that a specific format is required to specify what should be deleted. Each record should contain the same fields for primary key (or ID) that the Kafka ingester uses, and in addition to that, there should be one other field called "fields" which is an array of strings and contains the names of the fields which should have their values deleted for the record at the given key. An example schema is:


```json
{
	"namespace": "org.test",
	"type": "record",
	"name": "deletes",
	"doc": "",
	"fields": [
    	{
        	"name": "abc",
        	"doc": "The ABC",
        	"type": "string"
    	},
    	{
        	"name": "db",
        	"doc": "TE DB Number",
        	"type": "string"
    	},
    	{
        	"name": "user_id",
        	"doc": "User ID",
        	"type": "int"
    	},
    	{
        	"name": "fields",
        	"type": {
                	"type": "array",
                	"items": "string"
            	}
    	}
	]
}
```

There is one special case when using packed bools: the string identifying the field for deletion in this case should resemble "bools|is-alive", where "bools" is the name of the packed bools field (as specified in the ingester via `pack-bools`, but defaulting to `bools`) and `is-alive` is the name of an individual boolean field.


### Configuration

The Kafka delete ingester configuration is the same as the Kafka ingester with the addition of `pilosa-grpc-hosts` (or `featurebase-grpc-hosts` with `future.rename` flag) which is the endpoint on which FeatureBase is listening for GRPC connections. This is necessary as the delete ingester uses an `Inspect` call to figure out what values need to be deleted and that call is only available over this interface. By default it's `localhost:20101`.


## Kafka Static Ingester

The Kafka Static ingester reads JSON-encoded records from a Kafka topic, uses a statically defined schema (with the ingester JSON header format) to decode them, and ingests the data into Molecula.

[Full configuration reference](/reference/ingester-configuration#kafka-static-ingester)


## CSV Ingester

The CSV ingester can read CSV files (optionally gzipped) and ingest them to FeatureBase. It uses a naming convention in the header of the CSV file to [specify how each field](/explanations/ingesters#field-types) should be ingested. The header can either be included in the file or passed in separately if editing the file is not desirable. If passed in separately one should use the `--ignore-header` option if the CSV file has a header so that it is not interpreted as data.

[Full CSV Ingester Configuration Reference](/reference/ingester-configuration#csv-ingester)


## SQL Ingester

The SQL ingester uses a sql connection (via MSSQL, MySQL, or Postgres) to select data from a sql endpoint, and ingests the data into Molecula. It uses the SQL table column names to [specify how each field](/explanations/ingesters#field-types) should be ingested, similar to the CSV Ingester.

[Full SQL Ingester Configuration Reference](/reference/ingester-configuration#sql-ingester)

## Field types

Many Molecula ingesters use the same syntax for describing how you want the fields in your source data to be ingested into Molecula. The basic structure is 

`field_name__FieldType_Arg1_Arg2`

That is, you name each field, and then you specify the field's type (separated by two underscores), and then any arguments that the field type takes. For example:

`age__Int_0_120`

declares that field is named 'age', is expected to be an integer, and be between 0 and 120. In general, all arguments are optional, but they are also positional, so if you want to specify a maximum value for the int field, you must first specify a minimum value.

[Here](/reference/ingester-configuration#header-descriptions) is the full list of field types along with their arguments.

## Ingest Tuning

### Optimizing the ingest process

There are a few options to tune the ingest process for a specific workload:
1. Batch size
2. Cache length
3. Number of ingesters

#### 1. Batch size

There is a fixed overhead from setting up a transaction, as well as a fixed overhead for each row.
Ingesting larger batches will cause these to average out more.
In general, larger batches will improve performance and proportionally raise memory usage.
There is no default batch size because the memory usage per record varies greatly between workloads.
For workloads with a large number of sparse keys, batch sizes of around 20,000 will typically use a few hundred megabytes of memory.
For workloads mostly consisting of high-frequency keys, it may be practical to use batch sizes of a million or more.

#### 2. Cache length

Under most workloads, the key translation process is the most expensive part of the ingest process.
In order to make this more efficient, the ingester keeps a cache of recently used keys in order to avoid re-requesting them from FeatureBase.
Using a longer cache will use more memory but potentially improve performance.
Using a shorter cache will potentially reduce performance but will also reduce memory requirements.

Before Molecula `v2.1`, every ingester had several LRU caches configured to each store up to approximately 1 million keys, with >100 bytes of memory overhead per key.

After Molecula `v2.1`, every ingester stores all keys used in the past 64 batches (keys used in multiple batches are only stored once). This cache length value can be changed with the `--cache-length` CLI flag.

The steady-state cache miss rate can be approximated as:

```math
p = (1-q)^(l*s)
```

Where:
- `p` = probability of a cache miss on a key
- `q` = frequency of usage of the key
- `l` = cache length
- `s` = batch size

The graph below shows the cache miss rate over different cache lengths assuming a key with an average frequency of 1 per 10000 records and a batch size of 5000. The default of 64 gives a miss rate of approximately 4% for this frequency. Beyond this, there are substantial declining returns.

[![Cache Miss Rate vs Cache Length](/img/cache-miss-rate-vs-length.png "Cache Miss Rate vs Cache Length")](https://www.desmos.com/calculator/bjcjris94d)

The graph below shows the cache miss rate over different key frequencies with a batch size of 5000 and a variety of cache lengths. For the default length of 64, the miss rate is negligible for keys more frequent than 1 per 10000, and extremely high for keys less frequent than 1 per million. If the cache length is doubled to 128, it spikes at a frequency a bit lower, at the expense of double the memory:

[![Cache Miss Rate vs Key Frequency](/img/cache-miss-rate-vs-freq.png "Cache Miss Rate vs Key Frequency")](https://www.desmos.com/calculator/hdhzehaeeg)


#### 3. Number of ingesters

It may sometimes be desirable to run multiple ingesters in parallel.
This may improve utilization on multi-core systems, or allow for redundancy.

It is possible to run multiple identical ingesters in the same process with the `--concurrency` CLI flag.
These ingesters are mostly independent, and roughly behave the same as two independent ingester processes would.

Alternatively, it is possible to launch multiple ingester processes, possibly on multiple machines.

### Common performance problems

#### Large mutex fields

Ingest of a mutex field with many possible values can be extremely slow.
The FeatureBase cluster has to compare every ingested row with every row in the field to detect if a pre-existing value needs to be cleared.
When operating with many unique mutex values, this results in `O(n^2)` ingest complexity.


## Field Type Mappings

More details are available in [Header Descriptions](/reference/ingester-configuration#header-descriptions).

### Avro.SchemaField.Type to IDK.Field

| Avro                     | Properties                             | IDK                                                         |
| ----                     | -------                                | ---                                                         |
| avro.String              |                                        | idk.StringField                                             |
| avro.String              | mutex=(bool)                           | idk.StringField{Mutex}                                      |
| avro.String              | quantum=(YMD)                          | idk.StringField{Quantum}                                    |
| avro.Enum                |                                        | idk.StringField{Mutex: true}                                |
| avro.Bytes               | logicalType=decimal                    | idk.DecimalField{Scale}                                     |
| avro.Bytes               | fieldType=decimal                      | idk.DecimalField{Scale}                                     |
| avro.Bytes               | fieldType=dateInt                      | idk.DateIntField{Layout, Epoch, Unit, CustomUnit}           |
| avro.Bytes               | fieldType=recordTime                   | idk.RecordTimeField                                         |
| avro.Bytes               |                                        | idk.StringField                                             |
| avro.Bytes               | mutex=(bool)                           | idk.StringField{Mutex}                                      |
| avro.Bytes               | quantum=(YMD)                          | idk.StringField{Quantum}                                    |
| avro.Array : avro.String |                                        | idk.StringArrayField                                        |
| avro.Array : avro.Bytes  |                                        | idk.StringArrayField                                        |
| avro.Array : avro.Fixed  |                                        | idk.StringArrayField                                        |
| avro.Array : avro.Enum   |                                        | idk.StringArrayField                                        |
| avro.Array : avro.String | quantum=(YMD)                          | idk.StringArrayField{Quantum)                               |
| avro.Array : avro.Bytes  | quantum=(YMD)                          | idk.StringArrayField{Quantum)                               |
| avro.Array : avro.Fixed  | quantum=(YMD)                          | idk.StringArrayField{Quantum)                               |
| avro.Array : avro.Enum   | quantum=(YMD)                          | idk.StringArrayField{Quantum)                               |
| avro.Array : avro.Long   |                                        | idk.IDArrayField                                            |
| avro.Array : avro.Long   | quantum=(YMD)                          | idk.IDArrayField{Quantum}                                   |
| avro.Int, avro.Long      | fieldType=id                           | idk.IDField                                                 |
| avro.Int, avro.Long      | fieldType=id,mutex=(bool)              | idk.IDField{Mutex}                                          |
| avro.Int, avro.Long      | fieldType=id, quantum=(YMD)            | idk.IDField{Quantum}                                        |
| avro.Int, avro.Long      | fieldType=int                          | idk.IntField                                                |
| avro.Int, avro.Long      | fieldType=int,min=(int64), max=(int64) | idk.IntField{Min, Max}                                      |
| avro.Int, avro.Long      | fieldType=signedIntBoolKey             | idk.SignedIntBoolKeyField                                   |
| avro.Float, avro.Double  | scale=(uint)                           | idk.DecimalField{Scale}                                     |
| avro.Boolean             |                                        | idk.BoolField                                               |
| avro.Null                |                                        | NOT SUPPORTED                                               |
| avro.Map                 |                                        | NOT SUPPORTED                                               |
| avro.Recursive           |                                        | NOT SUPPORTED                                               |
| avro.Record              |                                        | ERROR                                                       |
| avro.Union               |                                        | supports one or two members (if two, one must be avro.NULL) |

### IDK.Field to Avro.SchemaField.Type

| IDK                       | Avro                   | Properties                                         |
| -                         | -                      | -                                                  |
| idk.BoolField             | avro.Boolean           |                                                    |
| idk.DateIntField          | avro.Bytes             | fieldType=dateInt, epoch, unit, customUnit, layout |
| idk.DecimalField          | avro.Bytes             | fieldType=decimal, scale, precision=18             |
| idk.IDArrayField          | avro.Array : avro.Long | quantum                                            |
| idk.IDField               | avro.Long              | fieldType=id, mutex, quantum                       |
| idk.IgnoreField           |                        |                                                    |
| idk.IntField              | avro.Long              | fieldType=int, min, max                            |
| idk.RecordTimeField       | avro.Bytes             | fieldType=recordTime, layout                       |
| idk.SignedIntBoolKeyField | avro.Long              | fieldType=signedIntBoolKey                         |
| idk.StringArrayField      | avro.String            | quantum                                            |
| idk.StringField           | avro.String            | mutex, quantum                                     |
