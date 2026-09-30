"""Geometry + type helpers for building clean, fill-only vector logos.

Every shape ends up as a pathops.Path (outlines only, no strokes), so the
exported SVG/PDF is embroidery/cut/print safe and has no font dependency.
"""
import io
import math

import pathops
import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from pathops import LineCap, LineJoin, Path, PathOp

K = 0.5522847498307936


# ---------------------------------------------------------------- primitives
def circle(cx, cy, r):
    p = Path()
    p.moveTo(cx + r, cy)
    p.cubicTo(cx + r, cy + K * r, cx + K * r, cy + r, cx, cy + r)
    p.cubicTo(cx - K * r, cy + r, cx - r, cy + K * r, cx - r, cy)
    p.cubicTo(cx - r, cy - K * r, cx - K * r, cy - r, cx, cy - r)
    p.cubicTo(cx + K * r, cy - r, cx + r, cy - K * r, cx + r, cy)
    p.close()
    return p


def ring(cx, cy, r_out, r_in):
    return diff(circle(cx, cy, r_out), circle(cx, cy, r_in))


def rect(x, y, w, h):
    p = Path()
    p.moveTo(x, y)
    p.lineTo(x + w, y)
    p.lineTo(x + w, y + h)
    p.lineTo(x, y + h)
    p.close()
    return p


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def arc_to(p, cx, cy, r, a0, a1):
    """Append circular arc (SVG angle convention, y down) from a0 to a1 degrees."""
    n = max(1, int(math.ceil(abs(a1 - a0) / 45.0)))
    step = (a1 - a0) / n
    for i in range(n):
        s = math.radians(a0 + i * step)
        e = math.radians(a0 + (i + 1) * step)
        k = 4.0 / 3.0 * math.tan((e - s) / 4.0)
        x0, y0 = cx + r * math.cos(s), cy + r * math.sin(s)
        x3, y3 = cx + r * math.cos(e), cy + r * math.sin(e)
        x1, y1 = x0 - k * r * math.sin(s), y0 + k * r * math.cos(s)
        x2, y2 = x3 + k * r * math.sin(e), y3 - k * r * math.cos(e)
        p.cubicTo(x1, y1, x2, y2, x3, y3)


def round_poly(points, radius):
    """Closed polygon with every corner rounded (radius may be a list)."""
    n = len(points)
    radii = radius if isinstance(radius, (list, tuple)) else [radius] * n
    p = Path()
    first = True
    for i in range(n):
        x0, y0 = points[i - 1]
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        r = radii[i]
        v1 = (x0 - x1, y0 - y1)
        v2 = (x2 - x1, y2 - y1)
        l1 = math.hypot(*v1)
        l2 = math.hypot(*v2)
        u1 = (v1[0] / l1, v1[1] / l1)
        u2 = (v2[0] / l2, v2[1] / l2)
        cosang = max(-1, min(1, u1[0] * u2[0] + u1[1] * u2[1]))
        ang = math.acos(cosang)
        if r <= 0 or ang < 1e-6:
            if first:
                p.moveTo(x1, y1)
                first = False
            else:
                p.lineTo(x1, y1)
            continue
        d = r / math.tan(ang / 2)
        d = min(d, l1 / 2, l2 / 2)
        r_eff = d * math.tan(ang / 2)
        a = (x1 + u1[0] * d, y1 + u1[1] * d)
        b = (x1 + u2[0] * d, y1 + u2[1] * d)
        # cubic approximation of the arc between a and b
        theta = math.pi - ang
        k = 4.0 / 3.0 * math.tan(theta / 4.0) * r_eff
        c1 = (a[0] - u1[0] * k, a[1] - u1[1] * k)
        c2 = (b[0] - u2[0] * k, b[1] - u2[1] * k)
        if first:
            p.moveTo(*a)
            first = False
        else:
            p.lineTo(*a)
        p.cubicTo(c1[0], c1[1], c2[0], c2[1], b[0], b[1])
    p.close()
    return p


def union(*paths):
    out = Path()
    for q in paths:
        out = pathops.op(out, q, PathOp.UNION) if list(out.segments) else _copy(q)
    return out


def diff(a, *bs):
    out = a
    for b in bs:
        out = pathops.op(out, b, PathOp.DIFFERENCE)
    return out


def inter(a, b):
    return pathops.op(a, b, PathOp.INTERSECTION)


def _copy(q):
    c = Path()
    q.draw(c.getPen())
    return c


def stroke(path, w, cap="round", join="round"):
    q = _copy(path)
    caps = {"round": LineCap.ROUND_CAP, "butt": LineCap.BUTT_CAP, "square": LineCap.SQUARE_CAP}
    joins = {"round": LineJoin.ROUND_JOIN, "miter": LineJoin.MITER_JOIN, "bevel": LineJoin.BEVEL_JOIN}
    q.stroke(w, caps[cap], joins[join], 4)
    q.convertConicsToQuads(0.01)
    return pathops.simplify(q)


def tf(path, a=1, b=0, c=0, d=1, e=0, f=0):
    return path.transform(a, b, c, d, e, f)


def rotate(path, deg, cx, cy):
    t = math.radians(deg)
    ca, sa = math.cos(t), math.sin(t)
    # translate(-c) -> rotate -> translate(c)
    return path.transform(ca, sa, -sa, ca, cx - ca * cx + sa * cy, cy - sa * cx - ca * cy)


def bounds(path):
    return path.bounds  # (xmin, ymin, xmax, ymax)


def to_d(path, prec=2):
    pen = SVGPathPen(None, ntos=lambda v: (f"{v:.{prec}f}").rstrip("0").rstrip("."))
    path.draw(pen)
    return pen.getCommands()


# ---------------------------------------------------------------- type
class Font:
    def __init__(self, path):
        tt = TTFont(path)
        tt.flavor = None
        buf = io.BytesIO()
        tt.save(buf)
        self.data = buf.getvalue()
        self.tt = TTFont(io.BytesIO(self.data))
        self.upem = self.tt["head"].unitsPerEm
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.hbface = hb.Face(self.data)
        self.hbfont = hb.Font(self.hbface)
        os2 = self.tt["OS/2"]
        self.cap = getattr(os2, "sCapHeight", 0) or 0.7 * self.upem
        self.xh = getattr(os2, "sxHeight", 0) or 0.5 * self.upem

    def text(self, s, size, x=0, baseline=0, tracking=0.0, features=None):
        """Return (Path, advance) for string s set at size (px), tracking in em."""
        buf = hb.Buffer()
        buf.add_str(s)
        buf.guess_segment_properties()
        feats = {"kern": True, "liga": True}
        if features:
            feats.update(features)
        hb.shape(self.hbfont, buf, feats)
        sc = size / self.upem
        out = Path()
        pen = pathops.PathPen(out, glyphSet=self.gs)  # decomposes composite glyphs
        cx = x
        n = len(buf.glyph_infos)
        for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
            name = self.order[info.codepoint]
            tpen = TransformPen(pen, (sc, 0, 0, -sc, cx + pos.x_offset * sc, baseline - pos.y_offset * sc))
            self.gs[name].draw(tpen)
            cx += pos.x_advance * sc
            if i < n - 1:
                cx += tracking * size
        return pathops.simplify(out), cx - x

    def width(self, s, size, tracking=0.0, features=None):
        return self.text(s, size, 0, 0, tracking, features)[1]


# ---------------------------------------------------------------- oriented-circle tangents
def _ang(cx, cy, x, y):
    return math.degrees(math.atan2(y - cy, x - cx))


def tangent(c1, c2):
    """Tangent segment between two oriented circles.

    c = (cx, cy, R, s) with s=+1 travelling with increasing SVG angle (clockwise
    on screen) and s=-1 decreasing. R=0 means a plain point. Returns (p1, p2).
    """
    (x1, y1, R1, s1), (x2, y2, R2, s2) = c1, c2
    dx, dy = x2 - x1, y2 - y1
    D = math.hypot(dx, dy)
    alpha = math.atan2(dy, dx)
    best = None
    for r1 in ((R1, -R1) if R1 else (0,)):
        for r2 in ((R2, -R2) if R2 else (0,)):
            v = (r1 - r2) / D
            if abs(v) > 1:
                continue
            for sg in (1, -1):
                phi = alpha + sg * math.acos(v)
                n = (math.cos(phi), math.sin(phi))
                p1 = (x1 + r1 * n[0], y1 + r1 * n[1])
                p2 = (x2 + r2 * n[0], y2 + r2 * n[1])
                t = (p2[0] - p1[0], p2[1] - p1[1])
                L = math.hypot(*t)
                if L < 1e-9:
                    continue
                t = (t[0] / L, t[1] / L)
                ok = True
                for (cx, cy, R, s), p in (((x1, y1, R1, s1), p1), ((x2, y2, R2, s2), p2)):
                    if not R:
                        continue
                    th = math.atan2(p[1] - cy, p[0] - cx)
                    tv = (-s * math.sin(th), s * math.cos(th))
                    if tv[0] * t[0] + tv[1] * t[1] < 0.999:
                        ok = False
                if ok:
                    best = (p1, p2)
    if best is None:
        raise ValueError("no tangent for %r %r" % (c1, c2))
    return best


def sweep(a0, a1, s):
    """Signed sweep from a0 to a1 (degrees) travelling in orientation s."""
    d = (a1 - a0) % 360.0
    return d if s > 0 else d - 360.0 if d else 0.0


def route(seq):
    """Build an open centre-line path through a sequence of oriented circles.

    seq items: ('pt', x, y) or ('circ', cx, cy, R, s) — consecutive items are
    joined by tangent lines; circles are traversed by arcs in orientation s.
    """
    items = []
    for it in seq:
        if it[0] == "pt":
            items.append((it[1], it[2], 0, 1))
        else:
            items.append(tuple(it[1:5]))
    segs = [tangent(items[i], items[i + 1]) for i in range(len(items) - 1)]
    p = Path()
    p.moveTo(*segs[0][0])
    for i, (a, b) in enumerate(segs):
        p.lineTo(*b)
        if i + 1 < len(segs):
            cx, cy, R, s = items[i + 1]
            if R:
                a0 = _ang(cx, cy, *b)
                a1 = _ang(cx, cy, *segs[i + 1][0])
                arc_to(p, cx, cy, R, a0, a0 + sweep(a0, a1, s))
    return p
