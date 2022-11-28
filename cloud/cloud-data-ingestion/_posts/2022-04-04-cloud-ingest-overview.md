---
title: How do I import data to FeatureBase Cloud?
---

Data can be imported to FeatureBase Cloud using source files in the following formats:

* JSON
* CSV

You can also setup the following streaming methods to import to FeatureBase cloud:

* Apache Kafka
* Confluent Cloud

This page provides an overview of each method, the pros and cons and links to process and procedure documentation to guide you through the process of importing your content to FeatureBase Cloud.

On this page you will find:
* A comparison of each method with pros and cons
* Detailed overview information of the requirements of each method
* Hyperlinks to process and procedure workflows to help you import your data

## Before you begin

Important: read the following conceptual pages to understand the process of importing data to FeatureBase.

{% include /concepts/ingest-before-begin.md %}

## Comparison of methods

| Data source | Pros | Cons | Further information |
|---|---|---|---|
| JSON file | Import using the UI | Experience with JSON | [JSON file import](#) |
| CSV file | ??? | API experience | [CSV file import](#) |
| Apache Kafka | ??? | API experience | [Apache Kafka import](#) |
| Confluent Cloud | ??? | API experience | [Confluent Cloud import](#) |

## Import JSON data using the web interface

This process can be performed exclusively in the Cloud web interface and requires:

| Task | Further information |
|---|---|
| Create JSON file(s) with table structure and data for import | {% include /cloud/json-workflow-pt1-link.md %} |
| Create target database | {% include /cloud/json-workflow-pt2-link.md %} |
| Create target tables | {% include /cloud/json-workflow-pt3-link.md %} |
| Map table column data types to JSON data | {% include /cloud/json-workflow-pt4-link.md %} |
| Add data source to create HTTPS endpoint to import data | {% include /cloud/json-workflow-pt5-link.md %} |
| Import JSON data to FeatureBase Cloud | {% include /cloud/json-workflow-pt6-link.md %} |

## Import data using a CSV file




## Import data using Apache Kafka



## Import data using Confluent Cloud




## Further information






<!-- ORIGINAL CONTENT BELOW

## Before you begin

{% include /cloud/database-dependencies.md %}

## Load data into your database

Sources are configurable resources that load data into databases. The product puts an emphasis on push-based, streaming models in which you, the client, create a process to push data to your databases. This model allows you to control how data is pushed and what(if any) processes run to transform or clean the data before ingestion. This model also keeps data in your datacenter should upstream issues arise. Lastly, push-based ingest helps protect your datacenter by keeping it closed to outside connections that reach in and pull data. Today, the tool only supports streaming data through HTTPS. Any process or application that can make calls over HTTPS is able to push data to databases.

Once data is pushed, the records accumulate in the uncompressed format they came in. This process then translates your data into FeatureBases’s feature-first format and writes the data into your table. This translation varies based on the type of data ingested, but you can learn more about the process [here](/community/community-data-ingestion/ingesters#2-translate-records-into-featurebases-roaring-bitmap-format). This process typically reduces your data’s footprint by 10x but has seen reductions upwards of 100x.

## Data Model

Data modeling determines how data is imported to FeatureBase and how it is represented to meet your needs.

* [Learn about data modeling](/concepts/data-modeling-overview).

## Next step

* [Learn about cloud streaming and ingestion endpoints](/cloud/cloud-data-ingestion/streaming-https-endpoint/cloud-streaming-overview)
-->
