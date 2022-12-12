## TIMEQUANTUM

TIMEQUANTUM creates a view of your data based on the specified time. This allows for lower latency queries at the cost of increased storage. For example, set TIMEQUANTUM to:
* `MD` for queries that include a range of months
* `D` for queries that include a small number of days

NOTE: Queries run on mismatched time granularities are slower but will function correctly. For example:  Querying days on a IDSET or STRINGSET column with TIMEQUANTUM set to `YM`.

You can omit but not skip time granularity.
* YM is valid
* YH is invalid

TIMEQUANTUM is used when:
* times need to be associated with column data for query purposes
* database space is not at a premium
