---
id: pql-intro
title: PQL Introduction
sidebar_label: PQL Introduction
---

Pilosa Query Language (PQL) is FeatureBase's native query language.

Like SQL, PQL is a declarative, set-based language. Unlike SQL, PQL expressions are built by composing function calls, using the familiar parentheses call syntax. With this function-compositional syntax, PQL functions operate on bitmaps as the atomic elements of the data store, expressing boolean operations of arbitrary complexity. PQL also provides a number of functions outside of this paradigm, which implement common data tasks like aggregation.

Many PQL calls return or accept objects representing rows ([row calls](#row-calls)) or columns ([rows calls](#rows-calls)), and understanding these types is key to composing the various types of PQL call to build a query.

For example, the [row call](#row-calls) is the basic query type for reading bitmaps and performing boolean operations on them. The input type signatures of row calls vary, but they always return an object representing a set contained in a single row (i.e. a *computed row*, not necessarily a *stored row*), which can be passed as an argument to other queries.

For a simple example, consider this diagram:

![PQL diagram](/img/pql-diagram.png)

This is a PQL query on a table of users which includes fields for gender, age, location, and interests. It asks a question involving a moderately complex boolean combination of these fields. Note that each annotated component within the `Count` is a separate [row call](#row-calls), representing a set of users; each of these could be a standalone query, or passed to a `Count` call, for example. `Count` accepts a single row call, regardless of its structure, and returns a scalar value.

While other calls may accept different types, this composition of function calls is an important concept for PQL usage.

For detailed information on each PQL call, see the [PQL reference](/reference/pql) section.

### A Note About Terminology

For historical reasons, FeatureBase's concepts of "row" and "column" are not conventional, and may be confusing.

In PQL:

- An *index* is a single "universe" of data, with a shared column space, and a group of related fields. The term *table* may be used interchangeably, as well as the deprecated term *VDS* (Virtual Data Source).
- A *column* represents an instance of the entity of concern for a given table, such as a user or an event. Columns are common to all fields and rows within an index. Because this concept might be referred to as a row in other data stores, to reduce ambiguity, a column may be referred to as a *record*.
- A *row* represents a single, binary characteristic that may be associated with any record. A row maintains a [set](https://en.wikipedia.org/wiki/Set_(mathematics)) of bits—a bitmap—indicating which records have a bit [Set](/reference/pql#set) for its attribute. Note that this is conceptually different from the use of "column" in other data stores, in that each row stores membership information per value. While this is mainly an implementation detail in normal FeatureBase usage, it can be helpful in understanding the underlying data model.
- A *field* is a grouping of rows, for example, to combine several single rows into a non-boolean categorical value, or an integer value. From a user's perspective, this term aligns well with usage by other data stores.

The names of the *Row Calls* and *Rows Calls* types, as well as calls like `Row` and `Rows` are all based on these definitions.


----

Because of the nested structure of the language, subexpressions in a query are often meaningful queries on their own, and terms like "query", "call", "keyword", and "function" may be used somewhat interchangeably. Here, *query* is used to refer to a conceptually complete, runnable query, and *call* refers to the individual named PQL functions from which queries are composed.

In some contexts, particularly FeatureBase's `/index/{index}/query` HTTP endpoint, a PQL *query request* may consist of any number of disjoint *queries* (also known as top-level calls), optionally separated by whitespace. These queries are executed serially, and their results are returned in order.


## Query Types

PQL queries can be broadly grouped into:

- Read operations, which comprise the majority of PQL keywords, and often the majority of PQL usage.
- Write operations, some of which are often avoided in favor of using [ingesters](/explanations/ingesters).
- [Other operations](/reference/pql#other-operations), currently including just the [options](/reference/pql#options) call, which modifies the execution context and return types of the queries passed to it.

Read operations can be further grouped into several types. All of these types are summarized here, with links to more detailed information on the [PQL Reference](/reference/pql) page.


### [Row Calls](/reference/pql#row-calls-read)

Row calls return an object representing a set of column keys, contained in a single row. Row calls may be used as input arguments to other queries. 

Row calls include:
- Row selection
  - [Row](/reference/pql#row) selects from a single set row, by row key.
  - [Row (Range)](/reference/pql#row-range) selects from a single time row, by row key and time range.
  - [Row (BSI)](/reference/pql#row-bsi) selects from a single integer row, by row key and integer value range.
  - [ConstRow](/reference/pql#constrow) provides a "literal" bitmap value, a constant bitmap.
- Boolean operations
  - [Union](/reference/pql#union) computes the set union across its one or more row call arguments.
  - [Intersect](/reference/pql#intersect) computes the set intersection across its two or more row call arguments.
  - [Difference](/reference/pql#difference) computes the set difference between its first argument and all subsequent arguments (all row calls).
  - [Xor](/reference/pql#xor) computes the exclusive set difference between its first argument and all subsequent arguments (all row calls).
  - [Not](/reference/pql#not) computes the complement of the single row call argument, relative to the *universal set* for the index.
  - [All](/reference/pql#all) returns the *universal set* for the index, all columns that have been set.
  - [UnionRows](/reference/pql#unionrows) computes the set union across many rows. Rather than accepting several row call arguments, `UnionRows` accepts any number of `Rows` arguments.
  
By return type, [Limit](/reference/pql#limit) is also a row call. It wraps other row calls to select a subset of results, in a pagination sense.

[Distinct](/reference/pql#distinct) is a special row-like call, in that it can be used in the same context that other row calls can be used, despite a slight variation in its output type.

### [Rows Calls](/reference/pql#rows-calls-read)

Rows calls return an object representing a set of row keys, contained in a single column. Rows calls may be used as input arguments to other queries.

Rows calls include:
- [Rows](/reference/pql#rows) returns a list of row IDs in the given field which have at least one bit set.

### [Membership Calls](/reference/pql#membership-calls-read)

Membership calls return a boolean value indicating set membership.

Membership calls include:
- [IncludesColumn](/reference/pql#includescolumn) indicates whether a given column key is present in a given row.

### [Count Calls](/reference/pql#count-calls-read)

Count calls return counts of the number of elements in *groups of sets*. Count calls are often the top-level call in a query.

Count calls include:
- [Count](/reference/pql#count) computes the scalar count of elements contained in its single [row call](#row-calls) argument.
- [GroupBy](/reference/pql#groupby) computes counts of the intersection of every combination of its [rows call](#rows-calls) arguments. GroupBy provides much of the basic grouping functionality that is available in a relational database.
- [TopN](/reference/pql#topn) computes the count of the top `N` rows in a field, with some caveats.
- [TopK](/reference/pql#topk) computes the count of the top `K` rows in a field, with fewer caveats.

### [Aggregation Calls](/reference/pql#aggregation-calls-read)
Aggregation calls perform other aggregation operations on *individual sets*.

Aggregation calls include:
- [Min](/reference/pql#min) computes the minimum integer value or timestamp value in a field, from a single row call argument.
- [Max](/reference/pql#max) computes the maximum integer value or timestamp value in a field, from a single row call argument.
- [Percentile](/reference/pql#percentile) computes the percentile of integer values in a field, from a single row call argument.
- [Sum](/reference/pql#sum) computes the sum of integer values in a field, from a single row call argument.

### [Exploratory Calls](/reference/pql#exploratory-calls-read)

Exploratory calls are used to drill down into a data set.

- [Extract](/reference/pql#extract) is analogous to a general `select` query in a relational database, returning a subset of both rows and columns.

### [Write Operations](/reference/pql#write-operations)

- [Store](/reference/pql#store) writes the results of the row call argument to the specified row.
- [ClearRow](/reference/pql#clearrow) sets all bits to zero in the specified row.
- [Set](/reference/pql#set) sets a single specified bit to one.
- [Clear](/reference/pql#clear) sets a single specified bit to zero.
- [Delete](/reference/pql#delete) iterates over all fields and views in a set of provided columns, removing the columns.
  
### [Other operations](/reference/pql#other-operations)

[Options](/reference/pql#options) modifies the execution context and return types of the queries passed to it.
