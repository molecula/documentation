---
title: SQL Overview
---

| | |
|-|-|
| **ℹ️NOTE** | This page contains information that only applies to SQL Preview functionality. Additionally, this page represents a work in progress that is subject to frequent changes. |

---

## SQL is a Preview Feature

By default, SQL is disabled in FeatureBase. To enable the feature, FeatureBase needs to be configured with the `sql.endpoint-enabled` option. For more information, see [FeatureBase Configuration](/setting-up-featurebase/enterprise/featurebase-configuration)

When this option is enabled, FeatureBase supports sql queries over a http endpoint and at the command line.

## Queries at the command line

To query FeatureBase on the same host at the command line:

```
featurebase cli
```

You should then see something like:

```
FeatureBase CLI (v3.20.0-14-g0a73abbb)
Type "exit" to quit.

fbsql>
```

You can then enter queries, seperated by the `;` character.

The get help on the FeatureBase cli, type:

```
featurebase cli --help
```

## Queries over the http endpoint

### Endpoint

`POST /sql`

The sql query text is passed in the body of the request, with a `Content-Type` of `text/plain`.


#### Result

``` request
curl -XPOST localhost:10101/sql -d 'select 1'
```
``` response
{
  "schema": {
    "fields": [
      {
        "name": "",
        "type": "INT"
      }
    ]
  },
  "data": [
    [
      1
    ]
  ],
  "exec_time": 16412581
}
```

#### Errors

If an error occurs during query execution, the request will still succeed, even though the body may contain an error.

``` request
curl -XPOST localhost:10101/sql -d 'select foo'
```
``` response
{
  "error": "[1:8] column 'foo' not found"
}
```

