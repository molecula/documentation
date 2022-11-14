---
title: How do I query my database status via SSH?
---

<!--source /cloud/cloud-setup/creating-database.md-->

You can query your database status via SSH.

## Before you begin

{% include install-curl.md %}

## Syntax

```shell
curl --location --request GET 'https://api.featurebase.com/v2/databases' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json'
```

## Arguments

| Argument | Description |
|---|---|
| IdToken | [Obtain the ID token](/cloud/query-cloud-data/cloud-obtain-tokens-ssh) |
