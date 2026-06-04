# Data — Hard Drive Consolidation

**Last Updated:** 2026-06-04

**Goal:** 3–5 hard drives of mixed/random content → review, catalog, dedup, and
consolidate into one canonical home (cloud + offline backup). Retire the loose drives
once their content is safely landed and verified.

Sibling project: [data-google-cleanup.md](data-google-cleanup.md) — both land data in
the same place. This file owns the shared **Target storage** decision below.

Status: **stub** — content review not yet started.

---

## Target storage (shared end-state)

The canonical destination both this project and the Google cleanup consolidate into.
Decisions TBD — fill in before bulk moves:

- **Cloud (canonical home):** which service? (Google Drive on `tgk@`, or other?) — TBD
- **Offline backup:** medium + standard. Aim for **3-2-1** (3 copies, 2 media, 1 off-site). — TBD
- **Folder taxonomy:** how consolidated data is organized at the destination — TBD

---

## The drives

| # | Label / id | Capacity | Connection | Contents (first pass) | State |
|---|---|---|---|---|---|
| 1 | TBD | — | — | — | not yet reviewed |
| 2 | TBD | — | — | — | not yet reviewed |
| 3 | TBD | — | — | — | not yet reviewed |
| 4? | TBD | — | — | — | not yet reviewed |
| 5? | TBD | — | — | — | not yet reviewed |

(Exact count is 3–5; fill in as each drive is mounted.)

---

## Workflow (per drive)

1. **Mount / image.** Connect; if a drive is failing or sketchy, image it first
   (`ddrescue`) and work from the image.
2. **Catalog.** Produce a file listing (type, size, date) so contents are reviewable
   without keeping the drive online. Note anything obviously junk vs. keep.
3. **Review with Gil.** Decide keep / dedup / discard per major folder.
4. **Dedup.** Against what's already in cloud and across drives (e.g. `rmlint` /
   `fdupes` / hash compare). Don't re-upload what's already landed.
5. **Consolidate.** Move keepers into the Target storage taxonomy (cloud + offline backup).
6. **Verify.** Confirm landed + backed up (checksums) before touching the source.
7. **Retire drive.** Wipe and repurpose or store, only after verification.

---

## Active Todos

- [ ] Locate and label all drives; fill in the drive table (count, capacity, connection).
- [ ] Decide Target storage (cloud + offline backup standard) above.
- [ ] First-pass catalog of drive 1 to learn scope before committing a full method.
