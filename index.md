---
title: Welcome to FeatureBase!
---

FeatureBase is a [B-tree](https://en.wikipedia.org/wiki/B-tree) database which uses [Roaring Bitmaps](https://roaringbitmap.org/). This makes it suitable for doing analytical queries on massive data sets immediately after ingestion. If you are the inquisitive type, you may be interested in the [architectural overview](/community/community-setup/architecture).

## Before you begin

* [Learn about Database Bitmaps](https://www.featurebase.com/blog/bitmaps-making-real-time-analytics-real)

## Comparing FeatureBase Cloud and Community

## Infrastructure

| Feature | Cloud  | Community |
| ------ | ----- | ----------- |
| Click to Deploy |  Yes | No |
| Automated Scale Up/Down|  No | No |
| Automated Scale In/Out |  No | No |
| Regional Deployment |  No | Yes |

## Security

|Feature | Cloud  | Community  |
| ------ | ----- | ----------- |
|Encryption In Flight |  Yes| Yes |
|Encryption at Rest |  Yes| Yes |
|Authentication + Authorization (OAuth) |  Yes | Yes |
|Role-Based Access Control (Basic) |  No | Yes |
|User Management |  Yes | Yes |
|Audit Logging |  Yes | Yes |

## Operations

| Feature | Cloud  | Community  |
| ------ | ----- | ----------- |
| Backup + Restore |  No | Yes |
| Data Replication |  Yes | Yes |
| Metrics & Monitoring |  No | Yes |
| Editable FeatureBase Config File |  No | Yes |

## Data Ingestion

|Feature | Cloud  | Community  | Notes  |
| ------ | ----- | ----------- | ----------- |
| Streaming (HTTPS)  |  Yes | No |   |
| Kafka (Pull-based) |  No| Yes | Client-side kafka consumption & push for Cloud |
| Database (Pull-based) |  No | Yes |  Client-side database consumption & push for Cloud |
| CSV/Bulk Ingest  |  No | Yes |  Client-side file consumption & push for Cloud |

## Data Consumption

|Feature | Cloud  | Community  | Notes  |
| ------ | ----- | ----------- | ----------- |
| Query UI  |  Yes| Yes |   |
| FeatureBase SQL - HTTPS |  Yes| No | Any language/tool (Python, Go, etc) that can read over HTTPS  |
| FeatureBase PQL - HTTPS |  Yes| Yes | Any language/tool (Python, Go, etc) that can read over HTTPS  |
| gRPC Endpoint |  No | Yes |   |
| Postgres Endpoint |  No| Yes |   |
| Unbounded Queries (Advanced Queries) |  No| Yes | Cloud Limited to 6mb and/or 30sec  |
| PQL Query Builder |  No| Yes |   |
| Python Client |  No | Yes |   |
| Grafana Plug-In |  No | Yes |   |
| Postgres Lookup Database Option |  No| Yes |   |

## Next step

* [Learn about FeatureBase Cloud](/cloud/cloud-setup/cloud-introduction)
* [Learn how to setup FeatureBase Community](/community/community-setup/community-install-config)

## Further information

* [Read the technical whitepaper](https://www.featurebase.com/blog/featurebase-technical-white-paper)
* [Learn the history of the product that became FeatureBase](https://www.featurebase.com/blog/pilosa-molecula-featurebase-a-story-of-evolution)
