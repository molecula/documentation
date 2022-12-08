---
title: TIMESTAMP data type
---

Timestamp is a date-time data type used with `timeunit` and `epoch` constraints.

## Syntax

```
TIMESTAMP [TIMEUNIT] [EPOCH]
```

## Arguments

| Argument | Description | Further information |
|---|---|---|
| TIMESTAMP | Time and date data type used for time series analysis | [Time stamp](https://en.wikipedia.org/wiki/Timestamp) |
| TIMEUNIT | The time unit in which to store a timestamp that defaults to second `s | See [TIMEUNIT values](#timeunit-values) |
| EPOCH | The epoch which timestamps will be stored relative to. This is represented as a RFC339 time stamp string | See [Epoch values](#epoch-values) |

## Additional information

### TIMEUNIT values

| Unit | Declaration |
|---|---|
| hours | `h` |
| minutes | `m` |
| seconds (default) | `s` |
| milliseconds | `ms` |
| microseconds | `us` |
| nanoseconds | `ns` |

### EPOCH values

* Represented as an [RFC339 time stamp string](https://www.rfc-editor.org/rfc/rfc3339)

| Timestamp | Example | Further information |
|---|---|---|
| Time zone | 1980-11-30T14:20:28.000+07:00 | [Time zone](https://en.wikipedia.org/wiki/Time_zone) |
| Zulu (military) time | 1980-11-30T14:20:28.000Z | [Zulu Time Zone](https://www.timeanddate.com/time/zones/z) |

## Examples
