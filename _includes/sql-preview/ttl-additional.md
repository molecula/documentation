## TTL (Time To Live)

NOTE: FeatureBase recommends using a TTL of `1h` or more to improve results.

* TTL enables the deletion of time views where a time range exceeds the stated Time To Live.
* The default TTL of `0s` indicates TIMEQUANTUM views will not be deleted.
* TTL runs:
  * when FeatureBase starts and every hour to make view deletion consistent
  * are not guaranteed to run at a specific time
* `error: unknown unit` is generated if an incorrect value is used (e.g., TTL is set to `60second`)

* TTL should not be used if you require complete and consistent historical data.

### TTL order of events

This example demonstrates the deletion dates of three column views where TTL is set to `30d`

| View date | ttl date of deletion | Explanation |
|---|---|---|
| 2022 | January 30, 2023 | Date assumed to be end of 2022 |
| 2022-09 | October 30, 2022 | Date assumed to be end of September |
| 2022-09-02 | October 2, 2022 | Deletion after 30 days as intended |
