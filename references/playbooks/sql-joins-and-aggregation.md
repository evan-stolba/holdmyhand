# Playbook: First SQL join and aggregation

## What it is
- A **join** combines two tables by matching a shared column (e.g. `orders.customer_id = customers.customer_id`).
- An **aggregation** collapses many rows into one per group and calculates a total, count or average (`GROUP BY`).

## When to use it
"Total sales by customer segment", "how many orders per region", "which products have no sales": any question where the answer needs columns from two tables, or a total per group.

## Before you start
- Read-only access (SELECT only). See the safety note in `../tools/sql.md`.
- Know the database dialect (Snowflake, BigQuery, Postgres, SQL Server); it changes small details.
- Names of the two tables and the column they share. If table or column names are confidential, use placeholders like `[TABLE_ORDERS]`.

## Steps
1. **Look at each table on its own.** `SELECT * FROM orders LIMIT 10;` (SQL Server: `SELECT TOP 10 *`). Note the columns and what one row represents ("one row per order").
2. **Count rows in each table.** `SELECT COUNT(*) FROM orders;` Write the numbers down. You'll need them to check the join.
3. **Check the join key is unique on the lookup side.**
   ```sql
   SELECT customer_id, COUNT(*) FROM customers GROUP BY customer_id HAVING COUNT(*) > 1;
   ```
   No rows back = good. Rows back = duplicates, which will multiply your orders (fan-out).
4. **Teach-back:** "If every order has exactly one matching customer, how many rows should the joined result have?" (Answer: the same as the orders table.)
5. **Write the join.** Start with LEFT JOIN so you don't silently lose rows:
   ```sql
   SELECT o.order_id, o.sales, c.segment
   FROM orders o
   LEFT JOIN customers c ON o.customer_id = c.customer_id;
   ```
   Explain `o` and `c` are short nicknames (aliases) for the tables.
6. **Count the joined rows** by wrapping it: `SELECT COUNT(*) FROM ( ...join... ) t;` Compare to step 2.
7. **Find non-matches:** add `WHERE c.customer_id IS NULL`. These are orders with no known customer. Decide with the user what to do with them (log it in the assumption log).
8. **Aggregate:**
   ```sql
   SELECT c.segment, COUNT(*) AS orders, SUM(o.sales) AS total_sales
   FROM orders o
   LEFT JOIN customers c ON o.customer_id = c.customer_id
   GROUP BY c.segment
   ORDER BY total_sales DESC;
   ```
   Explain: every column in SELECT is either in GROUP BY or inside SUM/COUNT/AVG.
9. **Teach-back:** "How many rows should this return?" (One per segment, plus one NULL row if some orders didn't match.)

## LEFT vs INNER, in one picture
- **INNER JOIN**: only orders that found a customer. Unmatched orders disappear silently.
- **LEFT JOIN**: all orders; customer columns are blank (NULL) where there's no match.
Default to LEFT while learning, so nothing vanishes without you noticing.

## Common mistakes
| Mistake | What happens | Fix |
|---|---|---|
| Duplicate keys in the lookup table | Totals are too high (fan-out) | Step 3 check; deduplicate first |
| INNER JOIN by habit | Rows silently dropped | Use LEFT, check step 7 |
| `WHERE c.segment = 'X'` after a LEFT JOIN | Turns it back into an INNER join | Put the condition in the `ON` clause, or accept it knowingly |
| Column not in GROUP BY | Error | Add it to GROUP BY or aggregate it |
| `COUNT(column)` vs `COUNT(*)` | COUNT(column) skips NULLs | Choose deliberately |
| Joining on names instead of IDs | Mismatches from spelling/spaces | Join on IDs |

## How to check this
- Joined row count = orders row count (step 6). If higher, you have fan-out.
- `SUM(sales)` of the final result = `SELECT SUM(sales) FROM orders;`
- Pick one segment, list its orders, add a few by hand.

## Dialect notes
- Row limit: `LIMIT 10` (Postgres, Snowflake, BigQuery), `TOP 10` (SQL Server).
- BigQuery table names: `` `project.dataset.table` `` in backticks.
- Snowflake: unquoted names are uppercase; `"MixedCase"` needs quotes.

## Practice exercise
Load `assets/sample_sales.csv` and `assets/sample_customers.csv` (any SQL tool that imports CSV, or SQLite). Join on CustomerID and total sales by Segment. Expected: 3 orders don't match a customer, and the file has 6 duplicate orders. Ask the user to find both.
