---
title: FeatureBase Time To Live reference
---

TTL (Time To Live) is an field option for time fields. It holds the duration for the views created by FeatureBase based on the time quantum. Once the TTL duration expires, those views will be deleted. Time quantum is required for TTL to function.

## Adapt content

/concepts/time-to-live


FROM /cloud/cloud-data-modeling/data-types

data types: IDSET, STRINGSET  

An optional time to live (TTL) argument can be passed that will delete old values for a record after that period of time passes.

TTL deletion runs when FeatureBase starts and every hour thereafter. You can specify the TTL by specifying an integer and a time unit from hours to nanoseconds (<integer>+`h`, `m`, `s`, `ms`, `us`, `ns`).

A TTL of `72h` will retain values for 72 hours before deletion. A TTL of `0s` indicates data will never be deleted.

, TTL (`0s`)

## Get support

{% include /docs/get-support-source.md %}
