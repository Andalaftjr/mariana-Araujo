"""Direction E, round 2 (E2): lockups, seal, colourways and pieces."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *  # noqa
import e
import emb
import emb2
from e import DESCRIPTOR, TRACK, DTRACK, NAVY, TERRA, LINEN, colorway, name, descriptor, place, arc_text, cap_h, _fonts  # noqa
from pets import grow

G = emb2.E2


def place_circle(lay, diameter, x, cy, g=G):
    """Scale an emblem so its collar has the given diameter, collar left edge at x, centre at cy."""
    s = diameter / (2 * g["R_out"])
    tx = x - (g["C"][0] - g["R_out"]) * s
    ty = cy - g["C"][1] * s
    out = [(p.transform(s, 0, 0, s, tx, ty), r) for p, r in lay]
    return out, diameter


def emblem_full(**kw):
    return emb2.emblem(**kw)


def emblem_simple(**kw):
    return emb2.simple(**kw)


def emblem_no_tag():
    """For avatars: the collar fills the circle the platform crops to."""
    lay = emb2.emblem(tag_dy=-1.0, tag_r=8.5)
    g = G
    cut = circle(g["C"][0], g["C"][1], g["R_out"] + 0.01)
    return [(inter(p, cut), r) for p, r in lay]


# ------------------------------------------------------------------ lockups
def lock_horizontal(knockout=False, desc=True, small=False):
    cap = cap_h(100)
    nm, w = name(100)
    lay = list(nm)
    top, bot = -cap, 0.0
    if desc:
        _, fd = _fonts()
        dsize = 21
        dcap = fd.cap / fd.upem * dsize
        base = cap * 0.6 + dcap
        lay.append((descriptor(dsize, 0, base), "text"))
        bot = base
    blk = bot - top
    dia = blk * (2.05 if desc else 2.3)
    sl, sw = place_circle(emblem_simple() if small else emblem_full(), dia, 0, (top + bot) / 2)
    gap = cap * 0.75
    return sl + [(p.transform(1, 0, 0, 1, sw + gap, 0), r) for p, r in lay]


def lock_signature(knockout=False):
    return lock_horizontal(knockout, desc=False, small=True)


def lock_compact(knockout=False):
    """Name on two lines beside the emblem: for square-ish spaces and social headers."""
    fn, fd = _fonts()
    size = 100
    cap = fn.cap / fn.upem * size
    l1, w1 = fn.text("Coleira ", size, 0, 0, TRACK)
    full1, _ = fn.text("Coleira &", size, 0, 0, TRACK)
    amp = diff(full1, l1)
    lead = size * 1.02
    l2, w2 = fn.text("Passaporte", size, 0, lead, TRACK)
    dw = fd.width(DESCRIPTOR, 20, DTRACK)
    dsize = 20 * w2 / dw
    dcap = fd.cap / fd.upem * dsize
    base = lead + size * 0.26 + cap * 0.32 + dcap
    d = descriptor(dsize, 0, base)
    top, bot = -cap, base
    dia = (bot - top) * 1.08
    sl, sw = place_circle(emblem_full(), dia, 0, (top + bot) / 2)
    gap = cap * 0.62
    text = [(l1, "text"), (amp, "amp"), (l2, "text"), (d, "text")]
    return sl + [(p.transform(1, 0, 0, 1, sw + gap, 0), r) for p, r in text]


def lock_vertical(knockout=False):
    cap = cap_h(100)
    nm, w = name(100)
    _, fd = _fonts()
    dsize = 21
    dcap = fd.cap / fd.upem * dsize
    base = cap * 0.6 + dcap
    d = descriptor(dsize, 0, base, w, center=True)
    dia = cap * 4.4
    tag_extra = (G["tag_dy"] + G["tag_r"]) / (2 * G["R_out"]) * dia
    cy = -cap - cap * 0.5 - tag_extra - dia / 2
    sl, sw = place_circle(emblem_full(), dia, w / 2 - dia / 2, cy)
    return sl + nm + [(d, "text")]


def lock_name(knockout=False):
    return name(100)[0]


def lock_emblem(knockout=False):
    return place(emblem_full(), 100, 0, 0)[0]


def lock_emblem_simple(knockout=False):
    return place(emblem_simple(), 100, 0, 0)[0]


def icon(knockout=False):
    return e.icon(knockout)


def lock_icon(knockout=False):
    return place(icon(knockout), 100, 0, 0)[0]


# ------------------------------------------------------------------ seal
SEAL = dict(C=(50.0, 50.0), R_out=48.0, R_in=33.5, gap=2.2)


def seal(tag=True, text="Coleira & Passaporte"):
    g = SEAL
    C, R_out, R_in, gap = g["C"], g["R_out"], g["R_in"], g["gap"]
    rm = (R_out + R_in) / 2
    fn, fd = _fonts()
    strap = ring(C[0], C[1], R_out, R_in)
    ncap = 6.1
    nsize = ncap / (fn.cap / fn.upem)
    parts = arc_text(fn, text, nsize, C[0], C[1], rm - ncap / 2, -90, TRACK + 0.015)
    txt = union(*[p for p, ch in parts if ch != "&"])
    amp = union(*[p for p, ch in parts if ch == "&"])
    dcap = 3.45
    dsize = dcap / (fd.cap / fd.upem)
    desc = union(*[p for p, _ in arc_text(fd, DESCRIPTOR, dsize, C[0], C[1], rm + dcap / 2, 90, 0.19, bottom=True)])
    holes = union(*[circle(C[0] + rm * math.cos(math.radians(a)), C[1] + rm * math.sin(math.radians(a)), 1.25) for a in (180, 0)])
    strap = diff(strap, holes)
    dash = []
    for k in range(0, 360, 6):
        pth = Path()
        rr = R_out - 2.1
        pth.moveTo(C[0] + rr * math.cos(math.radians(k)), C[1] + rr * math.sin(math.radians(k)))
        arc_to(pth, C[0], C[1], rr, k, k + 3.0)
        dash.append(stroke(pth, 0.7, cap="round"))
    stitch = union(*dash)
    # inside: the E2 pets and route (plane inside the collar: the strap carries the name)
    inner = emb2.emblem(plane_mode="inside", tag_r=0.01, tag_dy=-60, holes=False, stitch=False)
    k = (R_in - gap + G["gap"]) / G["R_in"]
    inside = [(p.transform(k, 0, 0, k, C[0] - G["C"][0] * k, C[1] - G["C"][1] * k), r)
              for p, r in inner if r in ("dog", "cat", "route")]
    lay_tag = []
    if tag:
        tc = (C[0], C[1] + R_out + 7.0)
        tg = circle(tc[0], tc[1], 9.0)
        tg = diff(tg, circle(tc[0], tc[1] - 9.0 + 3.0, 1.55))
        strap = diff(strap, grow(tg, gap))
        stitch = diff(stitch, grow(tg, gap))
        lay_tag = [(tg, "tag")]
    cut = union(txt, amp, desc, stitch)
    lay = [(diff(strap, cut), "ring"), (txt, "stext"), (amp, "samp"), (desc, "stext"), (stitch, "stext")]
    return lay + lay_tag + inside


def lock_seal(knockout=False):
    lay = seal()
    if knockout:
        lay = [(p, r) for p, r in lay if r not in ("stext", "samp")]
    return place(lay, 100, 0, 0)[0]


# ------------------------------------------------------------------ supporting elements
def el_route(knockout=False):
    return e.el_route(knockout)


def el_tag(knockout=False):
    tg = circle(50, 50, 9.0)
    return [(diff(tg, circle(50, 50 - 9 + 3.1, 1.6)), "tag")]


PIECES = [
    ("cp-selo", lock_seal, 3, 2400, "Selo: o nome escrito na coleira"),
    ("cp-logo-horizontal", lock_horizontal, 16, 3000, "Emblema + nome + descritor"),
    ("cp-logo-compacto", lock_compact, 14, 2600, "Emblema + nome em duas linhas + descritor"),
    ("cp-logo-assinatura", lock_signature, 14, 3000, "Emblema simplificado + nome"),
    ("cp-logo-vertical", lock_vertical, 18, 2400, "Emblema sobre o nome"),
    ("cp-logo-nome", lock_name, 12, 3000, "Só o nome"),
    ("cp-emblema", lock_emblem, 4, 2048, "Emblema completo"),
    ("cp-emblema-simplificado", lock_emblem_simple, 4, 1600, "Emblema para 32-96 px"),
    ("cp-icone", lock_icon, 2, 1024, "Ícone para até 32 px e favicon"),
]

SUPPORT = [
    ("cp-rota", el_route, 3, 2000, "Rota de voo para composições"),
    ("cp-plaquinha", el_tag, 2, 600, "Plaquinha de identificação"),
]


# names the presentation shares with round 1
from e import NAME_FONT  # noqa: E402
lock_principal = lock_horizontal
