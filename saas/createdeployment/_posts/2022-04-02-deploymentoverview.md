---
id: deploymentoverview
title: Deployments Overview
sidebar_label: Deployments Overview
---

 **⚠ WARNING:** This page contains information that only applies to Molecula's SaaS offering. Additionally, this page represents a work in progress that is subject to frequent changes. 

Deployments are instances of FeatureBase. All of your data will live in tables within FeatureBase. You can think of a deployment as a database. It is dedicated hardware for your data that you can load to and query against, and like databases, you can only join tables that exist in the same deployment. Below is a list of t-shirt size deployment choices Molecula offers today: 

### Sizes

|Deployment Memory (GB) | Note  |
| --- | ----------- |
|8           |  This deployment is meant for development and testing only |
|64         | This deployment is ready for production use, is over-provisioned on disk space and memory to ensure performance, and has data replicated should a node ever go down |
|128         | This deployment is ready for production use, is over-provisioned on disk space and memory to ensure performance, and has data replicated should a node ever go down |
|256         | This deployment is ready for production use, is over-provisioned on disk space and memory to ensure performance, and has data replicated should a node ever go down |
|512         | This deployment is ready for production use, is over-provisioned on disk space and memory to ensure performance, and has data replicated should a node ever go down |
|1024         | This deployment is ready for production use, is over-provisioned on disk space and memory to ensure performance, and has data replicated should a node ever go down |
|2048         | This deployment is ready for production use, is over-provisioned on disk space and memory to ensure performance, and has data replicated should a node ever go down |

Please note that all of these options might not appear for you. When signing up, our support team will help you size and identify the right options for your use cases. We will customize your experience so that you only see the options identified best for you. This is to protect your organization from creating unnecessarily large deployments that will incur additional costs. Additionally, we can work with you on a custom deployment option if none of our current options fit your need.

There are a couple of states associated with deployments that are important to understand. You will see these states as a “status” in the UI and API. The list of states can be seen below:

### States

|Status | Description  |
| --- | ----------- |
|CREATING           |  The state of provisioning the hardware, installing software, and everything else in order to create a FeatureBase deployment.This will generally transition into RUNNING state. |
|RUNNING           |  The healthy state of a deployment that is ready to use. |
|UPDATING           |  The state of a deployment when an update is being applied. This might occur when hardware is being updated, software is being patched, etc. |
|DELETING           |  The state when a deployment is being deleted and hardware is being spun down. This will generally transition into DELETED state. |
|DELETED           |  The state of a deployment that has been successfully deleted. |
|FAILED           |  The state of a deployment when something goes wrong. This can occur for a variety of reasons. If you see this state and the deployment is ok to delete, feel free to do so. Otherwise, please contact us.|

