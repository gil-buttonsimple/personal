"""Registration and line-tracing machinery for the farm-map sheets.

Two capabilities the first pass lacked.

1. Thin-plate-spline registration. Each sheet's 4-point projective fit is exact at
   the four boundary apexes and drifts through the interior, because a homography
   cannot bend and the sheets are folded paper photographed at an angle. Here the
   known 43-course traverse is snapped onto the boundary line as it actually appears
   in the photo (ICP), giving hundreds of correspondences spread around the whole
   perimeter, and a TPS is fitted through them. The TPS bends.

2. Skeleton graph tracing. `linemerge` on a bag of one-pixel segments explodes a
   drawn network into thousands of fragments: it only joins runs whose endpoints
   meet pairwise, so every junction and every pen-lift severs the line. Here the
   skeleton is walked as a graph -- junction to junction -- and small gaps are
   bridged before the walk, which turns the same pixels into a connected network.
"""
import os, json
import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree
from skimage.morphology import skeletonize, remove_small_objects
from shapely.geometry import LineString, mapping

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = os.path.join(REPO, "farm-map", "source-art")
TX = os.path.join(REPO, "farm-map", "source-data", "transforms")

MLAT = 111320.0


def mlon(lat):
    return 111320.0 * np.cos(np.radians(lat))


# ---- thin-plate spline ------------------------------------------------------
def _U(r2):
    # r^2 log r, written on r^2 to avoid a sqrt; 0 at r=0.
    out = np.zeros_like(r2)
    nz = r2 > 1e-12
    out[nz] = 0.5 * r2[nz] * np.log(r2[nz])
    return out


def tps_fit(src, dst, smooth=0.0):
    """Fit a TPS mapping src (N,2) -> dst (N,2). Returns a parameter dict.

    `smooth` is a regularizer (in src units squared) that lets the surface pass
    near, rather than exactly through, noisy correspondences -- which ICP snaps
    always are.
    """
    src = np.asarray(src, float)
    dst = np.asarray(dst, float)
    n = len(src)
    d2 = ((src[:, None, :] - src[None, :, :]) ** 2).sum(-1)
    K = _U(d2)
    if smooth:
        K = K + smooth * np.eye(n)
    P = np.hstack([np.ones((n, 1)), src])
    L = np.zeros((n + 3, n + 3))
    L[:n, :n] = K
    L[:n, n:] = P
    L[n:, :n] = P.T
    Y = np.zeros((n + 3, 2))
    Y[:n] = dst
    W = np.linalg.lstsq(L, Y, rcond=None)[0]
    return {"src": src, "w": W[:n], "a": W[n:]}


def tps_apply(tps, pts):
    pts = np.atleast_2d(np.asarray(pts, float))
    src = tps["src"]
    d2 = ((pts[:, None, :] - src[None, :, :]) ** 2).sum(-1)
    U = _U(d2)
    aff = np.hstack([np.ones((len(pts), 1)), pts]) @ tps["a"]
    return aff + U @ tps["w"]


def tps_to_json(tps):
    return {"src": tps["src"].tolist(), "w": tps["w"].tolist(), "a": tps["a"].tolist()}


def tps_from_json(d):
    return {"src": np.asarray(d["src"], float),
            "w": np.asarray(d["w"], float),
            "a": np.asarray(d["a"], float)}


# ---- projective (for initialization + comparison) ---------------------------
def h_apply(H, pts):
    pts = np.atleast_2d(np.asarray(pts, float))
    w = H[2, 0] * pts[:, 0] + H[2, 1] * pts[:, 1] + H[2, 2]
    x = (H[0, 0] * pts[:, 0] + H[0, 1] * pts[:, 1] + H[0, 2]) / w
    y = (H[1, 0] * pts[:, 0] + H[1, 1] * pts[:, 1] + H[1, 2]) / w
    return np.column_stack([x, y])


def h_fit(src, dst):
    """Normalized DLT homography src->dst."""
    def norm(p):
        c = p.mean(0)
        s = np.sqrt(2) / (np.linalg.norm(p - c, axis=1).mean() + 1e-12)
        T = np.array([[s, 0, -s * c[0]], [0, s, -s * c[1]], [0, 0, 1.0]])
        q = (T @ np.vstack([p.T, np.ones(len(p))])).T
        return q[:, :2], T

    src = np.asarray(src, float)
    dst = np.asarray(dst, float)
    sn, Ts = norm(src)
    dn, Td = norm(dst)
    A = []
    for (x, y), (u, v) in zip(sn, dn):
        A.append([-x, -y, -1, 0, 0, 0, u * x, u * y, u])
        A.append([0, 0, 0, -x, -y, -1, v * x, v * y, v])
    _, _, Vt = np.linalg.svd(np.array(A))
    H = Vt[-1].reshape(3, 3)
    return np.linalg.inv(Td) @ H @ Ts


# ---- world<->local metres ---------------------------------------------------
def world_to_m(lonlat, lat0):
    lonlat = np.atleast_2d(np.asarray(lonlat, float))
    return np.column_stack([lonlat[:, 0] * mlon(lat0), lonlat[:, 1] * MLAT])


def m_to_world(xy, lat0):
    xy = np.atleast_2d(np.asarray(xy, float))
    return np.column_stack([xy[:, 0] / mlon(lat0), xy[:, 1] / MLAT])


# ---- densify a polygon ------------------------------------------------------
def densify(ring, step_m, lat0):
    """Resample a closed lon/lat ring at ~step_m spacing."""
    pts = np.asarray(ring, float)
    xy = world_to_m(pts, lat0)
    out = []
    for i in range(len(xy)):
        a, b = xy[i], xy[(i + 1) % len(xy)]
        seg = np.linalg.norm(b - a)
        n = max(1, int(seg / step_m))
        for k in range(n):
            out.append(a + (b - a) * (k / n))
    return m_to_world(np.array(out), lat0)


# ---- ICP snap ---------------------------------------------------------------
def icp_snap(mask, model_px, radius_px):
    """For each model point, the nearest True pixel of `mask` within radius.

    Returns (model_kept, snapped). Uses a KD-tree over mask pixels -- the mask is
    a thin line, so this is a few hundred thousand points at most.
    """
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return np.empty((0, 2)), np.empty((0, 2))
    tree = cKDTree(np.column_stack([xs, ys]))
    d, i = tree.query(model_px, distance_upper_bound=radius_px)
    ok = np.isfinite(d)
    return model_px[ok], np.column_stack([xs[i[ok]], ys[i[ok]]])


# ---- skeleton graph tracing -------------------------------------------------
_N8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def bridge_gaps(mask, max_gap_px):
    """Close pen-lifts and scanner dropouts without fattening junctions.

    A dilate-then-skeletonize round trip reconnects anything separated by less
    than ~2*max_gap and leaves the centreline where it was.
    """
    if max_gap_px <= 0:
        return mask
    d = ndimage.binary_dilation(mask, iterations=max_gap_px)
    d = ndimage.binary_closing(d, iterations=1)
    return ndimage.binary_erosion(d, iterations=max_gap_px, border_value=1) | mask


def trace_skeleton(mask, min_branch_px=25):
    """Walk a skeleton as a graph. Returns a list of pixel polylines [(col,row)...].

    Nodes are endpoints (1 neighbour) and junctions (>=3). Each edge between two
    nodes becomes one polyline. Isolated loops (no node at all) are emitted whole.
    """
    skel = skeletonize(mask)
    pts = set(zip(*np.where(skel)))  # (row, col)

    def nbrs(p):
        r, c = p
        return [(r + dr, c + dc) for dr, dc in _N8 if (r + dr, c + dc) in pts]

    deg = {p: len(nbrs(p)) for p in pts}
    nodes = {p for p in pts if deg[p] != 2}

    lines = []
    seen_edges = set()

    for n in nodes:
        for start in nbrs(n):
            if (n, start) in seen_edges:
                continue
            path = [n, start]
            seen_edges.add((n, start))
            seen_edges.add((start, n))
            cur, prev = start, n
            while deg.get(cur, 0) == 2:
                nxt = [q for q in nbrs(cur) if q != prev]
                if not nxt:
                    break
                prev, cur = cur, nxt[0]
                seen_edges.add((prev, cur))
                seen_edges.add((cur, prev))
                path.append(cur)
            if len(path) >= 2:
                lines.append(path)

    # pure loops: components with no node
    remaining = pts - {p for ln in lines for p in ln}
    while remaining:
        seed = next(iter(remaining))
        comp = [seed]
        remaining.discard(seed)
        cur, prev = seed, None
        while True:
            nxt = [q for q in nbrs(cur) if q != prev and q in remaining]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            remaining.discard(cur)
            comp.append(cur)
        if len(comp) >= min_branch_px:
            comp.append(comp[0])
            lines.append(comp)

    # drop hairs: short branches that dead-end (spurs off a thick stroke)
    out = []
    for ln in lines:
        endpoints_free = deg.get(ln[0], 0) == 1 or deg.get(ln[-1], 0) == 1
        if endpoints_free and len(ln) < min_branch_px:
            continue
        out.append([(c, r) for (r, c) in ln])  # to (col,row)
    return out


def project_lines(px_lines, proj, simplify_m=3.0, min_len_m=15.0, lat0=34.66):
    """Project pixel polylines to lon/lat, simplify, drop stubs. -> shapely LineStrings."""
    tol = simplify_m / MLAT
    out = []
    for ln in px_lines:
        w = proj(np.array(ln, float))
        g = LineString(w)
        if len(w) < 2:
            continue
        g = g.simplify(tol)
        # geographic length in metres
        c = np.array(g.coords)
        seg = np.hypot(np.diff(c[:, 0]) * mlon(lat0), np.diff(c[:, 1]) * MLAT)
        if seg.sum() < min_len_m:
            continue
        out.append(g)
    return out


def line_len_m(g, lat0=34.66):
    c = np.array(g.coords)
    return float(np.hypot(np.diff(c[:, 0]) * mlon(lat0), np.diff(c[:, 1]) * MLAT).sum())
