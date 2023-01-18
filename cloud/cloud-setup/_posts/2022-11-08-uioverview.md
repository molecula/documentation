---
id: uioverview
title: UI Overview & Navigation
sidebar_label: UI Overview & Navigation
---

The user interface is meant to make provisioning, loading, querying, and monitoring your databases easy. When you log in on [cloud.featurebase.com](https://cloud.featurebase.com){:target="_blank"}, you will see a navigation bar on the left hand side of the screen. This is used to navigate between the different areas of the UI. This navigation bar is persisted to allow for switching between key areas quickly. The main working area of the page will populate based on the area you select. Each of the main areas is detailed below.

## Databases
Clicking “Get Started” or “Databases" from the home page will direct you to the databases page where you can create a new database. Databases are clusters of FeatureBase nodes. All of your data will live in tables within a FeatureBase database. The tool offers various database shapes, so all you need to provide is a choice from these options and a database name. This is a unique name for your database that will be used throughout the tool to reference a particular database. You can have multiple databases, so it’s important to name these something meaningful to you and your organization.

Within a database, the “Tables” tab allows you to create new tables and inspect or modify the schema of existing tables. Clicking on a table will allow users to see table metadata like the database it lives in, columns and types, and more.

## Query
The “Query” section allows you to ingest and explore data using PQL and SQL statements. The text editor allows for multiple queries to exist in the same pane. Individual queries are separated by newlines with only whitespace. You should first pick a database to query against in the top right corner. This will default to the oldest database created. Queries have an automatic limit of 100 records applied but can be adjusted up to a 10k maximum. This is to prevent impact to production databases resulting from accidentally trying to bring back too much data. The query page also allows you to browse tables and schemas, as well as see your historical queries.

## Configuration
The “Configuration” section allows you to manage general settings and your organization as a whole. “Manage Users” allows you to view users, invite new users, and deactivate/reactivate users in you organization. “Organization Settings” allows you to view and update relevant information about your organization, such as the billing or technical contacts listed for your organization.

## Get Help
The "Get Help" section contains helpful links on where to learn more and who to contact. Please reach out with any questions, feedback, or if you are trying to buy. We'd love to hear from you!