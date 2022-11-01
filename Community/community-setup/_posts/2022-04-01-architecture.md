---
id: architecture
title: Architecture
sidebar_label: Architecture
---

![FeatureBase Network Architecture Diagram](/img/molecula-architecture-diagram.png "FeatureBase Network Architecture Diagram")


## Components


### FeatureBase

FeatureBase  is a masterless multi-node system with a single node type. Like other common distributed data stores, it supports high availability (via shard replication), cluster resizing, and distributed query processing.

FeatureBase is similar to a columnar store, but breaks each column into each of its unique values so that they can be represented as a single bit. This data representation is excellent for a variety of analytical workloads.


### Ingester(s)

Ingesters are responsible for retrieving data from an upstream data source, transforming it into a FeatureBase-compatible format, and writing that data to FeatureBase. Ingesters are specific to the upstream data source, so in the case where the data source is a Kafka pipeline, a Kafka-specific ingester is used to read messages from a Kafka topic and transform the messages into FeatureBases's bit-columnar format. In that example, the Kafka-specific ingester can interact with a Confluent Schema Registry in order to determine message schema and to inform the specific field types used in FeatureBase.

The ingester takes configuration options which tell it how to interact with the upstream data source. For the Kafka ingester, those options include the address of the Kafka service as well as any authentication parameters, the topic from which to read, and the address of the schema registry.


## Interfaces


### Ports and Protocols

By default, FeatureBase listens for HTTP(S) on port 10101 and gRPC on port 20101. Both of these protocols are required for FeatureBase to function properly.

Optionally, FeatureBase listens on port 55342 for the PostgreSQL wire protocol. It can accept [PQL](/pql-guide/pql-introduction) queries, or a [subset of SQL](/sql-guide/sql) over this protocol.

Internally, FeatureBase uses [embedded etcd](https://pkg.go.dev/github.com/coreos/etcd/embed) for consistently managing things like cluster membership and schema, using ports 10301 and 10401 by default.

