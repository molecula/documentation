---
title: Issue - Data Modeling MIN/MAX Integer Precision Loss
---

Specifying the MIN and MAX constraint for `int` is limited to `-2^53` and `2^53 -1`

## Cause

Precision loss due to JS and Go integer limitations at scale

## Solution

If you plan to ingest integers outside of the listed range, simply specify the column with type `int` and no constraints, so the default values are applied internally.

## Further information

[INT Data Type](/sql-preview/data-types/data-type-int#arguments)
{% include contact-support.md %} to discuss upgrading your account.
