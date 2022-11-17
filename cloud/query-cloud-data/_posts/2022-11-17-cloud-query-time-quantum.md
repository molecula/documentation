---
title: How do I query the timestamp of a timeQuantum constraint?
---

* timeQuantum and ttl row queries are only supported by PQL queries.
* timestamps must be passed with each record for timeQuantum columns.
* Use closed time ranges in queries to guarantee results older than the `ttl` are not returned
