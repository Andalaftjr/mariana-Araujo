# Fonte vetorial

Código que constrói todos os logotipos de `../final` e `../exploracao`.
Os símbolos são desenhados com círculos, tangentes, retas e curvas; o nome é convertido
em curvas a partir da fonte (Fraunces nas direções Companheiros de viagem e Dobra; Plus Jakarta Sans, Outfit e Manrope nas anteriores). Na direção atual, os pets são desenhados em curvas de Bézier, à mão, no código. O resultado são SVG e PDF
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
| `pets.py`, `pets3.py`, `pets4.py` | Os perfis do cão e do gato (curvas), o respiro entre eles e utilitários de desenho |
| `emb.py` | O emblema da direção atual: coleira (alça, costura, furos, argola, plaquinha), pets, rota e avião; versões simplificada e ícone |
| `e.py` | Assinaturas, selo com o nome em arco, elementos de apoio, versões de cor e lista de peças da direção atual |
| `emb2.py` | O emblema da rodada 2 (atual): plaquinha presa na coleira, avião na alça, pets maiores |
| `e2.py` | Assinaturas (com o novo logo compacto), selo, elementos, versões de cor e lista de peças da rodada 2 |
| `export_e2.py` | Gera `final/` (rodada 2, atual): peças, elementos, avatar, favicon e a lista de renderização |
| `export_e.py` | Regera a rodada 1 desta direção (em `../historico/companheiros-r1`, sem tocar em `final/`) |
| `dobra.py` | O símbolo da direção Dobra: rosto, orelhas (cão, gato, coelho) e faceta |
| `d.py` | Assinaturas, selo, elementos de apoio e versões de cor da Dobra; lista de peças |
| `alternativas.py` | Estudos da rodada 3 (Janela e Retrato) |
| `export_d.py` | Regera a Dobra (em `../historico/dobra`, sem tocar em `final/`) e `exploracao/rodada-3/` |
| `export.py` | Regera a direção Elo r2 (em `../historico/elo-r2`, sem tocar em `final/`) e `exploracao/` (A, B, C r0) |
| `render.js` | Renderiza PNG transparente e PDF vetorial com Chromium (Playwright) |

## Regerar os arquivos

```bash
pip install fonttools brotli uharfbuzz skia-pathops pillow
mkdir -p fonts && cd fonts
for f in fraunces plus-jakarta-sans outfit manrope; do npm pack @fontsource/$f && mkdir -p $f && tar xzf fontsource-$f-*.tgz -C $f; done
cd ..
FONTS_DIR=$PWD/fonts python3 export_e2.py  # escreve SVG em ../final
node render.js export_jobs.json             # PNG + PDF (precisa do pacote playwright)
FONTS_DIR=$PWD/fonts python3 export_e2.py .. ico  # favicon.ico a partir dos PNG
```

As fontes são licenciadas sob a SIL Open Font License.
