---
id: keyconcepts
title: Key Concepts
sidebar_label: Key Concepts
---

 **⚠ WARNING:** This page contains information that only applies to Molecula's Cloud offering. Additionally, this page represents a work in progress that is subject to frequent changes. 

**Organization:** The entity that contains everything you own (users, resources, data, etc.) within the tool. You can think of this simply as your company.

**Deployment:** A FeatureBase cluster. Deployments are the underlying hardware used to both store and query your data. Clusters can consist of one or more nodes. Deployments are managed with the “Cloud Manager” in the UI.

**Table:** An object within a deployment that stores related data. While [data modeling](/data-modeling-guide/data-modeling) within FeatureBase is different than other databases, a table is analogous to a table found in a traditional RDBMS. A table is created and must be uniquely named within a deployment. A table’s name is immutable once created.

**Sources:** Resources that load data into tables within deployments. Today, the only source is an HTTPS endpoint that allows you to stream data into your deployment. Each endpoint has an associated schema and maps to one table within one deployment.

**Control Plane:** A centralized layer that contains information and APIs that help you create and manage resources within your organization. You can think of this as the management layer on top of your data. You can tell an API exists in the control plane if the route starts with https://api.molecula.cloud.

**Data Plane:** A layer that contains your data and APIs that let you directly communicate with your data. These APIs directly hit your deployments directly and are intended to be used when a high number of concurrent queries and low latency matter. You can tell an API exists in the control plane if the route starts with https://data.molecula.cloud.
