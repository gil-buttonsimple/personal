# Personal -- Current State

Last Updated: 2026-05-14 (updated Google cleanup detail)
Status: Active

---

## Migration Status

Migrated from Google Drive (`_personal_gk` folder) to local repo on 2026-05-14.

Files converted from Drive ZIP and committed locally:
- `vehicle-eurovan-profile.md` -- from Drive doc
- `vehicle-eurovan-loft-bed.md` -- from Drive doc
- `health-cholesterol-plan.md` -- from Drive doc
- `finance-canon.md` -- from Drive doc
- `finance-balances.csv` -- converted from Drive XLSX (187 rows)

Drive folder (`_personal_gk`) is now superseded locally. Originals can be deleted from Drive once GitHub repo is live.

---

## Open Items

- **Fix personal GitHub repo (https://github.com/gil-buttonsimple/personal):**
  Repo exists but is not accessible from Claude Code. Investigate: repo visibility
  (public/private), Claude Code git credentials, SSH vs HTTPS configuration for
  the gil-buttonsimple account. Until fixed, files live locally at
  /home/gil/Documents/Personal/. Needed to back the `boot personal` mode.

- **Delete Drive originals (_personal_gk folder):** Once GitHub repo is accessible
  and files are confirmed committed, delete the superseded Drive docs. Delete list
  (with IDs) is in the `_current-state.docx` from the Drive ZIP export.

- **Google clean-up:** Migrating `web@gkasparek.com` off Google Workspace to reduce cost.

  Accounts: `gil@buttonsimple.com` (Workspace, keeping), `web@gkasparek.com` (Workspace,
  migrating out), `tgkasparek@gmail.com` (free Gmail, destination)

  | # | Task | Status |
  |---|---|---|
  | 1 | Redirect email: Namecheap DNS forward web@ to tgk@ | Done |
  | 1.5 | Phone: add tgkasparek@gmail.com | Done |
  | 2 | Copy Google Drive contents | Done |
  | 3 | Copy Google Photos | Done -- verify with grsync comparison |
  | 4 | Expand Drive docs | Done |
  | 5 | Clean up files (remove largest, pull out photos/videos) | Done |
  | 5.5 | JSON fix | Done |
  | 6 | Merge + deduplicate photos | Done |
  | 7 | Copy emails | Next -- method TBD |
  | 8 | Change default domain on G-Workspace (and remove?) | Open |
  | 9 | Delete email attachments (various accounts) | Open |
  | 10 | Contacts | Test |
  | 10.5 | Calendar | Test |
  | 11 | Phone: remove web@ and gil@b (bug test first) | Open |
  | 12 | Delete Drive and Photos from web@ | Open |
  | 13 | Remove from all devices (phone, Chromebook) | Open |

  Open question (step 1): send-from `web@gkasparek.com` is working but custom domain
  email likely cannot stay on free Gmail -- may need Workspace or alternative provider.
