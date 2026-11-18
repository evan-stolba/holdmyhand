# Playbook: Cleaning messy data

## What it is
Fixing problems in raw data so totals, counts and joins come out right: duplicates, blanks, extra spaces, inconsistent labels, wrong data types, impossible values.

## When to use it
Always, before analyzing new or messy data. Most "wrong numbers" are dirty data, not wrong formulas.

## Before you start
- **Never clean the original.** Save a copy, or use a repeatable tool (Power Query, Alteryx, SQL) so the raw file is untouched.
- Start an **assumption and decision log**: every cleaning choice goes in it ("removed 6 duplicate orders", "blank Sales treated as 0" vs "blank Sales rows excluded").

## Steps
1. **Health check first.** Record: row count; blanks per important column; for number columns min and max; for category columns the list of unique values. (Excel: `COUNTA`, `COUNTBLANK`, `MIN`, `MAX`, filter dropdowns. SQL: `COUNT(*)`, `COUNT(col)`, `MIN`, `MAX`, `SELECT DISTINCT`.)
2. **Teach-back:** "Looking at the unique values in Region, what problems do you see?"
3. **Fix text:** trim extra spaces and standardize case. Excel `=PROPER(TRIM(C2))`; Power Query **Transform > Trim** and **Format > Capitalize Each Word**; Alteryx **Data Cleansing**; SQL `INITCAP(TRIM(region))` (Snowflake/Postgres).
4. **Map variants** to one label ("NY", "New York", "new york" become "New York") with a small mapping table and a lookup.
5. **Fix types:** numbers stored as text, dates stored as text. Check: numbers should sum; dates should sort in time order.
6. **Handle blanks:** decide per column, with the user: remove the row, fill with a default, or leave and flag. Log the decision and how many rows it affected.
7. **Remove duplicates:** first decide what makes a duplicate (same Order ID? same everything?). Count them before deleting.
8. **Flag impossible values:** negative quantities, future dates, ages over 120. Don't silently delete; ask the user.
9. **Re-run the health check** and compare to step 1.

## Common mistakes
| Mistake | Fix |
|---|---|
| Cleaning by hand in the original file | Work on a copy or in a repeatable tool |
| Remove Duplicates across all columns when only ID matters (or vice versa) | Decide the key first |
| Replacing blanks with 0 without asking | Blank (unknown) and 0 (none) mean different things |
| Cleaning steps not recorded | Keep the decision log; it's the audit trail |
| Fixing one month's file by hand every month | Build it once in Power Query / Alteryx and refresh |

## How to check this
- Before vs after: row count change = rows you deliberately removed (dupes + excluded blanks). Any other change is a bug.
- Totals: the Sales total changes only by the amounts in removed rows.
- Unique values of each category column are now the clean list you expect.

## Practice exercise
`assets/sample_sales.csv` has: 6 duplicate orders, Region variants ("east ", "EAST", "West ", "south", "North "), 3 blank Sales values and 3 orders whose customer doesn't exist. Ask the user to find all four problems with a health check before fixing anything. After cleaning: 194 unique orders and 4 regions.
