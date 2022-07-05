---
id: createstreamingsource
title: Create An Ingest Endpoint
sidebar_label: Create An Ingest Endpoint
---

 **⚠ WARNING:** This page contains information that only applies to Molecula's Cloud offering. Additionally, this page represents a work in progress that is subject to frequent changes. 

In order to create an ingest endpoint, the following pre-requisites must be met:

1. A database exists that is in the “Running” state
- Click [here](/setting-up-featurebase/cloud/creating-deployment) to learn how to create a database
- Click [here](/reference/api/cloud/api) to see the database API docs

If both prerequisites have been met, you can navigate to “Data Sources” on the left hand navigation bar. Here you will see all of the sources in your organization. Click “New Source” to create a ingest endpoint. You will need to pick a database using a dropdown. This is populated by all the databases in your organization. The source name must be unique within the database and only contain lower case alphanumeric, hyphen and underscore characters. This should be descriptive for your organization to understand what data is streaming from this source as well as what environment this source is loading. For example, web clickstream data loading to production might be named web_clicks_production. 

Next, you will need to pick a table using a dropdown. This is populated by all the tables in your organization. If you don’t have a table, you may create one here by clicking “+ Create New Table”. To learn more about table creation, please navigate [here](/data-ingestion/cloud/tables). Clicking “Next” will take you to the field definition section where you will define the schema of records being streamed into this source. This schema is appended into the table the source is loading. For more information on schemas, go [here](/data-ingestion/cloud/streaming/streamingoverview). This source requires a JSON schema that can either pasted or uploaded. A small example schema is below:

```json
[
    {
        "name": "language",
        "path": [
            "language"
        ],
        "type": "string",
        "config": {
            "mutex": true
        }
    },
    {
        "name": "project_id",
        "path": [
            "project_id"
        ],
        "type": "id",
        "config": {
            "mutex": false
        }
    }
]
```

Once a schema is uploaded, you must indicate what field or combination of fields make up a unique record. This can be thought of as a traditional RDMBS primary key. There are two options: ID Field and Primary Key Fields. The id-field option should be used when there is an existing field in the data which uniquely identifies each record in the table and consists of nearly-contiguous positive integers. The primary-key-fields option should be used when the data has no fields that could be used for id-field. This option uses one or more fields (any type) and concatenates them to create unique record IDs for your table. Selecting either option will yield a dropdown of fields to choose from that is populated based on the schema you uploaded. Finally, an “Allow missing fields” checkbox can be checked or unchecked. Having this box checked means that one or more of the fields defined in the schema can be missing from the JSON records streamed in. If a field is missing, that field is left null with no bits set. If this box isn’t checked and a field is missing from the JSON records, an error will return and data will not be loaded into your table. 

Clicking “create source” will start the process of creating your ingest endpoint. This entire process can also be accomplished programmatically.

**HTTP API Reference:**
```shell
curl --location --request POST 'https://api.molecula.cloud/v1/sinks' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{    
    "name": "<sink name>",    
  	"sink_details": {
      "database_id": "<database_id>",
      "table": "<table name>"
    },
    "schema": {
        "id_field": "<field-name>",
        "allow_missing_fields": false,
        "definition": <schema-definition-json like example above>
    }
}'
```

You will be returned to the “Data Sources” page and see a new entry with your source name with the status of “CREATING”. After a few moments, this will update to have a status of “ACTIVE”, which means your ingest endpoint is ready to use. Clicking on the source you just created will reveal a details page that contains your schema, all of your selections from the creation phase, as well as the "ingest endpoint". This is the endpoint you will stream records to in order to get data into your tables. All of your ingest endpoint statuses can also be queried programmatically.

**HTTP API Reference:**
```shell
curl --location --request GET 'https://api.molecula.cloud/v1/deployments' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' 
```

Only sources in the "ACTIVE" state can be sent data for ingest.
