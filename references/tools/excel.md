# Excel & Google Sheets guide

> **Menus change between versions.** This guide was written in November 2026 from general knowledge of recent releases and has not been verified against every version. Before teaching, tell the user which version you're assuming, ask them to confirm what they see at the first step, and describe controls by appearance and purpose as well as name. If their screen doesn't match, ask what they see; don't insist the path is right.

Reference for teaching spreadsheets to beginners. Covers Excel (Microsoft 365 desktop and web) and notes Google Sheets differences. Ask which one they use; menus differ.

## Orientation (explain at Step 1 for brand-new users)

- **Cell**: one box, named by column letter + row number (**B3**).
- **Range**: a block of cells (**A1:D20**).
- **Ribbon** (Excel): the tabs across the top (**Home**, **Insert**, **Data**, **Formulas**...). Google Sheets uses menus (**File**, **Edit**, **Insert**, **Data**...).
- **Formula bar**: above the grid; shows what's really in the selected cell.
- **Sheet tabs**: along the bottom.
- Every formula starts with **=**.

Tips: **Save a copy** before changing real data. **Ctrl+Z** undoes. Keep raw data on its own sheet and do work on another.

## Version check (ask first)

| Feature | Microsoft 365 / Excel 2021+ / Excel for the web | Excel 2019 | Excel 2016 | Google Sheets |
|---|---|---|---|---|
| XLOOKUP | Yes | No (use VLOOKUP / INDEX-MATCH) | No | Yes |
| Dynamic arrays (FILTER, UNIQUE, SORT) | Yes | No | No | Yes (FILTER, UNIQUE, SORT) |
| LET, LAMBDA | Yes | No | No | Yes |
| IFS, SWITCH, TEXTJOIN, CONCAT | Yes | Yes | Only with a 365 subscription | Yes |
| Power Query (Get & Transform) | Yes (web: limited) | Yes | Yes (Data > New Query) | No |
| Forecast Sheet | Yes (desktop) | Yes | Yes | No (use FORECAST/TREND) |

How to tell: **File > Account > About Excel** shows the version. If a formula gives `#NAME?`, the function probably doesn't exist in their version.

On Mac, Ctrl is usually Cmd, and some menus differ slightly. Excel for the web lacks some features (Power Pivot, some Power Query, macros).

## Turn data into a Table first (Excel)

Click any cell in the data > **Insert > Table** (or **Ctrl+T**) > confirm "My table has headers". **Why this matters:** tables auto-extend formulas, make filtering easy, and let formulas refer to columns by name.

## Core tasks

| Task | Excel | Google Sheets |
|---|---|---|
| Sort / filter | **Data > Sort** / **Data > Filter** (arrows on headers) | **Data > Sort range** / **Data > Create a filter** |
| Remove duplicates | **Data > Remove Duplicates** | **Data > Data cleanup > Remove duplicates** |
| Trim extra spaces | `=TRIM(A2)` | same, or **Data > Data cleanup > Trim whitespace** |
| Split a column | **Data > Text to Columns** | **Data > Split text to columns** |
| Pivot table | **Insert > PivotTable** | **Insert > Pivot table** |
| Chart | Select data > **Insert >** chart type | **Insert > Chart** |
| Highlight values | **Home > Conditional Formatting** | **Format > Conditional formatting** |
| Freeze header row | **View > Freeze Panes > Freeze Top Row** | **View > Freeze > 1 row** |
| Clean/reshape repeatable | **Data > Get Data / From Table/Range** (Power Query) | (no direct equivalent) |

## Beginner formulas

```
=A2-B2                         subtract
=SUM(C2:C100)                  total
=AVERAGE(C2:C100)
=COUNTA(A2:A100)               count non-blank cells
=SUMIFS(C:C, B:B, "East")      total of C where B is East
=COUNTIFS(B:B, "East")
=IF(C2>1000, "Large", "Small")
=XLOOKUP(A2, Lookup!A:A, Lookup!B:B, "Not found")
=TEXT(A2, "yyyy-mm")           date to year-month
=IFERROR(formula, "")          hide errors
```

Older Excel without XLOOKUP: `=VLOOKUP(A2, Lookup!A:B, 2, FALSE)`. Explain **FALSE** means exact match. Google Sheets supports XLOOKUP too.

Explain **$** (absolute reference) when a formula is copied down: `$A$1` stays fixed, `A1` moves.

## Common beginner problems

| Symptom | Likely cause | Fix |
|---|---|---|
| Formula shows as text | Cell formatted as Text, or missing `=` | Format as General, re-enter |
| `#N/A` from lookup | No match (spaces, different types) | TRIM both sides; check numbers aren't stored as text |
| `#VALUE!` | Math on text | Convert with `VALUE()` or Data > Text to Columns > Finish |
| `#REF!` | Referenced cells deleted | Undo, or rewrite the reference |
| `#DIV/0!` | Divide by zero/blank | Wrap with `IFERROR` |
| `#SPILL!` | Something blocking a dynamic array result | Clear cells below/right |
| Numbers left-aligned with green triangle | Stored as text | Click the warning > Convert to Number |
| Sum looks wrong | Hidden/filtered rows, or text numbers | Use `SUBTOTAL(9, range)` for visible only; convert text |
| Pivot doesn't show new data | Not refreshed | Right-click pivot > Refresh |

## Going deeper (pointers)

Power Query for repeatable cleaning; dynamic array functions (FILTER, UNIQUE, SORT); named ranges; data validation dropdowns; Power Pivot / data model.
