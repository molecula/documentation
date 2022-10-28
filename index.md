---
title: Welcome to FeatureBase!
---

FeatureBase is a [B-tree](https://en.wikipedia.org/wiki/B-tree) database which uses [Roaring Bitmaps](https://roaringbitmap.org/). This makes it suitable for doing analytical queries on massive data sets immediately after ingestion. If you are the inquisitive type, you may be interested in the [architectural overview](https://docs.featurebase.com/setting-up-featurebase/enterprise/architecture).

This welcome guide is designed to get you started using FeatureBase on a Mac or Linux/UNIX based system in around five minutes. It covers downloading and starting the FeatureBase server as well as ingesting and querying a small amount of data. Other guides and documentation may be accessed via the sidebar to your left.

If you are using Windows, you may [build the binary](https://github.com/featurebasedb/featureBase/#build-featurebase-server-from-source) yourself or use our [cloud trial](https://cloud.featurebase.com/signup).

## Install (Mac or Linux)
Start by heading over to the [downloads](https://github.com/FeatureBaseDB/FeatureBase/releases) on the [Github repo](https://github.com/FeatureBaseDB/featurebase) and select the builds needed for your particular architecture. The ARM versions are for newer Macs or devices like the Raspberry Pi. The AMD versions are for Intel architectures.

**NOTE:**
Be sure to download the corresponding IDK builds. They are used for ingesting data into the FeatureBase binary.

From here on, we'll assume you are using the v1.2.0 ARM versions on a newer macOS-based machine. Keep in mind there may be newer versions of the software available.

Open a terminal and move into the directory where you downloaded FeatureBase. Copy and paste these commands to create a new directory and move the tarball into it:

```
mkdir ~/featurebase
mv featurebase-*.tar.gz ~/featurebase
mv idk-*.tar.gz* ~/featurebase
cd ~/featurebase
```

**OUTPUT:**
```
kord@bob Downloads % mkdir featurebase
kord@bob Downloads % mv featurebase-*.tar.gz featurebase
kord@bob Downloads % mv idk-*.tar.gz featurebase
kord@bob Downloads % cd featurebase
kord@bob featurebase % ls
featurebase-v1.2.0-community-darwin-arm64.tar.gz
idk-v1.2.0-community-darwin-arm64.tar.gz.tar
```

Now use `tar` to uncompress the files:

```
tar xvfz featurebase-*-arm64.tar.gz
tar xvfz idk-*-arm64.tar.gz*
```

**OUTPUT:**
```
kord@bob featurebase % tar xvfz featurebase-*-arm64.tar.gz
x featurebase-v1.2.0-community-darwin-arm64/
x featurebase-v1.2.0-community-darwin-arm64/featurebase.redhat.service
x featurebase-v1.2.0-community-darwin-arm64/NOTICE
x featurebase-v1.2.0-community-darwin-arm64/featurebase
x featurebase-v1.2.0-community-darwin-arm64/featurebase.debian.service
x featurebase-v1.2.0-community-darwin-arm64/featurebase.conf

kord@bob featurebase % tar xvfz idk-*-arm64.tar.gz*
x idk-v3.23.0-darwin-arm64/
x idk-v3.23.0-darwin-arm64/molecula-consumer-kinesis
x idk-v3.23.0-darwin-arm64/molecula-consumer-csv
x idk-v3.23.0-darwin-arm64/molecula-consumer-kafka-static
x idk-v3.23.0-darwin-arm64/molecula-consumer-sql
x idk-v3.23.0-darwin-arm64/molecula-consumer-github
```

Let's move the directories into something that's a little easier to type:

```
mv featurebase-*-arm64/ opt
mv idk-*-arm64 idk
```

**OUTPUT:**
```
kord@bob featurebase % mv featurebase-*-community-darwin-arm64/ opt
kord@bob featurebase % mv idk-*-arm64 idk
```

Now remove the offending tarballs (optional AND BE CAREFUL WITH THIS):

```
rm *.gz*
```

Let's check the directory structure:

```
kord@bob featurebase % ls -lah
drwxr-xr-x@ 7 kord  staff   224B Oct 28 12:19 idk
drwxr-xr-x@ 7 kord  staff   224B Oct 28 12:19 opt
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
kord@bob opt % ./featurebase server
2022-10-28T19:59:50.223833Z INFO:  Molecula Pilosa v1.2.0-community (Oct 28 2022 12:19PM, daceee2a) go1.19.1
2022-10-28T19:59:50.230339Z INFO:  rbf config = &cfg.Config{MaxSize:4294967296, MaxWALSize:4294967296, MinWALCheckpointSize:1048576, MaxWALCheckpointSize:2147483648, FsyncEnabled:true, FsyncWALEnabled:true, DoAllocZero:false, CursorCacheSize:0, Logger:logger.Logger(nil), MaxDelete:65536}
2022-10-28T19:59:50.230372Z INFO:  cwd: /Users/kord/featurebase/opt
2022-10-28T19:59:50.230375Z INFO:  cmd line: ./featurebase server
2022-10-28T19:59:50.233328Z INFO:  open server. PID 58251
2022-10-28T19:59:51.579041Z INFO:  open holder path: /Users/kord/.pilosa
2022-10-28T19:59:51.579095Z INFO:  holder translation sync monitor initializing
2022-10-28T19:59:51.579114Z INFO:  holder translation sync beginning
2022-10-28T19:59:51.598429Z INFO:  opening index: allyourbase
2022-10-28T19:59:51.777437Z INFO:  open holder: complete
2022-10-28T19:59:51.778019Z INFO:  diagnostics disabled
2022-10-28T19:59:51.778111Z INFO:  listening as http://localhost:10101
2022-10-28T19:59:51.778202Z INFO:  start initial cluster state sync
2022-10-28T19:59:51.778219Z INFO:  completed initial cluster state sync in 37.959µs
2022-10-28T19:59:51.778278Z INFO:  enabled grpc listening on 127.0.0.1:20101
```

**NOTE:**
Pilosa is the older name of the FeatureBase server, which was created by Molecula (DBA FeatureBase). Pilosas are an order of xenarthran placental mammals, native to the Americas. It includes the anteaters, sloths, and the extinct ground sloths. The name comes from the Latin word for "hairy".

Together with the armadillos, which are in the order Cingulata, pilosans are part of the larger superorder [Xenarthra](https://en.wikipedia.org/wiki/Xenarthra).

Evidently the term "pilosa" is a profanity in Italian.

## Access the UI
Now we have the server running, open a new browser tab and access the UI using the following URL. It is recommended to use Chrome or Firefox as the UI does not work in Safari currently:

```
http://localhost:10101/
```

**NOTE:** 
FeatureBase runs on port `10101`.

![ui](/img/welcome/localhost.png)

## Create Data
Create a new terminal window and copy the following and paste it into a `sample.csv` file located in the `featurebase` directory under `~Documents`:

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

In the terminal, you can use `pico` to edit the file:

```
kord@bob featurebase % pico sample.csv

```

Crtl-X in pico will quit and save. You may also use another editor of your choice.

Now you have a `sample.csv` file, we'll use the `molecula-consumer-csv` tool (located in idk) to ingest the file:

```
idk/molecula-consumer-csv \
--auto-generate \
--index=allyourbase \
--files=sample.csv
```

**Output:**

```
kord@bob featurebase % idk/molecula-consumer-csv --auto-generate --index=allyourbase --files=gist/sample.csv
Molecula Consumer v3.23.0, build time 2022-10-27T23:42:47+0000
2022-10-28T20:14:17.518462Z INFO:  setting up stats: listen for metrics on 'localhost:9093': listen tcp 127.0.0.1:9093: bind: address already in use
2022-10-28T20:14:17.522488Z INFO:  start ingester 0
2022-10-28T20:14:17.522956Z INFO:  processFile: sample.csv
2022-10-28T20:14:17.523039Z INFO:  new schema: []idk.Field{idk.StringField{NameVal:"asset_tag", DestNameVal:"asset_tag", Mutex:false, Quantum:"", TTL:"", CacheConfig:(*idk.CacheConfig)(nil)}, idk.RecordTimeField{NameVal:"fan_time", DestNameVal:"fan_time", Layout:"2006-01-02", Epoch:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), Unit:""}, idk.StringField{NameVal:"fan_val", DestNameVal:"fan_val", Mutex:false, Quantum:"YMD", TTL:"", CacheConfig:(*idk.CacheConfig)(nil)}}
2022-10-28T20:14:17.531197Z INFO:  Listening for /debug/pprof/ and /debug/fgprof on 'localhost:6062'
2022-10-28T20:14:17.944749Z INFO:  translating batch of 1 took: 92.211042ms
2022-10-28T20:14:17.945077Z INFO:  making fragments for batch of 1 took 357.166µs
```

## Querying
Now we have our sample data loaded, we can write a simple SQL query in the admin UI to view the "rows":

```
select * from allyourbase;
```

![sql](/img/welcome/sql.png)

In the [next section](/setting-up-featurebase/enterprise/installing-featurebase), we'll cover running FeatureBase as a daemon on Linux.

