"""Hand-drawn (coded) pet profiles for round 4. Silhouettes facing right, grid 100 x 100."""
import json
import sys
import urllib.parse

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from geo import *  # noqa


def path(cmds):
    p = Path()
    for c in cmds:
        if c[0] == "M":
            p.moveTo(c[1], c[2])
        elif c[0] == "L":
            p.lineTo(c[1], c[2])
        elif c[0] == "C":
            p.cubicTo(*c[1:])
        elif c[0] == "Q":
            p.quadTo(*c[1:])
        elif c[0] == "Z":
            p.close()
    return pathops.simplify(p)


import pathops  # noqa: E402


def grow(p, d):
    return union(p, stroke(p, 2 * d, cap="round", join="round"))


def dog_profile():
    """Friendly retriever-type head and neck, facing right. Returns (head, ear)."""
    head = path([
        ("M", 18, 100),
        ("C", 17, 84, 17, 70, 20, 58),          # back of neck
        ("C", 23, 44, 28, 33, 38, 26),          # back of skull
        ("C", 46, 20, 56, 20, 62, 25),          # crown
        ("C", 66, 28, 67, 32, 69, 35),          # forehead to stop
        ("C", 75, 38, 83, 40, 88, 43),          # bridge of the nose
        ("C", 92, 45, 93, 50, 90, 53),          # nose tip
        ("C", 86, 57, 80, 58, 75, 58),          # upper lip
        ("C", 73, 61, 70, 63, 66, 64),          # lower jaw
        ("C", 62, 66, 58, 69, 56, 74),          # throat
        ("C", 54, 82, 55, 92, 57, 100),         # front of neck / chest
        ("Z",),
    ])
    ear = path([
        ("M", 44, 30),
        ("C", 38, 34, 33, 44, 32, 55),
        ("C", 31, 63, 36, 68, 42, 66),
        ("C", 48, 63, 51, 52, 52, 42),
        ("C", 52, 36, 49, 31, 44, 30),
        ("Z",),
    ])
    return head, ear


def cat_profile():
    """Cat head and neck, facing right, pointed ear."""
    head = path([
        ("M", 24, 100),
        ("C", 22, 84, 21, 70, 24, 58),          # back of neck
        ("C", 26, 50, 28, 45, 31, 41),          # back of skull
        ("L", 33, 18),                          # back edge of the ear up to the tip
        ("C", 34, 16, 36, 16, 37, 18),          # ear tip
        ("L", 49, 33),                          # front edge of the ear
        ("C", 55, 33, 61, 36, 64, 41),          # forehead
        ("C", 66, 44, 67, 46, 70, 48),          # nose bridge
        ("C", 73, 50, 73, 54, 70, 55),          # nose
        ("C", 67, 57, 66, 60, 63, 61),          # mouth
        ("C", 60, 63, 55, 64, 52, 67),          # chin / throat
        ("C", 50, 76, 50, 88, 52, 100),         # chest
        ("Z",),
    ])
    return head


def duo(gap=2.6, dog_scale=1.0, cat_scale=0.78, cat_dx=34, cat_dy=22):
    """Dog behind, cat in front, both looking forward (to the right)."""
    dh, de = dog_profile()
    ch = cat_profile()
    ch = ch.transform(cat_scale, 0, 0, cat_scale, cat_dx, cat_dy)
    ch = inter(ch, rect(0, 0, 200, 100))
    dog = diff(dh, grow(ch, gap))
    ear_line = diff(stroke(de, 2.2), grow(ch, gap))
    dog = diff(dog, ear_line)
    return [(dog, "primary"), (ch, "accent")]


def fit(layers, pad=6):
    ink = union(*[p for p, _ in layers]).bounds
    s = (100 - 2 * pad) / max(ink[2] - ink[0], ink[3] - ink[1])
    w, h = (ink[2] - ink[0]) * s, (ink[3] - ink[1]) * s
    return [(p.transform(s, 0, 0, s, 50 - w / 2 - ink[0] * s, 50 - h / 2 - ink[1] * s), r) for p, r in layers]


def svg(layers, bg, fg, acc):
    body = "".join(f'<path fill="{fg if r == "primary" else acc}" d="{to_d(p)}"/>' for p, r in layers)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="{bg}"/>{body}</svg>'


def img(s, px):
    return f"<img width={px} height={px} src='data:image/svg+xml;utf8,{urllib.parse.quote(s)}'>"


if __name__ == "__main__":
    NAVY, TERRA, LINEN = "#1B2B44", "#C8694A", "#F4EFE6"
    dh, de = dog_profile()
    items = [("cão", [(diff(dh, stroke(de, 2.2)), "primary")]), ("gato", [(cat_profile(), "primary")]), ("dupla", duo())]
    cells = "".join(f"<div style='background:#fff;padding:6px;font:12px sans-serif'>{n}<br>{img(svg(fit(l), LINEN, NAVY, TERRA), 300)} {img(svg(fit(l), '#fff', '#000', '#000'), 48)}</div>" for n, l in items)
    open("pets.html", "w").write(f"<html><body style='margin:0;background:#ccc'><div style='display:flex;gap:8px;padding:8px'>{cells}</div></body></html>")
    json.dump([{"html": "pets.html", "png": "pets.png", "width": 1100, "height": 360}], open("mpets.json", "w"))
