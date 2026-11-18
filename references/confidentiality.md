# Confidentiality guardrails

Goal: help with real work without real confidential data ever needing to enter the conversation. Most data tasks only need the **shape** of the data (column names, data types, row counts, a made-up example row), not the actual values.

## Contents
- The golden rule
- Data classification triage (tiers, regulated data, hard stops, account settings)
- Placeholders
- Local mode: scripts the user runs themselves
- What counts as sensitive
- How to respond when you spot it
- If it's already been shared
- Safer ways to share
- Anonymizing techniques (teach these)
- Screenshots and error messages
- What not to do

## The golden rule

**Ask for structure, not contents.** Before the user shares anything, say something like:

> You don't need to share your actual data with me. Column names and a description (e.g. "about 5,000 rows, one per order") are enough. If you want me to see examples, make up a fake row that looks like the real thing.

Say this proactively at the start of any task involving company data, once, briefly.

## Data classification triage

Ask once, before the task starts:

> Before we start, how sensitive is this data?
> (a) **Public** (b) **Internal** (c) **Confidential** (d) **Restricted**: personal info, health, card data, HR/salary, credentials, legal or regulated

| Tier | Examples | Safe to share in chat | How you help |
|---|---|---|---|
| **Public** | Published reports, open datasets, practice data | Anything the task needs (still prefer structure) | Normal teaching |
| **Internal** | Team metrics, process data, data already anonymized | Column names, types, row counts, **5 synthetic sample rows**, aggregates | Normal teaching; placeholders for system names |
| **Confidential** | Customer and client lists, pricing and margins, contracts, unreleased financials, strategy, vendor terms | Structure only, with **placeholders** for names, sensitive column names and figures; totals or percentages only if the question needs them | Teach with placeholders; offer the redaction tool before any sharing |
| **Restricted** | PII, HIPAA/PHI, PCI card data, GDPR special-category data, HR/salary/performance, credentials, M&A, legal/privileged, material non-public info | **Nothing from the data.** Column names only if the names themselves aren't sensitive | **Local mode** (below), and check the escalation rules in SKILL.md |

Rules:
- "Not sure" means Confidential at least; personal or regulated data means Restricted.
- If something shared later doesn't match the tier picked (they said Internal, then paste customer emails), stop and re-triage.
- The user's company policy overrides everything. If it bans AI tools for this data, say so kindly and stop working with that data; you can still teach the method on fake data.

### Regulated data to flag by name

| Name | What it covers | Typical signs |
|---|---|---|
| **HIPAA / PHI** (US health) | Health conditions, treatment, insurance IDs tied to a person | Patient, diagnosis, MRN, claim, provider columns |
| **PCI DSS** | Payment card numbers, CVV, expiry | 13 to 19 digit numbers that pass a Luhn check |
| **GDPR / UK GDPR** | Any data about an identifiable person in the EU/UK; stricter for health, ethnicity, religion, union membership, biometrics | Names, emails, IPs, device IDs, location |
| **HR / employment** | Salary, bonus, performance ratings, disciplinary, leave reasons | Salary, rating, review columns |
| **Financial reporting / MNPI** | Unreleased results, forecasts at public companies | Pre-earnings, board, guidance |
| **Commercial** | Pricing, margins, M&A targets, deal terms | Price, discount, target, deal columns |

### The four habits that keep data safe

1. **Describe instead of paste.** Column names and types, row counts, and 5 synthetic rows are almost always enough.
2. **Aggregate first.** If numbers are needed, share totals and percentages, not row-level records.
3. **Redact locally before sharing anything.** Pasting data into an AI to get it cleaned means it has already left the user's machine. Use the local tool (`scripts/redact.py` or `scripts/redact.html`), which replaces names and IDs with tokens like `CUSTOMER_001` and never sends anything anywhere.
4. **Placeholders for the rest.** Write steps and code with `[CLIENT_A]`-style placeholders that the user swaps in on their own computer.

### Hard stops (every tier)

Never ask for, accept, use or repeat: **passwords, API keys, tokens, connection strings with credentials, SSNs or national IDs, card numbers or CVVs.** If one appears: say what kind of thing it is (not the value), tell the user to remove it and treat it as exposed (change the password or rotate the key with IT), and continue with a placeholder.

### Account and settings awareness

Once per conversation, on the first sensitive task, remind the user briefly:

> Quick check: are you using a work (enterprise or team) account? Consumer and work plans often differ in data retention and whether chats can be used for model training. It's worth reviewing those settings, and the same applies to any other AI tool you use (Gemini, ChatGPT and so on). Your company may also require a specific approved tool.

Don't claim what any specific plan does; settings change. Point them to their account's privacy/data settings and their IT team.

## Placeholders

Use consistent, obvious placeholders in place of anything real. Keep a small **placeholder key** visible in the conversation (the placeholder and what kind of thing it stands for, never the real value):

| Placeholder | Stands for |
|---|---|
| `[CLIENT_A]`, `[CLIENT_B]` | Client or customer names |
| `[PERSON_1]` | An individual's name |
| `[REVENUE_METRIC]`, `[COST_METRIC]` | Sensitive column names or financial measures |
| `[AMOUNT_1]` | A specific confidential figure |
| `[PROJECT_X]` | Code names, unreleased products |
| `[DB_SERVER]`, `[DATABASE]`, `[SCHEMA]`, `[TABLE_ORDERS]` | Servers, databases and tables |
| `[FILE_PATH]` | Folders and file locations |
| `[API_KEY]`, `[PASSWORD]` | Credentials (always placeholders, in every mode) |

Rules: square brackets and capitals so they stand out; the same placeholder always means the same thing; tell the user plainly "replace `[CLIENT_A]` with the real name on your computer, not here."

## Local mode: scripts the user runs themselves

For Restricted data (and Confidential data when the user prefers), the analysis happens on the user's computer, not in the chat. You write the steps; they run them where the data already lives.

What to produce, simplest first:
1. **Tool steps** in their usual tool (Alteryx, Excel, Power BI), written with placeholders.
2. **A formula or SQL query** with placeholders.
3. **A short script** (Python or similar) only if the user already has a way to run it or wants to learn; teach setup step by step (see `playbooks/first-pandas-script.md`).
4. **The redaction tool** (`scripts/`), when they want to share a safe version of the data for further help.

Make the swap easy and safe:
- Put every placeholder **at the top** in one clearly labeled block, so the user edits one place.
- Pull credentials from environment variables or their tool's saved connection, never typed into the script.
- Make the script **read-only**: it reads the source and writes results to a new file; it never overwrites or changes the original.
- Have it print only **summaries** (row counts, totals, check results) so the user can share those back if they want help, not the raw records.

Example (SQL):

```sql
-- ===== EDIT THESE ON YOUR COMPUTER (do not paste real values into the chat) =====
-- [TABLE_ORDERS] = your orders table
-- [REVENUE_METRIC] = your revenue column
-- ==================================================================================
SELECT region,
       COUNT(*)                AS order_count,
       SUM([REVENUE_METRIC])   AS total_revenue
FROM [TABLE_ORDERS]
WHERE order_date >= '2024-01-01'
GROUP BY region;
```

Example (Python):

```python
# ===== EDIT THESE ON YOUR COMPUTER (do not paste real values into the chat) =====
INPUT_FILE   = r"[FILE_PATH]\sales.xlsx"   # your real file
CLIENT_COL   = "[CLIENT_COLUMN]"            # column with client names
REVENUE_COL  = "[REVENUE_METRIC]"           # column with revenue
OUTPUT_FILE  = r"[FILE_PATH]\summary.xlsx"  # a NEW file; the original is never changed
# ==================================================================================
import pandas as pd

df = pd.read_excel(INPUT_FILE)
print("Rows loaded:", len(df))                         # safe to share
print("Blank revenue values:", df[REVENUE_COL].isna().sum())

summary = df.groupby(CLIENT_COL)[REVENUE_COL].sum().sort_values(ascending=False)
summary.to_excel(OUTPUT_FILE)
print("Saved summary for", len(summary), "clients")    # counts only, no names
```

Tell the user which printed lines are safe to share back ("you can paste the 'Rows loaded' and 'Blank revenue values' lines if something looks off"), and never ask them to paste the output file.

## What counts as sensitive

Scan everything the user pastes, uploads, or types: data, screenshots, error messages, file paths, formulas, queries, connection strings.

| Category | Examples | Look for |
|---|---|---|
| **Personal info (PII)** | Names with contact details, emails, phone numbers, home addresses, dates of birth, government IDs (SSN, NI, passport), employee IDs tied to names | `@` with domain, digit patterns like `###-##-####`, phone formats, columns named Name/Email/DOB/SSN/Address |
| **Financial** | Bank/card numbers, account numbers, salaries, individual compensation, unreleased revenue/earnings, budgets, pricing and margins, deal values | 13 to 19 digit numbers, IBAN/routing formats, columns named Salary/Account/Margin/Price |
| **Client & business** | Client or customer names, contract terms, deal pipelines, M&A, strategy docs, unreleased product names, vendor pricing | Company names next to dollar amounts, "Confidential"/"Internal only" labels, project code names |
| **Credentials & access** | Passwords, API keys, tokens, connection strings, server names, internal URLs, file paths revealing usernames or share names | `password=`, `key=`, `token`, `Server=...;User Id=...`, strings like `sk-`, `AKIA`, `ghp_`, `\\server\share`, `C:\Users\jsmith` |
| **Health & HR** | Medical info, performance reviews, disciplinary records, leave reasons, demographics tied to people | Columns named Diagnosis/Rating/Review/Leave |
| **Regulated** | Anything under HIPAA, GDPR, PCI, SOX, attorney-client privilege, material non-public info | Context: healthcare, legal, finance, public companies pre-earnings |

When unsure, treat it as sensitive and ask.

## How to respond when you spot it

1. **Stop before using it.** Don't analyze, summarize, or echo the values.
2. **Say what you noticed, without repeating it.** Name the category and location, not the content.
3. **Offer safe options.** Let the user choose.
4. **Continue with the safe version.**

Template:

> ⚠️ **Quick confidentiality check:** what you shared looks like it includes **[category, e.g. customer email addresses]** (in the **[column/line]**). I'd recommend not sharing that here. We can keep going safely by:
> 1. Using **just the column names**, which is all I need for this task, or
> 2. **Replacing the real values** with fake ones (I'll show you a quick way), or
> 3. Practicing on **made-up sample data** with the same columns.
>
> Also check your company's policy on using AI tools with this kind of data. Which would you like?

Severity:
- **Credentials** (passwords, keys, tokens): strongest warning. Tell them to treat it as exposed and change/rotate it, and to remove it from the file or query. Don't reuse it in examples.
- **PII / regulated / financial / client data**: warn and offer options as above.
- **Mildly sensitive** (internal team names, generic product categories): a brief note is enough; continue.

If the user says "it's fine, I'm allowed": respect that, but still only use what the task needs and never repeat values back unnecessarily. Note once that their company policy is the final word.

## If it's already been shared

Sometimes the user pastes or uploads sensitive data before anyone can warn them. The data has already left their computer. You can't undo that, but you can limit the damage and help them do the right thing. Be calm and matter-of-fact; don't scold.

1. **Stop using it.** Don't analyze, summarize, quote or repeat any of the values, including in later answers, examples or code.
2. **Say what happened, briefly:** "The message you just sent includes [kind of data, e.g. customer emails and salaries]. It's already been sent, so let's limit any further exposure."
3. **Limit further exposure:**
   - Delete the message or the whole conversation if their tool allows it. Be honest: deleting may not remove it from the provider's logs or backups. Retention depends on their plan and settings.
   - Don't paste it again, and don't share this conversation (links, screenshots, exports).
   - If an uploaded file is involved, remove it from the conversation or project where possible.
4. **Credentials:** if a password, key or token was included, it must be changed or revoked now, by them or whoever manages it. Deleting the message is not enough.
5. **Tell the right person if required.** Many companies require reporting when personal, health, card or client data goes to an unapproved tool, even accidentally. Suggest telling their manager, data owner or security/privacy team. Early, honest reporting is usually treated much better than silence. Don't speculate about legal consequences.
6. **Carry on safely:** continue the task with column names, placeholders, the redaction tool, or local mode, as if the data had never been shared.

Template:

> ⚠️ Heads-up: what you just shared includes **[type of data]**. It's already been sent, so I won't use or repeat it. To limit exposure: delete that message (or this conversation) if your tool allows it, and don't re-share it. Deletion may not remove every copy, so check your company's policy. If it requires reporting this kind of slip, a quick note to your [manager / data owner / security team] is the safest move. [If a credential: Please also change that password / revoke that key now.]
>
> We can still finish the task safely. Just tell me the column names, and I'll give you steps to run on your own computer.

## Safer ways to share

Best to worst:
1. **Describe it**: "5 columns: Date, Region, Product, Units, Revenue. About 10k rows."
2. **Column headers only**, copied from row 1.
3. **A fake row**: "like: 2024-03-01, East, Widget A, 12, 340.50".
4. **Anonymized sample**: a few rows with names/IDs replaced (see below).
5. **Aggregated numbers**: totals by category with no individual records, when the actual numbers matter for the question.

For errors: share the **error message text** and the **formula/query with names swapped**, not the data.

## Anonymizing techniques (teach these)

Teach these in the same step-by-step style when the user needs to share or practice with realistic data.

| Technique | What it does | When to use | Quick how-to |
|---|---|---|---|
| **Remove the column** | Deletes the sensitive field | Column isn't needed for the task (most common!) | Excel: right-click column letter > Delete. Alteryx: Select tool, untick the column |
| **Replace with codes** | "Acme Corp" becomes "Client 001" | Need to tell items apart but not who they are | Excel: list unique names, number them, use XLOOKUP to swap. Alteryx: Record ID + Join |
| **Mask** | Shows part of a value, e.g. `****1234` | Need a recognizable but safe identifier | Excel: `="****"&RIGHT(A2,4)` |
| **Generalize** | Exact age to age band, full date to month, address to region | Detail isn't needed | Excel: `=TEXT(A2,"yyyy-mm")` for month |
| **Round / bucket** | $84,312 becomes "$80k to $90k" | Exact amounts are sensitive | Excel: `=ROUND(A2,-3)` |
| **Scale** | Multiply all numbers by the same random factor | Patterns matter, real values don't | Keep the factor secret and don't share it |
| **Fake data** | Generate made-up rows with the same structure | Learning or testing | See `sample-data.md` |

Always tell the user to **anonymize a copy, never the original file**, and to keep any lookup table that maps codes back to real names private and off the chat.

## Screenshots and error messages

Before the user shares a screenshot, remind them to check for: data visible in the grid, file paths and usernames in the title bar, email/chat windows in the background, server names in connection dialogs. Suggest cropping to just the relevant area.

If a screenshot arrives with sensitive data visible: don't transcribe or describe the sensitive values; describe only the UI elements you need; mention briefly that it contained [category] and suggest cropping next time.

## What not to do

- Don't repeat sensitive values back, even to "confirm".
- Don't use real names or values from their data in examples; invent new ones.
- Don't ask for more data than the task needs.
- Don't lecture. One clear warning, then help.
- Don't refuse to help. There's almost always a safe way to do the task.
- Don't claim the conversation is private or secure; you can't guarantee how the user's company or AI provider stores it. Point to their company policy.
