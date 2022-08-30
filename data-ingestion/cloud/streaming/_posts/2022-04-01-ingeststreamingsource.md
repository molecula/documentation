---
id: ingeststreamingsource
title: Stream Data With An Ingest Endpoint
sidebar_label: Stream Data With An Ingest Endpoint
---

 **⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes. 

Once an “ACTIVE” ingest endpoint exists, data can be streamed to it over HTTPS via “POST” requests. Individual records or micro-batched payloads can be sent. Navigate [here](/data-ingestion/cloud/streaming/streamingoverview) to learn more about the required format for data, existing limits, and recommendations around streaming data. The UI currently only supports the ability to create a ingest endpoint but not stream data to it. This must be done using the API. Based on the previous schema example, below is an example of how multiple records are sent to the ingest endpoint:


**HTTP API Reference:**
```shell
curl --location --request POST 'https://data.molecula.cloud/v1/sinks/<sink_id>' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "records": [
      { "value": { "language": "python", "project_id": 2 } },
      { "value": { "language": "golang", "project_id": 3 } }
  ]
}'
```

The full reference API for pushing data to an ingest endpoint can be found [here](/reference/api/cloud/api). For a tutorial on how to go from nothing to a database with data streaming in, see the [Getting Started page](/quick-start-guide/cloud).
