# SQL guide

> **Menus change between versions.** This guide was written in November 2026 from general knowledge of recent releases and has not been verified against every version. Before teaching, tell the user which version you're assuming, ask them to confirm what they see at the first step, and describe controls by appearance and purpose as well as name. If their screen doesn't match, ask what they see; don't insist the path is right.

Reference for teaching SQL to beginners. Ask which database and which program they type queries in (SQL Server Management Studio, Snowflake, BigQuery, Azure Data Studio, DBeaver...). Syntax varies a little between databases; note differences when they matter.

## Orientation (explain at Step 1 for brand-new users)

- A **database** holds **tables**; a table has **columns** (fields) and **rows** (records).
- A **query** is a question you ask the database in SQL. Reading queries (**SELECT**) don't change any data.
- Write the query in the editor, then **Run/Execute** (often a play button, **F5**, or **Ctrl+Enter**). Results appear below.

**Safety first:** beginners should only run **SELECT** queries. Warn clearly before anything with **UPDATE**, **DELETE**, **INSERT**, **DROP**, **TRUNCATE** or **ALTER**: these change or destroy data. Suggest they ask their data team for read-only access and to try queries on a test/dev database when possible.

**Confidentiality:** never paste connection strings, passwords, or server names into the chat. Table and column names are usually fine, but check if the names themselves are confidential (e.g. a project code name).

## Build queries in this order (teach one clause per step)

```sql
SELECT region, SUM(sales) AS total_sales   -- 4. which columns to show
FROM orders                                 -- 1. which table
WHERE order_date >= '2024-01-01'            -- 2. which rows
GROUP BY region                             -- 3. how to group
HAVING SUM(sales) > 10000                   -- 5. filter groups
ORDER BY total_sales DESC;                  -- 6. sort
```

Explain that you **write** SELECT first but the database **thinks** FROM > WHERE > GROUP BY > HAVING > SELECT > ORDER BY. That's why you can't use a SELECT alias in WHERE.

## Starter patterns

```sql
-- Peek at a table (always limit while exploring)
SELECT * FROM orders LIMIT 10;          -- SQL Server: SELECT TOP 10 * FROM orders;

-- Count rows
SELECT COUNT(*) FROM orders;

-- Distinct values in a column
SELECT DISTINCT region FROM orders;

-- Join orders to customers
SELECT o.order_id, c.segment, o.sales
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;

-- Keep all orders even without a matching customer
LEFT JOIN customers c ON o.customer_id = c.customer_id

-- Categorize
CASE WHEN sales > 1000 THEN 'Large' ELSE 'Small' END AS order_size

-- Find duplicates
SELECT order_id, COUNT(*) FROM orders GROUP BY order_id HAVING COUNT(*) > 1;
```

## Common beginner problems

| Symptom | Likely cause | Fix |
|---|---|---|
| "Invalid column name" / "column does not exist" | Typo, wrong table, or alias used in WHERE | Check spelling with `SELECT * ... LIMIT 10` |
| "Column must appear in GROUP BY" | Non-aggregated column in SELECT | Add it to GROUP BY or wrap in SUM/MAX |
| Text comparisons don't match | Quotes or case | Use single quotes for text: `'East'`; case sensitivity depends on database |
| Join returns way too many rows | Duplicate keys (one-to-many) | Check keys for duplicates first |
| Join loses rows | INNER JOIN drops non-matches | Use LEFT JOIN, check for NULLs |
| NULLs behave oddly | `= NULL` never matches | Use `IS NULL` / `IS NOT NULL` |
| Query runs forever | Huge table, no filter | Cancel; add WHERE and LIMIT; ask data team about indexes |

## Dialect notes

Examples default to generic SQL. Adjust for the user's database:

| Task | Snowflake | BigQuery | PostgreSQL | SQL Server |
|---|---|---|---|---|
| First 10 rows | `LIMIT 10` | `LIMIT 10` | `LIMIT 10` | `SELECT TOP 10 ...` |
| Table name | `db.schema.table` | `` `project.dataset.table` `` | `schema.table` | `db.schema.table` |
| Today | `CURRENT_DATE()` | `CURRENT_DATE()` | `CURRENT_DATE` | `CAST(GETDATE() AS date)` |
| Month of a date | `DATE_TRUNC('month', d)` | `DATE_TRUNC(d, MONTH)` | `DATE_TRUNC('month', d)` | `DATEFROMPARTS(YEAR(d), MONTH(d), 1)` |
| Days between | `DATEDIFF('day', a, b)` | `DATE_DIFF(b, a, DAY)` | `b - a` | `DATEDIFF(day, a, b)` |
| Text concat | `a \|\| b` | `CONCAT(a, b)` | `a \|\| b` | `a + b` or `CONCAT(a, b)` |
| Case-insensitive match | `ILIKE` | `LOWER(a) LIKE` | `ILIKE` | `LIKE` (usually case-insensitive) |
| Safe divide | `DIV0(a, b)` | `SAFE_DIVIDE(a, b)` | `a / NULLIF(b, 0)` | `a / NULLIF(b, 0)` |

Notes: Snowflake stores unquoted names in UPPERCASE. BigQuery bills by data scanned, so select only the columns you need and filter on partitioned date columns; preview tables with the **Preview** tab (free) rather than `SELECT *`.

## Going deeper (pointers)

CTEs (`WITH ... AS`) to break queries into steps; window functions (ROW_NUMBER, running totals); date functions for your database; views; exporting results to Excel.
