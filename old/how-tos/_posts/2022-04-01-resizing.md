---
id: resize-featurebase-cluster
title: Resizing Your FeatureBase Cluster
sidebar_label: Resizing FeatureBase
---

## Summary

The cluster backup & restore tooling provides a simple way to extract data from a cluster and restore that data to a new cluster—even if the new cluster is a different size.
We can use this process to migrate from a smaller cluster to a larger one in a relatively short amount of time.

Data in FeatureBase is typically historical data fed in via bulk ingest or streamed in via Kafka or another data pipeline.
As such, the latency requirements are looser than if FeatureBase were a system of record. Migration can be performed in several steps:
1. [Start a new FeatureBase cluster.](#1-start-a-new-featurebase-cluster)
2. [Stop ingestion via a bulk ingester.](#2-stop-ingestion-via-a-bulk-ingester)
3. [Backup data from the original FeatureBase cluster.](#3-backup-data-from-the-original-featurebase-cluster)
4. [Restore data to the new FeatureBase cluster.](#4-restore-data-to-the-new-featurebase-cluster)
5. [Redirect traffic to the new FeatureBase cluster.](#5-redirect-traffic-to-the-new-featurebase-cluster)
6. [Restart ingestion against the new FeatureBase cluster.](#6-restart-ingestion-against-the-new-featurebase-cluster)
7. [Shutdown the original FeatureBase cluster.](#7-shutdown-the-original-featurebase-cluster)

## 1. Start a new FeatureBase cluster.

First, create a new cluster of the desired size.
The configuration from the old cluster can be reused by changing:

- [`etcd.listen-client-address`](/reference/featurebase-configuration#etcd-listen-client-address) to the node's new network address
- [`etcd.listen-peer-address`](/reference/featurebase-configuration#etcd-listen-peer-address) to the node's new network address
- [`etcd.initial-cluster`](/reference/featurebase-configuration#etcd-initial-cluster) to use the new network addresses and add additional nodes

Additionally, if the replication factor needs to be changed, the [`cluster.replicas`](/reference/featurebase-configuration#cluster-replicas) setting should be updated now.

## 2. Stop ingestion via a bulk ingester

If data is written during/after a backup, it will not end up on the new cluster.
In order to ensure that all data are preserved, shut down the writing processes for the remainder of the migration.
If using an ingest consumer (e.g. `molecula-consumer-kafka`), this should be accomplished by completely shutting down the process.
Do not attempt to stall the consumer by creating an exclusive transaction.

## 3. Backup data from the original FeatureBase cluster.

The `featurebase` command line tool contains a [`backup`](/reference/backups#featurebase) subcommand for executing a backup against a cluster:
```
featurebase backup --host featurebase:10101 -o /path/to/backup/ --concurrency 4 # and TLS config
```
The [`--concurrency`](/reference/backups#backup-concurrency) flag is not required, but setting it to an appropriate number will improve backup speed.

It is possible to speed the process up more by [disabling sync](/reference/backups#storage-synchronization) of the backup data:
```
featurebase backup --host featurebase:10101 -o /path/to/backup/ --no-sync
```

This will allow the backup to complete without waiting for the operating system to move the data to persistent storage.
If the machine running the backup loses power, you may lose some (or all) of the backup data.

## 4. Restore data to the new FeatureBase cluster.

The `featurebase` command line tool has an accompanying [restore](/reference/backups#featurebase) subcommand that will restore a directory created by the backup subcommand:
```
featurebase restore --host newfeaturebase:10101 -s /path/to/backup/ --concurrency 4
```

## 5. Redirect traffic to the new FeatureBase cluster.

Once the data have been moved over to the new cluster, it is safe to redirect query traffic.
Change the targets of any load balancers, and update configurations for services which may be pointed manually to a node.

## 6. Restart ingestion against the new FeatureBase cluster.

Once the new system is up and running, the [ingester configurations](/reference/ingester-configuration) can be updated to point to the new cluster (`pilosa-hosts` and `pilosa-grpc-hosts`, respectively `--featurebase-hosts` and `--featurebase-grpc-hosts` with `--future.rename` flag).
They can then be started back up to import new data.

## 7. Shutdown the original FeatureBase cluster.

Once the new cluster is running and appears to be functioning properly, the old cluster may be shut down and deleted.
