# Personal -- Current State

Last Updated: 2026-06-24 (session 28)
Status: Active

---

## Session 28 Notes (2026-06-24)

Farm-map screensaver (natgeo.html) — Baobab-version feedback pass. Tracked under gov#26.

- **Cosmic open** (~12s, no text/no key): starts on a 3D globe in space, descends
  North America → United States → South Carolina → Chester County → Chester → K-Farm.
  Required **MapLibre v4.7 → v5** (globe projection is v5-only); confirmed rendering
  headlessly. Old gold title card and the legend/key box removed entirely.
- **Compass rose**, top-right: hidden in space, fades in at the South Carolina beat,
  tracks true north (counter-rotates the flyover spin).
- **All on-screen text → bottom-center yellow movie-subtitle style**, one short line
  at a time, black-outlined, held to read slowly. The descent narrates itself.
- **Roads reveal one at a time**: pulls the 5 named roads nearest the property from
  osm-roads-all.geojson, longest-first (Great Falls Highway leads, then side roads),
  each fading in under its own name. Replaces the single all-at-once paved layer.
- **POI line now derives from placed points** (poiSummary), so the narration can't
  claim a dam that isn't mapped (it was: code said "dam" but no pin existed).
- **place-points.html**: added **Dam/spillway** (marked MAP FIRST) and **The house**
  as priority-1 targets. Place them and they appear in the screensaver automatically.
- Open: dock & put-in sit ~250 ft apart — check for pin collision once the dam lands.
  Firestick copy is unaffected (separate hosted URL, not yet stood up).

---

## Session 27 Notes (2026-06-22)

Files project — pre-upload trim/compression pass on the staged `/home/gil/drive-archive`
(356 GB, 4 sources, deduped) before the Backblaze B2 push (#9, #14). Everything removed
is staged to `_TRASH` (reversible) until a final confirm; details in
[data-drives-consolidation.md](data-drives-consolidation.md).
- **Junk:** ~32 GB Batch-1 (installers/ISOs, `placelogic_OBSOLETE`, Postgres db dumps,
  DVD rips) staged; 13,449 OS-cruft files deleted; 5,926 empty dirs removed; Picasa
  caches (1.2 GB) staged.
- **GoPro H.264 → HEVC CRF 24:** 144 clips, **54.2 → 10.3 GB** (~44 GB saved), 0
  mismatches; spot-check page built; originals kept pending swap.
- **Non-GoPro H.264 → HEVC CRF 20:** ~52 GB / 432 files (mostly tgk Google Photos family
  video; Google holds originals) in progress; ~25–30 GB est. save. CRF 20 for memories.
- Open: folder taxonomy (organize before upload?); mine `72097` for portfolio first;
  then rclone → B2.
- Projected archive: ~356 GB → **~135 GB** before cloud.

---

## Session 26 Notes (2026-06-18)

Farm-map screensaver + a placement tool.

- **Lake fix**: replaced the bad sheet-06 blob water with the authoritative USGS NHD
  impoundment polygon (24.5 ac, perennial LakePond) in farm-map/source-data/derived/water.geojson;
  old blob kept as water-old.geojson. (committed ee07798)
- **natgeo.html** reworked into the screensaver: smooth continuous-drift flyover (5 patterns,
  one zoom-in excursion), progressive layer reveals (boundary, paved roads = OSM, trails =
  sheet 03 dashed, lake) each pulsing in and building a key, then all POI pins drop in a ~1s
  cascade, then the documentary "pages" (one morphing survey-sheet plate + sourced facts).
  Privacy-scrubbed (no surname, acreage, dollars). Real facts captured in
  farm-map/screensaver-facts.md (cited). Global 3x slow time-scale (TS, tunable; ?speed= to preview).
  POIs are point-only and load from farm-map/source-data/traces/poi-points.geojson (priority-1
  set: front gate, barn, dam, dock, boat put-in).
- **place-points.html** (new): web tool to locate points. Long prioritized list (18 across 3
  tiers), click-to-place + drag, auto-saves to source-data/traces/poi-points.geojson. All
  basemaps (Sentinel-2, USGS high-res aerial, USGS topo, USGS aerial+labels, OSM, OpenTopoMap),
  all reference layers, and the 7 georeferenced 1995 survey sheets as onion-skin overlays.
- **Marker offset bug -- RESOLVED**: the placed marker landing south of the click was NOT a
  HiDPI/Firefox scaling issue (that earlier guess was wrong). Cause: place-points.html defined
  `.pin{position:relative}` in its `<style>`, loaded after MapLibre's stylesheet at equal
  specificity, overriding MapLibre's `.maplibregl-marker{position:absolute}`. Because the custom
  marker element IS the `.pin` element, the marker root fell out of absolute positioning, so
  MapLibre's placement transform was added on top of the element's normal document-flow position
  (which runs downward = south). Confirmed MapLibre never sets `position` inline -- it relies
  solely on that class. Fix: `.pin{position:absolute}` (one line); the `::after` centre dot still
  anchors correctly (the pin is still a positioned ancestor). Plain clicks had always saved the
  true coordinate (display-only bug), so previously-placed points were correct on reload.
  natgeo.html and flyover.html were checked and are unaffected (their `.pin` is a nested child /
  uses a non-overriding class).
- **Placement list trimmed** to the 4 points actually wanted: front gate, barn, dock, boat
  put-in. Removed dam/spillway, cabin, shed, and the 9 other unplaced candidates (well, beaver
  dam, power line, culvert, ford, parking, camp, food plot, POB, landmark tree, mailbox); all
  recoverable from git history if re-added later. poi-points.geojson trimmed to the same 4.

---

## Session 25 Notes (2026-06-17)

Farm-map: stopped guessing at extraction and did the source read FIRST. Walked Gil
through all seven sheets; he said what each actually shows. Captured as the authoritative
**farm-map/source-map.md** (feature -> source sheet -> method). Key reframings:
- Most high-value features (lake boundary, rivers, road shoulders, power lines, electric-coop
  easement, emergency spillway, fences, flood area, woods/open) are SHARP UNIFORM black lines
  on the clean base -- colour can't separate them. They need HAND-TRACING with Gil labeling
  which line is which. Auto colour-extraction only works where a feature is its own colour
  (red stands on 04, orange/green road+trail network on 03/02).
- The blue "water" highlighter is NOT a water source -- it overlays creek/contour lines
  available cleaner elsewhere. The real water data is the base linework. The earlier
  sheet-03-blue water extraction (built this session, three tries: points -> creek-lines)
  was DROPPED. Water reverted to the sheet 06 lake blob as a rough INTERIM, pending a
  hand-traced lake from sheet 07 (the cleanest base, already georeferenced).
- Sheet 07 is the master hand-trace base. Sheet 04 base is unusable (uniform shading, many
  meanings). Sheet 02 green = some roads (not "trails"); 03 orange = roads/trails.
- Road/trail tiers must be classified, not lumped: Main road (to barn) / dirt road /
  2-track-ATV / foot trail. Public roads stay from OSM; these are the internal network OSM lacks.

Built the tool for this: **digitizer tracing mode** (farm-map/digitizer/index.html). New
"Trace features" mode alongside the georeference mode: pick a label (taxonomy of 14 across
Roads&trails / Water / Infrastructure / Land cover / Point), click along a feature on a
georeferenced sheet, machine projects each click through the sheet homography. Lines for
roads/creeks/fences/power; polygons (auto-closed) for lake/flood/woods; points for POI.
Finish/undo/cancel, per-feature delete, auto-save to source-data/traces/<sheet>-traces.geojson
via serve.py (kind:trace), and restore-on-reload. Demo (demo/index.html) gains a dynamic
"Traced features" section that loads any *-traces.geojson, grouped by label, coloured per
feature. Full save round-trip verified headless (POST -> file -> demo renders grouped toggles).

Also finalized extract_all.py to a consistent state: dropped sheet-03 water, restored sheet-06
lake as interim water.geojson, relabeled the fused 02+03 network "roads & trails (unclassified)"
(tiers come from hand-tracing). Stands (52) and food plots (34) unchanged.

Tried then DROPPED a "vectorize sheet 07 + deduce every line's class from the other
registered sheets (colour votes)" approach -- bunk: water massively over-claimed (washy
sheet-06 blue + big match radius), ~7200 text/fragment pieces. Boundary is already known
(deed traverse + county parcel), so it was never needed from this. Founder's call: go
FEATURE BY FEATURE from the best source, compare sheets, and learn.

Roads & paths (roads_compare.py): extracted the network from each colour sheet separately
(NOT fused) + clear_border to drop the wood-table band -- this fixed sheet 03 (2645 noisy
fragments -> 410 clean). Verdict on the satellite: SHEET 03 ORANGE is the accurate, complete
network and lands on real tracks; sheet 02 green is partial (central/north only); sheet 05
brown is unusable (blends into aged paper). So roads = sheet 03. Shown as a "Roads by source
-- compare" section in the demo (toggle one at a time).

Key features to build (founder, s25), each from its best source: lake surface, waterways/
creeks, roads & paths (=sheet 03), POWER LINES, BUILDINGS (important -- barn + cabins/sheds),
deer stands (done, sheet 04), + food plots, fences/gates, dam+spillway, fields (open/woods).
Method split: colour-auto for roads (03) and stands (04); HAND-TRACE (digitizer tracing tool,
built this session) for buildings, lake surface, power lines, fences -- few, precise, clean
base lines. Creeks TBD (GIS/USGS NHD or trace).

LESSON (banked in source-map.md): walk the founder through what each source shows, and go
feature by feature from the best source -- don't auto-deduce everything at once. Next:
nail roads from sheet 03 (de-fragment/smooth), then move to the next feature (likely creeks
or buildings). Farm = personal issue #4.

---

## Session 24 Notes (2026-06-17)

Farm-map deep dive + demo rework. Investigated why the extracted layers "looked wrong."
ROOT CAUSE (found by drawing the known boundary onto each rectified sheet in a shared
frame and comparing): sheet 06's saved homography was bad -- its East-apex pixel click was
placed ~700 px off the true corner. Sheet 07, same method, aligned fine, proving the method
works when the clicks are right. Because water, food plots, AND stands were ALL extracted
from sheet 06, they inherited that bad georeference -- so they were misplaced at the source,
not merely drifting. This overturns the first read ("not a coordinate bug"): it WAS a
georeference bug, on sheet 06 specifically. Fixed: Gil re-clicked sheet 06's East apex in
the digitizer (coverage 85% -> 97%; boundary now tracks the drawn line); re-ran warp_sheets.py
+ extract_all.py -> water 19, food 34, stands 42 re-projected through the corrected homography.
Display issues also fixed in the rework (raster no longer draped over all; polygons no-fill;
layers off by default). Remaining limitation: still a single 4-point homography per sheet, so
the interior carries some keystone/fold wobble; adding interior control points (dam, road
junction) is the next lever -- DEFERRED per Gil ("another day unless accuracy becomes a
problem"). Roads look sparse because OSM has only the public roads (Great Falls Hwy, Hinton
Rd), not the farm's internal network. Trails confirmed noise (1062 fragments). Full write-up
in property-mapping.md ("Registration accuracy").

Demo (demo/index.html) rewritten per Gil's spec: default = basemap + county parcel only;
basemap switcher (Esri / USGS topo / USGS NAIP / none) + opacity; per-layer opacity sliders
(onion-skin one at a time); polygons no-fill by default + fill slider; 3 line-colour schemes
(bright/dark/white); stands off by default.

Boundary export regenerated: sheet07-boundary.geojson + .kml now POB-registered (raw
traverse + SHIFT; POB pinned to parcel south corner -81.1504182, 34.6483774), retiring the
session-14 centroid anchor (~200 m off at south). Demo doesn't read this file (it computes
its own SHIFT); it's the QGIS/external export.

Sheet dating: 02-06 are one 1995 survey (K-Farm Hunt Club, Aug 29 1995, 1"=400', Ashmark;
06 rev. Oct 18 1996; 07 deed survey Aug 1995 rev 1996) themed five ways; 03/04/05 are
magnetic-north thematic overlays of the same base. Sheets do NOT differ in date -- feature
currency must come from modern imagery, not sheet dates.

Validation (Gil, on satellite): water/food much better after the 06 fix. Stands re-sourced
from sheet 06 (blue dots, collided with the blue lake -> inflated/mislocated) to SHEET 04
(dedicated red flag markers); now extracted with NO ROI clip -- ALL 52 shown, tagged inside
(20) / outside (32) the property boundary, human culls. Founder CONFIRMED the stands.
Multi-sheet direction adopted (Gil): extract each layer from its dedicated sheet, cross-check
across sheets to decide what's real, and always show all data (even outside the property) --
don't let an auto-filter silently hide marks. Next dedicated sources: water from sheet 03,
trails from 02+03. Open: number plots (1-30)/stands DURING validation
(not blind -- 35 polys vs 30 legend nums); improve interior registration; better trail
source; GIS-neighbour pull to decompose ~195 ac still deferred. Farm = personal issue #4.

---

## Session 23 Notes (2026-06-17)

Farm-map: georeferenced all 7 survey sheets (digitizer, 4 cardinal apexes each;
transforms in source-data/transforms/) and did the first comprehensive feature
extraction pass. Installed scipy/scikit-image/shapely (apt). Pipeline in
farm-map/extract/ (featurelib.py + extract_all.py + fetch_osm_roads.py): HSV colour
isolation, ROI = known boundary inverse-projected onto each sheet (auto-drops the
legend/margins), geometry via skimage/shapely (points/polygons/merged polylines),
projected through each sheet's homography. Full write-up in
farm-map/extraction-pass-1.md.

Key reframing (Gil's call): digitize only what no other map has. Roads now come from
OpenStreetMap (180 ways, fetch_osm_roads.py), NOT extracted -- the old extracted-road
PoC was meaningless dots and roads already exist in GIS. Extracted from sheet 06 (the
cleanest photo): deer stands (42 candidate points), water/creek/lake (20 polygons,
coherent N-S drainage + pond), food plots/woods (35 polygons). Trails too faint on
every sheet to extract cleanly -- left rough/off-by-default; needs a better scan.

Georeference independently validated: registered south apex (POB) lands 5 m from
Hinton Rd / 9 m from Great Falls Hwy (the junction Gil named at the south point); SW
boundary runs along Great Falls Hwy. All layers live + toggleable in demo/index.html.
Stands/plots are machine-first candidates to validate in the browser. Farm = personal
issue #4. Open: validate layers; regenerate stale sheet07-boundary.geojson (older
centroid anchor, ~200 m off at south); number plots/stands per legend; date sheets 02-05.

Also added to digitizer this session: load-saved-work (revisit a sheet -> restores
points/rotation/date for review/adjustment).

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
