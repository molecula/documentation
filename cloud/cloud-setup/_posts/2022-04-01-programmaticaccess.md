---
id: programmaticaccess
title: Programmatic Access
sidebar_label: Programmatic Access
---

 **⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes.

Everything that can be done in the user interface can be accomplished via REST api calls. Furthermore, APIs allow you to perform additional actions as well as gather more metadata about your organization and data. You will likely interact with the APIs in a production setting. Full Documentation for the APIs can be found [here](/cloud/cloud-api).

FeatureBase Cloud uses Oauth2.0 for all authorization, so every API call must be accompanied with a valid token. You can get tokens by passing your credentials to https://id.featurebase.com . The below cURL command can be run on any linux-based system:

**HTTP API Reference:**
```shell
curl --location --request POST 'https://id.featurebase.com' \
--data-raw '{
    "USERNAME": "<username>",
    "PASSWORD": "<password>"
}'
```

3 tokens are returned: Access, ID, and Refresh. Use the ID token for all of your API calls as the Authorization header:

`--header 'Authorization: Bearer <IdToken>'`

It’s best practice to have tokens that expire frequently in order to protect customers in the unlikely event attackers are able to obtain a token. The ID token is valid for 60 minutes. After that, you’ll need to perform the same call above. Alternatively you can use the refresh token to retrieve new ID tokens for up to 30 days. This is an option if you don’t want to re-authenticate using your credentials every time. You will need to keep these tokens somewhere in order to re-use them.
