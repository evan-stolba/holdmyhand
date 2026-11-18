# Playbook: Forecasting basics

## What it is
Using past data to estimate future values, with a range of uncertainty. A forecast is an educated guess, not a promise.

## When to use it
"What will next quarter's sales be?", "how many support tickets should we staff for?", "when will we hit the target?"

## Before you start
- **How much history?** At least 2 full cycles if there's seasonality (2 years for yearly patterns, 2+ months of daily data for weekly patterns). Less than that: keep it very simple and say so.
- **Is the data clean and complete?** A missing month looks like a crash. Run the data-cleaning health check.
- **Anything unusual?** Price changes, one-off big deals, COVID-like shocks, system changes. Note them in the assumption log.
- **What will it be used for?** A rough planning number needs less precision than a budget commitment. Budgets and external guidance: see escalation rules (financial reporting).

## Steps
1. **Plot it.** A line chart of the metric over time. Ask: going up, down, flat? Repeating pattern (seasonality)? Sudden jumps?
2. **Teach-back:** "Looking at the chart, what would you guess next month will be, roughly?" Their gut number is a useful benchmark.
3. **Start with simple baselines** (explain each in one line):
   - **Last value:** next month = this month.
   - **Same period last year:** next December = last December (handles seasonality).
   - **Moving average:** average of the last 3 months.
   - **Growth rate:** last year's value times this year's growth so far.
4. **Then a tool forecast:**
   - Excel 2016+: select dates and values > **Data > Forecast Sheet** (exponential smoothing with a confidence band). Or `=FORECAST.LINEAR(target_date, values, dates)` for a straight-line trend.
   - Google Sheets: `=FORECAST(...)` or `=TREND(...)` (straight line only).
   - Power BI: line chart > **Analytics pane > Forecast**.
   - Tableau: **Analytics pane > Forecast**.
5. **Test it on the past (backtest):** hide the last 3 months, forecast them from earlier data, compare to what actually happened. This shows how wrong the method usually is.
6. **Present a range, not one number:** "Most likely about X, probably between Y and Z", plus the assumptions.

## Common mistakes
| Mistake | Fix |
|---|---|
| Straight line through seasonal data | Use same-period-last-year or Forecast Sheet (handles seasonality) |
| Forecasting from too little data | Say so; use simple baselines; widen the range |
| Including an incomplete current month | Drop it, or it looks like a drop |
| One-off events in history | Remove or adjust them, and log it |
| Presenting a single precise number | Always give a range and assumptions |
| Complex model that beats baselines by a hair | Prefer the simple one; it's easier to explain and check |

## How to check this
- Backtest error: how far off was the method on the last 3 known months?
- Does the forecast beat the simplest baseline? If not, use the baseline.
- Sanity check vs known plans: does it roughly match targets, pipeline or last year's growth?

## Practice exercise
Using `assets/sample_sales.csv`, total Sales by month (2024), plot it, and forecast Q1 2025 with a 3-month moving average and with Forecast Sheet. Discuss why only 12 months of history makes any seasonal forecast unreliable.
