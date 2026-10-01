# Higgsfield: prompts finais, jobs e resultados

Projeto no Higgsfield: **"Imigrapet — Identidade Visual (Conceitos Guia e Salvo-conduto)"** (`db701b2a-97ae-4f7d-98ae-67d2fcedb990`).

| # | Conceito | Modelo | Resolução | Job | Status do CQ |
|---|---|---|---|---|---|
| 1 | Guia v1 (só texto) | Nano Banana Pro | 2k (2752×1536) | `73f956b4-b457-4c42-bdfb-6aecfed2128f` | **Descartada**: anel sobre a linha lido como "Q." |
| 2 | Salvo-conduto | Nano Banana Pro | 2k (2752×1536) | `f4fc7ff7-ef54-4fb3-9c33-ef56262d7103` | **Aprovada com ressalvas** |
| 3 | Guia v2 (com referência vetorial) | Nano Banana 2 | 1k (1376×768) | `881c8607-5656-4273-ba5c-a04e6b8633c7` | **Aprovada com ressalvas** |

Links das imagens (abrem no navegador):
- Guia v2: https://d8j0ntlcm91z4.cloudfront.net/user_3JPJsxNN2pM1KMZabzaNrYadD2s/hf_20260930_144533_881c8607-5656-4273-ba5c-a04e6b8633c7.png
- Salvo-conduto: https://d8j0ntlcm91z4.cloudfront.net/user_3JPJsxNN2pM1KMZabzaNrYadD2s/hf_20260930_143801_f4fc7ff7-ef54-4fb3-9c33-ef56262d7103.png
- Guia v1 (descartada, para registro): https://d8j0ntlcm91z4.cloudfront.net/user_3JPJsxNN2pM1KMZabzaNrYadD2s/hf_20260930_143800_73f956b4-b457-4c42-bdfb-6aecfed2128f.png
- Referência vetorial enviada para a v2 (media `8dce7cd8-a06e-4154-8392-ee8b2bbfdd08`): https://d2ol7oe51mr4n9.cloudfront.net/user_3JPJsxNN2pM1KMZabzaNrYadD2s/8dce7cd8-a06e-4154-8392-ee8b2bbfdd08.png

## Controle de qualidade aplicado
Rodado no sandbox do Higgsfield, porque o ambiente de trabalho bloqueia o CDN:
- **OCR (RapidOCR)** de todas as pranchas para conferir a grafia.
  - Guia v1: `imigrapet` ×4 corretos e `de coleira e passaporte` ×1 correto; o símbolo foi lido como "Q".
  - Guia v2: `imigrapet` ×4 corretos e `de coleira e passaporte` ×1 correto; na assinatura horizontal ainda leu "Qimigrapet".
  - Salvo-conduto: `Imigrapet` ×4 corretos e `de coleira e passaporte` ×2 corretos; o símbolo do painel monocromático foi lido como "1".
- **Leitura estrutural** por amostragem de pixels contra a paleta (forma do símbolo, cruzamento do laço, painéis e cores).

---

## Conceito 1 — Guia — v2 (aprovada)
Modelo `nano_banana_2`, 16:9, 1k, com referência `8dce7cd8-…` (a construção vetorial do laço, gerada a partir de `vetor/01-guia/guia-simbolo-cor.svg`).

```
Use the attached reference image as the EXACT logo symbol. Reproduce its geometry faithfully everywhere it appears: one continuous thick evergreen monoline that runs horizontally, rises into a narrow teardrop-shaped loop where the line visibly CROSSES OVER ITSELF, comes down and continues horizontally, followed by a separate small solid amber dot. Do not change it into a circle sitting on a line, do not close it into a letter Q, do not add anything to it.

Create a professional brand identity presentation board for the international pet relocation company "imigrapet" using this symbol. Flat vector style, precise geometry, optical balance, generous negative space, premium international branding studio quality. No mockups, no 3D, no shadows, no gradients, no textures, no photos, no animals, no airplane, no globe, no paw, no heart, no bird.

WORDMARK: "imigrapet" in all lowercase, geometric-humanist sans serif, medium weight, slightly open letterspacing, round i dots, single-story g, deep evergreen #0E3B34. Tagline "de coleira e passaporte" in small lowercase, light weight, wide letterspacing, muted grey-green, much smaller than the name.

BOARD on a very light cool grey-green background #EEF1EC, clean modular grid of 6 panels with thin gutters:
1) large panel: the symbol alone, big, centered, exactly as in the reference.
2) horizontal lockup: symbol at left, "imigrapet" at right; the symbol's horizontal line sits on the same baseline as the word.
3) stacked lockup: symbol on top, "imigrapet" below it, "de coleira e passaporte" below that, all centered.
4) dark panel filled with evergreen #0E3B34: horizontal lockup reversed in off-white, dot stays amber #E9A23B.
5) white panel: horizontal lockup in pure black only (monochrome version, dot also black).
6) reduction test: the symbol in four decreasing sizes in a row down to favicon size, and four plain flat color swatches (evergreen #0E3B34, amber #E9A23B, mist #E6ECE7, graphite #1B1F1E) with no text.

Spelling must be exact: "imigrapet" and "de coleira e passaporte". No other text, no hex codes, no labels, no captions.
```

## Conceito 1 — Guia — v1 (descartada)
Modelo `nano_banana_pro`, 16:9, 2k, só texto.

```
Professional brand identity presentation board for a premium international pet relocation company named "imigrapet". Flat vector logo design, precise geometry, optical balance, generous negative space, no mockups, no 3D, no shadows, no gradients, no textures, no photographs, no animals drawn, no airplane, no globe, no paw, no heart, no bird.

THE SYMBOL (concept "Guia"): one single continuous monoline stroke of uniform thick weight with rounded ends, in deep evergreen #0E3B34. From the left, a straight horizontal line runs to the right, then sweeps upward into one clean, rounded, closed loop — the line crosses over itself exactly once at the base of the loop — and then comes back down and continues as a straight horizontal line to the right. After a small gap at the right end sits one solid round dot in warm amber #E9A23B. The loop reads like the handle of a leash, a knot of a bond, and a route with a moment of care. Minimal, elegant, like a mark designed by a top branding studio.

WORDMARK: the word "imigrapet" in all lowercase, custom geometric-humanist sans serif, medium weight, slightly open letterspacing, perfectly round dots on both letters i, single-story g. Deep evergreen #0E3B34. Tagline "de coleira e passaporte" in small lowercase, light weight, wide letterspacing, muted green-grey, always much smaller than the name.

BOARD LAYOUT on a very light cool grey-green background #EEF1EC, clean modular grid of 6 panels with thin gutters:
1) large panel: the symbol alone, big, centered.
2) horizontal lockup: symbol at left, "imigrapet" at right.
3) stacked lockup: symbol on top, "imigrapet" below, "de coleira e passaporte" below that, centered.
4) dark panel filled with evergreen #0E3B34: horizontal lockup reversed in off-white, dot in amber.
5) monochrome panel: horizontal lockup in pure black on white.
6) reduction test: the symbol repeated in four decreasing sizes in a row down to tiny favicon size, plus four flat color swatches (evergreen #0E3B34, amber #E9A23B, mist #E6ECE7, graphite #1B1F1E) as plain rectangles with no text.

Spelling must be exact: "imigrapet" and "de coleira e passaporte". No other text anywhere, no hex codes written, no labels, no captions.
```

**Por que falhou:** só com texto, o modelo "corrigiu" o laço para um círculo apoiado na linha, a forma mais comum no treino dele. Um símbolo proprietário precisa de referência de construção.

## Conceito 2 — Salvo-conduto (aprovada)
Modelo `nano_banana_pro`, 16:9, 2k, só texto.

```
Professional brand identity presentation board for a premium international pet relocation and pet travel documentation company named "Imigrapet". Flat vector logo design, precise geometry, optical balance, generous negative space, no mockups, no 3D, no shadows, no gradients, no textures, no photographs, no animals drawn, no airplane, no globe, no paw, no heart, no bird, no medieval crest, no rubber stamp.

THE SYMBOL (concept "Salvo-conduto"): a compact solid badge in deep burgundy #5A1F2D. Its silhouette is a contemporary shield that is also a pet ID tag: a flat top edge with only slightly rounded corners, straight vertical sides, and a fully rounded semicircular bottom — taller than wide (about 4:5). Inside, pure negative space cuts out a lowercase letter "i" leaning forward about 12 degrees like an italic: the dot of the i is a perfectly round hole, exactly like the hole of a pet ID tag where the collar ring passes; the stem of the i is a rounded capsule shape, like a microchip. Only these three elements: badge silhouette, round hole, slanted capsule. Strong, institutional, premium, calm, readable at tiny sizes.

WORDMARK: the word "Imigrapet" with capital I and the rest lowercase, custom contemporary grotesque sans serif, semibold, slightly extended width, tight even spacing, crisp straight terminals, in burgundy #5A1F2D. Tagline "de coleira e passaporte" in small lowercase, regular weight, wide letterspacing, in muted brass #B08D57, always much smaller than the name.

BOARD LAYOUT on a very light warm stone-grey background #EDEBE7, clean modular grid of 6 panels with thin gutters:
1) large panel: the symbol alone, big, centered.
2) horizontal lockup: symbol at left, "Imigrapet" at right.
3) stacked lockup: symbol on top, "Imigrapet" below, "de coleira e passaporte" below that, centered.
4) dark panel filled with burgundy #5A1F2D: horizontal lockup reversed, symbol and name in light stone #E9E7E3, tagline in brass.
5) monochrome panel: horizontal lockup in pure black on white.
6) reduction test: the symbol repeated in four decreasing sizes in a row down to tiny favicon size, plus four flat color swatches (burgundy #5A1F2D, brass #B08D57, stone #E9E7E3, ink #1C1719) as plain rectangles with no text.

Spelling must be exact: "Imigrapet" and "de coleira e passaporte". No other text anywhere, no hex codes written, no labels, no captions.
```

**Desvios observados:** o painel 4 saiu preto-tinta em vez de bordô; no painel monocromático, o pingo do "i" ficou colado à haste (o OCR leu "1").

## Prompt sugerido para a próxima rodada (quando houver créditos)
Para o Salvo-conduto, com `vetor/02-salvo-conduto/salvo-conduto-simbolo-cor.svg` exportado em PNG como referência:
> "Use the attached reference as the EXACT symbol… keep a clear gap between the dot and the slanted stem in every size… panel 4 background must be burgundy #5A1F2D, not black."

Para o Guia, repetir a v2 em 2k com a assinatura horizontal em que **o ponto âmbar vira o pingo do primeiro "i"**, e testar a variação "assinatura de percurso" (linha correndo sob o nome).
