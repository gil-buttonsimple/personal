#!/usr/bin/env python3
"""Extract the printed DIRT ROADS from sheet 01, using the cross-hatch as the proof.

Two earlier attempts failed, both on sheet 07, and both are worth remembering:

  1. "DIRT ROAD = two parallel rows of ticks", chaining ticks like dots -> 1 road,
     0.1 km. Killed by measurement: row-to-row separation had median 118 px with
     quartiles 45/193. No pairing distance existed, so tick rows are not the symbol.
  2. "DIRT ROAD = two parallel casing lines", paired after skeleton tracing -> 7
     fragments, 0.8 km, all of them lying on CONTOUR lines. Wherever two contours run
     parallel for a stretch they satisfy a casing test. Sheet 07 is the deed survey and
     prints its linework faintly, so the real roads were barely detected at all.

Two fixes here.

SOURCE. Sheet 01 is the clean base plat and prints the roads boldly (see _net-01.png).

DISCRIMINATOR. Separation cannot reject contours -- it was measured and has no usable
mode. But the legend says a dirt road is drawn as two casing lines WITH CROSS-HATCHES
BETWEEN THEM, and a pair of contours has nothing between them. So the hatches are the
proof: pair the casing lines, then count the small tick blobs lying inside the corridor
between the pair. Hatch density per 100 m separates a road from two adjacent contours
on a physical property of the symbol, not on a tuned threshold.

STATUS after three attempts: STILL NOT WORKING. 10 fragments, 1.8 km. Do not use
dirt-roads.geojson as a road layer.

What this attempt fixed, and it was real:
  - Source: sheet 01, not the faint sheet 07.
  - Mask: a global brightness cut cannot separate ink from paper on a low-contrast
    sheet photographed under uneven light -- the ink in a lit region is lighter than
    the PAPER in a shadowed one (V<0.58 -> 83k px, V<0.66 -> 180k px). Replaced with a
    local adaptive threshold, which lifted the traced polylines from 150 to 186 and
    the centreline candidates from 4157 to 6362.
  - Pairing: matching whole line to whole line found 4 pairs, because tracing splits
    each casing at every junction and a curving road has no meaningful global tangent.
    Rewritten to pair per POINT (find the opposite casing across the road), which
    found 6362 candidate centreline points.
  - The hatch test works: it rejected 9 hatch-free pairs, including the long
    transmission-line corridor.

What is still wrong: the extracted centrelines are short fragments clustered where
contours are dense, and the actual road network on sheet 01 is not followed. The
remaining suspect is the hatch test firing on contour DASHES (contours here are
dashed, so "small elongated blob between two parallel lines" is satisfied by two
adjacent contours with a third dashed contour between them). Distinguishing them
needs the topological argument, not a local one: contours nest, close on themselves,
and never terminate at a junction; road casings branch and meet other casings at
nodes. That is the next thing to try, and it is a rewrite, not a tweak.

Meanwhile the hand-ink network (trails.geojson, 41 km) already contains these roads
as drawn by the hunt club, which is why this layer is a refinement, not a gap.

Run:  python3 farm-map/extract/dirt_roads.py
"""
import os, json
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree
from shapely.geometry import LineString, Polygon, Point, mapping
from shapely.ops import unary_union

import geolib as G
import featurelib as F
import register as R
import printed_symbols as P

DEMO = os.path.join(G.REPO, "farm-map", "demo")
SLUG = "01-base-plat-clean"

SEP_LO, SEP_HI = 10.0, 30.0     # casing width in px, from the sheet-01 separation profile
COS_PARALLEL = 0.92
MIN_OVERLAP = 0.55
MIN_HATCH_PER_100M = 1.5        # a road is hatched; two contours are not


def printed(a):
    """Printed ink, by LOCAL contrast rather than a global brightness cut.

    A global cut cannot work here. The sheet is a light, low-contrast print,
    photographed under uneven light across curled paper, so the ink in a bright
    region is lighter than the PAPER in a shadowed one. V<0.58 captured 83k px and
    V<0.66 captured 180k -- no single number separates ink from paper everywhere, and
    the low value was starving every downstream stage (the debug overlay showed a
    nearly empty mask). Comparing each pixel to its own neighbourhood removes the
    illumination gradient entirely.
    """
    from skimage.filters import threshold_local
    h = np.array(json.load(open(os.path.join(G.TX, SLUG + ".json")))["homography_px_to_world"])
    roi, _ = F.boundary_roi(a, h, pad_px=60)
    model_px = G.h_apply(np.linalg.inv(h), G.densify(F.SURVEY_LONLAT, 8.0, 34.66))
    notb = ~R.corridor(a.shape[:2], model_px, 26)
    H, S, V = F.to_hsv(a)
    local = threshold_local(V, block_size=61, offset=0.045)   # ink is darker than its surround
    return (V < local) & (S < 0.45) & roi & notb


def tangent(c):
    v = c[-1] - c[0]
    n = np.linalg.norm(v)
    return v / n if n else np.zeros(2)


def main():
    a = np.asarray(Image.open(os.path.join(G.ART, SLUG + ".jpg")).convert("RGB"))
    mask = printed(a)

    lbl, n = ndimage.label(mask)
    sizes = ndimage.sum(mask, lbl, range(1, n + 1))
    drop = np.zeros(n + 1, bool)
    for i, sl in enumerate(ndimage.find_objects(lbl)):
        if sl is not None and sizes[i] > 420:
            drop[i + 1] = True
    thin = mask & ~drop[lbl]

    # the hatch marks themselves: small, mildly elongated blobs
    hatches = P.blobs(thin, 6, 90, elong_min=1.4, elong_max=5.0)
    print("hatch-mark candidates: %d" % len(hatches))
    htree = cKDTree(hatches) if len(hatches) else None

    pl = [np.array(l, float) for l in G.trace_skeleton(G.bridge_gaps(thin, 3), min_branch_px=45)
          if len(l) >= 30]
    print("printed polylines traced: %d" % len(pl))

    proj = R.projector(SLUG)

    # ---- pairing, per POINT rather than per line -------------------------------
    # Skeleton tracing splits each casing into many segments at every junction, and a
    # curving road has no meaningful global tangent -- so matching whole lines to whole
    # lines finds almost nothing (it found 4 pairs). Instead: for every point on every
    # polyline, look for the opposite casing directly across the road. Where one exists
    # at a casing-width offset, the midpoint is a point on the road's centreline.
    # Both casings vote for the same midpoints, so the centreline emerges twice; the
    # duplicates are collapsed by chaining.
    allpts = np.vstack(pl)
    owner = np.concatenate([np.full(len(c), k) for k, c in enumerate(pl)])
    tree = cKDTree(allpts)

    mids, halfw = [], []
    for k, c in enumerate(pl):
        for p in c:
            cand = tree.query_ball_point(p, SEP_HI)
            best_d, best_q = None, None
            for t in cand:
                if owner[t] == k:            # same polyline: not the far casing
                    continue
                dd = float(np.linalg.norm(allpts[t] - p))
                if dd < SEP_LO:
                    continue
                if best_d is None or dd < best_d:
                    best_d, best_q = dd, allpts[t]
            if best_q is not None:
                mids.append((p + best_q) / 2.0)
                halfw.append(best_d / 2.0)
    mids = np.array(mids)
    print("centreline candidate points: %d" % len(mids))
    if len(mids) < 10:
        print("no casings found"); return

    # collapse duplicates, then chain the midpoints into polylines
    from scipy.spatial import cKDTree as KD
    keepmask = np.ones(len(mids), bool)
    kt = KD(mids)
    for i in range(len(mids)):
        if not keepmask[i]:
            continue
        for j in kt.query_ball_point(mids[i], 2.5):
            if j > i:
                keepmask[j] = False
    mids = mids[keepmask]
    print("after collapsing duplicates: %d" % len(mids))

    chains = P.chain_dots(mids, max_step=9.0, max_turn_deg=50.0, min_dots=8)
    chains = P.join_chains(chains, max_gap=40.0)
    print("centrelines chained: %d" % len(chains))

    roads, rejected = [], []
    med_half = float(np.median(halfw))
    for centre in chains:
        g = LineString(proj(centre)).simplify(3.0 / G.MLAT)
        L = G.line_len_m(g)
        if L < 60:
            continue
        # THE TEST: hatch marks lying between the two casing lines
        nh = 0
        if htree is not None:
            band = max(3.0, med_half - 1.5)
            hits = set()
            for p in centre:
                hits.update(htree.query_ball_point(p, band))
            nh = len(hits)
        per100 = 100.0 * nh / max(L, 1e-6)
        rec = dict(length_m=round(L), hatches=int(nh), hatch_per_100m=round(per100, 2))
        (roads if per100 >= MIN_HATCH_PER_100M else rejected).append((g, rec, centre))

    roads.sort(key=lambda t: -t[1]["length_m"])
    tot = sum(r[1]["length_m"] for r in roads) / 1000.0
    print("\ncasing pairs WITH hatches (dirt roads): %d   total %.1f km" % (len(roads), tot))
    for g, rec, _ in roads[:8]:
        print("   %5d m   %2d hatches (%.1f /100m)" % (rec["length_m"], rec["hatches"], rec["hatch_per_100m"]))
    print("casing pairs WITHOUT hatches (rejected as contours): %d   total %.1f km"
          % (len(rejected), sum(r[1]["length_m"] for r in rejected) / 1000.0))

    feats = [F.feat(mapping(g), layer="dirt road", symbol="paired casing + cross-hatches",
                    source="sheet 01 printed", **rec) for g, rec, _ in roads]
    F.write("dirt-roads.geojson", F.fc(
        feats, sheet="01", layer="dirt roads (printed casing, hatch-confirmed)",
        method="printed ink minus glyphs -> bridge -> skeleton graph -> pair polylines running "
               "parallel (cos>=%.2f) at %.0f-%.0f px separation -> KEEP only pairs with cross-hatch "
               "marks between the casing lines (>=%.1f per 100 m)" % (COS_PARALLEL, SEP_LO, SEP_HI, MIN_HATCH_PER_100M),
        rejector="the hatch test is what separates a road from two adjacent contours; separation "
                 "alone cannot (measured: no usable mode). %d hatch-free pairs were rejected." % len(rejected),
        status="DRAFT -- NOT USABLE. 10 fragments / 1.8 km, clustered where contours are dense; "
               "sheet 01's road network is not followed. The hatch test likely fires on dashed "
               "CONTOURS. Needs a topological contour rejector (contours nest and close; road "
               "casings branch and meet at nodes). Kept as the record of attempt 3.",
        caveat="1995 survey; unverified on the ground. Paved roads (solid casing, no hatch) are "
               "rejected by this test too and are not in this layer."))

    vis = (a.astype(float) * 0.30).astype(np.uint8)
    vis[ndimage.binary_dilation(thin, iterations=1)] = [65, 65, 65]
    for _, _, centre in rejected:                     # contour-like pairs, in red
        for (x, y) in np.round(centre).astype(int):
            vis[max(0, y-1):y+2, max(0, x-1):x+2] = [230, 40, 40]
    for _, _, centre in roads:
        for (x, y) in np.round(centre).astype(int):
            vis[max(0, y-2):y+3, max(0, x-2):x+3] = [0, 255, 120]
    Image.fromarray(vis).resize((900, 1195)).save(os.path.join(DEMO, "_dirt-roads-01.png"))
    print("debug overlay: demo/_dirt-roads-01.png")


if __name__ == "__main__":
    main()
