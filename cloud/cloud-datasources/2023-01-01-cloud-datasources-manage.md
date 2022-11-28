---
title: How do I manage my ingestion data sources in FeatureBase Cloud?
---

## Sources
* https://docs.featurebase.com/cloud/cloud-data-ingestion/streaming-https-endpoint/create-ingest-endpoint
* https://docs.featurebase.com/cloud/cloud-data-ingestion/streaming-https-endpoint/cloud-streaming-overview

{% include /concepts/ingestion-summary.md %}

## How do I set this up in FeatureBase cloud?

FeatureBase Cloud has the concept of data sources, which are configured with:
* name and destination database tables
* mapping of JSON source data to destination table columns.

A cloud data source has:
* an HTTPS endpoint used to receive data in JSON format
* a method of adding JSON batch files to run ingestion tasks
* metrics to indicate ingestion, error and request rates
* read-only column mapping
* an error log

## Before you begin

{% include /cloud/cloud-before-begin.md %}
{% include /cloud/cloud-ingest-before-begin.md %}

## How many data sources can I create?

{% include concepts/cloud-datasource-summary.md %}

##

## Source data

{% include /concepts/ingestion-json-summary.md %}

## Mapping data

Source and target columns:
* can be mapped in any order
* can omit mappings if desired, leaving an empty column

The exception is the ID column which is required for all mappings.

Dot notation us used in mapping, and can be derived from the JSON source.

For example,

| JSON data fragment | Dot notation for mapping |
|---|---|
| `"data": {"aircraftId": "40688E", "lat": 45.1199, "long": -43.416}` | data.aircraftID<br/>data.lat<br/>data.long |

## Trial accounts

{% include /cloud/trial-account-limits.md %}

## Naming standards

{% include /concepts/datasource-naming-standards.md %}

## Managing data sources in FeatureBase Cloud

* [Create a data source](/cloud/cloud-datasources/cloud-datasource-create)
* [Copy data source ingestion endpoint](/cloud/cloud-datasources/cloud-datasource-endpoint)
* [Setup JSON send record batches](/cloud/cloud-datasources/cloud-json-send-record)
* [Delete a data source](/cloud/cloud-datasources/cloud-datasource-delete)

## Managing data sources using the FeatureBase API

* [Data sources API reference](https://api-docs-featurebase-cloud.redoc.ly/v2#tag/Data-Sources)

## Next step

* [Learn how to stream data to a data source](/cloud/cloud-data-ingestion/cloud-ingest-overview.md)
