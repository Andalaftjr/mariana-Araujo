"""Direction E · Companheiros de viagem.

The collar is the frame (stitched strap, holes, D-ring and ID tag), the dog and the
cat look ahead, and the flight path crosses the sky above them.
Roles: ring (collar + D-ring), dog, cat, route, tag, sky (optional fill inside).
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *  # noqa
from amp_r1 import sample
from amp_r2 import arclen_points
from pets import grow, path
from pets3 import cat_layers
from pets4 import dog_layers


def duo(eye=True, gap=2.6, cs=0.8, cdx=30, cdy=20, v=2):
    dl = dog_layers(eye, v=v)
    cl = cat_layers(eye)
    t = lambda p: inter(p.transform(cs, 0, 0, cs, cdx, cdy), rect(0, 0, 200, 100))
    cl = [(t(p), r) for p, r in cl]
    cut = grow(union(*[p for p, _ in cl]), gap)
    return [(diff(p, cut), r) for p, r in dl] + cl


def dashed(pth, dash=2.4, space=2.2, w=1.5):
    pts = sample(pth)
    L = sum(math.dist(pts[i - 1], pts[i]) for i in range(1, len(pts)))
    segs, d = [], 0.0
    while d < L - 1:
        a = arclen_points(pts, [d, min(d + dash, L - 0.01)])
        pl = Path()
        pl.moveTo(*a[0][0])
        pl.lineTo(*a[1][0])
        segs.append(stroke(pl, w, cap="round"))
        d += dash + space
    return union(*segs)


def plane(cx, cy, size, ang_deg):
    """Small top-view plane pointing to ang_deg (0 = right)."""
    s = size / 20.0
    body = path([("M", 10, 0), ("C", 10, -1.3, 8.5, -1.6, 7, -1.6), ("L", -7, -1.2), ("L", -9, -0.8), ("L", -9, 0.8),
                 ("L", -7, 1.2), ("L", 7, 1.6), ("C", 8.5, 1.6, 10, 1.3, 10, 0), ("Z",)])
    wing = path([("M", 2.5, -1.3), ("L", -3, -9.5), ("L", -5.2, -9.5), ("L", -2.2, -1.3), ("Z",)])
    wing2 = wing.transform(1, 0, 0, -1, 0, 0)
    tail = path([("M", -6.2, -1.1), ("L", -9, -4.6), ("L", -10.4, -4.6), ("L", -8.6, -1.0), ("Z",)])
    tail2 = tail.transform(1, 0, 0, -1, 0, 0)
    p = union(body, wing, wing2, tail, tail2)
    a = math.radians(ang_deg)
    ca, sa = math.cos(a) * s, math.sin(a) * s
    return p.transform(ca, sa, -sa, ca, cx, cy)


E = dict(C=(50.0, 48.0), R_out=44.0, R_in=36.0, gap=2.2, pet_h=1.5, tag_r=9.0, ring_r=4.2,
         holes=True, stitch=True, route=True, end="dot", eye=True, sky=False,
         cs=0.76, cdx=38, cdy=34, px=-1.5, v=2)


def emblem(**kw):
    g = dict(E)
    g.update(kw)
    C, R_out, R_in, gap = g["C"], g["R_out"], g["R_in"], g["gap"]
    rm = (R_out + R_in) / 2
    strap = ring(C[0], C[1], R_out, R_in)
    pets = duo(g["eye"], cs=g["cs"], cdx=g["cdx"], cdy=g["cdy"], v=g["v"])
    ink = union(*[p for p, _ in pets]).bounds
    s = (R_in * g["pet_h"]) / (ink[3] - ink[1])
    ox = C[0] - (ink[0] + ink[2]) / 2 * s + g["px"]
    oy = C[1] + R_in - ink[3] * s + 1.0
    inner = circle(C[0], C[1], R_in - gap)
    pets = [(inter(p.transform(s, 0, 0, s, ox, oy), inner), r) for p, r in pets]
    ring_c = (C[0], C[1] + R_out + 1.2)
    dring = ring(ring_c[0], ring_c[1], g["ring_r"], g["ring_r"] * 0.48)
    tag_c = (C[0], ring_c[1] + g["ring_r"] + g["tag_r"] - 1.0)
    tag = circle(*tag_c, g["tag_r"])
    dring = diff(dring, grow(tag, gap * 0.9))
    strap = diff(strap, grow(tag, gap))
    if g["holes"]:
        strap = diff(strap, union(*[circle(C[0] + rm * math.cos(math.radians(a)), C[1] + rm * math.sin(math.radians(a)), 1.3)
                                    for a in (122, 131, 140)]))
    if g["stitch"]:
        dash = []
        for k in range(150, 390, 7):
            pth = Path()
            pth.moveTo(C[0] + rm * math.cos(math.radians(k)), C[1] + rm * math.sin(math.radians(k)))
            arc_to(pth, C[0], C[1], rm, k, k + 3.6)
            dash.append(stroke(pth, 0.85, cap="round"))
        strap = diff(strap, union(*dash))
    lay = [(strap, "ring"), (dring, "ring")] + pets + [(tag, "tag")]
    if g["route"]:
        pr = Path()
        pr.moveTo(C[0] - 24, C[1] - 12)
        pr.cubicTo(C[0] - 14, C[1] - 30, C[0] + 8, C[1] - 32, C[0] + 20, C[1] - 20)
        if g["end"] == "plane":
            pr = Path()
            pr.moveTo(C[0] - 24, C[1] - 12)
            pr.cubicTo(C[0] - 14, C[1] - 30, C[0] + 4, C[1] - 32, C[0] + 14, C[1] - 25)
            rt = union(dashed(pr), plane(C[0] + 20.5, C[1] - 20.5, 11, 38))
        else:
            rt = union(dashed(pr), circle(C[0] + 23, C[1] - 17, 2.4))
        rt = inter(rt, inner)
        lay = [(diff(p, grow(rt, 1.3)) if r in ("dog", "cat") else p, r) for p, r in lay] + [(rt, "route")]
    if g["sky"]:
        lay = [(circle(C[0], C[1], R_in), "sky")] + lay
    return lay


def simple(**kw):
    """For 32-96 px: no stitching, no holes, no route, no eyes; heavier ring."""
    return emblem(**dict(dict(stitch=False, holes=False, route=False, eye=False, R_in=35.0, R_out=44.0), **kw))


def icon(gap=2.4):
    """For <= 32 px and favicons: the pets on a solid disc, no frame details."""
    C, R = (50.0, 50.0), 46.0
    disc = circle(*C, R)
    pets = duo(eye=False, cs=E["cs"], cdx=E["cdx"], cdy=E["cdy"], v=E["v"])
    ink = union(*[p for p, _ in pets]).bounds
    s = (R * 1.5) / (ink[3] - ink[1])
    ox = C[0] - (ink[0] + ink[2]) / 2 * s - 2
    oy = C[1] + R - ink[3] * s
    pets = [(inter(p.transform(s, 0, 0, s, ox, oy), circle(*C, R)), r) for p, r in pets]
    return [(disc, "badge")] + pets
