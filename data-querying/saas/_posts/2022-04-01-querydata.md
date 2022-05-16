---
id: querydata
title: Query Data
sidebar_label: Query Data
---

 **⚠ WARNING:** This page contains information that only applies to Molecula's SaaS offering. Additionally, this page represents a work in progress that is subject to frequent changes. 
 
 All data querying within the product is performed over HTTPS. Data is queried using either PQL (Pilosa Query Language), our native query language, or the limited set of SQL we support. To learn more about PQL, please visit the [introduction page](/data-querying/pql-intro) and the [reference](/reference/data-querying/pql) page. To learn more about the SQL we support, please visit the [reference](/reference/data-querying/sql) page. As long as an application can issue HTTPS requests, it will be able to query and retrieve data.

The current query endpoint is a synchronous call that waits for your data to return. There are current limitations to the amount of data that can be returned and the amount of time the query can run. Those limits are shown below:

|Category (Exclsuvie) | Current Limit  |
| --- | ----------- |
|Data Limit           |  6MB |
|Execution Time Limit        | 29 sec|

You will receive an error if either limit is exceeded.

In order to query data, the following prerequisites must be met:

1. A deployment exists that is in the “Running” state
- Click [here](/setting-up-featurebase/saas/creating-deployment) to learn how to create a deployment
- Click [here](/reference/api/saas/controlplaneapi) to see the deployment API docs
2. A table exists in that deployment
- Click [here](/data-ingestion/saas/tables) to learn how to create a table
- Click [here](/reference/api/saas/controlplaneapi) to see the table API docs
3. Data has been loaded into the table
- Click [here](/data-ingestion/saas/ingestoverview) to learn how to ingest data

In the User interface, clicking the “Query” section on the left hand navigation bar will take you to a page where you can explore data using PQL & SQL statements. The text editor allows for multiple queries to exist in the same pane. Individual queries are separated by newlines with only whitespace. You should first pick a deployment to query against in the top right corner. This will default to the oldest deployment created. You can redirect any query to a particular deployment by aliasing/prepending it with `“{<deployment name>}”`. Queries can be run by either clicking the run button or with a key combination of `“ctrl + enter"`. This can also be accomplished programmatically <link to query in references> for both SQL and PQL by changing the “language” parameter to sql and pql respectively. Put these in tabs

**HTTP API Reference (SQL):**
```shell
curl --location --request POST 'https://data.molecula.cloud/v1/<deployment id>/query \
--header 'Authorization: <IdToken>' \
--header 'Content-Type: Content-Type: application/json' \
--data-raw '{ 
    "language": "sql", 
    "statement": "<SQL>"
}'
```

**HTTP API Reference (PQL):**
```shell
curl --location --request POST 'https://data.molecula.cloud/v1/<deployment id>/query \
--header 'Authorization: <IdToken>' \
--header 'Content-Type: Content-Type: application/json' \
--data-raw '{ 
    "language": "pql", 
    "statement": "<PQL>"
}'
```

Queries in the user interface have an automatic limit of 100 records applied but can be adjusted up to a 10k maximum. This limit is to protect users from accidentally running taxing queries against their deployments and impacting production performance. After running a query, you will see data populated in a tabular format below the text editor. You are free to explore your data and sort it by the columns returned. If you’d like to hide some of the returned columns, you can click “Columns” directly above the tabular results. You can also export this data to your local machine by clicking “Export” and either downloading a CSV or printing the results.

The query browser also allows users to browse their tables and schemas for easy reference to the tables and fields they can query. Click on “Schema Browser” at the top of the text editor to see a searchable list of all of your tables. Click on a table to have a searchable list of all the fields in that table populate. This feature allows you to easily pull up the tables and fields that you can query. Please note, this is populated based on the deployment you selected in the top right corner of the screen.

You are also able to see, search for, and re-run your historical queries. Click “History” at the top of the text editor to see a searchable list of all of your past queries with the most recent shown at the top. This will display the query, the execution time, the rows returned, and when it was run. The color next to each query signifies if the query execution was successful (green), unsuccessful (red), or still running (blue). Clicking on a query will give you two options. You can “replay” a query by clicking on the play button. This will create a new query entry at the top of your history. You can also copy the full query to your clipboard by clicking the copy button. Note that your query history is private to you and can be lost if you clear your browser cache.
