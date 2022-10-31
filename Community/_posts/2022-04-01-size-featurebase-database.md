---
id: size-molecula-database
title: Sizing Your FeatureBase Database
sidebar_label: Sizing FeatureBase
---

## Determining Hardware Requirements

Ingesters in FeatureBase are stateless and can be deployed in containers and easily scaled up and down. FeatureBase is stateful and has widely varying hardware requirements depending on the size of the data and query workload. FeatureBase can also be scaled up and down, but there's enough overhead in this process that you wouldn't want to be resizing it constantly in response to shifting demand. You may also need to adjust some operating system configuration features to take full advantage of larger systems; see [host system requirements](/reference/operations/enterprise/hostsystem).


#### Memory

If possible, determine the rough dimensions of the data you'll be storing in FeatureBase. The most important factors are the number of records, number of fields, type of each field (as it will be indexed in FeatureBase), and the cardinality of each field (number of distinct values).

FeatureBase breaks data into shards which are, by default, 2^20 (1,048,576) records. It is useful to figure out approximately how large each of your shards will be, and then use that to extrapolate memory requirements. The most accurate way to do this is to load a shard's worth of data into FeatureBase and measure its size on disk. Below is a table of some typical field configurations, and how much space they use, as a starting point for estimating hardware sizes. Please keep in mind that depending on data distribution, the actual size in your case might vary significantly from these numbers.

Depending on your storage backend, memory usage and disk usage can both vary. In general, you want at least a bit more memory than the on-disk storage of your data, possibly as much as twice as much memory available. This memory may look like it's directly being used by the FeatureBase engine, or may just be kernel disk caches.

The rough formula for calculating total cluster data storage (across all hosts) is

```math
(num_records/shard_width)*size_per_shard*2
```

For more detailed information on data size, see the [Data Modeling](/concepts/data-modeling) section.

| Field Type              | Cardinality | Size (per shard) |
| -                       |           - | -                |
| Int                     |  20 Million | 3.1 MB           |
| Int                     |  10 Billion | 4.3 MB           |
| Int                     |         256 | 1 MB             |
| Set/Bool/Mutex          |           2 | 0.3 MB           |
| Set/Bool/Mutex (sparse) |         500 | 2.1 MB           |
| Set/Bool/Mutex (sparse) |        1000 | 2.2 MB           |
| Set (dense)             |          10 | 1.3 MB           |
| Set (dense)             |         100 | 13 MB            |


As a worked example, if you expected to have about 100 million records, with the set of fields above, the calculation would look like:

`(100,000,000/1,048,576)*(3.1+4.3+1+0.3+2.1+2.2+1.3+13)*2 = 5207MB ~= 5GB` of disk storage across your whole cluster. If you were using a single node, you'd want at least 8-10GB of available memory for it.

When you split a cluster into multiple nodes, each node will have some duplication and overhead. So, if you were using 5GB on a single node, and switched to 5 nodes, you should budget for at least 2GB of storage on each node.


#### Disk

For disk size requirements, refer to the [memory](#memory) section. Faster disks such as SSDs will affect startup time and ingest performance. Read performance may be affected by disk speed, depending on your backend, but if you have enough memory, the kernel will usually keep everything in disk cache anyway.


#### CPU

In general, adding more CPU cores to a FeatureBase cluster improves query latency and throughput. For a single query, FeatureBase fans the query out to all shards which have data pertinent to the query, and each shard can be processed concurrently by a different CPU core. Adding cores past the number of shards in the cluster will not improve single query performance, though it will help with query throughput in the case of concurrent query loads. The number of CPU cores to allocate depends on latency needs, query workload, and data size and structure. A reasonable starting point might be to allocate 1 core for every 10 shards. You should also aim to provide at least one more core for general overhead not specific to processing results from shards.


#### Network

While network typically isn't a bottleneck, FeatureBase hosts should typically be on the same LAN to minimize latency. Use placement groups (in AWS) or similar functionality to ensure minimum latency between hosts.


#### Other Considerations

*   All FeatureBase hosts should be the same size. FeatureBase doesn't currently have the ability to shard data unevenly, so adding hosts of different sizes limits utilization to the size of the smallest host.
*   Typical databases have fewer but larger hosts — 8+ cores and 16+GB of RAM are typical.
*   OS: a recent version of Linux.
*   Filesystem: Most options will work well. We have occasionally encountered [problems with file truncation on XFS](https://stackoverflow.com/questions/47077828/xfs-rhel7-3-cold-reboot-file-truncate), so we do not recommend it.
