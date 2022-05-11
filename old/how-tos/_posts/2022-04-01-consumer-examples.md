---
id: consumer-usage-examples
title: Consumer Usage Examples
sidebar_label: Consumer Usage Examples
---


Also refer to the [ingester configuration reference](/reference/ingester-configuration) page for details on configuration flags for all consumers.


# Molecula consumer binaries

<!--
molecula-consumer-furan - customer-specific, deprecated
molecula-consumer-github - for internal benchmarking
-->


## CSV consumer

### Example 1: Simple ingest, internal header, multiple-file, ID autogen

Command:

```shell
molecula-consumer-csv \
    --batch-size=10000 \
    --auto-generate \
    --index=csv-ingest-test \
    --files=sample.csv,sample2.csv \
    --concurrency=2
```

sample.csv:

```csv
asset_tag__String,fan_time__RecordTime_2006-01-02,fan_val__String_F_YMD
ABCD,2019-01-02,70%
ABCD,2019-01-03,20%
BEDF,2019-01-02,70%
BEDF,2019-01-05,90%
ABCD,2019-01-30,40%
BEDF,2019-01-08,10%
BEDF,2019-01-08,20%
ABCD,2019-01-04,30%
```

Note the *Header Specification*:

`asset_tag__String,fan_time__RecordTime_2006-01-02,fan_val__String_F_YMD`

This specifies three fields:

- `asset_tag`, a `String` field, ...
- `fan_time`, a `RecordTime` field, with timestamp layout format `2006-01-02` (according to go time)
- `fan_val`, a `String` field, ...


<!-- TODO explanation -->
<!-- TODO sample queries -->

### Example 2: Simple ingest, external header

Command:

```shell
molecula-consumer-csv \
    --batch-size=10000 \
    --auto-generate \
    --header=asset_tag__String,fan_time__RecordTime_2006-01-02,fan_val__String_F_YMD \
    --ignore-header
    --index=csv-ingest-test \
    --files=sample.csv,sample2.csv \
    --concurrency=2
```

sample.csv:

```csv
asset_tag,fan_time,fan_val
ABCD,2019-01-02,70%
ABCD,2019-01-03,20%
BEDF,2019-01-02,70%
BEDF,2019-01-05,90%
ABCD,2019-01-30,40%
BEDF,2019-01-08,10%
BEDF,2019-01-08,20%
ABCD,2019-01-04,30%
```

Note that a header line is present in the csv file, however, we are ignoring it. The *Header specification*
is passed in the command line with `--header`.

### Example 3: Simple ingest over tls

Command

```shell
molecula-consumer-csv \
    --pilosa-hosts=https://localhost:10101
    --tls.certificate=featurebase.local.crt \
    --tls.key=featurebase.local.key \
    --tls.skip-verify \
    --batch-size=10000 \
    --auto-generate \
    --index=csv-ingest-test \
    --files=sample.csv \
    --concurrency=2
```

Or, equivalently, with the [`--future.rename` configuration flag](/reference/featurebase-rename):

```shell
molecula-consumer-csv \
    --future.rename \
    --featurebase-hosts=https://localhost:10101
    --tls.certificate=featurebase.local.crt \
    --tls.key=featurebase.local.key \
    --tls.skip-verify \
    --batch-size=10000 \
    --auto-generate \
    --index=csv-ingest-test \
    --files=sample.csv \
    --concurrency=2
```

Note that we provide tls configuration (`--tls.certificate` and `--tls.key`) to the command for securely
connecting to FeatureBase. The values for these parameters are the filenames for certificate and key that
correspond to the target FeatureBase instances. If verification of certificate is not desired
(especially for self-signed certificates), we need to include `--tls.skip-verify`. Since the default
bind point for FeatureBase hosts are HTTP, we provide the bind points using `--pilosa-hosts` (or,
`--featurebase-hosts` with the [`--future.rename` configuration flag](/reference/featurebase-rename)).

## Kafka consumer

The Kafka consumer requires:
- A list of Kafka hosts
- A FeatureBase index name (`--index <indexname>`),
- Exactly one primary key method (`--primary-key-field <fieldnames>`, `--id-field <fieldname>` or `--auto-generate`),

### Example 1: minimal

<!-- TODO -->

Command:
`molecula-consumer-kafka `

Data:
```json

```


### Kafka delete consumer
Configuration and usage for this consumer is identical to the Kafka consumer, with the exception of the `pilosa-grpc-hosts` (or `featurebase-grpc-hosts` with the [`--future.rename` configuration flag](/reference/featurebase-rename)). Instead of inserting data into FeatureBase from the received messages, it deletes the corresponding data from FeatureBase. This provides delete capabilities using the same Kafka interface.


## Kafka static consumer
Configuration and usage for this consumer is similar to the kafka consumer. It was developed for use in scenarios where Kafka is used without Confluent Schema Registry. In this case, the schema must be provided explicitly; the "static" in the consumer name refers to this "static schema". For compatibility with complex JSON message formats, the schema is specified with a JSON document rather than the "header spec" used in other consumers.

### Example 1: Simple ingest

Command:

```shell
molecula-consumer-kafka-static \
    --kafka-hosts "localhost:9092" \
    --index kafka-test \
    --batch-size 10000 \
    --topics test-topic \
    --max-msgs 10000 \
    --auto-generate \
    --external-generate \
    --header kafka-static-header-1.json
```


kafka-static-header-1.json:
```json
[
    {
        "name": "int-featurebase-name",
        "path": [
            "int-kafka-path"
        ],
        "type": "int"
    },
    {
        "name": "string-featurebase-name",
        "path": [
            "string-kafka-path"
        ],
        "type": "string"
    }
]
```

Example Kafka message:
```json
{
    "int-kafka-path": 12345,
    "string-kafka-path": "arbitraryString"
}
```

The header file specifies two fields:

- `int-featurebase-name`, a FeatureBase field of type `int`, populated with the value from the `int-kafka-path` item in the Kafka message.
- `string-featurebase-name`, a string-keyed FeatureBase field of type `set`, populated with the value from the `string-kafka-path` item in the Kafka message.

<!-- TODO explanation -->
<!-- TODO queries -->

### Example 2: 

Command:

```shell
molecula-consumer-kafka-static \
    --kafka-hosts "localhost:9092" \
    --index kafka-test \
    --batch-size=10000 \
    --topics test-topic \
    --auto-generate \
    --allow-missing-fields \
    --header kafka-static-header-2.json
```

kafka-static-header-2.json:
```json
[
    {
        "name": "from_ip",
        "path": [
            "from_interface",
            "ip"
        ],
        "type": "string"
    },
    {
        "name": "from_port",
        "path": [
            "from_interface",
            "port"
        ],
        "type": "int"
    },
    {
        "name": "to_ip",
        "path": [
            "to_interface",
            "ip"
        ],
        "type": "string"
    },
    {
        "name": "to_port",
        "path": [
            "to_interface",
            "port"
        ],
        "type": "int"
    },
    {
        "name": "event_time",
        "path": [
            "event_time"
        ],
        "type": "timestamp"
    },
    {
        "name": "severity",
        "path": [
            "severity"
        ],
        "type": "set"
    },
    {
        "name": "bytes",
        "path": [
            "bytes"
        ],
        "type": "int"
    },
    {
        "name": "protocol",
        "path": [
            "protocol"
        ],
        "type": "string"
    }
]
```
<!-- TODO more complex path selection -->
<!-- TODO more types and config options in header file -->


Sample Kafka message:

```json
{
    "from_interface": {
        "ip": "10.203.33.18",
        "port": 38935
    },
    "to_interface": {
        "ip": "203.77.221.220",
        "port": 5872
    },
    "event_time": "2021-06-01T16:02:55Z06:00",
    "protocol": "UDP",
    "severity": 0,
    "bytes": 8593
}
```

<!-- TODO queries -->

## SQL consumer


### Example 1

The `molecula-consumer-sql` examples use sample data represented by the following two tables.

Table: `assets`

| asset_tag | weight | warehouse |
|-----------|--------|-----------|
| ABCD      |     16 | US-EAST   |
| EFGH      |      9 | US-WEST   |
| IJKL      |     47 | US-WEST   |
| MNOP      |     30 | US-EAST   |


Table: `events`

| pk     | asset_tag | fan_time   | fan_vol |
|--------|-----------|------------|---------|
| aus-14 | ABCD      | 2021-06-21 | 90%     |
| aus-15 | EFGH      | 2021-06-19 | 10%     |
| aus-16 | ABCD      | 2021-06-20 | 60%     |
| den-11 | IJKL      | 2021-06-19 | 70%     |
| den-12 | MNOP      | 2021-06-20 | 90%     |
| nyc-78 | MNOP      | 2021-06-21 | 80%     |
| den-13 | MNOP      | 2021-06-21 | 80%     |
| nyc-79 | ABCD      | 2021-06-21 | 30%     |


based on these CREATE TABLE statements:

```sql
CREATE TABLE `assets` (
    `asset_tag` char(4) NOT NULL DEFAULT '',
    `weight` int(8) DEFAULT 0,
    `warehouse` char(10),
    PRIMARY KEY (`asset_tag`)
);
```

```sql
CREATE TABLE `events` (
    `pk` char(10) NOT NULL DEFAULT '',
    `asset_tag` char(4) NOT NULL DEFAULT '',
    `fan_time` date NOT NULL,
    `fan_vol` char(10),
    PRIMARY KEY (`pk`)
);
```

This example creates an index based directly on the `assets` table:

```shell
molecula-consumer-sql \
    --driver mysql \
    --connection-string 'username:password@(127.0.0.1:3306)/dbname' \
    --pilosa-hosts localhost:10101 \
    --batch-size 10000 \
    --index=asset_list \
    --primary-key-fields 'asset_tag' \
    --row-expr 'SELECT asset_tag as asset_tag__String, weight as weight__Int, warehouse as warehouse__String FROM assets'
```

Or, equivalently, with the [`--future.rename` configuration flag](/reference/featurebase-rename):

```shell
molecula-consumer-sql \
    --future.rename \
    --driver mysql \
    --connection-string 'username:password@(127.0.0.1:3306)/dbname' \
    --featurebase-hosts localhost:10101 \
    --batch-size 10000 \
    --index=asset_list \
    --primary-key-fields 'asset_tag' \
    --row-expr 'SELECT asset_tag as asset_tag__String, weight as weight__Int, warehouse as warehouse__String FROM assets'
```


It's important to understand that the data to be indexed does not necessarily align to a table in the source database. Rather, it aligns with the results of the SQL query specified in the `--row-expr` argument. In other words, you can use any SQL functionality to join or modify data, and the result of that query is what the consumer considers to be the source data.

So for example, you might want to ingest the `events` table, but treat the `fan_vol` field as an integer instead of a string. In that case, you can simply use SQL functions to convert that string field to an integer-ready value:

```shell
molecula-consumer-sql \
    --driver mysql \
    --connection-string 'username:password@(127.0.0.1:3306)/dbname' \
    --pilosa-hosts localhost:10101 \
    --batch-size 10000 \
    --index=event_list \
    --primary-key-fields 'pk' \
    --row-expr 'SELECT pk as pk__String, asset_tag as asset_tag__String, fan_time as `fan_time__Timestamp_s_2006-01-02`, SUBSTRING(fan_vol, 1, CHAR_LENGTH(fan_vol)-1) as fan_vol__Int FROM events'
```

Or, equivalently, with the [`--future.rename` configuration flag](/reference/featurebase-rename):

```shell
molecula-consumer-sql \
    --future.rename \
    --driver mysql \
    --connection-string 'username:password@(127.0.0.1:3306)/dbname' \
    --featurebase-hosts localhost:10101 \
    --batch-size 10000 \
    --index=event_list \
    --primary-key-fields 'pk' \
    --row-expr 'SELECT pk as pk__String, asset_tag as asset_tag__String, fan_time as `fan_time__Timestamp_s_2006-01-02`, SUBSTRING(fan_vol, 1, CHAR_LENGTH(fan_vol)-1) as fan_vol__Int FROM events'
```

This example illustrates using a SQL query which joins data from both tables into a single FeatureBase index which contains the event data along with the `weight` of the relative `asset_tag`. It also creates a new field completely, called `locale`, based on the first three characters of the `pk` field:

```shell
molecula-consumer-sql \
    --driver mysql \
    --connection-string 'username:password@(127.0.0.1:3306)/dbname' \
    --pilosa-hosts localhost:10101 \
    --batch-size 10000 \
    --index=events_plus_weight \
    --primary-key-fields 'pk' \
    --row-expr 'SELECT events.pk as pk__String, events.asset_tag as asset_tag__String, assets.weight as weight__Int, SUBSTRING(events.pk, 1, 3) as locale__String FROM events INNER JOIN assets on assets.asset_tag = events.asset_tag'
```

Or, equivalently, with the [`--future.rename` configuration flag](/reference/featurebase-rename):

```shell
molecula-consumer-sql \
    --future.rename \
    --driver mysql \
    --connection-string 'username:password@(127.0.0.1:3306)/dbname' \
    --featurebase-hosts localhost:10101 \
    --batch-size 10000 \
    --index=events_plus_weight \
    --primary-key-fields 'pk' \
    --row-expr 'SELECT events.pk as pk__String, events.asset_tag as asset_tag__String, assets.weight as weight__Int, SUBSTRING(events.pk, 1, 3) as locale__String FROM events INNER JOIN assets on assets.asset_tag = events.asset_tag'
```

<!-- TODO
## bigquery
-->
