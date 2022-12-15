---
title: IDSET data type
---

IDSET is a FeatureBase datatype used with `timeQuantum` and `ttl` constraints.

## API syntax

```
IDSET [TIMEQUANTUM {value} [TTL '{value}}']]
```

## Arguments

| Argument | Description |
|---|---|
| IDSET | Data type used where there is a need to set multiple ID values for a single column |
{% include /sql-preview/timequantum-ttl-args.md %}

## Additional information

The IDSET data type:
* has a `set` internal data type
* one standard view by default unless a timeQuantum is set.
* is used for:
  * grouping by
  * searching for discrete values

NOTE: Use the INT data type to perform range queries using `<` or `>`

{% include /sql-preview/timequantum-additional.md %}

{% include /sql-preview/ttl-additional.md %}
