# Personal -- GK

Last Updated: 2026-05-14

---

## Documents

| File | Domain | Description |
|---|---|---|
| [vehicle-eurovan-profile.md](vehicle-eurovan-profile.md) | Vehicle | 1999 VW Eurovan -- build intent, current phase, active todos |
| [vehicle-eurovan-loft-bed.md](vehicle-eurovan-loft-bed.md) | Vehicle | Loft bed sub-project spec and todos |
| [health-cholesterol-plan.md](health-cholesterol-plan.md) | Health | Cholesterol and diet plan, active todos |
| [finance-canon.md](finance-canon.md) | Finance | Financial principles, accounts, strategy |
| [finance-balances.csv](finance-balances.csv) | Finance | Account balances time series |
| [personal_state.md](personal_state.md) | System | Current state, open items, migration status |
| [_inbox.md](_inbox.md) | System | Cross-context captures (business items surfacing in personal chats) |

---

## Conventions

**Naming:** Domain prefix, kebab-case.
- `vehicle-` -- vehicle-related
- `health-` -- health, diet, medical
- `finance-` -- money, accounts
- Sub-projects extend the prefix: `vehicle-eurovan-loft-bed`
- Additional domains as they emerge: `home-`, `work-`, `family-`

**Todos:** Each project doc owns its own `## Active Todos` section near the top. No central todo list. Sub-projects without their own todos section roll up to the parent's Active Todos.

**Freshness:** Each doc keeps a `**Last Updated:**` line near the top.

**Index:** This file (README.md) is the index. Update whenever a doc is added, renamed, or significantly changed.

---

## Relationship Map

- `vehicle-eurovan-loft-bed` -- sub-project of `vehicle-eurovan-profile` (todos roll up to the profile)
- `finance-balances` <-> `finance-canon` (always paired)
- `health-cholesterol-plan` -- stands alone
