# Personal -- Current State

Last Updated: 2026-06-08 (session 16)
Status: Active

---

## Session 16 Notes (2026-06-08)

Cedar machine: personal repo was not present -- cloned fresh from GitHub.
gh CLI not authenticated on Cedar (git push works; gh issue creation does not).

Electrical puzzle (farm): two switch banks (1-4 south, 5-6 north) controlling
four light banks (A-D east-west). South bank is clean 1:1 (1→A, 2→B, 3→C,
4→D). North bank both switches mis-wired: SW5 landed in parallel on B's circuit
(should be A via 3-way); SW6 landed in series on A's circuit using NC contact
(should be B via 3-way). Two mistakes: crossed wires + wrong terminals. Fix:
pull north bank, rewire SW5 and SW6 as proper 3-way switches to A and B
respectively. North bank pull scheduled tomorrow.

GitHub issue not filed this session (gh not auth on Cedar). File in next session.

---

## Session 15 Notes (2026-06-07)

Personal issue-board triage (all changes live in GitHub Issues, not files):
- Closed #1 (trip AI audit) and #3 (Don/Mailchimp -- resolved pay-per-use; list
  trimmed under 250, downgraded to free, billing pointed at Don, no Jun 13 recharge).
- Priorities reset: #8 Google cleanup + #9 drive consolidation -> now (this week);
  #10 security audit -> someday (~3mo); #2 terbinafine -> someday, self-managed,
  revisit ~Jul 7.
- Farm is now a standing category (type: farm): #4 stays the mapping project; new
  farm items get their own issues. Created #11 Starlink residential dish install.
- Mobile: #5 reframed as the "Mobile OS for Gil" umbrella; #6 broadened to "control
  Spotify from AI on mobile" as a child of #5.
- VR (NEW, app repo #94): portable VR work environment for travel/van (code + run
  the business), NOT an app feature; app<->VR interaction parked as secondary.
  priority: now / type: infra. Dedicated thread to pressure-test the rationale
  (~30 min VR may beat the burdensome monitor/kbd/mouse rig; may supersede the
  deferred van display/input item), then procure (leaning Quest).

Open meta-decision (acute): business tasks are scattered across buttonsimple-app
issues, button-simple-governance issues (stale), and the stale org project board
(s204). Gov repo lacks the type:/priority: label scheme. Pick ONE home before
moving VR #94 to gov.

---

## Session 14 Notes (2026-06-07)

Georeferenced sheet 07 for the farm map. Reconstructed the boundary exactly from
the plat's 43-course bearing/distance table -- traverse closes 0.00 ft and computes
to 409.258 acres, matching the plat label to the thousandth (these are the
surveyor's balanced figures). Committed the boundary spine at
`farm-map/source-data/sheet07-boundary.geojson` + `.kml`: exact shape in WGS84,
all courses/area/closure/provenance embedded, anchored to county parcel 073
centroid (shape exact, position good to ~tens of m; grid vs true north <0.1deg).
Built a self-contained browser demo at `farm-map/demo/index.html` -- Esri satellite
+ exact boundary vector (green) + the 1995 survey sheet draped as an image overlay
(2-point similarity warp: North apex + POB) with an opacity slider and layer
toggles. Finding confirmed: parcel 073 (610 ac) is a genuinely different boundary
from the survey (different parcel ID, edge bearings don't match) -- good for
approximate position only, not edge-tie. Next: tighter raster alignment via
thin-plate-spline with 8-15 GCPs (absorbs paper curl); then trace the water/lake
layer into the same frame.

---

## Session 13 Notes (2026-06-04)

Filed Chester County's digitized parcel boundary into the farm project. Two Downloads
files (`Chester.kml`, `Chester.kmz`) were the same polygon -- county parcel
091-00-00-073-000, folder named "Farm." Kept the full-precision KML at
`farm-map/source-data/chester-county-parcel-073.kml`; discarded the lossy 6-decimal
KMZ. **Finding:** the county parcel computes to ~611 acres vs the 1995 deed survey's
409.258 (verified, not rounding). Two boundaries, different extent -- likely land
added since 1995. Logged in property-mapping.md as the georeference control layer plus
an open reconciliation task. Next: georeference sheet 07 against the county boundary,
then locate the extra ~200 acres.

---

## Session 12 Notes (2026-06-04)

Ingested the farm-map source art. Seven photographed survey plats of the Kasparek
family farm (~409 acres, Chester SC; Ashview/Ashmark survey, Aug 1995 rev Oct 1996)
copied from `~/Documents/farm-map/` into the repo at `farm-map/source-art/` with
descriptive names, checksum-verified against the untouched originals. Wrote
`farm-map/source-art.md` (property facts, per-sheet contents, annotation key,
digitization notes) and pointed property-mapping.md's Mapping Foundation at sheet 07
(deed survey, NAD 1983 / S.C. Grid North -- the georeference anchor) and sheet 06
(master legend + the lake missing from modern topo). Next: georeference sheet 07.

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

Personal tasks are now tracked in **GitHub Issues**:
https://github.com/gil-buttonsimple/personal/issues

- AI-conversation audit from the 12-day trip -> #1 (pending tail: GitHub-repo-access
  threads, remaining voice/hands-free content)

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

Active personal tasks now live in **GitHub Issues**:
https://github.com/gil-buttonsimple/personal/issues

Migrated 2026-06-07 (full context preserved in each issue):
- Terbinafine course -> #2
- Don Baldwin client check-in -> #3
- Farm / property mapping -> #4
- Mobile operating profile / multi-AI driving workflow -> #5
- Spotify taste session -> #6
- Vision correction -> #7
- Google account cleanup -> #8
- Hard drive consolidation -> #9
- Personal security audit (new capture) -> #10

### Gov-domain items (pending routing to the governance repo -- NOT migrated to personal Issues)

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

- **Suggestions for business canon:** Personal boot never writes to business canon
  directly. Items identified this session with work application: multi-AI workflow
  method (workflow-multi-ai-audit.md). Raise in a gov session.
