# Farm / Property Mapping Project

Last Updated: 2026-06-12
Status: Active (personal side project)

Captured from mobile/ChatGPT notes 2026-06-03. The goal is a clean, layered,
interactive map of the property plus a voice-first field workflow that builds a
searchable property knowledge base over time.

The property is the **Kasparek family farm** ("K-Farm"), ~409.258 acres SE of
Chester, S.C. Surveyed by Ashview/Ashmark Land Surveyors, Aug 1995 (rev. Oct 1996).

---

## Source Art (ingested 2026-06-04)

Seven photographed survey plats now archived in `farm-map/source-art/` and
cataloged in [source-art.md](farm-map/source-art.md). Originals retained untouched
in `~/Documents/farm-map/`. Key sheets:

- **Sheet 07** (deed survey, Gene A. Kasparek): the georeference anchor --
  S.C. Grid North, NAD 1983. Start alignment here.
- **Sheet 06** (master legend, 1995): annotation rosetta stone (roads, stands,
  food plots, water, boundary) and **shows the lake** that modern topo maps miss.
- **Sheets 02-05**: field annotations -- trails, deer stands, food plots, named
  creeks (Flake's Branch, Crane's Branch) -- the layers to digitize.

## County GIS Data (ingested 2026-06-04)

Chester County's digitized parcel boundary for the farm, pulled as KML and filed
at `farm-map/source-data/chester-county-parcel-073.kml` (parcel **091-00-00-073-000**,
WGS84 lat/lon, ~100 vertices, full precision). A lossy 6-decimal KMZ copy of the same
polygon was discarded.

This is the **georeference control layer**: a real-world-coordinate boundary to align
sheet 07 against, rather than tracing the boundary by hand.

## Parcel Record (Beacon / Schneider, retrieved 2026-06-12)

Authoritative county assessment record for parcel **091-00-00-073-000**, pulled from
Chester County SC's Beacon system (beacon.schneidercorp.com/?site=ChesterCountySC):

- **Owner:** K-Farm LLC, c/o **Gene A. Kasparek**, 2973 India Hook Road, Rock Hill SC 29732
  (family land; same India Hook address tied to Gil's mail forwarding).
- **Location address:** 1221 Great Falls Hwy.
- **Deeded / assessed acreage:** **604.69 acres** (the county's official figure — distinct
  from the ~611 ac our GIS polygon computes).
- **Class:** LA (Land Agricultural) / MV (Market Value) / RN (Residential Non-Owner Occ).
  Tax District 01.
- **Sale history (single record):** **11/18/1994 — W.B. Ward Jr → K-Farm LLC, $503,000.**
  Deed **Book 668-98**. Plat **Cabinet C, Slide 37 & 5** (likely two plats = two tracts).
  True Sale: Yes. No transfer since 1994 — K-Farm has held it continuously.
- **Improvements:** 2008 metal cabin, 1 bed / 1 full bath, 1,152 sqft, one story, porch
  (bldg value $112,200); metal pole barn (1,152 units, $3,525); garages/patios/storage
  ($46,000).
- **2026 valuation:** market land $1,901,550 + improvements $161,700 = **$2,063,250 total
  market**. Total taxable $227,550; total assessed $7,630 (agricultural-use valuation).
- **Plats to pull:** Cabinet C, Slide 37 and Slide 5. **Deed to pull:** Book 668, Page 98
  (sclandrecords.com or Clerk of Court).

## Acreage reconciliation (RESOLVED 2026-06-12)

Three acreage figures, two gaps, two stories:

| Figure | Acres | Source |
|---|---|---|
| County deeded / assessed | **604.69** | Beacon parcel record |
| GIS polygon area | ~611 | county KML (session 13) |
| 1995 Ashview survey (sheet 07) | 409.258 | our boundary spine |

- **604.69 − 409.258 = ~195.4 ac (the big gap).** This is the other tract(s) conveyed in
  the **same 1994 deed**, not a later addition. The Beacon sales tab shows only the one
  1994 acquisition, so the earlier "land added since 1995" hypothesis is ruled out: the
  farm is a single 1994 purchase of ~605 deeded acres, and the 409.258-ac Ashview survey
  (sheet 07) is one tract of a multi-tract deed. The two plat slides (37 & 5) corroborate
  two tracts. Price check: $503k ÷ 604.69 ≈ $832/ac (plausible 1994 rural SC) vs ÷ 409 ≈
  $1,230/ac — also leans toward the larger figure being what changed hands.
- **~611 (GIS) − 604.69 (deeded) ≈ 6 ac (the small gap).** Candidate for the "small piece
  sold off" (parcel now officially smaller than the raw polygon), or GIS-vs-deed
  measurement slop. The deed/plats will resolve which. A subdivided-out piece would NOT
  appear on this parcel's sales tab — it would be a separate child parcel with a deed
  *from* K-Farm; to find it, search Beacon for K-Farm LLC as seller, or check parcels
  adjacent to 073 for a recent carve-out.

Do not substitute the county boundary for the survey blindly. Next: pull deed 668-98 +
plats Cab C Slide 37 & 5 to break out the ~195-ac tract and confirm the ~6-ac sliver.

## Registration update (2026-06-13, session 21)

Survey<->parcel registration corrected. The demo now registers the 1995 survey (green)
to the county parcel by pinning the survey's southernmost apex (Point of Beginning) to
the parcel's south corner -- a single rigid translation, no scaling (replaces the s20
+193 m E / +110 m S least-squares fit). Result: the survey's E/S/W edges sit on the
parcel boundary; the divergences are real -- the NW lobe (~195 ac, the deed's second
tract) and a small south sliver (~6 ac, the GIS-vs-deed candidate). The survey SHAPE
comes from the plat's 43-course bearing/distance table (closes 0.00 ft), not from
tracing the photo, so its accuracy is independent of image quality. Registration is
now driven by one SHIFT constant in farm-map/demo/index.html.

Open, free reconciliation path (no Avenu pass): pull the parcels adjacent to 073 from
Chester County GIS (neighbors labeled on sheet 07: 032, 033 Hinton, 042 Odell Kennedy,
043, 070 Shannon). Where the survey and parcel diverge should coincide with real
parcel lines -- decomposes the ~195 ac and ~6 ac AND independently validates the POB
registration.

## Raster georeference (attempted, deferred)

Tried to warp sheet 07 to remove its keystone perspective + diagonal paper fold (both
confirmed in the original photo). Automated fitting failed: the plat has multiple heavy
lines (boundary, roads, "TRANS LINE 100' R/W") and the fit locks onto interior ink.
Verdict: warping is unnecessary for vector extraction (we need a pixel->world transform,
not a warped image), and a clean backdrop is an interactive job (QGIS Georeferencer / a
purpose-built digitizer), not headless auto-fit.

## Vector extraction pipeline -> [vector-pipeline-spec.md](farm-map/vector-pipeline-spec.md)

Speced (not built): trace features from the highest-res source in native pixels, convert
via a per-sheet pixel->world homography (control = the boundary drawn on every sheet),
fuse across sheets using shared features as tie-points (which brace the interior where
boundary-only control can't fix the fold), then validate layer by layer. Includes a
sheet-dating / feature-currency pass -- an older sheet's trails or stands may no longer
exist, so each sheet's date hints at which traced features are still real.

## Mapping Foundation

- Align and scale property maps / photos. → Anchor on sheet 07 (NAD 1983, S.C.
  State Plane); rotate magnetic-north sheets to grid north before overlay.
- Extract vector data from source maps. → Boundary first (sheets 01/07), then
  trails / stands / food plots / water from the annotated copies.
- Merge with existing GeoJSON property boundaries.
- Produce a clean, layered property map.
- Digitize the **lake** (sheet 06) and **dam** (sheet 07) to fill the topo gap.

## Data Layers

- Current elevation data.
- Historical weather information.
- Historical ownership records.
- Neighboring parcel ownership history.
- Lake representation (currently missing from topo maps).

## Outputs

- Interactive map.
- Printable maps.
- Video flyovers / montage.
- TV screensaver content.

## Field Data Collection

Voice-first annotation workflow: combine voice notes with photos in the field,
GPS-tagged. Reduces friction versus written documentation; builds a searchable
property knowledge base over time.

GPS-tag:
- Beaver dams
- Trails
- Points of interest
- Wildlife observations
- Infrastructure

## Recreation Layer

- Design new walking trails.
- Design new biking trails.
- Explore historical trail reconstruction.
- Build geocaching-style experiences.
- Consider a future property exploration app.

## Ecology Catalog

Inventory of:
- Native plants
- Invasive plants
- Wildlife
- Species to preserve
- Species to remove / control

Observations:
- Possible otter sighting -- verify later.

---

## Logistics

### Amazon delivery instructions

Current: no mailbox or obvious marker present. Leave packages behind the
right-side brick wall at the gate.

Future: reevaluate the drop location if staying on the property beyond the next
couple of months.
