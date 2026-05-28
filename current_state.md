# Personal -- Current State

Last Updated: 2026-05-28 (session 7)
Status: Active

---

## Session 7 Notes (2026-05-28)

vehicle-eurovan-profile.md task list audited and restructured: redundant tasks merged, completed tasks archived (head unit replacement done), 6x9/door panel audio path dropped in favor of subwoofer approach, rattle tasks consolidated under Starlink mount. Final list: 4 P1, 4 P2, 2 Decisions, 8 unprioritized.

---

## Session 6 Notes (2026-05-27)

vehicle-eurovan-profile.md restructured: replaced subsystem todo groups and Open Decisions section with a flat priority table (P1/P2/Deferred/Decision tags). Ignition/key retention archived as resolved. Misfire added as P1. Task tracking for the bus now lives entirely in vehicle-eurovan-profile.md.

---

## Session 5 Notes (2026-05-26)

vehicle-eurovan-profile.md updated with road trip findings:
- Audio: Alpine head unit confirmed current; passenger side crossover identified and bypassed; door woofer wired direct (4-ohm interim); 6x9 upgrade path documented (depth spacers needed)
- SRS: airbag light active (latching fault from unplugging SRS with battery live); VCDS Lite or VW handheld required to clear "Open Circuit" fault; clock spring / spiral cable identified
- Interior electrical: shifter illumination bulb holder identified and verified against spec

---

## Top Priority

- **Audit AI conversations from the past 12 days (by 2026-06-07):** Parse ChatGPT,
  Claude, and Gemini conversations from the bus trip for meaningful learning. Extract
  repair topics discussed, document what worked and what didn't for voice-command
  use while driving, and build a consolidated to-do list.
  - Claude Code sessions: done (voice/mobile setup, May 16-18)
  - Claude.ai export: done (Eurovan repair, voice findings -- see vehicle-eurovan-profile.md)
  - Gemini: done via in-app self-summary (shifter fix, audio shop, voice workflow)
  - ChatGPT: pending export -- at least 2 threads about getting ChatGPT working
    with GitHub repo (worth finding); also likely has voice/hands-free content

---

## Migration Status

Migrated from Google Drive (`_personal_gk` folder) to local repo on 2026-05-14.

Files converted from Drive ZIP and committed locally:
- `vehicle-eurovan-profile.md` -- from Drive doc
- `vehicle-eurovan-loft-bed.md` -- from Drive doc
- `vehicle-eurovan-bus-trip-notes.md` -- from Drive doc (added 2026-05-26)
- `health-cholesterol-plan.md` -- from Drive doc
- `finance-canon.md` -- from Drive doc
- `finance-balances.csv` -- converted from Drive XLSX (187 rows)

Drive folder (`_personal_gk`) deleted 2026-05-26. Local ZIP export also deleted. GitHub is sole source of truth.

---

## Open Items

- **Starlink Mini -- wired vs WiFi findings (2026-05-28):** Wired ethernet is significantly better than WiFi through an exterior wall. Test results: download +57% (59 to 93 Mbps), ping -74% (138 to 37 ms), jitter -74% (68 to 18 ms). Upload flat. Implications: (1) House: run wired ethernet from Mini to dev machine; use outdoor CAT6 for any exposed section. (2) Vehicle (VW bus): metal body blocks WiFi nearly entirely -- wired is the only reliable option for any permanent bus install. Any in-vehicle Starlink setup requires a physical ethernet run. Expense as business cost once Starlink is used for work.

- **Eurovan GPS + OBD2 data logger plan:** Stratux VK-162 G-Mouse (u-blox 7)
  confirmed working on /dev/ttyACM0. Gil added to `dialout` group. Plan:
  1. Install gpsd (`sudo apt install gpsd gpsd-clients; sudo systemctl enable gpsd`)
  2. Add udev rule for persistent /dev/gps0 symlink (vendor 1546, product 01a7)
  3. When OBD2 adapter arrives, add `python-obd`
  4. Build MCP server exposing `get_location` and `get_vehicle_data` tools
     so Claude Code has live GPS/OBD2 context during drive diagnostics.
  AI chat apps (Claude Android, ChatGPT, Gemini) cannot consume GPS directly --
  manual coordinate paste only, or a local HTTP endpoint as a workaround.

- **Mobile operating profile for Claude:** Deferred from May 14 session. Claude
  Android voice mode not ready for true hands-free driving use. Build a profile
  documenting workarounds and preferred AI per context. See workflow-multi-ai-audit.md.

- **Spotify taste session:** Started May 14 (Claude.ai), not completed. Export
  Spotify data and finish the discovery/rating session.

- **Vision correction:** Research prescription clip-on sunglasses ($15-90) for
  driving. Confirm Xtreme goggle model for swim lens compatibility.

- **Suggestions for business canon:** Personal boot never writes to business canon
  directly. Items identified this session with work application: multi-AI workflow
  method (workflow-multi-ai-audit.md). Raise in a gov session.

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
