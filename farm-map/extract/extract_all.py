#!/usr/bin/env python3
"""Comprehensive feature extraction pass. Vectorize the survey's unique layers
(the things no GIS has) into projected GeoJSON, and render a debug overlay per
feature on the source image so quality is visible before the map ever loads it.

Sources (chosen by the HSV palette analysis):
  sheet 06  boundary (pink) | water (blue, large) | stands (blue dots) | food plots (green)
  sheet 02  trails (green hand-drawn)   [best-effort]
Roads are NOT extracted here -- they come from GIS (fetch_osm_roads.py).

Run:  python3 farm-map/extract/extract_all.py
"""
import os, json
import numpy as np
from PIL import Image
from scipy import ndimage
import featurelib as F

def overlay(a, masks_colors, path, scale=(820, 1090)):
    base = (a.astype(float) * 0.28).astype(np.uint8); out = base.copy()
    for m, col in masks_colors:
        out[m] = col
    Image.fromarray(out).resize(scale).save(os.path.join(F.REPO, "farm-map", "demo", path))

def main():
    report = {}

    # ===================== SHEET 06 =====================
    a6, H6 = F.load_sheet("06-master-legend-1995")
    tx6 = json.load(open(os.path.join(F.TX, "06-master-legend-1995.json")))
    print("sheet06 homography self-check: %.3f m" % F.selfcheck(H6, tx6["gcps"]))
    proj6 = F.projector(H6)
    roi, pink = F.boundary_roi(a6, H6)
    print("ROI pixels: %d (%.1f%% of sheet)" % (roi.sum(), 100 * roi.mean()))

    from skimage.morphology import binary_closing, disk
    blue  = F.colour_mask(a6, 175, 260, s_min=0.28) & roi
    green = F.colour_mask(a6, 70, 170, s_min=0.30) & roi

    # classify blue blobs: large -> water polygons, small round -> stand points
    lbl, n = ndimage.label(blue)
    sizes = ndimage.sum(blue, lbl, range(1, n + 1))
    water_mask = np.isin(lbl, 1 + np.where(sizes >= 800)[0])
    water_mask = binary_closing(water_mask, disk(6))      # reconnect the creek band
    stand_mask = np.isin(lbl, 1 + np.where((sizes >= 40) & (sizes < 400))[0])

    water  = F.polygons_from_blobs(water_mask, proj6, area_min=1000, simplify_m=4.0)
    plots  = F.polygons_from_blobs(green, proj6, area_min=250, simplify_m=4.0, max_polys=60)
    # NOTE: deer stands now come from sheet 04 (dedicated stands sheet, red flag markers) --
    # see the SHEET 04 section below. Sheet 06's blue dots collided with the blue lake.
    # Blue on sheet 06 is overloaded: the lake AND the permanent-stand DOTS are both blue
    # (legend). The small ~0.16 ac "blobs" the water pass picked up are stand dots, not water
    # (confirmed by inspecting sheet 06 at each: every one is a blue dot). Keep only genuine
    # water -- the lake + its creek/pond lobes, which are far larger -- and drop the dots.
    # Stands themselves come from sheet 04 (red markers).
    LAKE_AC = 0.30
    water_feats = []
    for g in water:
        ring = g["coordinates"][0]                       # outer ring of the Polygon
        ac = F.polygon_area_m2(ring) / 4046.86
        if ac < LAKE_AC:                                 # stand-dot contamination -- skip
            continue
        water_feats.append(F.feat(g, layer="water", klass="lake", area_ac=round(ac, 2)))
    F.write("water.geojson", F.fc(
        water_feats,
        sheet="06", layer="water / lake (blue)",
        method="HSV blue blobs -> contour polygons, projected; kept lake (>=0.30 ac), dropped blue stand-dots"))
    F.write("food-plots.geojson", F.fc(
        [F.feat(g, layer="food plot") for g in plots],
        sheet="06", layer="food plots / woods (green)", method="HSV blobs -> contour polygons, projected"))

    report["sheet06"] = {"lake_polys": len(water_feats), "food_plots": len(plots)}
    overlay(a6, [(green, [0,220,0]), (water_mask, [0,150,255]), (stand_mask, [255,80,255]), (pink, [255,0,120])],
            "_dbg-06-classified.png")

    # ===================== SHEET 02 (trails, best-effort) =====================
    a2, H2 = F.load_sheet("02-trails-green")
    proj2 = F.projector(H2)
    roi2, _ = F.boundary_roi(a2, H2)            # clip to the property; drop margin noise
    # trails are faint hand-drawn green -- fragmentary at best on this photo
    tg = F.colour_mask(a2, 70, 175, s_min=0.28, v_min=0.18) & roi2
    trails = F.lines_from_mask(tg, proj2, min_obj=20, simplify_m=4.0)
    F.write("trails.geojson", F.fc(
        [F.feat(g, layer="trail") for g in trails],
        sheet="02", layer="trails (green hand-drawn) - best-effort",
        method="HSV -> skeleton -> merged polylines, projected"))
    report["sheet02"] = {"trail_lines": len(trails), "green_px": int(tg.sum())}
    overlay(a2, [(tg, [0,230,0])], "_dbg-02-trails.png")

    # ===================== SHEET 04 (deer stands: red flag markers) =====================
    # Dedicated stands sheet. Stands are red flags (no blue-lake collision). Show ALL
    # detected markers -- inside AND outside the property -- tagged `inside`; the human
    # culls. No ROI clipping (that silently dropped real edge stands on the first pass).
    a4, H4 = F.load_sheet("04-deer-stands"); proj4 = F.projector(H4)
    roi4, _ = F.boundary_roi(a4, H4, pad_px=40)
    red = F.colour_mask(a4, 340, 20, s_min=0.30, v_min=0.20)
    lbl4, n4 = ndimage.label(red)
    stand_feats = []
    for i in range(1, n4 + 1):
        ys, xs = np.where(lbl4 == i)
        if len(xs) < 80:                       # drop speckle; keep faint markers
            continue
        cx, cy = float(xs.mean()), float(ys.mean())
        lon, lat = proj4(cx, cy)
        inside = bool(roi4[int(round(cy)), int(round(cx))])
        stand_feats.append(F.feat({"type": "Point", "coordinates": [round(lon, 7), round(lat, 7)]},
                                   layer="deer stand", inside=inside, px_area=int(len(xs))))
    F.write("stands.geojson", F.fc(
        stand_feats, sheet="04", layer="deer stands (red flag markers)",
        method="HSV red markers on sheet 04, projected; ALL shown, inside=within property boundary"))
    report["sheet04"] = {"stands_total": len(stand_feats),
                         "inside": sum(1 for f in stand_feats if f["properties"]["inside"]),
                         "outside": sum(1 for f in stand_feats if not f["properties"]["inside"])}
    overlay(a4, [(red, [255, 60, 60])], "_dbg-04-stands.png")

    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
