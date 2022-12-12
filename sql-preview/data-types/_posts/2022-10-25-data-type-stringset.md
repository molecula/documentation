---
title: STRINGSET data type
---

STRINGSET is a FeatureBase datatype used with `TIMEQUANTUM` and `TTL` (Time To Live) constraints.

## Syntax

```
STRINGSET [TIMEQUANTUM {value} [TTL '{value}}']]
```

## Arguments

| Argument | Description |
|---|---|
| STRINGSET | Data type used to set multiple STRING values for a single column. |
{% include /sql-preview/timequantum-ttl-args.md %}

## Additional information

* STRINGSET data has one standard view by default unless a timeQuantum is set
* STRINGSET is used when:
  * grouping by
  * searching for discrete values

{% include /sql-preview/timequantum-additional.md %}

{% include /sql-preview/ttl-additional.md %}
