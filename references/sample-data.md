# Practice with fake sample data

Practicing on made-up data lets beginners learn without risk: no confidential info, no chance of damaging a real file, and mistakes are free.

## When to offer it
- Always offer at the roadmap (Phase 2) for brand-new users.
- When the user's real data is sensitive and can't be shared or anonymized easily.
- When debugging: reproduce the problem on fake data that has the same columns.

## Ready-made files in `assets/`

All names, companies, numbers and IDs are fictional.

| File | Rows | Columns | Good for |
|---|---|---|---|
| `sample_sales.csv` | 200 | OrderID, OrderDate, Region, Product, Category, CustomerID, Units, UnitPrice, Sales, Cost | Filtering, calculated columns (Profit), summarizing by region/product, trends, pivots, charts |
| `sample_customers.csv` | 40 | CustomerID, CustomerName, Segment, Region, SignupDate | Joins/merges with sales (on CustomerID), segment analysis |
| `sample_targets.csv` | 16 | Region, Quarter, SalesTarget | Actual vs target comparisons |

Built-in messiness for teaching cleaning (mention these only when the lesson reaches cleaning):
- A few duplicate orders (same OrderID twice).
- Some region values with extra spaces or different capitalization ("east ", "EAST").
- A few blank Sales values.
- Three sales rows with a CustomerID that isn't in the customers file (to show what a left join keeps and an inner join drops).

How to give the files to the user: share the CSV contents (they're small), or tell them to copy the text into a new file named `sample_sales.csv` and open it in their tool. In Excel they can also paste into a blank sheet and use **Data > Text to Columns** with comma as the delimiter.

## Making custom fake data

If the user needs fake data shaped like their real data:
1. Ask for the **column names and types only**, plus rough row count and any categories (e.g. "Region is one of 4 values").
2. Generate 10 to 50 rows of clearly fictional values: names like "Sample Co 01", "Alex Example"; emails at `example.com`; round, plausible numbers; dates in a realistic range.
3. Mirror the real structure closely enough that the steps transfer directly (same column names, same types, same quirks such as text-formatted numbers if their real file has them).
4. Present it as CSV text in a code block.

Never base fake data on real values the user mentioned (don't "lightly modify" a real client's name or salary).

## Moving from practice to real data

When the user is ready, give a short "swap" step: in Alteryx, point the Input tool at the real file; in Excel, paste the real data in place of the sample on the raw-data sheet; in Power BI, use **Transform data > Data source settings > Change Source**. Then tell them to check row counts and column names match what the workflow expects.
