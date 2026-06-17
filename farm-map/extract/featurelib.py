"""Shared helpers for vectorizing colour-keyed features off the survey sheets.

Everything funnels through one idea: a sheet's saved homography maps its pixels to
world coordinates, so any feature we can isolate in pixel space (by colour) we can
place on the map. Colour work is done in HSV (hue is stable under the uneven phone
exposure; RGB thresholds are not). Geometry comes out as real GeoJSON types:
points for stands, polygons for water/plots, merged polylines for trails.

Quality is best-effort: phone photos + a 4-point projective fit per sheet means
tens-of-metres wobble away from the control points and fragmented thin features.
The output is a draft to validate/correct in the digitizer, not survey truth.
"""
import os, json
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.morphology import skeletonize, remove_small_objects, binary_closing, disk
from skimage.measure import find_contours
from skimage.draw import polygon as skpolygon
from shapely.geometry import LineString, MultiLineString, Point, Polygon, mapping
from shapely.ops import linemerge, unary_union

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART  = os.path.join(REPO, "farm-map", "source-art")
TX   = os.path.join(REPO, "farm-map", "source-data", "transforms")

# Exact registered survey boundary (world lon,lat) -- traverse + POB-pinned SHIFT,
# identical to demo/index.html. Used to build a per-sheet ROI by inverse-projecting
# it into that sheet's pixel space (robust; independent of extracting the pink line).
_SHIFT = (-0.0011753, 0.0019292)
_RAW = [
 (34.6495527,-81.1523474),(34.6536156,-81.1568293),(34.6601593,-81.1640557),
 (34.6602285,-81.1639634),(34.6614509,-81.1623321),(34.6627292,-81.1637436),
 (34.6677877,-81.1569951),(34.6726967,-81.1534565),(34.6701087,-81.1513568),
 (34.6697552,-81.1504037),(34.6679685,-81.1507564),(34.6676831,-81.1494846),
 (34.6669591,-81.1494366),(34.6662387,-81.1495769),(34.6661748,-81.1495278),
 (34.6661226,-81.1494438),(34.6659990,-81.1494844),(34.6657248,-81.1494687),
 (34.6656399,-81.1495002),(34.6655156,-81.1494813),(34.6654462,-81.1495285),
 (34.6653266,-81.1495547),(34.6651742,-81.1494303),(34.6649675,-81.1492525),
 (34.6649649,-81.1491757),(34.6633606,-81.1493578),(34.6629126,-81.1492898),
 (34.6618783,-81.1489730),(34.6621229,-81.1499263),(34.6625455,-81.1515752),
 (34.6610315,-81.1521945),(34.6579598,-81.1534454),(34.6546086,-81.1548209),
 (34.6530302,-81.1493460),(34.6530003,-81.1492423),(34.6529604,-81.1492812),
 (34.6528464,-81.1494119),(34.6525019,-81.1498402),(34.6522948,-81.1500943),
 (34.6520949,-81.1503260),(34.6510338,-81.1514756),(34.6508461,-81.1516602),
 (34.6508878,-81.1518282)]
SURVEY_LONLAT = [(lon + _SHIFT[1], lat + _SHIFT[0]) for (lat, lon) in _RAW]

# ---- colour ----------------------------------------------------------------
def to_hsv(a):
    a = a.astype(float) / 255.0
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(-1); mn = a.min(-1); d = mx - mn
    V = mx; S = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0)
    H = np.zeros_like(mx)
    rm = (mx == R); gm = (mx == G) & ~rm; bm = (mx == B) & ~rm & ~gm
    with np.errstate(invalid="ignore", divide="ignore"):
        H[rm] = ((G - B)[rm] / np.maximum(d[rm], 1e-6)) % 6
        H[gm] = ((B - R)[gm] / np.maximum(d[gm], 1e-6)) + 2
        H[bm] = ((R - G)[bm] / np.maximum(d[bm], 1e-6)) + 4
    return (H * 60) % 360, S, V

def colour_mask(a, hue_lo, hue_hi, s_min=0.30, v_min=0.20, v_max=0.97):
    H, S, V = to_hsv(a)
    base = (S > s_min) & (V > v_min) & (V < v_max)
    if hue_lo <= hue_hi:
        hue = (H >= hue_lo) & (H < hue_hi)
    else:                                    # wrap-around (e.g. pink/red across 360)
        hue = (H >= hue_lo) | (H < hue_hi)
    return base & hue

# ---- sheet + homography ----------------------------------------------------
def load_sheet(slug):
    a = np.asarray(Image.open(os.path.join(ART, slug + ".jpg")).convert("RGB"))
    tx = json.load(open(os.path.join(TX, slug + ".json")))
    return a, tx["homography_px_to_world"]

def projector(H):
    """Return f(col,row)->(lon,lat) for the px->world homography."""
    def f(c, r):
        w = H[2][0] * c + H[2][1] * r + H[2][2]
        return ((H[0][0] * c + H[0][1] * r + H[0][2]) / w,
                (H[1][0] * c + H[1][1] * r + H[1][2]) / w)
    return f

def selfcheck(H, gcps):
    f = projector(H); mlat = 111320.0; worst = 0.0
    for p in gcps:
        c, r = p["pixel"]; lat, lon = p["world"]
        plon, plat = f(c, r); mlon = 111320.0 * np.cos(np.radians(lat))
        worst = max(worst, np.hypot((plon - lon) * mlon, (plat - lat) * mlat))
    return worst

# ---- region of interest (the property, inverse-projected onto the sheet) ----
def world_to_px(H):
    Hinv = np.linalg.inv(np.array(H))
    def g(lon, lat):
        v = Hinv @ np.array([lon, lat, 1.0]); return v[0] / v[2], v[1] / v[2]
    return g

def boundary_roi(a, H, pad_px=60):
    """ROI = the known survey polygon, inverse-projected into this sheet's pixels
    and rasterized. Robust (does not depend on cleanly extracting the pink line);
    auto-excludes the legend box and margins, which fall outside the property."""
    g = world_to_px(H)
    cols, rows = [], []
    for lon, lat in SURVEY_LONLAT:
        c, r = g(lon, lat); cols.append(c); rows.append(r)
    h, w = a.shape[:2]
    rr, cc = skpolygon(np.array(rows), np.array(cols), shape=(h, w))
    roi = np.zeros((h, w), bool); roi[rr, cc] = True
    if pad_px:
        roi = ndimage.binary_dilation(roi, iterations=pad_px)
    pink = colour_mask(a, 322, 8, s_min=0.33)     # still returned for the boundary layer
    return roi, pink

# ---- geometry builders -----------------------------------------------------
def points_from_blobs(mask, proj, area_min, area_max, circ_min=0.0):
    """Centroids of compact blobs -> list of (lon,lat). For dot features (stands)."""
    lbl, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lbl == i)
        area = len(xs)
        if area < area_min or area > area_max:
            continue
        # circularity: area vs bounding-box area (cheap compactness)
        bb = (xs.max() - xs.min() + 1) * (ys.max() - ys.min() + 1)
        if bb > 0 and area / bb < circ_min:
            continue
        out.append(proj(xs.mean(), ys.mean()))
    return out

def polygons_from_blobs(mask, proj, area_min, simplify_m=4.0, max_polys=None):
    """Outer contour of each large blob -> list of GeoJSON Polygon coord rings."""
    lbl, n = ndimage.label(mask)
    sizes = ndimage.sum(mask, lbl, range(1, n + 1))
    order = np.argsort(sizes)[::-1]
    polys = []
    tol = simplify_m / 111320.0
    for k in order:
        if sizes[k] < area_min:
            break
        comp = (lbl == (k + 1))
        cs = find_contours(comp.astype(float), 0.5)
        if not cs:
            continue
        ring = max(cs, key=len)                       # (row,col) pairs
        pts = [proj(c, r) for r, c in ring]
        if len(pts) < 4:
            continue
        poly = Polygon(pts)
        if not poly.is_valid:
            poly = poly.buffer(0)
        poly = poly.simplify(tol)
        if poly.is_empty:
            continue
        for geom in (poly.geoms if poly.geom_type == "MultiPolygon" else [poly]):
            polys.append(mapping(geom))
        if max_polys and len(polys) >= max_polys:
            break
    return polys

def lines_from_mask(mask, proj, min_obj=12, simplify_m=3.0):
    """Skeletonize -> 8-connected segments -> merge -> simplify. For trails/roads."""
    clean = remove_small_objects(mask, min_size=min_obj)
    skel = skeletonize(clean)
    ys, xs = np.where(skel)
    idx = {(int(y), int(x)): k for k, (y, x) in enumerate(zip(ys, xs))}
    segs = []
    for (y, x) in idx:
        for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):     # 4 of 8 to avoid dups
            if (y + dy, x + dx) in idx:
                a1 = proj(x, y); a2 = proj(x + dx, y + dy)
                segs.append(LineString([a1, a2]))
    if not segs:
        return []
    merged = linemerge(unary_union(segs))
    tol = simplify_m / 111320.0
    geoms = merged.geoms if merged.geom_type == "MultiLineString" else [merged]
    out = []
    for g in geoms:
        g = g.simplify(tol)
        if g.length > 0:
            out.append(mapping(g))
    return out

# ---- output ----------------------------------------------------------------
def fc(features, **meta):
    f = {"type": "FeatureCollection"}
    f.update(meta)
    f["features"] = features
    return f

def feat(geom, **props):
    return {"type": "Feature", "properties": props, "geometry": geom}

def write(name, obj):
    d = os.path.join(REPO, "farm-map", "source-data", "derived")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name)
    json.dump(obj, open(p, "w"))
    return os.path.relpath(p, REPO)
