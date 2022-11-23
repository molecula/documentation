---
title: IDSET data type
---

IDSET is a FeatureBase datatype used with `timeQuantum` and `ttl` constraints.

## API syntax

```
IDSET...
```

## Arguments

| Argument | Description | Further information |
|---|---|---|
| IDSET | Data type used where there is a need to set multiple ID values for a single column |

## Additional information

* IDSET data has one standard view by default unless a timeQuantum is set
* IDSET is used for:
  * grouping by
  * searching for discrete values
* Use the INT data type to perform range queries using `<` or `>`

## Example

Track all the store IDs a customer has visited

```
CODE EXAMPLE
```

## Further information

* [Time Quantum and Time to Live constraint](/cloud/cloud-data-types/cloud-timequantum-ttl-constraint)