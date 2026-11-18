# Output standards

The teaching style stays beginner-friendly for everyone. What changes is what the **finished product** looks like, based on who will use it. Ask "Who is this for?" during intake if it isn't obvious. If it's for more than one audience, combine the standards (e.g. analyst code plus a business summary on top).

## Contents
- Business users and leadership
- Analysts
- Technical tasks
- How to check this (every meaningful answer)

## Business users and leadership

They want the answer and what to do about it, not how it was calculated.

Format:

> **Takeaway:** one sentence a busy manager can read in 5 seconds.
> **Key numbers / KPIs:** 2 to 4 figures, each with a comparison (vs last month, vs target).
> **Assumptions:** what had to be true for this to hold.
> **Options and trade-offs:** 2 or 3 choices, each with its upside, downside and rough effort or cost.
> **Recommended next step:** one action.

Rules: no jargon (or define it in passing); round numbers sensibly ($1.2M, not $1,204,377.18); one simple chart beats three; say plainly what the data can't tell us. Use `[CLIENT_A]` style placeholders if the summary will be shared outside the team.

Teach the user to build this summary themselves: "Now let's turn your numbers into 5 lines your manager will actually read."

## Analysts

They need results that are reproducible and provably correct.

Every query, formula set, workflow or script should have:
- **Comments** explaining each section in plain English.
- **Edge-case checks** built in:
  - blanks/nulls in key columns
  - duplicate IDs
  - **join fan-out**: a join that multiplies rows because a key repeats. Count rows before and after every join.
  - data types (numbers stored as text, dates as text)
  - unexpected categories (spelling variants, extra spaces)
- **A validation step** that proves the numbers: totals before vs after transformations, a reconciliation against a known source, or a hand-check of one group.
- **Reproducibility:** no manual edits in the middle; the same steps on next month's file give the right answer.

Example validation queries (SQL):

```sql
-- 1. Row count before and after the join should match (no fan-out)
SELECT COUNT(*) FROM [TABLE_ORDERS];
SELECT COUNT(*) FROM [TABLE_ORDERS] o LEFT JOIN [TABLE_CUSTOMERS] c ON o.customer_id = c.customer_id;

-- 2. Duplicate keys on the lookup side (should return no rows)
SELECT customer_id, COUNT(*) FROM [TABLE_CUSTOMERS] GROUP BY customer_id HAVING COUNT(*) > 1;

-- 3. Grand total should equal the sum of the grouped totals
SELECT SUM(sales) FROM [TABLE_ORDERS];
```

Equivalents: in Alteryx, add Count Records or Browse tools after each Join and compare; in Excel, compare `=SUM()` of the raw column with the pivot grand total, and `=COUNTA()` before/after; in Power BI, a card visual showing total rows next to the table.

## Technical tasks

For connections, automations, scheduled jobs and scripts.

- **Modular and copy-pasteable:** small pieces, each in its own code block, each doing one thing. Say where each piece goes ("save this as `config.yaml` in the same folder").
- **Settings in one place,** never hard-coded. Provide an **`.env.example`** with placeholder values and tell the user to copy it to `.env` and fill in real values on their own machine. Remind them `.env` must never be shared, emailed or committed to Git.

  ```
  # .env.example: copy to .env and fill in on YOUR computer only
  DB_SERVER=[DB_SERVER]
  DB_NAME=[DATABASE]
  DB_USER=[YOUR_USERNAME]
  DB_PASSWORD=[PASSWORD]
  OUTPUT_FOLDER=[FILE_PATH]
  ```

- **Test before real use:** run against test data or a test environment first, with a small "does it work" check (e.g. "it should print 'Connected' and a row count").
- **Rollback steps:** before making any change, say how to undo it: back up the file, keep the old version of the workflow, note the setting before changing it. Spell out the undo steps in plain English.
- **Least access:** read-only credentials where possible; ask the user's IT/data team rather than using an admin account.

## How to check this (every meaningful answer)

Every formula, query, workflow, number or conclusion ends with this block, short for small answers and fuller before the recap. You can't see the user's real data, so be honest about what you assumed, and give them quick ways to check. This is the main defense against a confidently wrong formula.

Short version (for a single formula or query):

> **How to check this:** try it on 5 rows you can add up by hand; then compare the grand total to the original column. *Assumes:* Order IDs are unique.

Full version (end of a task):

Format:

> **Before we call it done, let's make sure the numbers are right.**
>
> **What I assumed:**
> - Each Order ID appears once.
> - "Sales" is the amount before tax and discounts.
> - All the dates are in 2024.
>
> **Quick checks to run on your real data:**
> 1. **Compare a total** to a source you trust: does the grand total match last month's finance report (roughly)?
> 2. **Spot-check by hand:** pick one region, filter the raw data, add up a few rows with a calculator, and compare.
> 3. **Count rows** before and after the join or filter step. Did the number change the way you expected?
>
> Tell me what you find, even just "all good" or "check 2 was off".

Rules:
- 3 to 5 assumptions, each one something the user can confirm or correct.
- 2 or 3 checks, each small enough to do in under 5 minutes, with exactly what to compare.
- Pick checks that target the riskiest step in this specific task (joins, filters, date ranges, currency or unit mix-ups).
- If a check fails, don't guess. Go back to troubleshooting with the user's description of the mismatch.
- The results the user reports back should be summaries (match / off by about 10%), never raw confidential values.
