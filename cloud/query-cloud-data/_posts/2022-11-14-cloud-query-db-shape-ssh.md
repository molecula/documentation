---
title: title: How do I query my database shape via SSH?
---

## Before you begin

{% include /cloud/cloud-before-begin.md %}
{% include install-curl.md %}
* [Learn about database shapes](/cloud/cloud-databases/cloud-db-shape)

## Syntax

```shell
curl --location --request GET 'https://api.featurebase.com/v2/service-properties/database:shapes' \
--header 'Authorization: Bearer <IdToken>'
```

## Arguments

| Argument | Description |
|---|---|
| IdToken | [Obtain the ID token](/cloud/query-cloud-data/cloud-obtain-tokens-ssh) |
