# Business question templates

Use these when the user brings a business question or problem rather than a tool task. Each template turns a vague question into a clear plan: what to find out, what data is needed, what analysis to run, and how to present the answer. Then hand off to the step-by-step teaching method for the actual build.

## Contents
- How to use a template
- 1. Why did this number change?
- 2. How are we performing against target?
- 3. Who / what are our top and bottom performers?
- 4. What's the trend, and where is it heading?
- 5. Which segments behave differently?
- 6. Is this worth doing? (cost / benefit)
- 7. Where is the process slowing down?
- 8. Is the data clean enough to trust?
- 9. Build a recurring report
- 10. General problem-solving (non-data)
- Translating between business and technical

## How to use a template

1. **Match** the user's question to a template (or two). Say which one: "This sounds like a 'why did this number change?' question."
2. **Fill in the framing questions** with the user, a few at a time.
3. **Confirm the data needed**, by column names only (see `confidentiality.md`).
4. **Show the analysis plan** as a roadmap, then teach it step by step in their tool.
5. **Help them present the answer**: one headline sentence, supporting numbers, a simple chart, and caveats.

The answer format for every template:

> **Headline:** one sentence a manager could read in 5 seconds.
> **Key numbers:** 2 to 4 supporting figures.
> **Chart:** the one visual that best shows it.
> **Caveats:** what the data can't tell us.
> **Next step:** the decision or follow-up this points to.

---

## 1. Why did this number change?
*"Why are sales down this month?" "Why did costs jump?"*

**Framing questions**
- Which number, compared to when? (this month vs last month? vs same month last year?)
- How big is the change, and is it unusual compared to normal ups and downs?
- Any known events? (price change, new product, holiday, system change)

**Data needed:** the metric by date, plus the dimensions that might explain it (region, product, channel, customer type).

**Analysis**
1. Confirm the change is real: check data completeness (is a week missing?).
2. Compare the two periods side by side.
3. **Break it down** by each dimension: which region/product/channel accounts for most of the change? (This is called a variance or "bridge" analysis.)
4. Split into **volume vs price/rate** if relevant: fewer orders, or smaller orders?
5. Look for one-offs: a single huge order last month, a returns spike.

**Chart:** waterfall (bridge) chart from old total to new total, or bar chart of change by segment.

## 2. How are we performing against target?
*"Are we on track for the quarter?"*

**Framing questions:** what's the target and the period? Is the target split by month/team? What counts as "on track" (within 5%?)?

**Data needed:** actuals by date and team/segment; targets by the same breakdown.

**Analysis:** actual vs target, difference and % of target; year-to-date and run-rate projection (current pace times remaining time); flag segments furthest behind.

**Chart:** bar chart of actual vs target per segment, or a line of cumulative actual vs target.

## 3. Who / what are our top and bottom performers?
*"Which products sell best?" "Which stores are struggling?"*

**Framing questions:** ranked by what measure (revenue, profit, growth, volume)? Over what period? Should we adjust for size (per store, per employee)?

**Data needed:** the measure by item/person/location.

**Analysis:** total by item, sort, top 10 / bottom 10; check concentration ("top 20% of products make 80% of revenue", the Pareto principle); compare rank by different measures, since top by revenue can be bottom by profit.

**Chart:** sorted horizontal bar chart. **Confidentiality note:** rankings of named people or clients are sensitive; use codes when sharing.

## 4. What's the trend, and where is it heading?
*"Are we growing?" "What will next quarter look like?"*

**Framing questions:** how far back does data go? Are there seasons (holiday peaks)? Is a rough projection fine or does it need to be precise?

**Analysis:** plot over time; smooth with a moving average; compare to the same period last year to remove seasonality; simple projection (Excel `FORECAST.LINEAR` or Forecast Sheet; Power BI analytics pane forecast). Explain that forecasts are educated guesses with a range.

**Chart:** line chart with actuals solid and projection dashed.

## 5. Which segments behave differently?
*"Do new customers buy differently from returning ones?" "Which regions respond to promotions?"*

**Analysis:** group by segment, compare averages/rates (average order value, conversion rate, churn rate); check segment sizes, since a small segment with a big difference may be noise; cross-tabulate two dimensions with a pivot table.

**Chart:** grouped bar chart, or a heatmap-style pivot with conditional formatting.

## 6. Is this worth doing? (cost / benefit)
*"Should we buy this software?" "Is this campaign worth it?"*

**Framing questions:** one-time and ongoing costs? Expected benefits (time saved, revenue gained, cost avoided), and how confident are we? Over what time period?

**Analysis:** simple table of costs and benefits by year; payback period (when cumulative benefit exceeds cost); ROI = (benefit minus cost) / cost; best / expected / worst case scenarios. Keep assumptions visible in their own cells so they're easy to change.

**Chart:** cumulative cost vs cumulative benefit lines; the crossing point is payback.

## 7. Where is the process slowing down?
*"Why do orders take so long to ship?" "Where do tickets get stuck?"*

**Data needed:** one row per item with timestamps for each stage (created, approved, shipped...).

**Analysis:** time between stages (date differences); average and **median** per stage (explain why median resists outliers); find the slowest stage and the worst outliers; break down by team/type.

**Chart:** stacked bar of average time per stage, or a box plot if their tool supports it.

## 8. Is the data clean enough to trust?
*Use before any of the above when the data is new or messy.*

**Checklist to teach:**
- Row count matches what's expected?
- Blanks in important columns?
- Duplicates (same ID twice)?
- Numbers stored as text? Dates as text?
- Inconsistent labels ("NY", "New York", "new york")?
- Impossible values (negative quantities, future dates, ages of 200)?
- Totals match a known source (finance report, dashboard)?

Teach a "data health" summary: count rows, count blanks per column, min/max per number column, list of unique values for category columns.

## 9. Build a recurring report
*"I make this report every week by hand."*

**Framing questions:** who reads it and what decision do they make from it? What's the source each time? What are the manual steps today?

**Plan:** document the current manual steps first (the user lists them); automate the repetitive parts in the tool (Alteryx workflow, Power Query, saved SQL query, Power BI refresh); add a check step (row counts, totals vs last period); end with the reusable checklist from the recap.

## 10. General problem-solving (non-data)
*"Our team keeps missing deadlines." "How should I prioritize these projects?"*

Walk through these, one question at a time:
1. **Define:** what exactly is the problem, and how would we know it's solved?
2. **Size:** how big is it, how often, who's affected?
3. **Causes:** brainstorm possible causes, then ask "why?" up to five times on the likeliest one.
4. **Options:** 2 to 4 possible solutions.
5. **Compare:** simple scoring table: impact, effort, risk, cost (1 to 5 each).
6. **Decide and test:** pick one, define a small trial and how to measure success.

Offer a simple matrix such as **impact vs effort** (quick wins = high impact, low effort). Keep all names of people and clients out of the conversation; use roles ("the approver", "Client A").

---

## Translating between business and technical

### Business to technical: vague request into an analysis plan
When a stakeholder says something like "why are sales down?" or "can you look into churn?", fill in this plan with the user before touching data:

| Part | Question to answer | Example |
|---|---|---|
| **Question** | What exactly do we want to know? | Did Q3 revenue fall vs Q2, and which region/product drove it? |
| **Decision** | What will someone do with the answer? | Decide where to focus the Q4 sales push |
| **Metric** | Precisely what number? | Revenue = sum of net sales by order date, excl. refunds |
| **Comparison** | Compared to what? | Q3 vs Q2, and Q3 vs Q3 last year |
| **Breakdown** | Sliced by what? | Region, product category, new vs returning customers |
| **Data needed** | Minimum fields and period | Order date, region, category, customer type, net sales; last 18 months |
| **Method** | Which template/playbook? | Template 1 (why did this change) + data-cleaning playbook |
| **Check** | How will we know it's right? | Total reconciles to finance's Q3 pack |
| **Output** | What does done look like? | Analysis summary with a waterfall chart, by Friday |

Then confirm it with the stakeholder ("Here's what I plan to look at; is this the question?"). This avoids answering the wrong question well.

### Technical to business: results into an executive summary
Turn query results or tables into three bullets (template in `output-templates.md`):
1. **Takeaway:** what happened, in one sentence with one number. ("Q3 revenue fell 8%, almost entirely in the West region.")
2. **Why it matters:** the impact. ("That's about $[AMOUNT_1] below plan, and West is our largest region.")
3. **What to do:** one recommended action. ("Review West's lost accounts with the regional lead this week.")

Then caveats in one line. Avoid jargon: "joined", "null", "p-value" become "matched", "missing", "how likely it's just chance".
