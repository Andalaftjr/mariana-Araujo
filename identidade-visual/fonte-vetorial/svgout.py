import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from geo import *  # noqa
from lockups import PALETTES, ink_bounds

TITLE = "Coleira &amp; Passaporte"


def colorway(d, way):
    P = [h for _, h, _ in PALETTES[d]]
    primary, accent, light = P[0], P[1], P[2]
    if way == "cor":
        return dict(text=primary, sym=primary, accent=accent, badge=primary, badge_fg=light, badge_acc=accent), False
    if way == "negativo":
        return dict(text=light, sym=light, accent=accent, badge=light, badge_fg=primary, badge_acc=accent), False
    if way == "cinza":
        return dict(text="#3B3B3B", sym="#3B3B3B", accent="#8F8F8F", badge="#3B3B3B", badge_fg="#F2F2F2", badge_acc="#8F8F8F"), False
    one = {"preto": "#000000", "branco": "#FFFFFF", "uma-cor": primary}[way]
    return dict(text=one, sym=one, accent=one, badge=one, badge_fg=None, badge_acc=None), True


def svg_string(layers, cols, margin=0.0, bg=None, vb=None, extra=""):
    if vb is None:
        x0, y0, x1, y1 = ink_bounds(layers)
        vb = (x0 - margin, y0 - margin, (x1 - x0) + 2 * margin, (y1 - y0) + 2 * margin)
    x, y, w, h = vb
    groups = {}
    order = []
    for p, role in layers:
        c = cols.get(role)
        if c is None:
            continue
        if c not in groups:
            groups[c] = []
            order.append(c)
        groups[c].append(p)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.2f} {y:.2f} {w:.2f} {h:.2f}" role="img" aria-label="{TITLE}"><title>{TITLE}</title>']
    if bg:
        out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{bg}"/>')
    # paint in layer order, one path per contiguous colour run
    runs = []
    for p, role in layers:
        c = cols.get(role)
        if c is None:
            continue
        if runs and runs[-1][0] == c:
            runs[-1][1].append(p)
        else:
            runs.append((c, [p]))
    for c, ps in runs:
        d = " ".join(to_d(p) for p in ps)
        out.append(f'<path fill="{c}" d="{d}"/>')
    out.append(extra)
    out.append("</svg>")
    return "".join(out)
