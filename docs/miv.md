# MIV — Manual de Identidade Visual — Código Itinerante

Identidade **"Estrada 1 — Lâmpada de hostel"**, aprovada em 2026-07-02.
Decisões e histórico em `docs/superpowers/specs/2026-07-02-identidade-visual-design.md`.

---

## 1. A marca

Código Itinerante constrói sites institucionais para hostels e pousadas em permuta por noites de hospedagem.

**Conceito visual**: base escura, tipografia protagonista, elegância contida — com um acento quente. A narrativa da cor: o âmbar é a luz da lâmpada de hostel à noite, o pôr-do-sol na estrada.

**Tom**: profissional com calor humano. Nem frieza de portfólio dev, nem informalidade de agência descolada. O público principal é o dono de hostel.

**Princípio nº 1 — a regra do acento**: a cor quente aparece pouco e sempre com intenção — um grifo, um link, uma linha, uma palavra. A marca é preta (ou clara, em papel) com **pontos** de calor. Nunca é uma marca laranja.

---

## 2. Wordmark

O logo é tipográfico puro (wordmark), sem símbolo. O nome conta a própria história:

> **Código** — sans rígida: a estrutura do código.
> ***Itinerante*** — itálico serifado: o movimento da viagem.

### Construção

| Parte | Fonte | Peso | Detalhes |
|---|---|---|---|
| "Código" | Archivo | 600 | tracking −0.03em |
| "*Itinerante*" | Instrument Serif Italic | 400 | corpo ~10% maior que "Código", tracking normal |

As duas palavras na mesma linha, separadas por espaço simples, alinhadas pela baseline.

### Versões de cor

| Contexto | "Código" | "*Itinerante*" |
|---|---|---|
| Fundo escuro (Breu) | Cal `#F4F1E8` | Âmbar `#E39A3B` |
| Fundo claro (Papel) | Tinta `#1A1915` | Queimado `#B85C2E` |
| Monocromática (fallback) | cor do texto | cor do texto (mantém o itálico serifado) |

### Tamanhos

- O wordmark se sustenta pequeno (validado a ~13px de corpo).
- Abaixo disso (favicon, avatar), usar o monograma.

### Monograma

"C" e "I" ambos em **Archivo 600, mesmo corpo** — mesmíssimo peso — com o "I" **inclinado 12°** e na cor de acento (Âmbar sobre escuro, Queimado sobre claro). Aqui não há serifa: em tamanhos minúsculos ela morre, então o movimento da viagem fica só na inclinação. Escolhido entre 4 candidatos em 2026-07-02 (venceu M4 "dupla sans"; preteridos: I-dentro-do-C, par sans+serifa equilibrado, C+cursor).

### O que não fazer

- Não inverter o par (serifa em "Código", sans em "Itinerante").
- Não aplicar o âmbar nas duas palavras, nem em "Código" isolado.
- Não usar itálico na palavra "Código" nem regular em "Itinerante".
- Não adicionar ícones, contornos, sombras ou gradientes ao wordmark.
- Não usar a palavra "Código" ou "Itinerante" sozinha como marca.

---

## 3. Paleta

### Neutros

| Nome | Hex | Papel |
|---|---|---|
| Breu | `#0A0A09` | Fundo principal (escuro) |
| Grafite | `#161513` | Superfícies e cards sobre Breu |
| Cal | `#F4F1E8` | Texto sobre escuro |
| Cinza-pedra | `#97928A` | Texto secundário sobre escuro |
| Papel | `#FBF9F4` | Fundo de documentos |
| Tinta | `#1A1915` | Texto sobre claro |

### Acentos

| Nome | Hex | Papel |
|---|---|---|
| Âmbar | `#E39A3B` | Acento principal sobre escuro: links, grifos, "*Itinerante*" |
| Barro | `#C4693F` | Acento secundário sobre escuro, estados hover |
| Dourado | `#EFC780` | Detalhes finos sobre escuro (réguas, ícones pequenos) |
| Queimado | `#B85C2E` | O acento em fundo claro — versão do âmbar com contraste para papel |

### Regras

- Proporção: acentos ocupam fração pequena de qualquer peça; o resto é neutro.
- Sobre escuro, nunca usar Queimado (é a versão para papel); sobre claro, nunca usar Âmbar/Dourado em texto (contraste insuficiente).
- Preto puro `#000` e branco puro `#FFF` não fazem parte da paleta — usar Breu e Cal/Papel.

**Exceção deliberada (site da marca, Fase 3 — 2026-07-19)**: o fundo do site
institucional é um degradê contínuo Breu → Âmbar revelado pela rolagem — a
lâmpada acendendo. O âmbar em área grande é o ponto de chegada da página, não
o tom geral da marca; a regra do acento segue valendo em todas as outras
aplicações. O trecho final (zona clara) usa as versões de papel: texto Tinta/
Breu, ícones `-papel`, monograma claro.

---

## 4. Tipografia

| Papel | Família | Pesos | Uso |
|---|---|---|---|
| Display / títulos | **Archivo** | 500–700 | Headlines, wordmark, títulos de documento |
| Acento itálico | **Instrument Serif** (italic) | 400 | "*Itinerante*" e palavras grifadas em headlines |
| Corpo | **Archivo** | 400–500 | Texto corrido |
| Rótulos / técnico | **Martian Mono** | 400–500 | Eyebrows, metadados, hex, detalhes dev |

- Todas livres (Google Fonts / `@fontsource`); no site, auto-hospedadas — mesmo padrão dos sites de cliente.
- O itálico serifado é tempero de headline: uma palavra ou expressão por título, nunca frases inteiras. Nas headlines ele é sempre ~10% maior que o corpo da frase (mesma regra do wordmark) e **nunca** em negrito.
- **Headlines não levam ponto final** (decisão 2026-07-17).
- Martian Mono em rótulos usa caixa alta e corpo pequeno (11–12px). Ela já é larga por desenho, então o letter-spacing é discreto (~0.04em), não o tracking largo que uma mono estreita pediria.
- Substituiu a IBM Plex Mono em 2026-07-17 (comparadas em `mockups/miv-revisao.html`: Space, Xanh, DM, Sometype, Kode e Martian Mono).

### Hierarquia de referência (validada no mockup)

- Headline: Archivo 700, tracking −0.035em, line-height ~1.05, com itálico em Âmbar na palavra-chave, ~10% maior, sem ponto final.
- Eyebrow: Martian Mono 500, caps, Cinza-pedra, com a palavra de destaque em Âmbar.
- Corpo: Archivo 400, line-height ~1.6.

---

## 5. Aplicações

### Documentos (proposta, briefing, contrato) — fundo claro

- Fundo Papel, texto Tinta.
- Cabeçalho: wordmark à esquerda; tipo do documento à direita em Martian Mono caps, cor Queimado; régua de 2px em Queimado fechando o cabeçalho.
- Metadados (Para / Data / Validade): rótulo em mono caps 11px cinza, valor em Archivo 600.
- Destaques do corpo em Queimado (negrito).
- Rodapé (assina o documento): monograma **CI** à esquerda (o "I" inclinado 12° em Queimado), o site e um contato ao centro, e a paginação (`1 / 3`) à direita — tudo em Martian Mono caps, corpo pequeno, sobre régua fina. O cabeçalho apresenta; o rodapé assina.

### Site do projeto (futuro)

- Fundo Breu; hero tipográfico com itálico em Âmbar (headline de referência: "Sites para hostels, pagos em *noites*" — sem ponto, o itálico ~10% maior).
- Cards em Grafite, cantos suaves (raio ~12px), bordas discretas.
- Botão primário: fundo Âmbar, texto Breu, pílula. Botão secundário: contorno, texto Cal.
- Foto da autora: única e abaixo da dobra; o site é do projeto.

### Assinatura / avatar

- Assinatura de e-mail: nome "Tatiana Burgos" em Archivo 600 (a mesma de "Código"); abaixo, o wordmark pequeno (versão de cor conforme o fundo) e a linha de contato (site · WhatsApp) em Martian Mono.
- Avatar/favicon: monograma (ver §2) — `marca/monograma-*.svg`.

---

## 6. Iconografia

Conjunto de ícones da marca, aprovado em 2026-07-19 (spec
`docs/superpowers/specs/2026-07-19-iconografia-design.md`; escolhas feitas nos mockups
`mockups/icones-propostas*.html` e `mockups/icones-refino.html`). Herda o estilo de
ilustração da Fase 1: linha solta, uma ideia por ícone, flat contido.

### O conjunto — 6 conceitos do negócio

| Conceito | Desenho | Acento |
|---|---|---|
| Site próprio | Casinha dentro da janela de navegador | o telhado |
| Permuta | Setas circulares de troca (a de baixo é a de cima girada 180°) | a seta de baixo |
| Noites de hospedagem | Lua + cama | a lua |
| Hostel/pousada | Casinha simétrica com janela redonda no oitão, árvores e escadinha | a porta |
| Estrada/viagem | Estrada convergindo pro horizonte, sol nascendo | o sol |
| Contato | Balão de conversa com pontinhos de "digitando" | o balão inteiro |

### Regras

- **Dois pesos por ícone**: **cheio** (traço 3.25/64, com detalhes finos — apresentações e
  tamanhos ≥ 32px) e **miúdo** (traço 4.5/64, destilação com menos detalhe — Word e
  tamanhos de 16–24px). Mesmo DNA; o miúdo nunca é um desenho diferente, só a redução.
- **Cores por fundo**: sobre Breu, linha Cal + acento Âmbar; sobre Papel, linha Tinta +
  acento Queimado. Regra do acento (§1) aplicada: no máximo uma mancha de acento por
  ícone.
- Grade 64×64, `stroke-linecap`/`linejoin` round, traço com imperfeição intencional.

### O que não fazer

- Nunca usar o logo oficial do WhatsApp em documentos — o contato é sempre o balão da marca.
- Não usar estes ícones nos sites de clientes (identidade da Código Itinerante ≠ tema do cliente).
- Não colorir o ícone inteiro de acento (exceto o balão de contato, que é a mancha única).

### Arquivos

`marca/icones/icone-<conceito>-<peso>-<fundo>.svg` — 6 conceitos × cheio/miúdo ×
breu/papel = 24 arquivos. Regenerar com `python marca/gera_icones.py`; a fonte de
verdade do desenho é `mockups/icones-refino.html`.

---

## 7. Entregáveis

1. ✅ `marca/` com wordmark e monograma em SVG (escuro, claro, mono; fontes em curvas) + `gera_wordmark.py` para regenerar.
2. ✅ `marca/tokens.css` com a paleta e as fontes para materiais HTML e o futuro site.
3. ✅ `marca/icones/` com os 24 SVGs da iconografia + `gera_icones.py` para regenerar.
4. ✅ `marca/miv.html` — versão navegável deste manual, e `marca/MIV-codigo-itinerante.pdf` — exportação em PDF (gerados a partir deste arquivo; regenerar manualmente quando o manual mudar de forma relevante).
5. Pendente: aplicar o cabeçalho padrão nos documentos comerciais quando forem redigidos (proposta, contrato).
