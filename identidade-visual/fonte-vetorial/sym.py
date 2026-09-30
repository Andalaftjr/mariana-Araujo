"""Final symbol construction for the three directions (100 x 100 unit grid).

Each function returns a list of (Path, role) with role in {"primary", "accent"}.
All geometry is built from circles, tangents and straight lines, so it can be
redrawn by hand in any vector tool from the construction notes.
"""
import math
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from geo import *  # noqa


def line(xa, ya, xb, yb):
    p = Path()
    p.moveTo(xa, ya)
    p.lineTo(xb, yb)
    return p


def rrect(x, y, w, h, r):
    return round_poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], r)


# ------------------------------------------------------------------ A: Tag de Embarque
def sym_tag():
    """Luggage-tag silhouette (chamfered top) = travel; eyelet ring = collar ring;
    negative route to a destination point = the planned journey."""
    x0, y0, x1, y1 = 23, 8, 77, 92
    c = 14
    body = round_poly([(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1), (x0, y1), (x0, y0 + c)],
                      [4, 4, 4, 11, 11, 4])
    gap = 2.6
    hc = (50, y0 + 15)
    grom = ring(*hc, 8.6, 4.6)
    body = diff(body, circle(*hc, 8.6 + gap))
    # passport data-page lines (negative), short line = the traveller's line
    l1 = stroke(line(x0 + 12, y1 - 31, x1 - 12, y1 - 31), 6.2)
    l2 = stroke(line(x0 + 12, y1 - 18, x1 - 24, y1 - 18), 6.2)
    body = diff(body, l1, l2)
    return [(body, "primary"), (grom, "accent")]


def sym_tag_small():
    """Reduced version for <= 24 px: silhouette + eyelet only."""
    x0, y0, x1, y1 = 23, 8, 77, 92
    c = 14
    body = round_poly([(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1), (x0, y1), (x0, y0 + c)],
                      [4, 4, 4, 11, 11, 4])
    hc = (50, y0 + 17)
    body = diff(body, circle(*hc, 9))
    return [(body, "primary")]


# ------------------------------------------------------------------ B: Rota da Coleira
def _strap_centerline():
    A = (34, 57, 17, -1)
    B = (66, 43, 17, 1)
    return route([("pt", 8, 74), ("circ",) + A, ("circ",) + B, ("pt", 86, 26)])


def _sample(path, n=24):
    pts = []
    for verb, seg in path.segments:
        if verb == "moveTo":
            pts.append(seg[0])
        elif verb == "lineTo":
            a, b = pts[-1], seg[0]
            pts += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(1, n + 1)]
        elif verb == "curveTo":
            a = pts[-1]
            c1, c2, b = seg
            for i in range(1, n + 1):
                t = i / n
                m = 1 - t
                pts.append((m ** 3 * a[0] + 3 * m * m * t * c1[0] + 3 * m * t * t * c2[0] + t ** 3 * b[0],
                            m ** 3 * a[1] + 3 * m * m * t * c1[1] + 3 * m * t * t * c2[1] + t ** 3 * b[1]))
    return pts


def _at(pts, fracs):
    d = [0]
    for i in range(1, len(pts)):
        d.append(d[-1] + math.dist(pts[i - 1], pts[i]))
    out = []
    for f in fracs:
        target = f * d[-1]
        for i in range(1, len(d)):
            if d[i] >= target:
                t = (target - d[i - 1]) / max(1e-9, d[i] - d[i - 1])
                out.append((pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * t,
                            pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * t))
                break
    return out


def sym_strap(buckle=True, holes=True):
    """A collar strap laid down as a winding road: buckle = departure, the holes
    read as road markings, the rounded tip points to the destination."""
    cl = _strap_centerline()
    bw = 15
    band = stroke(cl, bw, cap="butt")
    pts = _sample(cl)
    end = pts[-1]
    band = union(band, circle(end[0], end[1], bw / 2))
    if holes:
        hs = _at(pts, [0.60, 0.72, 0.84])
        band = diff(band, union(*[circle(x, y, 3.0) for x, y in hs]))
    layers = [(band, "primary")]
    if buckle:
        # buckle frame at the departure end; the strap passes under its right bar
        fx0, fx1 = 5, 17
        fy0, fy1 = 74 - bw / 2 - 5, 74 + bw / 2 + 5
        outer = rrect(fx0, fy0, fx1 - fx0, fy1 - fy0, 3.4)
        inner = rrect(fx0 + 3.8, fy0 + 3.8, fx1 - fx0 - 7.6, fy1 - fy0 - 7.6, 1.2)
        frame = diff(outer, inner)
        bar = rect(fx1 - 3.8, fy0, 3.8, fy1 - fy0)
        band = diff(band, rect(0, 0, fx0 + 3.8 + 2.4, 100), rect(fx1 - 3.8 - 2.4, fy0, 3.8 + 4.8, fy1 - fy0))
        layers = [(band, "primary"), (frame, "accent")]
    return layers


def sym_strap2():
    return sym_strap(buckle=False)


# ------------------------------------------------------------------ C: Elo (&)
AMP = dict(L=(46.5, 27.5, 12.5, 1), B=(38.5, 69.5, 19.5, -1), tail=(84.5, 92), arm=(76.5, 56.5), w=8.4,
           tag_r=7.2, tag_off=(4.4, -4.8), gap=2.5)


def amp_centerline(g=AMP):
    return route([("pt",) + g["tail"], ("circ",) + g["L"], ("circ",) + g["B"], ("pt",) + g["arm"]])


def sym_amp(g=AMP, w=None):
    """A single continuous line: collar loop (top) -> crossings (connections) ->
    identification tag at the end of the route."""
    c = amp_centerline(g)
    s = stroke(c, w or g["w"])
    tc = (g["arm"][0] + g["tag_off"][0], g["arm"][1] + g["tag_off"][1])
    s = diff(s, circle(*tc, g["tag_r"] + g["gap"]))
    return [(s, "primary"), (circle(*tc, g["tag_r"]), "accent")]


SYMBOLS = {"A": sym_tag, "B": sym_strap, "C": sym_amp}


# small-size optimised & (<= 32 px): heavier line, bigger loops and tag, same drawing
AMP_SMALL = dict(L=(46.5, 26.5, 13.5, 1), B=(38.5, 69.0, 20.5, -1), tail=(85.5, 93), arm=(76.0, 56.0), w=11.6,
                 tag_r=8.6, tag_off=(5.4, -5.8), gap=3.2)


def sym_amp_small():
    return sym_amp(AMP_SMALL)
