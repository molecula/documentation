---
id: monitoring
title: Monitoring
sidebar_label: Monitoring
---

## Metrics

All Molecula components expose metrics via a [Prometheus](https://prometheus.io)
compatible endpoint. 

Exposed metrics are described for each component below.

### Metric naming conventions:

- Valid metric names match the regular expression `[a-zA-Z_:][a-zA-Z0-9_:]*`. The colon character is reserved for [recording rules](https://prometheus.io/docs/practices/rules/) and is avoided otherwise.
- Format: `[namespaceprefix]_[metric_description]_[units]`. Example: `ingester_csv_deleter_rows_added_total` with namespace `ingester_csv`, metric name `deleter_rows_added`, and "unit" `total`, indicating a counter.
- Molecula uses a different namespace for each component, for example `featurebase` and something starting with `ingester` for various Ingester binaries.
- `snake_case`, not `camelCase`
- As a rule of thumb, either the sum() or the avg() over all dimensions of a given metric should be meaningful (though not necessarily useful).

For more information, see [Prometheus best practices on naming](https://prometheus.io/docs/practices/naming/), and [this related blog post](https://www.robustperception.io/on-the-naming-of-things).

### Label Descriptions

Some metrics are labeled, with labels following a key-value format. Some of these labels are used with multiple metrics, including the following:

- `index:<indexname>` - FeatureBase index
- `field:<fieldname>` - FeatureBase field
- `node_id:<nodeID>` - FeatureBase node ID

Some metrics are specific to individual components, and described below.

### Ingesters Metrics

| Metric Name                                                           | Description                         |
| -                                                                     | -                                   |
| `[namespaceprefix]_deleter_rows_added_total`                          | count of rows ingested for deletion<br/>(labels: type={packed-bool,set,mutex,bool,int,decimal}) |
| `[namespaceprefix]_ingester_schema_changes_total                      | count of schema changes |
| `[namespaceprefix]_ingester_rows_added_total`                         | count of rows ingested |
| `[namespaceprefix]_batch_import_duration_seconds`                     | per-batch import timing. Timings start from when the <br/>last record was added to the batch and<br/>end when the batch was fully imported.<br/>Prior to Molecula 3.0, this only timed importing processed<br/>batch data, and elided key translation and local processing.<br/>Note that this is reported within go-pilosa. |

where in the case of Ingesters, `[namespaceprefix]` is one of:
- ingester_csv
- ingester_kafka
- ingester_sql

### FeatureBase Metrics

| Metric Name                                                           | Description                         |
| -                                                                     | -                                   |
| `[featurebaseprefix]_create_index_total`                              | count of successful index creations |
| `[featurebaseprefix]_delete_index_total`                              | count of successful index deletions |   
| `[featurebaseprefix]_create_field_total`                              | count of successful field creations |
| `[featurebaseprefix]_delete_field_total`                              | count of successful field deletions |
| `[featurebaseprefix]_delete_available_shard_total`                    | count of successful shard deletions |
| `[featurebaseprefix]_recalculate_cache_total`                         | count of cache recalculations       |
| `[featurebaseprefix]_invalidate_cache_total`                          | count of cache invalidations          |
| `[featurebaseprefix]_invalidate_cache_skipped_total`                  |  count of skipped cache invalidations |
| `[featurebaseprefix]_dirty_cache_total`                               | count of dirty cache |
| `[featurebaseprefix]_rank_cache_length`                               | gauge of cache length |
| `[featurebaseprefix]_cache_threshold_reached_total`                   | count of times cache reaches threshold and trimming is required |
| `[featurebaseprefix]_query_row_total`                                 | count of row queries |
| `[featurebaseprefix]_query_row_bsi_total`                             | count of row queries that operate on a BSI (integer) field |
| `[featurebaseprefix]_set_bit_total`                                   | count of set bits, set by a query (as opposed to an import) |
| `[featurebaseprefix]_clear_bit_total`                                 | count of clear bits, set by a query (as opposed to an import) |
| `[featurebaseprefix]_importing_total`                                 | count of imported set bits, before importing |
| `[featurebaseprefix]_imported_total`                                  | count of imported set bits, after successfully importing (number that actually changed) |
| `[featurebaseprefix]_clearing_total`                                  | count of imported clear bits, before importing |
| `[featurebaseprefix]_cleared_total`                                   | count of imported clear bits, after successfully importing (number that actually changed) |
| `[featurebaseprefix]_snapshot_duration_seconds`                       | timing histogram of the snapshot process |
| `[featurebaseprefix]_block_repair_total`                              | count (labels: primary={true,false}) |
| `[featurebaseprefix]_sync_field_duration_seconds`                     | timing histogram of the field sync process |
| `[featurebaseprefix]_sync_index_duration_seconds`                     | timing histogram of the index sync process |
| `[featurebaseprefix]_http_request_duration_seconds`                   | timing histogram of all http requests. Labels: where, <br/>  - `where` - a value of `internal` indicates an in-cluster request, `external` indicates a request from outside the cluster<br/> - `path` - the path used to make a request. For example, `/index/<index>/query` for an HTTP PQL query request.<br/> - `useragent` - the user agent string used to make a request. For example, `curl/7.54.0`.<br/> - `method` - the method used to make a request. For example, `POST`.<br/> - `slow` - `true` or `false` indicates a "slow query" based on the `long-query-time` configuration option for FeatureBase |
| `[featurebaseprefix]_grpc_request_pql_unary_query_duration_seconds`   | timing histogram of the query processing part of unary GRPC requests |
| `[featurebaseprefix]_grpc_request_pql_unary_format_duration_seconds`  | timing histogram of the result formatting part of unary GRPC requests |
| `[featurebaseprefix]_grpc_request_pql_stream_query_duration_seconds`  | timing histogram of the query processing part of streaming GRPC requests |
| `[featurebaseprefix]_grpc_request_pql_stream_format_duration_seconds` | timing histogram of the result formatting part of streaming GRPC requests |
| `[featurebaseprefix]_maximum_shard`                                   |  gauge of the maximum shard in the index. For indexes which use `keys: true`,<br/>expect to see this around a multiple of 256<br/>due to how keys are partitioned around shards. |
| `[featurebaseprefix]_antientropy_total`                               | count of times the AntiEntropy process runs |
| `[featurebaseprefix]_antientropy_duration_seconds`                    | histogram of duration of AntiEntropy process |

where `[featurebaseprefix]` is either `featurebase` if the [`--future.rename` configuration flag](/reference/featurebase-rename) is set, or `pilosa`.

In addition, metrics are generated for counts of individual query calls. These are identified by the `query` prefix, for example `query_topn_total`. For PQL calls, these include the following queries: `Sum`, `Min`, `Max`, `MinRow`, `MaxRow`, `Count`, `TopN`, `Rows`, `GroupBy`. Note that the query name is represented as lower-case in the metric name. SQL calls may also affect these metrics, depending on SQL->PQL mapping of the particular query.

### Runtime Metrics

These metrics are pulled from the Go language runtime or operating system rather than being generated by FeatureBase itself. Note that these metrics are enabled by setting FeatureBase's configuration variable `metric.poll-interval` to a non-zero value.

| Metric Name                                    | Description                         |
| -                                              | -                                   |
| `[featurebaseprefix]_garbage_collection_total` |  counter                            |
| `[featurebaseprefix]_goroutines`               | gauge                               |
| `[featurebaseprefix]_open_files`               | gauge. FeatureBase can use a large number of open files <br/> depending on the amount of data and the schema. <br/> A sudden jump in the number of open files <br/> could indicate an issue. |
| `[featurebaseprefix]_heap_alloc`               | gauge                               |
| `[featurebaseprefix]_heap_inuse`               | gauge                               |
| `[featurebaseprefix]_stack_inuse`              | gauge                               |
| `[featurebaseprefix]_mallocs`                  | gauge                               |
| `[featurebaseprefix]_frees`                    | gauge                               |

where `[featurebaseprefix]` is either `featurebase` if the [`--future.rename` configuration flag](/reference/featurebase-rename) is set, or `pilosa`.

### Transaction Metrics
| Metric Name                                         | Description                              |
| -                                                   | -                                        |
| `[featurebaseprefix]_transaction_start`             | count of started transactions            |
| `[featurebaseprefix]_transaction_end`               | count of ended transactions              |
| `[featurebaseprefix]_transaction_blocked`           | count of blocked transactions            |
| `[featurebaseprefix]_transaction_exclusive_request` | count of exclusive transaction requests  |
| `[featurebaseprefix]_transaction_exclusive_active`  |  count of active exclusive transactions  |
| `[featurebaseprefix]_transaction_exclusive_end`     |  count of ended exclusive transactions   |
| `[featurebaseprefix]_transaction_exclusive_blocked` |  count of blocked exclusive transactions |

where `[featurebaseprefix]` is either `featurebase` if the [`--future.rename` configuration flag](/reference/featurebase-rename) is set, or `pilosa`.

### Query Metrics (not implemented)
| Metric Name                             | Description          |
| -                                       | -                    |
| `[featurebaseprefix]_pql_queries_total` | count of PQL queries |
| `[featurebaseprefix]_sql_queries_total` | count of SQL queries |

where `[featurebaseprefix]` is either `featurebase` if the [`--future.rename` configuration flag](/reference/featurebase-rename) is set, or `pilosa`.

### Prometheus Configuration

Reporting metrics to Prometheus is enabled by default for Ingesters (at :9093/metrics); `host:port` can be specified with the `--stats` flag.

For FeatureBase, reporting must be enabled, as detailed on the [Configuration page](/reference/featurebase-configuration#metric-service). E.g.

```toml
[metric]
  service = "prometheus"
  poll-interval = "0m15s"
```


Below is an example configuration excerpt for Prometheus (the `scrape_configs` section), using the default reporting settings for FeatureBase and Ingesters:

```yaml
  - job_name: 'featurebase'
    static_configs:
    - targets: ['localhost:10101', 'localhost:10102', 'localhost:10103']

  - job_name: 'ingester'
    static_configs:
    - targets: ['localhost:9093']
```

## Logging

All Molecula components log to standard error by default and can be configured to log to a file. When logging to a file, Molecula components will re-open the log file on receipt of the HUP signal. See [How To Set Up Log Rotation](/how-tos/set-up-log-rotation) for more information.

## Tracing

Molecula supports tracing via the [OpenTracing](https://opentracing.io/) standard. With this, tools such as [Jaeger](https://www.jaegertracing.io/) can be used to store and visualize trace data.


## External Diagnostics

Depending on contract details, Molecula may require the ability to "phone home" limited diagnostic information about its usage for billing, debugging, and license enforcement purposes. The details of connectivity and particulars of the data involved will be agreed upon prior to deployment.


## Health Checks


#### FeatureBase

FeatureBase's `/status` endpoint will respond with a JSON document describing the overall state of the cluster (NORMAL, DEGRADED, STARTING, DOWN, or RESIZING), along with some information about each node.


#### Other Components

To check the health of other Molecula components, use their Prometheus metrics endpoint.

## Scaling

### FeatureBase

To scale FeatureBase up, add a node to the cluster and provision it similarly to the others (with its own bind), and make sure it has gossip seeds which are already in the cluster. It will automatically join the cluster and FeatureBase will initiate a resize operation to balance the data in the cluster.

To scale FeatureBase down, decide which node you want to remove. Get the node's ID by querying FeatureBase's `/status` endpoint. Shut the node down. Issue a POST request to the cluster coordinator node with a JSON document specifying the node's ID as the payload. E.g.


```shell
curl -XPOST https://coordinator:10101/cluster/resize/remove-node -d'{"id": "d39851e7-9444-4033-a534-c92c1b470a8e"}'
```


FeatureBase will put the cluster into the RESIZING state and move data as necessary to make sure all nodes contain the correct shards given the cluster's replication factor.

While FeatureBase is in the RESIZING state, it denies any request which accesses index data (`/status`, `/version`, etc. still work). 


### Ingester

Generally, scaling is handled by starting or stopping Ingester instances. Other options may be available for specific Ingesters; see [ingest tuning](/explanations/ingesters#ingest-tuning)
