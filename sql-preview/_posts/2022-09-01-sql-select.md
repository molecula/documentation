---
title: SELECT
---

| | |
|-|-|
| **ℹ️NOTE** | This page contains information that only applies to SQL Preview functionality (more information [here](/sql-preview/sql-preview)). Additionally, this page represents a work in progress that is subject to frequent changes. |

---


Selects data from a FeatureBase table.

## Syntax

![expr](/img/sql/select_stmt.svg)

#### DISTINCT

The DISTINCT keyword specifies that only unique rows exist in the output.

### top_clause

![expr](/img/sql/top_clause.svg)

The TOP clause specifies that a limit is applied to the number of rows returned in the output. the _expr_ used in the TOP clause must be an integer literal.

### select_list

![expr](/img/sql/select_list.svg)
![expr](/img/sql/select_item.svg)

The _select_list_ contains the items selected to form the output result set. The select list is a series of expressions seperated by commas.

These items can be:

- `*` short hand for all columns in a table; similarly, `qualifier.*` limits this expression to all columns for the table _qualifier_ specified
- _expr_ can be any constant, function or combination thereof joined by operators, or a subquery

Items in the _select_list_ can be aliased with a _column_alias_.

### from_clause

![expr](/img/sql/from_clause.svg)

The FROM clause specifies which relations to select data from. It is a list of _table_or_subquery_ expressions.

### table_or_subquery

![expr](/img/sql/table_or_subquery.svg)

The _table_or_subquery_ expression can be:

- a _table_name_ or _table_valued_function_
- a parenthesized _select_statement_

both of these expressions can be aliased with a _table_alias_

### table_option

![expr](/img/sql/table_option.svg)

The SHARDS option allows you to specify against with shards the query will run.

### where_clause

![expr](/img/sql/where_clause.svg)

The WHERE clause specifies a filter condition for the rows returned by the query. The _expr_ defines the condition to be met for a row to be returned. It can be any constant, function or combination thereof joined by operators, or a subquery

### group_by_clause

![expr](/img/sql/group_by_clause.svg)

The GROUP BY clause seperates the query result into groups of rows allowing aggregates to be performed on each group.

_column_expr_ specifies a column or a non-aggregate calculation on a column. The column must exist in the FROM clause of the SELECT statement, but is not required to appear in the SELECT list.  If a column is referenced in a non-aggregated expression in the SELECT list, it must appear in the GROUP BY list.

### having_clause

![expr](/img/sql/having_clause.svg)

### order_by_clause

![expr](/img/sql/order_by_clause.svg)
![expr](/img/sql/order_by_expression.svg)

The ORDER BY clause allows specification of the order that data is returned. It is a list of _order_by_expression_ that specify a column name or column alias or a column position in the SELECT list and whether the order is ASC or DESC.

