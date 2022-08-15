---
id: streamingoverview
title: Streaming (HTTPS) Overview
sidebar_label: Streaming (HTTPS) Overview
---

 **⚠ WARNING:** This page contains information that only applies to Molecula's Cloud offering. Additionally, this page represents a work in progress that is subject to frequent changes. 

The ingest endpoint configuration will yield a persistent endpoint that allows you to stream data into your database over HTTPS. Each endpoint maps to one table within one database. If you have multiple disparate data sources, you may create multiple endpoints that push data to the same table. Once this source is provisioned, you can stream (post) JSON records to it using any method or application that can perform HTTPS requests. The table below describes the current limits of streaming data in:


|Category (Exclsuvie) | Current Limit  |
| --- | ----------- |
|Data Limit           |  1MB/sec |
|Record Limit         | 1000/sec |

There are a couple of states associated with these sources that are important to understand. You will see these states as a “status” through the UI and API. The list of states can be seen below:

|Status | Description  |
| --- | ----------- |
|CREATING           |  The state of provisioning the hardware, installing software, and everything else in order to create a source. This will generally transition into the ACTIVE state. |
|ACTIVE           |  The healthy state of a source that is ready to use. |
|UPDATING           |  The state of a source when an update is being applied. This might occur when hardware is being updated, software is being patched, etc. |
|DELETING           |  The state when a source is being deleted and hardware is being spun down. This will generally transition into the DELETED state. |
|DELETED           |  The state of a source that has been successfully deleted. |
|FAILED           | The state of a source when something goes wrong. This can occur for a variety of reasons. If you see this state and the source is ok to delete, feel free to do so. Otherwise, please contact us. |

This source's configuration requires a JSON schema for the data that streams through it This schema is essentially a list of columns that will be streaming in. Below is the schema syntax:

```json
[
  {
    "name": "the name of the destination column",
    "path": ["location within the JSON blob/records streaming in"],
    "type": "FeatureBase data type",
    "config": {
      "example": "optional param for a column type"
    }
  }
]
```

**Name**: The name is what you want the column name in your table to be. Column names can only contain lowercase alphanumeric characters, dashes (-), and underscores (_) but must start with an alphabetic character. They must be 230 characters or less in length.

**Path**: The path option is an array of JSON object keys which are applied in order. For example, `["a","b","c"]` would select 1 within `{"a":{"b":{"c":1}}}`. This path must only consist of strings.

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
* `"Quantum"`: the time quantum selection (Any Combination of  time granularity `Y`,`M`,`D`,`H` that doesn't skip a grain e.g. `"YM"`/`"YMD"` but not `YD`) to use when ingesting into a time column using the time value from a `"recordTime"`
* `"CacheConfig"`: the configuration when using a `TopN` cache; does not affect time columns
* `"TTL"`: Time To Live duration for views specifies when views will deleted. Allowed time units are `h`, `m`, `s`, `ms`, `us`, `ns`. Time quantum is required in order to use TTL.
* `"Layout"`: the format in which to parse time strings (defaults to RFC3339) - specified in [Go's format](https://golang.org/pkg/time/#pkg-constants)
* `"Min"`: the minimum possible value for an acceptable integer (defaults to -2^63)
* `"Max"`: the maximum possible value for an acceptable integer (defaults to 2^63 - 1)
* `"ForeignIndex"`: the target index to reference columns of
* `"Scale"`: the number of digits of precision to store after the decimal point
* `"Epoch"`: the epoch which timestamps should be relative to. This should only be set if the incoming data is an Epoch/number. The value may specify a timezone, for example `"1980-11-30T14:20:28.000+07:00"`, or use zulu time (i.e. +00:00) `"1980-11-30T14:20:28.000Z"`. Defaults to the Unix epoch if not configured.
* `"Unit"`: For a (`dateInt`) type column, `Unit` is the time unit in which to store a timestamp.  For the (`recordTime`, `timestamp`) type columns, only set `Unit` if the incoming data is an Epoch/number. The incoming value is interpreted as a duration with this `Unit`, starting at the configured `Epoch`. `Unit` Can be `"d"`, `"h"`, `"m"`, `"s"`, `"ms"`, `"us"`, `"ns"`, for day, hour, minute, second, millisecond, microsecond, nanosecond respectively or `"c"` for custom (using `"CustomUnit"` for `dateInt`). Defaults to `"s"`.
* `"CustomUnit"`: a 'duration' value which specifies a custom time unit; accepts values like "6h" for 6 hours, "1m30s" for 1 minute and 30 seconds; valid units can be described using "ns", "us", "ms", "s", "m", or "h"
* `"Granularity"`: the resolution at which the incoming values will be stored. Allowed values are `s`, `ms`, `us`, `ns`. Defaults to `"s"`.

Finally, there are a couple parameters that provide information about your schema:

|Parameter| Description  | Required? |
| ------- | ------------ | --------- |
|id_field   |  The id_field option should be used when there is an existing field in the data which uniquely identifies each record in the table and consists of contiguous positive integers. This maps to the _id column in your table. | Yes if primary key fields not provided |
|primary_key_fields  |  The primary_key_fields option should be used when the data has no columns that could be used for id_field. This option uses one or more columns (any type) and concatenates them to create unique record IDs for your table. This maps to the _id column in your table. | Yes if id column not provided |
|allow_missing_columns  |  A boolean option that allows one or more of the columns defined in the schema to be missing from the JSON records streamed in. If a column is missing and this parameter is true, that column is left null with no bits set. If this parameter is False and a column is missing from the JSON records, an error will return and data will not be loaded into your table. | Yes |

### Time Quantum

Setting a time quantums involves creating two columns. A column that contains the data that will be set with a time, and a column that holds the actual time. Note that the time column won't be a column in the target table and can be named anything. It is only is used as the time associated with all time quantums for the ingester. An example of the this might be "stores_visited_id" that holds all store ids someone has visited and at what time they visited that store last:

```json
[
	{
		"name": "stores_visited_id",
		"path": ["Path to stores_visited_id"],
		"type": "id",
		"config": {
			"Mutex": false
		}
	}
]
```

```json
[
	{
		"name": "Any name you want",
		"path": ["location to the timestamp/epoch"],
		"type": "recordTime"
	}
]
```

For `"recordTime"` columns, there are essentially two modes. If `"Epoch"` or `"Unit"` are set, then the incoming data is interpreted as a number. Otherwise it's assumed that the incoming data is interpreted as a date/timestamp and the `"Layout"` is used to parse that value.

### Record Format

Once an ingest endpoint is configured, data can be streamed to it. Each record should be composed of a JSON blob. One or many records can be sent in a single HTTPS request and should have the following syntax:

```json
{
    "records": [ 
        { "value": { <JSON blob containing columns of first record> } },
        { "value": { <JSON blob containing columns of second record> } },
        ...
    ]
}
```

It is recommended to “microbatch” records before sending them to maximize ingest rates. The maximum amount of records that can be sent in a single request is constrained by the limits above. The JSON blob does support nested structures, so it is up to your schema to define the “path” for each column’s value.
