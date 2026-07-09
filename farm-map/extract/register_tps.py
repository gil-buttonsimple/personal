#!/usr/bin/env python3
"""Re-register every sheet with a thin-plate spline instead of a 4-point homography.

Why. The existing transforms are exact at four boundary apexes and nowhere else.
A homography is a rigid family: it can rotate, scale, and keystone, but it cannot
bend. These sheets are folded paper shot with a phone, so the true pixel->world map
IS bent, and the error shows up where we care -- through the interior, where the
trails and the lake live.

How. The 43-course deed traverse is a known, exact polygon in world coordinates.
It is also visibly drawn on every sheet. So: project the traverse into the sheet
with the old homography (a good initial guess), snap each of ~500 densified traverse
points onto the boundary line as it actually appears in the photo, refit, repeat
with a tightening search radius. That yields correspondences all the way around the
perimeter. A regularized TPS through them absorbs the fold.

Honest limit. Control is perimeter-only, so the interior is interpolated, not
measured. TPS interpolation is smooth and well-behaved, and it beats a homography
because the fold is largely a perimeter-observable deformation -- but interior
accuracy remains an estimate. Cross-sheet agreement (see fuse_trails.py) is the
independent check on it.

Run:  python3 farm-map/extract/register_tps.py
"""
import os, json
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.draw import line as skline

import geolib as G
import featurelib as F

SHEETS = [
    "01-base-plat-clean",
    "02-trails-green",
    "03-trails-orange-water-blue",
    "04-deer-stands",
    "05-habitat-full-color",
    "06-master-legend-1995",
    "07-deed-survey-kasparek",
]

# Which ink draws the property boundary on each sheet. `dark` = printed/heavy black.
BOUNDARY_INK = {
    "01-base-plat-clean": "dark",
    "02-trails-green": "dark",
    "03-trails-orange-water-blue": "dark",
    "04-deer-stands": "dark",
    "05-habitat-full-color": "dark",
    "06-master-legend-1995": "pink",
    "07-deed-survey-kasparek": "dark",
}

LAT0 = 34.66
STEP_M = 8.0          # traverse densification
RADII = [70, 40, 22, 12, 7]   # ICP search radius schedule, pixels
SMOOTH = 40.0         # TPS regularizer, px^2 -- absorbs ICP slide along the line


def dark_mask(a):
    """Printed / heavy ink: low value, low saturation."""
    H, S, V = F.to_hsv(a)
    return (V < 0.45) & (S < 0.45)


def boundary_mask(a, ink):
    if ink == "pink":
        m = F.colour_mask(a, 322, 8, s_min=0.30, v_min=0.25)
        # highlighter is a broad wash; thin it toward its centreline
        return ndimage.binary_erosion(m, iterations=2) | (m & ~ndimage.binary_erosion(m, iterations=1))
    return dark_mask(a)


def corridor(shape, px, r):
    """Rasterize the model polyline and dilate it into a search corridor."""
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
    H = np.array(tx["homography_px_to_world"], float)
    Hinv = np.linalg.inv(H)

    model_world = G.densify(F.SURVEY_LONLAT, STEP_M, LAT0)       # (N,2) lon,lat
    model_m = G.world_to_m(model_world, LAT0)

    ink = boundary_mask(a, BOUNDARY_INK[slug])

    cur = Hinv.copy()   # world->px, refined each round
    stats = []
    kept_px = kept_world = None

    for r in RADII:
        model_px = G.h_apply(cur, model_world)
        corr = corridor(a.shape[:2], model_px, r)
        mask = ink & corr
        if mask.sum() < 200:
            stats.append({"radius": r, "matched": 0, "note": "too few boundary pixels"})
            continue
        mp, snapped = G.icp_snap(mask, model_px, r)
        if len(mp) < 30:
            stats.append({"radius": r, "matched": int(len(mp))})
            continue
        # world->px refit on the snapped correspondences
        idx = np.array([np.argmin(np.abs(model_px - m).sum(1)) for m in mp])
        mw = model_world[idx]
        cur = G.h_fit(mw, snapped)
        kept_px, kept_world = snapped, mw
        pred = G.h_apply(np.linalg.inv(cur), snapped)
        e = np.linalg.norm(G.world_to_m(pred, LAT0) - G.world_to_m(mw, LAT0), axis=1)
        stats.append({"radius": r, "matched": int(len(mp)),
                      "proj_resid_m_median": round(float(np.median(e)), 2),
                      "proj_resid_m_p90": round(float(np.percentile(e, 90)), 2)})

    if kept_px is None:
        raise RuntimeError("%s: ICP found no boundary" % slug)

    # subsample correspondences for a tractable, well-conditioned TPS
    n = len(kept_px)
    take = np.linspace(0, n - 1, min(n, 350)).astype(int)
    src = kept_px[take]
    dst = G.world_to_m(kept_world[take], LAT0)
    # dedupe identical snapped pixels (ICP can map several model pts to one pixel)
    _, uniq = np.unique(src, axis=0, return_index=True)
    src, dst = src[np.sort(uniq)], dst[np.sort(uniq)]

    tps = G.tps_fit(src, dst, smooth=SMOOTH)
    pred = G.tps_apply(tps, src)
    e = np.linalg.norm(pred - dst, axis=1)

    # projective residual on the SAME correspondences, for an apples-to-apples number
    Hproj = G.h_fit(src, dst)
    ep = np.linalg.norm(G.h_apply(Hproj, src) - dst, axis=1)

    out = {
        "sheet": slug,
        "transform_type": "thin-plate spline (pixel -> local metres -> WGS84)",
        "lat0": LAT0,
        "control_points": int(len(src)),
        "control_source": "43-course deed traverse, ICP-snapped to the drawn boundary",
        "smooth": SMOOTH,
        "tps_resid_m_median": round(float(np.median(e)), 2),
        "tps_resid_m_p90": round(float(np.percentile(e, 90)), 2),
        "tps_resid_m_max": round(float(e.max()), 2),
        "projective_resid_m_median": round(float(np.median(ep)), 2),
        "projective_resid_m_p90": round(float(np.percentile(ep, 90)), 2),
        "icp_rounds": stats,
        "tps": G.tps_to_json(tps),
    }
    p = os.path.join(G.TX, slug + ".tps.json")
    json.dump(out, open(p, "w"))

    if debug_dir:
        vis = (a.astype(float) * 0.35).astype(np.uint8)
        vis[ink] = [90, 90, 255]
        # reprojected traverse via TPS: world->px needs the inverse, so draw the
        # control correspondences instead (that is what the fit actually saw)
        for (c, r_) in np.round(src).astype(int):
            rr = slice(max(0, r_ - 3), r_ + 4)
            cc = slice(max(0, c - 3), c + 4)
            vis[rr, cc] = [255, 220, 0]
        Image.fromarray(vis).resize((820, 1090)).save(
            os.path.join(debug_dir, "_reg-%s.png" % slug[:2]))
    return out


def main():
    dbg = os.path.join(G.REPO, "farm-map", "demo")
    rows = []
    for s in SHEETS:
        r = register(s, debug_dir=dbg)
        rows.append(r)
        print("%-32s ctrl=%3d  TPS med %5.2f m  p90 %6.2f m   (projective med %6.2f m  p90 %7.2f m)"
              % (s, r["control_points"], r["tps_resid_m_median"], r["tps_resid_m_p90"],
                 r["projective_resid_m_median"], r["projective_resid_m_p90"]))
    json.dump({"sheets": [{k: v for k, v in r.items() if k != "tps"} for r in rows]},
              open(os.path.join(G.TX, "_registration-report.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
