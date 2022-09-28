---
id: percentile
title: Percentile()
sidebar_label: Percentile()
---

`Percentile()` returns the value at or below which some percent of values fall in the frequency distribution of a field's values.

Unlike the mean or median, the calculation of percentiles has no standard definition, but rather a variety of possible implementations. For large data sets following a continuous probability distribution, the results of different implementations should be very similar. The algorithm used by FeatureBase is **interpolated** and **inclusive**.

Interpolated means that the returned result value does not necessarily exist within the dataset. For example, for a field with two values, 1 and 5, the 50th percentile returned by FeatureBase is 3. In contrast, a nearest-rank implementation would return 1 or 5.

Inclusive means that the returned result value represents the value at or below which nth percent of values fall (the percentile includes the specified value), rather than just the value at which nth percent of values fall. For example, for a field with the values [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], the 50th percentile includes the value 5, which is exactly at the 50th percentile level, so the value returned by FeatureBase is 5. In contrast, an exclusive implementation would return 4.

## Call Definition

```
Percentile(field=FIELD, nth=NTH_VALUE, filter=ROW_CALL)
```

#### Mandatory Arguments
 - `field` / `FIELD`: the name of an Int field on which the percentile will be calculated. Decimal and Timestamp are not supported.
 - `nth` / `NTH_VALUE`: a whole number (such as 25) or a float (such as 80.5). This value should be within 0 and 100.0, both inclusive. When nth is 0, Percentile returns the minimum value. When nth is 100, Percentile returns the maximum value. When nth is 50, Percentile returns a value that is close to, but not necessarily exactly equal to, the median value.

#### Optional Arguments
 - `filter` / `ROW_CALL` : the [row call](/data-querying/pql#row-calls){:target="_blank"}  used to filter records if desired.
 
#### Returns
- the computed percentile and a count set to 1

## Examples

### Data:
```
Index: percentile

_id    | int (Int) 
-------+-----------
0      | 0           
1      | 10         
2      | 20        
3      | 30                                     
4      | 40          
5      | 50        
6      | 60        
7      | 70  
8      | 80          
9      | 90        
10     | 100         
11     | 110
12     | 120           
13     | 130         
14     | 140       
15     | 150
```
<hr>
### Example 1
Calculate the 20th percentile

#### Query
```
[percentile]Percentile(field=int, nth=20.0)
```
#### Tabular Response
```
 value | count
-------+-------
 30    | 1
```
#### HTTP Response
```json
{
  "results": [
    {
      "value": 30,
      "floatValue": 0,
      "decimalValue": null,
      "timestampValue": "0001-01-01T00:00:00Z",
      "count": 1
    }
  ]
}
```
#### Explanation
30 is larger than 0, 10, and 20 which together make up 18.75 percent of records. Note if we returned 40, it would be larger than 25 percent of records. Since we are using *inclusive*, we are returning the first value that is at or below the `nth` percentile argument.
