# Data — Google Account Cleanup

**Last Updated:** 2026-06-04

**Goal:** Retire `web@gkasparek.com` off Google Workspace — preserve all its data,
then shut the mailbox and account down. Keep `gil@buttonsimple.com` (Workspace).
Land everything personal on `tgkasparek@gmail.com` (free Gmail). Reduce Workspace cost.

Sibling project: [data-drives-consolidation.md](data-drives-consolidation.md) — both
feed the same end-state (cloud + offline backup). Canonical target storage decision
lives in that file's **Target storage** section; this project's exports follow it.

---

## Accounts

| Account | Type | Fate |
|---|---|---|
| `gil@buttonsimple.com` | Google Workspace | Keep (org / business) |
| `web@gkasparek.com` | Google Workspace | **Retire** — real mailbox, forwards to tgk@ already; preserve data then shut down |
| `tgkasparek@gmail.com` | Free Gmail | **Destination** — new personal primary |

Resolved open question (was step 1): `web@` is a live Gmail mailbox being retired,
not a permanent custom-domain inbox. Forwarding to `tgk@` already works, so once the
mailbox is preserved and shut down there is no send-from to maintain.

---

## Active Todos

### Phase A — Forwarding & access (DONE)

- [x] 1. Redirect email: Namecheap DNS forward `web@` → `tgk@`
- [x] 1.5. Phone: add `tgkasparek@gmail.com`

### Phase B — Preserve data off web@ (in progress)

- [x] 2. Copy Google Drive contents
- [x] 3. Copy Google Photos — *verify with grsync comparison before any deletion*
  - **2026-07-03: phone backup account flipped `web@` → `tgk@`. New-photo bleed into
    `web@` stopped.** This is why step 3 looked "done" but wasn't — the checkmark was
    the export, but new photos kept landing on `web@`. Remaining: one-time catch-up
    export of `web@` photos taken since the last pull (see Phase C).
- [x] 4. Expand Drive docs
- [x] 5. Clean up files (remove largest, pull out photos/videos)
- [x] 5.5. JSON fix
- [x] 6. Merge + deduplicate photos
- [ ] **7. Preserve web@ email — NEXT.** Mailbox is live; capture history before teardown:
  1. **Archive (canonical):** Google Takeout on `web@` → export Mail as **MBOX**.
     Store the MBOX with the offline backup (see drives doc Target storage).
  2. **Fold into tgk@ (optional but recommended):** in `web@` enable POP, then in
     `tgk@` → Settings → Accounts → *Import mail and contacts* to pull old mail +
     contacts over. (Workspace may restrict POP — enable it on `web@` first.)
  3. **Verify forwarding** is catching *new* mail at `tgk@` before deleting anything.
  - *Decision point:* archive-only, import-into-tgk@, or both. Recommend both.
- [ ] 10. Contacts — export from `web@`, confirm landed in `tgk@` (covered by 7.2 import, or Contacts export/import). Test.
- [ ] 10.5. Calendar — export `web@` calendars (ICS), import to `tgk@`. Test.

### Phase C — Tear down web@ (open)

- [ ] 8. Change default domain on Google Workspace (and remove web@ domain?)
- [ ] 9. Delete email attachments (various accounts) — storage reclaim
- [ ] 12a. **Final catch-up export of `web@` Photos** (full Takeout, `.zip`, 50 GB parts)
  — sweeps up photos taken between the last pull and the 2026-07-03 account flip. Land
  in `/home/gil/drive-archive`, dedup + verify + rclone to B2, THEN proceed to 12.
- [ ] 12. Delete Drive and Photos from `web@` (only after Phase B verified)
- [ ] 11. Phone: remove `web@` and `gil@b` accounts (bug-test first)
- [ ] 13. Remove `web@` from all devices (phone, Chromebook)
- [ ] **Final: shut down the mailbox / cancel the `web@` Workspace seat.** Confirm
  forwarding still routes anything stray, then close it out and stop the billing.

---

## Notes / gotchas

- Order matters: nothing gets deleted from `web@` (steps 9, 12) or the account closed
  until Phase B exports are verified present at their destination + offline backup.
- grsync photo comparison (step 3) is the gate on photo deletion.
- Billing only stops at the final shut-down step — that's the actual cost goal.
