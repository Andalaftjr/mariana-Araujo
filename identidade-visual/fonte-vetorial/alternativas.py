"""Round-3 concept studies kept for reference: Janela (cabin window) and Retrato (passport portrait)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *  # noqa


def _grow(p, d):
    return union(p, stroke(p, 2 * d, cap="round", join="round"))


def _rr(x, y, w, h, r):
    return round_poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], r)


def _line(xa, ya, xb, yb):
    p = Path()
    p.moveTo(xa, ya)
    p.lineTo(xb, yb)
    return p


def janela(gap=2.4):
    outer = _rr(21, 5, 58, 90, 29)
    inner = _rr(30, 14, 40, 72, 20)
    frame = diff(outer, inner)
    head = union(circle(50, 70, 13.5),
                 round_poly([(37.5, 66), (39.5, 49), (47.5, 58.5)], [2.6, 2.8, 2.6]),
                 round_poly([(52.5, 58.5), (60.5, 49), (62.5, 66)], [2.6, 2.8, 2.6]),
                 _rr(30, 76, 40, 12, 0))
    head = union(head, round_poly([(30, 90), (30, 82), (38, 78), (62, 78), (70, 82), (70, 90)], [0, 6, 6, 6, 6, 0]))
    head = inter(head, inner)
    skyp = diff(inner, _grow(head, gap))
    return [(frame, "primary"), (head, "primary"), (skyp, "accent")]


def retrato(gap=2.4):
    book = _rr(22, 8, 56, 84, 7)
    photo = _rr(32, 20, 36, 40, 5)
    shape = diff(book, photo)
    pet = union(circle(50, 48, 11.5),
                round_poly([(39, 45), (40.5, 29.5), (47.5, 38)], [2.4, 2.6, 2.4]),
                round_poly([(52.5, 38), (59.5, 29.5), (61, 45)], [2.4, 2.6, 2.4]),
                round_poly([(32, 64), (32, 58), (40, 54), (60, 54), (68, 58), (68, 64)], [0, 5, 5, 5, 5, 0]))
    pet = inter(pet, photo)
    shape = diff(shape, stroke(_line(32, 72, 68, 72), 4.2, cap="round"), stroke(_line(32, 81, 56, 81), 4.2, cap="round"))
    bgp = diff(photo, _grow(pet, gap))
    return [(shape, "primary"), (pet, "primary"), (bgp, "accent")]
