---
title: Stream Data With An Ingest Endpoint
---

**⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes.

## Before you begin

{% include /cloud/database-dependencies.md %}

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

It is recommended to “microbatch” records before sending them to maximize ingest rates. The maximum amount of records that can be sent in a single request is constrained by the limits [here](/cloud/cloud-data-ingestion/streaming-https-endpoint/cloud-streaming-overview). The JSON blob does support nested structures, so it is up to your schema to define the `path` for each column’s value.

Clicking on your endpoint in the UI will take you to a screen with a "SEND RECORDS" button. This allows you to send data by pasting json records in the format shown above. This can also be accomplished programmatically. Below is an example of how multiple records are sent to the ingest endpoint:


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

For each POST request, each record is validated against the table's schema. Records that pass validation will be sent for ingestion while others that fail will return an error synchronously. The request response will sum the successes and errors and return the status and errors for each record similar to below:

```json
{
    "success_count": 1,
    "error_count": 1,
    "records": [
        {
            "status": "success"
        },
        {
            "status": "error",
            "error_code": "InvalidBody",
            "error_message": "Incorrect values for one or more of record fields"
        }
    ]
}
```

It's important to note that passing initial validation is not a guarantee a record will be ingested. Further errors can occur before a record is written. These errors can be found on the "ERRORS" tab in the UI. These errors can take a couple minutes to propagate. It is important to look for these errors to ensure there is no data loss. They can also be queried for programmatically:

```shell
curl --location --request GET 'https://api.featurebase.com/v2/sinks/<sink_id>/errors' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
```

The UI shows various metrics to help you monitor your ingest endpoint:

|Metric | Definition  |
| --- | ----------- |
|Ingest Rate   |  This describes the number of records per minute that are sent for ingest. This does not reflect the number of records actually ingested. For example, if a different error occurs or if a record sent is updating an existing record |
|Request Rate   |  This describes the number of POST requests per minute the endpoint is receiving |
|Error Rate     | This describes the number of records that failed validation per minute that were not sent for ingestion|

These metrics can be queried for programmatically as well:

```shell
curl --location --request GET 'https://api.featurebase.com/v2/sinks/<sink_id>/metrics' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
```

Note that the metrics endpoint will only store data for time periods where records are sent. Gaps between timestamps indicates the endpoint received no records during that period.

For a tutorial on how to go from nothing to a database with data streaming in, see the [Getting Started With Streaming](/cloud/cloud-data-ingestion/streaming-https-endpoint/cloud-streaming-quickstart).
