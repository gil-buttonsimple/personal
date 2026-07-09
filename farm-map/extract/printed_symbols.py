#!/usr/bin/env python3
"""Extract the surveyor's PRINTED symbols, using sheet 07's legend as a dictionary.

Everything extracted so far came from hand-drawn marker (orange, brown, green). But
the survey draws a whole second world in printed ink, and its legend names it:

    DIRT ROAD       two parallel rows of fine ticks
    TREE LINE       bold long dashes
    WATER           thin line, occasional dashes
    FLOOD EASEMENT  a single row of round dots
    PAVED ROAD      two parallel solid lines
    BOUNDARY        heavy solid
    R/W             dash-dot

Gil marked a path the extraction missed; 94.8% of it lay on printed linework and
only 2-5% on any hand ink. Zoomed, it is a single row of round dots following the
creek -- the FLOOD EASEMENT -- which he confirmed. So the printed layer carries
real features, and colour cannot separate them: every symbol is the same black.

What separates them is PERIODICITY AND SHAPE, not colour. A round dot is compact
and small. A dash is elongated. So the symbols are recovered by classifying the
printed blobs and then CHAINING them -- the marks never touch, so skeleton tracing
(which walks connected pixels) cannot see these lines at all. That is the deeper
reason the printed layer was invisible to every earlier pass.

This module does the dot symbols. Chaining walks dot to dot, preferring a straight
continuation, which is what makes a row of dots a line rather than a cloud.

Run:  python3 farm-map/extract/printed_symbols.py
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

DEMO = os.path.join(G.REPO, "farm-map", "demo")
LAT0 = 34.66


def printed_mask(slug, a):
    """Printed ink, with the heavy boundary stroke removed (it is also black)."""
    h = np.array(json.load(open(os.path.join(G.TX, slug + ".json")))["homography_px_to_world"])
    roi, _ = F.boundary_roi(a, h, pad_px=40)
    model_px = G.h_apply(np.linalg.inv(h), G.densify(F.SURVEY_LONLAT, 8.0, LAT0))
    not_boundary = ~R.corridor(a.shape[:2], model_px, 26)
    H, S, V = F.to_hsv(a)
    return (V < 0.58) & (S < 0.45) & roi & not_boundary


def blobs(mask, area_lo, area_hi, elong_max=None, elong_min=None, fill_min=None):
    """Centroids of components matching a shape signature."""
    lbl, n = ndimage.label(mask)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lbl)):
        if sl is None:
            continue
        sub = lbl[sl] == (i + 1)
        area = int(sub.sum())
        if area < area_lo or area > area_hi:
            continue
        hgt = sl[0].stop - sl[0].start
        wid = sl[1].stop - sl[1].start
        elong = max(hgt, wid) / max(1, min(hgt, wid))
        fill = area / float(hgt * wid)
        if elong_max is not None and elong > elong_max:
            continue
        if elong_min is not None and elong < elong_min:
            continue
        if fill_min is not None and fill < fill_min:
            continue
        ys, xs = np.where(sub)
        out.append((sl[1].start + xs.mean(), sl[0].start + ys.mean()))
    return np.array(out)


def chain_dots(pts, max_step, max_turn_deg=55.0, min_dots=6):
    """Walk a cloud of dots into polylines.

    From each unused dot, step to the nearest unused neighbour within `max_step`.
    After the first step a direction exists, so every later step takes the candidate
    best aligned with it (and rejects turns sharper than `max_turn_deg`). That
    directional preference is what keeps two dot rows crossing each other from
    fusing into one line.

    Each chain is grown from both ends of its seed, so a seed landing mid-line does
    not produce two half-lines.
    """
    if len(pts) == 0:
        return []
    tree = cKDTree(pts)
    used = np.zeros(len(pts), bool)
    cos_max = np.cos(np.radians(max_turn_deg))
    chains = []

    def grow(seed, first):
        path = [seed, first]
        used[seed] = used[first] = True
        while True:
            cur = path[-1]
            d = pts[cur] - pts[path[-2]]
            nd = np.linalg.norm(d)
            if nd == 0:
                break
            d = d / nd
            best, best_cos = None, cos_max
            for j in tree.query_ball_point(pts[cur], max_step):
                if used[j]:
                    continue
                v = pts[j] - pts[cur]
                nv = np.linalg.norm(v)
                if nv == 0:
                    continue
                c = float(np.dot(d, v / nv))
                if c > best_cos:
                    best, best_cos = j, c
            if best is None:
                break
            used[best] = True
            path.append(best)
        return path

    order = np.argsort(pts[:, 0])
    for s in order:
        if used[s]:
            continue
        nbrs = [j for j in tree.query_ball_point(pts[s], max_step) if j != s and not used[j]]
        if not nbrs:
            continue
        nbrs.sort(key=lambda j: np.linalg.norm(pts[j] - pts[s]))
        used[s] = True
        fwd = grow(s, nbrs[0])
        # grow backwards from the seed too
        back = []
        rest = [j for j in tree.query_ball_point(pts[s], max_step) if not used[j]]
        if rest:
            rest.sort(key=lambda j: np.linalg.norm(pts[j] - pts[s]))
            back = grow(s, rest[0])[1:]
        path = list(reversed(back)) + fwd
        if len(path) >= min_dots:
            chains.append(pts[path])
    return chains


def join_chains(chains, max_gap, max_turn_deg=40.0):
    """Weld chains that continue one another across an interruption.

    The dot rows are broken wherever a text label ("BRANCH", "TRANS LINE") is printed
    over them, so a single easement comes out as several chains. Two chains are joined
    when an endpoint of one is near an endpoint of the other AND their local directions
    agree -- proximity alone would zip together lines that merely cross.
    """
    chains = [np.asarray(c, float) for c in chains]
    cos_max = np.cos(np.radians(max_turn_deg))

    def tangent(c, at_end):
        seg = c[-min(4, len(c)):] if at_end else c[:min(4, len(c))][::-1]
        v = seg[-1] - seg[0]
        n = np.linalg.norm(v)
        return v / n if n else np.zeros(2)

    merged = True
    while merged:
        merged = False
        for i in range(len(chains)):
            if chains[i] is None:
                continue
            for j in range(len(chains)):
                if i == j or chains[j] is None:
                    continue
                for ei in (0, 1):
                    for ej in (0, 1):
                        a = chains[i][-1] if ei else chains[i][0]
                        b = chains[j][-1] if ej else chains[j][0]
                        if np.linalg.norm(a - b) > max_gap:
                            continue
                        ti = tangent(chains[i], ei == 1)
                        tj = tangent(chains[j], ej == 0)
                        if float(np.dot(ti, tj)) < cos_max:
                            continue
                        ci = chains[i] if ei else chains[i][::-1]
                        cj = chains[j] if ej == 0 else chains[j][::-1]
                        chains[i] = np.vstack([ci, cj])
                        chains[j] = None
                        merged = True
                        break
                    if merged:
                        break
                if merged:
                    break
            if merged:
                break
    return [c for c in chains if c is not None]


def main():
    slug = "07-deed-survey-kasparek"
    a = np.asarray(Image.open(os.path.join(G.ART, slug + ".jpg")).convert("RGB"))
    mask = printed_mask(slug, a)
    proj = R.projector(slug)

    dots = blobs(mask, 8, 80, elong_max=1.9, fill_min=0.55)
    print("round-dot marks found: %d" % len(dots))

    # typical spacing sets the chaining step: measure it, do not guess
    tree = cKDTree(dots)
    d, _ = tree.query(dots, k=2)
    spacing = float(np.median(d[:, 1]))
    print("median dot spacing: %.1f px -> max_step %.1f px" % (spacing, 2.4 * spacing))

    chains = chain_dots(dots, max_step=2.4 * spacing, min_dots=6)
    print("chains built: %d" % len(chains))
    chains = join_chains(chains, max_gap=9.0 * spacing)
    print("after joining across printed labels: %d" % len(chains))

    feats = []
    for ch in chains:
        w = proj(ch)
        g = LineString(w).simplify(3.0 / G.MLAT)
        L = G.line_len_m(g)
        if L < 60:
            continue
        feats.append(F.feat(mapping(g), layer="flood easement", symbol="single row of round dots",
                            source="sheet 07 printed", length_m=round(L), dots=int(len(ch))))
    feats.sort(key=lambda f: -f["properties"]["length_m"])
    print("flood-easement lines >=60 m: %d   total %.1f km"
          % (len(feats), sum(f["properties"]["length_m"] for f in feats) / 1000.0))
    for f in feats[:6]:
        print("   %5d m  (%d dots)" % (f["properties"]["length_m"], f["properties"]["dots"]))

    F.write("flood-easement.geojson", F.fc(
        feats, sheet="07", layer="flood easement (printed: single row of round dots)",
        method="printed-ink blobs classified by shape (compact, area 8-80 px) then CHAINED "
               "dot-to-dot with a straight-continuation preference; skeleton tracing cannot "
               "see these lines because the dots never touch",
        legend="sheet 07 legend: FLOOD EASEMENT = single row of round dots; DIRT ROAD = double "
               "row of fine ticks. Confirmed by Gil against the line he marked as missing."))

    vis = (a.astype(float) * 0.30).astype(np.uint8)
    vis[ndimage.binary_dilation(mask, iterations=1)] = [70, 70, 70]
    for (x, y) in np.round(dots).astype(int):
        vis[max(0, y-3):y+4, max(0, x-3):x+4] = [255, 0, 255]
    Image.fromarray(vis).resize((820, 1090)).save(os.path.join(DEMO, "_flood-07.png"))


if __name__ == "__main__":
    main()
