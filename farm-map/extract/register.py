#!/usr/bin/env python3
"""Re-register every sheet against the whole drawn boundary, not four corners.

What was wrong. Each sheet's transform was fitted to exactly 4 control points --
the boundary apexes. A projective fit has 8 degrees of freedom, so 4 point-pairs
determine it exactly: residual zero at the corners by construction, and no
information at all about how well it does anywhere else. The stored
`residual_m_median: 0` was not a quality measure, it was arithmetic.

What this does. The 43-course deed traverse is exact in world coordinates and is
drawn on every sheet. Densify it, project it in with the old transform, snap each
point onto the boundary ink as it truly appears in the photo (ICP, tightening
radius), and refit -- now least-squares over ~350 correspondences spread around
the entire perimeter. Same model, vastly better conditioned, and for the first
time the residual means something.

What this does NOT do. It does not fix the interior. Zero OSM ways enter the
property, and no other independent interior reference exists, so interior accuracy
is interpolated and unverifiable. A thin-plate spline was tried (register_tps.py,
kept for the record) and rejected: with control only on the perimeter it fitted the
boundary no better than the projective model and was free to wander in the middle,
where there is no data to hold it. Cross-sheet agreement is our only interior check.

Run:  python3 farm-map/extract/register.py
"""
import os, json
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.draw import line as skline

import geolib as G
import featurelib as F

SHEETS = ["01-base-plat-clean", "02-trails-green", "03-trails-orange-water-blue",
          "04-deer-stands", "05-habitat-full-color", "06-master-legend-1995",
          "07-deed-survey-kasparek"]

BOUNDARY_INK = {"06-master-legend-1995": "pink"}   # everything else: printed/heavy black

LAT0 = 34.66
STEP_M = 8.0
RADII = [70, 40, 22, 12, 7]


def dark_mask(a):
    H, S, V = F.to_hsv(a)
    return (V < 0.45) & (S < 0.45)


def boundary_mask(a, slug):
    if BOUNDARY_INK.get(slug) == "pink":
        m = F.colour_mask(a, 322, 8, s_min=0.30, v_min=0.25)
        return m
    return dark_mask(a)


def corridor(shape, px, r):
    m = np.zeros(shape, bool)
    h, w = shape
    p = np.round(px).astype(int)
    for i in range(len(p)):
        c0, r0 = p[i]
        c1, r1 = p[(i + 1) % len(p)]
        if not (0 <= r0 < h and 0 <= c0 < w and 0 <= r1 < h and 0 <= c1 < w):
            continue
        rr, cc = skline(r0, c0, r1, c1)
        m[rr, cc] = True
    return ndimage.binary_dilation(m, iterations=r)


def register(slug, debug_dir=None):
    a = np.asarray(Image.open(os.path.join(G.ART, slug + ".jpg")).convert("RGB"))
    tx = json.load(open(os.path.join(G.TX, slug + ".json")))
    H_old = np.array(tx["homography_px_to_world"], float)

    model_world = G.densify(F.SURVEY_LONLAT, STEP_M, LAT0)
    ink = boundary_mask(a, slug)

    cur = np.linalg.inv(H_old)          # world -> px
    src = dst = None
    for r in RADII:
        model_px = G.h_apply(cur, model_world)
        mask = ink & corridor(a.shape[:2], model_px, r)
        if mask.sum() < 200:
            continue
        mp, snapped = G.icp_snap(mask, model_px, r)
        if len(mp) < 30:
            continue
        tree_idx = [int(np.argmin(np.abs(model_px - m).sum(1))) for m in mp]
        mw = model_world[np.array(tree_idx)]
        cur = G.h_fit(mw, snapped)
        src, dst = snapped, mw

    if src is None:
        raise RuntimeError("%s: ICP found no boundary" % slug)

    dst_m = G.world_to_m(dst, LAT0)
    H_new = G.h_fit(src, dst_m)                    # px -> local metres

    def resid(pred_m):
        e = np.linalg.norm(pred_m - dst_m, axis=1)
        return dict(median=round(float(np.median(e)), 2),
                    p90=round(float(np.percentile(e, 90)), 2),
                    max=round(float(e.max()), 2))

    old_m = G.world_to_m(G.h_apply(H_old, src), LAT0)
    r_old = resid(old_m)
    r_new = resid(G.h_apply(H_new, src))

    out = {
        "sheet": slug,
        "transform_type": "projective, least-squares over the full drawn perimeter",
        "lat0": LAT0,
        "control_points": int(len(src)),
        "control_source": "43-course deed traverse, ICP-snapped to the boundary ink",
        "homography_px_to_localm": H_new.tolist(),
        "residual_m_new": r_new,
        "residual_m_old_4pt": r_old,
        "note": "Residual is fit-to-perimeter only. The interior has no independent "
                "reference (0 OSM ways enter the property) and is not measured by this number.",
    }
    json.dump(out, open(os.path.join(G.TX, slug + ".reg.json"), "w"), indent=2)

    if debug_dir:
        vis = (a.astype(float) * 0.35).astype(np.uint8)
        vis[ink] = [70, 70, 200]
        for (c, r_) in np.round(src).astype(int):
            vis[max(0, r_ - 3):r_ + 4, max(0, c - 3):c + 4] = [255, 220, 0]
        Image.fromarray(vis).resize((820, 1090)).save(os.path.join(debug_dir, "_reg-%s.png" % slug[:2]))
    return out


def projector(slug):
    """px (col,row) -> (lon,lat) using the refitted registration."""
    d = json.load(open(os.path.join(G.TX, slug + ".reg.json")))
    H = np.array(d["homography_px_to_localm"], float)
    lat0 = d["lat0"]
    def f(px):
        return G.m_to_world(G.h_apply(H, px), lat0)
    return f


def main():
    dbg = os.path.join(G.REPO, "farm-map", "demo")
    rows = []
    for s in SHEETS:
        r = register(s, debug_dir=dbg)
        rows.append(r)
        o, n = r["residual_m_old_4pt"], r["residual_m_new"]
        print("%-32s ctrl=%3d | old-4pt med %6.2f p90 %7.2f max %8.2f | refit med %5.2f p90 %5.2f max %6.2f"
              % (s, r["control_points"], o["median"], o["p90"], o["max"], n["median"], n["p90"], n["max"]))
    json.dump({"sheets": rows}, open(os.path.join(G.TX, "_registration-report.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
