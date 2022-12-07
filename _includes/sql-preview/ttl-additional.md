## ttl

* ttl enables the deletion of time views where a time range exceeds the stated Time To Live.
* ttl should not be used if you require complete and consistent historical data.
* ttl runs:
  * when FeatureBase starts and every hour to make view deletion consistent
  * are not guaranteed to run at a specific time

* ttl time_units
  * ttl of 0s (default value) indicates views created on the timeQuantum will not be deleted
  * FeatureBase recommends using a ttl of one hour or more to improve results.
  * `error: unknown unit` is generated if an incorrect time_unit is used (e.g., `"ttl":"60second"`)

### TTL order of events

This example demonstrates the deletion dates of three column views where `ttl:30d`

| View date | ttl date of deletion | Explanation |
|---|---|---|
| 2022 | January 30, 2023 | Date assumed to be end of 2022 |
| 2022-09 | October 30, 2022 | Date assumed to be end of September |
| 2022-09-02 | 2022-10-02 | Deletion after 30 days as intended |
