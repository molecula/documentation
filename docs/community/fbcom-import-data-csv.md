---
title: How do I import data using a CSV?
---

## Before you begin

* Create a CSV file containing your data

NEED REF FILE INFO ON THE INGESTER AND THE FLAGS

## Run the CSV ingest script

1. Open a terminal and cd to the featurebase directory
2. Execute the following command and substitute your csv filename for `sample.csv`
```
idk/molecula-consumer-csv --auto-generate --index=allyourbase --files=gist/sample.csv
```

## Example

In this example, you will:
* create a CSV file based on supplied data
* run the CSV ingester

### Step one: create CSV file

1. Create `sample.csv` in the `/featurebase` directory.
2. Copy and paste the following data to the file:

```
asset_tag__String,fan_time__RecordTime_2006-01-02,fan_val__String_F_YMD
ABCD,2019-01-02,70%
ABCD,2019-01-03,20%
BEDF,2019-01-02,70%
BEDF,2019-01-05,90%
ABCD,2019-01-30,40%
BEDF,2019-01-08,10%
BEDF,2019-01-08,20%
ABCD,2019-01-04,30%
```

### Step two: ingest the data

1. Open a terminal and cd to the featurebase directory.
2. Execute the following command:
```
idk/molecula-consumer-csv --auto-generate --index=allyourbase --files=gist/sample.csv
```

## Next step

* [Learn how to query a FeatureBase database]()

## Further information


## Get support

{% include /docs/get-support-source.md %}
