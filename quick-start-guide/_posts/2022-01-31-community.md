---
title: Community Quick Start Guide
---

## Welcome to your FeatureBase Trial!

<!---
With the rebrand to FeatureBase, we should consider updating the use of molecula as users and in directories in the future. This needs to be coordinated with both this guide and the files that come in community releases
-->

Follow the guide outlined below for a hands-on demonstration of low-latency queries at scale using FeatureBase Community edition. As you work through the guide, please note any questions or feedback that you may have for the FeatureBase team. We’re always looking for ways to improve the experience!

In this demonstration you will:

1. Download a FeatureBase binary
2. Configure and run FeatureBase
3. Restore two large-scale datasets into the database
4. Run a set of analytics queries

>If you run into any roadblocks or have questions throughout the demonstration, please reach out to your FeatureBase representative or email se@featurebase.com.

## Download FeatureBase Binary
To download releases of FeatureBase, you must have a github account.

You can see the latest FeatureBase release [here](https://github.com/FeatureBaseDB/featurebase/releases/latest)

>Please note that by downloading FeatureBase you agree to the [License](https://github.com/FeatureBaseDB/featurebase/blob/master/LICENSE-2.0.txt) and to receive occasional marketing emails from the FeatureBase team. You also understand that we will process your personal information in accordance with our [Privacy Policy](https://www.featurebase.com/privacy-policy/).


Click on the option that best meets your hardware's needs to download the tarball containing the latest FeatureBase binary.
 

## Configuring FeatureBase - MacOS

>Note: The FeatureBase executable are built for x86_64 and ARM64 CPU architectures. If you aren't running macOS, there are two other options. You can install and run FeatureBase on [Linux](#configuring-featurebase---linux) or a Docker container. 

>**Note:** Make sure you have ```wget```. If not, run ```brew install wget```. 

>**Note:** If you receive this error, it can be resolved in security & privacy settings on your Mac
>```"featurebase" cannot be opened because the developer cannot be verified"```

First, open the Terminal application and type the code below to access the ```Downloads``` folder. 
```
cd ~/Downloads
```

Next, extract the ```.tar.gz file``` , copy the FeatureBase binary located in the ```featurebase=<version+architecture>/``` directory in the extract to your ```/usr/local/bin folder```, and make it executable. 
  
For the MacOS AMD64 Version: 
```
tar -zxvf featurebase-community-v1.0.0-darwin-amd64.tar.gz
sudo cp ~/Downloads/featurebase-community-v1.0.0-darwin-amd64/featurebase-v3.20.0-darwin-amd64/featurebase /usr/local/bin/
chmod ugo+x /usr/local/bin/featurebase
```
For the MacOS ARM64 Version: 
```
tar -zxvf featurebase-community-v1.0.0-darwin-arm64.tar.gz
sudo cp ~/Downloads/featurebase-community-v1.0.0-darwin-arm64/featurebase-v3.20.0-darwin-arm64/featurebase /usr/local/bin/
chmod ugo+x /usr/local/bin/featurebase
``` 
>**Note:** The copy or cp command above moves the FeatureBase binary to ```/usr/local/bin/```. 
Ensure this folder is in your path variable by, running ```echo $PATH``` in the command line and confirming ```/usr/local/bin/``` is there. 
If it's not, run ```export PATH=$PATH:/usr/local/bin``` to append it to your path variable.
  
Next, configure the FeatureBase server by creating and running the configuration file. Go to [FeatureBase Configuration](/setting-up-featurebase/enterprise/featurebase-configuration) for more on configuring FeatureBase.

<!---
we now include this file in a release, so we might want to consider making these align and conform in the future.
-->

```
sudo touch /etc/featurebase.conf
sudo chown `whoami` /etc/featurebase.conf
sudo nano /etc/featurebase.conf
```

Copy and paste the contents below. Then save and exit. 

```
name = "featurebase"
bind = "0.0.0.0:10101"
bind-grpc = "0.0.0.0:20101"

data-dir = "/var/lib/molecula"
log-path = "/var/log/molecula/featurebase.log"

[cluster]
    name = "cluster"
    replicas = 1

[etcd]
    listen-client-address = "http://localhost:10401"
    listen-peer-address = "http://localhost:10301"
    initial-cluster = "featurebase=http://localhost:10301"
 ```

In the code above, ```bind``` tells FeatureBase to listen for HTTP request on all IPv4 addresses on the local machine at port ```10101```. ```bind-grpc``` tells FeatureBase to listen for gRPC request on all IPv4 address on the local machine at port ```20101```. ```data-dir``` and ```log-path``` tell FeatureBase to write data and logs to their respective locations. 

You'll notice there is a generic featurebase.conf within the release that can be referenced and used outside of this guide.


### Setup Log and Data Folders
```featurebase.conf``` defined the ```data-dir``` and the ```log-path```. Here we'll want to create those folders and set the ```molecula``` user as the owner. The data directory is where FeatureBase puts the startup log file and the actual data that comprises the FeatureBase indexes. 

Create a log and data folder and change the owner: 

```
sudo mkdir -p /var/log/molecula && sudo chown $USER /var/log/molecula
sudo mkdir -p /var/lib/molecula && sudo chown $USER /var/lib/molecula
```
## Run FeatureBase

Next, run the `featurebase server` process in the background by running:

```
featurebase server -c /etc/featurebase.conf &
```
>**Note:** You may see a warning message similar to `“featurebase” can’t be opened because Apple cannot check it for malicious software.` If so, you need to navigate to "Security & Privacy" -> "General" settings to allow featurebase to be opened and run.

This concludes the deployment of FeatureBase on MacOS. Continue with [Restore 1 Billion Records](#restore-1b-records-of-demo-data-from-s3) to load data into your FeatureBase deployment.


## Configuring FeatureBase - Linux

>**Note:** If you aren't running Linux, there are two other options. You can install and run FeatureBase on [macOS](#configuring-featurebase---macos) or a Docker container. Note that FeatureBase executable is built for x86_64 and ARM64 CPU architectures.

>**Note:** Make sure you have ```wget``` . If not, run ```sudo yum install wget``` or ```sudo apt install wget```

First, download the appropriate binary for your system [here](https://github.com/FeatureBaseDB/featurebase/releases/latest).

Next, extract the ```.tar.gz file``` , copy the featurebase binary located in the ```featurebase=<version_architecture>/``` directory in the extract to your ```/usr/local/bin folder```, and make it executable. 

```
chmod +x featurebase
sudo cp featurebase /usr/local/bin
```

>**Note:** The copy or ```cp``` command above moves the ```featurebase``` binary to /usr/local/bin/. Ensure this folder is in your path variable by, running ```echo $PATH``` in the command line and confirming ```/usr/local/bin/``` is there. If it's not, run ```export PATH=$PATH:/usr/local/bin``` to append it to your path variable.

Next, create the configuration file: 
```
sudo nano /etc/featurebase.conf
```

<!---
we now include this file in a release, so we might want to consider making these align and conform in the future.
-->

Copy and paste the contents below. Then save and exit.
```
name = "featurebase"
bind = "0.0.0.0:10101"
bind-grpc = "0.0.0.0:20101"

data-dir = "/var/lib/molecula"
log-path = "/var/log/molecula/featurebase.log"

[cluster]
    name = "cluster"
    replicas = 1

[etcd]
    listen-client-address = "http://localhost:10401"
    listen-peer-address = "http://localhost:10301"
    initial-cluster = "featurebase=http://localhost:10301"
 ```
 
Above, ```bind``` tells FeatureBase to listen for HTTP request on all IPv4 addresses on the local machine at port ```10101```. ```bind-grpc``` tells FeatureBase to listen for gRPC request on all IPv4 address on the local machine at port ```20101```. ```data-dir``` and ```log-path``` tell FeatureBase to write data and logs to their respective locations. 

You'll notice there is a generic featurebase.conf within the release that can be referenced and used outside of this guide.

## Configure FeatureBase Service Unit
<!---
we now include the debian and redhat .service file in releases, so we may want to consider making these aligned or used in the future.
-->
On Linux, we recommend running FeatureBase as a ```systemd``` service unit. To learn more about ```systemd``` and units, go [here](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files). To configure the FeatureBase service unit's function, we'll create a ```.service``` file.

```
sudo nano /etc/systemd/system/featurebase.service
```
Copy and paste the contents below. Then save and exit.
```
[Unit]
    Description="Service for FeatureBase"

[Service]
    RestartSec=30
    Restart=on-failure
    User=molecula
    ExecStart=/usr/local/bin/featurebase server -c /etc/featurebase.conf

[Install]
    WantedBy=multi-user.target
```
>The service file above tells ```systemd``` we want to run ```/usr/local/bin/featurebase server -c /etc/featurebase.conf``` as the ```molecula``` user. This starts a FeatureBase server and configures it based on ```/etc/featurebase.conf```. Additionally, in the event that process fails, it tells ```systemd``` to try and restart that process 30 seconds.

## Setup Log and Data Folders
```featurebase.conf``` defined the ```data-dir``` and the ```log-path```. Here we'll want to create those folders and set the ```molecula``` user as the owner. The data directory is where FeatureBase puts the startup log file and the actual data that comprises the FeatureBase indexes. 

Create the molecula user:
```
sudo adduser molecula
```
Create a log and data folder and change the owner: 
```
sudo mkdir /var/log/molecula && sudo chown molecula:molecula /var/log/molecula
sudo mkdir -p /var/lib/molecula && sudo chown molecula:molecula /var/lib/molecula
```
## Run FeatureBase
Refresh ```systemd``` so the FeatureBase service unit will load. For more information on ```daemon-reload``` , go [here](https://serverfault.com/questions/700862/do-systemd-unit-files-have-to-be-reloaded-when-modified).

```
sudo systemctl daemon-reload
```

If you’d like to automatically start FeatureBase after a reboot, you can run:
```
sudo systemctl enable featurebase.service
```
Finally, start the FeatureBase service unit: 
```
sudo systemctl start featurebase
```
Verify it started successfully and is running:
```
sudo systemctl status featurebase
```
You get a message that looks like this:

```
● featurebase.service - "Service for FeatureBase"
     Loaded: loaded (/etc/systemd/system/featurebase.service; static; vendor preset: enabled)
     Active: active (running) since Fri 2021-10-08 13:29:38 CDT; 12s ago
   Main PID: 470112 (featurebase)
      Tasks: 17 (limit: 18981)
     Memory: 33.2M
     CGroup: /system.slice/featurebase.service
             └─470112 /usr/local/bin/featurebase server -c /etc/featurebase.conf

Oct 08 13:29:38 user systemd[1]: Started "Service for FeatureBase".
```
The key here is ```Active: active (running)....``` If you see something else, the following command is a good place to start troubleshooting.
```
journalctl -u featurebase -r
```

>**Note:** if you get a ```(code=exited, status=203/EXEC)``` error, you likely grabbed the wrong executable (e.g. you're working on an arm64 processor but grabbed the binary compiled for x86_64/amd64 processor)

If you do see ```Active: active (running)...``` then you can try to stop, start, and restart FeatureBase.

```
# stop FeatureBase services
sudo systemctl stop featurebase
# verify stop
sudo systemctl status featurebase
# start FeatureBase services
sudo systemctl start featurebase
# verify start
sudo systemctl status featurebase
# restart FeatureBase
sudo systemctl restart featurebase
# verify restart
sudo systemctl status featurebase
```


# Restore 1B records of Demo Data from S3
In order to use FeatureBase, you’ll need data! In a real-life situation, the FeatureBase team will provide guided onboarding and data modeling for our organization’s data. In this exercise, we’ll be working with curated demo data to showcase the low-latency capabilities of FeatureBase. Instructions to load the demo data are laid out below.

First, download the demo dataset from S3 using by clicking [this link](https://se-public-datasets.s3.us-east-2.amazonaws.com/cseg0_backup.tar.gz)

>**Please note that this file is large (~14GB) and contains over 1B records. Make sure that you have sufficient local storage. On average, it takes about 30 minutes to download, but actual download time may depend on your connection speed.**


>**To use your own data - check out our documentation for creating new sources [here](/reference/data-ingestion/ingester-configuration)

Next, in a new terminal window, make a directory for the data: 
```
mkdir ~/Cseg0_backup
```

And unzip it into the directory: 
```
tar -zxvf ~/Downloads/cseg0_backup.tar.gz -C ~/Cseg0_backup
```

Now, restore the data into FeatureBase: 
```
featurebase restore --host localhost:10101 -s ~/Cseg0_backup/
```

Once it's completed successfully, you'll see this message: 

```
... INFO:  http: Server closed
```

Now, you can run queries in the [FeatureBase web application](http://localhost:10101/)

You can monitor health of the FeatureBase cluster and other activity on the homepage.
![Cluster Health](https://user-images.githubusercontent.com/97700520/170797631-d80cebff-ddb1-4ee3-a56b-e8b6e94d453b.png)


## Data Exploration of Customer Segmentation Feature Table 

It’s always a good idea to understand what the dataset you’re working with contains before you get started. To do this, click on the ‘Tables’ section in the application to display the names of the tables in your deployment.

![Figure 1  Tables](https://user-images.githubusercontent.com/97700520/170796333-d1dec693-83c0-4070-a5f6-d5d4fff409e4.png)


Click on a table to show its contents. FeatureBase can ingest and represent a wide range of field types. One that may not be familiar is the **SET** field. **SET** fields are multi-valued and allow FeatureBase to collapse traditional data models, like the star schema, by efficiently storing multiple values for a single field.

![Figure 2  Customer segmentation (cseg) table](https://user-images.githubusercontent.com/97700520/170796463-04f080ec-3e50-413e-824f-00c619f014fc.png)

To understand the shape of the data contained in the customer dataset that was preloaded into this environment. First, navigate to the Query page by clicking “Query” on the left navigation bar. 

Let’s start by running a simple SQL statement to extract 10 records to explore.

```sql
SELECT * FROM cseg LIMIT 10;
```

Viewing this tabular output we can see each record contains several fields (attributes) and data types. Scroll left and right in the application to explore the full list of fields. For example, **names** and **cities** are captured in **STRING** fields. Income is captured in an **INT** field that will allow for range queries. You can also see that “education” is a SET field with multiple values in a single field.

![Figure 3  Select 10 items from table](https://user-images.githubusercontent.com/97700520/170796596-130f1cd8-9ad2-4080-a75a-19d14fcebe61.png)

Next, let’s check the full scale of this dataset by using another familiar SQL statement, the **COUNT**.

```sql
SELECT COUNT(*) FROM cseg;
```

This query will return the **COUNT** of records in the entire table and demonstrates we are working with a dataset of 1 billion records. Each record in the cseg table has 16 attributes.

![Figure 4  Select count from table](https://user-images.githubusercontent.com/97700520/170796676-19a466fb-5e1b-4d03-b5ad-a8e80fd3e2ff.png)

### Performing Large Aggregations

Aggregation workflows often require the ability to **SUM** large amounts of individual **INT** elements. This could be transaction amounts such as dollars (decimals), whole integers (counts, bandwidth), or any variation requiring a **SUM** across many records. In this example, we will **SUM** the income field across all 1 billion records.

```sql
SELECT SUM(income) FROM cseg;
```

![Figure 5  Select sum income from table](https://user-images.githubusercontent.com/97700520/170796734-8ac2e3d4-4674-494a-84e2-6d8f9439f345.png)

It is unlikely to need to SUM in this manner across all records. It is much more common to introduce complex conditions to SUM a segment of records that meets specified criteria.

Here we introduce comparative and logical operators including **GREATER THAN**, **AND**, and **OR**. 

```sql
SELECT SUM(income) 
FROM cseg 
WHERE income > 5000 AND age = 45 AND (skills='Ms Office' OR skills='Excel');
```

As you can see, the latency is in the sub-second time frame even when using complex searching criteria through 1 billion records.

![Figure 6 Complex SUM](https://user-images.githubusercontent.com/97700520/172648422-2d20bd75-1805-4f99-822d-6825e90075d1.png)


>**NOTE:**

>When aggregating over a SET field, values for a record will be included in multiple groups if not excluded in the query. For example, when SUM(income) is used with a GROUP BY of “education”, income for a record with both ‘Bachelor’s degree’ and ‘High school diploma or GED’ will be included in both groups.

>It is common for a single person to have multiple values for a field that may seem contradictory or redundant, like “education”. This may be due to differences in status over time as data are collected and aggregated. A person may be categorized as having “education” status of “Some college” and later be categorized as having a “Bachelor’s degree”. When those two data sources are matched up, the person may have multiple values associated with them.

Additionally, aggregations may include the AVERAGE argument.

```sql
SELECT AVG(income) FROM cseg;
```
![Figure 7 average income](https://user-images.githubusercontent.com/97700520/170796927-e7fc7f66-258d-49d2-a47f-a192d237ea9d.png)

>Note that we don’t currently support full SQL, but are working toward expanding SQL functionality. For example, the AVERAGE function is not currently supported in GROUP BY queries and will be added soon.

>**If you have issues with your queries, please contact a [FeatureBase Representative](mailto:se@featurebase.com). FeatureBase has a native language, called PQL, and we can help you translate your SQL queries to get the desired results.**

### INNER JOINs at Scale

FeatureBase can merge at ingest and eliminate preprocessing in cases where performant **INNER JOIN**s are required. Data from two separate tables or sources can be merged into a single normalized table by matching on a unique key in each dataset. Since FeatureBase can execute queries very quickly, workflows requiring **INNER JOIN**s can be simplified with FeatureBase by merging disparate datasets at ingest. In the following example, we are combining many of the queries in this guide and adding the **INNER JOIN**. 

The **INNER JOIN** is facilitating a **COUNT** of records, or people, are “available for hire” as indicated by  that have a string field true for “available_for_hire” located in the skills table, and have the string field true for “Teaching”. In other words, we would like to count the number of people who are teachers and also available for hire. The latency on this type of **INNER JOIN** at the billion records scale is still sub-second allowing for several interesting data models.

```sql
SELECT count(*) AS count 
FROM cseg AS t1 
INNER JOIN skills AS t2 ON t1._id = t2.id 
WHERE t2.bools = 'available_for_hire' and t1.hobbies = 'Teaching';
```

>**NOTE:** Included in the demo dataset is a table known as skills, please use the discovery queries to take a look at it!
![Figure 8  Inner Join Query](https://user-images.githubusercontent.com/97700520/170796998-7ce559da-58db-44c5-aa9b-a1a8c0b47c2b.png)



### TopK - A FeatureBase Superpower

Ranking queries are notorious for being computationally intensive - aka slow. Some solutions will use statistics to speed up a ranking query by approximating the true results, but that’s not always a desirable option. In addition to SQL, FeatureBase has a native language called [PQL](/reference/data-querying-ref/pql/introduction). In PQL, [```TopK```](/reference/data-querying-ref/pql/read/topk) queries can be run to return exact results in milliseconds. 

This query returns the top five hobbies across all customers from the cseg table, sifting through a billion records.

```
[cseg]TopK(hobbies, k=5);
```
![Figure 9  Top K Query](https://user-images.githubusercontent.com/97700520/170797209-70c365ab-82f6-4930-828f-4ceade77dcdd.png)


More complex, the next query returns the top ten hobbies among females who also like scuba diving from the cseg table in milliseconds. Even when adding complex filtering, the **TopK** queries can be run for exact results at scale without impacting query latency.

```
[cseg]TopK(hobbies, k=10, filter=Intersect(Row(sex=Female),Row(hobbies='Scuba Diving')));
```

![Figure 10 Top K Query with Filtering](https://user-images.githubusercontent.com/97700520/170797384-ea5b9573-3e2d-43ac-ab21-47c323f02418.png)

### Grouping with Complex Conditions and Aggregating

Another query commonly seen in aggregation-related use cases is the ```GROUP BY```. For example, let’s group by the hobbies counting only those with ultimate ```COUNT``` above 200,000,000. We'll execute this query in [PQL](/reference/data-querying-ref/pql/introduction).

```
[cseg]GroupBy(
Rows(hobbies),
sort="count desc",
having=CONDITION(count > 200000000)
);
```
![Figure 11. GROUP BY Query](/img/quick-start-guide/enterprise/ent_cseg_groupby_having.png)


Another useful facet of ```GROUP BY``` is the ability to add an aggregate argument and utilize the low-latency aggregation in another capacity. We'll execute this query in SQL.

```sql
SELECT education, SUM(income) 
FROM cseg 
WHERE age=18 
GROUP BY education; 
```

![Figure 12  Group by Query Filtered](https://user-images.githubusercontent.com/97700520/170797146-1ccdd6b5-82e6-4f5a-b8c2-f6b47d3e5897.png)


>**NOTE:** At this point, we encourage you to mix and match segmentation criteria to experience low-latency queries even as complex conditions are added. You can use the Query Builder to help construct queries in PQL.

![Query builder](https://user-images.githubusercontent.com/97700520/170797492-89ace99d-6de5-4a6f-ba14-275f53462fb2.png)



## What’s Next?

We hope that this hands-on experience has further demonstrated the power of FeatureBase to power real-time analytics workflows at scale. While this example focused on a customer segmentation use case, the same type of workflows are often used in anomaly detection or business process optimization use cases and continues to perform as workloads grow to trillions of records. Additionally, FeatureBase excels at combining streaming and historical data in real-time, allowing you to analyze data as soon at is available in FeatureBase with no need for time-consuming preprocessing or preaggregation. From here, partner with your FeatureBase representative to better understand how FeatureBase will work for your organization’s specific needs.

## Queries

### Data Exploration 

```sql
SELECT * FROM cseg LIMIT 10;
```

```sql
SELECT COUNT(*) FROM cseg;
```

### Complex Segmentation 

```sql
SELECT count(*) FROM cseg WHERE age = 45 AND income>50000 AND (skills='Ms Office' OR skills='Excel');
```

### Aggregations

```sql
SELECT SUM(income) FROM cseg;
```

```sql
SELECT SUM(income) FROM cseg where income > 5000;
```

```sql
SELECT AVG(income) FROM cseg;
```

### JOINS

```sql
SELECT count(*) AS count 
FROM cseg AS t1 
INNER JOIN skills AS t2 ON t1._id = t2.id 
WHERE t2.bools = 'available_for_hire' AND t1.hobbies = 'Teaching';
```

### Grouping with Complex Conditions

```
[cseg]GroupBy(
Rows(hobbies),
sort="count desc",
having=CONDITION(count > 200000000)
);
```

### Top K 

```
[cseg]TopK(hobbies, k=5);
```

```
[cseg]TopK(hobbies, k=10, filter=Intersect(Row(sex=Female),Row(hobbies='Scuba Diving')));
```

