---
id: install-config-community
title: Install and configure FeatureBase community
sidebar_label: Install & configure FeatureBase community
---

This welcome guide is designed to get you started using FeatureBase on a Mac or Linux/UNIX based system in around five minutes. It covers downloading and starting the FeatureBase server as well as ingesting and querying a small amount of data. Other guides and documentation may be accessed via the sidebar to your left.

If you are using Windows, you may [build the binary](https://github.com/featurebasedb/featureBase/#build-featurebase-server-from-source) yourself or use our [cloud trial](https://cloud.featurebase.com/signup).

## Install (Mac or Linux)
Start by heading over to the [downloads](https://github.com/FeatureBaseDB/FeatureBase/releases) on the [Github repo](https://github.com/FeatureBaseDB/featurebase) and select the builds needed for your particular architecture.

From here on, we'll assume you are using the v1.3.0 ARM version on a newer macOS-based machine. Keep in mind there may be newer versions of the software available.

Open a terminal and move into the directory where you downloaded FeatureBase. Copy and paste these commands to create a new directory and move the tarball into it:

```
mkdir ~/featurebase
mv featurebase-*.tar.gz ~/featurebase
cd ~/featurebase
```

**OUTPUT:**
```
kord@bob Downloads % mkdir ~/featurebase
kord@bob Downloads % mv ~/featurebase-*.tar.gz featurebase
kord@bob Downloads % cd ~/featurebase
kord@bob featurebase % ls
featurebase-v1.3.0-community-darwin-arm64.tar.gz
```

Now use `tar` to uncompress the file:

```
tar xvfz featurebase-*-arm64.tar.gz
```

**OUTPUT:**
```
kord@bob featurebase % tar xvfz featurebase-*-arm64.tar.gz
x featurebase-v1.3.0-community-darwin-arm64/
x featurebase-v1.3.0-community-darwin-arm64/featurebase.redhat.service
x featurebase-v1.3.0-community-darwin-arm64/NOTICE
x featurebase-v1.3.0-community-darwin-arm64/featurebase
x featurebase-v1.3.0-community-darwin-arm64/featurebase.debian.service
x featurebase-v1.3.0-community-darwin-arm64/featurebase.conf
x idk-v1.3.0-community-darwin-arm64/
x idk-v1.3.0-community-darwin-arm64/molecula-consumer-github
x idk-v1.3.0-community-darwin-arm64/molecula-consumer-sql
x idk-v1.3.0-community-darwin-arm64/ingester
x idk-v1.3.0-community-darwin-arm64/molecula-consumer-csv
x idk-v1.3.0-community-darwin-arm64/molecula-consumer-kafka-static
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
Before you start the server, if you are running macOS, you may need to turn off the quarantine flag on the executables so they may be run from the command line:

```
xattr -d com.apple.quarantine opt/featurebase
xattr -d com.apple.quarantine idk/*
```

## Start the Server
Start the server by changing into the `opt` directory and running `./featurebase server`:

```
cd ~/featurebase/opt/
./featurebase server
```


```
kord@bob ~ % cd ~/featurebase/opt
kord@bob fb % ./featurebase server
2022-11-18T16:03:06.968894Z INFO:  Molecula Pilosa v1.3.0-community-1-g2709973b (Nov 17 2022 8:21PM, 2709973b) go1.19.3
2022-11-18T16:03:06.973582Z INFO:  rbf config = &cfg.Config{MaxSize:4294967296, MaxWALSize:4294967296, MinWALCheckpointSize:1048576, MaxWALCheckpointSize:2147483648, FsyncEnabled:true, FsyncWALEnabled:true, DoAllocZero:false, CursorCacheSize:0, Logger:logger.Logger(nil), MaxDelete:65536}
2022-11-18T16:03:06.973613Z INFO:  cwd: /Users/kord/code/scratch/opt
2022-11-18T16:03:06.973615Z INFO:  cmd line: ./featurebase server
2022-11-18T16:03:07.029761Z INFO:  enabled Web UI at :10101
2022-11-18T16:03:07.029839Z INFO:  open server. PID 54729
2022-11-18T16:03:08.497600Z INFO:  open holder path: /Users/kord/.pilosa
2022-11-18T16:03:08.497659Z INFO:  holder translation sync monitor initializing
2022-11-18T16:03:08.497670Z INFO:  holder translation sync beginning
2022-11-18T16:03:08.498714Z INFO:  opening index: allyourbase
2022-11-18T16:03:08.663573Z INFO:  open holder: complete
2022-11-18T16:03:08.698390Z INFO:  diagnostics disabled
2022-11-18T16:03:08.698456Z INFO:  listening as http://localhost:10101
2022-11-18T16:03:08.698548Z INFO:  start initial cluster state sync
2022-11-18T16:03:08.698563Z INFO:  completed initial cluster state sync in 78.041µs
2022-11-18T16:03:08.698569Z INFO:  enabled grpc listening on 127.0.0.1:20101
```

**NOTE:**
Pilosa is the older name of the FeatureBase server, which was created by Molecula (DBA FeatureBase). Pilosas are a suborder of xenarthran placental mammals, native to the Americas. Xenartharans include armadillos (native to Texas), anteaters, and sloths. The super order also includes the extinct ground sloths, which were huge hairy creatures as large as a hippo.

## Access the UI
Now we have the server running, open a new browser tab and access the UI using the following URL. *It is recommended to use Chrome or Firefox as the UI does not work in Safari currently*:

```
http://localhost:10101/
```

**NOTE:**
FeatureBase runs on port `10101`.

![ui](/img/welcome/localhost.png)

## Ingest Data
We're now ready to create some ingest data. Start by copying the following text: 

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

On `macOS`, you can paste into the file from a terminal window:

```
pbpaste > sample.csv
```

**OUTPUT:**
```
kord@bob featurebase % pbpaste > sample.csv
kord@bob featurebase % ls sample.csv
sample.csv
```

### Run the Consumer
We'll use the `molecula-consumer-csv` tool (located in idk) to ingest the `sample.csv` file:

```
idk/molecula-consumer-csv \
--auto-generate \
--index=allyourbase \
--files=sample.csv
```

**Output:**

```
kord@bob featurebase % idk/molecula-consumer-csv --auto-generate --index=allyourbase --files=sample.csv
Molecula Consumer v1.3.0-community-1-g2709973b, build time 2022-11-18T02:20:21+0000
2022-11-18T16:05:53.776811Z INFO:  Serving Prometheus metrics with namespace "ingester_csv" at localhost:9093/metrics
2022-11-18T16:05:53.780819Z INFO:  start ingester 0
2022-11-18T16:05:53.781277Z INFO:  processFile: sample.csv
2022-11-18T16:05:53.781377Z INFO:  new schema: []idk.Field{idk.StringField{NameVal:"asset_tag", DestNameVal:"asset_tag", Mutex:false, Quantum:"", TTL:"", CacheConfig:(*idk.CacheConfig)(nil)}, idk.RecordTimeField{NameVal:"fan_time", DestNameVal:"fan_time", Layout:"2006-01-02", Epoch:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), Unit:""}, idk.StringField{NameVal:"fan_val", DestNameVal:"fan_val", Mutex:false, Quantum:"YMD", TTL:"", CacheConfig:(*idk.CacheConfig)(nil)}}
2022-11-18T16:05:53.782805Z INFO:  Listening for /debug/pprof/ and /debug/fgprof on 'localhost:6062'
2022-11-18T16:05:53.863171Z INFO:  translating batch of 1 took: 79.331125ms
2022-11-18T16:05:53.863343Z INFO:  making fragments for batch of 1 took 179µs
2022-11-18T16:05:53.864938Z INFO:  importing fragments took 1.59375ms
2022-11-18T16:05:53.865354Z INFO:  records processed 0-> (1)
<snip>
2022-11-18T16:55:32.272168Z INFO:  importing fragments took 957.417µs
2022-11-18T16:55:32.272698Z INFO:  records processed 0-> (8)
2022-11-18T16:55:32.272720Z INFO:  metrics: import=554.054959ms
```

## Querying
Now we have our sample data loaded, we can write a simple SQL query in the admin UI to view the "rows". Be sure to click on **Query** in the left bar to get the query UI up.

```
select * from allyourbase;
```

![sql](/img/welcome/sql.png)

In the [next section](/community/community-setup/installing-featurebase), we'll cover running FeatureBase as a daemon on Linux.
