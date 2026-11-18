# Alteryx Designer guide

> **Menus change between versions.** This guide was written in November 2026 from general knowledge of recent releases and has not been verified against every version. Before teaching, tell the user which version you're assuming, ask them to confirm what they see at the first step, and describe controls by appearance and purpose as well as name. If their screen doesn't match, ask what they see; don't insist the path is right.

Reference for teaching Alteryx Designer to beginners. Menu labels can shift between versions; if the user's screen doesn't match, ask what they see.

## Orientation (explain at Step 1 for brand-new users)

- **Canvas**: the big empty area in the middle where you build the workflow.
- **Tool palette**: the row of tabs across the top (**In/Out**, **Preparation**, **Join**, **Parse**, **Transform**, ...). Each tab holds tools you drag onto the canvas. Hover over an icon to see its name. There's also a search box to find tools by name.
- **Configuration window**: usually on the left. Click a tool on the canvas to see and change its settings here.
- **Results window**: usually at the bottom. After running, click a tool's output anchor to see the data at that point.
- **Run**: the **Run** button (play icon) near the top right. Shortcut: **Ctrl+R**.
- **Anchors**: small arrows on the sides of tools. Data flows from an output anchor (right) to an input anchor (left). Connect tools by dragging between anchors.

**Why this matters (big idea):** an Alteryx workflow is a recipe. Data flows left to right through each tool, and each tool does one job. You can re-run the recipe on next month's file without redoing the work.

Tip: tell beginners to **save early** (File > Save As, .yxmd file) and to keep the workflow tidy left-to-right.

## Core beginner tools

| Task | Tool | Palette tab | Key settings | Outputs |
|---|---|---|---|---|
| Load a file | **Input Data** | In/Out | Connect a File, pick the file; for Excel choose the sheet | 1 |
| Look at data mid-way | **Browse** | In/Out | None; shows full data in Results | none |
| Save result | **Output Data** | In/Out | Write to File; pick .xlsx/.csv, name the sheet; choose overwrite option | none |
| Choose / rename / retype columns | **Select** | Preparation | Tick to keep, edit Rename, change Type | 1 |
| Keep rows that pass a test | **Filter** | Preparation | Basic (column + operator + value) or Custom formula | **T** (passed) / **F** (failed) |
| New or changed column | **Formula** | Preparation | Output column name, data type, expression | 1 |
| Remove duplicates | **Unique** | Preparation | Tick the column(s) that define a duplicate | **U** (unique) / **D** (duplicates) |
| Sort | **Sort** | Preparation | Column + Ascending/Descending | 1 |
| Clean up text/blanks | **Data Cleansing** | Preparation | Remove leading/trailing whitespace, replace nulls, change case | 1 |
| Match two tables | **Join** | Join | Pick the matching field from Left and Right | **L** (left only) / **J** (matched) / **R** (right only) |
| Stack tables | **Union** | Join | Auto-config by name | 1 |
| Group and total | **Summarize** | Transform | Pick column > Group By; pick number > Sum/Count/Avg | 1 |
| Pivot wide | **Cross Tab** | Transform | Group by, header column, value column, method | 1 |

## Common formula expressions (Formula tool)

```
[Sales] - [Cost]                           // new Profit column
IF [Sales] > 1000 THEN "Large" ELSE "Small" ENDIF
Trim([Region])                             // remove extra spaces
Uppercase([Region])
DateTimeFormat([Date], "%Y-%m")            // year-month, e.g. 2024-03
DateTimeDiff([ShipDate], [OrderDate], "days")
IsNull([Sales])
ToNumber([SalesText])
```

Column names go in **[square brackets]**. Text goes in "double quotes". Remind users that the output **data type** must fit the result (a number calculation should be Double or Int, not V_String).

## Common beginner problems

| Symptom | Likely cause | Fix |
|---|---|---|
| Nothing happens / no data in Results | Tools not connected, or not run | Check connecting lines; click Run |
| Red exclamation on a tool | Configuration incomplete or error | Click the tool, read the message in the Results/Messages area |
| Math gives errors or nulls | Number column is text (V_String) | Add a **Select** tool before, change Type to Double |
| Join drops rows unexpectedly | Values don't match exactly (spaces, case, types) | Look at the **L** and **R** outputs; clean with Data Cleansing / Trim; make types match |
| Join creates more rows than expected | Duplicate keys on one side | Check with Unique tool; explain one-to-many joins |
| Output file error "file in use" | File open in Excel | Close it in Excel, run again |
| Dates won't sort/filter properly | Dates read as text | **DateTime** tool (Parse tab) to convert |
| Can't find a tool | Wrong tab | Use the search box in the palette |

## Typical workflow shapes

- **Clean and export:** Input Data > Select > Data Cleansing > Filter (T) > Unique (U) > Output Data
- **Calculate and summarize:** Input Data > Formula > Summarize > Sort > Output Data
- **Combine two files:** Input A + Input B > Join (J) > Select > Output Data. Teach checking L and R with Browse tools to see what didn't match.

## Going deeper (pointers)

Containers and comments for tidy workflows; macros; scheduling (Alteryx Server); Multi-Field Formula for many columns at once; In-Database tools for big data.
