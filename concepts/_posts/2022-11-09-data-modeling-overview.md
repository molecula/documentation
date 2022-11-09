---
title: Data Modeling
---

Data modeling is a key component in FeatureBase that involves understanding both how you will consume your data and how FeatureBase can represent your data to meet your needs.

IMPORTANT: Data modeling must be performed before ingestion to avoid long-term issues

<!--see DOCS-58 for other sources of information that need reviewing-->

## Before you begin

* [Learn about FeatureBase](/index.html)
* [Contact FeatureBase support with questions about data modeling](/https://www.featurebase.com/contact-us)

## Concepts

When importing data into FeatureBase, you have a number of choices about how to represent that data.

Choices about data representation mean trade-offs in both storage and runtime performance, and there are no best answers for all circumstances.

This section offers guidance on likely ways to make these decisions, and a bit of theory describing what's happening under the hood to help you make better choices. If you're not sure, it's always a good idea to try things out and compare results.

## Facts and Dimensions

In a standard relational model, one often hears about "fact" tables vs "dimensions". Each record in a fact table typically represents an immutable event (e.g. someone clicked a link or made a purchase, a temperature reading was recorded, etc). Dimensions on the other hand usually represent slower changing "metadata". If your fact is that a user performed a certain action, one of your dimensions might be a "users" table that records things like date of birth, gender, address. Recording this information along with every fact would lead to a huge amount of duplication so it is typically split out.

In FeatureBase, you can model things as you typically would in a relational database with facts and dimensions split apart, but FeatureBase has some unique capabilities that give you more options. Usually when you're doing queries that involve facts, you're not interested in the events themselves, but one of the dimensions that they affect. For example, you might want to know how many users visited a certain blog post as opposed to how many times that blog post was visited. They sound similar, but the first query is typically much more difficult because you're counting the distinct number of users rather than the number of events. In FeatureBase, you could add a "pages_visited" set type field directly to your users dimension and get the distinct functionality essentially for free. The power of the set field is that it can track multiple pages visited per user without additional overhead.

But wait! There's more. What if you only wanted to get the set of users who visited a page within the past month? You'd have to go back to joining the facts with the dimension right? Nope. FeatureBase also has "time" fields which are just like set fields except you have the option to associate a coarse-grained timestamp with every user-page association (in fact you can have multiple timestamps associated with a single user-page pair). Currently the timestamps can be at yearly, monthly, daily, or hourly granularity, and FeatureBase lets you query across arbitrary time ranges.

It takes up more space to store things like this, but if you have a workload that demands low latency for these types of queries it can be a very worthwhile tradeoff over storing the facts separately and joining across the dimensions at query time.

## Fields

Fields are used to segment rows within an index, for example to define different functional groups. A FeatureBase field might correspond to a single field in a relational table, where each row in a standard FeatureBase field represents a single possible value of the relational field. Similarly, an integer field could represent all possible integer values of a relational field.

<!-- TODO

### Field Options

this section is a placeholder, to provide minimal information about field options that are still exposed in the API, and linked from the http-api page -->

### Ranked

Ranked Fields maintain a sorted cache of column counts by Row ID (yielding the top rows by columns with a bit set in each). This cache facilitates the TopN query. The cache size defaults to 50,000 and can be set at Field creation.

<!-- TODO diagram? -->

#### LRU

The LRU cache maintains the most recently accessed Rows.

<!-- TODO diagram? -->

### Time Quantums

Setting a time quantum on a field creates extra views which allow ranged Row queries down to the time interval specified.

* [Learn about Time quantums and TTL](/concepts/time-quantums)

### TTL (Time To Live)

TTL is an option for fields with the type of time. Time quantum is required for TTL to function.

* [Learn about Time To Live](/concepts/time-to-live)

### Numeric Types

FeatureBase has three ways to represent numeric data; sets, mutexes, and integer fields. Each of these field types uses a set of bitmaps under the hood where each bitmap represents a particular value for the field, and each position in a bitmap represents whether a record has that value. In a set field, each record can have any number of different values. Each value is logically independent. In general, sets are a good way to represent data where multiple traits or parameters are logically independent.  A mutex is like a set, but each record can only have one value at a time; setting one value will clear the others. Int fields represent arbitrary values within a range, using multiple bitmaps to store binary digits of the values. Like a mutex, an int field has only one value per record at any given time.

Even in the case where only one value is likely to be set for a given record, you may prefer set fields. If you always know the previous value, clearing that value directly will be more efficient than relying on the mutex logic to clear the other possible values. Integer fields support range queries, but any query will generally have to access all the bitmaps in the field since each one represents a binary digit. Set and mutex fields don't support range queries, but can query only the values they care about.


### Integer Field Implementation

In FeatureBase's current architecture, integer fields are implemented using bitplanes. The values in the field are decomposed into bits, and corresponding bits from integer field become bitmaps in the storage. So, one of the bitmaps represents the lowest-order bit (value 1) of every record's value. An integer field has existence and sign bits, and represents values around a given base value. Thus, the total number of rows used will be 2 + log<sub>2</sub>(N), where N is the distance from the base to the highest or lowest value. (The exact size might vary depending on how you set the field up; a range from 0 to 100,000 which never uses negative values has a sign bit which is never set, a range from -50,000 to +50,000 with an offset of 50,000 has the same range but needs one less row for data values.)

The following table gives approximate estimated storage density for about a million records, assuming every record has values. A "weighted" distribution implies one with a significant variance in distribution, such as power-law or zipfian distributions, where some rows are very populated and some lightly populated.

Storage requirements for data


|                         | Integer |             |               | Mutex |             |               |
| ---                     |     --- | ---         | ---           |   --- | ---         | ---           |
| **Range, Distribution** |    Rows | Storage/Row | Total Storage |  Rows | Storage/Row | Total Storage |
| 0-15, even              |       4 | 128KiB*     | 513KiB        |    16 | 128KiB      | 2040KiB       |
| 0-15, weighted          |       4 | 60-128KiB*  | 445KiB        |    16 | 4KiB-128KiB | 638KiB        |
| 0-63, even              |       6 | 128KiB*     | 769KiB        |    64 | 33KiB       | 2064KiB       |
| 0-63, weighted          |       6 | 14-128KiB   | 506KiB        |    64 | 0.5-128KiB  | 687KiB        |
| 0-1023, even            |      10 | 128KiB      | 1282KiB       |  1024 | 2KiB        | 2304KiB       |
| 0-1023, weighted        |      10 | 1-128KiB    | 536KiB        |  1024 | 0-128KiB    | 743KiB        |


[*] Existence bitmaps are 352 bytes, and sign bitmaps are 0, in this data set; the table only shows sizes for the value bitmaps. In sparser data, the existence and sign bitmaps might be non-trivial.

Integer fields with evenly distributed values will tend to have fairly high cardinality -- every value will probably set every bit in its range about half the time, so if you have values for most records, the individual bitmaps will tend to be fairly full, and will approach the maximum storage requirements, slightly over one bit per record per bitmap. With weighted values, the top bits may well have low enough cardinality to produce some space savings. The differences are much more significant with set/mutex type fields; most of the higher values in the 1024-value mutex field were empty (no file created on disk at all), and most of them were under 50 bytes.

### Timestamp Field Implementation

Timestamp fields are implemented internally the same way as integer fields and store the number of time units (e.g. seconds) since an epoch.
By default, the `timeUnit` is in seconds (`s`) and the epoch is midnight, January 1, 1970 UTC. Other `timeUnit` values are `ms`, `us`, `ns`.
Adjusting the `timeUnit` and epoch can limit the range of integer value and reduce the storage requirements and computation time when processing records.

The following table gives approximate estimated storage density for about a million records, assuming every record has values.
Storage requirements for timestamp data when using a "seconds" time unit

|                         | Integer |             |               |
| ---                     |     --- | ---         | ---           |
| **Range, Distribution** |    Rows | Storage/Row | Total Storage |
| 1 day                   |      17 | 128KiB*     | 2176KiB       |
| 1 week                  |      20 | 128KiB*     | 2560KiB       |
| 1 month                 |      22 | 128KiB*     | 2816KiB       |
| 1 year                  |      25 | 128KiB*     | 3200KiB       |
| 10 years                |      29 | 128KiB*     | 3712KiB       |


Bottom line: If you're storing timestamps at second granularity, you can expect it to use about 3.7MB per million records.
At millisecond granularity, it would use 4.9MB per million records.
