# Playbook: First Python / pandas script

## What it is
A short Python program that loads a spreadsheet, cleans or summarizes it, and saves the result. **pandas** is the Python library for tables. Scripts are repeatable and run on your own computer, which makes them ideal for Confidential and Restricted data (local mode).

## When to use it
The same spreadsheet steps every week; files too big for Excel; data that shouldn't leave your machine; learning to automate.

## Before you start
- **Check with IT** whether you're allowed to install Python. Many companies have an approved way (Anaconda, a software portal, or a managed environment). Don't install unapproved software on a work laptop.
- Simplest beginner setup: **Anaconda** or **Miniconda** from the company portal, or an approved Jupyter environment. In a notebook, you run one cell at a time and see results immediately, which suits learning.
- Work on a **copy** of the data, in a folder you control.

## Steps
1. **Open your environment** (Jupyter Notebook, VS Code, or the Python terminal IT provides). Check it works:
   ```python
   import pandas as pd
   print(pd.__version__)
   ```
   Expected: a version number. Error `No module named 'pandas'` means pandas isn't installed: `pip install pandas openpyxl` (or ask IT).
2. **Set the file paths at the top** (placeholders, edited on your own computer):
   ```python
   # ===== EDIT THESE ON YOUR COMPUTER =====
   INPUT_FILE  = r"[FILE_PATH]\sales.csv"
   OUTPUT_FILE = r"[FILE_PATH]\sales_summary.xlsx"
   # =======================================
   ```
   The `r` before the quotes lets Windows backslashes work.
3. **Load and look:**
   ```python
   df = pd.read_csv(INPUT_FILE)        # Excel: pd.read_excel(INPUT_FILE, sheet_name="Sheet1")
   print(df.shape)                     # (rows, columns)
   print(df.dtypes)                    # data type of each column
   ```
   Explain `df` is a "data frame", a table in memory. Avoid `print(df.head())` on Restricted data if you plan to share the output; shape and dtypes are safe to share.
4. **Teach-back:** "If shape says (200, 10), what does that mean?"
5. **Clean:**
   ```python
   df["Region"] = df["Region"].str.strip().str.title()   # trim spaces, fix case
   before = len(df)
   df = df.drop_duplicates(subset="OrderID")
   print("Duplicates removed:", before - len(df))
   print("Blank Sales:", df["Sales"].isna().sum())
   ```
6. **Calculate and summarize:**
   ```python
   df["Profit"] = df["Sales"] - df["Cost"]
   summary = df.groupby("Region")[["Sales", "Profit"]].sum().sort_values("Sales", ascending=False)
   print(summary)
   ```
7. **Save to a new file** (never overwrite the input):
   ```python
   summary.to_excel(OUTPUT_FILE)
   print("Saved", OUTPUT_FILE)
   ```
8. Save the script/notebook with a clear name so it can be re-run next month.

## Common mistakes
| Error / symptom | Cause | Fix |
|---|---|---|
| `FileNotFoundError` | Wrong path or file name | Copy the path from File Explorer; use `r"..."` |
| `KeyError: 'Sales'` | Column name differs (space, case) | `print(df.columns)` and copy the exact name |
| `TypeError` / strange sums | Numbers read as text | `pd.to_numeric(df["Sales"], errors="coerce")` |
| `ModuleNotFoundError` | Library not installed | `pip install pandas openpyxl`, or ask IT |
| `PermissionError` on save | Output file open in Excel | Close it, re-run |
| Indentation error | Mixed spaces/tabs | Use 4 spaces consistently |

## How to check this
- `df.shape` before and after: rows changed only by duplicates removed.
- `df["Sales"].sum()` equals the total in Excel for the same file (minus removed duplicates).
- Open the output file and spot-check one region against a pivot table.

## Practice exercise
Run the script above on `assets/sample_sales.csv`. Expected: 6 duplicates removed, 3 blank Sales, 4 regions after cleaning.
