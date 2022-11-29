---
title: timeQuantum and TTL (Time To Live) Constraints
---

`timeQuantum` and `ttl` constraints are used with `IDSET` and `STRINGSET` data types.

A `timeQuantum` is a special constraint that allow users to track when values are set for records by passing a `"recordTime"` timestamp in addition to the value itself.

A `ttl` determines when `timeQuantum` views are deleted.

## Syntax

```

```

## Arguments

| Argument | Description | Further information |
|---|---|---|
| index_name |  | [naming standard](#naming-standard) |
| field_name |  | [naming standard](#naming-standard) |
| type |  |  |
| timeQuantum | Create a view on IDSET and STRINGSET columns that allow range queries down to the specified time. timeQuantum associates a time with each value in the column. |  |
| YMDH | Granularity of time represented by Year, Month, Day, Hour |
| "ttl" | Used to reduce the growth of a data footprint by deleting older views. |  |
| <integer> | integer value paired with the time unit. Defaults to `0s` |  |
| time_unit | `h` (hours), `m` (minutes), `s` (seconds) |  |

## Additional information

* IDSET and STRINGSET Data has one standard view by default unless a timeQuantum is set.

### Naming standard

{% include /concepts/object-naming-standard.md %}

### timeQuantum

`timeQuantum` creates a view of your data based on the specified time granularity.

`timeQuantum` is used when:
* times need to be associated with column data for query purposes
* database space is not at a premium
* querying times directly rather than filtering

IMPORTANT: time-stamps are required on all records to be imported to IDSET or STRINGSET `timeQuantum` columns.

### `timeQuantum` time granularity

Time granularity allows for lower latency queries at the cost of increased storage. It's represented by one or more values:

* Y = Year
* M = Months
* D = Days
* H = Hours

Values can be omitted but not skipped. For example:

| Value | Result |
|---|---|
| YMDH | Invalid value - Day and H in wrong order |
| YDH | Invalid value - Cannot skip values in the sequence |
| YM | Valid |
| DH | Valid |

Queries run on mismatched time granularities are slower but will function correctly. For example:

| time granularity | Query on | Result speed |
|---|---|---|
| YM | YM | fast query |
| YM | D | slow |

### ttl - time to live

WARNING: `ttl` should not be used if you require complete and consistent historical data.

`ttl` enables the deletion of time views created by the `timeQuantum` constraint and are represented as an integer value with a suffix:

* s = seconds
* m = minutes
* h = hours

For example:

| ttl  | Result | "ttl":"1s"
|---|---|
| "ttl":"0s" | timeQuantum views are not deleted (default value) |
| "ttl":"7200s" | 720 seconds or 2 hours |
| "ttl":"30m" | 30 minutes |
| "ttl":"1h" | Recommended `ttl` value to improve results |
| "ttl":"60second" | incorrect time unit that generates `error: unknown unit` |

Querying `ttl`
* always use closed time ranges on your queries if you need to guarantee that results older than the TTL don't show up

`ttl` deletion:
  * runs when FeatureBase starts and every hour afterwards
  * is not guaranteed to run at a specific time

## Examples

### When are time quantums deleted? (not a great title but all I've got)

```
syntax to represent what's going on in explanation below
...
..."ttl":"30d"
```

Where:
* a column `timeQuantum` `time interval` is set to `YMD`
* "ttl":"30d"

| `timeQuantum` view date | Deleted on |
|---|---|
| 2022-09-02 | 2022-10-02 |
| 2022-09 | 2022-10-30 |
| 2022 | 2023-01-30 |

### Query a time quantum

```
syntax to represent how the timeQuantum is applied to the column and table
```

Where:
* `customer` table has column `stores_visited`
* `stores_visited` column has `timeQuantum` views

Customer query to return all `stores_visited` between the following dates:

```
[customer]Extract(All(), Rows(stores_visited,from='2018-08-31', to='2022-02-18'))
```
