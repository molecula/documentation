---
title: Cloud Quick Start Guide
---

## Welcome to FeatureBase!

Follow the guide outlined below for a hands-on demonstration of low-latency queries at scale using our FeatureBase Cloud platform. As you work through the guide, please note any questions or feedback that you may have for the FeatureBase team. We’re always looking for ways to improve the experience!

In this demonstration you will:

1. Create a new FeatureBase database
2. Pre-load two large-scale demo datasets into the database
3. Run a set of analytics queries

If you run into any roadblocks or have questions throughout the demonstration, please reach out to [se@featurebase.com](mailto:se@featurebase.com).

## Sign-Up Overview


First, sign up for your [Free Trial](https://www.featurebase.com/cloud). Click the ```Start Cloud Trial``` button to navigate to the FeatureBase Cloud application and set up your account. You will be asked to enter your First Name, Last Name, Email address, and password. You will also be asked to read and agree to the [FeatureBase Terms of Service](https://www.featurebase.com/cloud-terms/).  

![Figure 1. Create an account and set your password](/img/quick-start-guide/cloud/account_signup.png)


Next, you'll be asked to verify your account using the code sent to the email address you used to create your account.

![Figure 2. Verify your account](/img/quick-start-guide/cloud/verification_email.png)



### Trial Accounts

{% include /cloud/trial-account-limits.md %}

If you encounter any problems during this process or would like to reactivate your account, contact [se@featurebase.com](mailto:se@featurebase.com).

Navigate back to FeatureBase using [cloud.featurebase.com](https://cloud.featurebase.com/)

![Figure 3. Sign In](/img/quick-start-guide/cloud/sign_in.png)


When you sign in, you'll be directed to the Home screen where you have options to complete a variety of actions using the navigation pane on the left side of the screen.

![Figure 4. FeatureBase Home Screen](/img/quick-start-guide/cloud/home_page.png)


## Configuring your environment

In order to use our application, you’ll need data. In a real-life situation, the FeatureBase team will provide guided onboarding and data modeling for our organization’s data. In this exercise, we’ll be working with curated demo data to showcase the low-latency capabilities of FeatureBase. Navigate to the ```Databases``` screen, click "New Database", and select ```Start with pre-loaded sample data``` to create a database pre-loaded with the demo data. You may need enter a Database name if this isn't your first Database.

>This is a great time to grab a cup of coffee or reply to all those waiting Slack messages! A new database is spinning up and over 1B records are loading.

![Figure 5. Configure a Quick Start Database that is pre-loaded with demo data](/img/quick-start-guide/cloud/create_cseg_db.png)


While the database is spinning up, you will see updates to "Status" on the ```Databases``` section as the creation progresses. The database will have a status of ```CREATING``` followed by ```PROVISIONING``` while the process is starting and resources are provisioned. The database will then shift to ```RESTORING```, which indicates that data is being loaded into your database. 

![Figure 6. New Database: PROVISIONING](/img/quick-start-guide/cloud/db_creating.png)


![Figure 7. New Database: Running](/img/quick-start-guide/cloud/db_running.png)


After about 10 minutes, the database status will progress to ```RUNNING```, and you can click on the database name and check the ```Tables``` tab to see the two tables that have been created in the database. One table is called ```cseg```, short for customer segmentation, and the other is called ```skills```. In the next section, we will perform a variety of common analytical queries on both datasets.

![Figure 8. Demo Data restored into tables from backup](/img/quick-start-guide/cloud/tables_page_with_cseg.png)


### Data Exploration of Customer Segmentation Feature Table

It’s always a good idea to understand what the dataset you’re working with contains before you get started. To do this, click on the ```Databases``` section in the application, click the database you just created, and click the ```Tables``` tab  to display the names of the tables in your database.

Click on a table to show its contents. FeatureBase can ingest and represent a wide range of data types. Two that may not be familiar are the ```IDSET``` and ```STRINGSET``` types. ```SET``` types are multi-valued and allow FeatureBase to collapse traditional data models, like the star schema, by efficiently storing multiple values for a single column.

![Figure 9. Customer Segmentation (cseg) table details](/img/quick-start-guide/cloud/cseg_cols.png)


To understand the shape of the data contained in the customer dataset that was preloaded into this environment. First, navigate to the Query page by clicking ```Query``` on the left navigation bar. 

Let’s start by running a simple SQL statement to extract 10 records to explore.

```sql
SELECT TOP(10) * FROM cseg;
```

Viewing this tabular output we can see each record contains several columns (attributes) and data types. Scroll left and right in the application to explore the full list of columns. For example, ```names``` and ```cities``` are captured in ```STRINGSET``` columns. ```income``` is captured in an ```INT``` column that will allow for range queries. You can also see that ```education``` is a ```STRINGSET``` column with multiple values in a single column.

![Figure 10. Select top ten items from table](/img/quick-start-guide/cloud/query_select_cseg_limit10.png)

Next, let’s check the full scale of this dataset by using another familiar SQL statement, the ```COUNT``` to return how many records are in the table.

```sql
SELECT COUNT(*) FROM cseg;
```

This query will return the ```COUNT``` of records in the entire table and demonstrates we are working with a dataset of 1 billion records. Each record in the cseg table has 16 attributes.

![Figure 11. Count all records in table](/img/quick-start-guide/cloud/query_count_cseg_all.png)

### Performing Large Aggregations

Aggregation workflows often require the ability to ```SUM``` large amounts of individual ```INT``` or ```DECIMAL``` elements. This could be transaction amounts such as dollars (decimals), whole integers (counts, bandwidth), or any variation requiring a ```SUM``` across many records. In this example, we will ```SUM``` the ```income``` column across all 1 billion records.

```sql
SELECT SUM(income) FROM cseg;
```

![Figure 12. SUM Query](/img/quick-start-guide/cloud/query_sum_income.png)


It is unlikely to need to ```SUM``` in this manner across all records. It is much more common to introduce complex conditions to ```SUM``` a segment of records that meets specified criteria.

Here we introduce comparative and logical operators including ```GREATER THAN```, ```AND```, and ```OR```. 

```sql
SELECT SUM(income) FROM cseg 
WHERE income > 5000 AND age = 45 AND (SETCONTAINSANY(skills,['Ms Office','Excel']));
```

As you can see, the latency is in the sub-second time frame even when using complex searching criteria through 1 billion records.

![Figure 13. Complex SUM Query](/img/quick-start-guide/cloud/query_sum_income_filters.png)

>NOTE: When aggregating over a SET column, values for a record will be included in multiple groups if not excluded in the query. For example, when SUM(income) is used with a GROUP BY of “education”, income for a record with both ‘Bachelor’s degree’ and ‘High school diploma or GED’ will be included in both groups.

>It is common for a single person to have multiple values for a column that may seem contradictory or redundant, like “education”. This may be due to differences in status over time as data are collected and aggregated. A person may be categorized as having “education” status of “Some college” and later be categorized as having a “Bachelor’s degree”. When those two data sources are matched up, the person may have multiple values associated with them.

Additionally, aggregations may include the ```AVERAGE``` argument.

```sql
SELECT AVG(income) FROM cseg;
```

>Note that we don’t currently support full SQL, but are working toward expanding SQL functionality.

![Figure 14. AVERAGE Query](/img/quick-start-guide/cloud/query_avg_income.png)


### INNER JOINs at Scale

<!--
This needs to be updated back to INNER JOIN and SQL once SQL3 JOIN functionality is stable
-->
FeatureBase can merge at ingest and eliminate preprocessing in cases where performant **INNER JOIN**s are required. Data from two separate tables or sources can be merged into a single normalized table by matching on a unique key in each dataset. Since FeatureBase can execute queries very quickly, workflows requiring ```INNER JOIN```s can be simplified with FeatureBase by merging disparate datasets at ingest. In the following example, we are combining many of the queries in this guide and adding the ```INNER JOIN``` functionality using the `DISTINCT` function in FeatureBase's native language called [PQL](/pql-guide/pql-introduction).

The ```INNER JOIN``` is facilitating a ```COUNT``` of records, or people, that are ```available for hire``` as indicated by having a ```STRING``` column true for ```available_for_hire``` located in the skills table, and having a ```STRING``` column true for ```Teaching```. In other words, we would like to ```COUNT``` the number of people who are teachers and also available for hire. The latency on this type of ```INNER JOIN``` at the billion records scale is still sub-second allowing for several interesting data models.

```sql
[cseg]Count(Intersect(
Row(hobbies="Teaching"),
Distinct(Row(bools='available_for_hire'), field= id, index=skills)))
```
![Figure 15. INNER JOIN Query](/img/quick-start-guide/cloud/query_join.png)


>NOTE: Included in the stock dataset is a table known as skills, please use the discovery queries to take a look!



### TopK - A FeatureBase Superpower

Ranking queries are notorious for being computationally intensive - aka slow. Some solutions will use statistics to speed up a ranking query by approximating the true results, but that’s not always a desirable option. In PQL, [```TopK```](/pql-guide/read/topk) queries can be run to return exact results in milliseconds. 

This query returns the top five hobbies across all customers from the cseg table, sifting through a billion records in milliseconds.

```
[cseg]TopK(hobbies, k=5)
```
![Figure 16. TOP K Query](/img/quick-start-guide/cloud/query_topk.png)


More complex, the next query returns the top ten hobbies among females who also like scuba diving from the ```cseg``` table in milliseconds. Even when adding complex filtering, the ```TopK``` queries can be run for exact results at scale without impacting query latency.

```
[cseg]TopK(hobbies, k=10, filter=Intersect(Row(sex=Female),Row(hobbies='Scuba Diving')))
```

![Figure 17. TOP K Query with Filters](/img/quick-start-guide/cloud/query_topk_filter.png)

### Grouping with Complex Conditions and Aggregating

Another query commonly seen in aggregation-related use cases is the ```GROUP BY```. For example, let’s group by the hobbies counting only those with ultimate ```COUNT``` above 200,000,000.

```sql
SELECT  hobbies, COUNT(*) as cnt
FROM cseg
GROUP BY hobbies
HAVING COUNT(*) > 200000000
ORDER BY cnt DESC;
```
![Figure 18. GROUP BY Query](/img/quick-start-guide/cloud/cseg_groupby_having.png)



Another useful facet of ```GROUP BY``` is the ability to add an aggregate argument and utilize the low-latency aggregation in another capacity.

```sql
SELECT education, SUM(income)
FROM cseg
WHERE age=18
GROUP BY education;
```
![Figure 19. GROUP BY Query with Filters](/img/quick-start-guide/cloud/cseg_groupby_filter.png)


>NOTE: At this point, we encourage you to mix and match segmentation criteria to experience low-latency queries even as complex conditions are added.

If you have issues with your queries, please contact your FeatureBase representative or email [se@featurebase.com](mailto:se@featurebase.com) to translate your SQL queries to get the desired results

## What’s Next?

We hope that this hands-on experience has further demonstrated the power of FeatureBase to power real-time analytics workflows at scale. While this example focused on a customer segmentation use case, the same type of workflows are often used in anomaly detection or business process optimization use cases and continues to perform as workloads grow to trillions of records. Additionally, FeatureBase excels at combining streaming and historical data in real-time, allowing you to analyze data as soon at is available in FeatureBase with no need for time-consuming preprocessing or preaggregation. From here, partner with your FeatureBase representative to better understand how FeatureBase will work for your organization’s specific needs. If you'd like to continue exploring, you can start learning how to:

* [INGEST DATA OVERVIEW](/cloud/cloud-data-ingestion/ingest-data-overview)
{% include /sql-preview/sql-insert-examples.md %}

## Queries

### Data Exploration 

```sql
SELECT TOP(10) * FROM cseg;
```

```sql
SELECT COUNT(*) FROM cseg;
```

### Complex Segmentation 

```sql
SELECT SUM(income) FROM cseg 
WHERE income > 5000 AND age = 45 AND (SETCONTAINSANY(skills,['Ms Office','Excel']));
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

```
[cseg]Count(Intersect(
Row(hobbies="Teaching"),
Distinct(Row(bools='available_for_hire'), field= id, index=skills)))
```

### Grouping with Complex Conditions

```sql
SELECT  hobbies, COUNT(*) as cnt
FROM cseg
GROUP BY hobbies
HAVING COUNT(*) > 200000000
ORDER BY cnt DESC;
```

```sql
SELECT education, SUM(income)
FROM cseg
WHERE age=18
GROUP BY education;
```

### Top K 

```
[cseg]TopK(hobbies, k=5)
```

```
[cseg]TopK(hobbies, k=10, filter=Intersect(Row(sex=Female),Row(hobbies='Scuba Diving')))
```

## Spinning Down Your Resources

When you have completed this guide, please take a few minutes to drop your tables and spin down your database. If you do not, it will continue to create charges on your account.

You can delete the database directly in the ```Databases``` section, which will drop all of the tables within it. Click the three dots and select ```Delete```. 

![Figure 20. Delete Database](/img/quick-start-guide/cloud/delete_database.png)

Confirm dropping the database by typing ```DELETE``` into the interface. It takes a minute or two to delete a database.

![Figure 21. Confirm Delete Database](/img/quick-start-guide/cloud/delete_database_confirm.png)

Alternatively, you can drop individual tables in the ```Databases``` section within a database in the ```Tables``` tab. This follows a similar process to dropping a database. Table deletion time is a function of the amount of data being deleted.

![Figure 22. Delete Table](/img/quick-start-guide/cloud/delete_table.png)

![Figure 23. Confirm Delete Table](/img/quick-start-guide/cloud/delete_table_confirm.png)