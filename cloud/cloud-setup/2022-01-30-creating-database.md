---
title: Creating a Database
---


 **⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes.


In the user interface, clicking "Databases" from the left hand navigation bar will direct you to the databases page. You can create a database by clicking “New Database". You will have the option to load sample data or start with an empty database. The tool has [sizes](/cloud/cloud-data-modeling/databases-overview#sizes) based on memory, so all you need to provide is a database memory (unless you load sample data) from a drop down and a database name. Note the UI will only display the choices your organization has access to, which is determined when you purchase the product. These choices can be queried for programmatically as well and are referred to as “database shapes” in the API:


**HTTP API Reference:**
```shell
curl --location --request GET 'https://api.featurebase.com/v2/service-properties/database:shapes' \
--header 'Authorization: Bearer <IdToken>'
```

The database name can only contain lowercase alphanumeric characters, dashes (-), and underscores (_) but must start with an alphabetic character. You can have multiple databases, so it’s important to name these something meaningful to you and your organization. For example, if you have a customer segmentation database and know you’ll have a full staging environment, you might want to name your production database as cust_seg_production and your staging database as cust_seg_staging. Clicking “Start” will start creating your database. This can also be accomplished programmatically:

**HTTP API Reference:**
```shell
curl --location --request POST 'https://api.featurebase.com/v2/databases' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '--data-raw '{
    "name": "<database_name>",
    "database_options":{
        "shape": "<memory_choice>"
    }
}'
```

After clicking "Create Database", you will see a new entry populate in the Database page with the name you provided. You will also see a status of “CREATING”. This is the state shown as the underlying hardware is provisioned. After a minute or two, the status will update to “RUNNING”, which indicates your database is ready to use. The other states you might encounter can be seen [here](/cloud/cloud-data-modeling/databases-overview#states). All of your databases' statuses can also be queried programmatically.

**HTTP API Reference:**
```shell
curl --location --request GET 'https://api.featurebase.com/v2/databases' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json'
```

Once your database is in the “RUNNING” state, you are free to start creating tables and ingesting data.

## Next step

* [Learn how to create tables](/cloud/cloud-data-ingestion/tables)
