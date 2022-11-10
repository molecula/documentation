---
id: topk
title: TopK()
sidebar_label: TopK()
---
`TopK()` returns the count of records associated with field values in a given field. The top K most common (i.e. highest count) values are returned. It is equivalent to:

```
GroupBy(
  Rows(FIELD), 
  filter=ROW_CALL, 
  limit=UINT,
  sort="count desc"
)
```

Differences from TopN:
- TopN returns approximate results, and TopK returns exact results
- TopK supports time ranges, and TopN does not
- TopN requires a cache (ranked/lru) and TopK does not
- TopK computes total counts for all rows, and TopN does not
- TopK is deterministic, and TopN is not
- TopK does not currently support Tanimoto

Usage notes:
- TopK may take a second or longer to run on high-cardinality set fields
- TopK is fast when a sparse filter is applied, as this allows a large portion of work to be skipped
- When applying a filter which is correlated with row values, TopN and TopK may return dramatically different results

## Call Definition

```
TopK(FIELD, k=UINT, filter=ROW_CALL, from=TIMESTAMP, to=TIMESTAMP)
```

#### Mandatory Arguments
- `FIELD` : the name of the field to group by (i.e. count the records that have a relationship with each value in the field)

#### Optional Arguments
- `filter` / `ROW_CALL`: the [row call](/pql-guide/pql-introduction#row-calls){:target="_blank"} used to filter records included in the count.
- `k` : the number of field values to return (i.e. return the top `UINT` most common field values).
- `from` : the start date and time  when querying Time fields (`TIMESTAMP` formatted like `'2006-01-02T00:00:00Z'`). `TIMESTAMP` here is an *inclusive* value - i.e. records with relationships made on or after this time will be included in the result -- for Time fields only.
- `to`: the end date and time when querying Time fields (`TIMESTAMP` formatted like `'2006-01-02T00:00:00Z'`). `TIMESTAMP` here is an *exclusive* value - i.e. records with relationships made before this time (but not on this time) will be included in the result -- for Time fields only.


#### Returns
- list of (key,count) pairs sorted in descending order

## Examples

### Data:
```
Index: customer (non keyed index)

 _id | age (Int) | has_purchased (Set) | last_purchase (Timestamp)
-----+-----------+---------------------+---------------------------
 0   |    23     | ["brand1","brand2"] | 2021-01-05T08:30:00Z
 1   |    31     | ["brand1","brand3"] | 2020-09-12T12:30:00Z
 2   |    28     | ["brand1","brand3"] | 2021-08-06T16:15:00Z
 3   |    19     | []                  | null
 4   |    25     | ["brand1","brand4"] | 2021-10-01T20:45:00Z
 5   |    40     | ["brand4"]          | 2022-01-13T11:00:00Z
```
<hr>
### Example 1
What are the top brands that have been purchased from?

#### Query
```
[customer]TopK(has_purchased)
```
#### Tabular Response
```
 has_purchased | count
---------------+-------
 brand1        | 4
 brand4        | 2
 brand3        | 2
 brand2        | 1
```
#### HTTP Response
```json
{
  "results": [
    [
      {
        "id": 0,
        "key": "brand1",
        "count": 4
      },
      {
        "id": 0,
        "key": "brand4",
        "count": 2
      },
      {
        "id": 0,
        "key": "brand3",
        "count": 2
      },
      {
        "id": 0,
        "key": "brand2",
        "count": 1
      }
    ]
  ]
}
```
#### Explanation
4 customers have purchased from brand1, 2 customers have purchased from brand3 and brand4, and 1 customer has purchased from brand2.

<hr>
### Example 2
What is the top brand that have been purchased from?

```
[customer]TopK(has_purchased, k=1)
```
#### Tabular Response
```
 has_purchased | count
---------------+-------
 brand1        | 4
```

#### HTTP Response
```json
{
  "results": [
    [
      {
        "id": 0,
        "key": "brand1",
        "count": 4
      }
    ]
  ]
}
```

#### Explanation
4 customers have purchased from brand1 making it the top brand. The `k` arguments limits the return set to the most common brand.

<hr>

### Example 3
What are the top 2 brand from customers over 25?

```
[customer]TopK(has_purchased, filter=Row(age > 25), k=2)
```
#### Tabular Response
```
 has_purchased | count
---------------+-------
 brand3        | 2
 brand1        | 2
```

#### HTTP Response
```json
{
  "results": [
    [
      {
        "id": 0,
        "key": "brand1",
        "count": 2
      },
      {
        "id": 0,
        "key": "brand3",
        "count": 2
      }
    ]
  ]
}
```

#### Explanation
The `Row()` call limits the records to users over 25 years old - i.e. customers 1, 2, and 5. brand3 and brand1 where both purchased the most at two times.
