---
id: uioverview
title: UI Overview & Navigation
sidebar_label: UI Overview & Navigation
---

 **⚠ WARNING:** This page contains information that only applies to Molecula's SaaS offering. Additionally, this page represents a work in progress that is subject to frequent changes. 

The user interface is meant to make provisioning, loading, querying, and monitoring your deployments easy. When you log in on app.molecula.cloud, you will see a navigation bar on the left hand side of the screen. This is used to navigate between the different areas of the UI. This navigation bar is persisted to allow for switching between key areas quickly. The main working area of the page will populate based on the area you select. Each of the main areas is detailed below.

## Cloud Manager
Clicking “Get Started” or “Cloud Manager” from the home page will direct you to the Cloud Manager page where you can create a “New Deployment”. Deployments are FeatureBase clusters created within the tool. All of your data will live in tables within a  FeatureBase deployment. Today, the tool has t-shirt memory choices, so all you need to provide is a memory selection from a drop down and a deployment name. This is a unique name for your deployment that will be used throughout the tool to reference a particular deployment of FeatureBase. You can have multiple deployments, so it’s important to name these something meaningful to you and your organization.

## Sources
Once a deployment is running, you will want to start loading data into it. “Sources” is where you will configure sources that load data into your deployments. Today, the tool only supports Streaming data through HTTPS. The “Streaming (HTTPS)” source configuration will yield a persistent endpoint that allows you to push data into your deployment over HTTPS. Each endpoint maps to one table within one deployment. If you have multiple disparate data sources, you may create multiple endpoints that push data to the same table. Once an endpoint is provisioned, you can post JSON records to it using any tool that can perform HTTPS requests. Posting records is not supported within the UI today. The table below describes the current limits of streaming data in:

|Category (Exclsuvie) | Current Limit  |
| --- | ----------- |
|Data Limit           |  1MB/sec |
|Record Limit         | 1000/sec |



## Tables
The “Tables” section allows you to create new table objects and inspect the schema of existing tables. Today, FeatureBase schemas are created during data ingest when data is loaded, so metadata around tables will not be populated until data is loaded. Clicking into a table will allow users to see table metadata like the deployment it's in, fields and types, and more.

## Query
The “Query” section allows you to explore data using PQL and SQL statements. The text editor allows for multiple queries to exist in the same pane. Individual queries are separated by newlines with only whitespace. You should first pick a deployment to query against in the top right corner. This will default to the oldest deployment created. Queries have an automatic limit of 100 records applied but can be adjusted up to a 10k maximum. This is to protect users from bogging down FeatureBase accidentally or trying to bring back too much data. The query page also allows you to browse tables and schemas, as well as see your historical queries.

## Configuration
The “Configuration” section allows you to manage general settings and your organization as a whole. Today, there are two pages under “Configuration”: “Manage Users” and a “Organization Settings”. “Manage Users” allows you to view users, invite new users, and deactivate/reactivate users in you organization. “Organization Settings” allows you to view and update relevant information about your organization, such as the billing or technical contacts listed for your organization.