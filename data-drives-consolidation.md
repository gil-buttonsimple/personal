# Data — Hard Drive Consolidation

**Last Updated:** 2026-06-23

**Goal:** 3–5 hard drives of mixed/random content → review, catalog, dedup, and
consolidate into one canonical home (cloud + offline backup). Retire the loose drives
once their content is safely landed and verified.

Sibling project: [data-google-cleanup.md](data-google-cleanup.md) — both land data in
the same place. This file owns the shared **Target storage** decision below.

Status: **active** — sources pulled, deduped, and staged at `/home/gil/drive-archive`
on baobab; a pre-upload trim/compression pass is underway before the off-site push.
The non-GoPro HEVC re-encode is **paused mid-run, resumable** (see below).

---

## Target storage (shared end-state)

The canonical destination both this project and the Google cleanup consolidate into:

- **Cloud (canonical home):** Google Drive on `tgk@`.
- **Off-site backup:** **Backblaze B2** (see personal #14) — the "1 off-site" of 3-2-1,
  on a different provider than Google. ~$6/TB/mo, restore-friendly.
- **Folder taxonomy:** how the staged archive is organized before/at the destination —
  **OPEN** (raised s27). Current staging keeps each source under its own top-level
  folder (`72097`, `tgk`, `copper`, `gk-usb`); a cleaner cross-source taxonomy is TBD.

---

## The drives (staged at `/home/gil/drive-archive`)

| Source | Origin | Size (post-dedup) | State |
|---|---|---|---|
| `72097` | hard drive | 251 GB | pulled, deduped; mining for portfolio content pending |
| `tgk` | Google Drive/Photos export (`tgk@`) | 100 GB | pulled, deduped |
| `copper` | hard drive | 5.4 GB | pulled, deduped |
| `gk-usb` | USB | ~1 MB | pulled |

Total ~356 GB after an rmlint dedup pass (2026-06-12). Original estimate was 3–5
drives; confirm whether any sources are still outstanding before treating the pull
as complete (#14).

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

## Pre-upload trim / compression pass (s27, 2026-06-22)

Goal: shrink the staged archive before pushing to B2 — don't pay to back up junk or
over-bitrated video. Reversible by design: removed items are staged to
`/home/gil/drive-archive/_TRASH` (not hard-deleted) until a final confirm.

Done this session:
- **Batch-1 junk staged (~32 GB):** old software installers/ISOs, `placelogic_OBSOLETE`,
  PlaceLogic Postgres `db/base` dumps, commercial DVD rips (`VIDEO_TS`/`.VOB`).
- **OS cruft purged:** 13,449 `Thumbs.db` / `.DS_Store` / `._*` / `desktop.ini` files
  hard-deleted; 5,926 empty dirs removed; `.Picasa3Temp` caches (1.2 GB, incl. a
  commercial movie rip) staged.
- **GoPro re-encode (H.264 → HEVC, CRF 24):** 144 clips, **54.2 GB → 10.3 GB** (~44 GB
  saved), 0 duration mismatches, originals kept in place pending spot-check + swap.
  HEVC set mirrored at `/home/gil/drive-archive/_gopro_hevc`.
- **Non-GoPro video re-encode (H.264 → HEVC, CRF 20):** **PAUSED 2026-06-23 at ~180 of
  544 candidates encoded (~20 GB out so far); ~115 skipped** (already HEVC / non-target).
  Mostly `tgk` Google Photos export family video; originals remain in Google. CRF 20 (not
  24) because these are irreplaceable memories.
  **Resume:** run `/home/gil/drive-archive/_proof/resume_encode.sh` — idempotent (skips
  done files via a valid-output `ffprobe` check) and re-applies a 4-of-16-core cgroup CPU
  cap (heavy multicore drops baobab's Bluetooth trackball; see infrastructure.md). The
  bare batch is `_proof/encode_video.sh` (runs unthrottled).
  **Mismatches:** 3 `DUR-MISMATCH` outputs flagged in `_video_hevc/encode.log`. Review ALL
  mismatches at the very end (after the batch completes), before swapping any originals —
  `grep DUR-MISMATCH _video_hevc/encode.log`.

Projected: archive ~356 GB → **~135 GB** before B2.

## Active Todos

- [ ] Spot-check GoPro HEVC, then swap originals → `_TRASH`; empty `_TRASH` for good.
- [ ] Resume + finish non-GoPro H.264 → HEVC (CRF 20) pass (`_proof/resume_encode.sh`);
      then review all `DUR-MISMATCH` files; spot-check; swap.
- [ ] Decide folder taxonomy (organize before upload — open).
- [ ] Mine `72097` (Egypt-PC, CD-archive, Magento) for portfolio content before trimming.
- [ ] Install rclone; create Backblaze B2 bucket; push the slimmed archive; verify hashes (#14).
