---
title: What types of database can I create in FeatureBase Cloud?
---
<!--source https://molecula.atlassian.net/wiki/spaces/PROD/pages/893222913/Packaging+Pricing -->
{% include /concepts/database-shape-summary.md %}

IMPORTANT: Cloud Database shapes incur an hourly fee, chargeable at the end of the month.

## Before you begin

{% include /cloud/cloud-before-begin.md %}

## Available shapes

NOTE: These options may not be available for some organizations. Contact FeatureBase Support for help.

### Production shapes

Production database shapes are over-provisioned on disk space and memory to ensure performance, and has data replicated should a node ever go down.

| Shape | Memory (GB) | Volume (GB) | Compute (vCPU) |
|---|---|---|---|
| 32GB | 32 | 100 | 12 |
| 64GB | 64 | 300 | 24 |
| 128GB | 128 | 500 | 48 |
| 256GB | 256 | 1200 | 96 |
| 512GB | 512 | 2500 | 192 |
| 1024GB | 1024 | 5000 | 320 |
| 2048GB | 2048 | 10000 | 576 |

### Development shapes

These shapes are intended for development and testing.

| Shape | Memory (GB) | Volume (GB) | Compute (vCPU) |
|---|---|---|---|
| 8GB-Development | 8 | 32(gp3) | 2 |
| 64GB-Development | 64 | 64 (gp3) | 16 |

## Further information

* [Learn how to manage FeatureBase Cloud databases](/cloud/cloud-database/cloud-db-manage)
