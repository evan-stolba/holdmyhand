# holdmyhand

A Claude skill that walks non-technical people through data analysis, spreadsheets, reports and business problems, one small step at a time, while keeping confidential company information out of the conversation.

## What it does

- **Teaches from scratch.** Turns a request like *"help me use Alteryx to build a new spreadsheet that removes duplicates, adds a profit column and totals by region"* into a roadmap and then one step at a time, each with what to click, why it matters, what you should see, common fixes, and a check-in before moving on.
- **Adjusts to your level.** Brand new, a little experience, or comfortable with the basics.
- **Explains jargon** in plain English the first time it comes up.
- **Ends with a recap** and a reusable checklist so you can do it again on your own.
- **Protects confidential data.** Spots personal info, financials, client names and credentials, warns before they're used, and teaches simple ways to anonymize. It asks for column names, not your actual data.
- **Sorts data by sensitivity first** (Public, Internal, Confidential, Restricted). For Restricted data it never asks to see it: it writes steps, queries or scripts with placeholders like `[CLIENT_A]` that you fill in and run on your own computer.
- **Checks its own work.** Before finishing, it lists what it assumed and gives you 2 to 3 quick checks to run on your real data.
- **Fits the audience:** executive takeaways for business readers, commented code with validation checks for analysts, `.env.example` files and rollback steps for technical tasks.
- **Frames business questions** ("why are sales down?", "are we on track?", "is this worth it?") with ready-made templates.
- **Lets you practice on fake data** first, with sample files included.
- **Works across tools:** Alteryx, Excel, Google Sheets, Power BI and SQL, with the same approach for others.

## Files

```
holdmyhand/
├── SKILL.md                         Core instructions (plain Markdown, portable)
├── references/
│   ├── confidentiality.md           4 sensitivity tiers, hard stops, placeholders, local mode
│   ├── teaching-method.md           Step format, skill dial, check-ins, teach-back, recap
│   ├── output-standards.md          Output by audience + "How to check this"
│   ├── output-templates.md          Step-by-step guide, analysis summary, data request, handoff doc
│   ├── business-templates.md        10 business-question templates + business/technical translation
│   ├── glossary.md                  Plain-English definitions
│   ├── sample-data.md               Practice data guide
│   ├── playbooks/                   9 "first time doing X" playbooks
│   │   ├── sql-joins-and-aggregation.md   ├── pivots-and-lookups.md
│   │   ├── data-cleaning.md               ├── forecasting-basics.md
│   │   ├── ab-test-interpretation.md      ├── first-dashboard.md
│   │   ├── data-request.md                ├── first-pandas-script.md
│   │   └── reading-an-error.md
│   └── tools/                       Alteryx, Excel/Sheets (with version table), Power BI/Tableau, SQL (dialects)
├── scripts/
│   ├── redact.py                    Local redaction tool (Python, no installs)
│   ├── redact.html                  Same tool as an offline web page (no Python needed)
│   └── README.md
├── assets/                          Fictional practice CSVs (sales, customers, targets)
├── adapters/                        Setup for Gemini (Gems, GEMINI.md) and ChatGPT (GPTs, custom instructions)
└── tests/                           15 behavior scenarios with pass/fail criteria, results, fixtures
```

## Install

Other assistants: see `adapters/README.md`.


- **Claude.ai / Claude app:** zip the `holdmyhand` folder and upload it under Settings > Capabilities > Skills.
- **Claude Code:** copy the folder to `~/.claude/skills/holdmyhand/` (personal) or `.claude/skills/holdmyhand/` in a project.

## Try it

> "Help me use Excel to make a summary of sales by region. I've never used pivot tables."

> "Our customer complaints went up last month. How do I figure out why?"

## A note on confidentiality

The skill reduces the chance of sharing sensitive data, but it can't guarantee it. Always follow your company's policy on using AI tools with company data.

All sample data is fictional.

## Testing

`tests/test-scenarios.md` has 15 behavior scenarios with pass/fail criteria, including privacy cases (a pasted customer list, an API key in an error message, HR data). `tests/results-2026-11-18.md` records the first runs in Claude. If you adapt the skill, re-run the privacy scenarios before you share it.

## License

MIT. See `LICENSE`.

This project is provided as is, with no warranty. It's a teaching aid, not a data-protection or compliance tool.
