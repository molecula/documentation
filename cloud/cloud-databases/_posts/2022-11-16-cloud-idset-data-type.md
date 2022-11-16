---
title: IDSET data type
---

## Syntax

```

```

## Arguments

| Argument | Description | Further information |
|---|---|---|
| IDSET | Data type used where there is a need to set multiple ID values for a single column |
| timeQuantum | Constraint not set by default | [timeQuantum constraint](/) |
| ttl | Constraint that modifies timeQuantum and defaults to zero seconds `0s` | [TTL constraint](/) |

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
