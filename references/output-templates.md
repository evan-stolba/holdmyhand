# Output templates

Consistent formats so results look professional and repeatable. Offer the right one at the end of a task ("Want me to put this into a handoff doc?"). Fill them with placeholders, never real confidential values; the user fills those in on their own computer.

## Contents
- 1. Step-by-step guide
- 2. Analysis summary (includes the 3-bullet executive summary)
- 3. Data request
- 4. Handoff doc
- Assumption and decision log format

---

## 1. Step-by-step guide
For: a process the user (or a colleague) will repeat.

```markdown
# How to [task], in [tool and version]

**What this does:** [one sentence]
**Time needed:** [about X minutes]
**You'll need:** [files, access, tool version]
**Data sensitivity:** [Public / Internal / Confidential / Restricted] (handle per company policy)

## Steps
1. [Action] ... **You should see:** [result]
2. ...

## How to check it worked
- [ ] [check 1, e.g. row count about the same as last month]
- [ ] [check 2, e.g. grand total matches the finance report]

## If something goes wrong
| Problem | Fix |
|---|---|
| ... | ... |

_Last updated: [date] by [name]_
```

## 2. Analysis summary
For: answering a business question for a manager or stakeholder.

```markdown
# [The question, e.g. Why did Q3 sales fall?]

## Executive summary
- **Takeaway:** [one sentence answer]
- **Why it matters:** [impact in money, time, customers, risk]
- **Recommended action:** [one next step and owner]

## Key numbers
| Metric | This period | Comparison | Change |
|---|---|---|---|
| [KPI] | ... | vs [last period / target] | ... |

## What we looked at
[Data sources, period, filters, in plain English. 2 to 3 lines.]

## Assumptions and caveats
- [assumption 1]
- [what the data can't tell us]

## Options and trade-offs (if a decision is needed)
| Option | Upside | Downside | Effort |
|---|---|---|---|

## How this was checked
- [e.g. totals reconciled to finance report within 1%]
```

The **3-bullet executive summary** (takeaway, why it matters, action) can stand alone for a chat message or email. Rules: no jargon, numbers rounded, the takeaway readable in five seconds.

## 3. Data request
For: asking IT or a data team for data or access. See `playbooks/data-request.md`.

```markdown
**Subject:** Data request: [short description], needed by [date]

**The question I'm trying to answer:** [one or two sentences]

**Data needed (minimum):**
| Field (plain words) | Why I need it |
|---|---|
| [e.g. order date] | [to see the trend by month] |

**Scope:** [time period], [filters], [level of detail: one row per ___]
**Use:** [one-off analysis / recurring report], shared with [who]
**Sensitivity:** I expect this to be [tier]. Anonymized or aggregated data is fine if it's easier to approve: [yes/no]. Please let me know any handling rules.
**Format:** [CSV / Excel / access to a table or dashboard]
**Deadline:** [date], for [reason]

Happy to jump on a quick call if that's easier.
```

## 4. Handoff doc
For: passing work to a colleague, a manager, or an auditor, or to your future self.

```markdown
# Handoff: [project or analysis name]

**Owner:** [name] | **Date:** [date] | **Status:** [done / in progress]
**Sensitivity:** [tier]; where the data lives: [location placeholder]

## What this is
[2 to 3 sentences: the question, what was built]

## How to run or update it
1. [steps, or link to the step-by-step guide]

## Inputs and outputs
| Input / output | Location | Refresh |
|---|---|---|

## Assumption and decision log
| # | Date | Assumption or decision | Why | Impact | Confirmed by |
|---|---|---|---|---|---|

## Checks
- [checks that were run and their result]
- [checks to run each time it's refreshed]

## Known issues and next steps
- ...
```

---

## Assumption and decision log format

Keep a running list throughout the task, update it at milestones, and drop it into the handoff doc.

| # | Assumption or decision | Why | Impact | Confirmed? |
|---|---|---|---|---|
| 1 | Sales are before tax | Column description says "net" | Totals exclude ~8% tax | Asked finance: pending |
| 2 | Removed 6 duplicate orders | Same OrderID twice | Sales total down by $X | Yes, user agreed |
| 3 | Treated blank Sales as excluded, not 0 | Unknown amounts | 3 rows excluded | Yes |

Rules: write it in plain English; record decisions the user made, not just yours; mark which ones are still unconfirmed. This builds trust with managers and auditors.
