---
title: How do I create a table using the FeatureBase Cloud API?
---


If you select a number for the ID, keys is false, and is otherwise true. You can see the full table api [here](/cloud/cloud-api).

## Syntax

```shell
curl --location --request POST 'https://api.featurebase.com/v2/tables/<database_id>' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "<table_name>",
    "description": "<table_description>"
    "options": {"keys":<bool>}    
}'
```

table names can include only lower-case alphabetic letters, numbers, dash and underscores. table names must lead with a lower-case alphabetic letter.

## Arguments

| Argument | Description | Further information |
|---|---|---|
| database_id | destination database for the table |  |
| IdToken |  | [Obtain ID Token](/cloud/query-cloud-data/cloud-obtain-tokens-ssh) |
| table_name | user supplied table name. |  |
| table_description | optional description of table |  |
| keys |  |  |

## Additional information



## Examples



## Further information
