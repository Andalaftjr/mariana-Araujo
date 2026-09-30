"""Lockup construction for the three directions.

A lockup is a list of (Path, role) + a bounding box. Roles:
  text      name + descriptor
  sym       symbol main body
  accent    symbol accent (tag / eyelet / buckle)
  badge     circular container (selo)
  badge_fg  symbol drawn inside the badge (knock-out in one-colour versions)
  badge_acc accent inside the badge
"""
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from geo import *  # noqa
from sym import AMP, amp_centerline, sym_amp, sym_strap, sym_tag, sym_tag_small
from typo import FULL_NAME, custom_amp, font, stem, wordmark

DESCRIPTOR = "CONSULTORIA EM PET TRAVEL"

PALETTES = {
    "A": [
        ("Grafite Pista", "#23272F", "Base do símbolo e do nome: firmeza, sinalização, leitura imediata."),
        ("Amarelo Embarque", "#F2B63D", "Acento do ilhós: atenção, orientação, o ‘ponto de embarque’."),
        ("Papel Bilhete", "#F7F5F0", "Fundo claro e respiros: limpeza de documento."),
        ("Cinza Terminal", "#8C939E", "Textos de apoio, linhas e ícones secundários."),
    ],
    "B": [
        ("Petróleo", "#0F4C5C", "Cor principal: profundidade, calma, viagem longa."),
        ("Ocre Fivela", "#D99A45", "Acento da fivela: calor, cuidado artesanal."),
        ("Névoa", "#EEF2EF", "Fundo claro e respiros."),
        ("Verde-água", "#7FA7A0", "Apoio: bem-estar e tranquilidade."),
    ],
    "C": [
        ("Azul Passaporte", "#1B2B44", "Cor institucional. Confiança, documentação, experiência internacional — o azul-marinho dos passaportes."),
        ("Terracota Tag", "#C8694A", "Acento exclusivo da tag do &. Calor, cuidado, o animal no centro. Usar com parcimônia."),
        ("Linho", "#F4EFE6", "Fundo principal. Acolhimento e calma, evita o branco clínico."),
        ("Céu de Cabine", "#A9BCCB", "Apoio: tranquilidade, mobilidade. Fundos de seção, gráficos, ícones."),
        ("Tinta", "#111A2B", "Texto corrido de alta legibilidade e versão escura profunda."),
    ],
}


def pal(d):
    return {n: h for n, h, _ in PALETTES[d]}


# ------------------------------------------------------------------ type per direction
def fonts(d):
    if d == "A":
        return font("manrope", 800), font("manrope", 700)
    if d == "B":
        return font("fraunces", 500), font("manrope", 600)
    return font("outfit", 500), font("outfit", 500)


def name_block(d, size=100, descriptor=True, align="left", dscale=1.0):
    """Name (+ descriptor) as paths. Baseline of the name at y=0, left at x=0."""
    fn, fd = fonts(d)
    if d == "C":
        wm = wordmark(fn, size, amp="custom")
    else:
        wm = wordmark(fn, size, amp="font")
    cap = wm["cap"]
    layers = [(wm["text"], "text")]
    if wm["amp"] is not None:
        layers.append((wm["amp"], "text"))
        layers.append((wm["tag"], "accent"))
    w = wm["width"]
    bottom = 0
    if descriptor:
        dsize = size * (0.215 if d != "B" else 0.2) * dscale
        track = 0.2
        dw = fd.width(DESCRIPTOR, dsize, track)
        dcap = fd.cap / fd.upem * dsize
        base = cap * 0.62 + dcap
        dx = 0 if align == "left" else (w - dw) / 2
        dp, _ = fd.text(DESCRIPTOR, dsize, dx, base, track)
        layers.append((dp, "text"))
        bottom = base
        w = max(w, dw)
    # tight x bounds of the name ink for optical alignment
    return layers, dict(width=w, cap=cap, top=-cap, bottom=bottom)


def symbol_layers(d, size_h, x, y_top, small=False):
    """Symbol scaled to height size_h (of its ink box) placed at (x, y_top)."""
    if d == "A":
        lay = sym_tag_small() if small else sym_tag()
    elif d == "B":
        lay = sym_strap()
    else:
        lay = sym_amp()
    ink = union(*[p for p, _ in lay]).bounds
    s = size_h / (ink[3] - ink[1])
    out = []
    for p, r in lay:
        role = "sym" if r == "primary" else "accent"
        out.append((p.transform(s, 0, 0, s, x - ink[0] * s, y_top - ink[1] * s), role))
    return out, (ink[2] - ink[0]) * s


def badge_layers(cx, cy, D, knockout=False):
    """Selo: the brand & inside a circle."""
    r = D / 2
    disc = circle(cx, cy, r)
    lay = sym_amp()
    ink = union(*[p for p, _ in lay]).bounds
    h = D * 0.56
    s = h / (ink[3] - ink[1])
    iw = (ink[2] - ink[0]) * s
    # optical centre: the & is right-heavy (tag) -> nudge left a touch
    ox = cx - iw / 2 - ink[0] * s - D * 0.012
    oy = cy - h / 2 - ink[1] * s + D * 0.01
    inner = [(p.transform(s, 0, 0, s, ox, oy), r_) for p, r_ in lay]
    if knockout:
        allin = union(*[p for p, _ in inner])
        # keep the gap between tag and line visible: subtract each shape separately
        return [(diff(disc, allin), "badge")]
    return [(disc, "badge")] + [(p, "badge_fg" if r_ == "primary" else "badge_acc") for p, r_ in inner]


# ------------------------------------------------------------------ lockups
def lock_horizontal(d, descriptor=True, badge=None, knockout=False):
    """Symbol left + name. For C the symbol is the selo (badge) to avoid reading
    "& Coleira & Passaporte"."""
    size = 100
    nl, m = name_block(d, size, descriptor)
    block_h = m["bottom"] - m["top"]
    if d == "C":
        use_badge = True if badge is None else badge
    else:
        use_badge = False
    if not descriptor:
        block_h = m["cap"]
    if use_badge:
        D = block_h * (1.55 if descriptor else 1.9)
        cy = m["top"] + block_h / 2
        sl = badge_layers(D / 2, cy, D, knockout)
        sw = D
    else:
        h = block_h * (1.35 if descriptor else 1.7)
        if d == "A":
            h = block_h * (1.5 if descriptor else 1.9)
        y_top = m["top"] + block_h / 2 - h / 2
        sl, sw = symbol_layers(d, h, 0, y_top)
    gap = m["cap"] * (0.55 if use_badge else 0.6)
    moved = [(p.transform(1, 0, 0, 1, sw + gap, 0), r) for p, r in nl]
    return sl + moved


def lock_wordmark(d, descriptor=False):
    nl, m = name_block(d, 100, descriptor)
    return nl


def lock_vertical(d, descriptor=True, knockout=False):
    size = 100
    nl, m = name_block(d, size, descriptor, align="center", dscale=1.12)
    w = m["width"]
    if d == "C":
        D = m["cap"] * 3.5
        sl = badge_layers(w / 2, m["top"] - m["cap"] * 0.75 - D / 2, D, knockout)
    else:
        h = m["cap"] * (3.2 if d == "A" else 2.9)
        y_top = m["top"] - m["cap"] * 0.75 - h
        sl, sw = symbol_layers(d, h, 0, y_top)
        sl = [(p.transform(1, 0, 0, 1, w / 2 - sw / 2, 0), r) for p, r in sl]
    # centre the name block using the actual ink width
    return sl + nl


def lock_stacked(d="C", descriptor=False):
    """Coleira / & / Passaporte — the & of the name *is* the symbol."""
    fn, fd = fonts(d)
    size = 100
    cap = fn.cap / fn.upem * size
    pl, wl = fn.text("Coleira", size, 0, 0)
    pr, wr = fn.text("Passaporte", size, 0, 0)
    W = max(wl, wr)
    amp_h = cap * 1.55
    lead = cap * 0.55
    # & centred between the two words
    st = stem(fn) * size * 0.92 * 1.25
    y_amp_base = lead + amp_h
    a_line, a_tag, aw = custom_amp(0, y_amp_base, amp_h, st)
    ax = W / 2 - aw / 2
    a_line = a_line.transform(1, 0, 0, 1, ax, 0)
    a_tag = a_tag.transform(1, 0, 0, 1, ax, 0)
    y2 = y_amp_base + lead + cap
    lay = [
        (pl.transform(1, 0, 0, 1, (W - wl) / 2, 0), "text"),
        (a_line, "sym"),
        (a_tag, "accent"),
        (pr.transform(1, 0, 0, 1, (W - wr) / 2, y2), "text"),
    ]
    if descriptor:
        dsize = size * 0.19
        dw = fd.width(DESCRIPTOR, dsize, 0.2)
        dcap = fd.cap / fd.upem * dsize
        dp, _ = fd.text(DESCRIPTOR, dsize, (W - dw) / 2, y2 + cap * 0.7 + dcap, 0.2)
        lay.append((dp, "text"))
    return lay


def lock_symbol(d, small=False):
    sl, _ = symbol_layers(d, 100, 0, 0, small=small)
    return sl


def lock_badge(knockout=False):
    return badge_layers(50, 50, 100, knockout=knockout)


def ink_bounds(layers):
    xs0, ys0, xs1, ys1 = [], [], [], []
    for p, _ in layers:
        b = p.bounds
        xs0.append(b[0]); ys0.append(b[1]); xs1.append(b[2]); ys1.append(b[3])
    return min(xs0), min(ys0), max(xs1), max(ys1)
