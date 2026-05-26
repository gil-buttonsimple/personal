# Personal Finance Canon
*Last updated: 2026-05-11*

This document captures the conventions, decisions, and analytical framing for personal finance tracking. Upload alongside balances.csv when starting a Claude conversation about finances.

## Purpose
The real goal is **runway visibility**: how long can I sustain current spending on life and business while staying comfortable. This is a cash-flow question answered via balance snapshots rather than transaction tracking.

Not tracking: monthly spending categorization, transactions, budgets. Tracking: account balances over time, with enough categorization to separate "money I'd actually use" from "money locked up."

## Canonical data file
**balances.csv** — long format, one row per account per snapshot date.

Schema:

date, account, type, category, balance, note

date — ISO format YYYY-MM-DD
account — full account name, stable across snapshots
type — Asset or Liability
category — see categories below
balance — signed number; liabilities are negative
note — free text for one-time events, account changes, anomalies

Long format chosen over wide so adding accounts or categories never invalidates history. Plain CSV chosen over markdown/JSON for tool-agnostic portability.

## Categories
| Category | Meaning | Counts toward runway? |
|---|---|---|
| Liquid | Cash-equivalent, immediately spendable | Yes |
| Investments-Taxable | Brokerage, 529, accessible w/ tax cost | Yes (with friction) |
| Investments-Retirement | IRA, TSP, 401k — locked until retirement age | No |
| Revolving Debt | Credit cards | Reduces runway |
| Student Loan | Edfinancial | Reduces runway (slow) |

## Current account list (as of 2026-05-06)
**Liquid (Assets):**

Checking (USAA)
Savings (USAA)
Venmo
Paypal

**Investments-Taxable (Assets):**

Baird-Other
Nest529

**Investments-Retirement (Assets):**

Baird-IRA
TSP (fema savings)

**Revolving Debt (Liabilities):**

BofA Visa "Unlimited Cash Rewards" (added 2026-05-06)
USAA Signature Visa (USAA) 2053
Wells Fargo 3834
Chase Freedom 7878

**Student Loan (Liabilities):**

Edfinancial

**Dropped/closed:**

Citi Simplicity Visa 0745 (closed; historical data discarded in CSV)

## Conventions
**Snapshot cadence:** flexible, not fixed. Pull data when convenient. The date column records when, not a target schedule.
**Schema stability:** old data preserved as-is. Adding accounts or categories adds new rows; never restructure history.
**Notes for anomalies:** when a one-time event distorts a trend, flag it in the note column so analysis can filter it out. Examples:
inheritance: +$100K deposit (2026-05-06, Baird-Other)
account drained (2026-05-06, Savings USAA)
new account added (2026-05-06, BofA Visa)
**Zero-balance accounts:** kept in the data, not removed. Zero is a real value.
**Closed accounts:** dropped from the active list once truly closed (e.g., Citi Simplicity).

## Analytical framing
When analyzing the data, the questions that matter:

**Burn rate** — average monthly change in (Liquid + Investments-Taxable), excluding flagged one-time events. Negative = burning, positive = accumulating.
**Runway** — (Liquid + Investments-Taxable) ÷ monthly burn rate = months of comfort.
**Trend changes** — is burn rate accelerating, decelerating, or steady? When did it shift?
**Composition drift** — is the mix between liquid / taxable / retirement / debt moving in a healthy direction?
**Anomaly investigation** — sudden balance changes flagged for explanation.

**Retirement accounts are excluded from runway math** — they're not accessible for current spending without significant penalty.

**Major event filter:** any row with a non-empty note should be considered for exclusion when computing trends. The inheritance (+$100K on 2026-05-06) is the obvious example — including it would mask the underlying burn pattern.

## Observations as of 2026-05-06
Net worth: ~$258K (with inheritance), ~$158K (excluding inheritance)
Of that, ~$154K is locked in retirement (Baird-IRA)
True runway pool (Liquid + Taxable, excluding retirement): ~$116K
Pre-inheritance liquid trend: ~$1.1K/month draw on liquid cash over Oct 2025 → May 2026
Credit card debt: substantially paid down over the past year ($12K+ → $1.2K)

## Storage
File location: Google Drive (personal account), root of My Drive
Backup: whatever Google Drive provides
Confidentiality: avoid connecting personal Drive to work-context Claude sessions

## Update process
When adding a new snapshot:

Pull current balances from each account
Append rows to balances.csv — one row per active account, same date
Add a note for any anomaly or one-time event
Save back to Drive

That's it. No spreadsheet formatting to maintain, no schema to update unless an account is added or closed.