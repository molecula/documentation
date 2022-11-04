---
title: Data modeling overview
---

# Status: Alpha (well before first draft)

## Source

/data-modeling-guide/_posts/2022-04-01-data-modeling.md
/data-ingestion/_posts/2022-04-04-ingestoverview.md

## Introduction (delete heading when finished)

Data modeling involves analysing:
* how you will use your data
* how FeatureBase represents your data
* performance trade-offs in performance and storage

<p class="warning">IMPORTANT: Perform data modelling before importing data to ensure FeatureBase provides the best value to your organisation.</p>

## Before you begin

* [Learn about the FeatureBase database](/docs/concepts/fb-db-overview.md)

## Concepts: Fact tables and Dimensions

In a standard relational model, one often hears about "fact" tables vs "dimensions" which are typically separated.

| Concept | Description | Example | Further information |
|---|---|---|---|
| Fact tables | Each record in a fact table typically represents an immutable event | Someone clicked a link or made a purchase, a temperature reading was recorded, etc | [Learn about Fact tables](https://en.wikipedia.org/wiki/Fact_table) |
| Dimensions | Dimensions usually represents slower changing "metadata" and is typically split from Fact data to reduce duplication.  | If your fact is that a user performed a certain action, one of your dimensions might be a "users" table that records things like date of birth, gender, address. | LINK?? |

## Modeling your data in FeatureBase

FeatureBase provides additional functionality to help model your data.

Usually when you're doing queries
that involve facts,
you're not interested in the events themselves,
but one of the dimensions that they affect.

### Example 1: querying blog page statistics


| Query type | Example | Description |
|---|---|---|
| Distinct number of users | Select unique_visitors on blog_post | more complex query |
| Number of events | Select page_loads on blog_post | simpler query |



In FeatureBase, you could add a "pages_visited" set type field directly to your users dimension and get the distinct functionality essentially for free.

The power of the set field is that it can track multiple pages visited per user without additional overhead.




## Next step

* [Learn about importing data to FeatureBase](/docs/concepts/importing-data-to-fb.md)

## Get support

{% include /docs/get-support-source.md %}
