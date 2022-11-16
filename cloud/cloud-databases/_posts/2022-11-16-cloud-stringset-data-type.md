---
title: STRINGSET data type
---

## Syntax

```

```

## Arguments

| Argument | Description | Further information |
|---|---|---|
| STRINGSET | Data type used to set multiple STRING values for a single column. |
| timeQuantum | Constraint not set by default | [timeQuantum constraint](/) |
| ttl | Constraint that modifies timeQuantum and defaults to zero seconds `0s` | [ttl constraint](/) |

## Additional information

* STRINGSET data has one standard view by default unless a timeQuantum is set
* STRINGSET is used when:
  * grouping by
  * searching for discrete values

## Example

Track all the store IDs a customer has visited

```
CODE EXAMPLE
```
