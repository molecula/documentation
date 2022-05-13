---
id: querydata
title: Query Data
sidebar_label: Query Data
---

 **⚠ WARNING:** This page contains information that only applies to Molecula's SaaS offering. Additionally, this page represents a work in progress that is subject to frequent changes. 

In order to query data, the following prerequisites must be met:

1. A deployment exists that is in the “Running” state
- Click [here](/saas/createdeployment/createdeployment) to learn how to create a deployment
- Click [here](/saas/saas-reference/controlplaneapi) to see the deployment API docs
2. A table exists in that deployment
- Click [here](/saas/ingestdata/tables) to learn how to create a table
- Click [here](/saas/saas-reference/controlplaneapi) to see the table API docs
3. Data has been loaded into the table
- Click [here](/saas/ingestdata/ingestoverview) to learn how to ingest data

In the User interface, clicking the “Query” section on the left hand navigation bar will take you to a page where you can explore data using PQL & SQL statements. The text editor allows for multiple queries to exist in the same pane. Individual queries are separated by newlines with only whitespace. You should first pick a deployment to query against in the top right corner. This will default to the oldest deployment created. You can redirect any query to a particular deployment by aliasing/prepending it with `“{<deployment name>}”`. Queries can be run by either clicking the run button or with a key combination of `“ctrl + enter"`. This can also be accomplished programmatically <link to query in references> for both SQL and PQL by changing the “language” parameter to sql and pql respectively. Put these in tabs

**cURL SQL API Reference:**
```shell
curl --location --request POST 'https://data.molecula.cloud/v1/<deployment id>/query \
--header 'Authorization: <IdToken>' \
--header 'Content-Type: Content-Type: application/json' \
--data-raw '{ 
    "language": "sql", 
    "statement": "<SQL>"
}'
```

**cURL PQL API Reference:**
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