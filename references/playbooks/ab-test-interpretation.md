# Playbook: Reading A/B test results

## What it is
An A/B test shows two versions (A = current, B = new) to randomly split groups and compares an outcome, like conversion rate. Interpreting it means deciding whether the difference is real or just luck.

## When to use it
"Marketing says the new email won, is that true?", "we tested two prices, which is better?", reading any experiment readout.

## Key ideas in plain English
- **Conversion rate:** % of people who did the thing. 50 buyers out of 1,000 visitors = 5%.
- **Lift:** how much better B is than A, in relative terms. 5% to 5.5% is a **10% lift** (but only 0.5 **percentage points**). Always say which one.
- **Statistical significance / p-value:** how surprising the result would be if there were really no difference. A common rule is p < 0.05. It is **not** "the chance B is better".
- **Confidence interval:** the range the true difference probably sits in. If it includes zero, the test hasn't shown a difference.
- **Sample size:** small tests produce big, unreliable swings.

## Steps
1. **Write down what was tested before looking at results:** what changed, the main metric, the planned duration and sample size. If the main metric was chosen after seeing the data, flag it.
2. **Check the setup:** were users split randomly? Are the group sizes about what was planned (e.g. 50/50)? A big imbalance (sample ratio mismatch) means something went wrong.
3. **Check it ran long enough:** at least one full week (to cover weekday/weekend behavior) and reached the planned sample size.
4. **Calculate each group's rate** and the difference, both in points and as lift.
5. **Check significance:** use the tool's readout, or a free online "A/B test significance calculator" with **just the four counts** (visitors and conversions per group; these aggregates are usually safe to enter, but check your tier). In Excel, a two-proportion z-test can be built step by step on request.
6. **Teach-back:** "The interval for the difference is −0.2 to +1.1 points. What does that tell us?" (Zero is in the range, so we can't be confident B is better.)
7. **Check guardrail metrics:** did B hurt anything else (refunds, unsubscribes, page speed)?
8. **Write the readout** using the analysis summary template: result, confidence, caveats, recommendation.

## Common mistakes
| Mistake | Why it matters |
|---|---|
| Stopping the test as soon as it looks significant ("peeking") | Inflates false wins; stick to the planned duration |
| Testing many metrics and reporting the one that won (p-hacking) | Something will "win" by chance; name the main metric up front |
| Mixing up percent and percentage points | Makes results sound bigger or smaller than they are |
| Tiny samples | Big swings that don't hold up |
| Slicing into many segments after the fact | Segment "wins" are often noise; treat them as ideas for the next test |
| "Not significant" read as "no effect" | It means "not shown yet"; the test may be too small |

## How to check this
- Group sizes match the planned split (within a percent or two).
- Recalculate one group's conversion rate from the raw counts.
- Re-enter the counts in a second calculator and see if it agrees.

## Escalation
Tests involving pricing, credit, health or anything regulated: involve the analytics owner and legal/compliance before acting on results.

## Practice exercise
Fake result: A had 10,000 visitors and 500 conversions; B had 10,000 visitors and 560 conversions. Ask the user: rates? lift (12%) vs points (0.6)? Then check significance with a calculator (about p ≈ 0.06, so borderline). What would you recommend?
