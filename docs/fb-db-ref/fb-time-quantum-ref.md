---
title: Time quantum reference
---

Source: /concepts/2022-11-08-time-quantums

Whole page of material there.

Source: /cloud/cloud-data-modeling/2022-04-01-data-types

data types: IDSET, STRINGSET  

Time quantums are special constraints that allow users to track when values are set for records by passing a `"recordTime"` timestamp in addition to the value itself. This is unique to SETs because the datatype supports multiple values that can be updated over time.  Tracking is supported by hour (`H`), day (`D`), month (`M`), or year (`Y`) or any combination of the four. Setting these allows for lower latency queries depending on the period of time you are querying over but increase storage. For example, If you plan to have queries with a range over multiple months, `MD` is the best option, but if you will be querying over only a couple of days, `D` will be preferred.

TIMEQUANTUM (Not set by default)
