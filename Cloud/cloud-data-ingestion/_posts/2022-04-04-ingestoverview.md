---
id: ingestoverview
title: Ingest Data Overview
sidebar_label: Ingest Data Overview
---

 **⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes. 

Once a database is running, it is available for loading data. Sources are configurable resources that load data into databases. The product puts an emphasis on push-based, streaming models in which you, the client, create a process to push data to your databases. This model allows you to control how data is pushed and what(if any) processes run to transform or clean the data before ingestion. This model also keeps data in your datacenter should upstream issues arise. Lastly, push-based ingest helps protect your datacenter by keeping it closed to outside connections that reach in and pull data. Today, the tool only supports streaming data through HTTPS. Any process or application that can make calls over HTTPS is able to push data to databases.

Once data is pushed, the records accumulate in the uncompressed format they came in. This process then translates your data into FeatureBases’s feature-first format and writes the data into your table. This translation varies based on the type of data ingested, but you can learn more about the process [here](/data-ingestion/enterprise/ingesters#2-translate-records-into-featurebases-roaring-bitmap-format). This process typically reduces your data’s footprint by 10x but has seen reductions upwards of 100x.

## Data Model
Data modeling is a key component in FeatureBase that involves understanding both how you will consume your data and how FeatureBase can represent your data to meet your consumption’s needs. This is a prerequisite that must be done before ingesting data and  involves tradeoffs in performance and storage. The FeatureBase team will help you understand modeling and how to model your data. Full documentation on data modeling can be found [here](/data-modeling-guide/data-modeling). 

