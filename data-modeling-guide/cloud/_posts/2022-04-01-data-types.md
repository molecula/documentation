---
id: data-types
title: Data Types
sidebar_label: Data Types
---

<!--
TODO: ensure all default values and ranges are defined for constraints
Clarify what CACHETYPE does for users in a concise way if it comes into UI:
| CACHETYPE (type and size)  | IDSET, STRINGSET, ID, STRING | CACHETYPE has two components; type and size. Type can be either `ranked` or `none`. Ranked Fields maintain a sorted cache of column counts by Row ID (yielding the top rows by columns with a bit set in each). This cache facilitates the TopN query. The cache size defaults to `50000` | size (`ranked`), size(`50000`) |

add EPOCH if offered:
| EPOCH  | TIMESTAMP  | The epoch which timestamps should be relative to. This is represented as a RFC339 time stamp string. The value may specify a timezone, for example 1980-11-30T14:20:28.000+07:00, or use zulu time (i.e. +00:00) 1980-11-30T14:20:28.000Z.  | The Unix epoch (`1970-01-01T00:00:00Z`) |

Add Bool to types:
| BOOL  | The BOOL type stores simple boolean (true/false) values. Any integer value will be interpreted as false if 0 and true otherwise. Strings (in any upper/lower case combination) ‘0’, ‘f’, ‘false’, and the empty string will be interpreted as false, and true otherwise. | This type is best for simple query filtering |

-->

 **⚠ WARNING:** This page contains information that only applies to Molecula's Cloud offering. Additionally, this page represents a work in progress that is subject to frequent changes. 

## Data Types

Each column in a table has a data type. FeatureBase Cloud supports the following data types:

|Data Type| Description | Ideal Queries |
| ------- | ------------ | --------- |
| INT  | The INT type is for integers that are between `-2^63` and `2^63 -1`  | You should plan to use the INT type for any integer data that spans a large range of values and that you plan to run aggregate queries on. If you plan to group by integers or look for discrete values, and the cardinaltiy of values is low, you might consider using an ID type instead.  |
| TIMESTAMP  | The TIMESTAMP type is for date and time data.  | This type is good when time series analysis is performed. |
| DECIMAL  | The DECIMAL type is for decimals and is ideal when the exact scale is known. Strings will be attempted to be parsed as floats. Values will be truncated to the appropriate decimal place, not rounded, so you should round the value as needed before ingesting.  | This type is best used with aggregate and range queries. If you plan to group by or search for distinct values, you should consider using the STRING type instead |
| STRING  | The STRING type is for string, char, and varchar data.  | This type is best used for looking for discrete values or grouping by (if cardinality isn't very high). If the data has high cardinality, performance can decrease and storage will increase. |
| STRINGSET  | The STRINGSET type is special and unique to FeatureBase. It is best when individual records need the ability to set multiple STRING values for a single column. A simple example would be tracking all of the store names that a customer has ever visited.  | This is type is best used for grouping by or searching for discrete values. |
| ID  | The ID type is for unsigned integers that are between `1` and `2^63 -1`.  | This type is best used for looking for discrete values or grouping by (if cardinality is not high).  |
| IDSET  | The IDSET type is special and unique to FeatureBase. It is best when individual records need the ability to set multiple ID values for a single column. A simple example would be tracking all of the stores IDs that a customer has ever visited.  | This type is best used for grouping by or searching for discrete values. If you need to perform range queries using `<` or `>`, the INT type should be considered.  |

## Constraints

Each data type has constraints that can be applied to modify and optimize how data is stored and accessed. Constraints must be applied when creating the column. Each constraint and their relevant data type(s) are listed below:

|Constraint| Relevant Data Types | Description | Default Values |
| ------- | ------------ | --------- | --------- |
| MIN, MAX   | INT  | The minimum and maximum integer values expected for the column. Integers need to be between `-2^63` and `2^63 -1` | MIN(`-2^63`)  MAX (`2^63 -1`) <!--UI/API is limited to `-2^53` and `2^53 -1` due to precision loss loss due to JS and Go integer limitations at scale"--> |
| TIMEUNIT  | TIMESTAMP  | The time unit in which to store a timestamp. The accepted units are days, hours, minutes, seconds, milliseconds, microseconds, and nanoseconds and are declared with  `d`, `h`, `m`, `s`, `ms`, `us`, `ns`  respectively | `s` |
| TIMEQUANTUM & TTL (coming soon) | IDSET, STRINGSET  | Time quantums are special constraints that allow users to track when values are set for records by passing a `"recordTime"` timestamp in addition to the value itself. This is unique to SETs because the datatype supports multiple values that can be updated over time.  Tracking is supported by hour (`H`), day (`D`), month (`M`), or year (`Y`) or any combination of the four. Setting these allows for lower latency queries depending on the period of time you are querying over but increase storage. For example, If you plan to have queries with a range over multiple months, `MD` is the best option, but if you will be querying over only a couple of days, `D` will be preferred. An optional time to live (TTL) argument can be passed that will delete old values for a record after that period of time passes. TTL deletion runs when FeatureBase starts and every hour thereafter. You can specify the TTL by specifying an integer and a time unit from hours to nanoseconds (<integer>+`h`, `m`, `s`, `ms`, `us`, `ns`). A TTL of `72h` will retain values for 72 hours before deletion. A TTL of `0s` indicates data will never be deleted. | TIMEQUANTUM (Not set by default), TTL (`0s`) |
| SCALE  | DECIMAL  | The number of digits of precision to store after the decimal point. | 2 |


