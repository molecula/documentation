## timeQuantum

timeQuantum creates a view of your data based on the specified time granularity.

timeQuantum is used when:
* times need to be associated with column data for query purposes
* database space is not at a premium
* querying times directly rather than filtering

### Time granularity

Time granularity allows for lower latency queries at the cost of increased storage. For example:
* set MD for queries that include a range of months
* set D for queries that include a small number of days

You can omit but not skip time granularity.
* YM is valid
* MS is invalid

NOTE: Queries run on mismatched time granularities are slower but will function correctly. For example: YM time granularity then query on days.
