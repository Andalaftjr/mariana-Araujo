"""Wordmark construction: exact text "Coleira & Passaporte" converted to outlines."""
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from geo import *  # noqa
from sym import AMP, amp_centerline

import os

# Pasta com os pacotes @fontsource (npm pack @fontsource/outfit, etc.), um subdiretório por família.
F = os.environ.get("FONTS_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")) + "/"
_cache = {}


def font(name, weight, style="normal"):
    key = (name, weight, style)
    if key not in _cache:
        _cache[key] = Font(f"{F}{name}/package/files/{name}-latin-{weight}-{style}.woff")
    return _cache[key]


def stem(fnt):
    """Vertical stem thickness in em units: width of 'l' sliced at half x-height."""
    p, _ = fnt.text("l", 1000)
    y = -fnt.xh / fnt.upem * 1000 / 2
    sl = inter(p, rect(-1000, y - 1, 3000, 2))
    b = sl.bounds
    return (b[2] - b[0]) / 1000.0


def stem_bounds(fnt):
    """r0 measure (bounds of 'l'); kept so the r0 files regenerate identically."""
    p, _ = fnt.text("l", 1000)
    b = p.bounds
    return (b[2] - b[0]) / 1000.0


NAME_L, NAME_R = "Coleira", "Passaporte"
FULL_NAME = "Coleira & Passaporte"


def custom_amp(x, baseline, height, stroke_w, g=AMP):
    """Brand ampersand scaled so its outer height == height, sitting on baseline."""
    # outer bounds of the centreline + half stroke, in grid units
    cl = amp_centerline(g)
    b = cl.bounds
    top = b[1] - g["w"] / 2
    bot = b[3] + g["w"] / 2
    left = b[0] - g["w"] / 2
    s = height / (bot - top)
    cl2 = cl.transform(s, 0, 0, s, x - left * s, baseline - bot * s)
    line_ = stroke(cl2, stroke_w)
    tc = (g["arm"][0] + g["tag_off"][0], g["arm"][1] + g["tag_off"][1])
    tcx, tcy = x + (tc[0] - left) * s, baseline + (tc[1] - bot) * s
    tr = g["tag_r"] * s
    gap = max(g["gap"] * s, stroke_w * 0.32)
    line_ = diff(line_, circle(tcx, tcy, tr + gap))
    tag = circle(tcx, tcy, tr)
    right = max(line_.bounds[2], tcx + tr)
    return line_, tag, right - x


def wordmark(fnt, size, amp="custom", tracking=0.0, amp_scale=1.0, space_scale=1.0):
    """Return dict(text=Path, amp=Path|None, tag=Path|None, width, cap, baseline=0)."""
    cap = fnt.cap / fnt.upem * size
    sp = fnt.width(" ", size) * space_scale
    if amp != "custom":
        p, w = fnt.text(FULL_NAME, size, 0, 0, tracking)
        return dict(text=p, amp=None, tag=None, width=w, cap=cap)
    pl, wl = fnt.text(NAME_L, size, 0, 0, tracking)
    st = stem_bounds(fnt) * size * 0.92
    a_line, a_tag, aw = custom_amp(wl + sp, 0, cap * amp_scale, st)
    xr = wl + sp + aw + sp
    pr, wr = fnt.text(NAME_R, size, xr, 0, tracking)
    return dict(text=union(pl, pr), amp=a_line, tag=a_tag, width=xr + wr, cap=cap)
