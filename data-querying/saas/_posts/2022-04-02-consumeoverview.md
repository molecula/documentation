---
id: consumeoverview
title: Consume Data Overview
sidebar_label: Consume Data Overview
---

 **⚠ WARNING:** This page contains information that only applies to Molecula's SaaS offering. Additionally, this page represents a work in progress that is subject to frequent changes. 

All data consumption within the product is performed over HTTPS. Data is queried using either PQL (Pilosa Query Language), our native query language, or the limited set of SQL we support today. To learn more about PQL, please visit the [introduction page](/explanations/pql-intro) and the [reference](/reference/pql) page. To learn more about the SQL we support today, please visit the [reference](/reference/sql) page. As long as an application can issue HTTPS requests, it will be able to query and retrieve data.

The current query endpoint is a synchronous call that waits for your data to return. There are current limitations to the amount of data that can be returned and the amount of time the query can run. Those limits are shown below:

|Category (Exclsuvie) | Current Limit  |
| --- | ----------- |
|Data Limit           |  6MB |
|Execution Time Limit        | 29 sec|

These limits will change in the near future but are important to keep in mind. You will receive an error if either limit is exceeded.