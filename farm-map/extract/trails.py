#!/usr/bin/env python3
"""Extract the road/trail network from every sheet that draws it, then fuse.

Why the old pass produced 3,288 fragments. It skeletonized the ink, emitted one
LineString per pair of adjacent skeleton pixels, and called shapely's `linemerge`.
`linemerge` only welds runs that meet end-to-end pairwise, so every junction (3+
neighbours) and every pen-lift severs the line. The data was never the problem --
the network was shattered by the merge step. Here the skeleton is walked as a
graph, junction to junction, and gaps are bridged before the walk.

Three hand-drawn inks draw the same network (a fourth source was tried and rejected):

  03  orange   bold, saturated, complete across both tracts -- the primary
  05  brown    bold, complete, but hue-adjacent to the printed black linework
  02  green    faint pencil, western half only -- the source the first pass used,
               and the reason trails were written off as needing a rescan
  01  printed  the surveyor's dashed dirt-road linework. TRIED AND REJECTED -- see
               the note above SOURCES. Its ink is indistinguishable, by colour and
               thickness, from the contours and lettering.

Fusion tags each line with how many independent sheets draw it. A line all three
sheets agree on is as good as this paper gets; a line only one sheet shows is a
candidate to check on the ground.

Run:  python3 farm-map/extract/trails.py
"""
import os, json
import numpy as np
from PIL import Image
from scipy import ndimage
from shapely.geometry import mapping, MultiLineString
from shapely.ops import unary_union

import geolib as G
import featurelib as F
import register as R

DEMO = os.path.join(G.REPO, "farm-map", "demo")
LAT0 = 34.66


def sheet(slug):
    return np.asarray(Image.open(os.path.join(G.ART, slug + ".jpg")).convert("RGB"))


def roi_for(slug, a, pad_px=220):
    """Generous property ROI. The network runs off the survey polygon into the north
    tract, so this is a margin/legend rejecter, not a property clip."""
    h = np.array(json.load(open(os.path.join(G.TX, slug + ".json")))["homography_px_to_world"])
    roi, _ = F.boundary_roi(a, h, pad_px=pad_px)
    return roi


def net_from(slug, mask, bridge, min_branch, min_len_m, dbg_name, dbg_col):
    a_shape = mask.shape
    m = G.bridge_gaps(mask, bridge)
    px_lines = G.trace_skeleton(m, min_branch_px=min_branch)
    proj = R.projector(slug)
    lines = G.project_lines(px_lines, proj, simplify_m=2.5, min_len_m=min_len_m, lat0=LAT0)
    return lines, m


def dbg(a, layers, name):
    vis = (a.astype(float) * 0.30).astype(np.uint8)
    for m, col in layers:
        vis[m] = col
    Image.fromarray(vis).resize((820, 1090)).save(os.path.join(DEMO, name))


# ---- per-sheet ink recipes --------------------------------------------------
def ink_03(a, roi):
    # bold orange marker
    return F.colour_mask(a, 8, 50, s_min=0.35, v_min=0.30) & roi


def ink_05(a, roi):
    # Brown ink: orange-ish hue, but darker and far less saturated than 03's marker,
    # so 03's threshold starves it (a sweep put s>0.28 at 10k px against 03's 91k).
    # Saturation still has to stay above the printed black linework, which is neutral.
    H, S, V = F.to_hsv(a)
    return (H >= 5) & (H < 45) & (S > 0.15) & (V > 0.15) & (V < 0.62) & roi


def ink_02(a, roi):
    # faint green pencil: saturation is low, so lean on hue and let bridging heal it
    return F.colour_mask(a, 65, 175, s_min=0.14, v_min=0.30) & roi


# Sheet 01 (printed dashed dirt-road linework) was tried and REJECTED as a trail
# source. "Thin + dark + unsaturated" is not a description of the dirt roads; it is a
# description of every printed contour, tree line, lot line, and text label on the
# sheet, and the mask returned all of them (278 lines / 21.7 km, see _net-01.png in
# the first run). Separating the dirt roads would need a dash-period detector, and
# the payoff is low: the printed roads are the surveyor's base linework, carrying no
# field knowledge that the three hand-drawn inks do not already record.

SOURCES = [
    ("03-trails-orange-water-blue", ink_03, 4, 30, 25.0, [255, 130, 0]),
    ("05-habitat-full-color",       ink_05, 4, 30, 25.0, [180, 100, 40]),
    ("02-trails-green",             ink_02, 5, 30, 25.0, [0, 220, 0]),
]


def main():
    nets = {}
    for slug, inkfn, bridge, min_branch, min_len, col in SOURCES:
        a = sheet(slug)
        roi = roi_for(slug, a)
        mask = inkfn(a, roi)
        lines, m = net_from(slug, mask, bridge, min_branch, min_len, None, col)
        nets[slug[:2]] = lines
        tot = sum(G.line_len_m(g) for g in lines)
        print("%-32s ink_px=%7d  lines=%4d  total=%7.0f m" % (slug, mask.sum(), len(lines), tot))
        dbg(a, [(mask, col), (m & ~mask, [90, 90, 90])], "_net-%s.png" % slug[:2])

    # ---- fuse: how many sheets draw each line? -----------------------------
    TOL_M = 18.0                       # cross-sheet agreement tolerance
    tol_deg = TOL_M / G.MLAT
    buffers = {k: unary_union([g.buffer(tol_deg) for g in v]) if v else None
               for k, v in nets.items()}

    feats = []
    for k, lines in nets.items():
        for g in lines:
            support = []
            for k2, buf in buffers.items():
                if k2 == k or buf is None:
                    continue
                inter = g.intersection(buf)
                if not inter.is_empty and inter.length > 0.5 * g.length:
                    support.append(k2)
            feats.append(F.feat(
                mapping(g),
                layer="road/trail", klass="unclassified", source=k,
                length_m=round(G.line_len_m(g)),
                confirmed_by=sorted(support),
                sheet_support=1 + len(support)))

    by = {}
    for f in feats:
        by[f["properties"]["sheet_support"]] = by.get(f["properties"]["sheet_support"], 0) + 1
    print("\nfused features: %d" % len(feats))
    print("sheet support histogram (1 = only one sheet draws it): %s" % dict(sorted(by.items())))

    F.write("trails.geojson", F.fc(
        feats,
        sheets="02+03+05",
        layer="roads & trails (internal network, unclassified)",
        method="per-sheet ink mask -> gap bridge -> skeleton GRAPH walk (junction to junction) "
               "-> projected through the perimeter-refit registration -> simplified",
        fusion="each line tagged with the other sheets that draw it within %.0f m "
               "(confirmed_by / sheet_support)" % TOL_M,
        caveat="tier (main road / dirt / two-track / foot trail) is NOT determined by ink colour "
               "and remains unclassified; all annotations date to the 1995 survey"))


if __name__ == "__main__":
    main()
