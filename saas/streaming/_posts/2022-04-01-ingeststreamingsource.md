---
id: ingeststreamingsource
title: Ingest Data from a Streaming (HTTPS) Source
sidebar_label: Ingest Data from a Streaming (HTTPS) Source
---

 **⚠ WARNING:** This page contains information that only applies to Molecula's SaaS offering. Additionally, this page represents a work in progress that is subject to frequent changes. 

Once an “ACTIVE” Streaming Source exists, data can be streamed to it over HTTPS via “POST” requests. Individual records or micro-batched payloads can be sent. Navigate [here](/saas/ingestdata/streamingoverview) to learn more about the required format for data, existing limits, and recommendations around streaming data. The UI currently only supports the ability to create a Streaming Source but not stream data to it. This must be done using the API. Based on the previous schema example, below is an example of how multiple records are sent to the streaming endpoint:


**HTTP API Reference:**
```shell
curl --location --request POST 'https://data.molecula.cloud/v1/sinks/<sink_id>' \
--header 'Authorization: <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "records": [
      { "value": { "language": "python", "project_id": 2 } },
      { "value": { "language": "golang", "project_id": 3 } }
  ]
}'
```

The full reference API for pushing data to an HTTPS Streaming Source can be found [here](/saas/saas-reference/controlplaneapi). For a tutorial on how to go from nothing to a deployment with data streaming in, see the [Getting Started page](/saas/saas-tutorials/saasquickstart).