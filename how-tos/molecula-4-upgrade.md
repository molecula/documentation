---
id: molecula-4-upgrade
title: How To Upgrade to Molecula 4.x
sidebar_label: Upgrade to Molecula 4.x
---

## Summary
Molecula 4.x includes FeatureBase version 3.x, which is the main change from Molecula version 3.x, which included Pilosa version 2.x. 

In Molecula version 4.x, we have introduced a product rename from Pilosa to FeatureBase, roaring B-tree format for storage, and etcd for key-value store. These changes were made to improve high availability and consistency.

### Pilosa Rename
Pilosa was renamed to FeatureBase. For details, refer to the [FeatureBase Rename](/reference/featurebase-rename) page.
### Roaring B-tree Format
The new roaring B-tree format (RBF) storage backend provides ACID semantics at a shard level. It reduces heap usage for more predictable memory consumption and garbage collection behavior. 

### etcd
FeatureBase 3.0 embeds etcd, which uses a Raft-based consensus algorithm to power a strongly consistent key/value store; FeatureBase uses this to maintain cluster state, node state, and data schema. This reduces internal complexity in FeatureBase's codebase while providing a more reliable store for important metadata.

## Operational/Configuration changes

### Add Log Prefix Levels
In FeatureBase v3.x, a log prefix level was introduced. The available prefix levels are `PANIC`, 
`ERROR`, `WARN`, `INFO` and `DEBUG`.

Pilosa v2.x:

```2021-10-22T20:56:32.199996Z Molecula Pilosa v2.8.7 (Oct 22 2021 3:56PM, 02f14f42) go1.16.7```

FeatureBase v3.x:

```2021-10-22T19:32:36.427981Z INFO:  Molecula Pilosa v3.5.0 (Sep 28 2021 6:53PM, f0b93da0) go1.16.3```

### UI Usage 
Some operations on the tables page of the UI can be very expensive on large datasets. One of these operations is the disk usage operation, which can be disabled with the `usage-duty-cycle` option (Additional details can be found in the [Configuration](#configuration) section). The tables page of the UI also calculates cardinality across all fields, which can be expensive. For FeatureBase v3.5, there is no configuration to disable calculating cardinality, but it is something to be aware of if using the UI. 

### Backup and Restore Functionality
FeatureBase v3.x has new backup and restore functionality. For details, refer to the [Backups](/reference/backups) page. 

### Configuration

For additional details on the new configuration, refer to the [FeatureBase Configuration](/reference/featurebase-configuration)

#### New Configuration 
`--name`: Set a unique name for this node within the cluster. This is used internally by etcd.

`--max-query-memory`: Set a limit for max query memory for Extract or Select queries. 

Many of the cluster related configuration options have changed. The coordinator node is no longer needed and there is no longer an option to set `coordinator` or `hosts`.  Instead, the `etcd` options must be set.

      --etcd.advertise-peer-address         
      --etcd.cluster-url 
      --etcd.initial-cluster
      --etcd.listen-client-address
      --etcd.listen-peer-address string

The entire `gossip` section has been removed as that functionality has been replaced by `etcd`. 

`--postgres.sql-version`: Set the version for SQL. SQL Version 2 is a new experimental Molecula SQL handling. You do not need to explicitly set this unless you're trying out the new SQL engine.       

`--query-history-length`: Set the maximum number of queries maintained for the `/query-history` endpoint.

`--usage-duty-cycle`: Set the percentage of time that is spent recalculating the disk and memory usage cache. 100.0 for always-running, 0 disables the cache and the `/ui/usage` endpoint. These computations can be quite intensive, and many users disable this endpoint to avoid disruptions. 

`--future.rename`: Set application name as FeatureBase instead of Pilosa. Default is false. Setting this to true changes all the flags and environment variables to use FeatureBase rather than Pilosa.

`--long-query-time`: Used to be nested under cluster, but it is now top level.

### Data Directory Structure    
Changes to the data directory structure in FeatureBase were made to account for RBF and etcd changes. For details, refer to the [Data Directory Structure](/explanations/data-directory-structure). In general, the Molecula team would like to discourage reliance on any particular details of the directory structure. 

Pilosa v2.x:
```
$ ls .pilosa/
idalloc.db      index1
```

FeatureBase v3.x:
```
$ ls .pilosa/
disco       idalloc.db      indexes     startup.log
```

## Remove Support for Attributes in FeatureBase
Pilosa previously provided the ability to associate arbitrary key/value pairs with any row or column in any index. This feature was almost entirely unused, and has been removed.

## Migration

### Migration Tool for RBF
Migration tool was built to convert data from a set of Pilosa v2.x data directories to FeatureBase backup format. Once the conversion is complete, the new FeatureBase restore functionality is used to populate data into an updated cluster. 

### Process to Migrate from Pilosa v2.x to FeatureBase v3.x
#### 1. Stop Ingest

#### 2. Backup as usual 

#### 3. Convert Pilosa Data to RBF  
The roaring-migrate binary is included in the FeatureBase release. To update Pilosa data to the new roaring B-tree format, run the following command. 

```
./roaring-migrate --data-dir /tmp/pilosa1,/tmp/pilosa2,/tmp/pilosa3 --backup-dir /tmp/backupDir
```
 - ```data-dir``` represents the directory where Pilosa is currently stored. Multiple directories (one for each node in the cluster) can be passed to the ```data-dir``` separated by a comma. 
 - ```backup-dir``` represents the directory where data converted to RBF will be stored. 

#### 4. Stand-up a New FeatureBase
Instructions for setting up FeatureBase are in the [How to Install FeatureBase](/how-tos/install-featurebase). Also, refer to the [FeatureBase Configuration](/reference/featurebase-configuration) for additional details. This stop is not necessarily dependent on the previous 3, and if your environment allows this, you'll probably want to do this first to minimize downtime.

The new FeatureBase cluster needs to contain an odd number of nodes due to reliance on an embedded `etcd` cluster.

#### 5. Restore Backup
Once FeatureBase is running, it is time to restore the backup data. 

```
./featurebase restore --source /tmp/backupDir
```

#### 6. Start Ingest
At this stage, the data has been restored to FeatureBase, and ingestion can be restarted. 