# Farm Map — Vector Extraction & Multi-Sheet Fusion Pipeline

Status: Spec (not yet built)
Last Updated: 2026-06-13 (session 21)
Context: [property-mapping.md](property-mapping.md), [source-art.md](source-art.md)

## 1. Goal

Turn the seven photographed 1995 survey plats into a single, layered, validated
vector map in a common world frame. Features are traced by hand from the sharpest
source, georeferenced via a per-sheet transform, merged across sheets using shared
features for redundancy, and validated by the operator layer by layer.

## 2. Principles (why it's built this way)

- Extract a transform, not a warped image. Tracing happens in the source image's
  native pixel space. A per-sheet pixel->world homography converts traces to WGS84.
  No rotation or resampling of the source is required for extraction; always trace
  from the highest-res original.
- The boundary self-georeferences every sheet. The exact boundary vector
  (source-data/sheet07-boundary.geojson, 409.258 ac, traverse closes 0.00 ft) is
  drawn on all sheets, giving known-world control points on each.
- Shared interior features brace the interior. Boundary-only control cannot remove
  paper fold/curl in the middle of a sheet. Features visible on multiple sheets
  (road junctions, the dam, pond corners) become tie-points that co-register sheets
  to one another -- lightweight bundle adjustment that pins the interior where the
  boundary can't reach.
- Human-in-the-loop, not auto-extraction. Automated line-following fails on these
  busy plats (boundary vs. roads vs. transmission line all heavy). The operator
  traces; the tool does the math.
- Two precision bars. Presentation backdrop = "close" + soft fade. Vector
  extraction = a few meters is plenty. Neither needs survey grade.

## 3. Common world frame

- WGS84 lat/lon, pinned to Chester County parcel 091-00-00-073-000 via the boundary
  (POB anchored to the parcel's south corner -- current demo registration).
- Plats are NAD83 / SC Grid North; grid ~ true north to <0.1deg, position good to
  ~tens of meters. Datum shift treated as negligible at this precision; revisit only
  if a layer needs it.

## 4. Data model

- Sheet transform -- per sheet: homography (pixel->world), the GCPs used, residual,
  and sheet metadata incl. date / date basis (see section 8). Stored as
  source-data/transforms/<sheet>.json.
- Raw trace -- one feature set as traced from one sheet, in world coords, tagged with
  source sheet + date. Stored as source-data/traces/<sheet>-<layer>.geojson.
- Merged layer -- the reconciled, validated layer composed from one or more raw
  traces. Stored as source-data/layers/<layer>.geojson, with provenance and a
  validated flag.

## 5. The digitizer (tool spec)

A single self-contained browser page (farm-map/digitizer/index.html, HTML canvas +
JS; served by the existing local http server). Modes:

A. Georeference mode
- Load a source sheet; zoom/pan at full res.
- Tool presents the known boundary corners as a checklist with their world coords
  (labeled: North apex, POB, East corner, plus numbered traverse vertices). Operator
  clicks each corresponding point on the image.
- Optional tie-points: operator drops a named shared point (e.g. "dam-N",
  "road-junction-3") that other sheets will also reference; world coord unknown
  initially, resolved by fusion (section 6).
- At >=4 GCPs, solve homography (DLT) live; back-project the full boundary in green
  onto the image as a visual lock-check; show median residual (px and meters).
- Save the transform.

B. Trace mode
- Pick a target layer (boundary, roads, creeks, lake, trails, stands, food plots,
  contours) and geometry type (point/line/polygon).
- Click to digitize; transform to world coords on finish; emit GeoJSON (download or
  copy) into traces/.
- Snapping to existing tie-points/vertices optional later.

Outputs: WGS84 GeoJSON per trace + the sheet transform JSON. No image warping.

## 6. Multi-sheet fusion

- Ideal: solve all sheet homographies jointly -- minimize (boundary-GCP error) +
  (disagreement between sheets at shared tie-points). Classic bundle adjustment.
- Pragmatic / phased: (1) georeference each sheet independently from its boundary
  (gets each "close"); (2) add shared tie-points and refine, prioritizing interior
  accuracy where the fold lives. Start with projective; upgrade a sheet to thin-plate
  spline only if its residual stays high.

## 7. Validation workflow (operator-driven)

- For each layer, load every contributing raw trace in the common frame.
- Toggle and overlay; inspect agreement. Disagreement flags either a bad trace or a
  weak georeference -> fix upstream.
- Reconcile: pick the authoritative trace, merge/average, or stitch (a creek clearer
  on each sheet in different stretches).
- Validate currency as well as position (section 8): a feature on an old sheet may no
  longer exist on the ground.
- Mark the merged layer validated with provenance + date. The map demo is the
  validation surface.

## 8. Feature currency (sheet dating)

Deduce each sheet's date; it hints at which traced features are still real.
- Known: the deed survey (07) and master legend (06) are 1995 (rev. Oct 1996).
- Unknown: the annotated field sheets (02-05) -- dates not yet established.
- Date-basis candidates: revision blocks / title stamps; neighbor deed-book and page
  references printed on the plat (each has a recording date); ink, color, and
  handwriting differences between the base plat and the field annotations.
- Use: an older sheet's trails, stands, or food plots may be overgrown, moved, or
  gone. Date-tag each sheet and carry it into validation so currency is judged, not
  assumed. Ground-truth (field visit / recent imagery) confirms the doubtful ones.

## 9. Layer catalog (authoritative source TBD with the legend)

| Layer | Primary sheet | Cross-check / notes |
|---|---|---|
| Boundary | 07 (done, exact) | drawn on all sheets = georef control |
| Dam | 07 | shared tie-point candidate |
| Lake / water | 06 (legend shows lake) | 03 (water in blue) |
| Creeks (Flake's, Crane's Branch) | 03 | 05, 06 |
| Roads | 01 or 06 (clean) | recurring -> tie-points |
| Trails | 02 (green), 03 (orange) | confirm: same set or existing-vs-proposed |
| Deer stands | 04 | point layer |
| Food plots / habitat | 05 | |
| Legend / symbology | 06 | reference only, not spatial |

## 10. Presentation surface

The existing demo/index.html becomes both validation surface and presentation.
Raster backdrops placed "close" via the same homographies, with a soft cross-fade
between basemap and survey art; validated vector layers styled and individually
toggleable. Downstream outputs (printable map, flyover, screensaver) per the
property-mapping goals.

## 11. Build phases

- P1 -- Digitizer MVP: load sheet, pick boundary GCPs, solve projective homography,
  back-project check, save transform.
- P2 -- Trace mode -> GeoJSON in world frame. Prove end-to-end on the lake (sheet 06).
- P3 -- Tie-points + fusion across all 7 sheets.
- P4 -- Merge + layer-by-layer validation in the demo.
- P5 -- Presentation polish (soft fade, styling, outputs).

## 12. Open decisions

- Authoritative source per layer (resolve against sheet 06 legend).
- Sheet dates / feature currency (section 8) -- establish dates for 02-05.
- Trails: is 02-green vs 03-orange the same trail set, or existing vs. proposed?
- Per-sheet transform type: projective default; TPS only where fold residual demands.
- Tie-point fusion: independent-per-sheet first, or joint bundle adjustment from the
  start?

## 13. Non-goals

Survey-grade accuracy; a full GIS; automated feature extraction. Human-traced,
a-few-meters-good-enough, purpose-built for these seven sheets.
