---
title: Shard MaxShard reference
---


## Description

The total number of shards allocated to handle the current set of records.

This value is important for all nodes to efficiently distribute queries.

MaxShard can be altered in FILENAME/MENUITEM

## Syntax

```
MaxShard = n
```

## Arguments

| Argument | Description |
|---|---|
| MaxShard | zero-indexed value where MaxShard=6 means there are five Shards available. |


## Additional information

* MaxShard is zero-indexed, so if an index contains six shards, its MaxShard will be 5.

## Examples


## Further information


## Get support

{% include /docs/get-support-source.md %}
