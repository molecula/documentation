---
title: How do I obtain Access, ID and Refresh tokens for my API query?
---

<!-- source: /cloud/cloud-data-ingestion/streaming-https-endpoint/cloud-streaming-quickstart.md -->

FeatureBase Cloud uses Oauth2.0 for all authorization which means all API calls must be accompanied by a valid token.

Tokens are obtained by passing credentials to https://id.featurebase.com

## Before you begin

{% include /cloud/cloud-before-begin.md %}

## Syntax

```shell
curl --location --request POST 'https://id.featurebase.com' \
--data-raw '{
    "USERNAME": "<username>",
    "PASSWORD": "<password>"
}' [| grep -Eo '"IdToken":.*?[^\\]",' | sed -e 's/[\"\,\: ]*//g' | sed -e 's/IdToken//']
```

## Arguments

| Argument | Description |
|---|---|
| USERNAME | FeatureBase Cloud owner email |
| PASSWORD | FeatureBase Cloud password |

## Returns

| Returns | Description |
|---|---|
| Access | |
| ID | Used as the **Authorization header** in all API calls |
| Refresh |  |

## Additional

Add this command after closing --data-raw to return only the ID token.

```
| grep -Eo '"IdToken":.*?[^\\]",' | sed -e 's/[\"\,\: ]*//g' | sed -e 's/IdToken//'
```

## Examples

```shell
--header 'Authorization: Bearer <IdToken>' \
```
