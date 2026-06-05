# Farm / Property Mapping Project

Last Updated: 2026-06-04
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

**Open discrepancy — county parcel is ~611 acres vs the 1995 survey's 409.258.** Not a
rounding error (verified against the bounding box). The two boundaries are *not* the same
extent. Most likely **land was added since 1995** (adjacent parcels acquired and merged
under one parcel ID); could also be that the survey covered one of several deed tracts.
Do not substitute the county boundary for the survey blindly — reconcile them: overlay
survey on parcel, locate the extra ~200 acres, and confirm the current true extent.

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
