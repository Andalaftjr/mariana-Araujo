# Fonte vetorial

Código que constrói todos os logotipos de `../final` e `../exploracao`.
Os símbolos são desenhados com círculos, tangentes e retas; o nome é convertido
em curvas a partir da fonte (Outfit, Manrope, Fraunces). O resultado são SVG e PDF
só com contornos preenchidos, sem traço e sem fonte embutida.

| Arquivo | O que faz |
| --- | --- |
| `geo.py` | Primitivas (círculo, polígono arredondado, tangentes entre círculos), booleanas e conversão de texto em curvas |
| `sym.py` | Símbolos das três direções; `AMP` guarda a geometria do & (direção C) |
| `typo.py` | Wordmark “Coleira & Passaporte” com o & próprio da marca |
| `lockups.py` | Paletas e montagem das assinaturas (horizontal, vertical, empilhada, selo) |
| `svgout.py` | Versões de cor (cor, negativo, preto, branco, cinza, uma cor) e escrita do SVG |
| `export.py` | Gera todos os arquivos e a lista de renderização |
| `render.js` | Renderiza PNG transparente e PDF vetorial com Chromium (Playwright) |

## Regerar os arquivos

```bash
pip install fonttools brotli uharfbuzz skia-pathops
mkdir -p fonts && cd fonts
for f in outfit manrope fraunces; do npm pack @fontsource/$f && mkdir -p $f && tar xzf fontsource-$f-*.tgz -C $f; done
cd ..
python3 export.py            # escreve SVG em ../final e ../exploracao
node render.js export_jobs.json   # PNG + PDF (precisa do pacote playwright)
```

As fontes são licenciadas sob a SIL Open Font License.
