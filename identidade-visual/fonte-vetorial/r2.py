"""R2 of the recommended direction (C · Elo): the & drawn as a pet collar.

Roles follow lockups.py (text, sym, accent, badge, badge_fg, badge_acc).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *  # noqa
from amp_r2 import R2, R2_SMALL, R2_TEXT, build, scaled, local_rect, _grow
from typo import font, stem

DESCRIPTOR = "CONSULTORIA EM PET TRAVEL"
FAMILY, WEIGHT, DWEIGHT = "plus-jakarta-sans", 700, 600
AMP_K = 1.36          # & height relative to cap height inside the name
SPACE = 0.86          # word space around the & (x normal space)
TRACK = -0.005        # name tracking (em)
DTRACK = 0.22         # descriptor tracking (em)


def _fonts():
    return font(FAMILY, WEIGHT), font(FAMILY, DWEIGHT)


def wordmark(size=100, amp_role="text", small=False):
    """'Coleira & Passaporte' with the knotted &; name baseline at y=0, left at x=0."""
    fn, _ = _fonts()
    cap = fn.cap / fn.upem * size
    pl, wl = fn.text("Coleira", size, 0, 0, TRACK)
    sp = fn.width(" ", size) * SPACE
    st = stem(fn) * size * 1.02
    amp, aw = scaled(wl + sp, 0, cap * AMP_K, st, g=R2_SMALL if small else R2_TEXT)
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


def name_block(size=100, desc=True, align="left", dscale=1.0, small=False):
    lay, m = wordmark(size, small=small)
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


def symbol(small=False, medium=False):
    lay = build(R2_SMALL if small else (R2_TEXT if medium else R2))
    return [(p, "sym" if r == "primary" else "accent") for p, r in lay]


def symbol_at(h, x, y_top, small=False, medium=False):
    lay = symbol(small, medium)
    ink = union(*[p for p, _ in lay]).bounds
    s = h / (ink[3] - ink[1])
    return [(p.transform(s, 0, 0, s, x - ink[0] * s, y_top - ink[1] * s), r) for p, r in lay], (ink[2] - ink[0]) * s


def badge(cx, cy, D, knockout=False, small=False, fill=0.6, medium=False):
    disc = circle(cx, cy, D / 2)
    lay = build(R2_SMALL if small else (R2_TEXT if medium else R2))
    ink = union(*[p for p, _ in lay]).bounds
    h = D * fill
    s = h / (ink[3] - ink[1])
    iw = (ink[2] - ink[0]) * s
    ox = cx - iw / 2 - ink[0] * s - D * 0.004
    oy = cy - h / 2 - ink[1] * s + D * 0.004
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


def lock_signature_small(knockout=False):
    lay, m = name_block(100, False, small=True)
    return lay


def lock_horizontal(knockout=False):
    """Selo + name + descriptor."""
    lay, m = name_block(100, True)
    top, bottom = -m["cap"], m["bottom"]
    D = (bottom - top) * 1.5
    cy = (top + bottom) / 2
    b = badge(D / 2, cy, D, knockout, small=True, fill=0.62)
    gap = m["cap"] * 0.55
    return b + [(p.transform(1, 0, 0, 1, D + gap, 0), r) for p, r in lay]


def lock_vertical(knockout=False):
    lay, m = name_block(100, True, align="center", dscale=1.1)
    D = m["cap"] * 3.6
    b = badge(m["width"] / 2, m["amp_top"] - m["cap"] * 0.6 - D / 2, D, knockout, medium=True)
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
    lay_amp, aw = scaled(0, y_amp, amp_h, stem(fn) * size * 1.5, g=R2)
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


def lock_symbol_medium(knockout=False):
    return symbol_at(100, 0, 0, medium=True)[0]


# ------------------------------------------------------------------ support elements (pet cues)
def strap_band(length=600.0, w=24.0, holes=5, knockout=False):
    """Faixa-coleira: a horizontal collar strap with buckle, keeper and perforated tip."""
    gap = w * 0.2
    y = 0.0
    bx = w * 0.62                                  # buckle centre
    hl, hn, t = w * 0.5, w / 2 + w * 0.26, w * 0.19
    band = stroke(_line(bx, y, length, y), w, cap="butt")
    band = union(band, circle(length, y, w / 2))
    step = w * 0.62
    band = diff(band, union(*[circle(length - w * 0.55 - i * step, y, w * 0.16) for i in range(holes)]))
    outer = local_rect(bx, y, 0, -hl, -hn, hl, hn, w * 0.2)
    inner = local_rect(bx, y, 0, -hl + t, -hn + t, hl - t, hn - t, w * 0.06)
    frame = diff(outer, inner)
    gin = w * 0.09
    inside = inter(band, local_rect(bx, y, 0, -hl + t + gin, -hn + t + gin, hl - t - gin, hn - t - gin, w * 0.04))
    band = union(diff(band, _grow(outer, gap)), inside)
    kx = bx + w * 2.1                              # keeper (passador)
    keeper = local_rect(kx, y, 0, -w * 0.16, -hn + w * 0.04, w * 0.16, hn - w * 0.04, w * 0.1)
    band = diff(band, _grow(keeper, gap * 0.8))
    return [(union(band, frame, keeper), "sym")]


def tag_badge(r=50.0, ring_r=None):
    """Plaquinha: disc with its ring on top, for numbers and highlights."""
    ring_r = ring_r or r * 0.34
    t = ring_r * 0.5
    rc = (0.0, -r - ring_r + t * 0.9)
    ringp = ring(rc[0], rc[1], ring_r, ring_r - t)
    disc = circle(0, 0, r)
    disc = diff(disc, _grow(inter(ringp, circle(0, 0, r + 3)), r * 0.06))
    return [(ringp, "sym"), (disc, "accent")]


def _line(xa, ya, xb, yb):
    p = Path()
    p.moveTo(xa, ya)
    p.lineTo(xb, yb)
    return p


def lock_badge(knockout=False):
    return badge(50, 50, 100, knockout)


PIECES = [
    ("cp-logo-principal", lock_principal, 16, 3000, "Logo principal: nome com o & em destaque + descritor"),
    ("cp-logo-horizontal-selo", lock_horizontal, 16, 3000, "Selo + nome + descritor"),
    ("cp-logo-assinatura", lock_signature, 14, 3000, "Nome em uma linha, sem descritor"),
    ("cp-logo-assinatura-reduzida", lock_signature_small, 14, 1600, "Nome em uma linha para menos de 240 px"),
    ("cp-logo-vertical", lock_vertical, 18, 2400, "Selo sobre o nome"),
    ("cp-logo-empilhado", lock_stacked, 18, 2000, "Coleira / & / Passaporte"),
    ("cp-simbolo", lock_symbol, 5, 2048, "& coleira: fivela, argola, plaquinha, nó e ponta furada"),
    ("cp-simbolo-medio", lock_symbol_medium, 5, 1024, "& sem os respiros do nó, de 32 a 64 px"),
    ("cp-simbolo-reduzido", lock_symbol_small, 5, 1024, "& só com laço, argola e plaquinha, até 32 px"),
    ("cp-selo", lock_badge, 2, 2048, "& dentro do círculo"),
]

SUPPORT = [
    ("cp-elemento-faixa-coleira", lambda ko=False: strap_band(), 4, 3000, "Faixa-coleira para divisores e bordas"),
    ("cp-elemento-faixa-coleira-longa", lambda ko=False: strap_band(length=1500.0, w=22.0), 4, 3000, "Faixa-coleira fina para cabeçalhos de documento"),
    ("cp-elemento-plaquinha", lambda ko=False: tag_badge(), 4, 1024, "Plaquinha para números e destaques"),
]
