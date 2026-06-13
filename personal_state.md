# Personal -- Current State

Last Updated: 2026-06-13 (session 22)
Status: Active

---

## Session 22 Notes (2026-06-13)

Farm-map: built a self-contained tool to match the survey sheets to the real world by
hand, with the machine doing the math. Files under farm-map/:
- digitizer/index.html -- open a survey photo, rotate it north-up, click the four outer
  tips (apexes) of the property against their known locations; at 4+ points it solves a
  photo-to-map fit (hand-rolled, no libraries) and draws the true outline back on in green.
  Same map frame as demo/index.html (POB-anchored SHIFT).
- digitizer/apexkey.js + apex-key.html -- shared diagram of the property north-up with the
  four apexes labelled (N/S/E/W); embedded in the digitizer as a draggable, resizable
  floating panel so the key stays visible while matching.
- serve.py -- tiny standard-library server that also accepts saves, so the digitizer
  auto-writes each alignment into source-data/transforms/<sheet>.json (no download/paste).
  Run: python3 farm-map/serve.py -> http://127.0.0.1:8099/farm-map/digitizer/index.html

Strategy shift (supersedes part of s21): manual clicking is tedious, so the direction is
machine-first / human-validates -- auto-fit the boundary per sheet + pull colour-keyed
features (water, stand dots, trails), then Gil + the hunt-club fellas validate/correct in
the browser; the digitizer becomes the correction tool. Tooling check: numpy + Pillow are
on baobab; still need scipy/scikit-image/shapely (NOT installed -- pending OK) and a
decision on remote vs local validation hosting (lean local-first). Still open from s21:
sheet dating for 02-05 (step 1, photos already pulled) and the free GIS-neighbor pull to
decompose the ~195 ac balance (step 3). Farm = personal issue #4.

---

## Session 21 Notes (2026-06-13)

Farm-map alignment + extraction strategy.

Registration FIXED: the survey<->parcel vectors didn't align because the s20 +193E/
+110S shift was a floating least-squares fit. Re-registered by pinning the survey's
southernmost apex (POB) to the parcel's south corner -- pure translation
(SHIFT = -0.0011753 lat, +0.0019292 lon). Survey E/S/W edges now sit on the parcel
boundary; the divergences are real (NW ~195 ac second tract + ~6 ac south sliver).
Demo (farm-map/demo/index.html) rewritten so one SHIFT constant drives both the green
vector and the raster overlay. Confirmed the survey polygon's SHAPE is from the plat's
43-course bearing/distance table (closes 0.00 ft), NOT a photo trace -- so boundary
accuracy is independent of image quality.

Raster warp attempted + deferred: the original sheet-07 photo has real keystone + paper
fold. Auto-georeferencing (homography ICP, grid search) kept locking onto interior ink
because the plat has three heavy lines (boundary, roads, transmission corridor).
Verdict: a warped image isn't needed for extraction (need a pixel->world transform);
a clean backdrop warp is an interactive job (QGIS / digitizer), not headless.

Strategy decided: vector extraction is the priority. Trace from highest-res source in
native pixels -> per-sheet homography (boundary = control on every sheet) -> fuse sheets
via shared features as tie-points (brace the interior, fix the fold) -> validate layer
by layer. Speced in farm-map/vector-pipeline-spec.md (digitizer tool + data model +
layer catalog + phases + sheet-dating/feature-currency). NOT built (spec only).

Next: (1) deduce each sheet's date (1995 known for 07/06; 02-05 undated) -- hints at
which features are still real; (2) build digitizer P1; (3) free GIS-neighbor pull to
decompose the acreage. Farm = personal issue #4.

---

## Session 20 Notes (2026-06-12)

Farm-map: resolved the 611-vs-409 acreage puzzle. Pulled the Beacon/Schneider
parcel record for 091-00-00-073-000: K-Farm LLC (c/o Gene A. Kasparek), 604.69
deeded ac, single 1994 deed (Book 668-98, $503k, Ward W.B. Jr -> K-Farm; plats
Cab C Slide 37 & 5). So the 409.258-ac Ashview survey is ONE tract of a single
1994 purchase, not a "land added later" event; the ~195-ac balance is the rest
of the same deed. Full record + reconciliation stored in property-mapping.md
(committed 91eaa5b). Deed/plat images need the $5/day Avenu pass or the Clerk
(free archive viewer stops at 1984; our docs are 1994-95) -- parked, not blocking.

Demo (farm-map/demo/index.html) rebuilt: county parcel (cyan) now the
authoritative boundary; basemap switcher (Esri / USGS imagery / USGS topo);
1995 survey tract registered onto the parcel by a rigid +193 m E / +110 m S move
(rotation ~0; edges tie at 3.6 m RMS) -> it's the SE tract, extra acreage is
N/NW. Survey-sheet raster moved with green and rotated +1 deg CCW (rotated-overlay
plugin). Open polish: exact tie-point refinement of green<->blue (3.6 m is the
survey-vs-GIS-digitizing floor); confirm overlay rotation direction/magnitude.
Next visible win: digitize the lake/water layer off sheet 06.

---

## Session 19 Notes (2026-06-12)

NYT Crossword daily auto-delivery -- PLANNED, not built ("do it later").
Goal: a cloud job that fetches the day's NYT Crossword PDF and emails it to Gil.
HOME DECIDED: personal repo, GitHub Actions on a cron -- runs in the cloud so no
fleet node need be awake, runs Python natively (for xword-dl), and encrypted
Actions secrets hold the NYT auth + email creds (never in the repo). Rejected:
Cloudflare Worker (no Python, more plumbing), Convex (it's the product backend,
org-bound). DELIVERY = email the PDF; a cloud runner can't reach a LAN printer,
and Gil doesn't need an email-to-print printer (the only hands-off-print path).
FETCH options: the NYT print-PDF endpoint
(.../svc/crosswords/v2/puzzle/print/{Mon}{DD}{YY}.pdf) sent with the NYT-S
subscription cookie, OR xword-dl with username/password (logs in fresh).
SCHEDULE ~6am ET (puzzle posts 10pm ET the night before; 6pm Sun for Sunday).
Effort ~30-60 min, almost all of it getting auth working once.

OPEN (resolve before building):
1. Does Gil have the NYT Crossword subscription? Separate paid add-on -- hard blocker.
2. NYT login method: email+password (script logs in fresh every run, zero
   maintenance) vs Google/Apple SSO (no password to script -> forced onto the
   manual NYT-S cookie pull, refresh every few months when it expires).
3. Email sender + destination: Gmail app password (SMTP, simplest) vs a personal
   Resend account; and which address to send to.

---

## Session 18 Notes (2026-06-11)

Investment proposal from Trea Floyd (CFP, Floyd McMillan Scott Group / Baird
Wealth), emailed Jun 9. Plan: invest $75k of $100k; $25k stays in money market
as a cash-flow buffer. Stated goals: high return, diversified, tax-sensitive.
Two strategies offered, Trea says either fits:
- **PFF 100** -- globally allocated, all-ETF portfolio (you see fund tickers
  only, no individual company names). Simple, cheap, tax-efficient.
- **BT Core + Satellite** -- same global allocation but a CORE of 25-30
  individual large-cap stocks (visible by name) plus ETF SATELLITES for the
  harder-to-hold categories (international, small-cap). The "BT Large Cap
  Equity" PDF is the stock core. Trea names visible stock names as the "biggest
  difference."

**KEY FACT (the hinge): two accounts are involved -- (1) a TAXABLE cash-savings
account and (2) a Roth (Rollover) IRA.** This drives ASSET LOCATION, not just
strategy choice. Tax-loss harvesting and individual-stock tax control only help
in the TAXABLE account. Inside the Roth, all growth is tax-free and harvesting
is useless -- so "sensitive to taxes" is moot there, and the Roth should take
the simpler/cheaper ETF approach (PFF-style). Verify the exact IRA type with
Trea ("Roth (Rollover)" is ambiguous -- a Rollover IRA is usually Traditional;
a true Roth changes nothing about the tax-free conclusion but confirm it).

OPEN QUESTIONS for Trea before deciding: all-in annual cost of each (advisory
fee + fund expense ratios, core vs satellite broken out); does BT Core do
automated tax-loss harvesting; expected turnover / historical cap-gains
distributions; and which strategy goes in WHICH account. Attachments (the two
PDFs) not yet reviewed -- Gil to share for holdings/fee detail.

NEXT: Gil gets the answers from Trea, then decide allocation per account
(likely: ETF/PFF in the Roth; consider BT Core only if the taxable account is
where the harvesting edge can pay off).

---

## Session 17 Notes (2026-06-09)

Trashed mountain bike rear derailleur -> derailleur-free conversion. Created #12
(priority: now, type: errand). Plan: anchor on the middle chainring of the triple.
Path A (free) -- shorten chain to a "magic gear" single-speed on the middle ring;
1 gear, no purchase, do this first. Path B (3-speed) -- add a ~$15-30 chain
tensioner on the hanger to keep all three front rings shifting; only path to 3-speed
(a fixed chain can't stay tight across ring sizes). Caution logged: size the cut to
the middle ring, trim a couple links at a time, don't over-cut or a later tensioner
build won't reach the big ring. Open: terrain/gearing, hanger-straight check, photos.

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
