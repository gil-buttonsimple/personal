# Personal -- Current State

Last Updated: 2026-06-04 (session 11)
Status: Active

---

## Session 11 Notes (2026-06-04)

Split the Google cleanup out of personal_state into its own project file and
established a `data-` domain for digital-data consolidation. Two sibling projects:
`data-google-cleanup.md` (web@ Workspace teardown -- 13 steps reorganized into
preserve/teardown phases; live step is preserving web@ email) and
`data-drives-consolidation.md` (3-5 hard drives to review/dedup/consolidate; stub).
They share a cloud + offline-backup end-state, decision owned by the drives doc.
Reconciled the 2026-06-02 inbox conflict: web@ is a real mailbox, preserve-then-
shut-down (not keep, not skip-copy); marked converted. README indexed + relationship
map updated.

---

## Session 10 Notes (2026-06-04)

Started a single consolidated meds tracker: `health/health-medications.md`
(no per-drug files). Active course recorded: terbinafine 250mg once daily,
June 4 -> July 3, day 1 taken. Daily-meds section stubbed pending the
Fadem med list. Watching scalp flaking as a possible fungal side benefit
(check-in ~Jun 17).

---

## Session 9 Notes (2026-06-01)

The personal/business line was redrawn in a gov session: infrastructure
(machines, network, connectivity, mobility) is now a governance/business domain.
The VW Eurovan is business. The three vehicle files (rebuild profile, loft bed,
trip notes) were merged into the gov repo at architecture/vehicle_eurovan.md and
removed from here. Personal now holds only finance, health, friends, and side
businesses. The fleet model (Baobab reference node, Cedar mirror + vehicle
overlay) and the new infrastructure.md live in gov.

---

## Session 8 Notes (2026-06-01)

Baobab is the new desktop replacing the old Bosgame box (now "Cedar", destined
for permanent VW onboard install -- see vehicle-eurovan-profile.md + the Starlink
wired-in-bus finding in Open Items). Built the Cedar -> Baobab migration plan
below. Scope deliberately narrow per Gil: Cedar = move projects off only (not a
wipe; personal data + destination still TBD); Baobab = apps (set TBD) + Claude
settings. Dev-tooling side is parked for a gov session.

---

## Baobab / Cedar Migration (session 8)

Executable plan. Run when Cedar is in front of you. Unknowns are flagged as
decision points, not blockers.

### Part A -- Move projects off Cedar

A1. **Reach Cedar.** Power on, confirm on LAN (`ip addr` on Cedar). From Baobab:
    `ping <cedar-ip>` and `ssh gil@<cedar-ip>` (or work at Cedar directly).

A2. **Inventory projects.** On Cedar: `ls -la ~/dev` (and anywhere else code
    lived). Sort each into repo vs. non-repo.

A3. **Repos -- find anything not on GitHub.** Per repo:
    - `git status` (uncommitted changes?)
    - `git stash list` (stashed work?)
    - `git log --branches --not --remotes --oneline` (local commits never pushed)
    Unpushed commits -> `git push`. Uncommitted/stashed work worth keeping ->
    commit & push or copy the working tree out. Nothing local-only -> already safe.

A4. **Non-repo projects -> pull to Baobab.** From Baobab:
    `rsync -av gil@<cedar-ip>:~/dev/<project>/ ~/dev/<project>/`
    (Destination is a parked decision; `~/dev/` is the default.)

A5. **Verify, then clear.** Confirm each project opens/builds on Baobab or is
    safely on GitHub. Only then is Cedar "projects-clear." Personal data stays
    on Cedar -- out of scope.

### Part B -- Baobab desktop

B1. **Claude settings -- diff before clobbering** (Baobab already has a live
    `~/.claude/settings.json`):
    `scp gil@<cedar-ip>:~/.claude/settings.json /tmp/cedar-claude.json`
    `diff /tmp/cedar-claude.json ~/.claude/settings.json`
    Merge anything missing (permissions, paplay completion-sound Stop hook) into
    Baobab's file. Do not overwrite.

B2. **Apps.** Maintain a running list as they surface. Install apt-first (matches
    the dev-machine convention: no snap/fnm/bun). Add each app here as needed.

### Parked -- needs a gov session (personal mode can't touch the gov repo)

- tech_stack v1.5 edits: Bosgame -> Cedar rename; machines/network tables.
- Gov "Extract from Cedar" In-Flight item (dev settings.json, config notes).

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
  - ChatGPT: partial -- a mobile-notes batch ingested 2026-06-03. Routed: product
    ideas -> gov roadmap.md Backlog; farm/property project -> property-mapping.md;
    VW tire leak -> gov vehicle_eurovan.md; Don Baldwin client task -> Open Items
    below. Still pending: the GitHub-repo-access threads and any remaining
    voice/hands-free content.

---

## Migration Status

Migrated from Google Drive (`_personal_gk` folder) to local repo on 2026-05-14.

Files converted from Drive ZIP and committed locally:
- `vehicle-eurovan-profile.md` -- moved to gov (architecture/vehicle_eurovan.md) 2026-06-01
- `vehicle-eurovan-loft-bed.md` -- moved to gov (architecture/vehicle_eurovan.md) 2026-06-01
- `vehicle-eurovan-bus-trip-notes.md` -- moved to gov (architecture/vehicle_eurovan.md) 2026-06-01
- `health-cholesterol-plan.md` -- from Drive doc
- `finance-canon.md` -- from Drive doc
- `finance-balances.csv` -- converted from Drive XLSX (187 rows)

Drive folder (`_personal_gk`) deleted 2026-05-26. Local ZIP export also deleted. GitHub is sole source of truth.

---

## Open Items

- **Terbinafine course -- ACTIVE (June 4 -> July 3, 2026):** 250mg once daily ~11am
  for toenail fungus. Daily tracking grid in `health/health-medications.md`.
  Last dose July 3. Confirm with prescriber whether a 4-6 week LFT check is needed.

- **Don Baldwin (private client, not Button) -- TIME-SENSITIVE (2026-06-03):**
  check in with Don, and coordinate an email blast with him within the next few days.

- **Farm / property mapping project:** full scope captured in property-mapping.md
  (mapping foundation, data layers, outputs, voice-first field data collection,
  recreation + ecology layers, property logistics / Amazon drop). Active side project.

- **Starlink Mini -- wired vs WiFi findings (2026-05-28):** Wired ethernet is significantly better than WiFi through an exterior wall. Test results: download +57% (59 to 93 Mbps), ping -74% (138 to 37 ms), jitter -74% (68 to 18 ms). Upload flat. Implications: (1) House: run wired ethernet from Mini to dev machine; use outdoor CAT6 for any exposed section. (2) Vehicle (VW bus): metal body blocks WiFi nearly entirely -- wired is the only reliable option for any permanent bus install. Any in-vehicle Starlink setup requires a physical ethernet run. Expense as business cost once Starlink is used for work.

- **Eurovan GPS + OBD2 data logger plan:** Stratux VK-162 G-Mouse (u-blox 7)
  confirmed working on /dev/ttyACM0. Gil added to `dialout` group. Plan:
  1. Install gpsd (`sudo apt install gpsd gpsd-clients; sudo systemctl enable gpsd`)
  2. Add udev rule for persistent /dev/gps0 symlink (vendor 1546, product 01a7)
  3. OBD2 adapter purchased; add `python-obd`
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

- **Google account cleanup** -- see [data-google-cleanup.md](data-google-cleanup.md).
  Retiring `web@gkasparek.com` off Workspace (preserve data, shut down; keep
  `gil@b`, land on `tgk@`). Next: preserve web@ email (step 7), then tear down.

- **Hard drive consolidation** -- see [data-drives-consolidation.md](data-drives-consolidation.md).
  3-5 drives of mixed content to review, catalog, dedup, consolidate into cloud +
  offline backup. Stub; content review not yet started.
