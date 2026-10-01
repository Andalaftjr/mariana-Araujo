"""Direction D · Dobra: lockups and support elements.

Roles: text, amp (the & of the name), sym (head), facet (lit half of the head),
accent (ears), badge / badge_fg / badge_facet / badge_acc (selo).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *  # noqa
import dobra
from typo import font

DESCRIPTOR = "CONSULTORIA EM PET TRAVEL"
NAME_FONT = ("fraunces", 600)
DESC_FONT = ("plus-jakarta-sans", 600)
TRACK = -0.012
DTRACK = 0.22


def _fonts():
    return font(*NAME_FONT), font(*DESC_FONT)


def cap_h(size=100):
    fn, _ = _fonts()
    return fn.cap / fn.upem * size


def name(size=100, amp_role="amp"):
    """'Coleira & Passaporte' in curves; the & may be coloured on its own."""
    fn, _ = _fonts()
    full, w = fn.text("Coleira & Passaporte", size, 0, 0, TRACK)
    pl, wl = fn.text("Coleira ", size, 0, 0, TRACK)
    amp, wa = fn.text("&", size, wl, 0, TRACK)
    amp = inter(full, _grow_box(amp))
    rest = diff(full, amp)
    return [(rest, "text"), (amp, amp_role)], w


def _grow_box(p):
    b = p.bounds
    return rect(b[0] - 0.5, b[1] - 50, b[2] - b[0] + 1, b[3] - b[1] + 100)


def descriptor(size, x, baseline, width=None, align="left"):
    _, fd = _fonts()
    dw = fd.width(DESCRIPTOR, size, DTRACK)
    if align == "center" and width:
        x = x + (width - dw) / 2
    p, _ = fd.text(DESCRIPTOR, size, x, baseline, DTRACK)
    return p, dw


def symbol(kind="dog", facet=True):
    lay = dobra.pet(kind, facet)
    return [(p, {"primary": "sym", "facet": "facet", "accent": "accent"}[r]) for p, r in lay]


def symbol_at(h, x, y_top, kind="dog", facet=True):
    lay = symbol(kind, facet)
    ink = union(*[p for p, _ in lay]).bounds
    s = h / (ink[3] - ink[1])
    return [(p.transform(s, 0, 0, s, x - ink[0] * s, y_top - ink[1] * s), r) for p, r in lay], (ink[2] - ink[0]) * s


def badge(cx, cy, D, knockout=False, kind="dog", fill=0.64, facet=True):
    disc = circle(cx, cy, D / 2)
    lay = dobra.pet(kind, facet)
    ink = union(*[p for p, _ in lay]).bounds
    s = D * fill / max(ink[2] - ink[0], ink[3] - ink[1])
    w, h = (ink[2] - ink[0]) * s, (ink[3] - ink[1]) * s
    ox, oy = cx - w / 2 - ink[0] * s, cy - h / 2 - ink[1] * s + D * 0.02
    inner = [(p.transform(s, 0, 0, s, ox, oy), r) for p, r in lay]
    if knockout:
        return [(diff(disc, *[p for p, _ in inner]), "badge")]
    m = {"primary": "badge_fg", "facet": "badge_facet", "accent": "badge_acc"}
    return [(disc, "badge")] + [(p, m[r]) for p, r in inner]


# ------------------------------------------------------------------ lockups
def lock_principal(knockout=False, desc=True):
    size = 100
    cap = cap_h(size)
    nm, w = name(size)
    lay = list(nm)
    top, bot = -cap, 0
    if desc:
        _, fd = _fonts()
        dsize = size * 0.2
        dcap = fd.cap / fd.upem * dsize
        base = cap * 0.62 + dcap
        dp, _ = descriptor(dsize, 0, base)
        lay.append((dp, "text"))
        bot = base
    blk = bot - top
    h = blk * (1.9 if desc else 1.75)
    sl, sw = symbol_at(h, 0, (top + bot) / 2 - h / 2 + blk * 0.02)
    gap = cap * 0.72
    return sl + [(p.transform(1, 0, 0, 1, sw + gap, 0), r) for p, r in lay]


def lock_signature(knockout=False):
    return lock_principal(knockout, desc=False)


def lock_name(knockout=False):
    nm, w = name(100)
    return nm


def lock_vertical(knockout=False):
    size = 100
    cap = cap_h(size)
    nm, w = name(size)
    _, fd = _fonts()
    dsize = size * 0.21
    dcap = fd.cap / fd.upem * dsize
    base = cap * 0.62 + dcap
    dp, _ = descriptor(dsize, 0, base, w, "center")
    h = cap * 3.3
    sl, sw = symbol_at(h, 0, -cap - cap * 0.62 - h)
    sl = [(p.transform(1, 0, 0, 1, w / 2 - sw / 2, 0), r) for p, r in sl]
    return sl + nm + [(dp, "text")]


def lock_stacked(knockout=False):
    """Symbol left, name on two lines (Coleira & / Passaporte)."""
    fn, fd = _fonts()
    size = 100
    cap = cap_h(size)
    l1, w1 = fn.text("Coleira &", size, 0, 0, TRACK)
    amp, _ = fn.text("&", size, fn.width("Coleira ", size, TRACK), 0, TRACK)
    amp = inter(l1, _grow_box(amp))
    l1 = diff(l1, amp)
    lead = cap * 1.42
    l2, w2 = fn.text("Passaporte", size, 0, lead, TRACK)
    top, bot = -cap, lead
    h = (bot - top) * 1.08
    sl, sw = symbol_at(h, 0, top - (h - (bot - top)) / 2)
    gap = cap * 0.62
    tx = sw + gap
    return sl + [(l1.transform(1, 0, 0, 1, tx, 0), "text"), (amp.transform(1, 0, 0, 1, tx, 0), "amp"),
                 (l2.transform(1, 0, 0, 1, tx, 0), "text")]


def lock_symbol(knockout=False, kind="dog"):
    return symbol_at(100, 0, 0, kind)[0]


def lock_badge(knockout=False, kind="dog"):
    return badge(50, 50, 100, knockout, kind)


# ------------------------------------------------------------------ support: the folded corner ("orelha")
def folded_corner_card(w=160.0, h=100.0, f=26.0, r=6.0, gap=2.2):
    """A card/page with its top-right corner folded: the brand's 'orelha'."""
    page = round_poly([(0, 0), (w - f, 0), (w, f), (w, h), (0, h)], [r, 1.5, 1.5, r, r])
    flap = round_poly([(w - f, 0), (w - f, f), (w, f)], [1.5, 2.5, 1.5])
    page = diff(page, union(flap, stroke(flap, 2 * gap, cap="round", join="round")))
    return [(page, "sym"), (flap, "accent")]


def family_row(knockout=False, gap=22.0):
    """Dog, cat and rabbit at the same head size (same fold, different ears)."""
    out = []
    x = 0.0
    for kind in ("dog", "cat", "rabbit"):
        lay = symbol(kind)
        ink = union(*[p for p, _ in lay]).bounds
        out += [(p.transform(1, 0, 0, 1, x - ink[0], 0), r) for p, r in lay]
        x += (ink[2] - ink[0]) + gap
    return out


PIECES = [
    ("cp-logo-principal", lock_principal, 16, 3000, "Símbolo + nome + descritor"),
    ("cp-logo-assinatura", lock_signature, 14, 3000, "Símbolo + nome, sem descritor"),
    ("cp-logo-vertical", lock_vertical, 18, 2400, "Símbolo sobre o nome"),
    ("cp-logo-compacto", lock_stacked, 14, 2400, "Símbolo + nome em duas linhas"),
    ("cp-logo-nome", lock_name, 12, 3000, "Só o nome"),
    ("cp-simbolo", lock_symbol, 4, 2048, "O cão de origami"),
    ("cp-simbolo-gato", lambda ko=False: lock_symbol(ko, "cat"), 4, 2048, "Família: gato"),
    ("cp-simbolo-coelho", lambda ko=False: lock_symbol(ko, "rabbit"), 4, 2048, "Família: coelho"),
    ("cp-selo", lock_badge, 2, 2048, "Símbolo no círculo"),
]
SUPPORT = [
    ("cp-elemento-orelha", lambda ko=False: folded_corner_card(), 3, 2000, "Página com a orelha dobrada"),
    ("cp-elemento-familia", family_row, 4, 3000, "Cão, gato e coelho"),
]


NAVY, TERRA, LINEN, SKY, INK = "#1B2B44", "#C8694A", "#F4EFE6", "#A9BCCB", "#111A2B"
FACET, FACET_NEG = "#2B4368", "#E2D9CB"


def colorway(way, amp_terra=True):
    amp = TERRA if amp_terra else None
    if way == "cor":
        c = dict(text=NAVY, amp=amp or NAVY, sym=NAVY, facet=FACET, accent=TERRA,
                 badge=NAVY, badge_fg=LINEN, badge_facet=FACET_NEG, badge_acc=TERRA)
        return c, False
    if way == "negativo":
        c = dict(text=LINEN, amp=amp or LINEN, sym=LINEN, facet=FACET_NEG, accent=TERRA,
                 badge=LINEN, badge_fg=NAVY, badge_facet=FACET, badge_acc=TERRA)
        return c, False
    if way == "cinza":
        c = dict(text="#3B3B3B", amp="#8F8F8F" if amp_terra else "#3B3B3B", sym="#3B3B3B", facet="#525252", accent="#8F8F8F",
                 badge="#3B3B3B", badge_fg="#F2F2F2", badge_facet="#DADADA", badge_acc="#8F8F8F")
        return c, False
    one = {"preto": "#000000", "branco": "#FFFFFF", "uma-cor": NAVY}[way]
    return {k: one for k in ("text", "amp", "sym", "facet", "accent", "badge", "badge_fg", "badge_facet", "badge_acc")}, True
