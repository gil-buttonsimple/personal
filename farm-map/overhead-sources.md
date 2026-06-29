# Farm Map -- Overhead Photos & Layers Catalog (deep dive)

Last Updated: 2026-06-28 (session 26)
Status: Active. A deep-dive inventory of overhead imagery and GIS data layers
available for the property BEYOND the seven paper plats and the handful of
sources already wired into the demo. Scoped to this exact parcel:
**091-00-00-073-000**, K-Farm LLC, 1221 Great Falls Hwy, ~605 deeded ac SE of
Chester, S.C. (the 409.258-ac Ashview survey is one tract of it).

Companion docs: [property-mapping.md](../property-mapping.md),
[source-art.md](source-art.md) (the 7 plats), [source-map.md](source-map.md)
(per-sheet read), [presentation-stack-research.md](presentation-stack-research.md)
(render/serve stack + the already-speced DEM/NAIP/Sentinel pipeline).

Constraint update (s26): **Esri is now allowed as a source.** The earlier
"no Esri anywhere" rule is relaxed -- Esri/ArcGIS data may be CONSUMED for
acquisition. The runtime stack stays open-source (MapLibre + MBTiles/PMTiles);
Esri products are an acquisition source, baked to local tiles, not a runtime
dependency. Google Earth imagery remains BLOCKED for commercial use.

## What's already in hand (do not re-acquire)

7 paper plats; Chester County parcel KML + Beacon assessment record; OpenStreetMap
roads/creeks; AWS Terrain Tiles (terrarium DEM, measured); USGS 3DEP 1 m LiDAR
(speced); Copernicus DEM GLO-30; USGS NAIP + Sentinel-2 (speced); OpenAerialMap;
USGS NHD hydrography (24.5-ac lake fetched).

---

## A. Overhead photos (imagery)

### Time-depth (the biggest gap -- nothing historical is wired in yet)

- **Esri World Imagery Wayback** -- dozens of DATED sub-meter captures since 2014;
  a true historical slider at far higher res than NAIP. Best single new imagery
  source. https://livingatlas.arcgis.com/wayback/
- **USGS EROS Aerial Photo Single Frames + Mosaics** -- 1937-2014, B&W / color /
  color-IR, 400-1000 dpi, mostly USDA farm flights. Search on EarthExplorer under
  Aerial Imagery. https://earthexplorer.usgs.gov/
- **USC South Carolina Aerial Photography** -- digitized USDA flights + 1937-1989
  flight indexes to find frame numbers over the parcel.
  https://scmemory.org/collection/south-carolina-aerial-photography/ ,
  https://aerialphotos.library.sc.edu/ ,
  https://digital.library.sc.edu/collections/south-carolina-aerial-photograph-indexes-1937-1989/
- **HistoricAerials.com** -- multi-decade slider viewer + historic topos.
  https://www.historicaerials.com/viewer
- **Vintage Aerial -- Chester County** -- 1980s low-OBLIQUE farm flyovers; good for
  the montage / "what it looked like" reel, not for georeferencing.
  https://vintageaerial.com/photos/south-carolina/chester

### Current / near-current high-res

- **Esri World Imagery (current)** -- sub-meter basemap, immediate.
  https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9
- **NAIP multi-year archive** -- NAIP is a ~2-year SC time series (2009/11/.../23),
  not one layer; a multi-date NAIP stack = cheap leaf-on change detection.
- **SC statewide ortho imagery** -- state-flown orthos (sometimes leaf-off /
  higher-res than NAIP) via SC GIS + SCDNR Open Data.
  https://data-scdnr.opendata.arcgis.com/ , http://www.gis.sc.gov/
- **Commercial high-res (paid, optional)** -- Nearmap / Vexcel / Maxar for recent
  leaf-off sub-foot imagery if a specific need justifies the cost. Not needed yet.

## B. Elevation / LiDAR (SC-specific, better than the speced generic path)

- **SCDNR LiDAR (SC LiDAR Consortium)** -- bare-earth DEMs, **contours, intensity
  images, hydro breaklines, hydro-enforced DEMs** in 10,000-ft tiles by county +
  county-wide geodatabases on FTP. Same 1 m-class data the spec pulls from USGS
  prd-tnm, but PRE-DERIVED (contours + hydro already cut) -- feeds lake/spillway/
  creek layers directly. Intensity image is itself a grayscale overhead layer.
  https://www.dnr.sc.gov/gis/lidar.html , status app:
  https://data-scdnr.opendata.arcgis.com/datasets/scdnr-lidar-status

## C. Thematic data layers (only NHD hydrography catalogued before)

- **NRCS soils (SSURGO/gSSURGO)** -- per-polygon soil type, drainage, flood
  frequency, woodland/pasture productivity. High value for habitat + ag-use.
  https://websoilsurvey.nrcs.usda.gov/app/
- **USFWS National Wetlands Inventory (NWI)** -- wetlands polygons; fits the
  creeks / beaver dams / flood-area work. https://www.fws.gov/program/national-wetlands-inventory
- **FEMA National Flood Hazard Layer (NFHL)** -- flood zones; pairs with the
  sheet 03/01 flood area + the impoundment.
- **USGS WBD watershed boundaries (HUC-12)** -- drainage basins for Flake's /
  Crane's Branch (NHD gave the lake; WBD adds the basin).
- **MRLC NLCD land cover + percent tree canopy** -- 30 m, multi-year; modern check
  on the 1995 woods/open annotations. https://www.mrlc.gov/data
- **USDA Cropland Data Layer (CDL)** -- 30 m annual crop/cover class.
- **Microsoft / OSM building footprints** -- auto polygons for the cabin + pole
  barn; cross-check on hand-traced buildings.
- **USGS topoView historical topo quads** -- 1880s-2006, GeoTIFF/KMZ; shows lake,
  dam, old roads across editions, independent of the 1995 plats.
  https://ngmdb.usgs.gov/topoview/viewer/
- **ArcGIS Living Atlas** -- one-stop hosted layers (soils, NWI, NLCD, parcels,
  imagery) now that Esri is allowed; convenient acquisition shortcut.
  https://livingatlas.arcgis.com/

## D. Chester County GIS (beyond the parcel KML already pulled)

- **Chester County GIS HUB** -- county zoning, address points, roads, contours,
  possibly building footprints. https://chester-county-s-gis-hub-chesco.hub.arcgis.com/

---

## E. How to decide what to invest in RIGHT NOW (decision framework)

Score each candidate on four axes, 1-3:
- **Fills a tracked gap** -- maps to an open farm-map feature/layer or a known hole.
- **Effort to acquire** -- one download / known API = high; manual frame-hunt = low.
- **Uniqueness** -- shows something no source in hand does.
- **Reuse** -- feeds multiple outputs (interactive map, flyover, screensaver, soils).

### Tier 1 -- do now (high gap x low effort x unique)
1. **Esri World Imagery Wayback** -- instant, sub-meter, dated. Single biggest
   visual upgrade; gives both a current crisp basemap AND time-depth. One source,
   two wins.
2. **SCDNR LiDAR (contours + hydro-enforced DEM + intensity)** -- pre-derived,
   directly feeds the still-pending lake / spillway / creek hand-trace layers and
   beats the generic terrarium/3DEP path already in the demo.
3. **NRCS soils (SSURGO)** -- one whole-survey download; a genuinely new thematic
   layer with high relevance to a hunt/ag property; trivial to acquire.

### Tier 2 -- next (high value, a little more effort)
4. **USGS topoView historical topos** + **NWI wetlands** + **FEMA NFHL** -- each a
   clean download, each fills a tracked gap (time-depth, wetlands, flood). Batch
   them in one acquisition pass.
5. **NAIP multi-year stack** -- cheap change-detection once Tier 1 imagery is in.

### Tier 3 -- opportunistic / on-demand
6. **USGS EROS + USC historical aerials** -- highest time-depth but manual
   frame-hunting; pull only when a specific question needs pre-1994 ground truth
   (e.g., when the lake/dam was built, old road alignments).
7. **NLCD/CDL, building footprints, WBD, Chester County Hub layers** -- nice-to-have
   context; grab as a feature needs them, not speculatively.

### Skip for now
- **Commercial imagery (Nearmap/Vexcel/Maxar)** -- no current need that free sub-meter
  Wayback + NAIP can't meet.
- **Vintage Aerial obliques** -- save for the montage/screensaver pass, not the map.
- **Google Earth** -- blocked for commercial use.

**One-line recommendation:** wire **Wayback imagery** + **SCDNR LiDAR contours/hydro**
+ **SSURGO soils** this cycle; everything else is a batched second pass or on-demand.
