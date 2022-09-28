---
title: SQL Functions
---

| | |
|-|-|
| **ℹ️NOTE** | This page contains information that only applies to SQL Preview functionality (more information [here](/data-querying/sql/sql-preview)). Additionally, this page represents a work in progress that is subject to frequent changes. |

---


## Table Valued Functions

![expr](/img/sql/table_valued_function.svg)

## Aggregate Functions

![expr](/img/sql/agg_function.svg)

## Non-Aggregate Functions
 
![expr](/img/sql/non_agg_function.svg)

### setcontains()

This function tests membership of a value within a set expression.

#### Syntax

```
setcontains(set, value)
```

#### Arguments
_set_

The set in which value is being tested for membership. set must be of type `stringset` or `idset`

_value_

The value to test membership for in the set. value must be assignment compatible with the element type of the set.

#### Return Type
`bool`
#### Return Value
`setcontains()` returns true if value is a member of the set and false if it is not.
#### Remarks
None.
#### Examples
A. Testing set membership in the select list

```sql
create table segments  
    (_id id, segment stringset);  
    
insert into segments(_id, segment)  
    values (1, ['RED', 'BLUE', 'GREEN']);  
    
select setcontains(segment, 'BLUE') as HasBlue  
    from segments;  

-- Returns: true
```

B. Testing set membership as a where clause filter

```sql
create table segments  
    (_id id, segment stringset);  
    
insert into segments(_id, segment)  
    values (1, ['RED', 'BLUE', 'GREEN']);  
    
select _id, segment from segments where setcontains(segment, 'BLUE');  
+-----+------------------+
| _id | segment          |
+-----+------------------+
|   1 | [RED BLUE GREEN] |
+-----+------------------+
```

### setcontainsany()
This function tests membership of a set of values within a set. It returns true if any of the members of testset exist in targetset

#### Syntax
```
setcontainsany(targetset, testset)
```

#### Arguments
_targetset_

The set in which the members of testset are being tested for membership. targetset must be of type `stringset` or `idset`

_testset_

The set of values to test membership for in the targetset. The types of targetset and testset must be the same.

#### Return Type
`bool`
#### Return Value
`setcontainsany()` returns true if any member of testset exists in targetset and false if no member exists.
#### Remarks
None.
#### Examples
A. Testing set membership in the select list

```sql
create table segments  
    (_id id, segment stringset);  
    
insert into segments(_id, segment)  
    values (1, ['RED', 'BLUE', 'GREEN']);  
    
select setcontainsany(segment, ['BLUE', 'RED']) as HasBlueOrRed  
    from segments;  

-- Returns: true
```

B. Testing set membership as a where clause filter

```sql
create table segments  
    (_id id, segment stringset);  
    
insert into segments(_id, segment)  
    values (1, ['RED', 'BLUE', 'GREEN']);  
    
select _id, segment from segments where setcontainsany(segment, ['BLUE', 'RED']);  
+-----+------------------+
| _id | segment          |
+-----+------------------+
|   1 | [RED BLUE GREEN] |
+-----+------------------+
```

### setcontainsall()
This function tests membership of a set of values within a set. It returns true if all of the members of testset exist in targetset
#### Syntax
```
setcontainsall(targetset, testset)
```
#### Arguments
_targetset_

The set in which the members of testset are being tested for membership. targetset must be of type `stringset` or `idset`

_testset_

The set of values to test membership for in the targetset. The types of targetset and testset must be the same.

#### Return Type
`bool`
#### Return Value
`setcontainsall()` returns true if all members of testset exists in targetset and false if they don’t.
#### Remarks
None.
#### Examples
A. Testing set membership in the select list

```sql
create table segments  
    (_id id, segment stringset);  
    
insert into segments(_id, segment)  
    values (1, ['RED', 'BLUE', 'GREEN']);  
    
select setcontainsall(segment, ['BLUE', 'RED']) as HasBlueOrRed  
    from segments;  

-- Returns: true
```
B. Testing set membership as a where clause filter
```sql
create table segments  
    (_id id, segment stringset);  
    
insert into segments(_id, segment)  
    values (1, ['RED', 'BLUE', 'GREEN']);  
    
select _id, segment from segments where setcontainsall(segment, ['BLUE', 'RED']);
+-----+------------------+
| _id | segment          |
+-----+------------------+
|   1 | [RED BLUE GREEN] |
+-----+------------------+
``` 

