---
title: How do I query my databases using the cloud API?
---

<!-- source /cloud/query-cloud/querydata.md -->

## Before you begin

{% include /cloud/cloud-before-begin.md %}
{% include install-curl.md %}

## Syntax

```shell
curl --location --request POST 'https://data.featurebase.com/v2/databases/<database-id>/query' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: Content-Type: application/json' \
--data-raw '{
    "language": "[sql | pql]",
    "statement": "[SQL-Query | PQL-Query]"
}'
```

## Arguments

| Argument | Description | Further information |
|---|---|---|
| database id |  |  |
| IdToken | [Obtain the ID token](/cloud/query-cloud-data/cloud-obtain-tokens-ssh) |
| language | enter either `sql` or `pql`|
| statement | SQL or PQL query | [Learn about PQL and SQL](#further-information) |

## Returns

SQL or PQL query results or an error message if there is an issue.

## Example

```shell
curl --location --request POST 'https://data.featurebase.com/v2/databases/featurebase-db1/query' \
--header 'Authorization: Bearer ABCDEFG' \
--header 'Content-Type: Content-Type: application/json' \
--data-raw '{
    "language": "sql",
    "statement": "select * from featurebase-db1.sampletable"
}'
```

## Further information

* [Learn about PQL](/pql-guide/pql-introduction)
* [Learn about supported SQL](/sql-guide/sql-introduction)
