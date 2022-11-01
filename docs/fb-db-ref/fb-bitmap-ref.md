---
id: fb-bitmap-ref
title: FeatureBase bitmapreference
sidebar_label: FeatureBase bitmap reference
---


## Description

A Bitmap is how FeatureBase represents rows.

NOTE: The FeatureBase concept of ROW differs from the traditional meaning. See [Record in the glossary](/concepts/glossary.md)

Within FeatureBase, a row conceptually describes the fundamental vertical data axis within the FeatureBase database.

Rows are namespaced to each field within an index and represented as a Bitmap.

Represented as a Bitmap. See [Record]() for the Featurebase implementation of database rows.

FeatureBase representation of a Row.

Implemented with RBF (Roaring B-tree format),

## Syntax


## Arguments


## Additional information

* FeatureBase bitmap is inspired by and evolved from the previous implementation

## Examples


## Further information

* [FeatureBase row reference]()
* [Roaring Bitmaps](https://roaringbitmap.org/).

## Get support

{% include /docs/get-support-source.md %}
