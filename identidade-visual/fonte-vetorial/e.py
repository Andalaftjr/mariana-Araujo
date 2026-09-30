"""Direction E · Companheiros de viagem: lockups, colourways and pieces."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *  # noqa
import emb
from typo import font
import pathops

DESCRIPTOR = "CONSULTORIA EM PET TRAVEL"
NAME_FONT = ("fraunces", 600)
DESC_FONT = ("plus-jakarta-sans", 600)
TRACK, DTRACK = -0.012, 0.22
NAVY, TERRA, LINEN, SKY, INK = "#1B2B44", "#C8694A", "#F4EFE6", "#A9BCCB", "#111A2B"


def _fonts():
    return font(*NAME_FONT), font(*DESC_FONT)


def cap_h(size=100):
    fn, _ = _fonts()
    return fn.cap / fn.upem * size


def _box(p):
    b = p.bounds
    return rect(b[0] - 0.5, b[1] - 50, b[2] - b[0] + 1, b[3] - b[1] + 100)


def name(size=100):
    fn, _ = _fonts()
    full, w = fn.text("Coleira & Passaporte", size, 0, 0, TRACK)
    _, wl = fn.text("Coleira ", size, 0, 0, TRACK)
    amp, _ = fn.text("&", size, wl, 0, TRACK)
    amp = inter(full, _box(amp))
    return [(diff(full, amp), "text"), (amp, "amp")], w


def descriptor(size, x, baseline, width=None, center=False):
    _, fd = _fonts()
    dw = fd.width(DESCRIPTOR, size, DTRACK)
    if center and width:
        x += (width - dw) / 2
    p, _ = fd.text(DESCRIPTOR, size, x, baseline, DTRACK)
    return p


def place(lay, h, x, y_top):
    ink = union(*[p for p, _ in lay]).bounds
    s = h / (ink[3] - ink[1])
    return [(p.transform(s, 0, 0, s, x - ink[0] * s, y_top - ink[1] * s), r) for p, r in lay], (ink[2] - ink[0]) * s


def emblem_full(**kw):
    return emb.emblem(end="plane", **kw)


def emblem_no_tag(**kw):
    """For avatars: the collar ring fills the circle, the tag is left out."""
    lay = emb.emblem(end="plane", **kw)
    g = emb.E
    cut = circle(g["C"][0], g["C"][1], g["R_out"] + 0.01)
    return [(inter(p, cut), r) for p, r in lay if r != "tag"]


def icon(knockout=False):
    lay = emb.icon()
    lay = [(p, "idog" if r == "dog" else r) for p, r in lay]
    if knockout:
        # one colour: the dog is cut out of the disc, the cat stays solid inside a thin gap
        disc = [p for p, r in lay if r == "badge"][0]
        dog = union(*[p for p, r in lay if r == "idog"])
        cat = union(*[p for p, r in lay if r == "cat"])
        return [(union(diff(disc, dog, grow_(cat, 2.4)), cat), "badge")]
    return lay


def grow_(p, d):
    return union(p, stroke(p, 2 * d, cap="round", join="round"))


# ------------------------------------------------------------------ lockups
def lock_principal(knockout=False, desc=True, small=False):
    cap = cap_h(100)
    nm, w = name(100)
    lay = list(nm)
    top, bot = -cap, 0.0
    if desc:
        _, fd = _fonts()
        dsize = 20
        dcap = fd.cap / fd.upem * dsize
        base = cap * 0.62 + dcap
        lay.append((descriptor(dsize, 0, base), "text"))
        bot = base
    blk = bot - top
    src = emb.simple() if small else emblem_full()
    h = blk * (2.6 if desc else 2.9)
    sl, sw = place(src, h, 0, (top + bot) / 2 - h * 0.44)
    gap = cap * 0.7
    return sl + [(p.transform(1, 0, 0, 1, sw + gap, 0), r) for p, r in lay]


def lock_signature(knockout=False):
    return lock_principal(knockout, desc=False, small=True)


def lock_vertical(knockout=False):
    cap = cap_h(100)
    nm, w = name(100)
    _, fd = _fonts()
    dsize = 21
    dcap = fd.cap / fd.upem * dsize
    base = cap * 0.62 + dcap
    d = descriptor(dsize, 0, base, w, center=True)
    h = cap * 4.6
    sl, sw = place(emblem_full(), h, 0, -cap - cap * 0.55 - h)
    sl = [(p.transform(1, 0, 0, 1, w / 2 - sw / 2, 0), r) for p, r in sl]
    return sl + nm + [(d, "text")]


def lock_name(knockout=False):
    return name(100)[0]


def lock_emblem(knockout=False):
    return place(emblem_full(), 100, 0, 0)[0]


def lock_emblem_simple(knockout=False):
    return place(emb.simple(), 100, 0, 0)[0]


def lock_icon(knockout=False):
    return place(icon(knockout), 100, 0, 0)[0]


PIECES = [
    ("cp-selo", lambda ko=False: lock_seal(ko), 3, 2400, "Selo: o nome escrito na coleira. Assinatura principal"),
    ("cp-logo-horizontal", lock_principal, 16, 3000, "Emblema + nome + descritor"),
    ("cp-logo-assinatura", lock_signature, 14, 3000, "Emblema simplificado + nome"),
    ("cp-logo-vertical", lock_vertical, 18, 2400, "Emblema sobre o nome"),
    ("cp-logo-nome", lock_name, 12, 3000, "Só o nome"),
    ("cp-emblema", lock_emblem, 4, 2048, "Emblema completo"),
    ("cp-emblema-simplificado", lock_emblem_simple, 4, 1600, "Emblema para 32-96 px"),
    ("cp-icone", lock_icon, 2, 1024, "Ícone para até 32 px e favicon"),
]


def colorway(way):
    if way == "cor":
        return dict(text=NAVY, amp=TERRA, ring=NAVY, dog=NAVY, cat=TERRA, route=TERRA, tag=TERRA, badge=NAVY, idog=LINEN,
                    stext=LINEN, samp=TERRA), False
    if way == "negativo":
        return dict(text=LINEN, amp=TERRA, ring=LINEN, dog=LINEN, cat=TERRA, route=TERRA, tag=TERRA, badge=LINEN, idog=NAVY,
                    stext=NAVY, samp=TERRA), False
    if way == "cinza":
        return dict(text="#3B3B3B", amp="#8F8F8F", ring="#3B3B3B", dog="#3B3B3B", cat="#8F8F8F", route="#8F8F8F", tag="#8F8F8F",
                    badge="#3B3B3B", idog="#F2F2F2", stext="#F2F2F2", samp="#8F8F8F"), False
    one = {"preto": "#000000", "branco": "#FFFFFF", "uma-cor": NAVY}[way]
    return {k: one for k in ("text", "amp", "ring", "dog", "cat", "route", "tag", "badge", "idog", "stext", "samp")}, True


# ------------------------------------------------------------------ seal: the name written on the collar
def arc_text(fnt, s, size, cx, cy, r, center_deg, tracking=0.0, bottom=False):
    """Set s along a circle. Top text reads clockwise with the baseline on radius r;
    bottom text reads left to right, upright, with the baseline on radius r."""
    import uharfbuzz as hb
    from fontTools.pens.transformPen import TransformPen
    buf = hb.Buffer()
    buf.add_str(s)
    buf.guess_segment_properties()
    hb.shape(fnt.hbfont, buf, {"kern": True, "liga": True})
    sc = size / fnt.upem
    glyphs, x = [], 0.0
    n = len(buf.glyph_infos)
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        adv = pos.x_advance * sc
        glyphs.append((fnt.order[info.codepoint], x, adv, s[info.cluster]))
        x += adv + (tracking * size if i < n - 1 else 0)
    W = x
    parts = []
    for name, gx, adv, ch in glyphs:
        xc = gx + adv / 2 - W / 2
        th = math.radians(center_deg) + (-xc / r if bottom else xc / r)
        phi = th - math.pi / 2 if bottom else th + math.pi / 2
        px, py = cx + r * math.cos(th), cy + r * math.sin(th)
        c, sn = math.cos(phi), math.sin(phi)
        g = Path()
        pen = pathops.PathPen(g, glyphSet=fnt.gs)
        # glyph centred on its advance, baseline at 0, y flipped; then rotate and move onto the arc
        a, b, cc, d = sc * c, sc * sn, sc * sn, -sc * c
        e_ = px + (-adv / 2) * c
        f_ = py + (-adv / 2) * sn
        fnt.gs[name].draw(TransformPen(pen, (a, b, cc, d, e_, f_)))
        parts.append((pathops.simplify(g), ch))
    return parts


SEAL = dict(C=(50.0, 50.0), R_out=48.0, R_in=33.5, gap=2.2)


def seal(tag=True, text="Coleira & Passaporte"):
    g = SEAL
    C, R_out, R_in, gap = g["C"], g["R_out"], g["R_in"], g["gap"]
    rm = (R_out + R_in) / 2
    fn, fd = _fonts()
    strap = ring(C[0], C[1], R_out, R_in)
    # the name on the top of the collar
    ncap = 5.9
    nsize = ncap / (fn.cap / fn.upem)
    name_parts = arc_text(fn, text, nsize, C[0], C[1], rm - ncap / 2, -90, TRACK + 0.015)
    txt = union(*[p for p, ch in name_parts if ch != "&"])
    amp = union(*[p for p, ch in name_parts if ch == "&"])
    # the descriptor on the bottom
    dcap = 3.45
    dsize = dcap / (fd.cap / fd.upem)
    desc = union(*[p for p, _ in arc_text(fd, DESCRIPTOR, dsize, C[0], C[1], rm + dcap / 2, 90, 0.19, bottom=True)])
    # two collar holes mark the ends of the lines
    holes = union(*[circle(C[0] + rm * math.cos(math.radians(a)), C[1] + rm * math.sin(math.radians(a)), 1.25) for a in (180, 0)])
    strap = diff(strap, holes)
    # stitching just inside the outer edge
    dash = []
    for k in range(0, 360, 6):
        pth = Path()
        rr = R_out - 2.1
        pth.moveTo(C[0] + rr * math.cos(math.radians(k)), C[1] + rr * math.sin(math.radians(k)))
        arc_to(pth, C[0], C[1], rr, k, k + 3.0)
        dash.append(stroke(pth, 0.7, cap="round"))
    stitch = union(*dash)
    # inside: the emblem's pets and route, rescaled to the inner circle
    inner = emb.emblem(end="plane", tag_r=0.01)
    E = emb.E
    k = (R_in - gap + E["gap"]) / E["R_in"]
    inside = [(p.transform(k, 0, 0, k, C[0] - E["C"][0] * k, C[1] - E["C"][1] * k), r) for p, r in inner if r in ("dog", "cat", "route")]
    cut = union(txt, amp, desc, stitch)
    lay = [(diff(strap, cut), "ring"), (txt, "stext"), (amp, "samp"), (desc, "stext"), (stitch, "stext")]
    if tag:
        ring_c = (C[0], C[1] + R_out + 1.2)
        dring = ring(ring_c[0], ring_c[1], 4.2, 2.0)
        tg = circle(C[0], ring_c[1] + 4.2 + 9.0 - 1.0, 9.0)
        lay.append((diff(dring, emb.grow(tg, gap * 0.9)), "ring"))
        lay.append((tg, "tag"))
    return lay + inside


def lock_seal(knockout=False):
    lay = seal()
    if knockout:
        # one colour: the text and stitching are cut out of the strap
        lay = [(p, r) for p, r in lay if r not in ("stext", "samp")]
    return place(lay, 100, 0, 0)[0]


# ------------------------------------------------------------------ supporting elements
def el_route(knockout=False):
    """The flight path on its own, for layouts: a long dashed arc ending in the plane."""
    pr = Path()
    pr.moveTo(0, 30)
    pr.cubicTo(40, -4, 110, -8, 150, 12)
    rt = union(emb.dashed(pr, 4.2, 3.8, 2.6), emb.plane(162, 18.5, 19, 27))
    return [(rt, "route")]


def el_tag(knockout=False):
    """The ID tag hanging from its ring: bullet, stamp for documents, stickers."""
    ring_c = (50.0, 0.0)
    dring = ring(ring_c[0], ring_c[1], 4.2, 2.0)
    tg = circle(50.0, ring_c[1] + 4.2 + 9.0 - 1.0, 9.0)
    return [(diff(dring, emb.grow(tg, 2.0)), "ring"), (tg, "tag")]


SUPPORT = [
    ("cp-rota", el_route, 3, 2000, "Rota de voo para composições"),
    ("cp-plaquinha", el_tag, 2, 800, "Plaquinha de identificação"),
]
