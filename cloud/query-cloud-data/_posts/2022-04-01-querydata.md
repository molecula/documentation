---
title: Query Data
---

**⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes.

All data querying within the product is performed over HTTPS. Data is queried using either PQL (Pilosa Query Language), our native query language, or the limited set of SQL we support.

As long as an application can issue HTTPS requests, it will be able to query and retrieve data.

## Before you begin

{% include cloud/database-dependencies %}
* [Learn how to import data to FeatureBase](/cloud/cloud-data-ingestion/ingest-data-overview)
* [Learn about PQL](/pql-guide/pql-introduction)
* [Learn about supported SQL](/sql-guide/sql-introduction)

## About the query endpoint

The current query endpoint is a synchronous call that waits for your data to return. There are current limitations to the amount of data that can be returned and the amount of time the query can run. Those limits are shown below:

|Category (Exclusive) | Current Limit  |
| --- | ----------- |
|Data Limit           |  6MB |
|Execution Time Limit        | <30 sec|

You will receive an error ("Network Error") if either limit is exceeded.

## Executing A Query

In the User interface, clicking the “Query” section on the left hand navigation bar will take you to a page where you can explore data using PQL & SQL statements. The text editor allows for multiple queries to exist in the same pane. Individual queries are separated by newlines with only whitespace. You should first pick a database to query against in the top right corner. This will default to the oldest database created. You can redirect any query to a particular database by aliasing/prepending it with `“{<database name>}”`. Queries can be run by either clicking the run button or with a key combination of `“Ctrl + Enter"` or `Cmd + Enter"`. This can also be accomplished programmatically <link to query in references> for both SQL and PQL by changing the “language” parameter to sql and pql respectively. Put these in tabs

**HTTP API Reference (SQL):**
```shell
curl --location --request POST 'https://data.featurebase.com/v2/databases/<database id>/query' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: Content-Type: application/json' \
--data-raw '{
    "language": "sql",
    "statement": "<SQL>"
}'
```

**HTTP API Reference (PQL):**
```shell
curl --location --request POST 'https://data.featurebase.com/v2/databases/<database id>/query' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: Content-Type: application/json' \
--data-raw '{
    "language": "pql",
    "statement": "<PQL>"
}'
```

Queries in the user interface have an automatic limit of 100 records applied but can be adjusted up to a 10k maximum. This limit is to protect users from accidentally running taxing queries against their databases and impacting production performance. After running a query, you will see data populated in a tabular format below the text editor. You are free to explore your data and sort it by the columns returned. If you’d like to hide some of the returned columns, you can click “Columns” directly above the tabular results. You can also export this data to your local machine by clicking “Export” and either downloading a CSV or printing the results.

The query browser also allows users to browse their tables and schemas for easy reference to the tables and columns they can query. Click on “Schema Browser” at the top of the text editor to see a searchable list of all of your tables. Click on a table to have a searchable list of all the columns in that table populate. This feature allows you to easily pull up the tables and columns that you can query. Please note, this is populated based on the database you selected in the top right corner of the screen. You may also click "CREATE SELECT STATEMENT" here to have a SELECT statement with all columns pasted into the text editor.

You are also able to see, search for, and re-run your historical queries. Click “History” at the top of the text editor to see a searchable list of all of your past queries with the most recent shown at the top. This will display the query, the execution time, the rows returned, and when it was run. The color next to each query signifies if the query execution was successful (green), unsuccessful (red), or still running (blue). Clicking on a query will give you two options. You can “replay” a query by clicking on the play button. This will create a new query entry at the top of your history. You can also copy the full query to your clipboard by clicking the copy button. Note that your query history is private to you and can be lost if you clear your browser cache.
