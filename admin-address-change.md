# Address Change — Consolidate to PO Box

Last Updated: 2026-06-11
Status: **P1 (priority: now)** — GitHub Issue #13 — start 2026-06-12
Current focus: Financial accounts + credit cards

Working checklist for a full change-of-address sweep, consolidating every
account onto the new PO box. This is personal life-admin and lives here even
though it includes the Button Simple items. When the *business* addresses
actually change, record the new mailing address as a durable fact in gov
`operations.md` (Legal & Company).

## New address (canonical)
**Mailing:** PO Box 152, Chester, SC 29706-0152
**Physical (where PO box is rejected):** 1221 Great Falls Hwy, Chester, SC (the farm)
  ← confirm ZIP. No USPS delivery there (no mailbox) — expect a "can't deliver,
  accept anyway" override.

## Old addresses being retired
- 2973 India Hook Rd, Rock Hill, SC 29732-8423 (most recent — confirmed; USPS COA filed 2026-06-12)
- 1770 Analani St, Wailuku, HI 96793 (Hawaii — confirm ZIP; for-the-record, chase in account profiles)
- 2443 Fillmore St, San Francisco, CA 94115 (California — the "Fillmore St box"; assoc. old phone 380-7839?; for-the-record)

"Some still hanging around" — stale ones lingering in systems that never updated.

## PO box caveat
A PO box is fine for MAILING but is rejected where a PHYSICAL address is
required: driver's license (physical addr), bank/brokerage KYC. Use the PO box
for mailing/contact, keep a physical address where mandated.

## Active Todos
- [~] USPS Change of Address — per-origin forwarding (see USPS forwarding section below)
- [ ] **Financial sweep (current focus — below)**
- [ ] Government / official
- [ ] Insurance / other
- [ ] Business (Button Simple)
- [ ] When business addresses change, record new mailing addr in gov operations.md

---

## USPS forwarding (one COA per old address → PO Box 152, Chester, SC 29706-0152)
Filed as: Travis G Kasparek · Individual · Permanent · web@gkasparek.com · (510) 427-4326.
File online at usps.com/move ($1.10 ID-verify fee each) or free in person on PS Form 3575.

| From address | Status | Forward date | Notes |
|---|---|---|---|
| 2973 India Hook Rd, Rock Hill, SC 29732-8423 | ✅ filed 2026-06-12 | 2026-06-13 | Permanent, Individual |
| 2443 Fillmore St, San Francisco, CA 94115 | ✕ N/A | — | Years old; mail no longer flows there, mailbox long closed. Not USPS-forwardable — for-the-record / account cleanup only |
| 1221 Great Falls Hwy, Chester, SC (farm) | ☐ very low priority | — | Precautionary only; likely rejected (no USPS delivery there) — try if convenient, don't sweat it |

Business (Button Simple) USPS forward: NOT filing at this time (decided 2026-06-12).
Personal forward (2973 → PO box) only. Business mail handled per-account if/when it changes.

---

## Financial — banks & brokerage  ← START HERE
| Account | Old addr on file | PO box OK? | Status | Notes |
|---|---|---|---|---|
| USAA — Checking | ? | verify | ✅ done | Updated 2026-06-12 (all USAA accounts in one pass) |
| USAA — Savings | ? | verify | ✅ done | Same login as checking |
| Baird — Other (taxable) | ? | yes | ☐ | |
| Baird — IRA | ? | yes | ☐ | |
| Nest529 | ? | yes | ☐ | |
| TSP (tsp.gov, FEMA) | ? | yes | ☐ | Federal Thrift Savings Plan |
| Venmo | ? | yes | ☐ | |
| PayPal | ? | yes | ☐ | |

## Financial — credit cards
| Card | Old addr on file | PO box OK? | Status | Notes |
|---|---|---|---|---|
| BofA Visa "Unlimited Cash Rewards" | ? | yes | ✅ done | PO box on card mailing; profile rejected PO box → used 1221 GFH physical (2026-06-11) |
| USAA Signature Visa ·2053 | ? | verify | ✅ done | Updated 2026-06-12 (USAA pass) |
| Wells Fargo ·3834 | ? | yes | ✅ done | Via phone 2026-06-12 (online wouldn't take it); PO box accepted; verified online. Billing ZIP for AVS now 29706 |
| ~~Chase Freedom ·7878~~ | — | — | ✅ closed | No action — account closed |
| Edfinancial (student loan) | ? | yes | ☐ | Loan servicer, not a card |
| ~~Citi Simplicity Visa ·0745~~ | — | — | ✅ closed | No action — account closed |

---

## Government / official
| Place | Old addr on file | PO box OK? | Status | Notes |
|---|---|---|---|---|
| USPS Change of Address | — | n/a | ◐ | Per-origin; see USPS forwarding section. 2973 ✅ filed 2026-06-12 |
| IRS (personal 1040) | — | yes (mailing) | ✅ decided | No action now; PO box on next 1040 (no paper IRS mail expected). Business EIN is separate — Form 8822-B, part of deferred business pass |
| SC DMV — license + registration | ? | mailing only | ✅ done | Updated 2026-06-12. Physical 1221 Great Falls Hwy on license; PO box mailing. County York→Chester = vehicle property tax now Chester |
| Voter registration (SC) | ? | ? | ☐ | |
| Social Security (SSA) | ? | yes | ☐ | |
| Passport | ? | yes | ☐ | Only at renewal — low priority |

## Insurance / other
| Place | Old addr on file | PO box OK? | Status | Notes |
|---|---|---|---|---|
| Health insurance | ? | yes | ☐ | |
| Auto insurance (USAA) | ? | yes | ✅ done | Address updated + coverage restructured 2026-06-12 (dropped comp/collision/rental; see finance-canon.md) |
| Renters/home (if any) | ? | — | ☐ | |
| Amazon delivery default | ? | n/a | ☐ | Farm has no mailbox (property-mapping.md) |

## Business — Button Simple
Durable new address also goes in gov `operations.md` once changed.

| Place | Old addr on file | PO box OK? | Status | Notes |
|---|---|---|---|---|
| IRS EIN business addr (Form 8822-B) | ? | yes | ☐ | EIN 33-2392297 |
| Northwest Registered Agent acct | ? | yes | ☐ | KEEP as RA (PO box can't be the RA) |
| Relay business banking | ? | verify (KYC) | ✅ done | Updated 2026-06-12. Confirm whether it took PO box mailing or required a physical addr — relevant to the later business pass |
| Apple Developer (seller addr) | ? | verify | ☐ | Shown publicly on paid apps |
| Google Play Developer | ? | verify | ☐ | Public seller addr |
| Domain WHOIS buttonsimple.com | ? | yes | ☐ | Often privacy-masked already |
| Google Workspace billing | ? | yes | ☐ | |
| Operating Agreement | ? | yes | ☐ | Already flagged for update (operations.md) |
| Business insurance (if any) | ? | verify | ☐ | |
