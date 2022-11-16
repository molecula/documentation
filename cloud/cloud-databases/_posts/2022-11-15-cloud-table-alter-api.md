---
title: How do I alter table columns using SSH?
---

NOTE: This method is not recommended.

## Syntax

```shell
curl --location --request POST 'https://api.featurebase.com/v2/tables/<database_id>/<table_name>/fields/<column_name>' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "options": {"type": "<data_type>", <constraint_options>}
}'
```

## Arguments

| Argument | Description | Further information |
|---|---|---|
| IdToken | Authentication token required to connect to database | [Obtain the ID token](/cloud/query-cloud-data/cloud-obtain-tokens-ssh) |
| data_type | table column data type | [Learn about valid data types](/cloud/cloud-databases/cloud-table-data-types) |
| constraint_options | table column data type constraint | [Learn about valid constraints](/cloud/cloud-databases/cloud-table-constraints) |

## Example


## Further information

* [Create field in API documentation](/community/community-api/http-api#create-field).
