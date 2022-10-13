---
title: Welcome to FeatureBase!
---

FeatureBase is a [B-tree](https://en.wikipedia.org/wiki/B-tree) database which uses [Roaring Bitmaps](https://roaringbitmap.org/). This makes it suitable for doing analytical queries on massive data sets immediately after ingestion. If you are the inquisitive type, you may be interested in the [architectural overview](https://docs.featurebase.com/setting-up-featurebase/enterprise/architecture).

This welcome guide is designed to get you started using FeatureBase on a Mac or Linux/UNIX based system in around five minutes. It covers downloading and starting the FeatureBase server as well as ingesting and querying a small amount of data. Other guides and documentation may be accessed via the sidebar to your left.

If you are using Windows, you may [build the binary](https://github.com/featurebasedb/featureBase/#build-featurebase-server-from-source) yourself or use our [cloud trial](https://cloud.featurebase.com/signup).

## Install (Mac or Linux)
Start by heading over to the [downloads](https://github.com/FeatureBaseDB/FeatureBase/releases) on the [Github repo](https://github.com/FeatureBaseDB/featurebase) and select the build needed for your particular architecture. The ARM version are for newer Macs or devices like the Raspberry Pi. The AMD versions are for Intel architectures.

From here on, we'll assume you are using the v1.1.0 ARM version on a newer macOS-based machine. Keep in mind there may be newer versions of the software available.

Open a terminal and move into the directory where you downloaded FeatureBase. Copy and paste these commands to create a new directory and move the tarball into it:

```
mkdir featurebase
mv featurebase-*.tar.gz featurebase
cd featurebase
```

**OUTPUT:**
```
kord@bob Downloads % mkdir featurebase
kord@bob Downloads % mv featurebase-*.tar.gz featurebase
kord@bob Downloads % cd featurebase
kord@bob featurebase % ls
featurebase-v1.1.0-community-darwin-arm64.tar.gz
```

Now use `tar` to uncompress the file:

```
tar xvfz featurebase-*-arm64.tar.gz
```

**OUTPUT:**
```
kord@bob featurebase % tar xvfz featurebase-*-arm64.tar.gz
x featurebase-v1.1.0-community-darwin-arm64/
x featurebase-v1.1.0-community-darwin-arm64/featurebase.redhat.service
x featurebase-v1.1.0-community-darwin-arm64/NOTICE
x featurebase-v1.1.0-community-darwin-arm64/featurebase
x featurebase-v1.1.0-community-darwin-arm64/featurebase.debian.service
x featurebase-v1.1.0-community-darwin-arm64/featurebase.conf
x idk-v1.1.0-community-darwin-arm64/
x idk-v1.1.0-community-darwin-arm64/molecula-consumer-github
x idk-v1.1.0-community-darwin-arm64/molecula-consumer-sql
x idk-v1.1.0-community-darwin-arm64/molecula-consumer-csv
x idk-v1.1.0-community-darwin-arm64/molecula-consumer-kafka-static
x idk-v1.1.0-community-darwin-arm64/molecula-consumer-kinesis
```

Let's move the directories into something that's a little easier to type:

```
mv featurebase-*-community-darwin-arm64/ opt
mv idk-*-arm64 idk
```

**OUTPUT:**
```
kord@bob featurebase % mv featurebase-*-community-darwin-arm64/ opt
kord@bob featurebase % mv idk-*-arm64 idk
```

Let's check the directory structure:

```
kord@bob featurebase % ls
opt    idk
```

**NOTE:**
The `idk` directory contains a few ingestion tools. We'll get to this in a minute.

## Set File Flags to Run
Before you start the server, you may need to turn off the quarantine flag on the executables so they can run them from the command line (assuming you are using macOS):

```
xattr -d com.apple.quarantine opt/featurebase
xattr -d com.apple.quarantine idk/*
```

## Start the Server
Start the server by changing into the `opt` directory and running `./featurebase server`:

```
kord@bob ~ % cd ~/Downloads/featurebase/opt
kord@bob fb % ./featurebase server
2022-09-30T21:26:19.033157Z INFO:  Molecula Pilosa v1.1.0-community (Sep 30 2022 3:26PM, e75abc3c) go1.19.1
2022-09-30T21:26:19.036403Z INFO:  rbf config = &cfg.Config{MaxSize:4294967296, MaxWALSize:4294967296, MinWALCheckpointSize:1048576, MaxWALCheckpointSize:2147483648, FsyncEnabled:true, FsyncWALEnabled:true, DoAllocZero:false, CursorCacheSize:0, Logger:logger.Logger(nil), MaxDelete:65536}
2022-09-30T21:26:19.036432Z INFO:  cwd: /Users/kord/code/scratch/opt
2022-09-30T21:26:19.036436Z INFO:  cmd line: ./featurebase server
2022-09-30T21:26:19.094964Z INFO:  enabled Web UI at :10101
2022-09-30T21:26:19.095062Z INFO:  open server. PID 90764
2022-09-30T21:26:20.926742Z INFO:  open holder path: /Users/kord/.pilosa
2022-09-30T21:26:20.926914Z INFO:  holder translation sync monitor initializing
2022-09-30T21:26:20.927158Z INFO:  holder translation sync beginning
2022-09-30T21:26:25.889248Z INFO:  diagnostics disabled
2022-09-30T21:26:25.889287Z INFO:  listening as http://localhost:10101
2022-09-30T21:26:25.889300Z INFO:  start initial cluster state sync
2022-09-30T21:26:25.889312Z INFO:  completed initial cluster state sync in 19.875µs
2022-09-30T21:26:25.889359Z INFO:  enabled grpc listening on 127.0.0.1:20101
```

**NOTE:**
Pilosa is the older name of the FeatureBase server, which was created by Molecula (DBA FeatureBase). Pilosas are an order of xenarthran placental mammals, native to the Americas. It includes the anteaters and sloths, which includes the extinct ground sloths. The name comes from the Latin word for "hairy".

## Access the UI
Now we have the server running, open a new browser tab and access the UI using the following URL:

```
http://localhost:10101/
```

**NOTE:** 
FeatureBase runs on port `10101`.

![ui](/img/localhost.png)

## Ingest Data
We're now ready to ingest data. Create a new terminal window and copy the following and paste it into a `sample.csv` file located in the `featurebase` directory:

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

We'll use the `molecula-consumer-csv` tool (located in idk) to ingest the `sample.csv` file:

```
idk/molecula-consumer-csv \
--auto-generate \
--index=allyourbase \
--files=sample.csv
```

**Output:**

```
kord@bob featurebase % idk/molecula-consumer-csv --auto-generate --index=allyourbase --files=gist/sample.csv
Molecula Consumer v3.20.0, build time 2022-08-26T00:11:50+0000
2022-09-23T20:07:25.430833Z INFO:  Serving Prometheus metrics with namespace "ingester_csv" at localhost:9093/metrics
2022-09-23T20:07:25.434554Z INFO:  start ingester 0
2022-09-23T20:07:25.434862Z INFO:  processFile: gist/sample.csv
2022-09-23T20:07:25.435059Z INFO:  new schema: []idk.Field{idk.StringField{NameVal:"asset_tag", DestNameVal:"asset_tag", Mutex:false, Quantum:"", TTL:"", CacheConfig:(*idk.CacheConfig)(nil)}, idk.RecordTimeField{NameVal:"fan_time", DestNameVal:"fan_time", Layout:"2006-01-02", Epoch:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), Unit:""}, idk.StringField{NameVal:"fan_val", DestNameVal:"fan_val", Mutex:false, Quantum:"YMD", TTL:"", CacheConfig:(*idk.CacheConfig)(nil)}}
2022-09-23T20:07:25.436104Z INFO:  Listening for /debug/pprof/ and /debug/fgprof on 'localhost:6062'
2022-09-23T20:07:25.478702Z INFO:  translating batch of 8 took: 41.931708ms
2022-09-23T20:07:25.478805Z INFO:  making fragments for batch of 8 took 110.25µs
2022-09-23T20:07:25.481605Z INFO:  importing fragments took 2.799375ms
2022-09-23T20:07:25.481918Z INFO:  1 records processed 0-> (9)
2022-09-23T20:07:25.481925Z INFO:  metrics: import=46.120541ms
```

**NOTE:** If you need to set the execute flag on the idk/ executables:

```
chmod 755 idk/*
```

## Querying
Now we have our sample data loaded, we can write a simple SQL query in the admin UI to view the "rows":

```
select * from allyourbase;
```

![sql](/img/sql.png)

In the [next section](/setting-up-featurebase/enterprise/installing-featurebase), we'll cover running FeatureBase as a daemon on Linux.

