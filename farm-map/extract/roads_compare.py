#!/usr/bin/env python3
"""Roads & paths -- compare the source sheets head to head, don't fuse yet.

Each colour copy draws the road/path network differently (green on 02, orange on 03,
brown on 05). We extract each ONE separately, source-tagged + coloured, and project all
into the same frame so the founder can turn one on at a time over the imagery + OSM roads
and judge which sheet is accurate / complete (it may be that sheet 03 alone is enough).

Border-touching blobs (the wood table the photo sits on, page margins) are dropped with
clear_border so the table's orange/brown wood grain doesn't masquerade as roads. No
survey-ROI clip -- the network runs into the north tract.

Run:  python3 farm-map/extract/roads_compare.py
Out:  source-data/derived/roads-compare.geojson  +  demo/_dbg-roads-{02,03,05}.png
"""
import os, json
import numpy as np
from PIL import Image
from skimage.morphology import binary_closing, disk
from skimage.segmentation import clear_border
import featurelib as F

# sheet slug, source tag, marker description, HSV mask params, display colour
SOURCES = [
 ("02-trails-green",              "02", "green",  dict(hue_lo=70,  hue_hi=170, s_min=0.18, v_min=0.30), "#2fd02f"),
 ("03-trails-orange-water-blue",  "03", "orange", dict(hue_lo=10,  hue_hi=52,  s_min=0.30, v_min=0.28), "#ff8200"),
 ("05-habitat-full-color",        "05", "brown",  dict(hue_lo=12,  hue_hi=45,  s_min=0.22, v_min=0.18, v_max=0.62), "#a0642d"),
]

def overlay(a, mask, col, path, scale=(820, 1090)):
    from scipy import ndimage
    base = (a.astype(float) * 0.30).astype(np.uint8); out = base.copy()
    out[ndimage.binary_dilation(mask, iterations=1)] = col
    Image.fromarray(out).resize(scale).save(os.path.join(F.REPO, "farm-map", "demo", path))

def main():
    feats = []
    report = {}
    for slug, src, marker, params, color in SOURCES:
        a, H = F.load_sheet(slug); proj = F.projector(H)
        mask = F.colour_mask(a, **params)
        mask = clear_border(binary_closing(mask, disk(4)))      # connect strokes, drop table/margin
        lines = F.lines_from_mask(mask, proj, min_obj=60, simplify_m=3.0)
        feats += [F.feat(g, layer="road/path", source=src, marker=marker, color=color) for g in lines]
        report[src] = {"marker": marker, "features": len(lines), "mask_px": int(mask.sum())}
        overlay(a, mask, [255, 120, 0], "_dbg-roads-%s.png" % src)
    F.write("roads-compare.geojson", F.fc(
        feats, sheet="02 vs 03 vs 05", layer="roads & paths -- per-sheet comparison (draft)",
        method="HSV colour per sheet -> clear_border (drop table/margin) -> closing -> skeleton -> merged polylines, projected; source-tagged, NOT fused"))
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
