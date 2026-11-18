# Playbook: Writing a data request to IT or the data team

## What it is
A short, clear ask to the people who own the data, so you get the right data, at the right level of detail, with the right permissions, the first time.

## When to use it
You don't have access to the data, don't know where it lives, need a new extract or report, or need permission to use data in a new way.

## Why it matters
Vague requests ("can I get sales data?") lead to back-and-forth, the wrong data, or more sensitive data than you need. A good request is faster and safer.

## Steps
1. **Start from the question,** not the data: "I need to find out why repeat purchases dropped in Q3."
2. **Teach-back:** "What's the smallest set of columns that would answer that?" Ask for **only what you need** (least privilege). Often aggregated or anonymized data is enough, and gets approved faster.
3. **List the fields** you need, in plain words. Don't guess table names; the data team knows them.
4. **Define the scope:** time period, filters (regions, products), level of detail (one row per order? per customer per month?).
5. **Say how you'll use it:** one-off analysis, recurring report, shared with whom.
6. **Say how sensitive you expect it to be** and ask whether anonymized data would work. Ask what handling rules apply.
7. **Give a deadline and why** ("for the 15 March leadership review").
8. **Offer a call** if it's complicated.

Use the **Data request** template in `../output-templates.md`.

## Common mistakes
| Mistake | Fix |
|---|---|
| "Send me everything" | Ask for the specific columns and period |
| Asking for names/emails when IDs would do | Ask for IDs or anonymized data |
| No definition of terms ("active customer") | Define it, or ask how they define it |
| No deadline or purpose | Include both; it helps them prioritize |
| Getting data by an unofficial route (a colleague's export) | Use the official process; it protects you |

## How to check this (when the data arrives)
- Row count and date range match what you asked for.
- Totals roughly match a known report ("Q3 revenue in the finance pack was about X").
- Only the fields you requested are included. If you received more sensitive data than you asked for, tell the data owner and don't use the extra fields.

## Practice exercise
User's stakeholder asks "why are our best customers leaving?" Have the user draft a data request with the template. Check it for: a clear question, minimum fields, a definition of "best customer" and "leaving", period, sensitivity, deadline.
