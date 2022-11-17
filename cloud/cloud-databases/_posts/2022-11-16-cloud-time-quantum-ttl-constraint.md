---
title: timeQuantum and TTL (Time To Live) Constraints
---

## Syntax

```
curl -XPOST http://localhost:10101/index/**[index_name]**/field/**field_name** -d'{ "options": {"type":"time", "timeQuantum":"YMDH", **"ttl":">integer>time_unit"**}}'
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

timeQuantum creates a view of your data based on the specified time granularity.

timeQuantum is used when:
* times need to be associated with column data for query purposes
* database space is not at a premium
* querying times directly rather than filtering

### Time granularity

Time granularity allows for lower latency queries at the cost of increased storage. For example:
* set MD for queries that include a range of months
* set D for queries that include a small number of days

You can omit but not skip time granularity.
* YM is valid
* MS is invalid

Queries run on mismatched time granularities are slower but will function correctly. For example: YM time granularity then query on days.

### ttl

* ttl enables the deletion of time views where a time range exceeds the stated Time To Live.
* ttl should not be used if you require complete and consistent historical data.
* time_units
  * ttl of 0s (default value) indicates views created on the timeQuantum will not be deleted
  * FeatureBase recommends using a ttl of one hour or more to improve results.
  * `error: unknown unit` is generated if an incorrect time_unit is used (e.g., `"ttl":"60second"`)

* TTL deletion
  * runs when FeatureBase starts and every hour thereafter to make view deletion consistent.
  * is not guaranteed to run at a specific time.

## Examples

### TTL explanation

A column with `YMD` has four views for 2022-09-02 and TTL is set to `30d`
* 2022
* 2022-09
* 2022-09-02 and standard

This means that the following views are deleted:
* 2022-09-02 view is cleared after 30 days (roughly on 2022-10-02),
* 2022-09 view is cleared on October 30, 2022
* 2022 view is deleted January 30, 2023.

### Create a new `ttl` field

```
curl -XPOST http://localhost:10101/index/**test_ttl_index**/field/**data_ttl** -d'{ "options": {"type":"time", "timeQuantum":"YMDH", **"ttl":"24h"**}}'
```

### Update an existing field to apply `ttl`

```
curl -XPATCH http://localhost:10101/index/**test_ttl_index**/field/**data_ttl** -d'{ **"option": "ttl", "value": "24h"**}
```
