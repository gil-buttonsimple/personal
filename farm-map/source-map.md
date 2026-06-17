# Farm Map -- Source Map (what's on each sheet, and where each feature comes from)

Last Updated: 2026-06-17 (session 25)
Status: Authoritative. This is the founder's own read of the seven sheets, captured
sheet by sheet. It supersedes earlier inferences drawn from the legend and the HSV
palette. When deciding where to get a feature, start here.

## The governing principle

Digitize only what no other map has, and get each feature from the sheet (and by the
method) where it is cleanest. Two methods:

- **Auto colour-extraction** -- only where a feature is its own distinct colour
  (red deer-stand dots, the orange/green road+trail marker network). HSV mask ->
  geometry -> projected through the sheet's homography.
- **Hand-trace + label (digitizer)** -- for everything drawn as sharp, uniform black
  linework on the clean base (lake, rivers, road shoulders, power lines, easement,
  spillway, fences, woods/open). Colour cannot separate these; the founder traces the
  line and assigns its label/class, the machine projects it to world coordinates.

The blue "water" highlighter is NOT a source: it only overlays creek/contour lines that
exist cleaner on the base sheets. The actual lake/flood/creek data is the base linework.

## Road & trail classes (founder, s25)

"Road" and "trail" out here span a wide range. Classify, do not lump:

- **Main road** -- the road to the barn (primary).
- **Dirt road** -- the larger dirt roads.
- **2-track / ATV** -- two-track suitable for 4-wheelers (most of the on-property network).
- **Trail** -- narrow / foot.

Public roads come from OpenStreetMap. These four are the *internal* network OSM lacks.

## Per-sheet read (founder's words, s25)

| # | Sheet | What's on it | Use |
|---|---|---|---|
| 01 | base plat (clean) | Lake boundary (the real one), emergency spillway, road shoulders, power lines + electric-coop easement, rivers, fences; colour marks for WOODS/OPEN (historic). Base is clean. | hand-trace source (backup to 07) |
| 02 | green | Green lines highlight **some roads**; hand-written numbers in circles (33, 38, 24, 10 -- unknown). Base too faded to use. | auto: part of the road/trail network |
| 03 | orange + blue | **Orange = roads/trails, very clear.** Base map good (backup of 01, maybe same source or better). Flood area. Brown dots (maybe spillway). Blue highlighter NOT a water source. | auto: roads/trails (orange). base: hand-trace backup |
| 04 | red / shaded | **Red dots = deer stands.** Base UNUSABLE -- uniformly shaded, same shade means many different things (lake surface, open areas, ...). | auto: stands only |
| 05 | habitat (full colour) | Green = open spaces, brown = roads. Supports other maps; nice in the animated demo. Base same. | low priority / demo support |
| 06 | master legend (1995) | Shaded colour: blue = lake, blue attached dots = (likely) stands, green = open areas, pink = border (likely useless, worth comparing), some creeks blue. Not much new. | interim lake; compare only |
| 07 | deed survey | **Great, very clean base.** Best candidate for extracting the most lines for identification. NAD83 / SC grid -- already the georeference anchor. | **primary hand-trace base** |

## Feature -> source -> method

| Feature | Geometry | Source sheet | Method | Status |
|---|---|---|---|---|
| Property boundary | polygon | 07 (deed traverse table) | computed (exact, closes 0.00 ft) | done |
| Deer stands | points | 04 (red dots) | auto colour (HSV red) | done |
| Roads & paths (internal) | lines | **03 (orange)** -- compared, accurate; 02 green partial; 05 brown unusable | auto colour (clear_border drops the table) | draft, sheet 03 chosen |
| -> tier: main / dirt / 2-track / path | lines | classify on top of sheet 03 | **hand-trace / label** | pending |
| Buildings (barn + cabins/sheds) | points/polys | 07/01 base | **hand-trace** (few, precise) | pending |
| Lake / impoundment boundary | polygon | 07 (01/03 backup) | **hand-trace** | tool pending |
| Emergency spillway | line | 07 / 01 | **hand-trace** | tool pending |
| Flood area | polygon | 03 / 01 | **hand-trace** | tool pending |
| Rivers / creeks | lines | OSM primary; 07/01 backup | OSM + hand-trace gaps | OSM only so far |
| Road shoulders | lines | 07 / 01 | **hand-trace** | tool pending |
| Power lines + coop easement | lines | 07 / 01; Duke line on 03 | **hand-trace** | tool pending |
| Fences | lines | 07 / 01 | **hand-trace** | tool pending |
| Woods / open | polygons | 01 colour marks, 05 green, 06 green | hand-trace (historic, low pri) | deferred |
| Food plots | polygons | 06 (green, numbered 1-30) | auto colour (rough) | draft |
| Public roads | lines | OpenStreetMap | GIS pull (fetch_osm_roads.py) | done |

## What changed in s25 (and why)

- Sheet 03 "blue water" extraction was built, then dropped: it shredded a highlighter
  laid over existing lines into meaningless dots. Water comes from the base linework.
- Water layer reverted to the sheet 06 lake blob as a rough **interim**, to be replaced
  by a hand-traced lake from sheet 07.
- The fused 02+03 network was relabeled "roads & trails (unclassified)"; tiers get
  assigned by hand-tracing, not colour.
- Tried + dropped a "vectorize sheet 07, deduce every line from the other sheets' colours"
  pass -- too noisy (water over-claimed, thousands of text/fragment pieces). Boundary is
  already known, so it was never needed. Direction: feature by feature from the best source.
- Roads & paths compared head-to-head (roads_compare.py): sheet 03 orange wins (clean,
  complete, lands on the imagery); 02 partial; 05 unusable. Roads = sheet 03.
- Lesson banked: walk the founder through what each sheet shows BEFORE building any
  extraction, and go feature by feature from the best source -- don't auto-deduce all at
  once. The source read drives the method; assumptions cost rebuilds.
