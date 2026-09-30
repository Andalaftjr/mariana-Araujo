# Fonte vetorial

Código que constrói todos os logotipos de `../final` e `../exploracao`.
Os símbolos são desenhados com círculos, tangentes e retas; o nome é convertido
em curvas a partir da fonte (Plus Jakarta Sans na r1; Outfit, Manrope e Fraunces nas explorações). O resultado são SVG e PDF
só com contornos preenchidos, sem traço e sem fonte embutida.

| Arquivo | O que faz |
| --- | --- |
| `geo.py` | Primitivas (círculo, polígono arredondado, tangentes entre círculos), booleanas e conversão de texto em curvas |
| `sym.py` | Símbolos das três direções (r0); `AMP` guarda a geometria do & da r0 |
| `amp_r1.py` | O & da r1: nó entrelaçado, pé reto, tag encaixada e versão reduzida (`R1`, `R1_SMALL`) |
| `r1.py` | Logotipo e assinaturas da r1 (Plus Jakarta Sans + &) |
| `amp_r2.py` | O & da r2 desenhado como coleira: fivela, argola, plaquinha, furos; `R2`, `R2_TEXT` (médio), `R2_SMALL` (reduzido) |
| `r2.py` | Logotipo, assinaturas, elementos de apoio (faixa-coleira, plaquinha) e a lista de peças exportadas |
| `typo.py` | Wordmark “Coleira & Passaporte” com o & próprio da marca |
| `lockups.py` | Paletas e montagem das assinaturas (horizontal, vertical, empilhada, selo) |
| `svgout.py` | Versões de cor (cor, negativo, preto, branco, cinza, uma cor) e escrita do SVG |
| `export.py` | Gera `final/` (r2) e `exploracao/` (r0) e a lista de renderização |
| `render.js` | Renderiza PNG transparente e PDF vetorial com Chromium (Playwright) |

## Regerar os arquivos

```bash
pip install fonttools brotli uharfbuzz skia-pathops
mkdir -p fonts && cd fonts
for f in plus-jakarta-sans outfit manrope fraunces; do npm pack @fontsource/$f && mkdir -p $f && tar xzf fontsource-$f-*.tgz -C $f; done
cd ..
python3 export.py            # escreve SVG em ../final e ../exploracao
node render.js export_jobs.json   # PNG + PDF (precisa do pacote playwright)
```

As fontes são licenciadas sob a SIL Open Font License.
