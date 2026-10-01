"""Export direction E, round 2 (E2) · Companheiros de viagem (final kit).

Writes outlined SVG, transparent PNG and vector PDF into ../identidade-visual.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *  # noqa
import e2 as e
import emb2
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
        cols, ko = e.colorway(way)
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


def square(way, bg, rx=None):
    """Avatar: the collar without the tag, filling the circle a platform crops to."""
    cols, _ = e.colorway(way)
    lay = e.place(e.emblem_no_tag(), 84, 8, 8)[0]
    svg = svg_string(lay, cols, vb=(0, 0, 100, 100), bg=bg)
    if rx:
        svg = svg.replace('<rect x="0.00" y="0.00" width="100.00" height="100.00"', f'<rect x="0" y="0" width="100" height="100" rx="{rx}"')
    return svg


def favicon():
    cols, _ = e.colorway("cor")
    lay = e.place(e.icon(), 96, 2, 2)[0]
    return svg_string(lay, cols, vb=(0, 0, 100, 100))


def main():
    F = "final"
    for name, builder, margin, png_w, _ in e.PIECES:
        export(F, name, builder, margin, png_w)
    for name, builder, margin, png_w, _ in e.SUPPORT:
        export(F + "/elementos", name, builder, margin, png_w, ways=["cor", "negativo", "preto", "branco"])
    av = {"cp-avatar_azul": square("negativo", e.NAVY), "cp-avatar_linho": square("cor", e.LINEN)}
    for n, s in av.items():
        sp = write(f"{F}/avatar/{n}.svg", s)
        for px in (1080, 640):
            jobs.append({"svg": sp, "png": os.path.join(OUT, f"{F}/avatar/{n}_{px}.png"), "width": px})
    sp = write(f"{F}/favicon/favicon.svg", favicon())
    for px, n in ((16, "favicon-16"), (32, "favicon-32"), (48, "favicon-48"), (180, "apple-touch-icon-180"),
                  (192, "icon-192"), (512, "icon-512")):
        jobs.append({"svg": sp, "png": os.path.join(OUT, f"{F}/favicon/{n}.png"), "width": px})
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(jobs, open(os.path.join(here, "export_jobs.json"), "w"))
    print(len(jobs), "render jobs")


def ico():
    """favicon.ico from the rendered 16/32/48 px PNGs (run after render.js)."""
    from PIL import Image
    d = os.path.join(OUT, "final/favicon")
    big = Image.open(os.path.join(d, "favicon-48.png"))
    big.save(os.path.join(d, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)],
             append_images=[Image.open(os.path.join(d, f"favicon-{s}.png")) for s in (16, 32)])


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "ico":
        ico()
    else:
        main()
