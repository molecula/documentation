---
title: Tutorial - Ingest NDJSON with BULK INSERT
---

## Before you begin
{% include /sql-preview/before_ingest.md %}

[Learn about the age dataset](https://www.gharchive.org/)

## Step 1: create table

```sql
CREATE TABLE github-stats (
_id ID, 
type STRING,
actor_id ID,
actor_login STRING,
actor_url STRING,
repo_id ID,
repo_name STRING,
repo_url STRING,
payload_ref STRING,
payload_ref_type STRING,
payload_master_branch STRING,
payload_description STRING,
payload_pusher_type STRING,
public BOOL,
created_at TIMESTAMP
);
```

## Step 2: ingest data

```sql
BULK INSERT INTO github-stats (
_id, 
type,
actor_id,
actor_login,
actor_url,
repo_id,
repo_name,
repo_url,
payload_ref,
payload_ref_type,
payload_master_branch,
payload_description,
payload_pusher_type,
public,
created_at
)
MAP (
'$.id' ID,
'$.type' STRING,
'$.actor.id' ID,
'$.actor.login' STRING,
'$.actor.url' STRING,
'$.repo.id' ID,
'$.repo.name' STRING,
'$.repo.url' STRING,
'$.payload.ref' STRING,
'$.payload.ref_type' STRING,
'$.payload.master_branch' STRING,
'$.payload.description' STRING,
'$.payload.pusher_type' STRING,
'$.public' BOOL,
'$.created_at' TIMESTAMP )
TRANSFORM(
@0,
@1,
@2,
@3,
@4,
@5,
@6,
@7,
@8,
@9,
@10,
@11,
@12,
CAST(@13 as BOOL),
@14)
FROM 'https://featurebase-public-data.s3.us-east-2.amazonaws.com/github-2015-data.json'
WITH
BATCHSIZE 10000
FORMAT 'NDJSON'
INPUT 'URL'
ALLOW_MISSING_VALUES;
```

## Step 3: query the data

```sql
SELECT COUNT(*) FROM github-stats;
```
```sql
SELECT TOP(10) * FROM github-stats;
```

## Further information

* [Bulk Insert](/sql-preview/sql-bulk-insert)