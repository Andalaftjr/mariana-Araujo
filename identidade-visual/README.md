# Coleira & Passaporte · identidade visual

Direção C · Elo · revisão r1 · 30/09/2026 · consultoria em Pet Travel

A apresentação completa (evolução, construção, sistema, testes e regras) está em
[`apresentacao/coleira-passaporte-identidade.html`](apresentacao/coleira-passaporte-identidade.html),
com versões em PNG e PDF na mesma pasta.

![Logo principal](final/png/cp-logo-principal_cor.png)

## O símbolo: um & que é um nó

O “&” do nome é desenhado como uma guia de passeio: um traço contínuo que começa na
coleira e termina na tag do animal. Na r1 esse traço passa por cima e por baixo de si
mesmo, como um nó de verdade. É um laço que não desata, e por isso transmite segurança
sem recorrer a cadeado ou escudo.

1. **Laço:** a coleira. Círculo de raio 14 no grid de 100.
2. **Nó de cima:** a diagonal passa por cima.
3. **Bojo:** o acolhimento. Círculo de raio 21.
4. **Nó de baixo:** agora quem passa por cima é o braço. Essa alternância é o que faz dele um nó real.
5. **Linha de base:** a cauda é cortada reta, alinhada ao fundo do bojo.
6. **Tag terracota:** identificação e destino. Seu respiro recorta a ponta do braço.

### O que mudou da r0 para a r1

- Traço 33% mais encorpado: passou de 8,4 para 11,2 no grid de 100.
- Entrelaçado nos dois cruzamentos, formando o nó.
- Pé reto na linha de base.
- Tag encaixada na ponta do braço.
- No logotipo, o & tem 1,32× a altura das maiúsculas: o símbolo vive dentro do nome.
- Tipografia: Plus Jakarta Sans Bold no lugar de Outfit Medium.
- A r0 continua no histórico do git (commit `58f7e5a`). As direções A, B e C (r0) estão em [`exploracao/`](exploracao).

## Arquivos (`final/`)

| Peça | Arquivo base | Uso |
| --- | --- | --- |
| Logo principal | `cp-logo-principal` | Nome com o & em destaque + descritor. Uso preferencial |
| Horizontal com selo | `cp-logo-horizontal-selo` | Símbolo + nome completo: site, cabeçalhos, documentos |
| Assinatura | `cp-logo-assinatura` | Nome em uma linha, sem descritor: rodapés e espaços estreitos |
| Vertical | `cp-logo-vertical` | Selo sobre o nome |
| Empilhada | `cp-logo-empilhado` | Coleira / & / Passaporte |
| Símbolo | `cp-simbolo` | & com nó e tag: padrões, carimbo seco, grandes formatos |
| Símbolo reduzido | `cp-simbolo-reduzido` | Sem os respiros do nó: até 24 px, e bordado ou gravação abaixo de 25 mm |
| Selo | `cp-selo` | & no círculo; é a assinatura reduzida |

Cada peça vem em seis versões (`_cor`, `_negativo`, `_preto`, `_branco`, `_cinza` e `_uma-cor`) e em três formatos:

- `svg/`: vetor, com o nome em curvas e fundo transparente.
- `pdf/`: vetor para gráfica, sem imagem embutida.
- `png/`: fundo transparente, de 1000 a 3000 px.

Além disso:

- `avatar/`: quadrados com fundo (azul e linho), com o & com nó, em SVG e em PNG de 1080 e 640 px.
- `favicon/`: `favicon.svg`, `favicon.ico` e PNG de 16, 32, 48, 180, 192 e 512 px, feitos com a versão reduzida.

## Paleta

| Cor | HEX | RGB | CMYK* | Papel |
| --- | --- | --- | --- | --- |
| Azul Passaporte | `#1B2B44` | 27, 43, 68 | 60 / 37 / 0 / 73 | Cor institucional: confiança, documentação, experiência internacional |
| Terracota Tag | `#C8694A` | 200, 105, 74 | 0 / 48 / 63 / 22 | Só na tag do &: calor, cuidado. Usar com parcimônia |
| Linho | `#F4EFE6` | 244, 239, 230 | 0 / 2 / 6 / 4 | Fundo principal; evita o branco clínico |
| Céu de Cabine | `#A9BCCB` | 169, 188, 203 | 17 / 7 / 0 / 20 | Apoio: tranquilidade e mobilidade |
| Tinta | `#111A2B` | 17, 26, 43 | 60 / 40 / 0 / 83 | Texto corrido e versão escura profunda |

\* O CMYK vem de uma conversão matemática, sem perfil ICC. Confirme com prova de impressão no perfil da gráfica (ex.: ISO Coated v2 / FOGRA39) e escolha o Pantone no guia físico.

Contrastes:

- Azul sobre Linho: 12,4:1.
- Terracota sobre Linho: 3,3:1.
- Terracota sobre Azul: 3,8:1. Use só em elementos gráficos e títulos grandes, nunca em texto pequeno.

## Tipografia

- **Plus Jakarta Sans** (Google Fonts, SIL OFL): nome, títulos e texto.
  - Bold 700 no nome.
  - SemiBold 600 nos títulos e no descritor (caixa alta, +220 de espaçamento).
  - Regular 400 no texto.
- **IBM Plex Mono** (Google Fonts, SIL OFL): dados como datas, códigos de voo, referências e checklists.

No logo, o nome já está em curvas e o “&” é o desenho próprio da marca, não o da fonte. Não redigite o logo.

## Regras básicas

- Área de proteção: x = altura da letra “C” do nome, em todos os lados.
- Tamanho mínimo:

  | Peça | Tela | Impressão |
  | --- | --- | --- |
  | Logo principal | 140 px | 40 mm |
  | Horizontal com selo | 150 px | 42 mm |
  | Assinatura | 110 px | 30 mm |
  | Vertical / empilhada | 90 px | 25 mm |
  | Símbolo / selo com nó | 32 px | 10 mm |
  | Versão reduzida | 16 px | 5 mm |

- Até 24 px, e em bordado ou gravação abaixo de 25 mm, use a versão reduzida.
- Não preencha os respiros do nó em tamanhos grandes.
- Com o nome ao lado, use o **selo**. O & livre colado ao nome seria lido como “& Coleira & Passaporte”.
- Nunca escreva “Coleira e Passaporte”, “Coleira + Passaporte” ou outra variação, nem monte o logo com o & da fonte.
- Não distorça, não gire, não troque cores e não aplique sombra, degradê, contorno ou 3D.
- Sobre fotografia, use a versão negativa numa área escura e calma. Se a foto for clara ou movimentada, use uma faixa sólida de Azul Passaporte.

## Processo e status

- **Estudos no Higgsfield (r0):** três estudos com Nano Banana 2, no projeto “Coleira & Passaporte — Identidade Visual”. A rede do ambiente bloqueou o servidor de imagens, então não consegui vê-los. Na r1 não houve geração por IA: os créditos estavam zerados, e a evolução foi desenhada direto em vetor.
- **Vetores:** construídos geometricamente em código, sem rastreamento de imagem de IA (ver [`fonte-vetorial/`](fonte-vetorial)). O nome está em curvas a partir da fonte, com a grafia exata “Coleira & Passaporte”.
- **Revisão recomendada antes do registro:** ajuste fino de espaçamento entre letras, junções do nó para bordado e gravação, e prova de cor impressa.

## Antes de usar comercialmente

Esta proposta **não declara a marca juridicamente disponível**. Ainda é preciso verificar:

- **INPI:** busca de anterioridade da marca nominativa e mista. A classe 39 é um ponto de partida; confirme as demais com um especialista.
- **Domínio:** o “&” não é aceito em endereços, então será preciso uma grafia técnica, sem mudar o nome da marca.
- **Redes sociais:** disponibilidade dos perfis.

Os contatos e @ dos mockups são fictícios. A foto do teste “sobre fotografia” é “Chelsea the cat”, de Stefan van der Walt, CC0 (banco de imagens do scikit-image).
