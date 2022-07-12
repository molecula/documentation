---
title: Grafana Connector
---

Molecula provides a Grafana plugin, which can be used to interact with FeatureBase (4.0 or higher <!-- TODO is this correct? -->) to run queries and view visualizations of results. Note that this is unrelated to using Grafana for operational monitoring of the FeatureBase cluster. For details on that, see the [monitoring reference page](/reference/operations/enterprise/monitoring)

## Setup

### Install Grafana
For the best experience, [install](https://grafana.com/grafana/download) Grafana version 7 using the binary, not brew. The plugin requires version 7 or greater, but version 7 works best. For convenience, here are the commands for mac. For other platforms, check the link.

```
curl -O https://dl.grafana.com/enterprise/release/grafana-enterprise-7.5.13.darwin-amd64.tar.gz
tar -zxvf grafana-enterprise-7.5.13.darwin-amd64.tar.gz
```

### Install Plugin
As of FeatureBase 4.3, a Grafana plugin archive should be included in your release archive. Unpack and note the location of the `/dist` folder.


In Grafana's configuration file `grafana-7-x.x/conf/defaults.ini` point the `plugins` field to the `/dist` folder.

```
plugins = /path/to/grafana-plugin/molecula/dist
```

Uncomment and add the plugin id to `allow_loading_unsigned_plugins`:

```
allow_loading_unsigned_plugins = molecula-datasource
```

The port which defaults to `3000` can be modified by setting the `http_port` field if necessary.

### Launch Grafana

From `grafana-7-x.x/` run the following command:

```
./bin/grafana-server web
```

- Direct your browser to Grafana which should be running on localhost:3000 by default.

### Add Datasource

- Sign in or create credentials (you can use admin/admin if logging in for the first time)
- Add Molecula as a datasource in Grafana and enter FeatureBase server information
    - The welcome page should include a link to the [Add data source page](http://localhost:3000/datasources).
      - See the [Grafana docs](https://grafana.com/docs/grafana/latest/datasources/add-a-data-source) for more details.
    - If your molecula-datasource plugin is installed, it should appear in the data source list.


![Grafana Welcome](/img/grafana-welcome.png "Grafana Welcome")  
*Click "Add your first data source"*

![Grafana Add Datasource](/img/grafana-add-datasource.png "Grafana Add Datasource")  
*Select the "Molecula" option. The "unsigned" label is expected*

### Configure Server

Point Grafana to a running FeatureBase server
- Default FeatureBase address: `localhost`
- Default FeatureBase GRPC port: `20101`
- `Max Query Results` limits the number of records returned by the server if no `Limit` call is provided.
  
![Grafana Configure Datasource](/img/grafana-configure-server.png "Grafana Configure Datasource")  
*If Featurebase server is running, you will see a similar message indicating success*

### Configure Authentication
If FeatureBase server has authentication enabled, select Auth Enabled Server in the Grafana configuration page for the FeatureBase data source. Three new fields will be displayed: `Email`, `Password`, and `Server CA Cert` .
- `Email`: the email for the user account associated with the configured IDP.
- `Password`: the password for the user account associated with the configured IDP.
- `Server CA Cert`: the contents of the certificate used for TLS on the FeatureBase server

![Grafana Configure Authentication](/img/grafana-configure-auth.png "Grafana Configure Authentication")  
*These are secure fields. Contents will be hidden once saved and will require resetting to change the value*

### Other Installation Methods


#### To install Grafana using Docker:

Run the Grafana Docker image with this command:

```
docker run -d  \
    -p 3000:3000 \   # app http port
    -p 20101:20101 \ # FeatureBase grpc port
    -v "$(pwd)":/var/lib/grafana/plugins \   # plugin directory volume mount
    --name=grafana \
    -e "GF_PLUGINS_ALLOW_LOADING_UNSIGNED_PLUGINS=molecula-datasource" \   # grafana configuration environment variable
    grafana/grafana:7.5.9
```

After any changes to the plugin directory, restart the container with `docker restart grafana`.

Configure the datasource using `host.docker.internal` for the server and `20101` the grpc port

#### Other methods:
If your environment requires a different installation method, please refer to the [Grafana documentation](https://grafana.com/docs/grafana/latest/installation/).


## Creating Panels
<!-- TODO: need sample dataset -->
<!-- TODO: dataset-specific examples for each "format as" option -->
<!-- TODO: screenshots of config and results -->


### Querying
The plugin supports any [SQL](/reference/data-querying/sql) and [PQL](/data-querying/pql/introduction) queries that FeatureBase supports. When using PQL, the index must be selected from the respective drop down.

![Query FeatureBase through Grafana](/img/grafana-query.png "Query FeatureBase through Grafana")  
*Enter your SQL or PQL query*

#### Fetching Ids
By default, `_id` will be filtered out in query results. Use the 'Fetch _id' toggle if required. 

### Data Series (Format As)
Query results can be broken up in different ways to aid the creation of different types of visualizations.

#### Single Series
Typically used for a single data-series on a time based plot such as, the 'Graph' panel. This will require a TimestampField and a numeric field in the query results. 

Special Consideration:
- DateInt fields will be interpreted as the number of seconds from the Unix epoch if it is named 'timestamp'.

```pql
Extract(Limit(All(), limit=1000), Rows(data_size), Rows(timestamp))
```
#### Series By Row

Typically used for aggregation queries where each row is a distinct category with a statistic. 
```pql
GroupBy(Rows(city))
```
As single series, this would return the count of each distinct city in a single table. But as 'Series By Row', it will promote each row to be its own data series.

#### Series By Metric
Typically used when you want to break up the query results into different data-series by the distinct values in a particular column. The column itself must be included in the query and selected as the 'metric'. <!-- TODO what is "the 'metric'" ??? -->

```pql
Extract(Limit(All(), limit=1000), Rows(data_size), Rows(timestamp), Rows(customer))
```

If 'customer' contains the distinct values of 'CVS' and 'Sprint', the result will be two separate data series. 

### Use Grafana Variables

- You can insert [Grafana variables](https://grafana.com/docs/grafana/latest/variables/variable-types/add-query-variable/) in your query to serve as placeholders. The variable is prepended with a $: `$var_name`.

```pql
Extract(Limit(Row(customer=$customer), limit=1000), Rows(data_size), Rows(timestamp), Rows(customer))
```

- You can define the values this variable can take in Dashboard Settings > Variables > New.
- Name the variable to match what you used in the query
- For 'Type' select 'Custom' or 'Query'
    - If 'Custom', provide a comma separated list of values
    - If 'Query', select Molecula as the datasource and provide a SQL query, e.g. `SELECT DISTINCT level FROM logs`. PQL cannot be used here.
      - To use field *names* for variable values, use a query like (useful for `Rows` calls): 
        - `show fields from <index>`
      - To use field *values* for variable values, use a query like (useful for `Row` calls):
        -  `select distinct <field> from <index> limit <integer>`
- Under Selection Options, you can choose if you would like users to be able to select multiple (or all) values for the variable

![Grafana Variables Edit](/img/grafana-variables-edit.png "Grafana Variables Edit")  
*Define your variable by setting the Name, Type, Query (or Custom values), and whether you would like the variable to take multiple values*

At the top of the dashboard, you can now dynamically select a value with which to process your query.   
  
![Grafana Variable Select](/img/grafana-variable-select.png "Grafana Variable Select")  
*Select a value for your variable in the drop down on the dashboard*

### Variable Interpolation
Variables can be used in the following calls. Interpolation of the variable differs for each call and is demonstrated below: 
#### Row
- `$var1` has the values: ["Informational", "Debug"]. 
- User input: `Count(Row(level=$var1))`
- Interpolated query: `Count(Union(Row(level="Informational"), Row(level="Debug")))`
- Conceptually, this is an OR of all selected values
  
#### Rows
- `$var2` has the values: ["customer", "region"]. 
- User input: `GroupBy(Rows($var2))`
- Interpolated query: `GroupBy(Rows("customer"), Rows("region"))`

**NOTE:** 
Considering how multi-valued variables are interpolated in `Rows` calls, you will not want to use it standalone like this:
Rows($var) since you'll get:
Rows(value1), Rows(value2),...
which is not a valid query. Instead, you'll want to use it as a child of another call like GroupBy.

  
#### ConstRow
- `$var3` has the values: `[5,10,15]`
- User input:  `Intersect(ConstRow(columns=$var3), Row(region="NW"))`
- Interpolated query: `Intersect(ConstRow(columns=[5,10,15]), Row(region="NW"))`
  
### Time Range Controls

Grafana has time range controls at the top of each graph and dashboard. 

![Grafana Variable Select](/img/grafana-time-range-control.png "Grafana Variable Select")  
*Grafana time range selector*

To utilize these controls, you must associate it with a field in your dataset. This can be done by adding the field name to `TimeField` in the query editor. The type of this field must be `timestamp`. 

![Grafana Variable Select](/img/grafana-timefield.png "Grafana Variable Select")  
*Select the field you would like to associate with Grafana's time range controls*
