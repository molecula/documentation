---
id: getting-started
title: Getting Started With FeatureBase
sidebar_label: Getting Started With FeatureBase
---

FeatureBase supports multiple interfaces for querying and [ingestion](/community/community-data-ingestion/ingesters). For this tutorial, we shall use the `csv-ingester` to insert data and both the web-UI and Postgres interface (via psql) to get familiar with querying FeatureBase. Ultimately you'll probably want to interact with FeatureBase through a [client library](/community/query-data/libraries/python-library).

**NOTE:** 
Note that FeatureBase server requires a high limit for open files. Check the documentation of your system to see how to increase it in case you hit that limit. As a workaround, you can also cap FeatureBase's [max-file-count](/community/community-setup/featurebase-configuration#max-file-count).

### Starting FeatureBase

Grab the appropriate FeatureBase binary for your system from the release you were provided, or from [here](https://github.com/FeatureBaseDB/featurebase/releases/latest). Existing customers can also look for releases at https://releases.molecula.cloud/.

The FeatureBase binary can be run directly, with no setup and minimal configuration. For a production installation, some additional setup may be appropriate; see the [installation guide](/community/community-setup/installing-featurebase). 

**NOTE:** 
FeatureBase runs well on Linux and MacOS. It will not run on Windows.

You can place it somewhere on your `PATH`, or run the binary directly.

Execute the following in a terminal to run FeatureBase with the default configuration (FeatureBase will be available at [localhost:10101](http://localhost:10101)). The `--handler.allowed-origins` argument enables you to query FeatureBase from the [web-UI](/reference/api/enterprise/web-ui) via the given port and address. The `--postgres.bind` argument enables you to query FeatureBase from its Postgres-wire compatible endpoint, also via the given address and port.

```shell
featurebase server \
  --handler.allowed-origins http://localhost:3000 \
  --postgres.bind "localhost:55432"
```

From there, start the [web UI](/reference/api/enterprise/web-ui). It will indicate whether FeatureBase is running successfully on the homepage.  
If you prefer using the CLI, you can connect to and query FeatureBase using `psql`

```shell
psql -h localhost -p 55432
```

You can also use `curl` to check several HTTP endpoints that provide additional information, including `/status`, `/info`, and `/schema`. For example:

```shell
curl localhost:10101/status
```
```json
{
  "state": "NORMAL",
  "nodes": [
    {
      "id": "32ce5e768b0d8ca5",
      "uri": {
        "scheme": "http",
        "host": "localhost",
        "port": 10101
      },
      "grpc-uri": {
        "scheme": "grpc",
        "host": "localhost",
        "port": 20101
      },
      "isPrimary": true,
      "state": "STARTED"
    }
  ],
  "localID": "32ce5e768b0d8ca5",
  "clusterName": "cluster0"
}
```

### Sample Project

In order to better understand FeatureBase's capabilities, we will create a sample project called "Star Trace" containing information about 1,000 popular Github repositories which have "go" in their name. The Star Trace index will include data points such as programming language and stargazers—people who have starred a project.

Although FeatureBase doesn't keep the data in a tabular format, we still use the terms "columns" and "rows" when describing the data model. We put the primary objects in columns, and the properties of those objects in rows. For example, the Star Trace project will contain an index called "repository" which contains columns representing Github repositories, and rows representing properties like programming languages and stargazers. We can better organize the rows by grouping them into sets called Fields. So the "repository" index might have a "languages" field as well as a "stargazers" field. You can learn more about indexes and fields in the [Data Model](/concepts/data-modeling) section of the documentation.

**NOTE:** 
If at any time you want to verify the data structure, you can request the schema as follows:

```shell
curl localhost:10101/schema
```
```json
{
  "indexes": [
    {
      "name": "repository",
      "options": {
        "keys": false,
        "trackExistence": true
      },
      "fields": [
        {
          "name": "language",
          "options": {
            "type": "set",
            "cacheType": "ranked",
            "cacheSize": 50000,
            "keys": false
          }
        },
        {
          "name": "stargazer",
          "options": {
            "type": "time",
            "timeQuantum": "YMD",
            "keys": false,
            "noStandardView": false
          }
        }
      ],
      "shardWidth": 1048576
    }
  ]
}
```
**NOTE:** 
This is the response you should receive once completing this project. It has also been formatted using [`jq`](https://stedolan.github.io/jq) (external link).


### Ingesting the data

To reiterate, each Project has a set of languages used and a set of users who starred the project. Additionally, we will also be tracking the time at which users starred a given project using time-quantums. As far as github projects go, the languages used within the project evolve separately from when users star a project. To simulate this, we'll ingest the languages used separately from the stargazers.

First, download the `stargazer.csv` and `language.csv` files using these commands:

```shell
curl -O https://raw.githubusercontent.com/pilosa/getting-started/master/stargazer.csv
curl -O https://raw.githubusercontent.com/pilosa/getting-started/master/language.csv
```

Note that both the user IDs and the repository IDs were remapped from Github entities to sequential integers in the data files. You can check out [languages.txt](https://github.com/pilosa/getting-started/blob/master/languages.txt) to see the mapping for languages.

### Ingest Data
Ingest the language data using the `molecula-consumer-csv` command:
```shell
molecula-consumer-csv \
    --index repository \
    --header "language__ID_F,project_id__ID_F" \
    --id-field project_id \
    --batch-size 1000 \
    --files language.csv 

```

There are a couple of things to note about the above command, particularly the flags and arguments used: 
* `--index`: set the index that shall be used. If this index does not exist, it shall be created automatically. 
* `--header`: set the header to be used if the original csv file does not have a header. Each column name also specifies the type that FeatureBase shall use to represent the data (after the two underscores). For more details on all the data-types that FeatureBase avails, be sure to check out the [Field Types](/community/community-data-ingestion/ingester-configuration) section later on. For now, it suffices to say that the `ID` type is a simple integer representation of a particular property that an object has. For example, if an object has `project_id` set to 10 and `language` set to 6, 8 and 18, it means that the object was assigned the project ID 10 and uses Go, C and Python. 
* `--id-field`: specify which column contains the primary key for the object. 
* `--batch-size`: by default `molecula-consumer-csv` ingests rows one at a time which is quite slow. To speed up ingestion, set the batch size to a higher number such as 1000. The exact batch-size to be used though depends on the domain, setting and tradeoffs. 
* `--files`: provide the path to the file to ingest data from.

Next,ingest the stargazers via the following command:

```shell
molecula-consumer-csv \
    --index repository \
    --header "stargazer__ID_F_YMD,project_id__ID_F,date__RecordTime_2006-01-02T15:04" \
    --id-field 'project_id' \
    --batch-size 50000 \
    --files stargazer.csv
```

Note that `--batch-size` is set to a larger value this time. Furthermore, as mentioned earlier, we are tracking not just which user starred a project, but also when they did it, with a time field. The last argument for the `stargazer` field, with the value of `YMD`, sets the field's [time quantum](/concepts/glossary#time-quantum) (granularity) to year, month, day.


### Querying the data
With the index populated, queries can now be used to explore the data. These can be executed via either psql or the web UI.

Which repositories did user 14 star:
```shell
[repository]Row(stargazer=14);
```
```table
 _id 
═════
 1
 2
 3
 362
 368
 391
 ... // truncated
 (27 rows)
```

What are the top 5 languages in the sample data:
```shell
[repository]TopN(language, n=5);
```
```table
+-----------+--------+
|  language | count  |
+-----------+--------+
|         5 |    119 |
|         1 |     50 |
|         4 |     48 |
|         9 |     31 |
|        13 |     25 |
+-----------+--------+
(5 rows)
```

Which repositories were starred by user 14 and 19:
```shell
[repository]Intersect(
    Row(stargazer=14), 
    Row(stargazer=19)
);
```
```table
 _id 
═════
 2
 3
 362
 396
 416
 461
 464
 466
 470
 486
(10 rows)
```

Which repositories were starred by user 14 or 19:
```shell
[repository]Union(
    Row(stargazer=14), 
    Row(stargazer=19)
);
```
```table
 _id 
═════
 1
 2
 3
 361
 362
 368
 376
 377
 378
... // truncated
(50 rows)
```

Which repositories were starred by user 14 and 19 and also were written in language 1:
```shell
[repository]Intersect(
    Row(stargazer=14), 
    Row(stargazer=19),
    Row(language=1)
);
```
```table
 _id 
═════
 2
 362
 416
 461
(4 rows)
```

Set user 99999 as a stargazer for repository 77777:
```shell
[repository]Set(77777, stargazer=99999);
```
```table
 result 
════════
 true
(1 row)
```

Please note that while user ID 99999 may not be sequential with the other column IDs, it is still a relatively low number. 
Don't try to use arbitrary 64-bit integers as column or row IDs in FeatureBase - this will lead to problems such as poor performance and out of memory errors.
