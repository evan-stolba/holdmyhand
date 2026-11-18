# Playbook: First pivot table and XLOOKUP

## What it is
- A **pivot table** summarizes a big table in a few clicks: totals, counts or averages grouped by categories, with no formulas.
- **XLOOKUP** finds a value in another table and brings it back, like looking up a customer's segment from their ID.

## When to use it
Pivot: "sales by region by month", "count of tickets per team". Lookup: "add the customer segment to each order", "pull the price from the price list".

## Before you start
- **Check the version.** XLOOKUP exists in Microsoft 365, Excel 2021 and later, Excel for the web, and Google Sheets. **Excel 2019 and 2016 don't have it**: use `VLOOKUP` or `INDEX/MATCH` instead (below).
- Data should be **tidy**: one header row, one row per record, no blank rows or merged cells, no subtotal rows inside the data.
- Work on a copy.

## Steps: pivot table
1. Click any cell inside the data. Optional but recommended: **Insert > Table** (Ctrl+T) so the pivot grows with new data.
2. **Insert > PivotTable** (Sheets: **Insert > Pivot table**). Choose **New worksheet**. OK.
3. In the field list on the right, drag **Region** to **Rows**, **Sales** to **Values**.
4. Check the Values box says **Sum of Sales**, not **Count of Sales**. If Count, the column has text in it (see mistakes), or click it > **Value Field Settings > Sum**.
5. **Teach-back:** "If you drag OrderDate to Columns, what do you expect to see?" Then try it. Excel may group dates into years/quarters/months automatically; right-click a date > **Group** to choose.
6. Format numbers: right-click a value > **Number Format**.
7. When the source data changes: right-click the pivot > **Refresh**. The pivot doesn't update by itself.

## Steps: XLOOKUP
1. Put the lookup table (e.g. customers) on its own sheet named `Customers`.
2. In the orders sheet, add a header `Segment` in the first empty column.
3. In the first data row, type:
   ```
   =XLOOKUP(F2, Customers!A:A, Customers!C:C, "Not found")
   ```
   In plain English: "Take the CustomerID in F2, find it in column A of Customers, and bring back what's in column C on that row. If it's not there, say Not found."
4. Copy it down (double-click the small square at the bottom right of the cell).
5. **Teach-back:** "What would make a row say Not found?" (The ID isn't in the customers list, or there's a stray space or a number-vs-text mismatch.)
6. Filter the new column for **Not found** and look at those rows.

## Older Excel (2016/2019)
```
=IFERROR(VLOOKUP(F2, Customers!A:C, 3, FALSE), "Not found")
=IFERROR(INDEX(Customers!C:C, MATCH(F2, Customers!A:A, 0)), "Not found")
```
`FALSE` / `0` mean **exact match**. Leaving it out is the most common VLOOKUP bug: it returns wrong values silently.

## Common mistakes
| Mistake | Fix |
|---|---|
| Pivot shows Count instead of Sum | Column contains text or blanks; convert to numbers, then change to Sum |
| Pivot missing new rows | Refresh; use a Table as the source |
| `#N/A` everywhere in lookup | IDs are text on one side, numbers on the other; or extra spaces. Use `TRIM`, or **Data > Text to Columns > Finish** to convert |
| VLOOKUP returns wrong values | Missing `FALSE` for exact match |
| Lookup table has duplicate IDs | XLOOKUP returns the first match only; deduplicate or decide which one is right |
| Formula references shift when copied | Use `$` for fixed ranges, or whole columns as above |

## How to check this
- Pivot **Grand Total** = `=SUM()` of the original Sales column.
- `=COUNTIF(G:G, "Not found")` tells you how many lookups failed. Is that number expected?
- Spot-check 3 rows by searching the ID in the lookup sheet manually (Ctrl+F).

## Practice exercise
Using `assets/sample_sales.csv` and `assets/sample_customers.csv`: look up Segment for each order (expect 3 Not found), then pivot Sales by Segment and Region. Notice that "East", "east " and "EAST" show as separate rows: that's the cue for the data-cleaning playbook.
