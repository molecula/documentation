---
id: import-data-overview
title: How do I import data to FeatureBase?
sidebar_label: How do I import data to FeatureBase?
---

# STATUS: ALPHA (NOT READY FOR REVIEW)


## SOURCE (delete when finished)

From glossary: Batch = A group of records that are preprocessed and simultaneously ingested into a FeatureBase index.





Once a database is running, it is available for loading data. Sources are configurable resources that load data into databases. The product puts an emphasis on push-based, streaming models in which you, the client, create a process to push data to your databases. This model allows you to control how data is pushed and what(if any) processes run to transform or clean the data before ingestion. This model also keeps data in your datacenter should upstream issues arise. Lastly, push-based ingest helps protect your datacenter by keeping it closed to outside connections that reach in and pull data. Today, the tool only supports streaming data through HTTPS. Any process or application that can make calls over HTTPS is able to push data to databases.

This page would include high level overviews of ingestion adapted from pages such as:

https://docs.featurebase.com/data-ingestion/enterprise/ingesters

https://docs.featurebase.com/reference/data-ingestion/ingester-configuration



Procedural pages would include content adapted from pages such as:

https://docs.featurebase.com/data-ingestion/cloud/streaming/createstreamingsource

https://docs.featurebase.com/ > Ingest data

https://docs.featurebase.com/how-tos/consumer-examples

## Get support

{% include /docs/get-support-source.md %}
