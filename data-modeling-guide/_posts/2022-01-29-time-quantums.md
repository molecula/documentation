---
title: Time Quantums And TTL
---

# Time Quantums
## What are time quantums?

A time quantum is a feature for `IDSET` and `STRINGSET` type columns that allows you to associate a time (or multiple times) with each value in the column. Setting a time quantum creates views on the column that allow range queries down to the time granularity specified. You can think of a view as a rollup of your data based on the granularity of time you specify. If no time quantums are set, your data has one "standard" view by default.

## When should you use time quantums?

You should use time quantums when you want to associate a time with each value in `IDSET` and `STRINGSET` type columns, in addition to querying by that time.

## When should you avoid time quantums? 

You should avoid time quantums if you don’t have a time you want to associate with a value, you aren't interested in deleting values over time to save space, and if you are looking to pull out time values as opposed to filtering by them.

## How do you use time quantums?

When creating a column, you specify the granularity of time you want views created for. FeatureBase supports hour (`H`), day (`D`), month (`M`), or year (`Y`) or any combination of the four (in descending order with no gaps in time. i.e. `YMD` but not `YD`). Setting these allows for lower latency queries depending on the period of time you are querying over, but at the cost of increased storage. For example, If you plan to have queries with a range of multiple months, `MD` is the best option, but if you will be querying over only a couple of days, `D` will be preferred. Note you can set just `D` and still query over multiple months, but it will not be as fast as using `MD`.

Once created, a timestamp must be passed with each record during ingest that will be associated with all time quantum columns. Note this means you can only pass one time for all the time quantums in a record. For more information on configuring ingest, see the appropriate section in "Data Ingestion" navigation.

Querying using time quantums is only supported in (PQL Rows Queries)[/reference/data-querying-ref/pql/read/rows]. You can pass a timestamp in the `to` and `from` arguments. In the example below, the `customer` table will pull back the customer IDs and what stores they visited between `2018-08-31` and `2022-02-18`

```
[customer]Extract(All(), Rows(stores_visited,from='2018-08-31', to='2022-02-18'))
```

You can associate multiple times with each value, so a value only has to exist in one view to be returned. This will not return the value twice and will only be counted once. You cannot return the underlying timestamps associated with each value.

## What is happening when you use time quantums? 

Whenever a record with time quantums is ingested, a view is created for each level of granularity specified. This is essentially a copy of the column over a specific time range. If `YMDH` is specified and the time `2018-08-31T22:30:00Z` is ingested, a time view will exist for `2018`, `2018-08`, `2018-08-31`, and `2018-08-31T22`. This means data accounting for every hour for two days will have 48 views for each hour.

# TTL (Time To Live)
## What is TTL?
TTL stands for time to live. TTL allows you to delete time views. Views are only deleted when the end of the time range passes TTL. TTL is only an option for `IDSET` and `STRINGSET` columns with time quantums set.

## When should you use TTL?

When you don't care about older views and want to reduce your datafootprint over time.

## When should you avoid TTL?

When you want to keep every view across your full historical data or you are looking for a solution that demands consistent removal of views.

## How do you use TTL?

TTL holds the duration for the views created by FeatureBase based on the time quantum and the current time. This means it deletes based on the value of timestamp associated with the value and the current time. It does not look at when a time is associated with a value. Once the TTL duration expires, those views will be deleted. If TTL's value is 0s (default value), the views created based on the time quantum will not be deleted.

Allowed time units for TTL are `h`, `m`, `s`, `ms`, `us`, `ns`. Time unit is required. Default value is `0s`.

Example:
- "ttl":"1s" is equal to 1 second.
- "ttl":"72h" is equal to 72 hours.
- "ttl":"72second" will return error `error: unknown unit "second" in duration "72second"`.

TTL removal is set to run when FeatureBase starts and every hour thereafter. This means view deletion is eventually consistent.

## What is happening when you use TTL?

A process runs every hour that looks at the views and the current time to see if it has exceeded the TTL set. Each time granularity uses slightly different rules that lead to eventually consistent deletion. For Example:

A column with `YMD` has three views for 9/2/2022 with TTL set to `30d`. The 9/2/2022 view is cleared after 30 days, the 9/2022 view is cleared at the end of 10/2022, and the 2022 view is deleted at the end of january 2023.  30 days passed at the end of the view. if the end of this view is past current time, delete.