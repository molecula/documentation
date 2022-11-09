---
title: Time To Live (TTL)
---

TTL stands for time to live. TTL allows you to delete time views. Views are only deleted when the end of the time range the view represents is older than the TTL. TTL is only an option for `IDSET` and `STRINGSET` columns with time quantums set.

## Before you begin

* [Learn about data modeling](/concepts/data-modeling-overview)
* [Learn about time quantums](/concepts/time-quantums)

## When should you use TTL?

When you don't care about older views and want to reduce the growth of your data footprint over time.

## When should you avoid TTL?

When you want to keep every view across your full historical data or you are looking for a solution that demands consistent removal of views.

## How do you use TTL?

TTL holds the duration for the views created by FeatureBase based on:

* the time quantum time and the current time
* the times associated with the data in time quantum views

Once the TTL duration exprires, those views will be deleted.

## Time units

Allowed time units for TTL are `h`, `m`, `s`. Time unit is required. Default value is `0s`.

<!--
Actually we allow more but are aligning to how they are deleted and removing small units.
Allowed time units for TTL are `h`, `m`, `s`, `ms`, `us`, `ns`. Time unit is required. Default value is `0s`.
-->

Example:
- "ttl":"1s" is equal to 1 second.
- "ttl":"7200s" is equal to 720 seconds (2 hours).
- "ttl":"72h" is equal to 72 hours.
- "ttl":"6000second" will return error `error: unknown unit "second" in duration "6000second"`.

If TTL's value is `0s` (default value), the views created based on time quantum will not be deleted.

## TTL removal

TTL removal is set to run when FeatureBase starts and every hour thereafter. This means view deletion is eventually consistent.

TTL removal is, in general, not guaranteed to run at any particular time, and you should always use closed time ranges on your queries if you need to guarantee that results older than the TTL don't show up.

For this reason, while you may specify times below an hour, it is recommended to use a TTL of one hour or more.

## What is happening when you use TTL?

A process runs periodically that looks at the views and the current time to see if they have exceeded the configured TTL. Each view may be deleted at a different time based on its granularity and how long it's been since the end of that view's time range.

The rule is, if the end of the time range represented by the view is older than the TTL, it can be deleted.

### Example of TTL

Acolumn with `YMD` has four views for 2022-09-02 and TTL is set to `30d`
* 2022
* 2022-09
* 2022-09-02 and standard

This means that the following views are deleted:
* 2022-09-02 view is cleared after 30 days (roughly on 2022-10-02),
* 2022-09 view is cleared on October 30, 2022
* 2022 view is deleted January 30, 2023.


## Create a new field using TTL

```
curl -XPOST http://localhost:10101/index/**test_ttl_index**/field/**data_ttl** -d'{ "options": {"type":"time", "timeQuantum":"YMDH", **"ttl":"24h"**}}'
```

## Update an existing field with TTL

```
curl -XPATCH http://localhost:10101/index/**test_ttl_index**/field/**data_ttl** -d'{ **"option": "ttl", "value": "24h"**}
```

## Further information

* [Case Study: Data Modeling](/concepts/case-study-data-modeling)
