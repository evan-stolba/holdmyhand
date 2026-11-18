# Playbook: Reading an error message

## What it is
A method for turning a scary error into a plain-English problem with a fix. Errors are the tool telling you what it needs; they are normal and fixable.

## When to use it
Any error, warning, red mark or unexpected result in any tool.

## Step 1: Share it safely
Ask the user for:
- The **exact error text** (copy and paste is better than retyping; a cropped screenshot is OK).
- What they were doing when it happened (the formula, query, or step).
- What tool and version.

Before using it, **screen it**. Error messages often contain sensitive details: file paths with usernames (`C:\Users\jsmith\...`), server and database names, connection strings, the actual data value that failed ("cannot convert 'Acme Corp' to number"), sometimes passwords. Ask them to replace those with placeholders (`[FILE_PATH]`, `[DB_SERVER]`, `[VALUE]`). If a password or key is visible: hard stop, tell them to treat it as exposed and rotate it.

## Step 2: Read it with them (teach the method)
Most errors have the same parts. Teach the user to find them:
1. **Error type / code:** `#N/A`, `KeyError`, `Invalid column name`, `ORA-00942`, `HTTP 401`.
2. **The message:** what went wrong, in the tool's words.
3. **Where:** line number, cell, tool name in the workflow, step in Applied Steps.
4. **The thing it complained about:** a name, value or file in quotes.

In long errors (Python tracebacks, Java stack traces), **the last line is usually the real error**, and the line pointing to the user's own file is usually where to look.

## Step 3: Explain, fix, prevent
Respond in this format:

> **What it means:** one or two plain sentences.
> **Most likely cause:** and how to confirm it ("Check if the column is called 'Sales' or 'Sales ' with a space").
> **Fix:** numbered steps, one fix at a time, most likely first.
> **How to avoid it next time:** one line.
> **How to check it's fixed:** what they should see now.

If the first fix doesn't work, ask what changed (a new error is progress) and go to the next most likely cause. After two failed fixes, ask for more context rather than guessing.

## Common error families
| Family | Examples | Usual cause |
|---|---|---|
| **Not found** | `#N/A`, `#NAME?`, `KeyError`, `Invalid column name`, `table does not exist`, `FileNotFoundError` | Typo, wrong case, extra space, wrong sheet/table, wrong path |
| **Wrong type** | `#VALUE!`, `TypeError`, `cannot convert`, `conversion failed` | Text where a number or date was expected |
| **Nothing to work with** | `#DIV/0!`, `NoneType`, `null` errors | Blank or zero values |
| **Structure** | `#REF!`, `#SPILL!`, `must appear in GROUP BY`, `IndentationError` | Deleted references, blocked cells, grouping rules, formatting |
| **Permission / access** | `Access denied`, `401`, `403`, `PermissionError`, `insufficient privileges` | No rights, expired login, file open elsewhere. **Escalation rule:** don't work around access controls; ask the data owner or IT |
| **Resource** | timeouts, `MemoryError`, "query exceeded" | Too much data; filter earlier, sample first |

## How to check this
- The error is gone **and** the result looks right (an error-free wrong answer is worse).
- Run the relevant check from the main skill: row counts, a total, a spot check.

## Practice exercise
Show a fake error: `KeyError: 'Region'` from `df.groupby("Region")`. Ask the user to identify the type, the thing it complained about, and a likely cause (column is actually "Region " or "region"). Then show the fix: `print(df.columns)`.
