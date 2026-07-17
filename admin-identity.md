# Legal Identity

**Last Updated:** 2026-07-17

Official identity facts. These are the values that appear on legal, financial,
and government records. Recorded here because they differ from the name used
day to day, and that gap has already caused real errors (see below).

Credentials and secrets are not stored here. See password manager.

---

## Full legal name

**Travis Gilmore Kasparek**

- Goes by **Gil**, which is short for the middle name, Gilmore.
- **"Travis Kasparek" and "Gil Kasparek" are the same person.** Travis is not a
  relative, a business partner, or a second account holder.

## Where each form shows up

| Surface | Name shown | Why |
|---|---|---|
| Bank of America | Travis Kasparek | Legal name on the account |
| Baird (brokerage) | KASPAREK TRAVIS | Legal name, surname-first |
| Apple Developer Program | Travis Kasparek | Account Holder of record |
| USAA | "Gil's checking" | Self-set account nickname, not a legal field |
| Git / GitHub / email | Gil Kasparek | Day-to-day name |

Rule of thumb: **anything legal, financial, or government-facing shows Travis.
Anything self-named or informal shows Gil.**

## Why this file exists

On 2026-07-17 a session scraping account balances found "Travis Kasparek" on the
Bank of America and Baird pages while `finance-canon.md` filed those accounts as
Gil's. Unable to tell whether it was a joint account, an authorized-user card, or
the wrong login entirely, it stopped and refused to write ~$240K of balances into
the runway math until the founder confirmed.

That was the right call on incomplete information, but the information should not
have been missing. The same gap had already produced a **false warning in
governance canon**: `execution/recurring_obligations.md` recorded the Apple
Developer Account Holder as "Travis Kasparek (not the founder -- a bus-factor
risk; the founder cannot recover this account alone)." There was no bus-factor
risk. The account holder was always the founder. That line was corrected on
2026-07-17.

An identity fact this basic, absent from the repo, costs a session every time it
surfaces and can silently harden into wrong canon. It is written down now.
