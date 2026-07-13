# Data — Google Account Cleanup

**Last Updated:** 2026-07-12

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
- [x] **7 / 10 / 10.5. Preserve web@ account-locked data (Mail + Contacts + Calendar) — DONE 2026-07-12.**
  A single Takeout of `web@` **excluding Drive and Photos** (those already preserved —
  Drive copied in step 2; Photos are the drive-02 `tgk` master, 98 GB, already on B2)
  captured everything account-locked: **Mail 9 GB, Contacts, Calendar + all small service
  exports** (Chat, Fi, Wallet, Keep, Tasks, YouTube, Pixel, etc.). Total 4.95 GB, 4 zip
  parts. Archived to Backblaze B2 at `b2archive:gk-drive-archive/_google-account-web@/takeout-2026-07-12/`,
  rclone-check parity verified (0 differences, 4/4).
  - **Method (new standard — never touches the LAN):** Takeout → delivery **"Add to Drive"**
    (lands in `web@` Drive) → `rclone` on **Mesquite** (cloud node) copies Drive→B2
    cloud-to-cloud. Baobab/LAN never hold the data. `webdrive:` remote (web@ OAuth) added to
    Mesquite's rclone.conf.
  - **Superseded:** the earlier 6×50 GB full Takeout (with Drive+Photos) was ~99.9% redundant
    (photos already in the tgk master) — abandoned in favor of this Drive/Photos-excluded export.
  - **QUEUED follow-up (not a teardown blocker) — searchable old mail in tgk@, the right way:**
    Gmail's "Import mail and contacts" is broken for Workspace-source accounts (POP "could not
    validate" even with an app password — tried 2026-07-12, abandoned). Do it instead by pushing
    the **archived MBOX (on B2) into tgk@ over IMAP**, agent-driven from the cloud side (no LAN,
    no founder UI-fighting). Needs one thing from Gil: a **tgk@ app password** for IMAP write.
    Deferred at founder's request 2026-07-12 (decide/schedule later).

### Phase C — Tear down web@ (open)

- [ ] 8. Change default domain on Google Workspace (and remove web@ domain?)
- [ ] 9. Delete email attachments (various accounts) — storage reclaim
- [ ] 12a. **Final catch-up export of `web@` Photos** (full Takeout, `.zip`, 50 GB parts)
  — sweeps up photos taken between the last pull and the 2026-07-03 account flip. Land
  in `/home/gil/drive-archive`, dedup + verify + rclone to B2, THEN proceed to 12.
- [ ] 12. Delete Drive and Photos from `web@` (only after Phase B verified).
  **TEARDOWN GATE (2026-07-12):** `web@` Drive still holds an **`OBSOLETE/` folder = 86.8 GB**
  (old Accounting, Business/Baldwin scans, "g-drive tgk@ 2020" personal zips, Stacey backups).
  The name implies it was already moved out, but 86.8 GB is not deleted on faith — confirm it
  is present in the B2 archive (or explicitly discard it) BEFORE deleting Drive or closing the account.
- [ ] 11. Phone: remove `web@` and `gil@b` accounts (bug-test first)
- [ ] 13. Remove `web@` from all devices (phone, Chromebook)
- [ ] **Final: shut down the mailbox / cancel the `web@` Workspace seat.** Confirm
  forwarding still routes anything stray, then close it out and stop the billing.

---

## SSO / linked-apps review (2026-07-03)

Concern: many services log in via `web@` Google SSO, which would break at teardown.
**Reviewed all three accounts' linked-apps lists — no hard blockers found.** `web@`
can be torn down without losing anything critical.

**Resolutions (web@ Tier-1 candidates, all cleared):**
- **Tailscale** — already moved to `gil@b`; web@ entry is a stale leftover. No action.
- **Stripe** — logged in via web@ SSO: shows "Finish setting up" = abandoned/incomplete
  signup, no bank/charges. Not a real account. Let it lapse.
- **Google TV Streamer** — device gone. No action.
- **rclone** — just an OAuth token, not data. Re-auth (`rclone config reconnect`) to
  `tgk@`/`gil@b` if any remote complains after teardown. Not a blocker.
- **YouTube on TV** — device pairing; re-sign-in with `tgk@` if/when needed.

**Soft residual (not a blocker):** Tier-2 SaaS whose *only* login may be web@ SSO —
ChatGPT, **LinkedIn**, Figma, Webflow, Airbnb, Hipcamp, Nord, Zoom, Spotify, Reddit.
Convert the ones worth keeping (LinkedIn especially) to a `tgk@`/password login before
teardown; let the rest go. Tier-3 junk (JustWatch, NYT Games, FrictionlessParking,
AmpereTime, nvidia mdarcy, WhatsApp) — ignore.

**Linked-apps inventory (snapshot 2026-07-03):**
- `web@gkasparek.com` (22): Airbnb, AmpereTime, ChatGPT, Figma, FrictionlessParkingLogin,
  Google TV Streamer, Hipcamp (x2), JustWatch, LinkedIn, Nord Account, nvidia mdarcy,
  NYT Games, rclone, Reddit, Spotify, Stripe, Tailscale, Webflow, WhatsApp, YouTube on TV, Zoom.
- `tgkasparek@gmail.com` (4): rclone, rclone-for-gphotos, Spotify, The New York Times.
- `gil@buttonsimple.com` (40): AngelList, Calendly, Chatbot, ChatGPT, Claude by Anthropic,
  Claude for Gmail (x2), Claude for Google Drive, Cloudflare Dashboard, Convex,
  DigitalOcean, draw.io, Export Sheet Data, Figma, Fiverr, Formaloo, GitHub, GNOME,
  Google Cloud SDK, GPT for Sheets and Docs, IconScout, LambdaTest, Make, Medium,
  Midjourney, monday.com (x2), OpenAI, OpenArt, Penpot, rclone, Recraft AI, Resend,
  Sanity, Slack (x2), Tailscale, Vecteezy, Webflow, Webstudio.

## Notes / gotchas

- Order matters: nothing gets deleted from `web@` (steps 9, 12) or the account closed
  until Phase B exports are verified present at their destination + offline backup.
- grsync photo comparison (step 3) is the gate on photo deletion.
- Billing only stops at the final shut-down step — that's the actual cost goal.
