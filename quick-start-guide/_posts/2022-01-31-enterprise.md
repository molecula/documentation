---
title: Enterprise Quick Start Guide
---

## Welcome to FeatureBase!

Follow the guide outlined below for a hands-on demonstration of low-latency queries at scale using our FeatureBase SaaS platform. As you work through the guide, please note any questions or feedback that you may have for the Molecula team. We’re always looking for ways to improve the experience!

In this demonstration you will:

1. Download a single-node FeatureBase binary
2. Configure FeatureBase
3. Restore two large-scale datasets into the deployment
4. Run a set of analytics queries

>If you run into any roadblocks or have questions throughout the demonstration, please reach out to your Molecula Representative or email SE@molecula.com.

## Download Single-Node FeatureBase Binary
Sign up on the Molecula website by entering your First Name, Last Name, Business Email, and Company Name. Next, click ```Start Free``` to navigate to the downloads page where you can choose to download a tarball with a single-node FeatureBase binary onto a single, local machine. 

>Please note that by clicking ```Start Free``` you agree to the [Terms of Service](https://www.molecula.com/) and to receive occasional marketing emails from Molecula. You also understand that we will process your personal information in accordance with our [Privacy Policy](https://www.molecula.com/privacy/).


Click ```Download``` on the option that best meets your needs to download the tarball containing the latest single-node FeatureBase binary.
 

## Configuring FeatureBase - MacOS

>Note: The FeatureBase executable are built for x86_64 and ARM64 CPU architectures. If you aren't running macOS, there are two other options. You can install and run FeatureBase on Linux or a Docker container. 


Next, extract the ```.tar.gz file``` and copy the featurebase binary to your ```/usr/local/bin folder```.
  
```
tar -zxvf molecula-v4.7.1.tar.gz
sudo cp -r molecula-v4.7.1/featurebase/featurebase_darwin_amd64 /usr/local/bin/featurebase
```
>Note: The copy or cp command above moves the ```amd64/x86_64 featurebase``` binary to ```/usr/local/bin/```. 
Ensure this folder is in your path variable by, running ```echo $PATH``` in the command line and confirming ```/usr/local/bin/``` is there. 
If it's not, run ```export PATH=$PATH:/usr/local/bin``` to append it to your path variable.
  
## Configuring FeatureBase - Linux

>The tutorial below goes over the installation steps required to run the FeatureBase server on a single Linux machine using ```systemd```. 

>If you aren't running Linux, there are two other options. You can install and run FeatureBase on macOS or a Docker container. Note that FeatureBase executable is built for x86_64 and ARM64 CPU architectures.

After you download FeatureBase, run the code below to ensure it is executable and move it to ```/usr/local/bin```.

>Note: The copy or cp command above moves the ```featurebase``` binary to ```/usr/local/bin/```. Ensure this folder is in your path variable by, running echo ```$PATH``` in the command line and confirming ```/usr/local/bin/``` is there. If it's not, run ```export PATH=$PATH:/usr/local/bin``` to append it to your path variable.

Next, configure the FeatureBase server by creating and running the configuration file. 

```
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

### Configure the FeatureBase Service Unit

On Linux, we recommend running FeatureBase as a ```systemd``` service unit. To learn more about ```systemd``` and ```units```, go  [here](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files). To configure the FeatureBase service unit's function, we'll create a ```.service``` file.

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
   
The service file above tells ```systemd``` we want to run ```/usr/local/bin/featurebase server -c /etc/featurebase.conf``` as the molecula user. This starts a FeatureBase server and configures it based on ```/etc/featurebase.conf```. Additionally, in the event that process fails, it tells ```systemd``` to try and restart that process 30 seconds.

### Setup Log and Data Folders
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

To automatically start FeatureBase after a reboot, you can run:
```
sudo systemctl enable featurebase.service
```

Verify it started successfully and is running: 
```
sudo systemctl status featurebase
```

You should get a response that looks like this: 
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

The key here is ```Active: active (running)....``` If you see something else, the following command is a good place to start troubleshooting. Or reach out to SE@molecula.com for assistance. 
```
journalctl -u featurebase -r
```

## Restore 1B records of Demo Data from S3
In order to use FeatureBase, you’ll need data! In a real-life situation, the Molecula team will provide guided onboarding and data modeling for our organization’s data. In this exercise, we’ll be working with curated demo data to showcase the low-latency capabilities of FeatureBase. Instructions to load the demo data are laid out below.

### Restore Demo Dataset from S3:


>**This is a great time to grab a cup of coffee or reply to all those waiting Slack messages! Over 1B records are loading into FeatureBase.**


## Introduction to the Demo Dataset

In a real-world situation, a Molecula expert will work with your organization to appropriately model data for your use cases in FeatureBase. To give you an idea of the process, this tutorial will walk you through how to interact with complex data in FeatureBase using data from the Customer Segmentation (cseg) dataset.

### Data Exploration of Customer Segmentation Feature Table (NEED TO UPDATE FOR BINARY)

It’s always a good idea to understand what the dataset you’re working with contains before you get started. To do this, click on the ‘Tables’ section in the application to display the names of the tables in your deployment.

![Figure 8. List of Tables ](/img/quick-start-guide/enterprise/fig8.png "Figure 8. List of Tables")

Click on a table to show its contents. FeatureBase can ingest and represent a wide range of field types. One that may not be familiar is the **SET** field. **SET** fields are multi-valued and allow FeatureBase to collapse traditional data models, like the star schema, by efficiently storing multiple values for a single field.

![Figure 9. Customer segmentation (cseg) table](/img/quick-start-guide/enterprise/fig10.png "Figure 9. Customer segmentation (cseg) table")

To understand the shape of the data contained in the customer dataset that was preloaded into this environment. First, navigate to the Query page by clicking “Query” on the left navigation bar. 

Let’s start by running a simple SQL statement to extract 10 records to explore.

```sql
SELECT * FROM cseg LIMIT 10;
```

Viewing this tabular output we can see each record contains several fields (attributes) and data types. Scroll left and right in the application to explore the full list of fields. For example, **names** and **cities** are captured in **STRING** fields. Income is captured in an **INT** field that will allow for range queries. You can also see that “education” is a SET field with multiple values in a single field.

![Figure 10. Select 10 items from table](/img/quick-start-guide/enterprise/fig11.png "Figure 10. Select 10 items from table")

Next, let’s check the full scale of this dataset by using another familiar SQL statement, the **COUNT**.

```sql
SELECT COUNT(*) FROM cseg;
```

This query will return the **COUNT** of records in the entire table and demonstrates we are working with a dataset of 1 billion records. Each record in the cseg table has 16 attributes.

![Figure 11. Select count from table](/img/quick-start-guide/enterprise/fig12.png "Figure 11. Select count from table")

### Performing Large Aggregations

Aggregation workflows often require the ability to **SUM** large amounts of individual **INT** elements. This could be transaction amounts such as dollars (decimals), whole integers (counts, bandwidth), or any variation requiring a **SUM** across many records. In this example, we will **SUM** the income field across all 1 billion records.

```sql
SELECT SUM(income) FROM cseg;
```

![Figure 12. SUM query](/img/quick-start-guide/enterprise/fig13.png "Figure 12. SUM query")

It is unlikely to need to SUM in this manner across all records. It is much more common to introduce complex conditions to SUM a segment of records that meets specified criteria.

Here we introduce comparative and logical operators including **GREATER THAN**, **AND**, and **OR**. 

```sql
SELECT SUM(income) 
FROM cseg 
WHERE income > 5000 AND age = 45 AND skills='Ms Office' OR skills='Excel';
```

As you can see, the latency is in the sub-second time frame even when using complex searching criteria through 1 billion records.

![Figure 13. Complex sum query](/img/quick-start-guide/enterprise/fig14.png "Figure 13. Complex sum query")

**NOTE:**

When aggregating over a SET field, values for a record will be included in multiple groups if not excluded in the query. For example, when SUM(income) is used with a GROUP BY of “education”, income for a record with both ‘Bachelor’s degree’ and ‘High school diploma or GED’ will be included in both groups.

It is common for a single person to have multiple values for a field that may seem contradictory or redundant, like “education”. This may be due to differences in status over time as data are collected and aggregated. A person may be categorized as having “education” status of “Some college” and later be categorized as having a “Bachelor’s degree”. When those two data sources are matched up, the person may have multiple values associated with them.

Additionally, aggregations may include the AVERAGE argument.

```sql
SELECT AVG(income) FROM cseg;
```

![Figure 14. average query](/img/quick-start-guide/enterprise/fig15.png "Figure 14. average query")

### INNER JOINs at Scale

FeatureBase can merge at ingest and eliminate preprocessing in cases where performant **INNER JOIN**s are required. Data from two separate tables or sources can be merged into a single normalized table by matching on a unique key in each dataset. Since FeatureBase can execute queries very quickly, workflows requiring **INNER JOIN**s can be simplified with FeatureBase by merging disparate datasets at ingest. In the following example, we are combining many of the queries in this guide and adding the **INNER JOIN**. 

The **INNER JOIN** is facilitating a **COUNT** of records, or people, are “available for hire” as indicated by  that have a string field true for “available_for_hire” located in the skills table, and have the string field true for “Teaching”. In other words, we would like to count the number of people who are teachers and also available for hire. The latency on this type of **INNER JOIN** at the billion records scale is still sub-second allowing for several interesting data models.

```sql
SELECT count(*) AS count 
FROM cseg AS t1 
INNER JOIN skills AS t2 ON t1._id = t2.id 
WHERE t2.bools = 'available_for_hire' and t1.hobbies = 'Teaching';
```

**NOTE:** Included in the demo dataset is a table known as skills, please use the discovery queries to take a look at it!

![Figure 15. inner join query](/img/quick-start-guide/enterprise/fig16.png "Figure 15. inner join query")


### Grouping with Complex Conditions and Aggregating

Another query commonly seen in aggregation-related use cases is the **GROUP BY**. For example, let’s group by the hobbies counting only those with ultimate count above 200,000,000.

```sql
SELECT hobbies, COUNT(*) 
FROM cseg 
GROUP BY hobbies HAVING count > 200000000;
```

![Figure 16. group by query](/img/quick-start-guide/enterprise/fig17.png "Figure 16. group by query")

Another useful facet of **GROUP BY** is the ability to add an aggregate argument and utilize the low latency aggregation in another capacity.

```sql
SELECT education, SUM(income) 
FROM cseg 
WHERE age=18 
GROUP BY education; 
```

![Figure 17. group by query filterd](/img/quick-start-guide/enterprise/fig18.png "Figure 17. group by query filtered")

### TopK - A FeatureBase Superpower

Ranking queries are notorious for being computationally intensive - aka slow. Some solutions will use statistics to speed up a ranking query by approximating the true results, but that’s not always a desirable option. In addition to SQL, FeatureBase has a native language called PQL. In PQL, TopK queries can be run to return exact results in milliseconds. 

This query returns the top five hobbies across all customers from the cseg table, sifting through a billion records in 117.2ms.

```
[cseg]TopK(hobbies, k=5)
```

![Figure 18. Top K query](/img/quick-start-guide/enterprise/fig19.png "Figure 18. Top K query")

More complex, the next query returns the top ten hobbies among females who also like scuba diving from the cseg table in milliseconds. Even when adding complex filtering, the **TopK** queries can be run for exact results at scale without impacting query latency.

```
[cseg]TopK(hobbies, k=10, filter=Intersect(Row(sex=Female),Row(hobbies='Scuba Diving')))
```

![Figure 19. Top K query with filtering](/img/quick-start-guide/enterprise/fig20.png "Figure 19. Top K query with filtering")

**NOTE:** At this point, we encourage you to mix and match segmentation criteria to experience low-latency queries even as complex conditions are added.

Note that we don’t currently support full SQL, but are working toward expanding SQL functionality. For example, the AVERAGE function is not currently supported in GROUP BY queries and will be added soon.

If you have issues with your queries, please contact Molecula Representative. FeatureBase has a native language, called PQL, and we can help you translate your SQL queries to get the desired results.

## What’s Next?

We hope that this hands-on experience has further demonstrated the power of FeatureBase to power real-time analytics workflows at scale. While this example focused on a customer segmentation use case, the same type of workflows are often used in anomaly detection or business process optimization use cases and continues to perform as workloads grow to trillions of records. Additionally, FeatureBase excels at combining streaming and historical data in real-time, allowing you to analyze data as soon at is available in FeatureBase with no need for time-consuming preprocessing or preaggregation. From here, partner with your Molecula representative to better understand how FeatureBase will work for your organization’s specific needs.

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
SELECT count(*) FROM cseg WHERE age = 45 AND income>50000 AND skills='Ms Office' OR skills='Excel';
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

```sql
SELECT hobbies, count(*) 
FROM cseg 
GROUP BY hobbies 
HAVING count > 200000000;
```

### Top K 

```
[cseg]TopK(hobbies, k=5)
```

```
[cseg]TopK(hobbies, k=10, filter=Intersect(Row(sex=Female),Row(hobbies='Scuba Diving')))
```

