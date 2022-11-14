---
title: How do I create a table using the Cloud API?
---

<!-- source /cloud/cloud-ingestion/streaming-https-endpoint/cloud-streaming-quickstart.md -->

## Before you begin

{% include /cloud/cloud-before-begin.md %}
{% include install-curl.md %}
* [Learn about database shaping](/cloud/cloud-databases/cloud-db-shape)
* [Obtain ID token for SSH](/cloud/query-cloud-data/cloud-obtain-tokens-ssh)

## Syntax

```shell
curl --location --request POST 'https://api.featurebase.com/v2/databases' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "iris_demo_database",
    "database_options":{
        "shape": "<DbShape>"
    }
}'
```

## Arguments

| Argument | Description | Further information |
|---|---|---|
| IdToken | [Obtain the ID token](/cloud/query-cloud-data/cloud-obtain-tokens-ssh) |
| name | database name |
| DbShape | [Learn about database shaping](/cloud/cloud-databases/cloud-db-shape) |

## Example

```shell
curl --location --request POST 'https://api.featurebase.com/v2/databases' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "iris_demo_database",
    "database_options":{
        "shape": "8GB-Development"
    }
}'
```

## Further information

* [Query the status of a database](/cloud/query-cloud/cloud-query-db-status-ssh)
