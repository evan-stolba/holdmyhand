# Playbook: Building a first dashboard

## What it is
A single page of charts and key numbers that answers a few recurring questions at a glance, and refreshes when the data changes.

## When to use it
A report someone looks at regularly (weekly sales, team KPIs, project status). For a one-off question, a single chart or the analysis summary template is usually better.

## Before you start (business questions first, tool second)
1. **Who looks at it, and what decision do they make from it?**
2. **Which 3 to 5 questions must it answer?** ("Are we on target this month?", "Which region is behind?")
3. **Define each KPI precisely:** name, formula, time period, filters. "Revenue = sum of Sales, excluding refunds, by order date, in USD." Put these in a KPI definition table; it prevents arguments later.
4. **Data:** tidy, one row per record, cleaned (see data-cleaning playbook), with a refreshable source.
5. **Who can see it?** If it contains Confidential or Restricted data, sharing settings and row-level security matter. Check with the data owner before publishing.

## Steps (Power BI; Tableau and Excel notes below)
1. **Get data** and clean it in Power Query (**Home > Transform data**). **Close & Apply**.
2. Add a **date table** and relationships if you have more than one table (see `../tools/power-bi.md`).
3. Create **measures** for each KPI (`Total Sales = SUM(Sales[Sales])`). Teach measures vs columns.
4. **Top row: KPI cards.** 3 to 5 **Card** visuals, each with a comparison (vs target, vs last month).
5. **Middle: the main trend.** A line chart of the key metric over time.
6. **Bottom: the breakdown.** A sorted bar chart (by region, product, team).
7. **Slicers** for the 1 or 2 filters people really use (date range, region). Not more.
8. **Teach-back:** "If you click East on the bar chart, what do you expect the cards to do?" (Cross-filter: they update to East only.)
9. Title each chart with the question it answers ("Which region is behind target?"), not just the field name.
10. Publish/share only through approved channels.

## Choosing the chart
| Question | Chart |
|---|---|
| Single number now | Card / KPI tile |
| Change over time | Line |
| Compare categories | Sorted bar (horizontal if labels are long) |
| Part of a whole (2 to 4 parts) | Stacked bar; avoid pies with many slices |
| Actual vs target | Bar with target line, or bullet chart |
| Two measures' relationship | Scatter |
| Exact values | Table (keep it small) |

## Tableau notes
Connect to data > drag dimensions to Rows/Columns and measures to the marks card; build each chart on its own **sheet**; combine sheets on a **Dashboard**; use **Actions** for click-to-filter; calculated fields via **Analysis > Create Calculated Field**.

## Excel notes
Pivot tables + pivot charts on one sheet, **Insert > Slicer** connected to all pivots (right-click slicer > **Report Connections**). Refresh with **Data > Refresh All**.

## Common mistakes
| Mistake | Fix |
|---|---|
| Too many charts | 3 to 5 questions, one chart each |
| KPIs without context | Always show vs target or vs last period |
| Vague KPI definitions | KPI definition table, agreed with the owner |
| Pie charts with 10 slices, 3D charts | Sorted bar chart |
| Numbers don't match finance's report | Reconcile definitions (dates, refunds, currency) |
| Shared too widely | Check sharing permissions and row-level security |

## How to check this
- Each KPI card matches an independent calculation (a pivot table or SQL query on the same data).
- Clicking a filter changes all visuals the way you'd expect.
- After a refresh with new data, totals change by the expected amount.

## Practice exercise
Using the three files in `assets/`: cards for Total Sales, Total Profit (Sales minus Cost), and % of target; a line of monthly sales; a bar of sales by region vs target (from `sample_targets.csv`); a Region slicer.
