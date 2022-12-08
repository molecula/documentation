---
title: timeQuantum and TTL (Time To Live) Constraints
---

## Syntax

```
Would be nice to have syntax referring back to the
```

## Arguments

| Argument | Description | Further information |
|---|---|---|
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
* ttl runs when FeatureBase starts and every hour to make view deletion consistent
* ttl is not guaranteed to run at a specific time
* ttl should not be used if you require complete and consistent historical data.

* time_units
  * ttl of 0s (default value) indicates views created on the timeQuantum will not be deleted
  * FeatureBase recommends using a ttl of one hour or more to improve results.
  * `error: unknown unit` is generated if an incorrect time_unit is used (e.g., `"ttl":"60second"`)

#### TTL order of events

This example demonstrates the deletion dates of three views where `ttl:30d`

| Views on column | Date of deletion | Explanation |
|---|---|---|
| 2022 | January 30, 2023 | Date assumed to be end of 2022 |
| 2022-09 | October 30, 2022 | Date assumed to be end of September |
| 2022-09-02 | 2022-10-02 | Deletion after 30 days as intended |
