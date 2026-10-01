"""Round 4, v2: dog ear as a single fold line; emblem composition fixed."""
import json, math, sys
sys.path.insert(0, '.')
from geo import *
from pets import path, grow
from pets3 import cat, cat_layers
from amp_r2 import arclen_points
from amp_r1 import sample

def dog(v=2):
    """Retriever-type head facing right. v=1 is the first, pointier muzzle."""
    top = [("M", 18, 100), ("C", 17, 90, 16, 82, 17, 74),
           ("C", 15, 70, 15, 64, 18, 58),                      # ear bump breaking the neck line
           ("C", 20, 44, 26, 32, 36, 26), ("C", 42, 22, 50, 21, 56, 22),
           ("C", 62, 23, 65, 27, 67, 31)]
    if v == 1:
        muzzle = [("C", 72, 33, 80, 35, 86, 37),
                  ("C", 90, 38, 93, 40, 93, 43), ("C", 93, 46, 91, 48, 88, 49),
                  ("C", 84, 50, 81, 50, 79, 51),
                  ("C", 78, 54, 75, 57, 71, 57),
                  ("C", 67, 58, 63, 61, 59, 62)]
    else:
        muzzle = [("C", 72, 33, 79, 34, 85, 35.2),              # bridge of the nose, nearly level
                  ("C", 88.5, 35.6, 91, 37, 91.2, 40), ("C", 91.4, 43, 90, 45, 87.6, 45.4),   # blunt nose
                  ("C", 87.8, 48, 86.4, 50.2, 83.5, 50.8),      # front of the upper lip
                  ("C", 80.5, 51.4, 77.5, 51.4, 75.5, 51.8),    # lip line
                  ("C", 74.5, 55, 71.5, 57, 67.5, 57.6),        # lower jaw
                  ("C", 63.5, 58.2, 60.5, 60, 58.5, 62)]        # chin to throat
    neck = [("C", 55, 63.5, 52, 66, 51, 71), ("C", 50, 80, 50, 90, 52, 100), ("Z",)]
    if v == 1:
        neck = [("C", 55, 63, 52, 66, 51, 71), ("C", 50, 80, 50, 90, 52, 100), ("Z",)]
    head = path(top + muzzle + neck)
    # front edge of the drop ear: from the top of the skull down to the ear tip
    ear_edge = Path()
    ear_edge.moveTo(49, 25.5)
    ear_edge.cubicTo(53, 34, 52, 50, 44, 62)
    ear_edge.cubicTo(38, 70, 30, 72, 21, 70)
    eye = path([("M", 60.5, 33), ("C", 62, 31.6, 64.6, 31.6, 66, 33), ("C", 64.6, 34.6, 62, 34.6, 60.5, 33), ("Z",)])
    return head, ear_edge, eye

def dog_layers(eye=True, line=2.1, v=2):
    h, edge, ey = dog(v)
    body = diff(h, stroke(edge, line, cap="round"))
    if eye:
        body = diff(body, ey)
    return [(body, "dog")]

def duo(eye=True, gap=2.6, cs=0.8, cdx=30, cdy=20):
    dl = dog_layers(eye)
    cl = cat_layers(eye)
    t = lambda p: inter(p.transform(cs, 0, 0, cs, cdx, cdy), rect(0, 0, 200, 100))
    cl = [(t(p), r) for p, r in cl]
    cut = grow(union(*[p for p, _ in cl]), gap)
    return [(diff(p, cut), r) for p, r in dl] + cl

def dashed(pth, dash=2.6, space=2.4, w=1.6):
    pts = sample(pth)
    L = sum(math.dist(pts[i-1], pts[i]) for i in range(1, len(pts)))
    segs, d = [], 0.0
    while d < L - 1:
        a = arclen_points(pts, [d, min(d + dash, L - 0.01)])
        pl = Path(); pl.moveTo(*a[0][0]); pl.lineTo(*a[1][0])
        segs.append(stroke(pl, w, cap="round"))
        d += dash + space
    return union(*segs)

def emblem(route=True, holes=True, stitch=True, gap=2.2, pet_h=0.9, R_out=44.0, R_in=36.0, tag_r=9.0):
    C = (50.0, 48.0)
    strap = ring(C[0], C[1], R_out, R_in)
    rm = (R_out + R_in) / 2
    pets = duo()
    ink = union(*[p for p, _ in pets]).bounds
    s = (R_in * pet_h) / (ink[3] - ink[1])
    ox = C[0] - (ink[0] + ink[2]) / 2 * s - 1.5
    oy = C[1] + R_in - ink[3] * s + 1.0
    inner = circle(C[0], C[1], R_in - gap)
    pets = [(inter(p.transform(s, 0, 0, s, ox, oy), inner), r) for p, r in pets]
    ring_c = (C[0], C[1] + R_out + 1.2)
    dring = ring(ring_c[0], ring_c[1], 4.2, 2.0)
    tag_c = (C[0], ring_c[1] + 4.2 + tag_r - 1.0)
    tag = circle(*tag_c, tag_r)
    dring = diff(dring, grow(tag, gap * 0.9))
    strap = diff(strap, grow(tag, gap))
    if holes:
        strap = diff(strap, union(*[circle(C[0] + rm * math.cos(math.radians(a)), C[1] + rm * math.sin(math.radians(a)), 1.3) for a in (122, 131, 140)]))
    if stitch:
        dash = []
        for k in range(150, 390, 7):
            a0 = k
            pth = Path(); pth.moveTo(C[0] + rm * math.cos(math.radians(a0)), C[1] + rm * math.sin(math.radians(a0)))
            arc_to(pth, C[0], C[1], rm, a0, a0 + 3.6)
            dash.append(stroke(pth, 0.85, cap="round"))
        strap = diff(strap, union(*dash))
    lay = [(strap, "ring"), (dring, "ring")] + pets + [(tag, "tag")]
    if route:
        pr = Path()
        pr.moveTo(C[0] - 24, C[1] - 12)
        pr.cubicTo(C[0] - 14, C[1] - 30, C[0] + 8, C[1] - 32, C[0] + 20, C[1] - 20)
        rt = union(dashed(pr, 2.4, 2.2, 1.5), circle(C[0] + 23, C[1] - 17, 2.4))
        rt = inter(rt, inner)
        lay = [(diff(p, grow(rt, 1.3)) if r in ("dog", "cat") else p, r) for p, r in lay] + [(rt, "tag")]
    return lay

if __name__ == "__main__":
    NAVY, TERRA, LINEN = "#1B2B44", "#C8694A", "#F4EFE6"
    def sv(l, bg, m, pad=4):
        ink = union(*[p for p, _ in l]).bounds
        body = "".join(f'<path fill="{m[r]}" d="{to_d(p)}"/>' for p, r in l)
        return f'<svg viewBox="{ink[0]-pad} {ink[1]-pad} {ink[2]-ink[0]+2*pad} {ink[3]-ink[1]+2*pad}" style="display:block;width:100%;background:{bg}">{body}</svg>'
    M = {"dog": NAVY, "cat": TERRA, "ring": NAVY, "tag": TERRA}
    Mneg = {"dog": LINEN, "cat": TERRA, "ring": LINEN, "tag": TERRA}
    Mblk = {k: "#000" for k in M}
    items = [("dupla", duo(), M), ("emblema", emblem(), M), ("emblema, pets maiores", emblem(pet_h=1.0), M), ("negativo", emblem(), Mneg), ("preto", emblem(), Mblk)]
    cells = "".join(f"<div style='background:#fff;padding:6px;font:12px sans-serif'>{n}{sv(l, NAVY if n=='negativo' else LINEN, m)}<div style='display:flex;gap:6px;align-items:end;margin-top:4px'><div style='width:64px'>{sv(l, '#fff', Mblk)}</div><div style='width:40px'>{sv(l, '#fff', M)}</div><div style='width:24px'>{sv(l, '#fff', M)}</div></div></div>" for n, l, m in items)
    open("pets4.html", "w").write(f"<html><body style='margin:0;background:#ccc'><div style='display:grid;grid-template-columns:repeat(5,1fr);gap:8px;padding:8px'>{cells}</div></body></html>")
    json.dump([{"html": "pets4.html", "png": "pets4.png", "width": 1400, "height": 430}], open("mpets4.json", "w"))
