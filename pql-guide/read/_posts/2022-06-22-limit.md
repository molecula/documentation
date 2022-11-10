---
id: limit
title: Limit()
sidebar_label: Limit()
---

The `Limit()` query returns some subset of record IDs / keys from a given [row call](/pql-guide/pql-introduction#row-calls){:target="_blank"} based on the limit and offset arguments provided. 

`Limit()` is a [row call](/pql-guide/pql-introduction#row-calls){:target="_blank"}.

## Call Definition
    
```pql
Limit(ROW_CALL, limit=UINT, offset=UINT)
```

#### Mandatory Arguments
- `ROW_CALL` : the [row call](/pql-guide/pql-introduction#row-calls){:target="_blank"} to be limited

#### Optional Arguments
- `limit` : the number of records you'd like to limit the query to. For example, limit=0 returns nothing and limit=100 returns 100 records. This is an optional argument. If it's not supplied there will be no limit on the number of records returned.
- `offset` : the offset from the beginning you'd like to use. For example, offset=0 starts at the beginning and could potentially return all the records. An offset=100 will start returning records after the first 100 that would have been returned by the `ROW_CALL`. This is an optional argument. If it's not supplied there will be no offset applied.

#### Returns

- list of record IDs or record keys


## Examples

### Data:

```
Index: customer

 _id | age |     has_bought	 |    last_purchase
-----+-----+---------------------+----------------------
 0   | 23  | ["brand1","brand2"] | 2021-01-05T08:30:00Z
 1   | 31  | ["brand1","brand3"] | 2020-09-12T12:30:00Z
 2   | 28  | ["brand1","brand3"] | 2021-08-06T16:15:00Z
 3   | 19  | []                  | null
 4   | 25  | ["brand1","brand4"] | 2021-10-01T20:45:00Z
 5   | 40  | ["brand4"]          | 2022-01-13T11:00:00Z
```
-----------------------------------------------------------------------
### Example 1
Return the first 3 record IDs

#### Query
```
[customer]Limit(All(), limit=3)
``` 

#### Tabular Response
```
 _id
-----
 0
 1
 2
```
#### HTTP Response
```json
{
  "results": [
    {
      "columns": [
        0,
        1,
        2
      ]
    }
  ]
}
```

#### Explaination
The first 3 record IDs are 0, 1, 2. No offset was applied so we start at the beginning.

-----------------------------------------------------------------------
### Example 2
Return 3 record IDs but start after the first record

#### Query
```
[customer]Limit(All(), limit=3, offset=1)
```
#### Tabular Response
```
 _id
-----
 1
 2
 3
```
#### HTTP Response
```json
{
  "results": [
    {
      "columns": [
        1,
        2,
        3
      ]
    }
  ]
}
```

#### Explanation
Offset of one means we start at the second record. Then we get a limit of 3 records which are 1, 2, 3.

-------------------------------------------------------------------------
### Example 3
Return the third record ID 

#### Query
```
[customer]Limit(All(), limit=1, offset=2)
```
#### Tabular Response
```
 _id
-----
 2
```

#### HTTP Response
```json
"results": [
    {
       "columns": [
         2
       ]
    }
]
```

#### Explanation
Offset of 2 means we start at the third record. Limit of 1 means we will only get one record - i.e. the third record.

-------------------------------------------------------------------------
### Example 4
Return Limit() using the default values.

#### Query
```
[customer]Limit(All())
```
#### Tabular Response
```
 _id
-----
 0
 1
 2
 3
 4
 5
```

#### HTTP Response
```json
{
  "results": [
    {
      "columns": [
        0,
        1,
        2,
        3,
        4,
        5
      ]
    }
  ]
}
```

#### Explanation
As we can see, if limit and offset arguments aren't supplied we get the same results as an All() query.
