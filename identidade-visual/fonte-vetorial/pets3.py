"""Round 4: refined pets + the collar emblem."""
import json, math, sys
sys.path.insert(0, '.')
from geo import *
from pets import path, grow, fit, svg, img

def dog():
    head = path([
        ("M", 16, 100), ("C", 15, 88, 15, 78, 18, 68),
        ("C", 20, 50, 26, 34, 36, 27), ("C", 42, 23, 50, 21, 56, 22),
        ("C", 62, 23, 65, 27, 67, 31),
        ("C", 72, 33, 80, 35, 86, 37),
        ("C", 90, 38, 93, 40, 93, 43), ("C", 93, 46, 91, 48, 88, 49),
        ("C", 84, 50, 81, 50, 79, 51),
        ("C", 78, 54, 75, 57, 71, 57),
        ("C", 67, 58, 63, 61, 59, 62),
        ("C", 55, 63, 52, 66, 51, 71),
        ("C", 50, 80, 50, 90, 52, 100), ("Z",)])
    ear = path([
        ("M", 39, 27), ("C", 43, 25, 47, 25, 50, 27),
        ("C", 51, 33, 50, 42, 47, 50), ("C", 45, 55, 42, 58, 39, 58),
        ("C", 35, 57, 33, 52, 33, 46), ("C", 33, 39, 35, 31, 39, 27), ("Z",)])
    eye = path([("M", 60.5, 33), ("C", 62, 31.6, 64.6, 31.6, 66, 33), ("C", 64.6, 34.6, 62, 34.6, 60.5, 33), ("Z",)])
    return head, ear, eye

def cat():
    head = path([
        ("M", 22, 100), ("C", 21, 88, 21, 76, 23, 66),
        ("C", 23, 57, 25, 50, 30, 45),
        ("L", 33.5, 25), ("C", 34, 22.5, 36.5, 22, 37.5, 24),
        ("L", 46, 36),
        ("C", 54, 34, 61, 37, 65, 43),
        ("C", 67, 45, 70, 46, 72.5, 47.5), ("C", 74, 48.5, 74, 51, 72, 52),
        ("C", 71, 54, 69, 55.5, 67, 56),
        ("C", 66, 59, 62, 61, 57, 61.5),
        ("C", 52, 63, 49, 67, 48.5, 74),
        ("C", 48, 84, 49, 92, 50, 100), ("Z",)])
    far_ear = path([("M", 41, 36), ("L", 46.5, 21.5), ("C", 47.5, 19.5, 50, 19.8, 50.5, 22), ("L", 53, 35), ("Z",)])
    eye = path([("M", 55.5, 44.5), ("C", 57, 43, 59.6, 43, 61, 44.5), ("C", 59.6, 46, 57, 46, 55.5, 44.5), ("Z",)])
    return head, far_ear, eye

def dog_layers(eye=True, gap=2.2):
    h, e, ey = dog()
    front = diff(h, grow(e, gap))
    lay = [(front, "dog"), (inter(e, h), "dog")]
    return [(diff(p, ey), r) for p, r in lay] if eye else lay

def cat_layers(eye=True, gap=2.0):
    h, fe, ey = cat()
    far = diff(fe, grow(h, gap))
    body = diff(h, ey) if eye else h
    return [(far, "cat"), (body, "cat")]

def duo(eye=True, gap=2.6, cs=0.8, cdx=30, cdy=20):
    dl = dog_layers(eye)
    cl = cat_layers(eye)
    t = lambda p: inter(p.transform(cs, 0, 0, cs, cdx, cdy), rect(0, 0, 200, 100))
    cl = [(t(p), r) for p, r in cl]
    cut = grow(union(*[p for p, _ in cl]), gap)
    return [(diff(p, cut), r) for p, r in dl] + cl

def emblem(route=True, holes=True, gap=2.2):
    """The collar as a round frame, the pets inside looking ahead, the tag hanging below."""
    C = (50, 48)
    R_out, R_in = 44, 36.5
    strap = ring(C[0], C[1], R_out, R_in)
    # stitching: dashed line in the middle of the strap
    lay = []
    # pets, cropped by the inner circle
    pets = duo()
    ink = union(*[p for p, _ in pets]).bounds
    s = (R_in * 2 * 0.98) / (ink[3] - ink[1])
    ox = C[0] - (ink[0] + ink[2]) / 2 * s - 4
    oy = C[1] + R_in - ink[3] * s + 0.5
    inner = circle(C[0], C[1], R_in - gap)
    pets = [(inter(p.transform(s, 0, 0, s, ox, oy), inner), r) for p, r in pets]
    # buckle at the bottom of the collar: a frame across the strap
    bw, bh, t = 12, R_out - R_in + 7, 2.2
    bx, by = C[0] - 14, C[1] + (R_out + R_in) / 2
    ang = math.atan2(by - C[1], bx - C[0])
    # D-ring + tag at the bottom centre
    ring_c = (C[0], C[1] + R_out + 1.5)
    dring = ring(ring_c[0], ring_c[1], 4.4, 2.1)
    tag_c = (C[0], ring_c[1] + 4.4 + 8.5)
    tag = circle(*tag_c, 9.5)
    dring = diff(dring, grow(tag, gap * 0.9))
    strap = diff(strap, grow(tag, gap))
    if holes:
        hs = [circle(C[0] + (R_out + R_in) / 2 * math.cos(math.radians(a)), C[1] + (R_out + R_in) / 2 * math.sin(math.radians(a)), 1.35) for a in (118, 128, 138)]
        strap = diff(strap, union(*hs))
    # stitching dashes along the upper part of the strap
    rm = (R_out + R_in) / 2
    dashes = []
    for k in range(-80, 20, 8):
        a0, a1 = math.radians(180 + k), math.radians(180 + k + 4.5)
        pth = Path(); pth.moveTo(C[0] + rm * math.cos(a0), C[1] + rm * math.sin(a0))
        arc_to(pth, C[0], C[1], rm, 180 + k, 180 + k + 4.5)
        dashes.append(stroke(pth, 0.9, cap="round"))
    strap = diff(strap, union(*dashes))
    lay = [(strap, "ring"), (dring, "ring")] + pets + [(tag, "tag")]
    if route:
        # dashed flight path over the pets, ending at the destination point
        pr = Path(); pr.moveTo(C[0] - 20, C[1] - 22)
        pr.cubicTo(C[0] - 6, C[1] - 34, C[0] + 14, C[1] - 32, C[0] + 24, C[1] - 18)
        segs = []
        from amp_r2 import arclen_points
        from amp_r1 import sample
        pts = sample(pr)
        L = 0
        for i in range(1, len(pts)): L += math.dist(pts[i-1], pts[i])
        d = 0
        while d < L - 6:
            a = arclen_points(pts, [d, min(d + 2.6, L)])
            pl = Path(); pl.moveTo(*a[0][0]); pl.lineTo(*a[1][0])
            segs.append(stroke(pl, 1.6, cap="round"))
            d += 5
        dest = circle(C[0] + 25.5, C[1] - 16.5, 2.6)
        rt = union(*segs, dest)
        lay = [(diff(p, grow(rt, 1.4)) if r in ("dog", "cat") else p, r) for p, r in lay] + [(rt, "tag")]
    return lay

if __name__ == "__main__":
    NAVY, TERRA, LINEN = "#1B2B44", "#C8694A", "#F4EFE6"
    def col(l, m):
        return "".join(f'<path fill="{m[r]}" d="{to_d(p)}"/>' for p, r in l)
    def sv(l, bg, m, pad=4):
        ink = union(*[p for p, _ in l]).bounds
        return f'<svg viewBox="{ink[0]-pad} {ink[1]-pad} {ink[2]-ink[0]+2*pad} {ink[3]-ink[1]+2*pad}" style="display:block;width:100%;background:{bg}">{col(l, m)}</svg>'
    M = {"dog": NAVY, "cat": TERRA, "ring": NAVY, "tag": TERRA}
    Mneg = {"dog": LINEN, "cat": TERRA, "ring": LINEN, "tag": TERRA}
    Mblk = {k: "#000" for k in M}
    items = [("dupla", duo(), M), ("emblema", emblem(), M), ("emblema sem rota", emblem(route=False), M), ("emblema negativo", emblem(), Mneg), ("emblema preto", emblem(), Mblk)]
    cells = "".join(f"<div style='background:#fff;padding:6px;font:12px sans-serif'>{n}{sv(l, NAVY if 'negativo' in n else LINEN, m)}<div style='display:flex;gap:6px;align-items:end;margin-top:4px'><div style='width:64px'>{sv(l, '#fff', Mblk)}</div><div style='width:40px'>{sv(l, '#fff', M)}</div><div style='width:24px'>{sv(l, '#fff', M)}</div></div></div>" for n, l, m in items)
    open("pets3.html", "w").write(f"<html><body style='margin:0;background:#ccc'><div style='display:grid;grid-template-columns:repeat(5,1fr);gap:8px;padding:8px'>{cells}</div></body></html>")
    json.dump([{"html": "pets3.html", "png": "pets3.png", "width": 1400, "height": 420}], open("mpets3.json", "w"))
