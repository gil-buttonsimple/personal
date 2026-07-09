#!/usr/bin/env python3
"""Re-extract the remaining annotation layers through the refit registration.

Deer stands (sheet 04, red markers) and food plots (sheet 06, green). Both were
already extracted in the first pass, but through the 4-point transforms, which are
off by a median of 3.1 m (sheet 04) and 5.6 m (sheet 06) against the drawn boundary.
Re-projecting costs nothing and is strictly more accurate.

Two corrections beyond re-projection:

  Stands. The first pass emitted 52 candidates. Most of the excess was not on the
  map at all: with no region-of-interest clip, the red mask was detecting the wooden
  table and coasters the sheet was photographed on. Restricting to a generous pad
  around the property leaves 25 markers whose pixel areas cluster tightly (201-319,
  median 256) -- the signature of one consistently drawn symbol. 19 fall inside the
  deed boundary, 6 on adjoining land. The legend numbers woods stands 40-50 and says
  to reuse food-plot numbers for stands on plots, so ~19 inside is the right order.

  Food plots. The legend numbers plots 1-30. This pass finds 24, so the layer is
  UNDER-detected, not over: small or faint green blobs are being missed at the
  250-px floor. Emitted as-is with areas; numbering and the missing plots are for
  digitizer validation against sheet 06, not for an auto-guess.

Run:  python3 farm-map/extract/rest.py
"""
import os, json
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.morphology import binary_closing, disk
from skimage.measure import find_contours
from shapely.geometry import Polygon, mapping

from shapely.geometry import Point as ShPoint

import geolib as G
import featurelib as F
import register as R

SURVEY = Polygon(F.SURVEY_LONLAT)

DEMO = os.path.join(G.REPO, "farm-map", "demo")


def sheet(slug):
    return np.asarray(Image.open(os.path.join(G.ART, slug + ".jpg")).convert("RGB"))


def old_h(slug):
    return np.array(json.load(open(os.path.join(G.TX, slug + ".json")))["homography_px_to_world"])


def stands():
    slug = "04-deer-stands"
    a = sheet(slug)
    proj = R.projector(slug)
    # Generous pad, not a property clip: real stands sit right on the boundary, but the
    # photo also contains a wooden table and reddish coasters, which the red mask loves.
    far, _ = F.boundary_roi(a, old_h(slug), pad_px=300)

    red = F.colour_mask(a, 340, 20, s_min=0.30, v_min=0.20) & far
    lbl, n = ndimage.label(red)
    sizes = ndimage.sum(red, lbl, range(1, n + 1))

    cand = [(i + 1, int(s)) for i, s in enumerate(sizes) if s >= 60]
    areas = np.array([s for _, s in cand])
    print("stand marker candidates >=60 px: %d" % len(cand))
    if len(areas):
        qs = np.percentile(areas, [10, 25, 50, 75, 90])
        print("  px-area percentiles 10/25/50/75/90: %s" % np.round(qs).astype(int).tolist())

    feats = []
    for i, s in cand:
        ys, xs = np.where(lbl == i)
        cx, cy = float(xs.mean()), float(ys.mean())
        lon, lat = proj(np.array([[cx, cy]]))[0]
        # Containment is decided in WORLD space against the deed traverse. Testing it
        # in pixel space against the old homography's ROI -- while projecting through
        # the new registration -- mixes two frames and mislabels edge markers.
        inside = SURVEY.contains(ShPoint(lon, lat))
        # compactness: a drawn marker is blobby, an ink smear or letter stroke is not
        bb = (xs.max() - xs.min() + 1) * (ys.max() - ys.min() + 1)
        feats.append(F.feat({"type": "Point", "coordinates": [round(float(lon), 7), round(float(lat), 7)]},
                            layer="deer stand", inside=inside, px_area=int(s),
                            compactness=round(float(s) / bb, 2)))
    ins = sum(1 for f in feats if f["properties"]["inside"])
    print("  markers: %d total, %d inside the property, %d outside" % (len(feats), ins, len(feats) - ins))
    F.write("stands.geojson", F.fc(
        feats, sheet="04", layer="deer stands (red markers)",
        method="HSV red markers, projected through the perimeter-refit registration",
        note="25 markers, px-area tightly clustered (201-319, median 256) = one drawn symbol. "
             "A generous pad excludes the wooden table/coasters the sheet was shot on, which the "
             "first pass mistook for markers. Still over-inclusive by design; culled in the digitizer"))
    return len(feats), ins


def food_plots():
    slug = "06-master-legend-1995"
    a = sheet(slug)
    proj = R.projector(slug)
    roi, _ = F.boundary_roi(a, old_h(slug), pad_px=60)

    green = F.colour_mask(a, 70, 170, s_min=0.30) & roi
    green = binary_closing(green, disk(3))
    lbl, n = ndimage.label(green)
    sizes = ndimage.sum(green, lbl, range(1, n + 1))

    feats = []
    for i in np.argsort(sizes)[::-1]:
        if sizes[i] < 250:
            break
        comp = lbl == (i + 1)
        cs = find_contours(comp.astype(float), 0.5)
        if not cs:
            continue
        ring = max(cs, key=len)
        px = np.array([[c, r] for r, c in ring])
        poly = Polygon(proj(px))
        if not poly.is_valid:
            poly = poly.buffer(0)
        poly = poly.simplify(3.0 / G.MLAT)
        if poly.is_empty:
            continue
        if poly.geom_type == "MultiPolygon":
            poly = max(poly.geoms, key=lambda g: g.area)
        ac = F.polygon_area_m2(list(poly.exterior.coords)) / 4046.86
        feats.append(F.feat(mapping(poly), layer="food plot", area_ac=round(ac, 2)))

    acres = sorted(f["properties"]["area_ac"] for f in feats)
    print("food plots: %d polygons, %.1f ac total, sizes %.2f-%.2f ac"
          % (len(feats), sum(acres), acres[0], acres[-1]))
    print("  legend numbers plots 1-30 -- this pass finds %d, so small/faint plots are MISSED" % len(feats))
    F.write("food-plots.geojson", F.fc(
        feats, sheet="06", layer="food plots (green)",
        method="HSV green blobs -> contour polygons, projected through the perimeter-refit registration",
        note="legend numbers food plots 1-30; only %d polygons detected -- the layer is "
             "UNDER-detected (faint/small green blobs fall below the 250-px floor). Plot "
             "NUMBERING and the missing plots are resolved by eye on sheet 06 in the digitizer"
             % len(feats)))
    return len(feats)


if __name__ == "__main__":
    stands()
    print()
    food_plots()
