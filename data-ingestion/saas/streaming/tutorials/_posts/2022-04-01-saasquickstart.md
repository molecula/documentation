---
id: saasquickstart
title: Getting Started With Streaming
sidebar_label: Getting Started With Streaming
---

 **⚠ WARNING:** This page contains information that only applies to Molecula's SaaS offering. Additionally, this page represents a work in progress that is subject to frequent changes. 


## Prerequisites

The following QuickStart guide requires the following:

1. You have signed up with Molecula and have a user account and your credentials
2. You have a linux environment capable of running cURL commands

## Getting Started

The guide will take you from nothing in the product to having a small deployment with data to query. Its purpose is to get you up and running quickly, while simultaneously teaching you how to use the product. While this tutorial will populate most information for you, there will be inputs required from you in the code snippets (indicated by <> symbols)

**⚠ WARNING:** This process creates resources that can create additional costs for you as a customer.

### Getting A Token

Molecula uses Oauth2.0 for all authorization, so every API call must be accompanied with a valid token. You can get tokens by passing your credentials to https://id.molecula.cloud.

Inputs:
1. USERNAME - your email
2. PASSWORD - your password

**HTTP API Reference:**
```shell
curl --location --request POST 'https://id.molecula.cloud' \
--data-raw '{
    "USERNAME": "<username>",
    "PASSWORD": "<password>"
}'
```

3 tokens are returned: Access, ID, and Refresh. Use the ID token for all of your API calls as the Authorization header:

**HTTP API Reference:**
```shell
--header 'Authorization: <IdToken>' \
```

### Create A Deployment

Deployments are clusters of FeatureBase nodes. All of your data will live in tables within FeatureBase. You can think of a deployment as a database. Molecula offers deployment sizes to choose from. For this guide, we will be using the "8GB" option. For more information on deployments, see [Deployments Overview](/setting-up-featurebase/saas/deployments-overview). The below command will start creating your deployment

Inputs:
1. IdToken - IdToken from auth token call to pass as "Authorization" header
2. deployment_name - the name you want to give your deployment i.e iris_demo_deployment
3. deployment_shape - deployment shape/memory you are choosing i.e. 8GB

**HTTP API Reference:**
```shell
curl --location --request POST 'https://api.molecula.cloud/v1/deployments' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "iris_demo_deployment",
    "deployment_options":{
        "shape": "8GB"
    }
}'
```

A deployment takes some time to create. You can look at all of your deployments and their statuses. You should be able to see the "iris_demo_deployment" as "Creating".

**HTTP API Reference:**
```shell
curl --location --request GET 'https://api.molecula.cloud/v1/deployments' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' 
```

Grab your deployment’s id. This is a unique id for your deployment. Once your deployment is "Running" (a minute or two), you can move to the next step.

### Ingest Data

Once a deployment is running, you will want to start loading data into it. Sources are configurable resources that load data into deployments. This section will help you creating a "Streaming (HTTPS)" Source, which will yield a persistent endpoint that allows you to push data into your deployment over HTTPS. For more information on ingesting data, see [Ingest Data](/data-ingestion/saas/ingestoverview).

#### Create A Table

A table is an object within a deployment that stores related data. You must create a table before you can ingest data.

Inputs:
1. IdToken - IdToken from auth token call to pass as "Authorization" header
2. table_name - The name you want to give your table i.e. iris_table
3. table_description - The description of the table i.e. "table holding flower data"
4. deployment id - The ID returned from running a get on the /deployments endpoint above

**HTTP API Reference:**
```shell
curl --location --request POST 'https://api.molecula.cloud/v1/tables/<deployment_id>' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "iris_table",
    "description": "table holding flower data"    
}'
```

#### Create A Streaming Source

After a table exists, you can configure a source to load data into it. The “Streaming (HTTPS)” source configuration will yield a persistent endpoint that allows you to stream data to. Here you can see our JSON schema that details the data being streamed to the source. The below schema contains various flower species and their measurements.

Inputs:
1. IdToken - IdToken from auth token call to pass as "Authorization" header
2. table_name - The name you want to give your table i.e. iris_table
3. source_name - The name you want to give your source i.e. iris_streaming_source
4. deployment id - The unique ID of your deployment
5. schema - a JSON blob that contains information about the data streaming into the source.

**HTTP API Reference:**
```shell
curl --location --request POST 'https://api.molecula.cloud/v1/sinks' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{    
    "name": "iris_streaming_source",    
  	"sink_details": {
      "deployment_id": "<deployment_id>",
      "table": "iris_table"
    },
    "schema": {
        "id_field": "id",
        "allow_missing_fields": false,
        "definition": [
        {
            "name": "id",
            "path": ["id"],
            "type": "id",
            "config": {
              "Mutex": false
            }
        },
        {
            "name": "sepallength",
            "path": ["sepalLength"],
            "type": "decimal",
            "config": {
              "Scale": 2
            }
        },
        {
            "name": "sepalwidth",
            "path": ["sepalWidth"],
            "type": "decimal",
            "config": {
              "Scale": 2
            }
        },
        {
            "name": "petallength",
            "path": ["petalLength"],
            "type": "decimal",
            "config": {
              "Scale": 2
            }
        },
        {
            "name": "petalwidth",
            "path": ["petalWidth"],
            "type": "decimal",
            "config": {
              "Scale": 2
            }
        },
        {
            "name": "species",
            "path": ["species"],
            "type": "string",
            "config": {
              "Mutex": true
            }
        }]
    }
}'
```

Like deployments, sources takes some time to create. You can look at all of your sources and their statuses. You should be able to see the "iris_streaming_source" as "Creating".

**HTTP API Reference:**
```shell
curl --location --request GET 'https://api.molecula.cloud/v1/sinks' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' 
```

Grab your source's id. This is a unique id for your source. Once your source is "Running" (a minute or two), you can move to the next step.

#### Ingest Data

We now have an endpoint we can stream data to. This guide will only send one micro-batched payload of records, but data can be continually pushed to this endpoint. For more information, please see the [Streaming (HTTPS)](/data-ingestion/saas/streaming/streamingoverview).

Inputs:
1. IdToken - IdToken from auth token call to pass as "Authorization" header
2. source id - The unique ID of your source
3. records - JSON blobs that each represent an individual record

**HTTP API Reference:**
```shell
curl --location --request POST 'https://data.molecula.cloud/v1/sinks/<sourceId>' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "records": [
    { "value": {"id": 1, "sepalLength": "5.1", "sepalWidth": "3.5", "petalLength": "1.4", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 2, "sepalLength": "4.9", "sepalWidth": "3.0", "petalLength": "1.4", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 3, "sepalLength": "4.7", "sepalWidth": "3.2", "petalLength": "1.3", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 4, "sepalLength": "4.6", "sepalWidth": "3.1", "petalLength": "1.5", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 5, "sepalLength": "5.0", "sepalWidth": "3.6", "petalLength": "1.4", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 6, "sepalLength": "5.4", "sepalWidth": "3.9", "petalLength": "1.7", "petalWidth": "0.4", "species": "setosa"}},
    { "value": {"id": 7, "sepalLength": "4.6", "sepalWidth": "3.4", "petalLength": "1.4", "petalWidth": "0.3", "species": "setosa"}},
    { "value": {"id": 8, "sepalLength": "5.0", "sepalWidth": "3.4", "petalLength": "1.5", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 9, "sepalLength": "4.4", "sepalWidth": "2.9", "petalLength": "1.4", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 10, "sepalLength": "4.9", "sepalWidth": "3.1", "petalLength": "1.5", "petalWidth": "0.1", "species": "setosa"}},
    { "value": {"id": 11, "sepalLength": "5.4", "sepalWidth": "3.7", "petalLength": "1.5", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 12, "sepalLength": "4.8", "sepalWidth": "3.4", "petalLength": "1.6", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 13, "sepalLength": "4.8", "sepalWidth": "3.0", "petalLength": "1.4", "petalWidth": "0.1", "species": "setosa"}},
    { "value": {"id": 14, "sepalLength": "4.3", "sepalWidth": "3.0", "petalLength": "1.1", "petalWidth": "0.1", "species": "setosa"}},
    { "value": {"id": 15, "sepalLength": "5.8", "sepalWidth": "4.0", "petalLength": "1.2", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 16, "sepalLength": "5.7", "sepalWidth": "4.4", "petalLength": "1.5", "petalWidth": "0.4", "species": "setosa"}},
    { "value": {"id": 17, "sepalLength": "5.4", "sepalWidth": "3.9", "petalLength": "1.3", "petalWidth": "0.4", "species": "setosa"}},
    { "value": {"id": 18, "sepalLength": "5.1", "sepalWidth": "3.5", "petalLength": "1.4", "petalWidth": "0.3", "species": "setosa"}},
    { "value": {"id": 19, "sepalLength": "5.7", "sepalWidth": "3.8", "petalLength": "1.7", "petalWidth": "0.3", "species": "setosa"}},
    { "value": {"id": 20, "sepalLength": "5.1", "sepalWidth": "3.8", "petalLength": "1.5", "petalWidth": "0.3", "species": "setosa"}},
    { "value": {"id": 21, "sepalLength": "5.4", "sepalWidth": "3.4", "petalLength": "1.7", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 22, "sepalLength": "5.1", "sepalWidth": "3.7", "petalLength": "1.5", "petalWidth": "0.4", "species": "setosa"}},
    { "value": {"id": 23, "sepalLength": "4.6", "sepalWidth": "3.6", "petalLength": "1.0", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 24, "sepalLength": "5.1", "sepalWidth": "3.3", "petalLength": "1.7", "petalWidth": "0.5", "species": "setosa"}},
    { "value": {"id": 25, "sepalLength": "4.8", "sepalWidth": "3.4", "petalLength": "1.9", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 26, "sepalLength": "5.0", "sepalWidth": "3.0", "petalLength": "1.6", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 27, "sepalLength": "5.0", "sepalWidth": "3.4", "petalLength": "1.6", "petalWidth": "0.4", "species": "setosa"}},
    { "value": {"id": 28, "sepalLength": "5.2", "sepalWidth": "3.5", "petalLength": "1.5", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 29, "sepalLength": "5.2", "sepalWidth": "3.4", "petalLength": "1.4", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 30, "sepalLength": "4.7", "sepalWidth": "3.2", "petalLength": "1.6", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 31, "sepalLength": "4.8", "sepalWidth": "3.1", "petalLength": "1.6", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 32, "sepalLength": "5.4", "sepalWidth": "3.4", "petalLength": "1.5", "petalWidth": "0.4", "species": "setosa"}},
    { "value": {"id": 33, "sepalLength": "5.2", "sepalWidth": "4.1", "petalLength": "1.5", "petalWidth": "0.1", "species": "setosa"}},
    { "value": {"id": 34, "sepalLength": "5.5", "sepalWidth": "4.2", "petalLength": "1.4", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 35, "sepalLength": "4.9", "sepalWidth": "3.1", "petalLength": "1.5", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 36, "sepalLength": "5.0", "sepalWidth": "3.2", "petalLength": "1.2", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 37, "sepalLength": "5.5", "sepalWidth": "3.5", "petalLength": "1.3", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 38, "sepalLength": "4.9", "sepalWidth": "3.6", "petalLength": "1.4", "petalWidth": "0.1", "species": "setosa"}},
    { "value": {"id": 39, "sepalLength": "4.4", "sepalWidth": "3.0", "petalLength": "1.3", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 40, "sepalLength": "5.1", "sepalWidth": "3.4", "petalLength": "1.5", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 41, "sepalLength": "5.0", "sepalWidth": "3.5", "petalLength": "1.3", "petalWidth": "0.3", "species": "setosa"}},
    { "value": {"id": 42, "sepalLength": "4.5", "sepalWidth": "2.3", "petalLength": "1.3", "petalWidth": "0.3", "species": "setosa"}},
    { "value": {"id": 43, "sepalLength": "4.4", "sepalWidth": "3.2", "petalLength": "1.3", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 44, "sepalLength": "5.0", "sepalWidth": "3.5", "petalLength": "1.6", "petalWidth": "0.6", "species": "setosa"}},
    { "value": {"id": 45, "sepalLength": "5.1", "sepalWidth": "3.8", "petalLength": "1.9", "petalWidth": "0.4", "species": "setosa"}},
    { "value": {"id": 46, "sepalLength": "4.8", "sepalWidth": "3.0", "petalLength": "1.4", "petalWidth": "0.3", "species": "setosa"}},
    { "value": {"id": 47, "sepalLength": "5.1", "sepalWidth": "3.8", "petalLength": "1.6", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 48, "sepalLength": "4.6", "sepalWidth": "3.2", "petalLength": "1.4", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 49, "sepalLength": "5.3", "sepalWidth": "3.7", "petalLength": "1.5", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 50, "sepalLength": "5.0", "sepalWidth": "3.3", "petalLength": "1.4", "petalWidth": "0.2", "species": "setosa"}},
    { "value": {"id": 51, "sepalLength": "7.0", "sepalWidth": "3.2", "petalLength": "4.7", "petalWidth": "1.4", "species": "versicolor"}},
    { "value": {"id": 52, "sepalLength": "6.4", "sepalWidth": "3.2", "petalLength": "4.5", "petalWidth": "1.5", "species": "versicolor"}},
    { "value": {"id": 53, "sepalLength": "6.9", "sepalWidth": "3.1", "petalLength": "4.9", "petalWidth": "1.5", "species": "versicolor"}},
    { "value": {"id": 54, "sepalLength": "5.5", "sepalWidth": "2.3", "petalLength": "4.0", "petalWidth": "1.3", "species": "versicolor"}},
    { "value": {"id": 55, "sepalLength": "6.5", "sepalWidth": "2.8", "petalLength": "4.6", "petalWidth": "1.5", "species": "versicolor"}},
    { "value": {"id": 56, "sepalLength": "5.7", "sepalWidth": "2.8", "petalLength": "4.5", "petalWidth": "1.3", "species": "versicolor"}},
    { "value": {"id": 57, "sepalLength": "6.3", "sepalWidth": "3.3", "petalLength": "4.7", "petalWidth": "1.6", "species": "versicolor"}},
    { "value": {"id": 58, "sepalLength": "4.9", "sepalWidth": "2.4", "petalLength": "3.3", "petalWidth": "1.0", "species": "versicolor"}},
    { "value": {"id": 59, "sepalLength": "6.6", "sepalWidth": "2.9", "petalLength": "4.6", "petalWidth": "1.3", "species": "versicolor"}},
    { "value": {"id": 60, "sepalLength": "5.2", "sepalWidth": "2.7", "petalLength": "3.9", "petalWidth": "1.4", "species": "versicolor"}},
    { "value": {"id": 61, "sepalLength": "5.0", "sepalWidth": "2.0", "petalLength": "3.5", "petalWidth": "1.0", "species": "versicolor"}},
    { "value": {"id": 62, "sepalLength": "5.9", "sepalWidth": "3.0", "petalLength": "4.2", "petalWidth": "1.5", "species": "versicolor"}},
    { "value": {"id": 63, "sepalLength": "6.0", "sepalWidth": "2.2", "petalLength": "4.0", "petalWidth": "1.0", "species": "versicolor"}},
    { "value": {"id": 64, "sepalLength": "6.1", "sepalWidth": "2.9", "petalLength": "4.7", "petalWidth": "1.4", "species": "versicolor"}},
    { "value": {"id": 65, "sepalLength": "5.6", "sepalWidth": "2.9", "petalLength": "3.6", "petalWidth": "1.3", "species": "versicolor"}},
    { "value": {"id": 66, "sepalLength": "6.7", "sepalWidth": "3.1", "petalLength": "4.4", "petalWidth": "1.4", "species": "versicolor"}},
    { "value": {"id": 67, "sepalLength": "5.6", "sepalWidth": "3.0", "petalLength": "4.5", "petalWidth": "1.5", "species": "versicolor"}},
    { "value": {"id": 68, "sepalLength": "5.8", "sepalWidth": "2.7", "petalLength": "4.1", "petalWidth": "1.0", "species": "versicolor"}},
    { "value": {"id": 69, "sepalLength": "6.2", "sepalWidth": "2.2", "petalLength": "4.5", "petalWidth": "1.5", "species": "versicolor"}},
    { "value": {"id": 70, "sepalLength": "5.6", "sepalWidth": "2.5", "petalLength": "3.9", "petalWidth": "1.1", "species": "versicolor"}},
    { "value": {"id": 71, "sepalLength": "5.9", "sepalWidth": "3.2", "petalLength": "4.8", "petalWidth": "1.8", "species": "versicolor"}},
    { "value": {"id": 72, "sepalLength": "6.1", "sepalWidth": "2.8", "petalLength": "4.0", "petalWidth": "1.3", "species": "versicolor"}},
    { "value": {"id": 73, "sepalLength": "6.3", "sepalWidth": "2.5", "petalLength": "4.9", "petalWidth": "1.5", "species": "versicolor"}},
    { "value": {"id": 74, "sepalLength": "6.1", "sepalWidth": "2.8", "petalLength": "4.7", "petalWidth": "1.2", "species": "versicolor"}},
    { "value": {"id": 75, "sepalLength": "6.4", "sepalWidth": "2.9", "petalLength": "4.3", "petalWidth": "1.3", "species": "versicolor"}},
    { "value": {"id": 76, "sepalLength": "6.6", "sepalWidth": "3.0", "petalLength": "4.4", "petalWidth": "1.4", "species": "versicolor"}},
    { "value": {"id": 77, "sepalLength": "6.8", "sepalWidth": "2.8", "petalLength": "4.8", "petalWidth": "1.4", "species": "versicolor"}},
    { "value": {"id": 78, "sepalLength": "6.7", "sepalWidth": "3.0", "petalLength": "5.0", "petalWidth": "1.7", "species": "versicolor"}},
    { "value": {"id": 79, "sepalLength": "6.0", "sepalWidth": "2.9", "petalLength": "4.5", "petalWidth": "1.5", "species": "versicolor"}},
    { "value": {"id": 80, "sepalLength": "5.7", "sepalWidth": "2.6", "petalLength": "3.5", "petalWidth": "1.0", "species": "versicolor"}},
    { "value": {"id": 81, "sepalLength": "5.5", "sepalWidth": "2.4", "petalLength": "3.8", "petalWidth": "1.1", "species": "versicolor"}},
    { "value": {"id": 82, "sepalLength": "5.5", "sepalWidth": "2.4", "petalLength": "3.7", "petalWidth": "1.0", "species": "versicolor"}},
    { "value": {"id": 83, "sepalLength": "5.8", "sepalWidth": "2.7", "petalLength": "3.9", "petalWidth": "1.2", "species": "versicolor"}},
    { "value": {"id": 84, "sepalLength": "6.0", "sepalWidth": "2.7", "petalLength": "5.1", "petalWidth": "1.6", "species": "versicolor"}},
    { "value": {"id": 85, "sepalLength": "5.4", "sepalWidth": "3.0", "petalLength": "4.5", "petalWidth": "1.5", "species": "versicolor"}},
    { "value": {"id": 86, "sepalLength": "6.0", "sepalWidth": "3.4", "petalLength": "4.5", "petalWidth": "1.6", "species": "versicolor"}},
    { "value": {"id": 87, "sepalLength": "6.7", "sepalWidth": "3.1", "petalLength": "4.7", "petalWidth": "1.5", "species": "versicolor"}},
    { "value": {"id": 88, "sepalLength": "6.3", "sepalWidth": "2.3", "petalLength": "4.4", "petalWidth": "1.3", "species": "versicolor"}},
    { "value": {"id": 89, "sepalLength": "5.6", "sepalWidth": "3.0", "petalLength": "4.1", "petalWidth": "1.3", "species": "versicolor"}},
    { "value": {"id": 90, "sepalLength": "5.5", "sepalWidth": "2.5", "petalLength": "4.0", "petalWidth": "1.3", "species": "versicolor"}},
    { "value": {"id": 91, "sepalLength": "5.5", "sepalWidth": "2.6", "petalLength": "4.4", "petalWidth": "1.2", "species": "versicolor"}},
    { "value": {"id": 92, "sepalLength": "6.1", "sepalWidth": "3.0", "petalLength": "4.6", "petalWidth": "1.4", "species": "versicolor"}},
    { "value": {"id": 93, "sepalLength": "5.8", "sepalWidth": "2.6", "petalLength": "4.0", "petalWidth": "1.2", "species": "versicolor"}},
    { "value": {"id": 94, "sepalLength": "5.0", "sepalWidth": "2.3", "petalLength": "3.3", "petalWidth": "1.0", "species": "versicolor"}},
    { "value": {"id": 95, "sepalLength": "5.6", "sepalWidth": "2.7", "petalLength": "4.2", "petalWidth": "1.3", "species": "versicolor"}},
    { "value": {"id": 96, "sepalLength": "5.7", "sepalWidth": "3.0", "petalLength": "4.2", "petalWidth": "1.2", "species": "versicolor"}},
    { "value": {"id": 97, "sepalLength": "5.7", "sepalWidth": "2.9", "petalLength": "4.2", "petalWidth": "1.3", "species": "versicolor"}},
    { "value": {"id": 98, "sepalLength": "6.2", "sepalWidth": "2.9", "petalLength": "4.3", "petalWidth": "1.3", "species": "versicolor"}},
    { "value": {"id": 99, "sepalLength": "5.1", "sepalWidth": "2.5", "petalLength": "3.0", "petalWidth": "1.1", "species": "versicolor"}},
    { "value": {"id": 100, "sepalLength": "5.7", "sepalWidth": "2.8", "petalLength": "4.1", "petalWidth": "1.3", "species": "versicolor"}},
    { "value": {"id": 101, "sepalLength": "6.3", "sepalWidth": "3.3", "petalLength": "6.0", "petalWidth": "2.5", "species": "virginica"}},
    { "value": {"id": 102, "sepalLength": "5.8", "sepalWidth": "2.7", "petalLength": "5.1", "petalWidth": "1.9", "species": "virginica"}},
    { "value": {"id": 103, "sepalLength": "7.1", "sepalWidth": "3.0", "petalLength": "5.9", "petalWidth": "2.1", "species": "virginica"}},
    { "value": {"id": 104, "sepalLength": "6.3", "sepalWidth": "2.9", "petalLength": "5.6", "petalWidth": "1.8", "species": "virginica"}},
    { "value": {"id": 105, "sepalLength": "6.5", "sepalWidth": "3.0", "petalLength": "5.8", "petalWidth": "2.2", "species": "virginica"}},
    { "value": {"id": 106, "sepalLength": "7.6", "sepalWidth": "3.0", "petalLength": "6.6", "petalWidth": "2.1", "species": "virginica"}},
    { "value": {"id": 107, "sepalLength": "4.9", "sepalWidth": "2.5", "petalLength": "4.5", "petalWidth": "1.7", "species": "virginica"}},
    { "value": {"id": 108, "sepalLength": "7.3", "sepalWidth": "2.9", "petalLength": "6.3", "petalWidth": "1.8", "species": "virginica"}},
    { "value": {"id": 109, "sepalLength": "6.7", "sepalWidth": "2.5", "petalLength": "5.8", "petalWidth": "1.8", "species": "virginica"}},
    { "value": {"id": 110, "sepalLength": "7.2", "sepalWidth": "3.6", "petalLength": "6.1", "petalWidth": "2.5", "species": "virginica"}},
    { "value": {"id": 111, "sepalLength": "6.5", "sepalWidth": "3.2", "petalLength": "5.1", "petalWidth": "2.0", "species": "virginica"}},
    { "value": {"id": 112, "sepalLength": "6.4", "sepalWidth": "2.7", "petalLength": "5.3", "petalWidth": "1.9", "species": "virginica"}},
    { "value": {"id": 113, "sepalLength": "6.8", "sepalWidth": "3.0", "petalLength": "5.5", "petalWidth": "2.1", "species": "virginica"}},
    { "value": {"id": 114, "sepalLength": "5.7", "sepalWidth": "2.5", "petalLength": "5.0", "petalWidth": "2.0", "species": "virginica"}},
    { "value": {"id": 115, "sepalLength": "5.8", "sepalWidth": "2.8", "petalLength": "5.1", "petalWidth": "2.4", "species": "virginica"}},
    { "value": {"id": 116, "sepalLength": "6.4", "sepalWidth": "3.2", "petalLength": "5.3", "petalWidth": "2.3", "species": "virginica"}},
    { "value": {"id": 117, "sepalLength": "6.5", "sepalWidth": "3.0", "petalLength": "5.5", "petalWidth": "1.8", "species": "virginica"}},
    { "value": {"id": 118, "sepalLength": "7.7", "sepalWidth": "3.8", "petalLength": "6.7", "petalWidth": "2.2", "species": "virginica"}},
    { "value": {"id": 119, "sepalLength": "7.7", "sepalWidth": "2.6", "petalLength": "6.9", "petalWidth": "2.3", "species": "virginica"}},
    { "value": {"id": 120, "sepalLength": "6.0", "sepalWidth": "2.2", "petalLength": "5.0", "petalWidth": "1.5", "species": "virginica"}},
    { "value": {"id": 121, "sepalLength": "6.9", "sepalWidth": "3.2", "petalLength": "5.7", "petalWidth": "2.3", "species": "virginica"}},
    { "value": {"id": 122, "sepalLength": "5.6", "sepalWidth": "2.8", "petalLength": "4.9", "petalWidth": "2.0", "species": "virginica"}},
    { "value": {"id": 123, "sepalLength": "7.7", "sepalWidth": "2.8", "petalLength": "6.7", "petalWidth": "2.0", "species": "virginica"}},
    { "value": {"id": 124, "sepalLength": "6.3", "sepalWidth": "2.7", "petalLength": "4.9", "petalWidth": "1.8", "species": "virginica"}},
    { "value": {"id": 125, "sepalLength": "6.7", "sepalWidth": "3.3", "petalLength": "5.7", "petalWidth": "2.1", "species": "virginica"}},
    { "value": {"id": 126, "sepalLength": "7.2", "sepalWidth": "3.2", "petalLength": "6.0", "petalWidth": "1.8", "species": "virginica"}},
    { "value": {"id": 127, "sepalLength": "6.2", "sepalWidth": "2.8", "petalLength": "4.8", "petalWidth": "1.8", "species": "virginica"}},
    { "value": {"id": 128, "sepalLength": "6.1", "sepalWidth": "3.0", "petalLength": "4.9", "petalWidth": "1.8", "species": "virginica"}},
    { "value": {"id": 129, "sepalLength": "6.4", "sepalWidth": "2.8", "petalLength": "5.6", "petalWidth": "2.1", "species": "virginica"}},
    { "value": {"id": 130, "sepalLength": "7.2", "sepalWidth": "3.0", "petalLength": "5.8", "petalWidth": "1.6", "species": "virginica"}},
    { "value": {"id": 131, "sepalLength": "7.4", "sepalWidth": "2.8", "petalLength": "6.1", "petalWidth": "1.9", "species": "virginica"}},
    { "value": {"id": 132, "sepalLength": "7.9", "sepalWidth": "3.8", "petalLength": "6.4", "petalWidth": "2.0", "species": "virginica"}},
    { "value": {"id": 133, "sepalLength": "6.4", "sepalWidth": "2.8", "petalLength": "5.6", "petalWidth": "2.2", "species": "virginica"}},
    { "value": {"id": 134, "sepalLength": "6.3", "sepalWidth": "2.8", "petalLength": "5.1", "petalWidth": "1.5", "species": "virginica"}},
    { "value": {"id": 135, "sepalLength": "6.1", "sepalWidth": "2.6", "petalLength": "5.6", "petalWidth": "1.4", "species": "virginica"}},
    { "value": {"id": 136, "sepalLength": "7.7", "sepalWidth": "3.0", "petalLength": "6.1", "petalWidth": "2.3", "species": "virginica"}},
    { "value": {"id": 137, "sepalLength": "6.3", "sepalWidth": "3.4", "petalLength": "5.6", "petalWidth": "2.4", "species": "virginica"}},
    { "value": {"id": 138, "sepalLength": "6.4", "sepalWidth": "3.1", "petalLength": "5.5", "petalWidth": "1.8", "species": "virginica"}},
    { "value": {"id": 139, "sepalLength": "6.0", "sepalWidth": "3.0", "petalLength": "4.8", "petalWidth": "1.8", "species": "virginica"}},
    { "value": {"id": 140, "sepalLength": "6.9", "sepalWidth": "3.1", "petalLength": "5.4", "petalWidth": "2.1", "species": "virginica"}},
    { "value": {"id": 141, "sepalLength": "6.7", "sepalWidth": "3.1", "petalLength": "5.6", "petalWidth": "2.4", "species": "virginica"}},
    { "value": {"id": 142, "sepalLength": "6.9", "sepalWidth": "3.1", "petalLength": "5.1", "petalWidth": "2.3", "species": "virginica"}},
    { "value": {"id": 143, "sepalLength": "5.8", "sepalWidth": "2.7", "petalLength": "5.1", "petalWidth": "1.9", "species": "virginica"}},
    { "value": {"id": 144, "sepalLength": "6.8", "sepalWidth": "3.2", "petalLength": "5.9", "petalWidth": "2.3", "species": "virginica"}},
    { "value": {"id": 145, "sepalLength": "6.7", "sepalWidth": "3.3", "petalLength": "5.7", "petalWidth": "2.5", "species": "virginica"}},
    { "value": {"id": 146, "sepalLength": "6.7", "sepalWidth": "3.0", "petalLength": "5.2", "petalWidth": "2.3", "species": "virginica"}},
    { "value": {"id": 147, "sepalLength": "6.3", "sepalWidth": "2.5", "petalLength": "5.0", "petalWidth": "1.9", "species": "virginica"}},
    { "value": {"id": 148, "sepalLength": "6.5", "sepalWidth": "3.0", "petalLength": "5.2", "petalWidth": "2.0", "species": "virginica"}},
    { "value": {"id": 149, "sepalLength": "6.2", "sepalWidth": "3.4", "petalLength": "5.4", "petalWidth": "2.3", "species": "virginica"}},
    { "value": {"id": 150, "sepalLength": "5.9", "sepalWidth": "3.0", "petalLength": "5.1", "petalWidth": "1.8", "species": "virginica"}}
  ]
}'
```

This will yield a response that details the number of successes and errors from the request, as well as a status for each record. You should see something similar return below and can move on to the next step

```json
{'success_count': 150,
 'error_count': 0,
 'records': [{'status': 'success'},
  {'status': 'success'},
  ...
```

### Consume Data

Now that data is loaded into your table, you are able to query it. Data is queried using either PQL (Pilosa Query Language), our native query language, or the limited set of SQL we support. An example of both can be seen below:

Inputs:
1. IdToken - IdToken from auth token call to pass as "Authorization" header
2. deployment id - The unique ID of your deployment
3. language - the query language being used i.e. "pql" or "sql"
4. statement - the query to run i.e. "select * from iris_table"


**HTTP API Reference (SQL):**
```shell
curl --location --request POST 'https://data.molecula.cloud/v1/deployments/<deployment id>/query' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{ 
    "language": "sql", 
    "statement": "select * from iris_table limit 10"
}'
```

**HTTP API Reference (PQL):**
PQL
```shell
curl --location --request POST 'https://data.molecula.cloud/v1/deployments/<deployment id>/query' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{ 
    "language": "pql", 
    "statement": "[iris_table]GroupBy(Rows(species))"
}'
```

Queries will yield JSON responses containing the requested data. Now is a good time to explore running other queries if you would like. This marks the end of the quick start. While this guide doesn't show the massive scale FeatureBase can perform against, it does show how fast and simple it is to get started. Please feel free to reach out with any questions or feedback you have for this guide.

### Environment Cleanup

 Lastly, it is important to delete these resources to avoid creating costs for your organization. You'll find commands to do so below. Please note the order to deleting resources is important, and resources do take time to fully shutdown. All Successful delete requests should result in a 202 response.

#### Delete Source

Inputs:
1. IdToken - IdToken from auth token call to pass as "Authorization" header
2. source id - The unique ID of your source

**HTTP API Reference:**
```shell
curl --location --request DELETE 'https://api.molecula.cloud/v1/sinks/<sourceid>' \
--header 'Authorization: Bearer <IdToken>'  
```

This will take some time to delete. You can check the status of the delete with the command below until the resource is no longer found.

**HTTP API Reference:**
```shell
curl --location --request GET 'https://api.molecula.cloud/v1/sinks/<sourceid>' \
--header 'Authorization: Bearer <IdToken>'  
```

#### Delete Table

Inputs:
1. IdToken - IdToken from auth token call to pass as "Authorization" header
2. deployment id - The unique ID of your deployment
2. table_name - The name you want to give your table i.e. iris_table

**HTTP API Reference:**
```shell
curl --location --request DELETE 'https://api.molecula.cloud/v1/tables/<deployment id>/iris_table' \
--header 'Authorization: Bearer <IdToken>'  
```

#### Delete Deployment

Inputs:
1. IdToken - IdToken from auth token call to pass as "Authorization" header
2. deployment id - The unique ID of your deployment

**HTTP API Reference:**
```shell
curl --location --request DELETE 'https://api.molecula.cloud/v1/deployments/<deployment id>' \
--header 'Authorization: Bearer <IdToken>' 
```

This will take some time to delete. You can check the status of the delete with the command below until the resource is no longer found.

**HTTP API Reference:**
```shell
curl --location --request GET 'https://api.molecula.cloud/v1/deployments/<deployment id>' \
--header 'Authorization: Bearer <IdToken>' 
```

