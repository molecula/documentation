---
id: rows
title: Rows()
sidebar_label: Rows()
---

`Rows()` returns a list of field values (row IDs / keys) in a field. Most of the time, `Rows()` will be used as the argument of another call (e.g. [Extract()](/pql-guide/read/extract) or [GroupBy()](/pql-guide/read/groupby)) and only the FIELD argument will be supplied. In some cases (i.e. [GroupBy()](/pql-guide/read/groupby))) it makes sense to use additional arguments as filters to group by a subset of field values. See [GroupBy()](/pql-guide/read/groupby) for examples.


## Call Definition

```
Rows(
  FIELD, 
  like=STRING,
  column=UNIT_STRING,
  limit=UNIT, 
  from=TIMESTAMP, 
  to=TIMESTAMP, 
  previous=UINT_STRING
)
```

#### Mandatory Arguments
- `FIELD` : The field argument is the field you would like to return field values from. Note that Set, Mutex, and Time fields are the only supported fields for this arguement.

#### Optional Arguments
- `like` : The like argument is used to filter field values that returned for keyed fields. Only field values that match this filter will be returned. `_` represents any single character. `%` is used to match any number of characters - including 0. Every other character is matched exactly 
- `column` : The column argument can be an unsigned integer (record ID for unkeyed records) or a string value (record key for keyed records). When this argument is supplied, `Rows()` only returns the field value that this one record has.
- `limit` : The limit argument is an unsigned integer which represents the number of field values that will be returned. It limits the size of the returned set of field values
- `from` : The from argument should be a TIMESTAMP (e.g. '2006-01-02T00:00:00Z'). It can be used to filter a Time field based on the underlying timestamp(s) associated with each relationship. Only relationship made after this argument will be considered
- `to` : The from argument should be a TIMESTAMP (e.g. '2006-01-02T00:00:00Z'). It can be used to filter a Time field based on the underlying timestamp(s) associated with each relationship. Only relationship that happened before this argument will be considered
- `previous` : The previous argument can be an unsigned integer (non keyed records) or a string value (keyed records). Field values prior to and including this value will not be returned

Below are some examples and explanations of possible like argument values:

- `%` - match everything
- `_` - match all field values that are a single character
- `_%_` - match all field values that are 2 or more characters long
- `%a%` - match all field values that contain an 'a' and is any number or characters long
- `a_c` - match all field values that start with an 'a', end with 'c', and are three characters long
- `%t` - match all field values that end in 't'
- `boot` - only match field values that are exactly 'boot'

#### Returns
- Object with “rows” or “keys” keys and a value which is a list of unsigned integers or strings respectively.

## Examples

### Data:
```
Index: customer (non keyed index)

 _id | age |      has_purchased      |    last_purchase
-----+-----+-------------------------+----------------------
 0   | 23  | ["brand_a1","brand_a2"] | 2021-01-05T08:30:00Z
 1   | 31  | ["brand_b1","brand_a3"] | 2020-09-12T12:30:00Z
 2   | 28  | ["brand_a2","brand_b1"] | 2021-08-06T16:15:00Z
 3   | 19  | []                      | null
 4   | 25  | ["brand_c1","brand_c3"] | 2021-10-01T20:45:00Z
 5   | 40  | ["brand_a3"]            | 2022-01-13T11:00:00Z
```

<hr>
### Example 1
What are the brands that have been purchased from (i.e. what are the values in the `has_purchased` field)?

#### Query
```
[customer]Rows(has_purchased)
```
#### Tabular Response
```
 has_purchased
---------------
 brand_a1
 brand_a2
 brand_b1
 brand_a3
 brand_c1
 brand_c3
```
#### HTTP Response
```json
{
  "results": [
    {
      "rows": null,
      "keys": [
        "brand_a1",
        "brand_a2",
        "brand_b1",
        "brand_a3",
        "brand_c1",
        "brand_c3"
      ]
    }
  ]
}
```
#### Explanation
`Rows(has_purchased)` returns the list of values in the has_purchased field.

<hr>
### Example 2
What are the brands that have been purchased from (i.e. what are the values in the has_purchased field) that start with "brand_a"?

```
[customer]Rows(has_purchased, like="brand_a%")
```
#### Tabular Response
```
 has_purchased
---------------
 brand_a1
 brand_a2
 brand_a3
```

#### HTTP Response
```json
{
  "results": [
    {
      "rows": null,
      "keys": [
        "brand_a1",
        "brand_a2",
        "brand_a3"
      ]
    }
  ]
}
```

#### Explanation
The like argument above limits the returned field values to only the values that start with "brand_a".
