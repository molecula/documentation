---
title: Time Quantums And TTL
---

# Time Quantums
## What are time quantums?

A time quantum is a feature for `IDSET` and `STRINGSET` type columns that allows you to associate a time (or multiple times) with each value in the column. Setting a time quantum creates views on the column that allow range queries down to the time granularity specified. You can think of a view as a rollup of your data based on the granularity of time you specify. If no time quantums are set, your data has one "standard" view by default.

## When should you use time quantums?

You should use time quantums when you want to associate a time with each value in `IDSET` and `STRINGSET` type columns, in addition to querying by that time.

## When should you avoid time quantums? 

You should avoid time quantums if you don’t have a time you want to associate with a value, if you aren't interested in deleting values over time to save space, if you are trying to count the number of distinct time quantums associated to a particular value, and if you are looking to pull out time values as opposed to filtering by them.

## How do you use time quantums?

When creating a column, you specify the granularity of time you want views created for. FeatureBase supports hour (`H`), day (`D`), month (`M`), or year (`Y`) or any combination of the four (in descending order with no gaps in time. i.e. `YMD` but not `YD`). Setting these allows for lower latency queries depending on the period of time you are querying over, but at the cost of increased storage. For example, If you plan to have queries with a range of multiple months, `MD` is the best option, but if you will be querying over only a couple of days, `D` will be preferred. Note you can set just `D` and still query over multiple months, but it will not be as fast as using `MD`.

Once created, a timestamp must be passed with each record during ingest that will be associated with all time quantum columns. Note this means you can only pass one time for all the time quantums in a record. For more information on configuring ingest, see the appropriate section in "Data Ingestion" navigation.

Querying using time quantums is only supported in (PQL Rows Queries)[/reference/data-querying-ref/pql/read/rows]. You can pass a timestamp in the `to` and `from` arguments. In the example below, the `customer` table will pull back the customer IDs and what stores they visited between `2018-08-31` and `2022-02-18`

```
[customer]Extract(All(), Rows(stores_visited,from='2018-08-31', to='2022-02-18'))
```

You can associate multiple times with each value, so a value only has to exist in one view to be returned. This will not return the value twice and will only be counted once. You cannot return the underlying timestamps associated with each value.

## What is happening when you use time quantums? 

Whenever a record with time quantums is ingested, a view is created for each level of granularity specified. This is essentially a copy of the column over a specific time range. If `YMDH` is specified and the time `2018-08-31T22:30:00Z` is ingested, a time view will exist for `2018`, `2018-08`, `2018-08-31`, and `2018-08-31T22`. This means data which has times for every hour for two days (say May 2nd and 3rd) in a column with `YMDH` time quantums configured will have 48+2+1+1+1 views (53) in total. 48 hours, 2 days, 1 month, 1 year, and the standard view. 

# TTL (Time To Live)
## What is TTL?
TTL stands for time to live. TTL allows you to delete time views. Views are only deleted when the end of the time range the view represents is older than the TTL. TTL is only an option for `IDSET` and `STRINGSET` columns with time quantums set.

## When should you use TTL?

When you don't care about older views and want to reduce the growth of your data footprint over time.

## When should you avoid TTL?

When you want to keep every view across your full historical data or you are looking for a solution that demands consistent removal of views.

## How do you use TTL?

TTL holds the duration for the views that will be used to delete them based on the time quantum time and the current time. It does not care when the data is ingested, it only looks at the times associated with the data in time quantum views. Once the TTL duration expires, those views will be deleted. If TTL's value is 0s (default value), the views created based on the time quantum will not be deleted.

<!--
Actually we allow more but are aligning to how they are deleted and removing small units.
Allowed time units for TTL are `h`, `m`, `s`, `ms`, `us`, `ns`. Time unit is required. Default value is `0s`.

-->

Allowed time units for TTL are `h`, `m`, `s`. Time unit is required. Default value is `0s`.

Example:
- "ttl":"7200s" is equal to 720 seconds (2 hours).
- "ttl":"72h" is equal to 72 hours.
- "ttl":"6000second" will return error `error: unknown unit "second" in duration "6000second"`.

TTL removal is set to run when FeatureBase starts and every hour thereafter. This means view deletion is eventually consistent. TTL removal is, in general, not guaranteed to run at any particular time, and you should always use closed time ranges on your queries if you need to guarantee that results older than the TTL don't show up. For this reason, while you may specify times below an hour, it is recommended to use a TTL of one hour or more.

## What is happening when you use TTL?

A process runs periodically that looks at the views and the current time to see if they have exceeded the configured TTL. Each view may be deleted at a different time based on its granularity and how long it's been since the end of that view's time range. For Example:

A column with `YMD` has four views for 2022-09-02 (2022, 2022-09, 2022-09-02 and standard) with TTL set to `30d`. The 2022-09-02 view is cleared after 30 days (roughly on 2022-10-02), the 2022-09 view is cleared on October 30, 2022, and the 2022 view is deleted January 30, 2023.

The rule is, if the end of the time range represented by the view is older than the TTL, it can be deleted.
