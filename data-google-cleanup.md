# Data — Google Account Cleanup

**Last Updated:** 2026-07-15

**Stacey external-share fix (2026-07-15).** Sharing 'Stacey's Content' with an outside
address failed: *"cannot be shared outside of Gil Kasparek."* Root cause: the slice was
uploaded to `bsdrive:` = the **gil@buttonsimple.com** business Workspace Drive (should have
been tgk@ per the consolidation plan), and that org had **external Drive sharing off**. Fixed
in Admin console: external sharing turned **on**, and the org's display name renamed
'Gil Kasparek' -> 'Button Simple' (it defaulted to the account holder's name). Tracked in
gov#83. Bulk source for the slice is already in B2 (under original source folders), so a
served B2 link remains an option if we later want Stacey off the org Drive entirely.

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
    **STARTED 2026-07-15:** app password provided; running detached on **Mesquite**
    (`~/mail-import/import.py`, log `import.log`, resumable via `import.state`). Source =
    the web@ Mail mbox pulled from B2 (`takeout-2026-07-12/...-7-001.zip` ->
    `web-all.mbox`, 9.67 GB, **117,566 msgs**, "All mail incl. Spam and Trash"). Uploads
    via IMAP into tgk@ under label **`web-archive`**. Hours-long (Gmail throttles); state
    file lets it resume. TODO after finish: confirm imported count vs 117,566, decide
    whether to prune Spam/Trash from the label, then delete Mesquite staging + the app
    password.

### Phase C — Tear down web@ (open)

- [ ] 8. Change default domain on Google Workspace (and remove web@ domain?)
- [ ] 9. Delete email attachments (various accounts) — storage reclaim
- [ ] 12a. **Final catch-up of `web@` Photos — DELTA ONLY, not a full re-Takeout.**
  A full Takeout re-pulls all ~98 GB we already hold in the `tgk` master; wasteful. Only the
  *delta* is needed: photos that landed in `web@` between the last pull and the 2026-07-03
  backup flip. Plan: size the delta first via rclone's Google Photos backend (date-scoped,
  read-only, from Mesquite); if trivial → skip. If worth keeping and metadata matters, do a
  **date-scoped Takeout** of just that window (rclone gphotos download strips GPS metadata).
- [~] 12. Delete Drive and Photos from `web@` (only after Phase B verified).
  **OBSOLETE sub-step COMPLETE (2026-07-16):** `rclone purge webdrive:OBSOLETE` finished;
  `rclone size webdrive:OBSOLETE` now returns "directory not found" — the 86.8 GB folder is
  gone from `web@` and verified present in B2. **The teardown gate on OBSOLETE is closed.**
  Original verification record (2026-07-15): `web@` Drive `OBSOLETE/` folder
  (~86.8 GB, old Accounting / Business-Baldwin scans / "g-drive tgk@ 2020" personal zips /
  Stacey backups) verified present in B2 at
  `_google-account-web@/web-drive-OBSOLETE` — **13,897 files matching, 0 real differences**
  (only 7 dangling shortcuts missing; 8 dirs unverified due to Google rate-limit, folder is
  founder-designated obsolete so accepted). Deletion from `web@` running on Mesquite
  (`rclone purge webdrive:OBSOLETE`, throttled). Remaining under step 12: the rest of Drive + Photos.
- [ ] 11. Phone: **demote `web@`, do not remove it** — make `tgk@` the phone primary (backup,
  Photos, Play, Wallet, identity) and leave `web@` signed in as a Gmail-only secondary. Android
  runs several accounts at once; this is deliberately not a cutover. Full plan: personal **p#19**.
  **UNBLOCKED 2026-07-16** — both gates now cleared:
  - SSO conversion checklist (below) — cleared by founder decision 2026-07-15.
  - Play purchase audit (the one real trap: paid apps/subs do NOT transfer between Google
    accounts) — **done 2026-07-16, and it came back empty.** No paid apps have ever been bought
    on `web@`; MLB+ was the only active subscription and the founder canceled it 2026-07-16.
    Nothing on `web@` is tied to a card any more.

  **System backup moved to `tgk@` (2026-07-16) — DONE, and it was a real gap.** The phone's
  Google **system backup destination** (app data, settings, SMS, call log) was still
  `web@gkasparek.com`; the 2026-07-03 flip moved **Photos only**. Had `web@` closed with system
  backup pointed at it, the phone's backup would have broken and the existing backup stranded in
  a dead account. Founder switched it in Settings > System > Backup; verified by reading the
  device (`adb shell dumpsys backup | grep destination` -> `tgkasparek@gmail.com`).
  Accepted cost: switching starts a **fresh** backup under `tgk@` — Google provides no way to
  migrate the old `web@` backup. Fine here (live phone re-uploads its state), but one-way.

  Remaining under step 11: nothing blocking. `tgk@` + `web@` both signed in, Photos on `tgk@`,
  system backup on `tgk@`, no paid apps. `web@` stays as the Gmail-only secondary per p#19.
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

## SSO conversion checklist (prioritized) — GATE on phone teardown (steps 11 & 13)

Retiring `web@` breaks any service whose only login is "Sign in with Google (`web@`)".
Dashlane does NOT fix this: it stores/fills a password, it can't detach an account from
Google SSO or move its email off `web@`. **Per-service action = set a password + change the
account email from `web@gkasparek.com` to `tgk@`, then save the new password in Dashlane.**
Links are best-guess to each service's login/security page.

**CAVEAT (2026-07-15):** the 22-app inventory below came from the `web@` Google
linked-apps list, which is **apps holding `web@` Google OAuth access — NOT proof the app
logs in via `web@` Google SSO.** Some are mere permission grants (e.g. Spotify — verified
NOT a Google login). Check each app's *actual* login method before converting; the real
conversion list is smaller than 22.

**GATE STATUS (2026-07-15): cleared by founder decision — Nord + ChatGPT converted, all
others deemed not worth converting. Steps 11 & 13 (remove `web@` from phone/devices) are
UNBLOCKED.** LinkedIn + Airbnb below were left unconverted by choice; if `web@` SSO to
either is ever needed again, convert then.

### Tier 1 — convert BEFORE teardown (real value, hard to recover)
- [~] **LinkedIn** — left unconverted (founder call 2026-07-15) — https://www.linkedin.com/psettings/sign-in-and-security
- [~] **Airbnb** (trip history / bookings) — left unconverted (founder call 2026-07-15) — https://www.airbnb.com/account-settings/login-and-security
- [x] ~~**Spotify**~~ — NOT a Google-SSO login (inventory was an OAuth grant, not the login method). No conversion needed; just confirm its account email isn't `web@`.
- [x] **Nord** (2026-07-15) — login switched to `tgk@` SSO. **Residual:** account email left as
  `web@` → password-resets/notices go to a dying mailbox; optionally change email to `tgk@`.

### Tier 2 — convert only if still used, else let lapse
- [x] **ChatGPT** (2026-07-15) — changed off `web@`.
- [~] **Figma / Webflow / Zoom / Reddit / Hipcamp** — **founder decided 2026-07-15: none of
  these matter, let lapse.** No conversion.

### Tier 3 — no action, let die / already handled
Stripe (abandoned signup), Tailscale (already on `gil@b`), rclone (token re-auth),
Google TV / YouTube-on-TV (re-sign the device), and junk: JustWatch, NYT Games,
FrictionlessParking, AmpereTime, nvidia-mdarcy, WhatsApp.

Once Tier 1 (and any kept Tier 2) are converted and Dashlane holds the new passwords,
steps 11 & 13 (remove `web@` from phone + all devices) unblock.

## The archived Takeout is a queryable answer surface (2026-07-16)

Reach for the B2 archive before poking the live `web@` account or a device. The Jul 12 Takeout
(`_google-account-web@/takeout-2026-07-12/`) is not just a preservation blob — it answers
questions. Part `...Z-6-001.zip` (39 MB) carries **43 service exports**, including a full
`Takeout/Google Play Store/` (Purchase History, Subscriptions, Library, Installs, Order
History), plus Google Pay, Wallet, Fi, Pixel, Chrome, Contacts, Calendar, Keep, Tasks, Maps,
Timeline. Inspect it from **Mesquite** (`rclone copy` the small part down, read with Python's
`zipfile` — note: `unzip` is not installed there). This is how the Play purchase audit got
answered with the live account untouched.

Corollary — **Play purchase ownership is NOT readable off an Android phone.** Verified on the
Pixel 10 Pro (2026-07-16): no root, locked bootloader (`verifiedbootstate=green`),
`com.android.vending` not debuggable, `/data/data/com.android.vending/` permission denied.
USB vs network adb makes no difference — same `uid=2000(shell)` either way. The Takeout export
or the Play Store UI are the only routes.

## Notes / gotchas

- Order matters: nothing gets deleted from `web@` (steps 9, 12) or the account closed
  until Phase B exports are verified present at their destination + offline backup.
- grsync photo comparison (step 3) is the gate on photo deletion.
- Billing only stops at the final shut-down step — that's the actual cost goal.
