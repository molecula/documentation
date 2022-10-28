---
id: ingeststreamingsource
title: Stream Data With An Ingest Endpoint
sidebar_label: Stream Data With An Ingest Endpoint
---

 **⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes. 

Once an “ACTIVE” ingest endpoint exists, data can be streamed to it over HTTPS via “POST” requests. Individual records or micro-batched payloads can be sent. 

### Record Format

Once an ingest endpoint is configured, data can be streamed to it. Each record should be composed of a JSON blob. One or many records can be sent in a single HTTPS request and should have the following syntax:

```json
{
    "records": [ 
        { "value": { <JSON blob containing columns of first record> } },
        { "value": { <JSON blob containing columns of second record> } },
        ...
    ]
}
```

It is recommended to “microbatch” records before sending them to maximize ingest rates. The maximum amount of records that can be sent in a single request is constrained by the limits [here](/cloud/data-ingestion/streaming/streamingoverview). The JSON blob does support nested structures, so it is up to your schema to define the `path` for each column’s value.

Below is an example of how multiple records are sent to the ingest endpoint:


**HTTP API Reference:**
```shell
curl --location --request POST 'https://data.featurebase.com/v2/sinks/<sink_id>' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "records": [
      { "value": { "language": "python", "project_id": 2 } },
      { "value": { "language": "golang", "project_id": 3 } }
  ]
}'
```

The full reference API for pushing data to an ingest endpoint can be found [here](/reference/api/cloud/api). For a tutorial on how to go from nothing to a database with data streaming in, see the [Getting Started With Streaming](/cloud/data-ingestion/streaming/tutorials/cloudquickstart).
