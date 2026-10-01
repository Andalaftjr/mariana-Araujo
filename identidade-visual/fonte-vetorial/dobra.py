"""Dobra: the origami pet. A passport page folded into a pet's head.

Head = inverted triangle (also a shield); ears = the folded corners of the page.
Dog: ears folded down. Cat: ears up. Rabbit: long ears up. Grid 100 x 100.
Roles: "primary" (head), "facet" (lighter fold of the head, colour version only),
"accent" (ears).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *  # noqa


def _grow(p, d):
    return union(p, stroke(p, 2 * d, cap="round", join="round"))


def _p(pts, r):
    return round_poly(pts, r)


G = dict(W=66.0, H=62.0, top=26.0, rc=2.4, chin=5.4, gap=2.5,
         ear_w=0.29, ear_len=40.0, ear_out=5.0,           # dog
         cat_h=26.0, cat_w=0.30, cat_lean=2.0,           # cat
         rab_h=44.0, rab_w=0.24, rab_lean=4.0)           # rabbit


def head(g=G):
    x0, x1, y0 = 50 - g["W"] / 2, 50 + g["W"] / 2, g["top"]
    y1 = y0 + g["H"]
    return (x0, x1, y0, y1), _p([(x0, y0), (x1, y0), (50, y1)], [g["rc"], g["rc"], g["chin"]])


def ears(kind, g=G):
    (x0, x1, y0, y1), _ = head(g)
    W, rc = g["W"], g["rc"]
    if kind == "dog":
        ew, L, o = W * g["ear_w"], g["ear_len"], g["ear_out"]
        el = _p([(x0, y0), (x0 + ew, y0), (x0 - o + ew * 0.25, y0 + L), (x0 - o, y0 + L * 0.8)], [rc, rc, rc * 2.2, rc * 1.6])
        er = _p([(x1 - ew, y0), (x1, y0), (x1 + o, y0 + L * 0.8), (x1 + o - ew * 0.25, y0 + L)], [rc, rc, rc * 1.6, rc * 2.2])
    else:
        h, ew, lean = (g["cat_h"], W * g["cat_w"], g["cat_lean"]) if kind == "cat" else (g["rab_h"], W * g["rab_w"], g["rab_lean"])
        el = _p([(x0, y0), (x0 + ew, y0), (x0 + lean, y0 - h)], [rc, rc, rc * 1.4])
        er = _p([(x1 - ew, y0), (x1, y0), (x1 - lean, y0 - h)], [rc, rc, rc * 1.4])
    return union(el, er)


def pet(kind="dog", facet=True, g=G):
    (x0, x1, y0, y1), hd = head(g)
    e = ears(kind, g)
    hd = diff(hd, _grow(e, g["gap"]))
    lay = [(hd, "primary")]
    if facet:
        # the right half of the face catches the light: same drawing, lighter tone
        right = inter(hd, _p([(50, y0 - 10), (x1 + 20, y0 - 10), (x1 + 20, y1 + 10), (50, y1 + 10)], 0))
        lay = [(diff(hd, right), "primary"), (right, "facet")]
    lay.append((e, "accent"))
    return lay
