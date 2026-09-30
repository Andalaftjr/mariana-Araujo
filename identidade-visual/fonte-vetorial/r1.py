"""R1 of the recommended direction (C · Elo): knotted ampersand + integrated wordmark.

Roles follow lockups.py (text, sym, accent, badge, badge_fg, badge_acc).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *  # noqa
from amp_r1 import R1, R1_SMALL, build, scaled
from typo import font, stem

DESCRIPTOR = "CONSULTORIA EM PET TRAVEL"
FAMILY, WEIGHT, DWEIGHT = "plus-jakarta-sans", 700, 600
AMP_K = 1.32          # & height relative to cap height inside the name
SPACE = 0.86          # word space around the & (x normal space)
TRACK = -0.005        # name tracking (em)
DTRACK = 0.22         # descriptor tracking (em)


def _fonts():
    return font(FAMILY, WEIGHT), font(FAMILY, DWEIGHT)


def wordmark(size=100, amp_role="text"):
    """'Coleira & Passaporte' with the knotted &; name baseline at y=0, left at x=0."""
    fn, _ = _fonts()
    cap = fn.cap / fn.upem * size
    pl, wl = fn.text("Coleira", size, 0, 0, TRACK)
    sp = fn.width(" ", size) * SPACE
    st = stem(fn) * size * 1.02
    amp, aw = scaled(wl + sp, 0, cap * AMP_K, st, gap_ratio=0.3)
    xr = wl + sp + aw + sp
    pr, wr = fn.text("Passaporte", size, xr, 0, TRACK)
    lay = [(union(pl, pr), "text")] + [(p, amp_role if r == "primary" else "accent") for p, r in amp]
    return lay, dict(width=xr + wr, cap=cap, amp_top=-cap * AMP_K)


def descriptor(size, x0, width, baseline, align="left"):
    _, fd = _fonts()
    dw = fd.width(DESCRIPTOR, size, DTRACK)
    x = x0 if align == "left" else x0 + (width - dw) / 2
    p, _ = fd.text(DESCRIPTOR, size, x, baseline, DTRACK)
    return p, dw, fd.cap / fd.upem * size


def name_block(size=100, desc=True, align="left", dscale=1.0):
    lay, m = wordmark(size)
    bottom = 0
    if desc:
        dsize = size * 0.2 * dscale
        _, fd = _fonts()
        dcap = fd.cap / fd.upem * dsize
        base = m["cap"] * 0.6 + dcap
        dp, dw, _ = descriptor(dsize, 0, m["width"], base, align)
        lay.append((dp, "text"))
        bottom = base
    m.update(top=m["amp_top"], bottom=bottom)
    return lay, m


def symbol(small=False):
    lay = build(R1_SMALL if small else R1)
    return [(p, "sym" if r == "primary" else "accent") for p, r in lay]


def symbol_at(h, x, y_top, small=False):
    lay = symbol(small)
    ink = union(*[p for p, _ in lay]).bounds
    s = h / (ink[3] - ink[1])
    return [(p.transform(s, 0, 0, s, x - ink[0] * s, y_top - ink[1] * s), r) for p, r in lay], (ink[2] - ink[0]) * s


def badge(cx, cy, D, knockout=False, small=False, fill=0.56):
    disc = circle(cx, cy, D / 2)
    lay = build(R1_SMALL if small else dict(R1, gap=3.3))
    ink = union(*[p for p, _ in lay]).bounds
    h = D * fill
    s = h / (ink[3] - ink[1])
    iw = (ink[2] - ink[0]) * s
    ox = cx - iw / 2 - ink[0] * s - D * 0.01
    oy = cy - h / 2 - ink[1] * s + D * 0.006
    inner = [(p.transform(s, 0, 0, s, ox, oy), r) for p, r in lay]
    if knockout:
        return [(diff(disc, *[p for p, _ in inner]), "badge")]
    return [(disc, "badge")] + [(p, "badge_fg" if r == "primary" else "badge_acc") for p, r in inner]


# ------------------------------------------------------------------ lockups
def lock_principal(knockout=False):
    """Main logo: integrated wordmark (the & of the name is the symbol) + descriptor."""
    lay, m = name_block(100, True)
    return lay


def lock_signature(knockout=False):
    lay, m = name_block(100, False)
    return lay


def lock_horizontal(knockout=False):
    """Selo + name + descriptor."""
    lay, m = name_block(100, True)
    top, bottom = -m["cap"], m["bottom"]
    D = (bottom - top) * 1.5
    cy = (top + bottom) / 2
    b = badge(D / 2, cy, D, knockout)
    gap = m["cap"] * 0.55
    return b + [(p.transform(1, 0, 0, 1, D + gap, 0), r) for p, r in lay]


def lock_vertical(knockout=False):
    lay, m = name_block(100, True, align="center", dscale=1.1)
    D = m["cap"] * 3.6
    b = badge(m["width"] / 2, m["amp_top"] - m["cap"] * 0.6 - D / 2, D, knockout)
    return b + lay


def lock_stacked(knockout=False, desc=True):
    """Coleira / & / Passaporte — the big & is the symbol itself."""
    fn, fd = _fonts()
    size = 100
    cap = fn.cap / fn.upem * size
    pl, wl = fn.text("Coleira", size, 0, 0, TRACK)
    pr, wr = fn.text("Passaporte", size, 0, 0, TRACK)
    W = max(wl, wr)
    amp_h = cap * 2.05
    lead = cap * 0.5
    y_amp = lead + amp_h
    lay_amp, aw = scaled(0, y_amp, amp_h, stem(fn) * size * 1.55, gap_ratio=0.3)
    ax = W / 2 - aw / 2 + cap * 0.04
    lay_amp = [(p.transform(1, 0, 0, 1, ax, 0), "sym" if r == "primary" else "accent") for p, r in lay_amp]
    y2 = y_amp + lead + cap
    lay = [(pl.transform(1, 0, 0, 1, (W - wl) / 2, 0), "text")] + lay_amp + [
        (pr.transform(1, 0, 0, 1, (W - wr) / 2, y2), "text")]
    if desc:
        dsize = size * 0.18
        dcap = fd.cap / fd.upem * dsize
        dp, _, _ = descriptor(dsize, 0, W, y2 + cap * 0.62 + dcap, align="center")
        lay.append((dp, "text"))
    return lay


def lock_symbol(knockout=False):
    return symbol_at(100, 0, 0)[0]


def lock_symbol_small(knockout=False):
    return symbol_at(100, 0, 0, small=True)[0]


def lock_badge(knockout=False):
    return badge(50, 50, 100, knockout)


PIECES = [
    ("cp-logo-principal", lock_principal, 16, 3000, "Logo principal: nome com o & em destaque + descritor"),
    ("cp-logo-horizontal-selo", lock_horizontal, 16, 3000, "Selo + nome + descritor"),
    ("cp-logo-assinatura", lock_signature, 14, 3000, "Nome em uma linha, sem descritor"),
    ("cp-logo-vertical", lock_vertical, 18, 2400, "Selo sobre o nome"),
    ("cp-logo-empilhado", lock_stacked, 18, 2000, "Coleira / & / Passaporte"),
    ("cp-simbolo", lock_symbol, 5, 2048, "& com nó e tag"),
    ("cp-simbolo-reduzido", lock_symbol_small, 5, 1024, "& para até 32 px"),
    ("cp-selo", lock_badge, 2, 2048, "& dentro do círculo"),
]
