---
id: createstreamingsource
title: Create An Ingest Endpoint
sidebar_label: Create An Ingest Endpoint
---

 **⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes. 

In order to create an ingest endpoint, the following pre-requisites must be met:

1. A database exists that is in the “Running” state
- Click [here](/cloud/cloud-setup/creating-database) to learn how to create a database
- Click [here](/cloud/api) to see the database API docs
2. A table exists in the database
- Click [here](/cloud/cloud-data-ingestion/tables) to learn how to create a table
- Click [here](/cloud/api) to see the table API docs

If both prerequisites have been met, you can navigate to “Data Sources” on the left hand navigation bar. Here you will see all of the sources in your organization. Click “New Source” to create a ingest endpoint. You will need to pick a database using a dropdown. This is populated by all the databases in your organization. The source name can only contain lowercase alphanumeric characters, dashes (-), and underscores (_) but must start with an alphabetic character. This should be descriptive for your organization to understand what data is streaming from this endpoint as well as what environment this source is loading. For example, web clickstream data loading to production might be named web_clicks_production. 

Next, you will need to pick a table using a dropdown. This is populated by all the tables in your database. Choosing a table will dynamically populate all of the columns in that table below. You must map how the JSON records you send to the endpoint relate to your table's columns. This is done with dot notation and represents the JSON "path" that leads to the column's value for that record. In the example record below `data.aircraftId` would map to the value `40688E`"

```json
{"id": "PD2tRswoE3:0:0", "timestamp": 1659981468260, "encoding": "json", "data": {"aircraftId": "40688E", "lat": 45.1199, "long": -43.416, "track": 250, "altitude": 37996, "speed": 495, "type": "B788", "reg": "G-ZBJA", "origin": "LHR", "destination": "BNA", "iataId": "", "icaoId": "BAW223N", "airline": "BAW"}, "name": "data"}
```

You must map something to the _id column as this is the primary ID (key) for your table and requires a value. All of the other columns are optional. You only should map the columns that will be populated by records sent to this ingest endpoint. Data for a single _id in your table might be populated by different endpoints, which is why these mappings are optional. 

If you map any columns that have a time quantum, you'll also need to map a `_timeQuantum` column. This will automatically be generated in the UI and needs the mapping to the timestamp to be used for all mapped time quantum columns. It is valid to have multiple columns use the same mapping.

After mapping the columns you want, you have to decide how to handle cases when a record arrives with missing values from those you mapped. You have the option to continue processing and store the record with the data that was found or to discard the entire batch of records sent and log an error. In the case of discarding the batch, each record will be ensured to have a value for each column *that has a mapping*. columns with no mapping are assumed to not be sent to this endpoint

Clicking “create source” will start the process of creating your ingest endpoint. This entire process can also be accomplished programmatically:

**HTTP API Reference:**
```shell
curl --location --request POST 'https://api.featurebase.com/v2/sinks' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{    
    "name": "<source name>",    
  	"sink_details": {
      "database_id": "<database_id>",
      "table": "<table name>"
    },
    "schema": {
        "id_field": "_id",
        "allow_missing_fields": false,
        "definition": [ <json mapping like example below>]
    }
}'
```

The syntax for the API differs from that in the UI. You'll need to pass your database's ID and the target table's name. The "schema" is essentially a mapping of the data being pushed to the columns of the table it's loading. There are a couple parameters that provide information about your schema:

|Parameter| Description  | Required? |
| ------- | ------------ | --------- |
|id_field   |  The id_field option should be used when there is an existing field in the data which uniquely identifies each record in the table and consists of contiguous positive integers. This maps to the _id column in your table. | Yes if primary key fields not provided |
|primary_key_fields  |  The primary_key_fields option should be used when the data has no columns that could be used for id_field. This option uses one or more columns (any type) and concatenates them to create unique record IDs for your table. This maps to the _id column in your table. | Yes if id column not provided |
|allow_missing_fields  |  A boolean option that allows one or more of the columns defined in the schema to be missing from the JSON records streamed in. If a column is missing and this parameter is true, that column is left null with no bits set. If this parameter is False and a column is missing from the JSON records, an error will return and data will not be loaded into your table. `allow_missing_fields` is equivalent to "how to handle cases when a record arrives with missing values" in the UI | Yes |

 **Note:** The value for `id_field` and `primary_key_fields` will always be "_id"
 
The "definition" parameter holds the mappings of the data being pushed to the endpoint and the columns in the table the endpoint is loading:

```json
[
  {
    "name": "the name of the destination column",
    "path": ["location within the JSON blob/records streaming in"]
  }
]
```

**Name**: The name is what the column name in your table is. Column names can only contain lowercase alphanumeric characters, dashes (-), and underscores (_) but must start with an alphabetic character. They must be 230 characters or less in length.

**Path**: The path option defines the location of the value in the JSON to load to the column. It is an array of JSON object keys which are applied in order. For example, `["a","b","c"]` would select 1 within `{"a":{"b":{"c":1}}}`. This path must only consist of strings.

You are required to map the ID of your table with the `name` equal to  `_id`. If you map any columns with time quantums, you'll also need to pass a mapping with the `name` equal to `_timeQuantum`.

 **Note:** The UI uses dot notation, which is translated to an array as a value for `path` as can be seen with `project_id` below. 


```json
[
    {
        "name": "language",
        "path": [
            "language"
        ]
    },
    {
        "name": "_id",
        "path": [
            "project", "project_id"
        ]
    },
    {
        "name": "_timeQuantum",
        "path": [
            "timestamp"
        ]
    }
]
```

After creating the source in the UI, you will be returned to the “Data Sources” page and see a new entry with your source name with the status of “CREATING”. After a few moments, this will update to have a status of “ACTIVE”, which means your ingest endpoint is ready to use. Clicking on the source you just created will reveal a details page that contains your configuration details as well as the "ingest endpoint". This is the endpoint you will stream records to in order to get data into your tables. All of your ingest endpoint statuses can also be queried programmatically.

**HTTP API Reference:**
```shell
curl --location --request GET 'https://api.featurebase.com/v2/sinks' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' 
```

Only sources in the "ACTIVE" state can have data pushed for ingest. To learn more about pushing data, click [here](/cloud/cloud-data-ingestion/streaming-https-endpoint/stream-ingest-endpoint). The full reference API for configuring an ingest endpoint can be found [here](/cloud/api).




