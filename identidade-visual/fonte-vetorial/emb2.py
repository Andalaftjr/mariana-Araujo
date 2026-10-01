"""Direction E, round 2 (E2): a compact collar.

Changes from emb.py: the ID tag hangs from the collar itself, overlapping its lower
edge, so the emblem is nearly round; the flight path can leave the collar and the
plane can sit on the strap or outside it; the pets can be larger.
Roles: ring, dog, cat, route, tag.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *  # noqa
from emb import duo, dashed, plane
from pets import grow

E2 = dict(C=(50.0, 50.0), R_out=44.0, R_in=35.5, gap=2.2, pet_h=1.55, px=-1.0, py=1.0,
          cs=0.76, cdx=38, cdy=34, v=2, eye=True,
          stitch=True, holes=True,
          tag="tucked", tag_r=9.5, tag_dy=2.0, tag_angle=90,
          route=True, plane_mode="strap", plane_at=-48, plane_size=12.5)


def at(C, r, deg):
    return C[0] + r * math.cos(math.radians(deg)), C[1] + r * math.sin(math.radians(deg))


def emblem(**kw):
    g = dict(E2)
    g.update(kw)
    C, Ro, Ri, gap = g["C"], g["R_out"], g["R_in"], g["gap"]
    rm = (Ro + Ri) / 2
    strap = ring(C[0], C[1], Ro, Ri)
    inner = circle(C[0], C[1], Ri - gap)

    pets = duo(g["eye"], cs=g["cs"], cdx=g["cdx"], cdy=g["cdy"], v=g["v"])
    ink = union(*[p for p, _ in pets]).bounds
    s = (Ri * g["pet_h"]) / (ink[3] - ink[1])
    ox = C[0] - (ink[0] + ink[2]) / 2 * s + g["px"]
    oy = C[1] + Ri - ink[3] * s + g["py"]
    pets = [(inter(p.transform(s, 0, 0, s, ox, oy), inner), r) for p, r in pets]

    if g["holes"]:
        strap = diff(strap, union(*[circle(*at(C, rm, a), 1.3) for a in (124, 133, 142)]))
    if g["stitch"]:
        dash = []
        for k in range(150, 390, 7):
            pth = Path()
            pth.moveTo(*at(C, rm, k))
            arc_to(pth, C[0], C[1], rm, k, k + 3.6)
            dash.append(stroke(pth, 0.85, cap="round"))
        strap = diff(strap, union(*dash))

    extra = []
    # the ID tag: hangs from the collar, over its lower edge, with its eyelet
    tc = at(C, Ro + g["tag_dy"], g["tag_angle"])
    disc = circle(tc[0], tc[1], g["tag_r"])
    eye_c = at(tc, g["tag_r"] - 3.1, g["tag_angle"] + 180)
    tag = diff(disc, circle(eye_c[0], eye_c[1], 1.6))
    strap = diff(strap, grow(disc, gap))

    lay = [(strap, "ring")] + extra + pets + [(tag, "tag")]

    if g["route"]:
        pr = Path()
        p0 = (C[0] - 25, C[1] - 11)
        pa = at(C, rm, g["plane_at"])
        pr.moveTo(*p0)
        pr.cubicTo(C[0] - 15, C[1] - 31, C[0] + 2, C[1] - 36, pa[0] - 7, pa[1] + 2)
        rt = inter(dashed(pr), inner)
        if g["plane_mode"] == "strap":
            # the plane flies across the strap: cut from the collar, in the accent colour
            pl = plane(pa[0], pa[1], g["plane_size"], g["plane_at"] + 90 + 8)
        elif g["plane_mode"] == "inside":
            pr = Path()
            pr.moveTo(*p0)
            pr.cubicTo(C[0] - 14, C[1] - 30, C[0] + 4, C[1] - 32, C[0] + 14, C[1] - 25)
            rt = inter(dashed(pr), inner)
            pl = plane(C[0] + 20.5, C[1] - 20.5, 11, 38)
            rt = inter(union(rt, pl), inner)
            pl = None
        elif g["plane_mode"] == "out":
            pa = at(C, Ro + 6, g["plane_at"])
            pl = plane(pa[0], pa[1], g["plane_size"], g["plane_at"] + 90 + 8)
        else:
            pl = None
        if pl is not None:
            lay = [(diff(p, grow(pl, gap)) if r == "ring" else p, r) for p, r in lay]
            rt = union(rt, pl)
        lay = [(diff(p, grow(rt, 1.3)) if r in ("dog", "cat") else p, r) for p, r in lay] + [(rt, "route")]
    return lay


def simple(**kw):
    return emblem(**dict(dict(stitch=False, holes=False, route=False, eye=False, R_in=34.5), **kw))
