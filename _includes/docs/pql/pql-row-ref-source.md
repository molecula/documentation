
## Description

Rows are the fundamental vertical data axis within FeatureBase. They are namespaced to each field within an index. Represented as a Bitmap.

From /data-querying/_posts/2022-06-22-pql:

A *row* represents a single, binary characteristic that may be associated with any record. A row maintains a [set](https://en.wikipedia.org/wiki/Set_(mathematics)){:target="_blank"} of bits — a bitmap — indicating which records have a bit [Set](/reference/data-querying-ref/pql/write/set){:target="_blank"} for its attribute. To reduce ambiguity, a row may be referred to as a field value. Note that this is conceptually different from the use of "column" in other data stores, in that each row stores membership information per value. While this is mainly an implementation detail in normal FeatureBase usage, it can be helpful in understanding the underlying data model.

## Syntax


## Arguments


## Additional information


## Examples


## Further information

* [PQL Row]()
* [PQL Row bsi]()
* [PQL Rows]()
* [PQL Row timestamp]
