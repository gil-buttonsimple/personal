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
| BofA Visa ...6657 "Unlimited Cash Rewards" | Monthly statement | 2026-08-11 (this cycle) | 2026-07-17 (paid $483.31 in full) | USAA Bill Pay | Min was $35.00; paid in full instead. Statement balance was $453.20, current $483.31. **No autopay -- deliberate** (confirmed 2026-07-17). Paid by hand, in full. |
| Wells Fargo ...3834 | Monthly statement | **unknown -- confirm** | 2026-07-17 (paid $2,544.44 in full) | USAA Bill Pay | Balance was -$2,544.44, paid in full 2026-07-17. Doubled unobserved since May (-$1,216.33 on 2026-05-06). **No autopay -- deliberate** (confirmed 2026-07-17). Due date **unknown -- confirm**. |

### Direct debits

| Obligation | Cadence | Next due | Last done | How / where | Notes |
|---|---|---|---|---|---|
| Direct debits (unenumerated) | varies | unknown -- confirm | -- | -- | Founder reports these exist but are "rare." Not enumerated. They bypass the card funnels, so they are the one thing this register's two-funnel model does not cover. Worth naming them once. |

---

## Delivery: two independent reminders

The register is inert; something has to fire off it. Two nudges run, on purpose
redundant, so a missed payment is hard:

1. **baobab desktop ding** (`scripts/finance-reminder.sh` + user timer). Daily
   check, self-clearing: fires only if this month has no snapshot yet, escalates
   by persisting. Only works when baobab is awake and in front of you.
2. **mesquite email** (`scripts/finance-reminder-mail.sh` + user timer on the
   always-on cloud node). Fires once on the 10th, emails via Resend (from
   support@buttonsimple.com) to gil@buttonsimple.com. **Baobab-independent** --
   this is the one that survives baobab being shut down. Per-month stamp guards
   against double-send. Keeps zero git credentials on the droplet, so it does not
   read the CSV: it nudges unconditionally on the 10th rather than self-clearing.

Set up 2026-07-17 when baobab was going down for an extended period. The email
reuses the app's existing Resend key (stored on mesquite at
~/.config/finance-reminder/resend_key, out of git). Follow-ups: a dedicated
Resend key rather than the app's auth key, and richer delivery (this is the
seed of gov#75, the unified messaging hub).

## Known trap: USAA Bill Pay does not post same-day

Bill Pay **initiates** a payment; it takes days to settle. A payment started on
the 10th against an 11th due date is late.

This is survivable only because the ritual pays a cycle ahead: the 2026-07-17
payment covers the statement due 2026-08-11, roughly a month of slack. **Do not
"catch up" a payment near its due date and assume it lands.** If a due date is
ever within ~5 business days, pay by card or at the biller directly, not Bill Pay.

---

## To confirm (turns "unknown" into real dates)

1. **Wells Fargo ...3834**: due date. (Balance -$2,544.44 and paid-in-full both
   confirmed 2026-07-17. Autopay: none, by choice.)
2. **Chase Freedom ...7878** and **USAA Signature Visa ...2053**: both $0.00 since
   at least May. Still open? Unused? If closed, drop from `finance-canon.md`.
3. **Edfinancial**: paid off 2026-07-17. Account closed, or open at $0?
4. **Direct debits**: which ones, against which account, what cadence?
5. **Nest529 / TSP / Venmo / PayPal**: all $0.00 since May, never re-verified.
