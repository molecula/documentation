---
title: Streaming (HTTPS) Overview
---

**⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes.

## Before you start

{% include /cloud/database-dependencies.md %}

## Streaming data to tables

FeatureBase allows you to stream data into your tables using one source type called an "ingest endpoint". The ingest endpoint configuration will create a persistent endpoint that allows you to push data over HTTPS. Each endpoint maps to one table within one database. If you have multiple disparate data sources, you may create multiple endpoints that push data to the same table. Once this endpoint is provisioned, you can stream (POST) JSON records to it using any method or tool that can perform HTTPS requests. The table below describes the current limits of streaming data in for each endpoint:

|Category (Exclusive) | Current Limit  |
| --- | ----------- |
|Data Limit           |  1MB/sec |
|Record Limit         | 1000/sec |

## States

There are a couple of states associated with these sources that are important to understand. You will see these states as a “status” through the UI and API. The list of states can be seen below:

|Status | Description  |
| --- | ----------- |
|CREATING           |  The state of provisioning the hardware, installing software, and everything else in order to create a source. This will generally transition into the ACTIVE state. |
|ACTIVE           |  The healthy state of a source that is ready to use. |
|RESTARTING           |  The state of a source when an update is being applied. This will occur when the mappings are changed, hardware is being updated, software is being patched, etc. |
|DELETING           |  The state when a source is being deleted and hardware is being spun down. This will generally transition into the DELETED state. |
|DELETED           |  The state of a source that has been successfully deleted. |
|FAILED           | The state of a source when something goes wrong. This can occur for a variety of reasons. If you see this state and the source is ok to delete, feel free to do so. Otherwise, please contact us. |


## Configuration

* [Learn how to create an ingest endpoint](/cloud/cloud-data-ingestion/streaming-https-endpoint/create-ingest-endpoint)

## Streaming Data

* [Learn how to stream data to an ingest endpoint](/cloud/cloud-data-ingestion/streaming-https-endpoint/stream-ingest-endpoint)

<!--
**Type**: This is the FeatureBase type you are storing the value as. A list of types is below:

| `"type":`            | JSON Input Type                         | FeatureBase Data Type                       | Config Options                                   |
|----------------------|-----------------------------------------|----------------------------------------------|--------------------------------------------------|
| `"id"`               | `10`                                    | set/mutex/time                               | `"Mutex"`, `"Quantum"`, `"TTL"`, `"CacheConfig"` |
| `"ids"`              | `[1, 2, 3]`                             | set/time                                     | `"Quantum"`, `"TTL"`, `"CacheConfig"`            |
| `"string"`           | `"example"`                             | keyed set/mutex/time                         | `"Mutex"`, `"Quantum"`, `"TTL"`, `"CacheConfig"` |
| `"strings"`          | `["a", "b", "c"]`                       | keyed set/time                               | `"Quantum"`, `"TTL"`, `"CacheConfig"` |
| `"bool"`             | `true`/`false`                          | packed bool column (row in keyed set columns)  | None                                             |
| `"int"`              | `10`/`-12`/`"example"`                  | integer (possibly a foreign-index reference) | `"Min"`, `"Max"`, `"ForeignIndex"`               |
| `"decimal"`          | `10.9`/`"10.9"`                         | decimal                                      | `"Scale"`                                        |
| `"signedIntBoolKey"` | `10`/`-12`                              | same as id, except a negative value clears   | None                                             |
| `"recordTime"`       | `"2006-01-02T15:04:05Z07:00"`/`1273823` | applied to id(s)/string(s) (using "Quantum") | `"Layout"`, `"Epoch"` , `"Unit"`                  |
| `"dateInt"`          | `"2006-01-02T15:04:05Z07:00"`/`1273823` | integer timestamp relative to an epoch       | `"Layout"`, `"Epoch"`, `"Unit"`, `"CustomUnit"`  |
| `"timestamp"`        | `"2006-01-02T15:04:05Z07:00"`/`1273823` | integer(BSI) timestamp relative to an epoch  | `"Granularity"`, `"Layout"`, `"Epoch"`, `"Unit"` |

### Column Configuration Options

When all config options are left as default, the `"Config"` column may be omitted. Otherwise, the config options are:
* `"Mutex"`: if set to `true`, the data will be ingested into a mutex column instead of a set column
* `"Quantum"`: the time quantum selection (Any Combination of  time granularity `Y`,`M`,`D`,`H` that doesn't skip a grain e.g. `"YM"`/`"MDH"` but not `YD`) to use when ingesting into a time column using the time value from a `"recordTime"`
* `"CacheConfig"`: the configuration when using a `TopN` cache; does not affect time columns
* `"TTL"`: Time To Live duration for views specifies when views will deleted. Allowed time units are `h`, `m`, `s`, `ms`, `us`, `ns`. Time quantum is required in order to use TTL.
* `"Layout"`: the format in which to parse time strings (defaults to RFC3339) - specified in [Go's format](https://golang.org/pkg/time/#pkg-constants)
* `"Min"`: the minimum possible value for an acceptable integer (defaults to -2^63)
* `"Max"`: the maximum possible value for an acceptable integer (defaults to 2^63 - 1)
* `"ForeignIndex"`: the target index to reference columns of
* `"Scale"`: the number of digits of precision to store after the decimal point
* `"Epoch"`: Only set `Epoch` if the incoming data is a number (rather than a timestamp string). The incoming number will be interpreted as the number of `Unit` since `Epoch`. The value may specify a timezone, for example `"1980-11-30T14:20:28.000+07:00"`, or use zulu time (i.e. +00:00) `"1980-11-30T14:20:28.000Z"`. Defaults to the Unix epoch if not configured.  E.G. If the `Unit` is 's' and the `Epoch` is January 1, 2000 and the number is 86,400 then the number represents January 2, 2000.
* `"Unit"`: For a (`dateInt`) type column, `Unit` is the time unit in which to store a timestamp.  For the (`recordTime`, `timestamp`) type columns, only set `Unit` if the incoming data is a number (rather than a timestamp string). The incoming number will be interpreted as the number of `Unit` since `Epoch`. `Unit` Can be `"d"`, `"h"`, `"m"`, `"s"`, `"ms"`, `"us"`, `"ns"`, for day, hour, minute, second, millisecond, microsecond, nanosecond respectively or `"c"` for custom (using `"CustomUnit"` for `dateInt`). Defaults to `"s"`.  E.G. If the `Unit` is 's' and the `Epoch` is January 1, 2000 and the number is 86,400 then the number represents January 2, 2000.
* `"CustomUnit"`: a 'duration' value which specifies a custom time unit; accepts values like "6h" for 6 hours, "1m30s" for 1 minute and 30 seconds; valid units can be described using "ns", "us", "ms", "s", "m", or "h"
* `"Granularity"`: the resolution at which the incoming values will be stored. Allowed values are `s`, `ms`, `us`, `ns`. Defaults to `"s"`.





### Time Quantum

Setting a time quantum involves creating two columns. A `IDSET` or `STRINGSET` column that contains the data that will be associated with a time, and a column that holds the actual time. Note that the time column won't be a column in the target table and must be named "_timeQuantume". It is only used as the time associated with all time quantum `IDSET` or `STRINGSET` columns for the endpoint. An example of the this might be "stores_visited_id" that holds all store ids someone has visited and at what time they visited that store last:

```json
[
	{
		"name": "stores_visited_id",
		"path": ["Path to stores_visited_id"]
	}
]
```

```json
[
	{
		"name": "_timeQuantum",
		"path": ["location to the timestamp/epoch"]
	}
]
```

For `"recordTime"` columns, there are essentially two modes. If `"Epoch"` or `"Unit"` are set, then the incoming data is interpreted as a number. Otherwise it's assumed that the incoming data is interpreted as a date/timestamp and the `"Layout"` is used to parse that value.
-->
