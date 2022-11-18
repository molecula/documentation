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

| Shape | Memory (GB) | AWS GP3 Volume (GB) | Compute (vCPU) |
|---|---|---|---|
| 8GB-Development | 8 | 32(gp3) | 2 |
| 64GB-Development | 64 | 64 (gp3) | 16 |

### Production shapes

Production shapes are available on paid accounts. These have:
* overprovisioned disk space and memory to ensure best performance
* data replication should a node go down.

| Shape | Memory (GB) | GP3 Volume (GB) | Compute (vCPU) |
|---|---|---|---|
| 32GB | 32 | 100 | 12 |
| 64GB | 64 | 300 | 24 |
| 128GB | 128 | 500 | 48 |
| 256GB | 256 | 1200 | 96 |
| 512GB | 512 | 2500 | 192 |
| 1024GB | 1024 | 5000 | 320 |
| 2048GB | 2048 | 10000 | 576 |

## Further information

* [Learn how to manage FeatureBase Cloud databases](/cloud/cloud-database/cloud-db-manage)
