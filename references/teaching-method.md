# Teaching method

How to turn any "help me do X" request into a from-scratch lesson.

## Contents
- Breaking a request into steps
- The step format
- Skill-level dial
- Check-ins
- Troubleshooting branches
- "Want to go deeper?" pointers
- Recap and reusable checklist
- Worked example

## Breaking a request into steps

Users often ask in one sentence for several things: "help me use Alteryx to build a new spreadsheet that removes duplicates, adds a profit column, and totals by region."

1. **List the items they asked for.** Repeat them back as a short list so they can correct you.
2. **Add the hidden steps they didn't mention.** Every task has setup and finish steps beginners don't know about: opening the tool, loading the data, checking the data loaded correctly, saving/exporting, and checking the output.
3. **Order by dependency.** Clean before you calculate, calculate before you summarize, summarize before you chart.
4. **Size each step for one screen of action.** If a step needs more than about 5 clicks or two different windows, split it.
5. **Group steps into milestones** for the roadmap (3 to 8 milestones). A milestone may contain several steps.

Typical shape of a data task:

| Milestone | What happens |
|---|---|
| Set up | Open the tool, create a new file/workflow, save it with a name |
| Bring in data | Load the file, confirm columns and row count look right |
| Clean | Remove blanks, duplicates, fix data types, filter out rows |
| Combine | Join or append other data |
| Calculate | New columns, formulas |
| Summarize | Group and total, pivot |
| Present | Chart, format, sort |
| Deliver | Save/export, check the output opens correctly |

## The step format

Use this for every step. Headings may be bold text rather than markdown headings to keep it compact.

```
**Step 3 of 8: Remove rows with no sales amount**

**Do this:**
1. In the tool palette at the top, click the **Preparation** tab.
2. Drag the **Filter** tool onto the canvas (hover over icons to see their names) and drop it to the right of your Input tool.
3. Connect them: drag from the small arrow on the right of the Input tool to the left side of the Filter tool.
4. In the panel on the left, choose **Basic filter**, pick the column **SalesAmount**, choose **Is not null**.
5. Click **Run** (the green play button, top right).

**Why this matters:** Blank rows would quietly throw off your totals later. Filtering means "keep only the rows that pass a test."

**What you should see:** The Filter tool has two outputs, **T** (true, rows that passed) and **F** (false, rows that didn't). Click T: the row count should be a bit lower than your original.

**If something looks wrong:**
- *Nothing happens when you Run:* check the tools are connected by a line.
- *All rows went to F:* the column might be text, not a number. We'll fix that with a Select tool.

**Want to go deeper?** I can explain the difference between "null" and "empty", or how to write a custom filter formula.

**Check-in:** Click the T output. Roughly how many rows do you see?
```

Rules:
- **Hedge menu paths and verify.** Say "should be" for locations you can't be sure of in their version, and include a "What you should see" line so mismatches surface right away. If the first step reveals a different version or layout, say so and adapt.
- Use **bold** for anything they need to find on screen (buttons, menus, tool names, column names).
- Number the actions; one action per number.
- Describe icons and locations ("top right", "green play button") since beginners don't know names yet.
- Give exact text to type in a code block when it's a formula or query.

## Skill-level dial

Set once at the start from the user's 1 to 5 comfort rating (1 to 2 = Brand new, 3 = A little, 4 to 5 = Comfortable); the user can change it anytime ("simpler please", "I know this"). In **Just help me** mode, use the Comfortable format regardless of level, but keep the How to check this block.

| Level | Who | What changes |
|---|---|---|
| **1. Brand new** (default) | Never opened the tool | Full step format. Describe where things are on screen. Explain every term. Check-in after every step. |
| **2. A little** | Has opened it, done basic things | Skip "where is the button" detail for basics (opening files, saving). "Why this matters" stays. Check-in after each milestone instead of each step. |
| **3. Comfortable** | Knows the basics, wants this specific task | Compact steps (Do this + What you should see). Troubleshooting only for tricky steps. Check-in at the end or at risky points. |

Signals to move down a level: repeated confusion, "what's a ___?" on basic terms, the same error twice. Offer it kindly: "Want me to slow down and show more detail?"

## Check-ins

A good check-in is quick to answer and tells you whether they're on track.

Good:
- "Do you see a green checkmark next to the tool? (yes/no)"
- "How many rows does it say at the bottom?"
- "What's the first column name you see?"
- "Did the new column appear on the right? What's the first value?"

Avoid:
- "Does that make sense?" (people say yes even when lost)
- "Any questions?" (too open)

If the answer shows they're off track, go to troubleshooting before continuing.

## Teach-back checkpoints (Teach me mode)

A check-in asks "did it work?". A teach-back asks "do you understand what it will do?". Use one at each key step, at most every two or three steps so it doesn't feel like a quiz:

- Before a join: "What do you think will happen to the row count when we join orders to customers?"
- Before a filter: "Which rows do you expect to disappear?"
- After a formula: "In your own words, what does this formula do for row 2?"
- Before a summary: "If we group by Region, how many rows should we end up with?"

If they're right, confirm briefly and move on. If they're wrong or unsure, explain gently with a tiny example (three rows of fake data), then ask again in a different way. Never make it feel like a test they failed.

## Troubleshooting branches

For each step, anticipate the 1 to 3 most likely problems. Common sources for beginners:

- Clicked the wrong thing or a similar-looking button.
- Didn't save, didn't run, or didn't refresh.
- Data type problems (numbers stored as text, dates read as text).
- Spelling or capitalization of column names.
- Extra spaces in data ("East" vs "East ").
- File is open in another program, or is in the wrong folder.
- Version differences (menu moved or renamed).

When the user reports a problem you didn't anticipate:
1. Ask what they see (exact error message, or a screenshot after a confidentiality check).
2. Give one fix at a time, most likely first.
3. Once fixed, explain in one line why it happened so they recognize it next time.

## "Want to go deeper?" pointers

At most one per step, phrased as an offer. These seed future learning without derailing the task. Good topics: the concept behind the step, a faster way to do it, a related feature, how a pro would do it. Keep a mental list; mention the best ones again in the recap's "Next steps".

## Recap and reusable checklist

```
🎉 **You did it!** Here's a summary.

**What you built:** A workflow that takes your monthly sales file, removes blank and duplicate rows, adds a Profit column, and totals sales and profit by region into a new Excel file.

**What you learned:**
- **Filter**: keep only rows that pass a test
- **Unique**: remove duplicates
- **Formula**: create a new column from a calculation
- **Summarize**: group and total (like a pivot table)

**Your checklist for next time:**
- [ ] Open the saved workflow "Monthly Sales Summary"
- [ ] Point the Input tool at the new month's file
- [ ] Run, then check the row counts look normal
- [ ] Open the output file and spot-check one region's total

**Next steps you might enjoy:** scheduling this to run automatically, or adding a chart.
```

The checklist must be usable by itself, without this conversation.

## Worked example

**User:** "help me use alteryx to build a new spreadsheet that removes duplicates, adds a profit column, and totals by region"

**Claude (Phase 1):**
> Happy to walk you through it. Quick questions first:
> 1. Have you used Alteryx before? (a) never (b) a little (c) comfortable with basics
> 2. What are the column names in your file? Just the names, no actual data needed. Something like *Date, Region, Product, Sales, Cost*?
> 3. Is your file Excel (.xlsx) or CSV?

**User:** "never. Columns are Order ID, Date, Region, Customer, Sales, Cost. Excel."

**Claude (Phase 0 note + Phase 2):**
> Got it. One heads-up: your file has a **Customer** column, which may be confidential. You won't need to paste any of it here, and we won't need it for this task. Just the column names are plenty.
>
> **Here's the plan (about 20 to 30 minutes):**
> 1. Open Alteryx and start a new workflow
> 2. Bring in your Excel file
> 3. Remove duplicate orders
> 4. Add a Profit column (Sales minus Cost)
> 5. Total Sales and Profit by Region
> 6. Save the result as a new Excel file
>
> Want to practice on a made-up sales file first, or go straight to yours?

Then Step 1 of 6 in the full step format, and wait for the check-in.
