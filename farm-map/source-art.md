# Farm Map -- Source Art Catalog

Last Updated: 2026-07-07
Status: Archival (ingested source material)

Photographs of the physical paper survey plats for the Kasparek family farm
("K-Farm" = KaFam; cf. `finance-2025-kafam-k1-gil.pdf`). All eight sheets depict
the **same ~409-acre property** near Chester, S.C., in different working/annotated
copies. Sheets 01-07 shot 2026-01-26; sheet 08 shot 2026-07-06. Taken on a phone;
the sheets were weighted flat with wood-slice coasters, so several photos are
rotated or partial (sheet 08 is rotated 180 degrees, title block reads
upside-down).

These are the authoritative source for the project's Mapping Foundation: sheet 07
is the georeference anchor, sheet 06 is the legend rosetta stone, and sheets 02-05
carry the field annotations (trails, stands, food plots, water) to be digitized.

## Property facts (from the plats)

- Owner / legal name: **Gene A. Kasparek** (deed survey, sheet 07).
- Working name: **K-Farm Hunt Club**.
- Area: **409.258 acres** (sheet 07; annotated copies round to 409.298).
- Location: southeast of Chester, S.C.
- Surveyor: **Ashview / Ashmark Land Surveyors** (name appears both ways across sheets).
- Survey date: **August 29, 1995**, revised **October 1996** (sheet 06).
- Scale: **1" = 400'**.
- Datum / projection: **S.C. Grid North, NAD 1983** (sheet 07). Other sheets show
  Magnetic North only.

## Archival location

`farm-map/source-art/` -- renamed to descriptive slugs. Originals also retained,
untouched, at `~/Documents/farm-map/Farm maps/` (+ the redundant
`Farm maps-3-001.zip`, a byte-identical Drive export). Repo copies are
checksum-verified identical to the originals.

## Sheets

| Archival name | Original file | Contents |
|---|---|---|
| `01-base-plat-clean.jpg` | PXL_20260126_175254160 | **Base plat, clean.** Parcel boundary, adjoining-owner deed-book references, topo contours. "Note: this map for general orientation purposes only." Best clean base for tracing the boundary. |
| `02-trails-green.jpg` | PXL_20260126_175403833 | **Green-marker trails copy.** Hand-drawn trail/loop network in green. Carries a course/bearing/distance table and the surveyor legend (dirt road, tree line, water, flood easement, paved road, railroad). Vicinity map names Chester, S.C. |
| `03-trails-orange-water-blue.jpg` | PXL_20260126_175433425 | **Orange/blue working copy.** Orange trail network, blue water features, heavy black property outline. Landscape orientation. |
| `04-deer-stands.jpg` | PXL_20260126_175447234 | **Deer-stand copy.** Red dots mark permanent stand locations across the property; pencil field notes. Aged/stained sheet. |
| `05-habitat-full-color.jpg` | PXL_20260126_175515246 | **Full-color habitat copy (richest layer).** Green woods/forest stands, brown trail+road network, blue named creeks (Flake's Branch, Crane's Branch). Most data-dense sheet. |
| `06-master-legend-1995.jpg` | PXL_20260126_175525696 | **Master legend / management copy** (Ashmark, Aug 29 1995, rev. Oct 1996). The rosetta stone for the color annotations: Main roads = orange, Permanent stands = blue dots, Water = blue, Food plots = green, Property boundary = pink. Numbering: woods stands #40-50, food plots #1-30. **Shows the lake/pond** that the project notes flag as missing from topo maps. |
| `07-deed-survey-kasparek.jpg` | PXL_20260126_175547606 | **Deed survey: "Plat of Survey for Gene A. Kasparek," 409.258 acres.** S.C. Grid North, NAD 1983 -- the georeference anchor. Topo contours, WOODS / ROAD / DAM labels, creeks. Authoritative legal base for scaling and aligning all other sheets. |
| `08-compartments-green.jpg` | PXL_20260706_152709896 | **Green-boundary management-compartment copy** (Ashmark, "Part C," 409.258 acres, rev. Oct 18 1996). Green-highlighter property boundary, blue highlighter lake fill, and green-filled hunt-club compartments lettered by zone (C1-C20, R1, E1-E3, G1, P1-P6). Carries the full course/bearing/distance table, the surveyor legend, Duke Power Co. transmission line, and the Chester S.C. vicinity map. Magnetic North. Rotated 180 degrees as shot. New copy vs. the 01-26 batch -- distinct compartment-lettering scheme not on the other sheets. |

## Annotation key (consolidated from sheet 06; founder-confirmed against the printed legend)

- Main roads -- yellow / orange
- Trails -- hand-drawn, varies: green on sheet 02, brown/orange on sheets 03 & 05
- Permanent deer stands -- **blue DOTS** (solid, round, saturated) on sheet 06; **red markers**
  on the dedicated stand copy (sheet 04, the cleanest source)
- Water / creeks / lake -- **blue HIGHLIGHTER** (translucent wash, broad strokes)
- Food plots -- green; numbered 1-30
- Woods stands -- numbered 40-50
- Property boundary -- pink (sheet 06) / heavy black (sheets 01, 03)

**Extraction trap (the key distinction):** stands and water are BOTH blue on sheet 06. They
are told apart by *mark type*, not hue -- permanent stands are small solid round dots; water
is a washy translucent highlighter. A plain blue mask conflates them: it catches stand dots
as fake small "water" and the highlighter edges as noise. Detect water by the highlighter
(broad, lower-saturation fill) and stands by the dots (small, round, saturated) -- or take
stands from sheet 04 (red, no blue collision) and water/lake as the large highlighter fill.

## Digitization notes

- Start georeferencing from **sheet 07** (stated datum NAD 1983, S.C. State Plane
  grid north). The magnetic-north-only sheets must be rotated to grid north before
  overlay -- magnetic declination for Chester, S.C. in 1995 is the offset to apply.
- The boundary on sheet 01/07 should be vectorized first, then reconciled against
  any existing GeoJSON property boundary (see `property-mapping.md`).
- The **lake** is present on sheet 06 and the dam on sheet 07 -- digitize from these
  to fill the gap in modern topo data.
- Trails, stands, and food plots are the field-annotation layers; sheets 04, 05, 06
  are the primary sources for those.
