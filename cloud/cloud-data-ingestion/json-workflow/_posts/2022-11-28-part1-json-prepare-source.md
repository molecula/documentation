---
title: Part 1 - prepare JSON source files
---

{% include /cloud/json-workflow-summary.md %}

## Before you begin

{% include /concepts/ingest-before-begin.md %}
{% include /cloud/cloud-ingest-overview-link.md %}
* You will need some experience of working with JSON files

## What is a valid JSON file for import? (change title later)



### Syntax



```json
{
    "records": [
        { "value": { <JSON blob containing columns of first record> } },
        { "value": { <JSON blob containing columns of second record> } },
        ...
    ]
}

```

## Import limitations

Importing data is limited to:
* 1000 records/second OR
* 1MB records/per second

FeatureBase recommends creating small JSON files for initial testing to make errors easier to recover from.

## Other stuff user needs to know (add proper heading or remove)


## Next step

* {% include /cloud/json-workflow-pt2-link.md %}
