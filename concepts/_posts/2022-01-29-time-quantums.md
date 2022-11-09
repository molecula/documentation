---
title: Time Quantums
---

## Before you begin

* [Learn about data modeling](/concepts/data-modeling-overview-overview)

## What are time quantums?

A time quantum is a feature for `IDSET` and `STRINGSET` type columns that allows you to associate a time (or multiple times) with each value in the column. Setting a time quantum creates views on the column that allow range queries down to the time granularity specified. You can think of a view as a rollup of your data based on the granularity of time you specify. If no time quantums are set, your data has one "standard" view by default.

## When should you use time quantums?

You should use time quantums when you want to associate a time with each value in `IDSET` and `STRINGSET` type columns, in addition to querying by that time.

## When should you avoid time quantums?

You should avoid time quantums if you don’t have a time you want to associate with a value, if you aren't interested in deleting values over time to save space, if you are trying to count the number of distinct time quantums associated to a particular value, and if you are looking to pull out time values as opposed to filtering by them.

## How do you use time quantums?

When creating a column, you specify the granularity of time you want views created for. FeatureBase supports hour (`H`), day (`D`), month (`M`), or year (`Y`) or any combination of the four (in descending order with no gaps in time. i.e. `YMD` but not `YD`). Setting these allows for lower latency queries depending on the period of time you are querying over, but at the cost of increased storage. For example, If you plan to have queries with a range of multiple months, `MD` is the best option, but if you will be querying over only a couple of days, `D` will be preferred. Note you can set just `D` and still query over multiple months, but it will not be as fast as using `MD`.

Once created, a timestamp must be passed with each record during ingest that will be associated with all time quantum columns. Note this means you can only pass one time for all the time quantums in a record. For more information on configuring ingest, see the appropriate section in "Data Ingestion" navigation.

Querying using time quantums is only supported in (PQL Rows Queries)[/pql-guide/read/rows]. You can pass a timestamp in the `to` and `from` arguments. In the example below, the `customer` table will pull back the customer IDs and what stores they visited between `2018-08-31` and `2022-02-18`

```
[customer]Extract(All(), Rows(stores_visited,from='2018-08-31', to='2022-02-18'))
```

You can associate multiple times with each value, so a value only has to exist in one view to be returned. This will not return the value twice and will only be counted once. You cannot return the underlying timestamps associated with each value.

## What is happening when you use time quantums?

Whenever a record with time quantums is ingested, a view is created for each level of granularity specified. This is essentially a copy of the column over a specific time range. If `YMDH` is specified and the time `2018-08-31T22:30:00Z` is ingested, a time view will exist for `2018`, `2018-08`, `2018-08-31`, and `2018-08-31T22`. This means data which has times for every hour for two days (say May 2nd and 3rd) in a column with `YMDH` time quantums configured will have 48+2+1+1+1 views (53) in total. 48 hours, 2 days, 1 month, 1 year, and the standard view.

## Further information

* [Learn about Time To Live](/concepts/time-to-live)
