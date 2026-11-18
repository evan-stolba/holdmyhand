# Local redaction tools

Two tools that do the same job: make a **safe copy** of a data file before you share anything with an AI tool. Both run only on your computer and never upload anything.

| | `redact.py` | `redact.html` |
|---|---|---|
| Needs | Python 3.8+ (no installs) | Any modern web browser |
| Files | CSV, TSV, Excel .xlsx (output as CSV), JSON, any text/log file | CSV/TSV and text (paste or open) |
| Extras | Dry-run preview, schema-only summary, synthetic sample rows, optional private mapping file | Schema-only summary |
| Network | No network code | Page is locked by a security policy that blocks all connections |

> **Best effort only.** Both tools print a reminder every run: they can miss names written in sentences, ID formats they don't know, and non-standard layouts. Always read the output before sharing.

**Same secret, same tokens.** Both tools use the same method (HMAC-SHA256 with your private secret), so `Acme Corp` becomes the same `CUSTOMER_xxxxxxxx` token in every file, and joins still work. Paste the contents of your Python secret file into the HTML page's "Secret phrase" box to get identical results.

## What gets replaced

**Columns, by their name:** customer/client/company names and IDs, person names, managers and reps, employee IDs, emails, phones, addresses, dates of birth, IP addresses, health fields, user IDs, bank accounts. Values become tokens like `CUSTOMER_0E414ADA`.

**Always fully removed** (no token): passwords, keys and tokens (`[REDACTED_SECRET]`), card numbers (`[REDACTED_CARD]`), SSNs and government IDs (`[REDACTED_ID]`).

**Flagged but kept:** salary/pay columns, because they're often what you're analyzing. Use `--columns Salary` to replace them, or round them first.

**Found anywhere in text:** emails, phone numbers, US SSNs, UK National Insurance numbers, UK postcodes, card numbers (Luhn-checked), IBANs, IP addresses, API keys, `password=...` style secrets, `user:pass@` in URLs, and file paths that reveal usernames.

**Your own ID formats:** `--pattern "EMP-\d{5}"` (repeatable) replaces anything matching that pattern, for company IDs the tool doesn't know.

**Free-text columns:** the report marks columns that look like sentences (notes, comments, descriptions) with a FREE TEXT warning, because names inside sentences are easy to miss. If you don't need the column, remove it with `--drop "Notes"`.

**Your own list:** put client names, project code names, etc. in a text file (one per line) and pass `--terms list.txt` (or the "Extra names" box in the HTML page).

## Your secret, and when to use numbered tokens

- `redact.py` creates a random 256-bit secret the first time it runs (`~/.holdmyhand_secret`). There is no built-in default secret. It warns you if other users on the computer can read the file.
- The HTML page has no default either: it requires at least 12 characters, and has a **Generate** button for a strong random secret.
- **Why it matters:** tokens are a keyed hash. Without the secret, nobody can reverse them. But someone who **has** your secret and can guess the possible values (all employee IDs from 1 to 5000, a list of client names) could hash each guess and match the tokens. So keep the secret private, and don't share it alongside redacted files.
- **Numbered tokens** (`--sequential`, or the checkbox in the HTML page) give `CUSTOMER_001`, `CUSTOMER_002`… for that run only. They can't be reversed or matched across files, even with the secret. Use them whenever you don't need to join files.

## What it can't do (read this)

- It **can't reliably find names written in sentences** ("call Jane about the renewal"). Use `--terms`, or remove free-text comment columns entirely if you don't need them.
- Business-sensitive numbers (prices, margins, revenue) are **kept**, since they're usually the point of the analysis. Aggregate, round, or scale them if they're confidential.
- Detection is pattern-based, so it can miss unusual formats and occasionally replace harmless values (a long product number that looks like a card number).
- Excel dates come out as serial numbers (e.g. 45292). Format them as dates in Excel before saving as CSV, or convert after.
- **Always open the result and read it before sharing.** Your company's policy comes first.

## Python quick start

```bash
python redact.py customers.csv --dry-run                  # preview, writes nothing
python redact.py customers.csv                            # writes customers.redacted.csv
python redact.py sales.xlsx --sheet "Q3"                  # writes sales.Q3.redacted.csv
python redact.py orders.csv --schema-only                 # column names, types, counts: no values
python redact.py orders.csv --synthetic 5                 # 5 fake rows with the same columns
python redact.py notes.txt --terms clients.txt            # replace listed names everywhere
python redact.py orders.csv --columns "Region" --keep "Product"
python redact.py orders.csv --mapping                     # ALSO writes a private token->original file
python redact.py tickets.csv --drop "Notes"               # remove a free-text column entirely
python redact.py hr.csv --pattern "EMP-\d{5}"             # also replace your own ID format
python redact.py one_off.csv --sequential                 # numbered tokens, not linkable
```

On Windows, use `py` instead of `python` if `python` isn't found.

- Your secret is created automatically at `~/.holdmyhand_secret` (change with `--secret-file`). Keep it private; reuse it for consistent tokens.
- The original file is never changed, and existing outputs aren't overwritten without `--force`.
- **No mapping file unless you ask** (`--mapping`). If you create one, it can turn tokens back into real values: store it securely, never share it, delete it when done.

## HTML quick start

1. Double-click `redact.html` to open it in your browser (no internet needed).
2. Open a file or paste the data.
3. Type a secret of at least 12 characters or click **Generate** (save it somewhere private to reuse), or tick **numbered tokens** if you don't need to join files.
4. Click **Make safe copy**, read the result, then **Download** or **Copy**.

## Which output should I share?

Safest first:
1. **Schema only**: column names, types, counts. Enough for most "how do I…" questions.
2. **Synthetic rows**: fake data with the same shape, for showing an example.
3. **Redacted copy**: when the AI really needs to see the pattern of real values.
4. **Aggregates**: totals and percentages, when the numbers themselves matter.
