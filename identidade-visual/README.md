# Coleira & Passaporte · identidade visual

Direção D · Dobra · 30/09/2026 · consultoria em Pet Travel

A apresentação completa (conceito, construção, sistema, testes e regras) está em
[`apresentacao/coleira-passaporte-identidade.html`](apresentacao/coleira-passaporte-identidade.html),
com versões em PNG e PDF na mesma pasta.

![Logo principal](final/png/cp-logo-principal_cor.png)

## O conceito: uma página de passaporte, dobrada, vira um pet

O símbolo é um cão de origami feito com três dobras:

1. **A página:** uma página de passaporte, quadrada.
2. **Dobra ao meio:** na diagonal, a página vira um triângulo. É o rosto, com o vinco no centro.
3. **Dobra das orelhas:** os cantos de cima descem e viram as orelhas.

O desenho carrega quatro ideias:

- **Pet:** as orelhas dizem "animal" na hora, sem patinha, osso ou personagem.
- **Documento:** é papel dobrado. Em inglês, a dobra no canto de uma página se chama *dog-ear*.
- **Segurança:** o rosto em triângulo invertido é também um escudo.
- **Cuidado:** origami é precisão e paciência, cada dobra no lugar certo.

**Família:** a mesma dobra serve para todos os pets. Só muda a orelha: caída para cães (símbolo principal), em pé para gatos e longa para coelhos.

## Arquivos (`final/`)

| Peça | Arquivo base | Uso |
| --- | --- | --- |
| Logo principal | `cp-logo-principal` | Símbolo + nome + descritor. Uso preferencial |
| Horizontal | `cp-logo-assinatura` | Símbolo + nome, sem descritor: menu, rodapé, assinatura |
| Vertical | `cp-logo-vertical` | Símbolo sobre o nome |
| Compacta | `cp-logo-compacto` | Nome em duas linhas ao lado do símbolo |
| Nome | `cp-logo-nome` | Só o logotipo, quando o símbolo já está na peça |
| Símbolo | `cp-simbolo` | O cão de origami |
| Família | `cp-simbolo-gato`, `cp-simbolo-coelho` | Conteúdo por espécie |
| Selo | `cp-selo` | Símbolo no círculo; é a assinatura reduzida |

Cada peça vem em seis versões (`_cor`, `_negativo`, `_preto`, `_branco`, `_cinza`, `_uma-cor`) e em três formatos:

- `svg/`: vetor, com o nome em curvas e fundo transparente.
- `pdf/`: vetor para gráfica, sem imagem embutida.
- `png/`: fundo transparente, de 2000 a 3000 px.

Pastas complementares:

- `elementos/`: a orelha de canto (canto dobrado em terracota) e a família lado a lado.
- `avatar/`: quadrados com fundo, em azul e em linho, em SVG e em PNG de 1080 e 640 px.
- `favicon/`: `favicon.svg`, `favicon.ico` e PNG de 16, 32, 48, 180, 192 e 512 px.

O símbolo é o mesmo desenho em todos os tamanhos, sem versão reduzida.

## Paleta

| Cor | HEX | RGB | CMYK* | Papel |
| --- | --- | --- | --- | --- |
| Azul Passaporte | `#1B2B44` | 27, 43, 68 | 60 / 37 / 0 / 73 | Cor institucional; o rosto do cão |
| Terracota Orelha | `#C8694A` | 200, 105, 74 | 0 / 48 / 63 / 22 | As orelhas, o “&” e a orelha de canto |
| Azul Dobra | `#2B4368` | 43, 67, 104 | 59 / 36 / 0 / 59 | Lado iluminado da dobra; só no símbolo em cor |
| Linho | `#F4EFE6` | 244, 239, 230 | 0 / 2 / 6 / 4 | Fundo principal: papel e calma |
| Céu de Cabine | `#A9BCCB` | 169, 188, 203 | 17 / 7 / 0 / 20 | Apoio: tranquilidade e mobilidade |
| Tinta | `#111A2B` | 17, 26, 43 | 60 / 40 / 0 / 83 | Texto corrido e fundo escuro profundo |

\* O CMYK vem de conversão matemática, sem perfil ICC. Confirme com prova de impressão no perfil da gráfica (ex.: ISO Coated v2 / FOGRA39) e escolha o Pantone no guia físico.

## Tipografia

- **Fraunces SemiBold** (Google Fonts, SIL OFL): nome e títulos. É uma serifada de desenho suave, que dá o tom de consultoria cuidadosa e faz contraste com a geometria do símbolo. No logo, o “&” fica em terracota.
- **Plus Jakarta Sans** (Google Fonts, SIL OFL): texto corrido, botões e descritor. No descritor, SemiBold 600 em caixa alta, com +220 de espaçamento.
- **IBM Plex Mono** (Google Fonts, SIL OFL): datas, códigos de voo e referências.

No logo, o nome já está em curvas. Não redigite o logo com a fonte.

## Regras básicas

- **Área de proteção:** x = altura da letra “C” do nome, em todos os lados.
- **Tamanho mínimo:**

  | Peça | Tela | Impressão |
  | --- | --- | --- |
  | Logo principal | 180 px | 45 mm |
  | Horizontal / compacta | 120 px | 30 mm |
  | Vertical | 100 px | 25 mm |
  | Símbolo / selo | 16 px | 5 mm (bordado: 8 mm) |

- **Família:** o cão é o símbolo principal. Gato e coelho entram em conteúdo por espécie.
- **Orelha de canto:** aplique a orelha terracota no canto superior direito de documentos, cartões e posts.
- **Terracota:** fica nas orelhas, no “&” e na orelha de canto. Não é cor de texto corrido.
- **Símbolo:** não desenhe olhos, boca ou nariz (o símbolo é uma dobra, não um personagem). Não acrescente patinha, osso, coração ou avião.
- **Nome:** nunca escreva “Coleira e Passaporte”, “Coleira + Passaporte” ou outra variação.
- **Efeitos:** não distorça, não gire, não troque cores e não aplique sombra, degradê, contorno ou 3D.
- **Sobre fotografia:** use a versão negativa numa área escura e calma, com o “&” em linho. Se a foto for clara ou movimentada, use uma faixa sólida de Azul Passaporte.

## Processo e status

- **Direção anterior (Elo, r0 a r2):** substituída pela Dobra. As versões continuam no histórico do git (commits `58f7e5a`, `d6bf88c` e `07f2724`).
- **Estudos:**
  - As direções A, B e C (r0) estão em [`exploracao/`](exploracao).
  - Os estudos desta rodada, Janela e Retrato, estão em [`exploracao/rodada-3/`](exploracao/rodada-3).
- **Sem IA nesta rodada:** tudo foi desenhado direto em vetor, porque os créditos do Higgsfield estavam zerados.
- **Vetores:** construídos geometricamente em código, sem rastreamento de imagem de IA (ver [`fonte-vetorial/`](fonte-vetorial)). O nome está em curvas a partir da fonte, com a grafia exata “Coleira & Passaporte”.
- **Revisão recomendada antes do registro:** ajuste fino de espaçamento do nome e prova de cor impressa.

## Antes de usar comercialmente

Esta proposta **não declara a marca juridicamente disponível**. Ainda é preciso verificar:

- **INPI:** busca de anterioridade da marca nominativa e mista. A classe 39 é um ponto de partida; confirme as demais com um especialista.
- **Domínio:** o “&” não é aceito em endereços, então será preciso uma grafia técnica, sem mudar o nome da marca.
- **Redes sociais:** disponibilidade dos perfis.

Os contatos e @ dos mockups são fictícios. A foto do teste “sobre fotografia” é “Chelsea the cat”, de Stefan van der Walt, CC0 (banco de imagens do scikit-image).
