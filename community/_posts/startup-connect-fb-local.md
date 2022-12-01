---
title: Startup & connect
layout: default
parent: Community
has_children: true
nav_order: 4
---

# How do I startup and connect to FeatureBase Community?

These instructions explain how to run FeatureBase Community after you’ve installed on the target system.

{% include /docs/page-toc.md %}

<p class="note">NOTE: FeatureBase does not currently run on Mac Safari</p>

## Before you begin

* [Learn about Featurebase](welcome.md)
* Install FeatureBase on the destination system:
  * [Install FeatureBase on Linux](/docs/install-featurebase-linux)
  * [Install FeatureBase on Mac](/docs/install-featurebase-mac)
  * [Install FeatureBase on Windows](/docs/install-featurebase-windows)
* Install Mozilla Firefox or Google Chrome on the target system

## How do I start the FeatureBase Community server?

1. Login to the system
2. Open a terminal window and cd to the folder
2. Execute these commands in a terminal window:

```
CD /featurebase/opt
./featurebase server
```

## How do I connect to FeatureBase community?

Open the following URL in your web browser:

```
http://localhost:10101/
```

## Troubleshooting

* [Issue: FeatureBase Community won't startup on Mac](/community/issue-fb-community-mac.md)

## Get support

{% include /docs/get-support-source.md %}
