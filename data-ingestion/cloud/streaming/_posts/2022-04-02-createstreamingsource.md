---
id: createstreamingsource
title: Create An Ingest Endpoint
sidebar_label: Create An Ingest Endpoint
---

 **⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes. 

In order to create an ingest endpoint, the following pre-requisites must be met:

1. A database exists that is in the “Running” state
- Click [here](/setting-up-featurebase/cloud/creating-deployment) to learn how to create a database
- Click [here](/reference/api/cloud/api) to see the database API docs
2. A table exists in the database
- Click [here](/data-ingestion/cloud/tables) to learn how to create a table
- Click [here](/reference/api/cloud/api) to see the table API docs

If both prerequisites have been met, you can navigate to “Data Sources” on the left hand navigation bar. Here you will see all of the sources in your organization. Click “New Source” to create a ingest endpoint. You will need to pick a database using a dropdown. This is populated by all the databases in your organization. The source name can only contain lowercase alphanumeric characters, dashes (-), and underscores (_) but must start with an alphabetic character. This should be descriptive for your organization to understand what data is streaming from this source as well as what environment this source is loading. For example, web clickstream data loading to production might be named web_clicks_production. 

Next, you will need to pick a table using a dropdown. This is populated by all the tables in your database. Choosing a table will dynamically populate all of the columns in that table below. You must map how the JSON records you send to the endpoint relate to your table's columns. This is done with dot notation and represents the JSON "path" that leads to the column's value for that record. In the example record below `data.aircraftId` would map to the value `40688E`"

```json
{"id": "PD2tRswoE3:0:0", "timestamp": 1659981468260, "encoding": "json", "data": {"aircraftId": "40688E", "lat": 45.1199, "long": -43.416, "track": 250, "altitude": 37996, "speed": 495, "type": "B788", "reg": "G-ZBJA", "origin": "LHR", "destination": "BNA", "iataId": "", "icaoId": "BAW223N", "airline": "BAW"}, "name": "data"}
```

You must map something to the _id column as this is the primary key for your table and requires a value. All of the other columns are optional. You only should map the columns that will be populated by records sent to this ingest endpoint. Data for a single _id in your table might be populated by different endpoints, which is why these mappings are optional. 

After mapping the columns you want, you have to decide how to handle cases when a record arrives with missing values from those you mapped. You have the option to continue processing and store the record with the data that was found or to discard the entire batch of records sent and log an error. In the case of discarding the batch, each record will be ensured to have a value for each column *that has a mapping*. columns with no mapping are assumed to not be sent to this endpoint

Clicking “create source” will start the process of creating your ingest endpoint. This entire process can also be accomplished programmatically:

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
        "id_field": "<column-name>",
        "allow_missing_fields": false,
        "definition": <schema-definition-json like example below>
    }
}'
```

The syntax for the API differs from that in the UI, so please reference the [Streaming Overview](/data-ingestion/cloud/streaming/streamingoverview) for more details. a couple of key differences are below

- In the API, you must define the _id column of your table using one of two options: `id-field `and `primary-key-fields`.
- `allow_missing_fields` is "how to handle cases when a record arrives with missing values" described previously, and should be set as true if missing values is allowed.
- You must define the columns (including those that map to your _id column) in the "definition" like the example below. 

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

You will be returned to the “Data Sources” page and see a new entry with your source name with the status of “CREATING”. After a few moments, this will update to have a status of “ACTIVE”, which means your ingest endpoint is ready to use. Clicking on the source you just created will reveal a details page that contains your configuration details as well as the "ingest endpoint". This is the endpoint you will stream records to in order to get data into your tables. All of your ingest endpoint statuses can also be queried programmatically.

**HTTP API Reference:**
```shell
curl --location --request GET 'https://api.molecula.cloud/v2/sinks' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' 
```

Only sources in the "ACTIVE" state can be sent data for ingest.
