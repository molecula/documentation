---
id: enterprisevscloud
title: Enterprise vs Cloud
sidebar_label: Enterprise vs Cloud
---

 
There are Enterprise and Cloud versions of FeatureBase. While both use FeatureBase to store your data and power your analytics, there are key differences between the two when it comes to features. The capability matrices below help compare features between the two in key areas.

## Infrastructure

|Feature | Cloud  | Enterprise  | Notes  |
| ------ | ----- | ----------- | ----------- |
|Click to Deploy |  &#9745;| &#9744; |   |
|Automated Scale Up/Down|  &#9744;| &#9744; |   |
|Automated Scale In/Out |  &#9744;| &#9744; |   |
|Regional Deployment |  &#9744;| &#9745; |   |


## Data Ingestion

|Feature | Cloud  | Enterprise  | Notes  |
| ------ | ----- | ----------- | ----------- |
|Streaming (HTTPS)  |  &#9745;| &#9744; |   |
|Kafka (Pull-based) |  &#9744;| &#9745; | Client-side kafka consumption & push for Cloud |
|Database (Pull-based) |  &#9744;| &#9745; |  Client-side database consumption & push for Cloud |
|CSV/Bulk Ingest  |  &#9744;| &#9745; |  Client-side file consumption & push for Cloud |

## Data Consumption

|Feature | Cloud  | Enterprise  | Notes  |
| ------ | ----- | ----------- | ----------- |
|Query UI  |  &#9745;| &#9745; |   |
|FeatureBase SQL - HTTPS |  &#9745;| &#9744; | Any language/tool (Python, Go, etc) that can read over HTTPS  |
|FeatureBase PQL - HTTPS |  &#9745;| &#9745; | Any language/tool (Python, Go, etc) that can read over HTTPS  |
|gRPC Endpoint|  &#9744;| &#9745; |   |
|Postgres Endpoint |  &#9744;| &#9745; |   |
|Unbounded Queries (Advanced Queries) |  &#9744;| &#9745; | Cloud Limited to 6mb and/or 30sec  |
|PQL Query Builder|  &#9744;| &#9745; |   |
|Python Client |  &#9744;| &#9745; |   |
|Grafana Plug-In|  &#9744;| &#9745; |   |
|Postgres Lookup Database Option |  &#9744;| &#9745; |   |

## Operations

|Feature | Cloud  | Enterprise  | Notes  |
| ------ | ----- | ----------- | ----------- |
|Backup + Restore|  &#9744;| &#9745; |   |
|Data Replication |  &#9745;| &#9745; |  |
|Metrics & Monitoring|  &#9744;| &#9745; |   |
|Editable FeatureBase Config File|  &#9744;| &#9745; |   |

## Security

|Feature | Cloud  | Enterprise  | Notes  |
| ------ | ----- | ----------- | ----------- |
|Encryption In Flight |  &#9745;| &#9745; |  |
|Encryption at Rest |  &#9745;| &#9745; |   |
|Authentication + Authorization (OAuth) |  &#9745;| &#9745; |  |
|Role-Based Access Control (Basic)|  &#9744;| &#9745; |   |
|User Management|  &#9745;| &#9745; |  |
|Audit Logging|  &#9745;| &#9745; |   |
