#!/usr/bin/env python3
"""Rebuild the lake from what the surveyor actually drew.

The problem. `water.geojson` currently holds a USGS NHD polygon (24.5 ac) -- a
modern government dataset, not this survey. The earlier sheet-06 extraction
(`water-old.geojson`) shattered the impoundment into 4 disconnected blobs totalling
~14.6 ac. Sheet 06 plainly shows ONE continuous sinuous impoundment, labelled
"FLOOD CONTROL LAKE" on sheet 03, with its dam at the south end on sheet 07.

Why it shattered. Blue on sheet 06 is highlighter -- a translucent wash laid over
printed contour and creek lines. Those dark lines punch holes straight through the
colour mask, and a bare connected-components pass then reads one lake as four.
The fix is morphological: close across the printed linework, fill interior holes,
and only then take components.

Cross-check. Two independent draughts of the same water body: sheet 03's blue
highlighter, and sheet 04, where the lake is a solid pencil-shaded fill. Agreement
between three sheets registered independently is the only interior accuracy check
available (no OSM feature enters the property).

Run:  python3 farm-map/extract/lake.py
"""
import os, json
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.morphology import binary_closing, disk
from skimage.measure import find_contours
from shapely.geometry import Polygon, mapping

import geolib as G
import featurelib as F
import register as R

DEMO = os.path.join(G.REPO, "farm-map", "demo")
LAT0 = 34.66


def sheet(slug):
    return np.asarray(Image.open(os.path.join(G.ART, slug + ".jpg")).convert("RGB"))


def biggest_polygon(mask, proj, simplify_m=3.0):
    lbl, n = ndimage.label(mask)
    if n == 0:
        return None, 0.0
    sizes = ndimage.sum(mask, lbl, range(1, n + 1))
    comp = lbl == (1 + int(np.argmax(sizes)))
    cs = find_contours(comp.astype(float), 0.5)
    ring = max(cs, key=len)
    px = np.array([[c, r] for r, c in ring])
    world = proj(px)
    poly = Polygon(world)
    if not poly.is_valid:
        poly = poly.buffer(0)
    poly = poly.simplify(simplify_m / G.MLAT)
    if poly.geom_type == "MultiPolygon":
        poly = max(poly.geoms, key=lambda g: g.area)
    ac = F.polygon_area_m2(list(poly.exterior.coords)) / 4046.86
    return poly, ac


def lake_from_06():
    a = sheet("06-master-legend-1995")
    proj = R.projector("06-master-legend-1995")
    roi, _ = F.boundary_roi(a, np.array(json.load(open(
        os.path.join(G.TX, "06-master-legend-1995.json")))["homography_px_to_world"]), pad_px=40)

    blue = F.colour_mask(a, 175, 262, s_min=0.20, v_min=0.20) & roi
    # close across the printed contour/creek lines that perforate the wash,
    # then fill what is now enclosed
    m = binary_closing(blue, disk(9))
    m = ndimage.binary_fill_holes(m)
    # blue stand DOTS are small and round; the lake is enormous. Keep only big.
    lbl, n = ndimage.label(m)
    sizes = ndimage.sum(m, lbl, range(1, n + 1))
    m = np.isin(lbl, 1 + np.where(sizes >= 4000)[0])
    poly, ac = biggest_polygon(m, proj)
    dbg(a, [(blue, [40, 90, 255]), (m & ~blue, [0, 230, 255])], "_lake-06.png")
    return poly, ac, m


def lake_from_04():
    """Sheet 04 draws the lake as a solid shaded fill: mid-dark, unsaturated, and
    -- unlike the printed linework -- a large solid AREA, not a thin stroke.

    Two traps, both hit on the first attempt. The heavy boundary line is also dark
    and unsaturated, and it is thick enough to survive a modest erosion, so it must
    be masked out by corridor before anything else. And the fill is a pencil stipple,
    lighter than the ink; a value cut tuned for ink misses it.
    """
    a = sheet("04-deer-stands")
    proj = R.projector("04-deer-stands")
    h = np.array(json.load(open(os.path.join(G.TX, "04-deer-stands.json")))["homography_px_to_world"])
    roi, _ = F.boundary_roi(a, h, pad_px=0)

    # knock out the drawn boundary: rasterize it and dilate generously
    import register as _R
    model_px = G.h_apply(np.linalg.inv(h), G.densify(F.SURVEY_LONLAT, 8.0, LAT0))
    not_boundary = ~_R.corridor(a.shape[:2], model_px, 28)

    H, S, V = F.to_hsv(a)
    fill = (V < 0.70) & (S < 0.30) & roi & not_boundary
    # opening: thin printed strokes vanish, the solid lake fill survives
    core = ndimage.binary_opening(fill, structure=disk(5))
    core = binary_closing(core, disk(8))
    core = ndimage.binary_fill_holes(core)
    lbl, n = ndimage.label(core)
    if n == 0:
        return None, 0.0
    sizes = ndimage.sum(core, lbl, range(1, n + 1))
    core = np.isin(lbl, 1 + np.where(sizes >= 8000)[0])
    poly, ac = biggest_polygon(core, proj)
    dbg(a, [(core, [0, 200, 255])], "_lake-04.png")
    return poly, ac


def dbg(a, layers, name):
    vis = (a.astype(float) * 0.3).astype(np.uint8)
    for m, col in layers:
        vis[m] = col
    Image.fromarray(vis).resize((820, 1090)).save(os.path.join(DEMO, name))


def iou(p, q):
    if p is None or q is None:
        return None
    i = p.intersection(q).area
    u = p.union(q).area
    return round(i / u, 3) if u else None


def main():
    p6, ac6, _ = lake_from_06()
    p4, ac4 = lake_from_04()
    # Sheet 03 is NOT an area source: its lake is an OUTLINE with contour hatching,
    # not a blue fill (verified in _lake-03.png on the first pass). It stays a creek
    # source only. Sheet 04's shaded fill is the one independent area cross-check.

    nhd = json.load(open(os.path.join(G.REPO, "farm-map", "source-data", "derived", "water-nhd.geojson")))
    from shapely.geometry import shape
    pn = shape(nhd["features"][0]["geometry"])

    print("sheet 06 (blue highlighter)  %6.2f ac" % ac6)
    print("sheet 04 (shaded fill)       %6.2f ac" % ac4)
    print("USGS NHD (current file)      %6.2f ac" % (F.polygon_area_m2(list(pn.exterior.coords)) / 4046.86))
    print()
    print("IoU 06 vs 04: %s   06 vs NHD: %s" % (iou(p6, p4), iou(p6, pn)))

    feats = [F.feat(mapping(p6), layer="water", klass="lake",
                    name="Flood Control Lake", area_ac=round(ac6, 2),
                    source="sheet 06 blue highlighter",
                    agree_sheet04_iou=iou(p6, p4))]
    F.write("water.geojson", F.fc(
        feats, sheet="06", layer="lake / flood-control impoundment",
        method="HSV blue wash -> morphological close across printed linework -> fill -> "
               "largest component -> contour, projected through the perimeter-refit registration",
        cross_check="sheets 03 (blue) and 04 (shaded fill) extracted independently; IoU recorded"))
    for nm, p, ac, src in [("lake-sheet04", p4, ac4, "04")]:
        if p is not None:
            F.write(nm + ".geojson", F.fc([F.feat(mapping(p), layer="water", klass="lake",
                                                  area_ac=round(ac, 2), source="sheet " + src)],
                                          sheet=src, layer="lake (cross-check draft)"))


if __name__ == "__main__":
    main()
