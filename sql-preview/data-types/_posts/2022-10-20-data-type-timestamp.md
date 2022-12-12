---
title: TIMESTAMP data type
---

Timestamp is a date-time data type used with `timeunit` and `epoch` constraints.

## Syntax

```
TIMESTAMP [TIMEUNIT {value}] [EPOCH {value}]
```

## Arguments

| Argument | Description | Further information |
|---|---|---|
| TIMESTAMP | Time and date data type used for time series analysis | [Time stamp](https://en.wikipedia.org/wiki/Timestamp) |
| TIMEUNIT | The time unit in which to store a timestamp that defaults to second `s` | See [TIMEUNIT values](#timeunit-value) |
| EPOCH | The epoch which timestamps will be stored relative to. This is represented as [RFC339 time stamp string](https://www.rfc-editor.org/rfc/rfc3339). Defaults to the [Unix epoch](https://www.unixtutorial.org/unix-epoch/) | See [Epoch values](#epoch-value) |

## Additional information

### TIMEUNIT value

| Unit | Declaration |
|---|---|
| hours | `h` |
| minutes | `m` |
| seconds (default) | `s` |
| milliseconds | `ms` |
| microseconds | `us` |
| nanoseconds | `ns` |

### EPOCH value

The epoch which timestamps should be relative to. The value may specify one of the following:

| Timestamp | Example | Further information |
|---|---|---|
| Unix (default) | 1970-01-01T00:00:00Z | [Unix epoch](https://www.unixtutorial.org/unix-epoch/) |
| Time zone | 1980-11-30T14:20:28.000+07:00 | [Time zone](https://en.wikipedia.org/wiki/Time_zone) |
| Zulu (military) time | 1980-11-30T14:20:28.000Z | [Zulu Time Zone](https://www.timeanddate.com/time/zones/z) |
