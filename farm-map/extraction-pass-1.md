# Farm Map -- Feature Extraction, Pass 1

Last Updated: 2026-06-17 (session 23)
Status: Draft layers for validation

First comprehensive vectorization of the survey's annotation layers into projected
GeoJSON. Tooling: numpy, scipy, scikit-image, shapely, Pillow (installed 2026-06-17).
Scripts in `farm-map/extract/`; outputs in `farm-map/source-data/`. Live in
`farm-map/demo/index.html` as toggleable layers.

## Guiding principle

Digitize only what no other map has. Roads, the parcel, and the legal boundary are
already authoritative elsewhere, so we take those from real sources (OpenStreetMap
roads; county GIS parcel; the exact 43-course traverse for the boundary). The
survey's unique value is its **field annotations** -- trails, deer stands, food
plots, water -- which exist on no other map. Those are what we extract.

## Method

Each sheet has a saved homography (pixel -> world) from the digitizer. Any feature
isolated in pixel space therefore projects onto the map. Colour isolation is done in
**HSV** (hue is stable under the uneven phone-photo exposure; RGB thresholds drift
sheet to sheet). Region of interest is the known survey polygon inverse-projected
into each sheet's pixels and rasterized -- this auto-excludes the legend box and
marginalia (they fall outside the boundary). Geometry comes out as real GeoJSON:

- **Points** (stands): round blob centroids.
- **Polygons** (water, food plots): blob outer contours, simplified.
- **Lines** (trails): skeleton -> 8-connected segments -> shapely linemerge -> simplify.

Result figure: `extraction-pass-1-layers.png` (all layers over OSM roads + boundary).

## What was extracted (all from sheet 06, the cleanest multi-colour photo)

| Layer | Source colour | Geometry | Count | Confidence |
|---|---|---|---|---|
| Deer stands | blue dots | points | 42 candidates | medium -- validate; over-inclusive by design |
| Water / creek / lake | blue (large blobs) | polygons | 20 | good -- coherent N-S drainage + pond |
| Food plots / woods | green | polygons | 35 | good -- matches the ~30 numbered plots |
| Trails | green (sheet 02) | lines | fragmentary | low -- faint pencil; rough, off by default |
| Roads | n/a (OpenStreetMap) | lines | 180 ways | authoritative (not extracted) |

Homography self-check on sheet 06: 0.005 m at the control points.

## Validation

- **Georeference** is confirmed independently: the registered south apex (POB) lands
  5 m from Hinton Rd and 9 m from Great Falls Hwy (OSM), and the SW boundary runs
  along Great Falls Hwy -- exactly the road junction Gil identified at the south point.
- **Extracted features** sit inside the boundary and form a sensible whole: a central
  creek with a pond, plots through the interior, stands along water and field edges.

## Caveats

- Positions carry tens-of-metres wobble away from the four control apexes (a 4-point
  projective fit cannot absorb the photo's keystone/paper-fold). Good enough to
  validate and correct, not survey-grade.
- Stands are automated candidates: the count (42) is deliberately inclusive. Real
  stands are confirmed/deleted by Gil + the hunt club in the digitizer.
- Trails are too faint on every photographed sheet to extract cleanly. Better source
  (rescan or higher-res photo of sheet 02/05) needed before trails are worth vectoring.

## Correction (session 24): re-extracted after fixing sheet 06's georeference

The first pass above inherited a bad homography: sheet 06's East-apex click was ~700 px
off the true corner, so every layer extracted from sheet 06 (water, food plots, stands)
was misplaced at the source. Found by drawing the known boundary onto each rectified sheet
in a shared frame (sheet 07 aligned, sheet 06 did not). Fixed by re-clicking the East apex
in the digitizer (frame coverage 85% -> 97%) and re-running this script. Current counts:
water 19, food plots 34, stands 42. See property-mapping.md "Registration accuracy."
Validation note: some stand candidates fall in the lake -- the blue-dot detector is
catching blue marks/labels inside the water blob. Tighten stand extraction (exclude the
water mask) or cull in the digitizer.

## Open / next

- Validate stands, plots, water in the browser (machine-first / human-validates).
  Demo reworked for this (session 24): default = basemap + parcel only; per-layer
  opacity sliders (onion-skin); polygons no-fill by default; basemap switcher; stands
  off by default; all 7 survey sheets rectified into one frame as onion-skin overlays
  (warp_sheets.py).
- DONE (session 24): regenerated `source-data/sheet07-boundary.geojson` + `.kml` into
  the POB-pinned frame, retiring the ~200 m-off centroid anchor.
- DONE (session 24): sheet dating -- 02-06 are one 1995 survey (Aug 29 1995, 06 rev.
  Oct 18 1996) themed five ways, not independent dates; currency must come from modern
  imagery, not sheet dates. See property-mapping.md.
- Improve interior registration (the real accuracy limit): validate-and-nudge in the
  digitizer, add interior control points, or thin-plate-spline warp. See
  property-mapping.md "Registration accuracy."
- Number the food plots (1-30) and woods stands (40-50) per the legend -- do this DURING
  digitizer validation, not as a blind auto-pass (extractor gave 35 polys vs 30 legend
  numbers; assignment needs the human eye on sheet 06).
