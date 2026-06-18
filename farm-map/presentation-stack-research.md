# Farm Map — Presentation Stack Research (open-source, no Esri)

Status: Reference. Captured for the EXPANSION phase (full interactive documentary
kiosk). The near-term build is a simplified TV screensaver; this is the long-term
target stack. Open-source all the way; Esri / ArcGIS excluded everywhere.
Last Updated: 2026-06-17

Context: [property-mapping.md](../property-mapping.md),
[vector-pipeline-spec.md](vector-pipeline-spec.md). Near-term demos:
presentation.html (plate), screensaver-pan.html (vertical Ken-Burns),
screensaver-3d.html (3D topo flythrough).

---

## Key decisions (top-line)

1. **Render engine: MapLibre GL JS (BSD-3-Clause), currently 5.x.** Lowest-risk for a
   24/7 kiosk on modest hardware: permissive license, light WebGL footprint, built-in
   3D terrain (`setTerrain`), sky, and a real cinematic camera (free-camera API plus
   `flyTo`/`easeTo`). Use **CesiumJS (Apache 2.0)** only if a true curved-Earth globe
   or photoreal 3D Tiles is needed, accepting its documented long-run WebGL
   context-loss and RAM-growth risks.
2. **Aspect-ratio approach: forward-pitched oblique camera (north up, no heading
   change) + slow vertical Ken-Burns drift, with designed side mattes / split panel.**
   The cinematic/documentary norm (National Geographic / Heinrich Berann panorama
   tradition). Foreshortening makes a tall north-south footprint fill 16:9 without
   rotating the map. Add a short point-of-interest tour to defeat repetition/burn-in.
3. **Data, all open, no Esri:** terrain from **AWS Terrain Tiles (terrarium)** for a
   fast build or **USGS 3DEP 1 m LiDAR** from the non-Esri `prd-tnm` S3 bucket for top
   quality; aerial from **USGS NAIP** (public domain, ~0.6 m) with **Sentinel-2** as a
   free-anywhere fallback. Avoid the Esri-hosted `*.arcgis.com` elevation services.
4. **Offline tiles:** bake with **rio-rgbify** (terrain-RGB) and **gdal2tiles**
   (imagery) into **MBTiles**, optionally **PMTiles** served as a static file straight
   to MapLibre, or via **Martin** / **TileServer GL**. No internet, no Esri at runtime.
5. **Kiosk loop:** vanilla-JS `idle-timeout` (MIT) toggling an attract auto-tour and
   the interactive app; ~60 s idle timeout with a visible "Still there?" countdown.
   `chromium --kiosk` on Linux Mint, screen-blanking disabled, supervised by a systemd
   user service plus a nightly restart.
6. **Storytelling:** start from **opengeos/maplibre-gl-storymaps (MIT)** or
   **digidem/maplibre-storymap (BSD-3)** — open ports of the BSD-3 `mapbox/storytelling`
   template — using **Scrollama.js (MIT)**. Model POIs as a GeoJSON Point
   FeatureCollection with rich nested `properties` (schema below).

Every required component is MIT / BSD / Apache 2.0. No Esri product anywhere.

---

## 1. Aspect-ratio: tall footprint on a 16:9 screen, north up

Techniques practitioners use, with screensaver trade-offs:

- **Oblique / tilted 3D camera** — pitch forward (not nadir) so foreshortening makes a
  tall area recede to the horizon and fill the width; pitch changes without heading, so
  north stays up. Cinematic; a fixed tilt feels static unless paired with slow motion;
  true orbit breaks north-up.
- **Vertical Ken-Burns pan** — keep the map flat/north-up, frame tight, slowly pan along
  the long N-S axis with gentle zoom. Trivial, perfect north-up, no 3D pipeline; viewer
  never sees the whole shape at once; a single linear loop gets repetitive.
- **Designed side mattes / pillarbox panels** — design the leftover columns (title,
  legend, photos, north arrow) instead of black bars. Zero distortion, whole shape
  visible; more static unless panels animate.
- **Point-of-interest tour** — camera visits framed hotspots ("start wide, then go
  deep"). Naturally long-running and varied (good vs burn-in); needs authored content.
- **Split layout** — map in one vertical half, content/legend in the other. Tall map
  fits with no distortion; reads as "interface" more than "cinema."
- **Plain pillarbox** — center + black bars. Correctness baseline; looks like an error.

**Most used for cinematic/documentary work: oblique tilted 3D camera + slow Ken-Burns
drift.** Solves the geometry for free and adds the canonical documentary motion device.
Recommendation here: forward-pitched oblique camera, heading locked north, very slow
vertical drift, side columns designed as mattes or split panel; avoid orbit and a single
repeating linear pan; insert a short POI tour between framed stops.

Refs: NatGeo best new maps, PSU GEOG 486 oblique views, Felt "mapmaking at National
Geographic", Ken Burns effect (Wikipedia/MasterClass), mapanimation.io camera guide.

## 2. Google-Earth-like rendering, open source

- **MapLibre GL JS (BSD-3, 5.x) — recommended core.** `map.setTerrain({source,
  exaggeration})` on a `raster-dem` source (terrarium/terrain-RGB), drape aerial as a
  `raster` layer; `setSky(...)`; globe projection. Cinematic flights via `flyTo`/`easeTo`
  chained, or the **free-camera API** (`getFreeCameraOptions`/`setFreeCameraOptions`,
  `MercatorCoordinate.fromLngLat`, `lookAtPoint`) frame-by-frame. Strong for 24/7; add a
  `webglcontextlost` reload watchdog. Good on modest hardware (cap pixel ratio, DEM zoom,
  exaggeration).
- **CesiumJS (Apache 2.0) — most capable, riskiest unattended.** Full WGS84 globe,
  quantized-mesh terrain, 3D Tiles, CZML time-dynamic scenes; `Camera.flyTo`,
  `CameraFlightPath`. 24/7 risk: documented WebGL context loss in long sessions and RAM
  growth as 3D Tiles data is retained. Use only if you need globe-scale or 3D Tiles.
- **deck.gl (MIT)** — `TerrainLayer` from an RGB heightmap, first-class MapLibre
  integration (`@deck.gl/mapbox`). Add only for large animated data overlays.
- **Three.js (MIT) / Potree (BSD)** — max control terrain mesh + draped texture (high
  effort) / browser point-cloud viewer (only if LiDAR point clouds are the medium).
- **Google Earth Studio — render-to-video only, BLOCKED for commercial use.** No live
  embed; "we currently do not offer a license to use Google Earth imagery for commercial
  applications"; output watermarked. Do not use here.

## 3. Data sources, open and offline-capable (no Esri)

**Terrain/DEM**
- **AWS Terrain Tiles (terrarium)** — fast path, live; bucket `elevation-tiles-prod`,
  `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png`; decode
  `elev = (R*256 + G + B/256) - 32768`. MapLibre reads with `encoding:'terrarium'`.
  Carry the tilezen attribution file. Successor to dead `tile.mapzen.com`.
- **USGS 3DEP / The National Map** — best raw DEM. AVOID Esri-hosted services
  (`*.arcgis.com`, `elevation.nationalmap.gov/arcgis/...`). USE plain GeoTIFF/COG on
  `prd-tnm.s3.amazonaws.com` (1 m under `StagedProducts/Elevation/1m/Projects/`),
  `rockyweb.usgs.gov` mirror, discovery via the TNM Access API. SC has modern 1 m LiDAR.
  Public domain.
- **OpenTopography API** — one-call clipped GeoTIFF (SRTM/ALOS/Copernicus, 3DEP 1"/13").
- **Copernicus DEM GLO-30** — 30 m global DSM COGs (`copernicus-dem-30m`), attribution.

**Aerial / satellite**
- **USGS NAIP** — best aerial for SC, public domain, ~0.6-1 m; AWS `naip-visualization`
  (3-band RGB COG, best for tiling). Bucket is Requester Pays (free within us-east-1).
  Discover via Earth Search STAC (`naip`).
- **Sentinel-2 L2A** — 10 m, Copernicus open, free anywhere; COGs via Earth Search.
- **OpenAerialMap** — community CC-BY, patchy coverage for SC.

**Bake offline:** rio-rgbify (DEM->terrain-RGB MBTiles), gdal2tiles (imagery XYZ),
MBTiles single-file store, PMTiles (static, HTTP-range, no backend), Martin/TileServer GL.
Pipeline: DEM -> gdalwarp 3857 -> rio rgbify -> MBTiles -> (pmtiles convert) -> MapLibre.

## 4. Kiosk / attract-loop

- Auto-play when idle -> switch to interactive on touch -> idle-timeout back to attract.
- Durations (vendor rules of thumb): attract loop 30-60 s; idle timeout ~30-90 s
  (60-120 s where reading is needed). Visible countdown with cancel; idle-reset timer.
- Open-source idle libs: `idle-timeout` (jacobmllr95, MIT, has a `loop` setter), or plain
  `setTimeout` reset on `pointerdown`/`touchstart`/`keydown`.
- Linux Mint 24/7: `chromium --kiosk <url> --noerrdialogs --disable-session-crashed-bubble
  --disable-infobars --no-first-run`; `xset s off -dpms`; `unclutter -idle 1 -root`;
  systemd user service `Restart=always` + a `while true` relaunch loop. Real risk is
  memory growth -> scheduled nightly restart + hardware watchdog. Firefox alt:
  `firefox --kiosk`.

## 5. Documentary / storytelling layer

- Scrollytelling: `mapbox/storytelling` (BSD-3) pattern; MapLibre ports
  `opengeos/maplibre-gl-storymaps` (MIT, no key, 3D terrain, inset minimap,
  chapter enter/exit reveals) or `digidem/maplibre-storymap` (BSD-3, offline-first).
- Scroll engine: Scrollama.js (MIT). For an auto-advancing attract tour, chain `flyTo`
  on a per-chapter timer instead of scroll.
- POI rendering: HTML markers/popups are stylable but DOM-heavy; symbol/circle layers
  render on WebGL and scale to thousands with clustering. Hybrid: all POIs as a symbol
  layer, render a rich popup from the clicked feature's `properties`; reserve standalone
  Markers for the active POI.

### Recommended POI GeoJSON schema

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "poi-old-mill",
      "geometry": { "type": "Point", "coordinates": [-81.0351, 34.9213] },
      "properties": {
        "id": "poi-old-mill",
        "title": "The Old Grist Mill",
        "category": "structure",
        "subtitle": "Built 1887",
        "description_md": "The **grist mill** powered the valley's first economy...",
        "year": 1887,
        "photos": [
          { "url": "photos/mill-1900.jpg", "caption": "circa 1900", "credit": "County Historical Society", "width": 1600, "height": 1067 }
        ],
        "audio": { "url": "audio/mill.mp3", "duration_sec": 142, "title": "How the mill worked", "transcript": "When the spring melt came down..." },
        "track_ref": "track-river-trail",
        "nearby": ["poi-covered-bridge", "poi-millpond"],
        "links": [ { "label": "National Register listing", "url": "https://example.gov/nr/87001234" } ]
      }
    }
  ]
}
```

`category`+`title` stay top-level scalars (style/filter); `description_md` is Markdown;
`photos` carry width/height; `track_ref` points to a separate LineString collection;
`nearby` is POI ids resolved at runtime. RFC 7946 allows nested properties (MapLibre
preserves them; some older importers flatten).

## 6. Recommended stack + references

| Layer | Choice | License |
|---|---|---|
| 3D render engine | MapLibre GL JS 5.x | BSD-3 |
| Cinematic camera | MapLibre free-camera API + flyTo/easeTo | built in |
| Aspect handling | Oblique pitch (north up) + Ken-Burns + side mattes | n/a |
| Terrain data | AWS terrarium or USGS 3DEP 1 m (prd-tnm S3) | public domain / attribution |
| Aerial imagery | USGS NAIP (~0.6 m) + Sentinel-2 fallback | public domain / Copernicus |
| Tile baking | rio-rgbify + gdal2tiles -> MBTiles -> PMTiles | BSD/MIT |
| Tile serving | PMTiles static, or Martin / TileServer GL | BSD / MIT-Apache |
| Story layer | opengeos/maplibre-gl-storymaps + Scrollama.js | MIT |
| POI data | GeoJSON Point FeatureCollection (schema above) | n/a |
| Attract loop | idle-timeout (vanilla JS) | MIT |
| Kiosk runtime | chromium --kiosk on Linux Mint + systemd + nightly restart | n/a |

**Risks:** Chromium memory growth (nightly restart + watchdog); WebGL context loss
(reload listener even on MapLibre); DEM/imagery acquisition effort (NAIP requester-pays,
confirm 1 m LiDAR over the exact parcel); burn-in (slow motion + POI tour); a true
photoreal twin would mean drone photogrammetry (WebODM) and possibly Cesium 3D Tiles.

**Reference projects:** opengeos/maplibre-gl-storymaps (MIT, closest precedent);
mapbox/storytelling (BSD-3, the pattern's lineage); digidem/maplibre-storymap (BSD-3,
offline); MapLibre camera examples (BSD-3); WebODM / OpenDroneMap (open path to a 3D
digital twin of the actual property). Look-and-feel references (proprietary, concept
only): FATMAP, OuterSpatial, NPS 3D tours.

## Uncertainties / to verify
- MapLibre free-camera exact method names in 5.x — verify against the live Map API docs.
- NAIP requester-pays + egress cost; confirm current SC NAIP year/resolution; process
  in us-east-1 to avoid egress.
- 3DEP 1 m LiDAR coverage over the exact parcel (TNM Downloader).
- AWS Terrain Tiles long-term maintenance (community-run; mitigate by self-hosting baked
  tiles).
- Idle-timeout durations are vendor rules of thumb, not peer-reviewed.
- Confirm licenses for react-idle-timer and StoryMapJS before commercial reliance.
- No single documented standard ties "tall portrait, north-up, 16:9 TV screensaver"
  together; section 1 is informed synthesis.
- Google Earth Studio commercial prohibition confirmed; do not use here.
