---
title: BULK INSERT
---

| | |
|-|-|
| **ℹ️NOTE** | This page contains information that only applies to SQL Preview functionality (more information [here](/sql-preview/sql-preview)). Additionally, this page represents a work in progress that is subject to frequent changes. |

---

Bulk inserts data into a FeatureBase table. Using bulk insert you can insert multiple rows of data from a file, URL or an inline blob, using CSV or NDJSON formats. Additionally bulk insert allows for lightweight data transformation all within one request.

FeatureBase bulk insert uses an update/insert semantic. If the row exists, the values in each column will be updated to the new values.

Here is an example of a bulk insert statement that reads from a CSV file and does some lightweight transformations:

```sql
bulk replace
    into insert_test (_id, int1, string1, timestamp1) 
    map (0 id, 1 int, 2 string)
    transform (@0, @1, @2, current_timestamp) 
from 
    '/dev/queries/insert_test.csv' 
with
    format 'CSV'
    input 'FILE';
```

## Syntax

![expr](/img/sql/bulk_insert_stmt.svg)

### column_list

![expr](/img/sql/column_list.svg)

_column_list_ is the target list of columns to be inserted into. They must be valid columns for the specified table _table_name_, and one of the columns must be the `_id` column. If no _column_list_ is specified, a column list consisting of all columns in the table is assumed.

### MAP clause

![expr](/img/sql/map_list.svg)

The MAP clause defines how the source data is read and what the expected data types are.

_map_list_ is a list of expressions and data types that specify how to get the source data from the source. If a TRANSFORM clause is specified, the values from the map can be referenced using variables named for the ordinal position they are specified in the map clause. For example, given a MAP clause as follows:

`MAP (0 id, 1 int, 4 string)`

the values can be referred to using the variables `@0`, `@1` and `@2` respectively. If there is no TRANSFORM clause specified, the values from the map clause are placed directly into the columns specified in the _column_list_.


#### MAP clause for CSV data

If CSV is specified as the source, the map expression should be an integer offset for the desired column in the CSV data. The data in that column is read and an attempt is made to convert it to the specified data type. An error occurs if the data cannot be converted to the type specified.

#### MAP clause for NDJSON data

If NDJSON is specified as the source, the map expression should be a string [JsonPath expression](https://goessner.net/articles/JsonPath/index.html#e2) for the desired value in the NDJSON data:

`MAP ('$.idpath' id, '$.int.path.' int, '$.path.to.string' string)`

 The expression is evaluated on the data and an attempt is made to convert it to the specified data type. An error occurs if the data cannot be converted to the type specified.

### TRANSFORM clause

![expr](/img/sql/value_list.svg)

The TRANSFORM clause allows specification of transforms before the rows are inserted. It is a list of expressions that are evaluated during execution for each row. Any valid SQL expression can be used in the transform clause. The values from the map can be referenced using variables named for the ordinal position they are specified in the map clause. For example, given a MAP clause as follows:

`MAP (0 id, 1 int, 4 string)`

the values can be referred to using the variables `@0`, `@1` and `@2` respectively.

The number of expressions in the TRANSFORM clause must match the number of expressions in the column list. Transforms can be any valid expression e.g. (given the `MAP` clause above):

```sql
TRANSFORM (
    @0 + 10, -- offset the new _id value by 10
    @1,      -- pass through unchanged
    case     -- clean up state names
        when @2 = 'Texas' then 'TX' end
        when @2 = 'California' then 'CA' end
        else @2
    end
)
```


### FROM clause

The FROM clause specifies the source of the data. It can be a single line string literal or a multi-line string literal. The way this literal is interpreted depends on the value of the INPUT option (ses below).

#### FROM clause for files

For files, the FROM clause should be a valid file name. In FeatureBase Cloud this will fail with an error because there is no local access to the file system.

#### FROM clause for urls

For urls, the FROM clause should be a valid url.

#### FROM clause for inline stream

For an inline stream, the contents of the literal a read as though they were in a file. A stream can be specified using the multi-line string literal syntax:

```sql
x'this
is
a
multi-line
string
literal'
```

FeatureBase will treat the contents of this string literal as though it was a file and read from it line by line.

#### FROM clause for STREAM data with single quotes (`'`) and double quotes(`"`)

Data in the FROM clause that contain single quotes (`'`) must be escaped with an additional single quote (even if CSV values are quoted). 

Incorrect inline STREAM example:

`FeatureBase's speed`

Correct inline STREAM example:

`FeatureBase''s speed`

If data in the FROM clause is quoted, the double quotes (`"`) in the data must be escaped with an additional double quote.

Incorrect inline STREAM example:

`""Time is money." – Benjamin Franklin."`

Correct inline STREAM example:

`"""Time is money."" – Benjamin Franklin."`

### WITH clause

![expr](/img/sql/bulk_insert_options.svg)
![expr](/img/sql/bulk_insert_option.svg)

The WITH clause allows you to pass statement level options

#### BATCHSIZE

Bulk insert commits row in batches. Use the `BATCHSIZE` option to specfify the batch size. The default is 1000.

#### ROWSLIMIT

Bulk insert allows you you limit the number of rows processed. Setting the `ROWSLIMIT` option to 100, for example, will limit the number of rows processed to 100.

#### INPUT

The `INPUT` option sets the type of input. Valid values are `'FILE'`, `'URL'` or `'STREAM'`

#### FORMAT

The `FORMAT` option sets the format of the source data. Valid values are `'CSV'` and `'NDJSON'`

#### NDJSON Options

The following options are only valid when `FORMAT` is `'NDJSON'`

##### ALLOW_MISSING_VALUES

If `ALLOW_MISSING_VALUES` is specified, any JsonPath expressions in the MAP clause that are valid but can't find a value in the data will return a `NULL`. This is useful if you expect some missing data and want to continue inserting. If `ALLOW_MISSING_VALUES` is not specified, an error will return on the first record of missing data.

#### CSV Options

The following options are only valid when `FORMAT` is `'CSV'`

##### HEADER_ROW

If `HEADER_ROW` is specified, the first row in the CSV is skipped.