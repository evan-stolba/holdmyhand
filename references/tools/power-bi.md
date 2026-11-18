# Power BI Desktop guide (with Tableau notes)

> **Menus change between versions.** This guide was written in November 2026 from general knowledge of recent releases and has not been verified against every version. Before teaching, tell the user which version you're assuming, ask them to confirm what they see at the first step, and describe controls by appearance and purpose as well as name. If their screen doesn't match, ask what they see; don't insist the path is right.

Reference for teaching Power BI Desktop to beginners. Microsoft updates the interface often; confirm with the user what they see.

## Orientation (explain at Step 1 for brand-new users)

- **Three views** (icons down the left edge): **Report** (build visuals), **Table/Data** (see the data), **Model** (see how tables connect).
- **Data pane** (right): your tables and columns.
- **Visualizations pane** (right): chart types, and the field wells (**X-axis**, **Y-axis**, **Values**, **Legend**...) where you drop columns.
- **Filters pane**: filter one visual, one page, or the whole report.
- **Power Query Editor**: opened with **Home > Transform data**. This is where cleaning happens, before data reaches the report.

**Big idea:** Power BI has two halves. **Power Query** cleans and shapes data (every step is recorded and replays on refresh). The **report** shows it. Clean in Power Query, not by hand.

## Core tasks

| Task | Where |
|---|---|
| Load data | **Home > Get data** > Excel workbook / Text/CSV > pick tables > **Transform Data** (to clean first) or **Load** |
| Remove columns / rows | Power Query: right-click column header > **Remove**; **Home > Remove Rows** |
| Change data type | Power Query: click the type icon (ABC/123) on the column header |
| Remove duplicates | Power Query: select column(s) > right-click > **Remove Duplicates** |
| Trim spaces | Power Query: right-click column > **Transform > Trim** |
| Undo a step | Power Query: **Applied Steps** list on the right, click the X next to a step |
| Combine tables (join) | Power Query: **Home > Merge Queries** |
| Stack tables | Power Query: **Home > Append Queries** |
| Apply changes | Power Query: **Home > Close & Apply** |
| Relationships | **Model** view: drag a column from one table onto the matching column in another |
| Build a chart | Report view: click a visual type, drag fields into the wells |
| New calculation | **Home > New measure** (DAX) |
| Refresh | **Home > Refresh** |
| Share | **Home > Publish** (needs Power BI service access; check company policy) |

## Starter DAX measures

```
Total Sales = SUM(Sales[Amount])
Total Profit = SUM(Sales[Amount]) - SUM(Sales[Cost])
Profit Margin = DIVIDE([Total Profit], [Total Sales])
Order Count = DISTINCTCOUNT(Sales[OrderID])
Sales East = CALCULATE([Total Sales], Sales[Region] = "East")
```

Explain **measure vs calculated column**: a measure is calculated on the fly for whatever's on screen (use for totals and ratios); a column is calculated once per row (use for labels or categories). Beginners should default to measures for numbers.

`DIVIDE` is safer than `/` because it handles divide-by-zero.

## Common beginner problems

| Symptom | Likely cause | Fix |
|---|---|---|
| Same number repeated in every row of a visual | Missing or wrong relationship | Check Model view; connect the tables on the right column |
| Numbers won't sum (shows Count) | Column type is text | Power Query: change type to Decimal/Whole Number |
| Dates show as Year/Quarter/Month hierarchy unexpectedly | Auto date hierarchy | Click the dropdown on the field in the well, choose the date itself |
| Changes in Power Query don't show | Not applied | **Close & Apply** |
| Merge gives nulls | Values don't match exactly | Trim and make types match before merging |
| "Couldn't refresh" | File moved or renamed | **Transform data > Data source settings > Change Source** |

## Going deeper (pointers)

Star schema modeling; a proper date table; time intelligence (TOTALYTD, SAMEPERIODLASTYEAR); row-level security (important for confidentiality); bookmarks and drill-through; scheduled refresh in the service.

## Tableau equivalents

| Power BI | Tableau |
|---|---|
| Get data / Power Query | **Connect** pane; **Data Source** tab for joins, unions, and cleaning (or Tableau Prep for heavier cleaning) |
| Relationships (Model view) | Relationships ("noodles") on the Data Source canvas |
| Measure (DAX) | **Calculated field** (Analysis > Create Calculated Field), e.g. `SUM([Sales]) - SUM([Cost])` |
| Visual + field wells | Drag fields to **Rows**, **Columns** and the **Marks** card on a **Sheet** |
| Report page | **Dashboard** made of sheets |
| Slicer | **Filter** shown on the dashboard; **Actions** for click-to-filter |
| Analytics pane forecast | **Analytics** pane > Forecast |
| Publish to service | Publish to Tableau Server / Cloud (check sharing permissions) |

Common Tableau beginner traps: dimensions (blue, categories) vs measures (green, numbers); fields aggregated as SUM by default when you wanted AVG or a count; date fields defaulting to YEAR (click the pill to change to month); a join in the Data Source tab duplicating rows (check row counts, prefer relationships).
