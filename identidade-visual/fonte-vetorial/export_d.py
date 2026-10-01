"""Export direction D · Dobra (now history: historico/dobra) + the round-3 alternates.

Writes outlined SVG, transparent PNG and vector PDF into ../identidade-visual.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *  # noqa
import d
from svgout import svg_string

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WAYS = ["cor", "negativo", "preto", "branco", "cinza", "uma-cor"]
jobs = []


def write(rel, svg):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(svg)
    return path


def export(folder, name, builder, margin, png_w, ways=WAYS, pdf=True):
    for way in ways:
        cols, ko = d.colorway(way)
        svg = svg_string(builder(ko), cols, margin)
        sp = write(f"{folder}/svg/{name}_{way}.svg", svg)
        pp = os.path.join(OUT, f"{folder}/png/{name}_{way}.png")
        os.makedirs(os.path.dirname(pp), exist_ok=True)
        job = {"svg": sp, "png": pp, "width": png_w}
        if pdf:
            fp = os.path.join(OUT, f"{folder}/pdf/{name}_{way}.pdf")
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            job.update(pdf=fp, pdfWidth=600)
        jobs.append(job)


def square(bg, fg, facet_c, acc, fill, facet=True, rx=None):
    lay = [(p, r) for p, r in d.badge(50, 50, 100, fill=fill, facet=facet) if r != "badge"]
    svg = svg_string(lay, {"badge_fg": fg, "badge_facet": facet_c, "badge_acc": acc}, vb=(0, 0, 100, 100), bg=bg)
    if rx:
        svg = svg.replace('<rect x="0.00" y="0.00" width="100.00" height="100.00"', f'<rect x="0" y="0" width="100" height="100" rx="{rx}"')
    return svg


def main():
    F = "historico/dobra"
    for name, builder, margin, png_w, _ in d.PIECES:
        export(F, name, builder, margin, png_w)
    for name, builder, margin, png_w, _ in d.SUPPORT:
        export(F + "/elementos", name, builder, margin, png_w, ways=["cor", "negativo", "preto", "branco"])
    av = {
        "cp-avatar_azul": square(d.NAVY, d.LINEN, d.FACET_NEG, d.TERRA, 0.66),
        "cp-avatar_linho": square(d.LINEN, d.NAVY, d.FACET, d.TERRA, 0.66),
    }
    for n, s in av.items():
        sp = write(f"{F}/avatar/{n}.svg", s)
        for px in (1080, 640):
            jobs.append({"svg": sp, "png": os.path.join(OUT, f"{F}/avatar/{n}_{px}.png"), "width": px})
    fav = square(d.NAVY, d.LINEN, d.LINEN, d.TERRA, 0.78, facet=False, rx=22)
    sp = write(f"{F}/favicon/favicon.svg", fav)
    for px, n in ((16, "favicon-16"), (32, "favicon-32"), (48, "favicon-48"), (180, "apple-touch-icon-180"),
                  (192, "icon-192"), (512, "icon-512")):
        jobs.append({"svg": sp, "png": os.path.join(OUT, f"{F}/favicon/{n}.png"), "width": px})

    # round-3 alternates (concept studies, symbol only)
    try:
        import alternativas
        alts = {"janela": alternativas.janela, "retrato": alternativas.retrato}
        for n, fn in alts.items():
            for way, cols in (("cor", {"primary": d.NAVY, "accent": d.TERRA}), ("preto", {"primary": "#000", "accent": None})):
                svg = svg_string(fn(), cols, 3)
                sp = write(f"exploracao/rodada-3/{n}_{way}.svg", svg)
                jobs.append({"svg": sp, "png": os.path.join(OUT, f"exploracao/rodada-3/{n}_{way}.png"), "width": 1024})
    except ImportError:
        pass

    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(jobs, open(os.path.join(here, "export_jobs.json"), "w"))
    print(len(jobs), "render jobs")


if __name__ == "__main__":
    main()
