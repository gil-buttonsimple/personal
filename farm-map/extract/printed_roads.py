#!/usr/bin/env python3
"""Extract the printed DIRT ROAD / PAVED ROAD casings from sheet 07.

Correcting a wrong model. The first attempt read "DIRT ROAD = two parallel rows of
fine ticks" and chained the ticks as if they were dots. That produced one road, 0.1 km.
The measurement that killed it: row-to-row separation had median 118 px with quartiles
at 45 and 193 -- no pairing distance existed, because tick rows are not what the symbol
is. Zoomed, a dirt road is two parallel CONTINUOUS thin lines (a casing) with small
cross-hatches between them. Continuous means skeleton tracing sees it; the pairing of
the two casing lines is the signature.

So: printed ink, minus the large glyph blobs (letters and numerals), bridged across the
cross-hatch interruptions, skeletonized and walked as a graph. That yields ~270 printed
polylines -- contours, tree lines, creeks, roads, all mixed. Then the discriminator: a
road casing is TWO polylines running parallel, close, and overlapping along their
length. Its centreline is the mean of the pair, which is better than either line alone.

Contours are the adversary here: they also run near-parallel to one another. They are
rejected by requiring tight separation AND sustained overlap AND low curvature relative
to the pair -- contours drift apart and rejoin, casings do not.

STATUS: NOT WORKING. Do not use printed-roads.geojson as a road layer.
The current run yields 7 fragments totalling 0.8 km, and the debug overlay
(demo/_printed-roads-07.png) shows them lying on CONTOUR lines, not roads: where two
contours happen to run parallel for a stretch, they satisfy the casing test. The roads
themselves are barely picked up, because sheet 07 is the deed survey and its printed
linework is faint. Sheet 01 (the clean base plat) prints the roads boldly and is the
right source -- see _net-01.png, where the road network is plainly visible.

Next: rerun this against 01-base-plat-clean, and add a contour rejector. Contours are
closed, smoothly curving, and nest without ever terminating at a junction; road casings
terminate, branch, and meet other casings at nodes. That topological difference is a
far stronger discriminator than separation, which was measured and found to have no
usable mode (median 118 px, quartiles 45/193).

Run:  python3 farm-map/extract/printed_roads.py
"""
import os, json
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree
from shapely.geometry import LineString, mapping

import geolib as G
import featurelib as F
import register as R
import printed_symbols as P

DEMO = os.path.join(G.REPO, "farm-map", "demo")
SLUG = "07-deed-survey-kasparek"

SEP_LO, SEP_HI = 9.0, 26.0      # casing width, px
COS_PARALLEL = 0.94             # ~20 degrees
MIN_OVERLAP = 0.60              # fraction of the shorter line running alongside


def thin_printed(a):
    mask = P.printed_mask(SLUG, a)
    lbl, n = ndimage.label(mask)
    sizes = ndimage.sum(mask, lbl, range(1, n + 1))
    drop = np.zeros(n + 1, bool)
    for i, sl in enumerate(ndimage.find_objects(lbl)):
        if sl is not None and sizes[i] > 420:      # letters, numerals, solid symbols
            drop[i + 1] = True
    return mask & ~drop[lbl]


def tangent(c):
    v = c[-1] - c[0]
    n = np.linalg.norm(v)
    return v / n if n else np.zeros(2)


def local_parallel(ci, cj):
    """Fraction of cj running within [SEP_LO, SEP_HI] of ci, and their direction agreement."""
    d, _ = cKDTree(ci).query(cj)
    band = (d >= SEP_LO) & (d <= SEP_HI)
    return band.mean(), abs(float(np.dot(tangent(ci), tangent(cj))))


def main():
    a = np.asarray(Image.open(os.path.join(G.ART, SLUG + ".jpg")).convert("RGB"))
    thin = thin_printed(a)
    m = G.bridge_gaps(thin, 3)
    pl = [np.array(l, float) for l in G.trace_skeleton(m, min_branch_px=45) if len(l) >= 30]
    print("printed polylines traced: %d" % len(pl))

    proj = R.projector(SLUG)
    used = set()
    centres = []
    for i in range(len(pl)):
        if i in used:
            continue
        best, best_ov = None, MIN_OVERLAP
        for j in range(len(pl)):
            if j == i or j in used:
                continue
            ov, cosang = local_parallel(pl[i], pl[j])
            if cosang < COS_PARALLEL:
                continue
            if ov > best_ov:
                best, best_ov = j, ov
        if best is None:
            continue
        used.add(i); used.add(best)
        long_, short_ = (pl[i], pl[best]) if len(pl[i]) >= len(pl[best]) else (pl[best], pl[i])
        d, idx = cKDTree(short_).query(long_)
        keep = (d >= SEP_LO) & (d <= SEP_HI)
        if keep.sum() < 10:
            continue
        centres.append(((long_[keep] + short_[idx[keep]]) / 2.0, best_ov))

    print("casing pairs found: %d" % len(centres))

    feats = []
    for c, ov in centres:
        g = LineString(proj(c)).simplify(3.0 / G.MLAT)
        L = G.line_len_m(g)
        if L < 60:
            continue
        feats.append(F.feat(mapping(g), layer="road (printed casing)",
                            symbol="two parallel casing lines",
                            source="sheet 07 printed", length_m=round(L),
                            pair_overlap=round(float(ov), 2)))
    feats.sort(key=lambda f: -f["properties"]["length_m"])
    tot = sum(f["properties"]["length_m"] for f in feats) / 1000.0
    print("printed roads >=60 m: %d   total %.1f km" % (len(feats), tot))
    for f in feats[:8]:
        print("   %5d m  overlap %.2f" % (f["properties"]["length_m"], f["properties"]["pair_overlap"]))

    F.write("printed-roads.geojson", F.fc(
        feats, sheet="07", layer="roads from the printed casing (dirt + paved)",
        method="printed ink minus glyphs -> bridge -> skeleton graph -> pair polylines that run "
               "parallel (cos>=%.2f), separated %.0f-%.0f px, overlapping >=%.0f%% of their length; "
               "centreline = mean of the pair" % (COS_PARALLEL, SEP_LO, SEP_HI, 100 * MIN_OVERLAP),
        status="DRAFT -- NOT USABLE. These 7 fragments lie on contour lines, not roads. "
               "Sheet 07's printed linework is too faint; sheet 01 is the correct source. "
               "Kept only as the record of a failed approach.",
        caveat="DIRT vs PAVED is not distinguished. Contours mimic a casing wherever two run "
               "parallel for a stretch, and that is exactly what this run captured."))

    vis = (a.astype(float) * 0.30).astype(np.uint8)
    vis[ndimage.binary_dilation(thin, iterations=1)] = [70, 70, 70]
    for c, _ in centres:
        for (x, y) in np.round(c).astype(int):
            vis[max(0, y-2):y+3, max(0, x-2):x+3] = [0, 255, 120]
    Image.fromarray(vis).resize((900, 1195)).save(os.path.join(DEMO, "_printed-roads-07.png"))
    print("debug overlay: demo/_printed-roads-07.png")


if __name__ == "__main__":
    main()
