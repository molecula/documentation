---
id: unionrows
title: UnionRows()
sidebar_label: UnionRows()
---

`UnionRows()` is supplied, as arguments, any number of [Rows()](/pql-guide/read/rows) calls. Conceptually, `UnionRows()` does the following:
- unions all the field values in all the `Rows()` calls
- then, returns record IDs / keys for records that have at least one of field values in that list of field values.

`UnionRows(Rows(FIELD))` is equivalent to:

```
Union(
  Row(FIELD=FIELD_VALUE_0),
  Row(FIELD=FIELD_VALUE_1),
  ...
  Row(FEILD=FIELD_VALUE_N)
)
```

`UnionRows()` is a [row call](/pql-guide/pql-introduction#row-calls){:target="_blank"}.

## Call Definition

```
UnionRows(ROWS_CALL, ... )
```

#### Mandatory Arguments
- `ROWS_CALL` : a [rows call](/pql-guide/pql-introduction#rows-calls){:target="_blank"} (set of record IDs / keys). Note the FIELD argument to `Rows()` here must be a Set, Mutex, or Time field.

#### Optional Arguments
- `...` : Any number of additional [rows calls](/pql-guide/pql-introduction#rows-calls){:target="_blank"} seperated by commas. Note the FIELD argument to `Rows()` here must be a Set, Mutex, or Time field.

#### Returns
- list of record IDs or record keys

## Examples

### Data:
```
Index: customer (non keyed index)

 _id | age (Int) |  has_purchased (Set)    | last_purchase (Timestamp)
-----+-----------+-------------------------+--------------------------
 0   | 23        | ["brand_a1","brand_a2"] | 2021-01-05T08:30:00Z
 1   | 31        | ["brand_b1"]            | 2020-09-12T12:30:00Z
 2   | 28        | ["brand_a2","brand_b1"] | 2021-08-06T16:15:00Z
 3   | 19        | []                      | null
 4   | 25        | ["brand_c1","brand_c3"] | 2021-10-01T20:45:00Z
 5   | 40        | ["brand_a3"]            | 2022-01-13T11:00:00Z
```
<hr>
### Example 1
Which users have purchased from any brand?

#### Query
```
[customer]UnionRows(
  Rows(has_purchased)
)
```

#### Tabular Response
```
 _id
-----
 0
 1
 2
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
        4,
        5
      ]
    }
  ]
}
```
#### Explanation
`Rows(has_purchased)` returns the field values in the has_purchased field -- i.e. brand_a1, brand_a2, brand_b1, brand_a3, brand_c1, brand_c3. `UnionRows()` returns all the records that have any of those values. Note that record 3 is not included.

The equivalent `Union()` query would be:
```
[customer]Union(
  Row(has_purchased=brand_a1),
  Row(has_purchased=brand_a2),
  Row(has_purchased=brand_a3),
  Row(has_purchased=brand_b1),
  Row(has_purchased=brand_c1),
  Row(has_purchased=brand_c3)
)
```
<hr>
### Example 2
Which users have purchased from any brand that start with brand_a?

#### Query
```
[customer]UnionRows(
  Rows(has_purchased, like="brand_a%")
)
```

#### Tabular Response
```
 _id
-----
 0
 2
 5
```
#### HTTP Response
```json
{
  "results": [
    {
      "columns": [
        0,
        2,
        5
      ]
    }
  ]
}
```
#### Explanation
`Rows(has_purchased, like="brand_a%")` returns the field values in the has_purchased field that start with brand_a -- i.e. brand_a1, brand_a2, and brand_a3. `UnionRows()` returns all the records that have any of those values.

The equivalent `Union()` query would be:
```
[customer]Union(
  Row(has_purchased=brand_a1),
  Row(has_purchased=brand_a2),
  Row(has_purchased=brand_a3)
)
```
<hr>
### Example 3
Which users have purchased from any brand that start with brand_a ?

#### Query
```
[customer]UnionRows(
  Rows(has_purchased, like="brand_a%"),
  Rows(has_purchased, like="brand_c%")
)
```

#### Tabular Response
```
 _id
-----
 0
 2
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
        2,
        4,
        5
      ]
    }
  ]
}
```
#### Explanation
`Rows(has_purchased, like="brand_a%")` returns the field values in the has_purchased field that start with brand_a - i.e.  brand_a1, brand_a2, and brand_a3. `Rows(has_purchased, like="brand_c%")` returns the field values in the has_purchased field that start with brand_a -- i.e. brand_c1 and brand_c3. `UnionRows()` returns all the records that have any of those values.

The equivalent Union() `query` would be:
```
[customer]Union(
  Row(has_purchased=brand_a1),
  Row(has_purchased=brand_a2),
  Row(has_purchased=brand_a3),
  Row(has_purchased=brand_c1),
  Row(has_purchased=brand=c3)
)
```
