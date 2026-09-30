"""Export the final identity kit (direction C, "Elo") + exploration files (A, B).

Writes SVG (outlined, no font dependency), transparent PNG (via Chromium) and
vector PDF into ../identidade-visual.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *  # noqa
from lockups import (PALETTES, badge_layers, ink_bounds, lock_badge, lock_horizontal, lock_stacked,
                     lock_symbol, lock_vertical, lock_wordmark)
from svgout import colorway, svg_string
from sym import sym_amp, sym_amp_small

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WAYS = ["cor", "negativo", "preto", "branco", "cinza", "uma-cor"]
jobs = []
index = {}


def write(rel, svg):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(svg)
    return path


def export_lockup(folder, name, builder, margin, png_w, pdf=True, ways=WAYS, d="C"):
    for way in ways:
        cols, ko = colorway(d, way)
        lay = builder(ko)
        svg = svg_string(lay, cols, margin)
        base = f"{name}_{way}"
        sp = write(f"{folder}/svg/{base}.svg", svg)
        pp = os.path.join(OUT, f"{folder}/png/{base}.png")
        os.makedirs(os.path.dirname(pp), exist_ok=True)
        job = {"svg": sp, "png": pp, "width": png_w}
        if pdf:
            fp = os.path.join(OUT, f"{folder}/pdf/{base}.pdf")
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            job["pdf"] = fp
            job["pdfWidth"] = 600
        jobs.append(job)
        index.setdefault(name, {})[way] = svg


def square_symbol(fn, bg, fg, acc, fill=0.66, size=100):
    lay = fn()
    ink = union(*[p for p, _ in lay]).bounds
    h = size * fill
    s = h / (ink[3] - ink[1])
    w = (ink[2] - ink[0]) * s
    out = [(p.transform(s, 0, 0, s, size / 2 - w / 2 - ink[0] * s - size * 0.012, size / 2 - h / 2 - ink[1] * s + size * 0.008),
            "a" if r == "primary" else "b") for p, r in lay]
    return svg_string(out, {"a": fg, "b": acc}, vb=(0, 0, size, size), bg=bg)


def main():
    F = "final"
    # 1. principal: selo + nome + descritor (horizontal)
    export_lockup(F, "cp-logo-principal-horizontal", lambda ko: lock_horizontal("C", True, knockout=ko), 18, 3000)
    # 2. horizontal assinatura: nome em linha (o & do nome é o símbolo)
    export_lockup(F, "cp-logo-horizontal-assinatura", lambda ko: lock_wordmark("C"), 18, 3000)
    # 3. vertical: selo sobre nome + descritor
    export_lockup(F, "cp-logo-vertical", lambda ko: lock_vertical("C", True, knockout=ko), 20, 2400)
    # 4. empilhada: Coleira / & / Passaporte
    export_lockup(F, "cp-logo-empilhado", lambda ko: lock_stacked("C", True), 20, 2000)
    # 5. símbolo isolado (& livre) e selo
    export_lockup(F, "cp-simbolo", lambda ko: lock_symbol("C"), 5, 2048)
    export_lockup(F, "cp-selo", lambda ko: lock_badge(ko), 2, 2048)

    # avatares (quadrados, com fundo) + favicon
    P = {n: h for n, h, _ in PALETTES["C"]}
    navy, terra, linen = P["Azul Passaporte"], P["Terracota Tag"], P["Linho"]
    av = {
        "cp-avatar_azul": square_symbol(sym_amp_small, navy, linen, terra, 0.58),
        "cp-avatar_linho": square_symbol(sym_amp_small, linen, navy, terra, 0.58),
    }
    for n, s in av.items():
        sp = write(f"{F}/avatar/{n}.svg", s)
        for px in (1080, 640):
            jobs.append({"svg": sp, "png": os.path.join(OUT, f"{F}/avatar/{n}_{px}.png"), "width": px})
        index[n] = s
    fav = square_symbol(sym_amp_small, navy, linen, terra, 0.7)
    # rounded-square favicon
    fav = fav.replace('<rect x="0.00" y="0.00" width="100.00" height="100.00"', '<rect x="0" y="0" width="100" height="100" rx="22"')
    sp = write(f"{F}/favicon/favicon.svg", fav)
    for px, n in ((16, "favicon-16"), (32, "favicon-32"), (48, "favicon-48"), (180, "apple-touch-icon-180"),
                  (192, "icon-192"), (512, "icon-512")):
        jobs.append({"svg": sp, "png": os.path.join(OUT, f"{F}/favicon/{n}.png"), "width": px})
    index["favicon"] = fav

    # exploração: A e B (e C) — símbolo, horizontal, vertical em cor + preto
    for d, folder in (("A", "exploracao/A-tag-de-embarque"), ("B", "exploracao/B-rota-da-coleira"),
                      ("C", "exploracao/C-elo")):
        export_lockup(folder, f"{d}-simbolo", lambda ko, d=d: lock_symbol(d), 5, 1200, pdf=False,
                      ways=["cor", "preto", "negativo"], d=d)
        export_lockup(folder, f"{d}-horizontal", lambda ko, d=d: lock_horizontal(d, True, knockout=ko), 18, 2400,
                      pdf=False, ways=["cor", "preto", "negativo"], d=d)
        export_lockup(folder, f"{d}-vertical", lambda ko, d=d: lock_vertical(d, True, knockout=ko), 20, 1600,
                      pdf=False, ways=["cor", "preto", "negativo"], d=d)

    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(jobs, open(os.path.join(here, "export_jobs.json"), "w"))
    json.dump(index, open(os.path.join(here, "svg_index.json"), "w"))
    print(len(jobs), "render jobs")


if __name__ == "__main__":
    main()
