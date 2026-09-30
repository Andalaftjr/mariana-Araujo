"""R1 of the brand ampersand: bolder, interlaced (over/under) like a knot, with
parametric terminals and tag shapes. Grid 100 x 100."""
import math
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from geo import *  # noqa


def sample(path, n=60):
    """Flatten a path to (points, cumulative length)."""
    pts = []
    for verb, seg in path.segments:
        if verb == "moveTo":
            pts.append(seg[0])
        elif verb == "lineTo":
            a, b = pts[-1], seg[0]
            L = math.dist(a, b)
            k = max(2, int(L / 0.4))
            pts += [(a[0] + (b[0] - a[0]) * i / k, a[1] + (b[1] - a[1]) * i / k) for i in range(1, k + 1)]
        elif verb == "curveTo":
            a = pts[-1]
            c1, c2, b = seg
            for i in range(1, n + 1):
                t = i / n
                m = 1 - t
                pts.append((m ** 3 * a[0] + 3 * m * m * t * c1[0] + 3 * m * t * t * c2[0] + t ** 3 * b[0],
                            m ** 3 * a[1] + 3 * m * m * t * c1[1] + 3 * m * t * t * c2[1] + t ** 3 * b[1]))
    return pts


def crossings(pts):
    res = []
    for i in range(len(pts) - 1):
        for j in range(i + 3, len(pts) - 1):
            p1, p2, p3, p4 = pts[i], pts[i + 1], pts[j], pts[j + 1]
            d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
            if abs(d) < 1e-12:
                continue
            t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
            u = ((p3[0] - p1[0]) * (p2[1] - p1[1]) - (p3[1] - p1[1]) * (p2[0] - p1[0])) / d
            if 0 <= t <= 1 and 0 <= u <= 1:
                res.append(((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])), i, j))
    return res


def polyline(pts):
    p = Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    return p


G_R1 = dict(
    L=(47.0, 26.0, 14.0, 1),      # collar loop
    B=(38.0, 67.5, 21.0, -1),     # bowl
    tail=(86.0, 96.0),            # start of the line (extends below baseline, then trimmed)
    arm=(75.0, 55.0),             # end of the arm
    w=12.0,                       # stroke
    gap=3.2,                      # interlace / tag gap
    baseline=88.5,                # flat foot
    tag="disc", tag_r=8.4, tag_off=(6.0, -6.4),
    over=("diag", "desc"),        # which strand passes over at crossing (lower, upper)
    slant=0.0,
)


def build(g=None, **kw):
    g = dict(G_R1 if g is None else g)
    g.update(kw)
    w, gap = g["w"], g["gap"]
    cl = route([("pt",) + g["tail"], ("circ",) + g["L"], ("circ",) + g["B"], ("pt",) + g["arm"]])
    full = stroke(cl, w, cap="round")
    pts = sample(cl)
    xs = crossings(pts)
    # xs: list of (point, i, j) with i on the earlier strand (diagonal from the tail)
    xs.sort(key=lambda c: c[1])  # first encountered along the path first = lower crossing
    out = full
    if g.get("interlace", True):
        for k, (c, i, j) in enumerate(xs):
            which = g["over"][k]
            idx = i if which == "diag" else j
            # local over-strand polyline around the crossing
            R = w * 2.4
            lo = idx
            while lo > 0 and math.dist(pts[lo], c) < R:
                lo -= 1
            hi = idx
            while hi < len(pts) - 1 and math.dist(pts[hi], c) < R:
                hi += 1
            pl = polyline(pts[lo:hi + 1])
            over = stroke(pl, w, cap="butt")
            cut = stroke(pl, w + 2 * gap, cap="butt")
            win = circle(c[0], c[1], w * 1.9)
            out = union(diff(out, inter(cut, win)), inter(over, circle(c[0], c[1], w * 2.2)))
    # flat foot: trim everything below the baseline
    if g.get("baseline"):
        base = g["B"][1] + g["B"][2] + w / 2 if g["baseline"] == "auto" else g["baseline"]
        out = inter(out, rect(-50, -50, 200, 50 + base))
    # tag
    tcx, tcy = g["arm"][0] + g["tag_off"][0], g["arm"][1] + g["tag_off"][1]
    tr = g["tag_r"]
    kind = g["tag"]
    if kind == "disc":
        tag = circle(tcx, tcy, tr)
        halo = circle(tcx, tcy, tr + gap)
    elif kind == "eyelet":
        tag = diff(circle(tcx, tcy, tr), circle(tcx - tr * 0.28, tcy - tr * 0.28, tr * 0.24))
        halo = circle(tcx, tcy, tr + gap)
    elif kind == "passport":
        ww, hh = tr * 1.55, tr * 2.05
        t = round_poly([(tcx - ww / 2, tcy - hh / 2), (tcx + ww / 2, tcy - hh / 2), (tcx + ww / 2, tcy + hh / 2),
                        (tcx - ww / 2, tcy + hh / 2)], tr * 0.42)
        tag = rotate(t, g.get("tag_rot", 38), tcx, tcy)
        halo = pathops.simplify(_grow(tag, gap))
    elif kind == "none":
        tag, halo = None, None
    if halo is not None:
        out = diff(out, halo)
    layers = [(out, "primary")]
    if tag is not None:
        layers.append((tag, "accent"))
    if g.get("slant"):
        sh = math.tan(math.radians(g["slant"]))
        layers = [(p.transform(1, 0, -sh, 1, sh * g.get("baseline", 88), 0), r) for p, r in layers]
    return layers


def _grow(p, d):
    return union(p, stroke(p, 2 * d, cap="round", join="round"))


import pathops  # noqa: E402


R1 = dict(G_R1, over=("arm", "diag"), baseline="auto", w=11.2, gap=3.0)
R1_SMALL = dict(R1, interlace=False, L=(47.0, 25.0, 15.0, 1), B=(37.5, 67.0, 22.0, -1), w=12.6, gap=3.6,
                tag_r=9.4, tag_off=(6.8, -7.2))


def symbol(small=False):
    return build(R1_SMALL if small else R1)


def scaled(x, baseline, height, stroke_w, g=None, gap_ratio=0.3, min_gap=None, interlace=True):
    """The R1 & scaled to an outer height, with its line re-drawn at stroke_w
    (so it can sit next to text of any weight). Bottom of the ink on baseline."""
    g = dict(R1 if g is None else g)
    s = 1.0
    for _ in range(3):
        wg = stroke_w / s
        gap = max(wg * gap_ratio, (min_gap / s) if min_gap else 0)
        lay = build(g, w=wg, gap=gap, interlace=interlace)
        ink = union(*[p for p, _ in lay]).bounds
        s = height / (ink[3] - ink[1])
    out = [(p.transform(s, 0, 0, s, x - ink[0] * s, baseline - ink[3] * s), r) for p, r in lay]
    return out, (ink[2] - ink[0]) * s
