---
title: What types of database can I create in FeatureBase Cloud?
---

{% include /cloud/cloud-db-shape-summary.md %}

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Contact FeatureBase Support](https://www.featurebase.com/contact-us) to upgrade your account to access production database shapes

## Estimating your requirements

NOTE: {% include contact-support.md%} for help estimating your data requirements.

{% include /concepts/data-modeling-overview.md %}

* [Learn about the data modeling process](/concepts/data-modeling-overview)

## Trial account and Development shapes

Two database shapes are available on all accounts. These can be used for data modeling, development and testing.

{% include /cloud/cloud-db-shape-dev.md %}

## Production shapes

Production shapes are available on paid accounts. These have:
* overprovisioned disk space and memory to ensure best performance
* data replication should a node go down.

{% include /cloud/cloud-db-shape-prod.md %}


## Further information

* [Learn about FeatureBase Cloud pricing](https://www.featurebase.com/pricing){:target=""_blank}
* [Learn about data modeling](/concepts/data-modeling-overview)
* [Learn how to manage FeatureBase Cloud databases](/cloud/cloud-databases/cloud-db-manage)
* [Query database shapes via the API](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/getServiceProperties)
