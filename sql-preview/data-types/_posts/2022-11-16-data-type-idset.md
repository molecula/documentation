---
title: IDSET data type
---

IDSET is a FeatureBase datatype used with `timeQuantum` and `ttl` constraints.

## API syntax

```
IDSET
```

## Arguments

| Argument | Description |
|---|---|
| IDSET | Data type used where there is a need to set multiple ID values for a single column |
{% include /sql-preview/timequantum-ttl-args.md %}

## Additional information

* IDSET data has one standard view by default unless a timeQuantum is set
* IDSET is used for:
  * grouping by
  * searching for discrete values
* Use the INT data type to perform range queries using `<` or `>`

{% include /sql-preview/timequantum-additional.md %}

{% include /sql-preview/ttl-additional.md %}

## Further information

* [Time Quantum and Time to Live constraint](/sql-preview/data-types/constraint-timequantum-ttl)
