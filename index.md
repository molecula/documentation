---
title: Welcome to FeatureBase!
---

FeatureBase is a [B-tree](https://en.wikipedia.org/wiki/B-tree) database which uses [Roaring Bitmaps](https://roaringbitmap.org/). This makes it suitable for doing analytical queries on massive data sets immediately after ingestion. If you are the inquisitive type, you may be interested in the [architectural overview](https://docs.featurebase.com/setting-up-featurebase/Community/architecture).

## Comparing Cloud and Community editions


## Infrastructure

| Feature | Cloud  | Community  | Notes  |
| ------ | ----- | ----------- | ----------- |
| Click to Deploy |  No | Yes | Windows installations require a Hypervisor  |
| Automated Scale Up/Down|  Yes | Yes |   |
| Automated Scale In/Out |  Yes | Yes |   |
| Regional Deployment |  Yes | No |   |


## Data Ingestion

| Feature | Cloud  | Community  | Notes  |
| ------ | ----- | ----------- | ----------- |
| Streaming (HTTPS)  |  No | Yes |   |
| Kafka (Pull-based) |  Yes | No | Client-side kafka consumption & push for Cloud |
| Database (Pull-based) |  Yes | No |  Client-side database consumption & push for Cloud |
| CSV/Bulk Ingest  |  Yes | No |  Client-side file consumption & push for Cloud |

## Data Consumption

| Feature | Cloud  | Community  | Notes  |
| ------ | ----- | ----------- | ----------- |
| Query UI  |  No | No |   |
| FeatureBase SQL - HTTPS |  No | Yes | Any language/tool (Python, Go, etc) that can read over HTTPS  |
| FeatureBase PQL - HTTPS |  No | No | Any language/tool (Python, Go, etc) that can read over HTTPS  |
| gRPC Endpoint |  Yes | No |   |
| Postgres Endpoint |  Yes | No |   |
| Unbounded Queries (Advanced Queries) |  Yes | No | Cloud Limited to 6mb and/or 30sec  |
| PQL Query Builder |  Yes | No |   |
| Python Client |  Yes | No |   |
| Grafana Plug-In |  Yes | No |   |
| Postgres Lookup Database Option |  Yes | No |   |

## Operations

| Feature | Cloud  | Community  | Notes  |
| ------ | ----- | ----------- | ----------- |
| Backup + Restore |  Yes | No |   |
| Data Replication |  No | No |  |
| Metrics & Monitoring |  Yes | No |   |
| Editable FeatureBase Config File |  Yes | No |   |

## Security

| Feature | Cloud  | Community  | Notes  |
| ------ | ----- | ----------- | ----------- |
| Encryption In Flight |  No | No |  |
| Encryption at Rest |  No | No |   |
| Authentication + Authorization (OAuth) |  No | No |  |
| Role-Based Access Control (Basic) |  Yes | No |   |
| User Management |  No | No |  |
| Audit Logging |  No | No |   |

## Next Step

You can choose to setup a cloud account, or install FeatureBase on a local server.

* [Setup your FeatureBase cloud account](/docs/cloud/part1-signup-to-cloud)
* [Install FeatureBase on Linux](/docs/community/install-featurebase-linux)
* [Install FeatureBase on Mac](/docs/community/install-featurebase-mac)
* [Install FeatureBase on Windows](/docs/community/install-featurebase-windows)

## Further information


## Get support

{% include /docs/get-support-source.md %}
