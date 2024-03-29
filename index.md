---
title: Welcome to FeatureBase Help
---

FeatureBase Help contains high level overviews of software functionality, plus procedural documentation for FeatureBase Cloud and the self-managed Community edition.

## What is FeatureBase?

FeatureBase is a feature-oriented database platform that powers real-time analytics and machine learning applications by executing low-latency, high-throughput, and highly concurrent workloads. Similar to the evolution of data formats from row-oriented to columnar, FeatureBase further evolves columnar into a feature-oriented format that makes each distinct data value individually addressable (accessible, readable, writable and retrievable).

Our novel approach minimizes I/O on queries by allowing the database engine to read and write exactly the data it needs and intelligently compress that data in memory. The result is a step-function improvement in analytical workloads.

## Before you begin

* [Learn more about FeatureBase](https://www.featurebase.com/){:target="_blank"}
* [Contact FeatureBase support](https://www.featurebase.com/contact-us){:target="_blank"}

## Comparing Cloud and Community editions

These tables provided a side-by-side comparison of Cloud and Community functionality.

## Infrastructure

| Feature | Cloud  | Community  | Notes  |
| ------ | ----- | ----------- | ----------- |
| Click to Deploy |  Yes | No | Windows installations require a Hypervisor  |
| Automated Scale Up/Down|  No | No |   |
| Automated Scale In/Out |  No | No |   |
| Regional Deployment |  No | Yes |   |

## Data Ingestion

| Feature | Cloud  | Community  | Notes  |
| ------ | ----- | ----------- | ----------- |
| Streaming (HTTPS)  |  Yes | No |   |
| Kafka (Pull-based) |  No | Yes | Client-side kafka consumption & push for Cloud |
| Database (Pull-based) |  No | Yes |  Client-side database consumption & push for Cloud |
| CSV/Bulk Ingest  |  No | Yes |  Client-side file consumption & push for Cloud |

## Data Consumption

| Feature | Cloud  | Community  | Notes  |
| ------ | ----- | ----------- | ----------- |
| Query UI  |  Yes | Yes |   |
| FeatureBase SQL - HTTPS |  Yes | No | Any language/tool (Python, Go, etc) that can read over HTTPS  |
| FeatureBase PQL - HTTPS |  Yes | Yes | Any language/tool (Python, Go, etc) that can read over HTTPS  |
| gRPC Endpoint |  No | Yes |   |
| Postgres Endpoint |  No | Yes |   |
| Unbounded Queries (Advanced Queries) |  No | Yes | Cloud Limited to 6mb and/or 30sec  |
| PQL Query Builder |  No | Yes |   |
| Python Client |  No | Yes |   |
| Grafana Plug-In |  No | Yes |   |
| Postgres Lookup Database Option |  No | Yes |   |

## Operations

| Feature | Cloud  | Community  | Notes  |
| ------ | ----- | ----------- | ----------- |
| Backup + Restore |  Yes | Yes |   |
| Data Replication |  Yes | Yes |  |
| Metrics & Monitoring |  No | Yes |   |
| Editable FeatureBase Config File |  No | Yes |   |

## Security

| Feature | Cloud  | Community  | Notes  |
| ------ | ----- | ----------- | ----------- |
| Encryption In Flight |  Yes | Yes |  |
| Encryption at Rest |  Yes | Yes |   |
| Authentication + Authorization (OAuth) |  Yes | Yes |  |
| Role-Based Access Control (Basic) |  No | Yes |   |
| User Management |  Yes | Yes |  |
| Audit Logging |  Yes | Yes |   |

## Next Step

You can choose to setup a cloud account, or install FeatureBase on a local server.

* [Setup your FeatureBase cloud account](/cloud/cloud-introduction)
* [Install FeatureBase Community locally](/community/community-setup/community-install-config)
