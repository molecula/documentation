To take advantage of fast queries, reduced storage and hardware overheads, you must import your data to FeatureBase.

The multi-part process to do this is called **ingestion** and involves:

* data modeling and mapping to determine the best data types and constraints to apply to destination table columns
* setup and configuration of HTTPS streaming endpoints to receive JSON data
* automatic transformation of JSON source data to roaring bitmap format
* copy of data to destination table columns
