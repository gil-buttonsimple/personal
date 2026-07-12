# Data — Hard Drive Consolidation

**Last Updated:** 2026-06-23

**Goal:** 3–5 hard drives of mixed/random content → review, catalog, dedup, and
consolidate into one canonical home (cloud + offline backup). Retire the loose drives
once their content is safely landed and verified.

Sibling project: [data-google-cleanup.md](data-google-cleanup.md) — both land data in
the same place. This file owns the shared **Target storage** decision below.

Status: **B2 upload COMPLETE** (2026-07-12) — sources pulled, deduped, trimmed, and
HEVC-re-encoded; `_TRASH` emptied (archive ~281 GB local staging). Full bulk archive is
on Backblaze B2: **278.4 GiB / 207,969 objects**, all six folders present
(`72097`, `tgk`, `copper`, `gk-usb`, `_analysis`, `_proof`). Bucket `gk-drive-archive`
(region `us-east-005`, private, encryption on); rclone remote `b2archive:`; secret in
`~/.config/rclone/rclone.conf` only. Filter excludes scratch dirs (`_proof`, `_analysis`,
`_*_hevc`, root logs) at `_proof/b2_upload.filter`; sync log `_proof/b2_sync.log`.
This is the "1 off-site" of 3-2-1 (personal #14).

---

## Target storage (shared end-state)

The canonical destination both this project and the Google cleanup consolidate into.
**Corrected 2026-07-06/07-12:** the *bulk archive* has ONE home — **Backblaze B2** — not
Google Drive. (An in-session error briefly uploaded 85.6 GB of the bulk to Google Drive;
that folder was deleted and repointed to B2.) Google Drive on `tgk@` is used only for small
**share slices** that need a human-friendly link (e.g. Stacey's ~15 GB delivery), never the
bulk. The founder's standing preference (2026-07-12) is **nothing resting on the LAN**: data
lives in the cloud (B2), and the baobab `/home/gil/drive-archive` copy is staging to be reclaimed.

- **Canonical home (bulk archive):** **Backblaze B2** — `b2archive:gk-drive-archive`
  (see personal #14). ~$6/TB/mo, restore-friendly.
- **Google Drive (`tgk@`):** share slices only, not the bulk.
- **3-2-1 note / OPEN decision:** B2 is currently the *only* copy of the bulk (the planned
  "write keeper set to a wiped local drive" master was never written). One cloud copy is not
  a full backup — founder to decide: accept B2-only and reclaim baobab, or add one local master.
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
- **Non-GoPro video re-encode (H.264 → HEVC, CRF 20):** **COMPLETE 2026-06-24.** All 544
  candidates resolved: 107 encoded in the final run + 183 from the earlier run + 254 skipped
  (already HEVC / non-target codec). Output ~27 GB at `/home/gil/drive-archive/_video_hevc`.
  Mostly `tgk` Google Photos export family video; originals remain in Google. CRF 20 (not
  24) because these are irreplaceable memories.
  **Resume (no longer needed):** `_proof/resume_encode.sh` is idempotent (skips done files
  via a valid-output `ffprobe` check) and re-applies a 4-of-16-core cgroup CPU cap (heavy
  multicore drops baobab's Bluetooth trackball; see infrastructure.md) — kept for re-runs if
  more sources land. Bare batch: `_proof/encode_video.sh` (unthrottled).
  **Mismatches resolved:** the 3 `DUR-MISMATCH` outputs were the 2012 PlaceLogic training
  screencasts (1024×768, ~5–8 fps screen captures). HEVC at forced 10 fps came out 3–5×
  *larger* than the H.264 source and ~34 s short, so the 3 re-encodes were deleted and the
  originals kept as-is. No other mismatches.

Projected: archive ~356 GB → **~135 GB** before B2.

## Active Todos

- [x] Spot-check GoPro HEVC (144/144 valid, audio intact, 0 mismatches) + swap all
      re-encoded originals → `_TRASH` — **done 2026-06-25** (431 swapped: 144 GoPro + 287
      non-GoPro; HEVC now in place; manifest at `_TRASH/swap_manifest_2026-06-25.log`).
- [x] **Empty `_TRASH` for good** — **done 2026-06-25** (113 GB reclaimed; `drive-archive`
      394 GB → 281 GB). Swap manifest preserved at `_proof/swap_manifest_2026-06-25.log`.
- [x] Resume + finish non-GoPro H.264 → HEVC (CRF 20) pass — **done 2026-06-24** (544/544);
      3 DUR-MISMATCH screencasts reviewed → kept H.264 originals, deleted bloated HEVC copies.
- [ ] Decide folder taxonomy (organize before upload — open).
- [ ] Mine `72097` (Egypt-PC, CD-archive, Magento) for portfolio content before trimming.
- [~] Backblaze B2 off-site backup (#14): rclone installed, bucket `gk-drive-archive` +
      key created, sync **launched 2026-06-25** (278.5 GiB in flight). Remaining: let it
      finish, then `rclone check` parity, mark #14 done. Decide one-time vs scheduled cadence.
