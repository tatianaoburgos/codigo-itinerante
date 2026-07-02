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

---

## 4. Tipografia

| Papel | Família | Pesos | Uso |
|---|---|---|---|
| Display / títulos | **Archivo** | 500–700 | Headlines, wordmark, títulos de documento |
| Acento itálico | **Instrument Serif** (italic) | 400 | "*Itinerante*" e palavras grifadas em headlines |
| Corpo | **Archivo** | 400–500 | Texto corrido |
| Rótulos / técnico | **IBM Plex Mono** | 400–500 | Eyebrows, metadados, hex, detalhes dev |

- Todas livres (Google Fonts / `@fontsource`); no site, auto-hospedadas — mesmo padrão dos sites de cliente.
- O itálico serifado é tempero de headline: uma palavra ou expressão por título, nunca frases inteiras.
- IBM Plex Mono em rótulos usa caixa alta e letter-spacing largo (~0.12em), corpo pequeno (11–12px).

### Hierarquia de referência (validada no mockup)

- Headline: Archivo 700, tracking −0.035em, line-height ~1.05, com itálico em Âmbar na palavra-chave.
- Eyebrow: IBM Plex Mono 500, caps, Cinza-pedra, com a palavra de destaque em Âmbar.
- Corpo: Archivo 400, line-height ~1.6.

---

## 5. Aplicações

### Documentos (proposta, briefing, contrato) — fundo claro

- Fundo Papel, texto Tinta.
- Cabeçalho: wordmark à esquerda; tipo do documento à direita em IBM Plex Mono caps, cor Queimado; régua de 2px em Queimado fechando o cabeçalho.
- Metadados (Para / Data / Validade): rótulo em mono caps 11px cinza, valor em Archivo 600.
- Destaques do corpo em Queimado (negrito).

### Site do projeto (futuro)

- Fundo Breu; hero tipográfico com itálico em Âmbar (headline de referência: "Sites para hostels, pagos em *noites*.").
- Cards em Grafite, cantos suaves (raio ~12px), bordas discretas.
- Botão primário: fundo Âmbar, texto Breu, pílula. Botão secundário: contorno, texto Cal.
- Foto da autora: única e abaixo da dobra; o site é do projeto.

### Assinatura / avatar

- Assinatura de e-mail: wordmark pequeno (versão de cor conforme o fundo).
- Avatar/favicon: monograma (ver §2) — `marca/monograma-*.svg`.

---

## 6. Entregáveis

1. ✅ `marca/` com wordmark e monograma em SVG (escuro, claro, mono; fontes em curvas) + `gera_wordmark.py` para regenerar.
2. ✅ `marca/tokens.css` com a paleta e as fontes para materiais HTML e o futuro site.
3. Pendente: aplicar o cabeçalho padrão nos documentos comerciais quando forem redigidos (proposta, contrato).
