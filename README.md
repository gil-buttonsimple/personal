# Personal -- GK

Last Updated: 2026-06-01

---

## Documents

| File | Domain | Description |
|---|---|---|
| [health-cholesterol-plan.md](health-cholesterol-plan.md) | Health | Cholesterol and diet plan, active todos |
| [finance-canon.md](finance-canon.md) | Finance | Financial principles, accounts, strategy |
| [finance-balances.csv](finance-balances.csv) | Finance | Account balances time series |
| [data-google-cleanup.md](data-google-cleanup.md) | Data | Retire web@ off Google Workspace; preserve data, shut down |
| [data-drives-consolidation.md](data-drives-consolidation.md) | Data | 3-5 hard drives → review, dedup, consolidate to cloud + offline backup |
| [property-mapping.md](property-mapping.md) | Side | Farm / property mapping project |
| [admin-address-change.md](admin-address-change.md) | Admin | Change-of-address sweep, consolidating accounts to the new PO box |
| [admin-identity.md](admin-identity.md) | Admin | Legal identity: full legal name and which surfaces show Travis vs Gil |
| [finance-obligations.md](finance-obligations.md) | Finance | Recurring money obligations: the monthly ritual, the two card funnels, due dates |
| [personal_state.md](personal_state.md) | System | Current state, open items, migration status |
| [_inbox.md](_inbox.md) | System | Cross-context captures (business items surfacing in personal chats) |

---

## Conventions

**Scope:** Genuinely personal content only -- finance, health, friends, side
businesses. Infrastructure (machines, network, mobility, the VW Eurovan) is a
business domain and lives in the governance repo (architecture/). The VW files
moved to gov on 2026-06-01.

**Naming:** Domain prefix, kebab-case.
- `health-` -- health, diet, medical
- `finance-` -- money, accounts
- `data-` -- digital data consolidation: storage, migration, backup
- `admin-` -- life admin: addresses, accounts, official records, filings
- Sub-projects extend the prefix
- Additional domains as they emerge: `friends-`, `side-`

**Todos:** Each project doc owns its own `## Active Todos` section near the top. No central todo list. Sub-projects without their own todos section roll up to the parent's Active Todos.

**Freshness:** Each doc keeps a `**Last Updated:**` line near the top.

**Index:** This file (README.md) is the index. Update whenever a doc is added, renamed, or significantly changed.

---

## Relationship Map

- `finance-balances` <-> `finance-canon` (always paired)
- `finance-obligations` -> `finance-balances` (the monthly ritual produces the snapshot)
- `health-cholesterol-plan` -- stands alone
- `data-google-cleanup` <-> `data-drives-consolidation` (share the cloud + offline backup end-state; target storage decision lives in the drives doc)
