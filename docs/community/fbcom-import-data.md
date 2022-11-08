---
Title: How do I import data to FeatureBase?
---

## Source (delete when finished)

* http://docs.featurebase.com/data-ingestion/enterprise/ingesters#field-types
* http://docs.featurebase.com/data-ingestion/enterprise/ingesters#field-type-mappings
* http://docs.featurebase.com/reference/data-ingestion/ingester-configuration#header-descriptions
* http://docs.featurebase.com/data-ingestion/enterprise/ingesters#ingest-tuning (possible new page?)
* https://molecula.atlassian.net/wiki/spaces/EN/pages/720338949/The+Book+of+Wisdom#Ingest-considerations%2C-recommendations%2C-etc.
* 

You can import data to FeatureBase using CSV, METHOD, METHOD

## Before you begin

* [Learn how FeatureBase imports data](/docs/concepts/featurebase-ingestion)

---



ADD from: http://docs.featurebase.com/data-ingestion/enterprise/ingesters

http://docs.featurebase.com/data-ingestion/enterprise/ingesters#id-generation

The process of obtaining these Key IDs is referred to as translation in the ingester’s logs:

2020/07/20 14:14:47 translating batch of 10 took: 10.1172ms

The process of copying this data into FeatureBase is referred to as “flushing” in the ingester’s logs, and typically takes a very small amount of time:

2020/07/20 14:14:47 flushing batch of 10 to fragments took 84.2µs
---

## Before you begin

* **Ingestion** is the FeatureBase term for importing data
* [Startup the FeatureBase server](/docs/community/fbcom-startup-connect)



## Import data from a CSV

* [Import data using a CSV file](/docs/community/fbcom-import-data-csv.md)

## Import data from GitHub


## Import data using Kafka


## Import data


## Further information


## Get support

{% include /docs/get-support-source.md %}
