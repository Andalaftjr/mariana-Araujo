"""R2: the & drawn as a real pet collar.

The line is a collar strap: the tail is the strap tip with holes, the top loop is
closed by a buckle, and the arm ends in a D-ring with the ID tag hanging from it.
Interlace (over/under) from r1 is kept. Grid 100 x 100 (normalised on export).
"""
import math
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import pathops  # noqa: E402
from geo import *  # noqa
from amp_r1 import crossings, polyline, sample


def _grow(p, d):
    return union(p, stroke(p, 2 * d, cap="round", join="round"))


def local_rect(cx, cy, ang, x0, y0, x1, y1, r):
    """Rounded rect given in a local frame (x along ang, y across), placed at (cx, cy)."""
    p = round_poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], r)
    ca, sa = math.cos(ang), math.sin(ang)
    return p.transform(ca, sa, -sa, ca, cx, cy)


def arclen_points(pts, dists):
    d = [0.0]
    for i in range(1, len(pts)):
        d.append(d[-1] + math.dist(pts[i - 1], pts[i]))
    out = []
    for t in dists:
        for i in range(1, len(d)):
            if d[i] >= t:
                f = (t - d[i - 1]) / max(1e-9, d[i] - d[i - 1])
                p = (pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f)
                tan = (pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
                out.append((p, math.atan2(tan[1], tan[0])))
                break
    return out


G_R2 = dict(
    L=(46.5, 25.0, 15.5, 1),
    B=(37.5, 68.0, 21.0, -1),
    tail=(84.0, 91.0),
    arm=(74.5, 55.5),
    w=12.0,
    gap=2.8,
    over=("arm", "diag"),
    interlace=True,
    holes=3, hole_r=2.1, hole_start=6.0, hole_step=6.4,
    buckle=True, buckle_ang=208.0, buckle_s=None, buckle_len=7.5, buckle_over=3.4, buckle_bar=2.3, prong=False,
    ring_r=4.7, ring_t=2.5, tag_r=8.2, swing=28.0, tag="disc", tag_on="arm", ring_ang=-12.0,
)


def build(g=None, **kw):
    g = dict(G_R2 if g is None else g)
    g.update({k: tuple(v) if isinstance(v, list) else v for k, v in kw.items()})
    w, gap = g["w"], g["gap"]
    cl = route([("pt",) + g["tail"], ("circ",) + g["L"], ("circ",) + g["B"], ("pt",) + g["arm"]])
    strap = stroke(cl, w, cap="round")
    pts = sample(cl)
    # ---- interlace
    if g["interlace"]:
        xs = sorted(crossings(pts), key=lambda c: c[1])
        for k, (c, i, j) in enumerate(xs):
            idx = i if g["over"][k] == "diag" else j
            R = w * 2.4
            lo, hi = idx, idx
            while lo > 0 and math.dist(pts[lo], c) < R:
                lo -= 1
            while hi < len(pts) - 1 and math.dist(pts[hi], c) < R:
                hi += 1
            pl = polyline(pts[lo:hi + 1])
            over = stroke(pl, w, cap="butt")
            cut = stroke(pl, w + 2 * gap, cap="butt")
            strap = union(diff(strap, inter(cut, circle(c[0], c[1], w * 1.9))), inter(over, circle(c[0], c[1], w * 2.2)))
    # ---- holes near the strap tip (tail)
    if g["holes"]:
        hs = arclen_points(pts, [g["hole_start"] + i * g["hole_step"] for i in range(g["holes"])])
        strap = diff(strap, union(*[circle(p[0], p[1], g["hole_r"]) for p, _ in hs]))
    extra = []
    # ---- buckle (frame across the strap; the strap runs through it)
    if g["buckle"]:
        if g.get("buckle_s") is not None:
            (px, py), tang = arclen_points(pts, [g["buckle_s"]])[0]
        else:
            cx, cy, R_, s = g["L"]
            a = math.radians(g["buckle_ang"])
            px, py = cx + R_ * math.cos(a), cy + R_ * math.sin(a)
            tang = a + math.pi / 2
        hl = g["buckle_len"] / 2
        hn = w / 2 + g["buckle_over"]
        t = g["buckle_bar"]
        gin = g.get("buckle_gap_in", 1.3)
        outer = local_rect(px, py, tang, -hl, -hn, hl, hn, min(2.8, hl * 0.5))
        inner = local_rect(px, py, tang, -hl + t, -hn + t, hl - t, hn - t, 0.9)
        frame = diff(outer, inner)
        parts = frame
        # strap stops at a thin gap outside the frame and shows again inside the opening
        inside = inter(strap, local_rect(px, py, tang, -hl + t + gin, -hn + t + gin, hl - t - gin, hn - t - gin, 0.6))
        strap = union(diff(strap, _grow(outer, gap * 0.8)), inside)
        extra.append(parts)
    body = union(strap, *extra) if extra else strap
    # ---- D-ring + hanging tag (on the collar loop, or at the end of the arm)
    layers = []
    rr, rt = g["ring_r"], g["ring_t"]
    if g.get("tag_on", "arm") == "loop":
        cx, cy, R_, _s = g["L"]
        a = math.radians(g["ring_ang"])
        dd = R_ + w / 2 + rr - rt * 0.9
        rc = (cx + dd * math.cos(a), cy + dd * math.sin(a))
    else:
        end = pts[-1]
        prev = pts[-8]
        u = (end[0] - prev[0], end[1] - prev[1])
        L_ = math.hypot(*u)
        u = (u[0] / L_, u[1] / L_)
        rc = (end[0] + u[0] * (w / 2 + rr - rt * 0.35), end[1] + u[1] * (w / 2 + rr - rt * 0.35))
    ring_p = ring(rc[0], rc[1], rr, rr - rt)
    sw = math.radians(g["swing"])
    tr = g["tag_r"]
    dist = rr - rt * 0.5 + tr * 0.72
    tc = (rc[0] + math.sin(sw) * dist, rc[1] + math.cos(sw) * dist)
    tag = circle(tc[0], tc[1], tr)
    # the ring passes through the tag: ring over the tag top, gap around it
    tag = diff(tag, _grow(inter(ring_p, circle(tc[0], tc[1], tr + 3)), gap * 0.7))
    body = diff(body, _grow(tag, gap), circle(tc[0], tc[1], tr + gap))
    body = union(body, ring_p)
    layers.append((body, "primary"))
    layers.append((tag, "accent"))
    return layers


R2 = dict(G_R2, L=(46.5, 24.0, 17.0, 1), tail=(86.5, 94.5), tag_on="loop", swing=12.0, tag_r=9.0, ring_ang=-14.0,
          buckle_len=12.0, buckle_over=3.4, buckle_bar=2.4, buckle_ang=196.0)
# reduced (<= 32 px / small embroidery): collar loop + ring + tag only
R2_SMALL = dict(R2, interlace=False, holes=0, buckle=False, w=13.0, gap=3.2, tag_r=10.0, ring_r=4.6, ring_t=4.6,
                ring_ang=-16.0)
# text size (inside the wordmark): keeps holes, buckle and tag; no interlace gaps
R2_TEXT = dict(R2, interlace=False)


def symbol(small=False):
    return build(R2_SMALL if small else R2)


def scaled(x, baseline, height, stroke_w, g=None, gap_ratio=0.28):
    """R2 & scaled to an outer height with its strap re-drawn at stroke_w; ink bottom on baseline.
    Hardware (buckle, ring, holes, tag) scales with the strap width."""
    g = dict(R2_TEXT if g is None else g)
    s = 1.0
    for _ in range(3):
        k = (stroke_w / s) / g["w"]
        gg = dict(g, w=g["w"] * k, gap=max(g["gap"] * k, g["w"] * k * gap_ratio),
                  hole_r=g["hole_r"] * k, buckle_over=g["buckle_over"] * k, buckle_bar=g["buckle_bar"] * k,
                  ring_r=g["ring_r"] * k, ring_t=g["ring_t"] * k)
        lay = build(gg)
        ink = union(*[p for p, _ in lay]).bounds
        s = height / (ink[3] - ink[1])
    out = [(p.transform(s, 0, 0, s, x - ink[0] * s, baseline - ink[3] * s), r) for p, r in lay]
    return out, (ink[2] - ink[0]) * s
