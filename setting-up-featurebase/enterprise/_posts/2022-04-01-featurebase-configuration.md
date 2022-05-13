---
id: featurebase-configuration
title: FeatureBase Configuration
sidebar_label: FeatureBase Configuration
---


### Configuration

FeatureBase can be configured through command line flags, environment variables, and/or a TOML configuration file; configured options take precedence in that order.

| CLI Flag                       | Environment Variable                  | Environment Variable (with `-future.rename` flag) | Type  | Note |
|--------------------------------|---------------------------------------|---------------------------------------------------|-------|------|
| advertise                      | PILOSA_ADVERTISE                      | FEATUREBASE_ADVERTISE                             | str   |      |
| advertise-grpc                 | PILOSA_ADVERTISE_GRPC                 | FEATUREBASE_ADVERTISE_GRPC                        | str   |      |
| bind                           | PILOSA_BIND                           | FEATUREBASE_BIND                                  | str   |      |
| bind-grpc                      | PILOSA_BIND_GRPC                      | FEATUREBASE_BIND_GRPC                             | str   |      |
| data-dir                       | PILOSA_DATA_DIR                       | FEATUREBASE_DATA_DIR                              | str   |      |
| log-path                       | PILOSA_LOG_PATH                       | FEATUREBASE_LOG_PATH                              | str   |      |
| max-file-count                 | PILOSA_MAX_FILE_COUNT                 | FEATUREBASE_MAX_FILE_COUNT                        | int   |      |
| max-map-count                  | PILOSA_MAX_MAP_COUNT                  | FEATUREBASE_MAX_MAP_COUNT                         | int   |      |
| max-writes-per-request         | PILOSA_MAX_WRITES_PER_REQUEST         | FEATUREBASE_MAX_WRITES_PER_REQUEST                | int   |      |
| max-query-memory               | PILOSA_MAX_QUERY_MEMORY               | FEATUREBASE_MAX_QUERY_MEMORY                      | int   |      |
| name                           | PILOSA_NAME                           | FEATUREBASE_NAME                                  | str   |      |
| verbose                        | PILOSA_VERBOSE                        | FEATUREBASE_VERBOSE                               | bool  |      |
| usage-duty-cycle               | PILOSA_USAGE_DUTY_CYCLE               | FEATUREBASE_USAGE_DUTY_CYCLE                      | float |      |
| anti-entropy.interval          | PILOSA_ANTI_ENTROPY_INTERVAL          | FEATUREBASE_ANTI_ENTROPY_INTERVAL                 | str   |      |
| cluster.name                   | PILOSA_CLUSTER_NAME                   | FEATUREBASE_CLUSTER_NAME                          | str   |      |
| cluster.long-query-time        | PILOSA_CLUSTER_LONG_QUERY_TIME        | FEATUREBASE_CLUSTER_LONG_QUERY_TIME               | str   |      |
| cluster.replicas               | PILOSA_CLUSTER_REPLICAS               | FEATUREBASE_CLUSTER_REPLICAS                      | int   |      |
| cluster.partition-to-node-assignment               | PILOSA_CLUSTER_PARTITION_TO_NODE_ASSIGNMENT               | CLUSTER_PARTITION_TO_NODE_ASSIGNMENT                      | str   |      |
| etcd.advertise-client-address  | PILOSA_ETCD_ADVERTISE_CLIENT_ADDRESS  | FEATUREBASE_ETCD_ADVERTISE_CLIENT_ADDRESS         | str   |      |
| etcd.advertise-peer-address    | PILOSA_ETCD_ADVERTISE_PEER_ADDRESS    | FEATUREBASE_ETCD_ADVERTISE_PEER_ADDRESS           | str   |      |
| etcd.cluster-url               | PILOSA_ETCD_CLUSTER_URL               | FEATUREBASE_ETCD_CLUSTER_URL                      | str   |      |
| etcd.initial-cluster           | PILOSA_ETCD_INITIAL_CLUSTER           | FEATUREBASE_ETCD_INITIAL_CLUSTER                  | str   |      |
| etcd.listen-client-address     | PILOSA_ETCD_LISTEN_CLIENT_ADDRESS     | FEATUREBASE_ETCD_LISTEN_CLIENT_ADDRESS            | str   |      |
| etcd.listen-peer-address       | PILOSA_ETCD_LISTEN_PEER_ADDRESS       | FEATUREBASE_ETCD_LISTEN_PEER_ADDRESS              | str   |      |
| handler.allowed-origins        | PILOSA_HANDLER_ALLOWED_ORIGINS        | FEATUREBASE_HANDLER_ALLOWED_ORIGINS               | list  |      |
| metric.diagnostics             | PILOSA_METRIC_DIAGNOSTICS             | FEATUREBASE_METRIC_DIAGNOSTICS                    | bool  |      |
| metric.host                    | PILOSA_METRIC_HOST                    | FEATUREBASE_METRIC_HOST                           | str   |      |
| metric.poll-interval           | PILOSA_METRIC_POLL_INTERVAL           | FEATUREBASE_METRIC_POLL_INTERVAL                  | str   |      |
| metric.service                 | PILOSA_METRIC_SERVICE                 | FEATUREBASE_METRIC_SERVICE                        | str   |      |
| postgres.bind                  | PILOSA_POSTGRES_BIND                  | FEATUREBASE_POSTGRES_BIND                         | str   |      |
| postgres.max-connections       | PILOSA_POSTGRES_MAX_CONNECTIONS       | FEATUREBASE_POSTGRES_MAX_CONNECTIONS              | int   |      |
| postgres.max-startup-size      | PILOSA_POSTGRES_MAX_STARTUP_SIZE      | FEATUREBASE_POSTGRES_MAX_STARTUP_SIZE             | int   |      |
| postgres.read-timeout          | PILOSA_POSTGRES_READ_TIMEOUT          | FEATUREBASE_POSTGRES_READ_TIMEOUT                 | str   |      |
| postgres.startup-timeout       | PILOSA_POSTGRES_STARTUP_TIMEOUT       | FEATUREBASE_POSTGRES_STARTUP_TIMEOUT              | str   |      |
| postgres.write-timout          | PILOSA_POSTGRES_WRITE_TIMOUT          | FEATUREBASE_POSTGRES_WRITE_TIMOUT                 | str   |      |
| postgres.tls                   | PILOSA_POSTGRES_TLS                   | FEATUREBASE_POSTGRES_TLS                          | dict  |      |
| profile.block-rate             | PILOSA_PROFILE_BLOCK_RATE             | FEATUREBASE_PROFILE_BLOCK_RATE                    | int   |      |
| profile.mutex-fraction         | PILOSA_PROFILE_MUTEX_FRACTION         | FEATUREBASE_PROFILE_MUTEX_FRACTION                | int   |      |
| schema-details-on              | PILOSA_SCHEMA_DETAILS_ON              | FEATUREBASE_SCHEMA_DETAILS_ON                     | bool  |      |
| storage.backend                | PILOSA_STORAGE_BACKEND                | FEATUREBASE_STORAGE_BACKEND                       | str   |      |
| tls.ca-certificate             | PILOSA_TLS_CA_CERTIFICATE             | FEATUREBASE_TLS_CA_CERTIFICATE                    | str   |      |
| tls.certificate                | PILOSA_TLS_CERTIFICATE                | FEATUREBASE_TLS_CERTIFICATE                       | str   |      |
| tls.enable-client-verification | PILOSA_TLS_ENABLE_CLIENT_VERIFICATION | FEATUREBASE_TLS_ENABLE_CLIENT_VERIFICATION        | bool  |      |
| tls.key                        | PILOSA_TLS_KEY                        | FEATUREBASE_TLS_KEY                               | str   |      |
| tls.skip-verify                | PILOSA_TLS_SKIP_VERIFY                | FEATUREBASE_TLS_SKIP_VERIFY                       | bool  |      |
| tracing.agent-host-port        | PILOSA_TRACING_AGENT_HOST_PORT        | FEATUREBASE_TRACING_AGENT_HOST_PORT               | str   |      |
| tracing.sampler-param          | PILOSA_TRACING_SAMPLER_PARAM          | FEATUREBASE_TRACING_SAMPLER_PARAM                 | float |      |
| tracing.sampler-type           | PILOSA_TRACING_SAMPLER_TYPE           | FEATUREBASE_TRACING_SAMPLER_TYPE                  | str   |      |
| translation.map-size           | PILOSA_TRANSLATION_MAP_SIZE           | FEATUREBASE_TRANSLATION_MAP_SIZE                  | int   |      |
| translation.primary-url        | PILOSA_TRANSLATION_PRIMARY_URL        | FEATUREBASE_TRANSLATION_PRIMARY_URL               | str   |      |
| auth.enable                    | PILOSA_AUTH_ENABLE                    | FEATUREBASE_AUTH_ENABLE                           | bool  |      |
| auth.client-id                 | PILOSA_AUTH_CLIENT_ID                 | FEATUREBASE_AUTH_CLIENT_ID                        | str  |      |
| auth.client-secret             | PILOSA_AUTH_CLIENT_SECRET             | FEATUREBASE_AUTH_CLIENT_SECRET                    | str  |      |
| auth.authorize-url             | PILOSA_AUTH_AUTHORIZE_URL             | FEATUREBASE_AUTH_AUTHORIZE_URL                    | str  |      |
| auth.token-url                 | PILOSA_AUTH_TOKEN_URL                 | FEATUREBASE_AUTH_TOKEN_URL                        | str  |      |
| auth.group-endpoint-url        | PILOSA_AUTH_GROUP_ENDPOINT_URL        | FEATUREBASE_AUTH_GROUP_ENDPOINT_URL               | str  |      |
| auth.redirect-base-url         | PILOSA_AUTH_REDIRECT_BASE_URL         | FEATUREBASE_AUTH_REDIRECT_BASE_URL                | str  |      |
| auth.logout-url                | PILOSA_AUTH_LOGOUT_URL                | FEATUREBASE_AUTH_LOGOUT_URL                       | str  |      |
| auth.scopes                    | PILOSA_AUTH_SCOPES                    | FEATUREBASE_AUTH_SCOPES                           | list |      |
| auth.secret-key                | PILOSA_AUTH_SECRET_KEY                | FEATUREBASE_AUTH_SECRET_KEY                       | str  |      |
| auth.permissions               | PILOSA_AUTH_PERMISSIONS               | FEATUREBASE_AUTH_PERMISSIONS                      | str  |      |
| auth.query-log-path            | PILOSA_AUTH_QUERY_LOG_PATH            | FEATUREBASE_AUTH_QUERY_LOG_PATH                   | str  |      |

Options are listed in the table by their CLI and Environment names. Further details are given below with the TOML configuration file variables. Note that there is a direct correlation between the CLI name and the TOML name. For example, the CLI flag `etcd.initial-cluster` is identified in TOML as:

```toml
[etcd]
  initial-cluster = "featurebase1=http://localhost:10301,featurebase2=http://localhost:10302"
```


#### Advertise

Address advertised by the server to other nodes in the cluster and to clients via the `/status` endpoint. Host defaults to the IP address represented by `bind` and port to 10101. If `bind` is set to `0.0.0.0` and `advertise` is not specified, then FeatureBase will try to determine a reasonable, external IP address to use for `advertise`.


```toml
    advertise = 192.168.1.100:10101
```



#### Anti Entropy Interval

Interval at which the cluster will run its anti-entropy routine which ensures that all replicas of each shard are in sync.


```toml
    [anti-entropy]
      interval = "10m0s"
```



#### Bind

host:port on which the FeatureBase server will listen for requests. Host defaults to localhost and port to 10101. If `bind` is set to `0.0.0.0` then FeatureBase will listen on all available interfaces.


```toml
    bind = localhost:10101
```



#### CORS (Cross-Origin Resource Sharing) Allowed Origins

List of allowed origin URIs for CORS


```toml
    [handler]
      allowed-origins = ["https://myapp.com", "https://myapp.org"]
```



#### Data Dir

Directory to store FeatureBase data files.


```toml
    data-dir = "/opt/molecula/featurebase"
```



#### Log Path

Path of log file.


```toml
    log-path = "/path/to/logfile"
```



#### Name

Unique name for the node in the cluster.


```toml
    name = "featurebase0"
```



#### Verbose

Enable verbose logging.


```toml
    verbose = true
```



#### Max Map Count

Maximum number of active memory maps FeatureBase will use for fragment files (actual total usage may be slightly higher). Best practice is to set this ~10% lower than your system's maximum map count (obtained via `sysctl vm.max_map_count` on Linux). If you plan on having lots of fragments per host, it's a good idea to raise both the system's max map count, and FeatureBase's. The number of fragments is a function of the number of shards, fields, and time quantums. Using, for example, YMDH time quantum fields with a wide range of timestamps will create lots of fragments. When FeatureBase exhausts the max-map-count it falls back to reading files directly into memory. This can be a bit slower, and cause slower restarts, but is generally fine.

  


```toml
    max-map-count = 1000000
```



#### Max Writes Per Request

Maximum number of mutating commands allowed per request. This includes Set, Clear, ClearRow, and Store.


```toml
    max-writes-per-request = 5000
```



#### Max File Count

A soft limit on the maximum number of files that FeatureBase will keep open simultaneously. When past this limit, FeatureBase will only keep files open for as long as it needs to write updates. This will negatively affect performance in cases where FeatureBase is doing lots of small updates.


```toml
    max-file-count = 1000000
```
#### Max Query Memory
A limit on the maximum memory allowed per Extract() or SELECT query. When past this limit, FeatureBase will return an error ```"query result exceeded memory threshold"```. When limit is not set, the max query memory is set to 20% of total memory of the node by default. The max query memory is specified in bytes. 

```toml
    max-query-memory = 4000000000
```

#### Cluster Name

Name for the cluster, must be the same on all nodes in the cluster.


```toml
    [cluster]
      name = "cluster0"
```



#### Cluster Replicas

Number of hosts each piece of data should be stored on. Must be greater than or equal to 1 and less than or equal to the number of nodes in the cluster.


```toml
    [cluster]
      replicas = 1
```


#### Cluster Partition To Node Assignment

 *CAUTION*: This controls how partitions are assigned to cluster nodes. Default is "jmp-hash". Larger clusters will experience more equal data distribution using "modulus". This *must* not be changed once a cluster has data, only set this option to something different on a brand new cluster. To change from the default to modulus, take a backup, start up a new empty cluster with the setting set to "modulus", then restore your backup into the new cluster.


 ```toml
     [cluster]
       partition-to-node-assignment = jmp-hash
 ```


#### Etcd Advertise Client Address

Address to advertise externally for client connections. If a value is not provided, this will default to the value provided for `etcd.listen-client-address`.

```toml
    [etcd]
      advertise-client-address = "http://localhost:10401"
```



#### Etcd Advertise Peer Address

Address to advertise externally for peer connections. If a value is not provided, this will default to the value provided for `etcd.listen-peer-address`.


```toml
    [etcd]
      advertise-peer-address = "http://localhost:10301"
```



#### Etcd Cluster URL

URL of an existing cluster that a new node should join to when growing the cluster.


```toml
    [etcd]
      cluster-url = "http://localhost:10401"
```



#### Etcd Initial Cluster

Comma-separated list of `node=address` pairs which make up the initial cluster when it's first started. In each pair, the `node` value—the left side of the `=` sign—should match the name of the node which is specified by its `name` configuration parameter.


```toml
    [etcd]
      initial-cluster = "featurebase1=http://localhost:10401,featurebase2=http://localhost:10402"
```



#### Etcd Listen Client Address

Address and port to bind to for client communication.


```toml
    [etcd]
      listen-client-address = "http://localhost:10401"
```



#### Etcd Listen Peer Address

Address and port to bind to for peer communication.


```toml
    [etcd]
      listen-peer-address = "http://localhost:10301"
```



#### Profile CPU

If this is set to a path, collect a cpu profile and store it there.


```toml
    [profile]
      cpu = "/path/to/somewhere"
```



#### Profile CPU Time

Amount of time to collect cpu profiling data at startup if `profile.cpu` is set.


```toml
    [profile]
      cpu-time = "30s"
```



#### Metric Service

Which stats service to use for collecting metrics. Choose from [statsd, expvar, prometheus, none].


```toml
    [metric]
      service = "statsd"
```



#### Metric Host

Address of the StatsD service host.


```toml
    [metric]
      host = "localhost:8125"
```



#### Metric Poll Interval

Rate at which runtime metrics (such as open file handles and memory usage) are collected.


```toml
    [metric]
      poll-interval = "0m15s"
```



#### Metric Diagnostics

Enable reporting of limited usage statistics to FeatureBase developers. To disable, set to false.


```toml
    [metric]
      diagnostics = true
```



#### Storage Backend

Storage backend to use for all indexes in the cluster. Options are: "rbf", "roaring", "bolt". "bolt" is used for testing, and "roaring" is deprecated. Don't change this unless you know what you're doing. Default: "rbf". 


```toml
    [storage]
      backend = "rbf"
```



#### TLS Certificate

Path to the TLS certificate to use for serving HTTPS. Usually has one of `.crt` or `.pem` extensions.


```toml
    [tls]
      certificate = "/srv/featurebase/certs/server.crt"
```



#### TLS Certificate Key

Path to the TLS certificate key to use for serving HTTPS. Usually has the `.key` extension.


```toml
    [tls]
      key = "/srv/featurebase/certs/server.key"
```



#### TLS Skip Verify

Disables verification for checking TLS certificates. This configuration item is mainly useful for using self-signed certificates for a FeatureBase cluster. Do not use in production since it makes man-in-the-middle attacks trivial.


```toml
    [tls]
      skip-verify = true
```



#### Tracing Sampler Type

Jaeger sampler type (const, probabilistic, ratelimiting, or remote). Set to '`off`' to disable tracing completely.


```toml
    [tracing]
      sampler-type = "remote"
```



#### Tracing Sampler Parameter

Jaeger sampler parameter (number)


```toml
    [tracing]
      sampler-param = 0.001
```



#### Tracing Agent Host/Port

Jaeger agent host:port


```toml
    [tracing]
      agent-host-port = "localhost:6831"
```



#### Profile Block Rate

Block Rate is passed directly to Go's runtime.SetBlockProfileRate. Goroutine blocking events will be sampled at 1 per `rate` nanoseconds. A value of "1" samples every event, and 0 disables profiling.


```toml
    [profile]
      block-rate = 10000000
```



#### Profile Mutex Fraction

Mutex Fraction is passed directly to Go's runtime.SetMutexProfileFraction. 1/`fraction` of events will be sampled. 


```toml
    [profile]
      mutex-fraction = 100
```



#### Translation Map Size

Size in bytes of mmap to allocate for key translation


```toml
    [translation]
      map-size = 10737418240
```

#### Postgres Endpoint Bind

Address to bind a postgres wire protocol endpoint.
No postgres endpoint will be exposed unless a bind address is specified.
Requires Molecula v3.0 or newer.

```toml
    [postgres]
      bind = "localhost:55432"
```

#### Postgres Endpoint TLS

The TLS configuration for the postgres endpoint is structured the same as the TLS configuration for FeatureBase's other endpoints, but placed under `[postgres.tls]`.
If TLS is configured on the postgres endpoint, FeatureBase will reject unsecured connections.

Example configuration with mutual TLS:

```toml
    [postgres]
      bind = "localhost:55432"
      [postgres.tls]
        certificate = "/srv/featurebase/certs/server.crt"
        key = "/srv/featurebase/certs/server.key"
        ca-certificate = "/srv/featurebase/certs/ca.crt"
        enable-client-verification = true
```

#### Postgres Endpoint Connection Limit

The postgres endpoint has support for a connection limit.
This is generally not necessary, so it is disabled by default.

```toml
    [postgres]
      connection-limit = 10000
```

#### Postgres Maximum Startup Packet Size

By default, the postgres endpoint uses an 8 MiB limit on incoming postgres startup packets.
This should typically be sufficient, but may be exceeded if a client sends an unusually large amount of configuration data.
Oversized startup packets are typically caused by connecting with a different protocol (e.g. HTTP).

```toml
    [postgres]
      max-startup-size = 10000000
```

#### Postgres Timeouts

In order to detect stalled clients, the Postgres endpoint has connection read and write timeouts.
There is also a startup timeout, which is used for connection setup.

The read timeout does not impact idle connections.
Idle connections will only be closed by the server if TCP keepalive reports a break in the connection.
TCP keepalives use the default configuration provided by the host.

:::caution
Due to a limitation of the postgres wire protocol, raising the write timeout may delay the shutdown of a FeatureBase node.
:::

```toml
    [postgres]
      startup-timeout = "20s"
      read-timeout = "20s"
      write-timeout = "20s"
```

#### Usage Duty Cycle

FeatureBase maintains a disk/memory usage cache that is calculated periodically in the background and accessed by the ui/usage endpoint. Because this disk scan can take a long, and unpredictable, amount of time, its timing behavior is specified in a relative, rather than absolute, sense. That is, the duty cycle sets the percentage of time that is spent recalculating this cache. 
Special considerations:
- If disk usage can be calculated quickly (less than 5 seconds), fresh results will be calculated when accessed. 
- When disk usage takes longer to calculate, there is a minimum of one hour wait between cache recalculations. 

```toml
      usage-duty-cycle = 20
```
#### Schema Details Endpoint Toggle

The /schema/details endpoint is used by the UI to populate the “Tables” page. It is can be a time intensive calculation on certain datasets since it calculates the cardinality for every field in every index. Queries that are running while this is calculation is happening can be slow. If cardinality information is not needed, this feature can be turned off, in which case /schema/details will behave like the general /schema endpoint. 

```toml
      schema-details-on=false
```

#### Auth (Authentication/Authorization) configuration
Parameters to configure FeatureBase authentication and authorization with an identity provider.
#### Parameters
- `enable`: enable/disable auth in FeatureBase.
- `secret-key`: Use `keygen` included in FeatureBase release to generate a secret key. This key is used for securing intra-node communication in a FeatureBase cluster.
```
featurebase keygen
```
- `permissions`: path to `permissions.yaml` file which maps group IDs from identity provider to permissions for indexes in FeatureBase.

Identity provider specific parameters should be obtained from the identity provider.
- `client-id`: client id for registered application.
- `client-secret`: client secret for registered application.
- `authorize-url`: authorization endpoint on the identity provider's domain.
- `token-url`: token endpoint to obtain JWT from identity provider.
- `redirect-base-url`: redirect url configured in identity provider without `/redirect`. This is usually the URI of your primary featurebase node, e.g. "https://your-ip-here:10101"
- `group-endpoint-url`: HTTP endpoint that returns groups for a user's valid JWT
- `logout-url`: identity provider's logout URL
- `scopes`: a list of scopes required for an access token to request groups from the identity provider.

