# Data — Hard Drive Consolidation

**Last Updated:** 2026-07-15

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

**Cold-drive master (offline 2nd copy) — WRITTEN 2026-07-15.** The keeper set is now on
the 1 TB Toshiba (ext4, label `gk-cold-master`, ~281 GB, all folders present), written via
`tar` streaming (per-file rsync was sub-1 MB/s on the USB disk; see Transfer method below).
Checksum verification (`rclone check --one-way`) run 2026-07-15; only non-data diffs (a
copy-time log file + venv symlinks). Once verified clean: eject and stow **unplugged** at
the farm/drawer, then reclaim the baobab `/home/gil/drive-archive` staging. Completes 3-2-1.

**⚠ NEEDS `fsck` BEFORE IT IS TRUSTED AS FINAL (2026-07-16).** The drive was physically
unplugged while still mounted, so the ext4 journal aborted mid-update:
`Aborting journal on device sda1-8` / `JBD2: I/O error when updating journal superblock`.
Nothing was writing to it at the time (the archive was written 2026-07-15 and idle since),
so data loss is unlikely and the 2026-07-15 verification still stands — but the filesystem
did not close cleanly and is marked dirty. **Next time it is plugged in, run `fsck` before
reading from it or calling it verified**, and ideally re-run `rclone check` against B2. This
matters more than it would for an ordinary disk: it is one of only two copies of the
archive, the other being B2.

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
- **3-2-1 — DECIDED 2026-07-12: B2 primary + one OFFLINE cold-drive master.** B2 alone is
  one copy in one account (lockout / billing lapse / accidental delete = total loss), unacceptable
  for irreplaceable family history. Plan: write the keeper set once to a single external drive
  (06's 1 TB Toshiba after a clean reformat is the natural candidate) that lives **unplugged**
  in a drawer / at the farm — off, not on the LAN, so it honors "nothing resting on the LAN"
  while giving a true 2nd copy. THEN reclaim baobab's ~281 GB staging. (Local master step,
  dropped as B2-only earlier, is back ON.)
- **Folder taxonomy:** how the staged archive is organized before/at the destination —
  **OPEN** (raised s27). Current staging keeps each source under its own top-level
  folder (`72097`, `tgk`, `copper`, `gk-usb`); a cleaner cross-source taxonomy is TBD.

---

## The drives (staged at `/home/gil/drive-archive`)

| Source | Origin | Size (post-dedup) | State |
|---|---|---|---|
| `72097` | hard drive | 251 GB | pulled, deduped; mining for portfolio content pending |
| `tgk` | Google Drive/Photos export (`tgk@`) | 100 GB | pulled, deduped; **source drive verified + WIPED 2026-07-16** → reformatted exFAT as `SABRENT500G`, now an empty spare |
| `copper` | hard drive | 5.4 GB | pulled, deduped |
| `gk-usb` | USB | ~1 MB | pulled |

Total ~356 GB after an rmlint dedup pass (2026-06-12). Original estimate was 3–5
drives; confirm whether any sources are still outstanding before treating the pull
as complete (#14).

---

## Transfer method — copying to a slow disk (learned 2026-07-15)

Writing the cold master to the USB Toshiba, `rsync -a` crawled at ~0.4 MB/s and
projected many hours. **Diagnosis: it was never the "protocol" — it's per-file overhead
on a spinning USB disk.** The source (`/home/gil/drive-archive`) sits on the internal
NVMe, so *reads* are free; the only slow medium is the USB write side, and rsync writes
each of tens of thousands of tiny files individually (open + write + fsync per file),
thrashing the head. That drops a disk capable of ~120 MB/s sequential down to sub-1 MB/s.

**Rule for next time — pick the copy method up front by file-size profile:**
- **Many small files → a slow/USB disk:** do NOT use per-file `rsync`. Stream it:
  `tar -C src -cf - . | tar -C dst -xpf -`. Streaming turns the random small-file writes
  into one sequential write and hits near disk speed (~40 min here vs. hours). Keeps a
  browsable tree.
- **Large files only (already-deduped video/photos):** `rsync` or `tar` are both fine;
  large sequential writes already run near disk speed.
- **Compression (`zstd`) is usually NOT worth it for this archive.** ~103 GB of it
  (`tgk` family video, HEVC sets) is already compressed and won't shrink; only `72097`
  compresses. Space isn't scarce (916 GB drive, ~30% full) and a compressed tarball is
  opaque to browse/restore. Streaming (uncompressed `tar`) gets the whole speed win
  without any of that.
  **Trackball caveat retired 2026-07-16:** this used to also cite heavy multicore
  compression dropping baobab's Bluetooth trackball, which is why the video re-encode was
  core-capped. That fault was on the onboard MediaTek radio; the peripherals moved to the
  UB500 dongle on 2026-06-23 and the founder reports it fixed. Do not core-cap on the
  trackball's account. See infrastructure.md.

## `tgk` source drive — verified safe to wipe (2026-07-16)

The 500 GB Sabrent-enclosed `tgk` drive (drive 02 in the storage catalog: master personal
photo library, Google Photos export 2000–2026 + iCloud) was re-plugged and checked against
the archive before wiping. **Result: nothing on it is missing from B2. Cleared, and WIPED 2026-07-16** — reformatted GPT + exFAT, labelled `SABRENT500G` (enclosure make + nominal size; exFAT caps labels at 11 chars). exFAT chosen so the drive is usable on Linux (native since kernel 5.4) and also on Windows/Mac. It is now an empty ~466 GB general-purpose spare.

What was checked, and what it settles:
- **Re-encode quality.** Of 321 archived files with an original still on the drive, only
  **135 were actually converted** by us (H.264 → HEVC); the other 186 were already HEVC off
  the phone and are byte-identical copies. Frame comparisons on 8 samples plus full-clip
  side-by-side playback on 2 (including the single most aggressive compression in the whole
  set — 6% of source, 75 MB → 5 MB) all held resolution, matched duration, and kept audio
  (AAC stereo both sides). Founder reviewed: "look perfect." **The CRF 20 re-encode is sound.**
- **iCloud material (`iCloud_photos/`, 1.6 GB, 493 files).** This was the real risk: unlike
  the Google Photos export it has NO upstream copy to fall back on. `rclone check` against
  `b2archive:gk-drive-archive/tgk/iCloud_photos`: **491 hash-identical**. The 2 flagged as
  "missing" are false alarms — both are re-encode swaps (`.MOV` H.264 → `.mp4` HEVC), present
  in B2 under the new extension, durations matching to ~0.01s with audio intact. rclone only
  flagged them because it matches on filename and the extension changed.

Method note for re-verifying any source drive: `rclone check <drive-path> b2archive:<bucket-path>
--one-way`. Expect extension-change false positives wherever the re-encode swapped `.MOV`/`.AVI`
→ `.mp4`; confirm each by probing codec + duration rather than treating it as a gap.

## Known defect: some re-encodes came out LARGER than the source

Found 2026-07-16 while sampling. HEVC at CRF 20 does not always shrink a file — on
low-detail or low-framerate sources it can inflate. **2 of 8 sampled conversions grew**
(81 MB → 138 MB; 26 MB → 29 MB), and one of the two iCloud conversions grew as well
(98 MB → 146 MB). This is the same pathology already caught and reverted for 3 screencasts
(see the DUR-MISMATCH note below) — but those were caught only because their durations were
off. Files that inflated *without* a duration mismatch were kept silently.

**No data is at risk** — these are valid, full-quality conversions, just bigger than what
they replaced. The cost is storage (local, cold master, and B2 bytes) plus the irony of
having discarded a smaller H.264 original. Cleanup is optional: sweep the 135 conversions
for any where the HEVC exceeds its source, and where the original still exists (Google, or
a source drive not yet wiped) prefer the original. Tracked in personal #14.

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
- [ ] Mine `72097` (Egypt-PC, CD-archive, Magento) for portfolio content.
      **Source moved (2026-07-15):** the original raw `72097` Toshiba was reformatted into the
      offline cold master (below), so mine from the deduped copy instead —
      `/home/gil/drive-archive/72097` (staging) or the `72097/` folder in B2
      (`b2archive:gk-drive-archive/72097`). Nothing unique was lost in the wipe (drive held
      pre-dedup dupes only; deduped set verified in B2).
- [~] Backblaze B2 off-site backup (#14): rclone installed, bucket `gk-drive-archive` +
      key created, sync **launched 2026-06-25** (278.5 GiB in flight). Remaining: let it
      finish, then `rclone check` parity, mark #14 done. Decide one-time vs scheduled cadence.
