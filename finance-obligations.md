# Personal Recurring Obligations

**Last Updated:** 2026-07-17

The authoritative list of recurring, calendar-driven money obligations: things
that come due on a cadence and cost real money if nothing surfaces them.

Paired with `finance-canon.md` (principles + account list) and
`finance-balances.csv` (the time series). This file answers "what is owed, and
when," which neither of those tracks.

Credentials are not stored here. See password manager.

---

## The model: two funnels, not twenty bills

Confirmed by Gil 2026-07-17: **there is no long list of separate bills.**
Effectively everything charges to a credit card, or (rarely) direct-debits.
So the entire bill surface is the cards themselves.

This changes what can go wrong. The risk is not forgetting an obscure vendor.
It is a **card quietly filling up while nobody looks**, then a due date passing.

That already happened. Wells Fargo ...3834 was -$1,216.33 on 2026-05-06 and
took a **$2,544.44** payment on 2026-07-17 -- it roughly doubled, unobserved,
because the balance file had not been updated in ten weeks. Nothing was
overdrawn and nothing was late, but nobody knew the number.

**So the snapshot is itself the load-bearing obligation.** Every other line here
depends on it. If the snapshot slips, the cards go dark again.

---

## How to use

- **Replace, do not append.** When something is satisfied, update its row: set
  Last done, advance Next due. Do not add a second row or a log line.
- **Next due is the live field.** It always points at the next time the thing is
  owed. Everything surfaces off it.
- **Unknown dates are tracked, not hidden.** An obligation with no known date
  gets `unknown -- confirm` so it keeps surfacing until it is pinned down.

---

## Obligations

### The monthly ritual

| Obligation | Cadence | Next due | Last done | How / where | Notes |
|---|---|---|---|---|---|
| **Balance snapshot + pay cards** | Monthly, the 10th | 2026-08-10 | 2026-07-17 | Log into each account, then Claude scrapes; append to `finance-balances.csv` | The keystone. Founder-set cadence 2026-07-17: monthly, ~10th, deliberately not near the start of the month. Prior cadence was "flexible" and drifted to 10 weeks. Pay both card balances in the same sitting. |

### Cards (the funnels)

| Obligation | Cadence | Next due | Last done | How / where | Notes |
|---|---|---|---|---|---|
| BofA Visa ...6657 "Unlimited Cash Rewards" | Monthly statement | 2026-08-11 (this cycle) | 2026-07-17 (paid $483.31 in full) | USAA Bill Pay | Min was $35.00; paid in full instead. Statement balance was $453.20, current $483.31. Autopay status **unknown -- confirm**. |
| Wells Fargo ...3834 | Monthly statement | **unknown -- confirm** | 2026-07-17 (paid $2,544.44) | USAA Bill Pay | Balance never verified -- the session logged out before it could be read, and it is unconfirmed whether the $2,544.44 cleared the full balance. Doubled unobserved since May. Due date and autopay status **unknown -- confirm**. |

### Direct debits

| Obligation | Cadence | Next due | Last done | How / where | Notes |
|---|---|---|---|---|---|
| Direct debits (unenumerated) | varies | unknown -- confirm | -- | -- | Founder reports these exist but are "rare." Not enumerated. They bypass the card funnels, so they are the one thing this register's two-funnel model does not cover. Worth naming them once. |

---

## Known trap: USAA Bill Pay does not post same-day

Bill Pay **initiates** a payment; it takes days to settle. A payment started on
the 10th against an 11th due date is late.

This is survivable only because the ritual pays a cycle ahead: the 2026-07-17
payment covers the statement due 2026-08-11, roughly a month of slack. **Do not
"catch up" a payment near its due date and assume it lands.** If a due date is
ever within ~5 business days, pay by card or at the biller directly, not Bill Pay.

---

## To confirm (turns "unknown" into real dates)

1. **Wells Fargo ...3834**: actual balance, due date, autopay on/off, and whether
   the $2,544.44 paid it in full.
2. **BofA ...6657**: is autopay on? If yes, the reminder is a check, not a task.
3. **Chase Freedom ...7878** and **USAA Signature Visa ...2053**: both $0.00 since
   at least May. Still open? Unused? If closed, drop from `finance-canon.md`.
4. **Edfinancial**: paid off 2026-07-17. Account closed, or open at $0?
5. **Direct debits**: which ones, against which account, what cadence?
6. **Nest529 / TSP / Venmo / PayPal**: all $0.00 since May, never re-verified.
