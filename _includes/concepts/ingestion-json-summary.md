Data ingestion relies on properly configured JSON files which contain:
* Primary key data to map to the target ID column
* Source column names and data

FeatureBase ingests data in batches of:
* up to 1000 records, or
* 1MB of data.
