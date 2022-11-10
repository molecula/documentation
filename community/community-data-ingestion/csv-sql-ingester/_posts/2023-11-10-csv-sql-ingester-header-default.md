---
title: CSV and SQL ingester default header
---

This is a list of headers suitable for use with CSV and SQL ingesters. These describe how fields in source data are to be ingested by FeatureBase.

## Before you begin

* [Learn about ingester configuration](/community/community-data-ingestion/ingester-configuration)
* [Learn about CSV ingester configuration](/community/community-data-ingestion/csv-sql-ingester/csv-ingester-configuration)
* [Learn about SQL ingester configuration](/community/community-data-ingestion/csv-sql-ingester/sql-ingester-configuration)

## Syntax

```
field_name__FieldType_Arg1_Arg2
```

## Arguments

* field_name
* __FieldType - list of field types found under [/community/community-data-ingestion/]
* _argN - optional arguments that are positional

## Examples

Declare a field named `age`, that it is expected to be an integer and two positional arguments which represent a minimum and maximum value

```
age__Int_0_120`
```

## Header field types

Here is the full list of field types along with their arguments:

| Field type | Further information |
|---|---|
| String | [/community/community-data-ingestion/csv-sql-ingester]

### String
Example:
`state__String_T_YMD`

String is for arbitrary string data. The data will be stored in a 'set', 'mutex', or 'time' type field depending on the arguments given, but will always use key translation.

Argument 1 — Mutex: Either 'T' or 'F'. Specifies whether a "mutex" type field should be used  in FeatureBase. If 'T', a "mutex" field is used, and any particular record may only have a single value. If 'F', a "set" field is used, and a particular record may have multiple values for this field.

Argument 2 — Time Quantum: If this argument is provided, the field will be a "time" field rather than "set" or "mutex". "time" fields work similarly to "set" fields but each value can have a coarse grained timestamp associated with it. The granularity is controlled by this argument and can be anything from yearly down to hourly. See the [FeatureBase Data Model docs](/concepts/data-modeling-overview) for more information about time fields.

### ID
Example:
`class__ID_T_YMD`

ID has the same arguments and works the same way as String, but doesn't use key translation. The values must be parseable into unsigned integers.

### Bool
Example:
`is_alive__Bool`

Bool will either be stored in a "bool" field, or into packed bools fields if that option is enabled and available on the ingester in use. In the case of packed bools, the name of the field becomes the value at which a bit will be set in the "bools" and "bools-exists" fields. The ingester attempts to coerce incoming data to `true` or `false`. Any integer value will be interpreted as `false` if 0 and `true` otherwise. The strings (in any upper/lower case combination) '0', 'f', 'false',  and the empty string will be interpreted as `false`, and `true` otherwise.

No arguments.

### Int
Example:
`age__Int_1_120`

Int will be stored in an "int" field in FeatureBase. A string value will be attempted to be parsed as an integer.

Argument 1 — Min: The lower bound on the field's values.

Argument 2 — Max: The upper bound on the field's values.

### Decimal
Example:
`cost__Decimal_2`

Decimal will be stored in a "decimal" field in FeatureBase. Strings will be attempted to be parsed as floats. Note that values will be truncated to the appropriate decimal place, not rounded, so you should round the value as needed before ingesting.

Argument 1 — Scale: The "scale" for the decimal field. Essentially the number of digits after the decimal point that you wish to store. In the example we have a cost, so we use a scale of '2' to track cost in dollars down to the cent.

### ForeignKey
Example:
`user_id__ForeignKey_users`

ForeignKey is used when values of a field refer to records in another table. The foreign table may be using keys or not, and if it is using keys, the foreign key values can be strings, otherwise they should be unsigned integers. Under the hood, this uses an int field, so each record may only have a single value (as opposed to a 'set' field where each record may have many values associated).

Argument 1 — The name of the foreign table.

### DateInt
Example:
`modified_day__DateInt_2006-01-02_1970-01-01_C_1d`

DateInt stores a datetime in an "int" field in FeatureBase. The dates are converted to ints according to the arguments. The integer value stored represents the number of units of time since some 'epoch' time.

Argument 1 - Layout: gives an example format for how the date value should be parsed. The default value for layout is '2006-01-02T15:04:05Z07:00'. Write this same datetime in whatever format your values have. For example, for a traditional MM/DD/YYYY representation, you would use '01/02/2006' for layout.

Argument 2 - Epoch: The 'zero' timestamp from which the int values are calculated. Written using the same layout as specified by argument 1.

Argument 3 - Unit: The time unit to store. If the unit is a day, then a value of 17 means 17 days since the epoch. Unit may be `"d"`, `"h"`, `"m"`, `"s"`, `"ms"`, `"us"`, `"ns"` or `"c"` for custom. If `"c"` is used, argument 4 specifies the customer duration.

Argument 4 - Custom Unit: A 'duration' value which specifies a custom time unit. Accepts values like "6h" for 6 hours, "1m30s" for 1 minute and 30 seconds. Valid time units are "ns", "us", "ms", "s", "m", "h".


### RecordTime
Example:
`time__RecordTime_2006-01-02_2018-03-04_d`

RecordTime is for a timestamp in a record which applies to the whole record. Any field in the record which will be stored as a 'time' field in FeatureBase will have this time associated with its value. Note that using this field type alone will not explicitly create a field in FeatureBase.

Argument 1: Layout: gives an example format for how the date value should be parsed. The default value for layout is '2006-01-02T15:04:05Z07:00'. Write this same datetime in whatever format your values have. For example, for a traditional MM/DD/YYYY representation, you would use '01/02/2006' for layout.

Argument 2 - Epoch: The 'zero' timestamp from which the int values are calculated. Written using the same layout as specified by argument 1.

Argument 3 - Unit: the incoming value will be interpreted as a duration with this Unit, starting at the configured Epoch. Can be `"d"`, `"h"`, `"m"`, `"s"`, `"ms"`, `"us"`, `"ns"`, for day, hour, minute, second, millisecond, microsecond, or nanosecond respectively. Defaults to `"s"`.


### Timestamp
Example:
`purchase_date__Timestamp_s_2006-01-02T15:04:05Z07:00_2018-03-04T15:04:05Z_ms`

Timestamp fields are implemented internally the same way as integer fields and store the number of time units (e.g. seconds) since an epoch. By default, the time unit is in seconds and the epoch is midnight, January 1, 1970 UTC. Adjusting the granularity and epoch can reduce the storage requirements and computation time when processing records.

Argument 1 - Granularity: the resolution at which the incoming values will be stored. Allowed values are `s`, `ms`, `us`, `ns`. Defaults to `"s"`.

Argument 2 - Layout: gives an example format for how the date value should be parsed. The default value is RFC3339Nano: '2006-01-02T15:04:05.999999999Z07:00'. Write this same datetime in whatever format your values have. Refer to [Go's format docs](https://golang.org/pkg/time/#pkg-constants).

Argument 3 - Epoch: The 'zero' timestamp from which the int values are calculated. Written using the same layout as specified by argument 2.

Argument 4 - Unit: the incoming value will be interpreted as a duration with this Unit, starting at the configured Epoch. Can be `"d"`, `"h"`, `"m"`, `"s"`, `"ms"`, `"us"`, `"ns"`, for day, hour, minute, second, millisecond, microsecond, or nanosecond respectively. Defaults to `"s"`.


### StringArray
Example:
`tags__StringArray_`

StringArray is similar to the `String` type, but expects multiple values in a single record. Each value will be set in the corresponding row of the FeatureBase 'set' or 'time' field. To retrieve Array values from a CSV file, the data within the CSV column should be a comma separated list of array values enclosed in double quotes, e.g. `"Georgia,Texas,Oregon"`.

Argument 1 — Time Quantum: If this argument is provided, the field will be a "time" field rather than "set". "time" fields work similarly to "set" fields but each value can have a coarse grained timestamp associated with it. The granularity is controlled by this argument and can be anything from yearly down to hourly. See the [FeatureBase Data Model docs](/concepts/data-modeling-overview) for more information about time fields.

### IDArray
Example:
`links__IDArray_`

IDArray is similar to the `ID` type, but expects multiple values in a single record. Each value will be set in the corresponding row of the FeatureBase 'set' or 'time'  field. To retrieve Array values from a CSV file, the data within the CSV column should be a comma separated list of values enclosed in double quotes, e.g. `"10,23,18"`.

Argument 1 — Time Quantum: If this argument is provided, the field will be a "time" field rather than "set". "time" fields work similarly to "set" fields but each value can have a coarse grained timestamp associated with it. The granularity is controlled by this argument and can be anything from yearly down to hourly. See the [FeatureBase Data Model docs](/concepts/data-modeling-overview) for more information about time fields.

### Ignore
Example:
`uuid__Ignore`

Ignore the value in this field. If you have values you don't want to ingest, but it is inconvenient to remove them ahead of time, you can use the Ignore field to explicitly ignore them.
