---
title: What types of database can I create in FeatureBase Cloud?
---
<!--source https://molecula.atlassian.net/wiki/spaces/PROD/pages/893222913/Packaging+Pricing -->
{% include /concepts/database-shape-summary.md %}

IMPORTANT: Cloud Database shapes incur an hourly fee, chargeable at the end of the month.

## Before you begin

{% include /cloud/cloud-before-begin.md %}
* [Databases are created on AWS GP3 systems](https://aws.amazon.com/ebs/general-purpose/)
* [Contact FeatureBase Support](https://www.featurebase.com/contact-us) to upgrade your account to access production database shapes

### Trial account and Development shapes

Two database shapes are available on all accounts. These are intended for development and testing purposes.

{% include /cloud/cloud-db-shape-dev.md %}

### Production shapes

Production shapes are available on paid accounts. These have:
* overprovisioned disk space and memory to ensure best performance
* data replication should a node go down.

{% include /cloud/cloud-db-shape-prod.md %}

## Further information

* [Learn how to manage FeatureBase Cloud databases](/cloud/cloud-database/cloud-db-manage)
* [Query database shapes via the API](https://api-docs-featurebase-cloud.redoc.ly/v2#operation/getServiceProperties)
