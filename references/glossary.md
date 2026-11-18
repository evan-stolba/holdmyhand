# Plain-English glossary

Use these definitions inline the first time a term comes up: bold the term, then the plain-English meaning in parentheses or a short sentence. Add an everyday analogy for brand-new users.

## Data basics
- **Dataset / table**: a grid of information, like a spreadsheet tab. Rows going across, columns going down.
- **Row / record**: one item, e.g. one order or one customer.
- **Column / field**: one kind of information about every item, e.g. "Order Date".
- **Header**: the top row with the column names.
- **Data type**: what kind of value a column holds: number, text, date, or true/false. Tools treat them differently; you can't add up text.
- **Null / blank**: a missing value. "Null" means nothing was ever entered; "empty" can mean an empty piece of text. Both can break totals.
- **Duplicate**: the same record appearing more than once.
- **ID / key**: a column that uniquely identifies each row, like an order number. Used to match tables.
- **CSV**: a plain text file where commas separate the columns. Opens in any spreadsheet tool.

## Shaping data
- **Filter**: keep only the rows that pass a test ("Region is East").
- **Sort**: put rows in order.
- **Join / merge**: match rows from two tables using a shared column, like matching orders to customers by Customer ID. Like matching name tags to a guest list.
- **Inner join**: keep only rows that match on both sides.
- **Left join**: keep everything from the first table, and add matches from the second where they exist.
- **Union / append**: stack two tables with the same columns on top of each other (January + February).
- **Group by / summarize / aggregate**: collapse many rows into one per group and calculate totals or averages, e.g. total sales per region.
- **Pivot / cross tab**: turn values from a column into new column headers, e.g. months across the top.
- **Unpivot / transpose**: the opposite; turn columns into rows.
- **Calculated column / formula**: a new column worked out from others (Profit = Sales minus Cost).
- **Parse**: split or convert text into usable pieces, e.g. turning "2024-03-15" text into a real date.
- **Trim**: remove extra spaces at the start or end of text. A hidden space makes "East " different from "East".

## Analysis
- **Metric / measure / KPI**: a number you track to judge performance (revenue, churn rate). KPI = key performance indicator, a metric that really matters to the business.
- **Dimension**: a category you slice metrics by (region, product, month).
- **Average (mean)**: total divided by count.
- **Median**: the middle value when sorted; not thrown off by a few extreme values.
- **Outlier**: a value far from the rest; might be a mistake or a real one-off.
- **Variance (business sense)**: the difference between two numbers, like actual vs target. (In statistics it means spread; clarify which.)
- **Year over year (YoY)**: comparing to the same period last year, which removes seasonal effects.
- **Run rate**: projecting the full-period result from current pace.
- **Trend**: the general direction over time.
- **Moving average**: the average of the last few periods, which smooths out bumps.
- **Correlation**: two things moving together. Doesn't prove one causes the other.
- **Segment**: a group of customers or items that share a trait.
- **Churn**: customers who stop buying or cancel.
- **Conversion rate**: the percent who take a desired action (visitors who buy).
- **ROI**: return on investment = (benefit minus cost) divided by cost.
- **Payback period**: how long until benefits cover the cost.

## Tools & workflows
- **Workflow (Alteryx)**: a saved chain of tools that processes data step by step, like a recipe.
- **Query (SQL / Power Query)**: a saved set of instructions to fetch or shape data.
- **Power Query**: the data cleaning engine built into Excel and Power BI; it records each step and replays it on refresh.
- **DAX**: the formula language for calculations in Power BI.
- **Measure (Power BI)**: a calculation that updates based on what's on screen (filters, chart grouping).
- **Relationship (Power BI)**: a link between two tables on a shared column so they can be used together.
- **Refresh**: re-run the steps to pull in the latest data.
- **Dashboard / report**: a page of charts and numbers for quick reading.
- **Schema**: the structure of a database: its tables, columns and how they connect.

## Confidentiality
- **PII**: personally identifiable information; anything that could identify a real person (name + email, phone, ID numbers).
- **Anonymize**: change data so individuals or clients can't be identified.
- **Mask**: hide part of a value, e.g. `****1234`.
- **Pseudonymize**: replace real identifiers with codes ("Client 001") while keeping a private lookup.
- **Aggregate**: share only totals, not individual records.
- **Least privilege**: only use or share the minimum data needed for the job.
