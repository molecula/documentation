---
title: How do I query my cloud database?
---

FeatureBase Cloud provides a built-in Query Builder for writing [PQL and SQL statements](#further-information) to query your databases.

The FeatureBase Cloud Query builder offers:
* Syntax highlighting
* Schema browser for the selected database
* Result limits of 10 to 10,000 rows
* Filter results by column
* Reorder results by Ascending or Descending
* Export results to CSV
* Query history

## Query languages

You can write queries using the FeatureBase PQL query language or supported SQL.

* [Learn about PQL](/pql-guide/pql-introduction)
* [Learn about supported SQL](/sql-guide/sql-introduction)

## Query Endpoint

All queries are performed over HTTPS.

The Cloud query endpoint is a synchronous call that waits for your data to return.

## Query limitations

Queries are limited as follows:

| Limit | Values |
|---|---|
| Data | 6MB |
| Execution Time | <30 sec |

Queries that excede these limits will return `Network Error`

## Query Builder syntax

The FeatureBase Query Builder follows SQL formatting standards for all queries, including PQL.

* [Learn about SQL standards](https://www.w3schools.com/sql/sql_syntax.asp)

NOTE: Not all SQL syntax is currently supported.

## Before you begin

{% include /cloud/database-dependencies.md %}
* [Learn how to import data to FeatureBase](/cloud/cloud-data-ingestion/ingest-data-overview)

## How do I run a query?

1. Click Query
2. Choose a database
3. Enter the query.
4. Click **Run**.

## How do I filter results?

| Filter | Method |
|---|---|
| Filter by columns | Click <svg class="MuiSvgIcon-root MuiSvgIcon-fontSizeMedium css-vubbuv" focusable="false" aria-hidden="true" viewBox="0 0 24 24" data-testid="ColumnIconIcon"><path d="M6 5H3c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h3c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1zm14 0h-3c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h3c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1zm-7 0h-3c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h3c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1z"></path></svg> |

## Further information

* [Learn about PQL](/pql-guide/pql-introduction)
* [Learn about supported SQL](/sql-guide/sql-introduction)





Queries in the user interface have an automatic limit of 100 records applied but can be adjusted up to a 10k maximum. This limit is to protect users from accidentally running taxing queries against their databases and impacting production performance. After running a query, you will see data populated in a tabular format below the text editor. You are free to explore your data and sort it by the columns returned. If you’d like to hide some of the returned columns, you can click “Columns” directly above the tabular results. You can also export this data to your local machine by clicking “Export” and either downloading a CSV or printing the results.

The query browser also allows users to browse their tables and schemas for easy reference to the tables and columns they can query. Click on “Schema Browser” at the top of the text editor to see a searchable list of all of your tables. Click on a table to have a searchable list of all the columns in that table populate. This feature allows you to easily pull up the tables and columns that you can query. Please note, this is populated based on the database you selected in the top right corner of the screen. You may also click "CREATE SELECT STATEMENT" here to have a SELECT statement with all columns pasted into the text editor.

You are also able to see, search for, and re-run your historical queries. Click “History” at the top of the text editor to see a searchable list of all of your past queries with the most recent shown at the top. This will display the query, the execution time, the rows returned, and when it was run. The color next to each query signifies if the query execution was successful (green), unsuccessful (red), or still running (blue). Clicking on a query will give you two options. You can “replay” a query by clicking on the play button. This will create a new query entry at the top of your history. You can also copy the full query to your clipboard by clicking the copy button. Note that your query history is private to you and can be lost if you clear your browser cache.

## Further information

* [Learn how to query databases using the API](https://api-docs-featurebase-cloud.redoc.ly/v2#tag/Query)
