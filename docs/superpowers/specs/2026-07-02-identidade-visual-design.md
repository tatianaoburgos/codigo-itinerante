# Identidade Visual — Código Itinerante

Spec da identidade visual da marca, decidida em 2026-07-02 via brainstorm com mockups comparativos (2 direções → 3 variações da direção vencedora). Nome interno da identidade: **"Estrada 1 — Lâmpada de hostel"**.

## Contexto e propósito

Código Itinerante é o projeto de sites institucionais para hostels/pousadas em permuta por noites de hospedagem. A identidade precisa vestir:

1. **Documentos comerciais** (proposta, briefing, contrato) — o uso mais imediato e frequente, em fundo claro.
2. **Site do projeto** (futuro) — fundo preto, sobre o projeto (não pessoal); haverá uma seção "sobre mim" com uma única foto, visível só abaixo da dobra.

**Público principal: donos de hostel.** A marca deve passar profissionalismo com calor humano — não frieza de portfólio dev.

## Conceito

Base escura, tipografia protagonista, elegância contida — com **um acento quente**. A narrativa da cor: âmbar é a luz da lâmpada de hostel à noite, o pôr-do-sol na estrada. **A cor aparece pouco e sempre com intenção**: um grifo, um link, uma linha. Nunca em blocos grandes.

## Wordmark (logo) — "W2"

Tipográfico puro, sem símbolo. O nome conta a própria história:

- **"Código"** — Archivo, peso 600, tracking −0.03em: a estrutura rígida do código.
- **"*Itinerante*"** — Instrument Serif itálico, peso 400, corpo ~10% maior que o de "Código", tracking normal: o movimento da viagem.

Regras:

- Sobre fundo escuro: "Código" em Cal (`#F4F1E8`), "*Itinerante*" em Âmbar (`#E39A3B`).
- Sobre fundo claro (documentos): "Código" em Tinta (`#1A1915`), "*Itinerante*" em Queimado (`#B85C2E`) — versão do âmbar com contraste adequado em papel.
- Versão monocromática (quando cor não for possível): tudo na cor do texto, mantendo o contraste sans × itálico serifado.
- Tamanho mínimo: o wordmark se sustenta pequeno (testado a ~13px); abaixo disso, usar só "C*I*" com o mesmo par tipográfico (a definir na implementação do favicon).

## Paleta

Neutros:

| Nome | Hex | Papel |
|---|---|---|
| Breu | `#0A0A09` | Fundo principal (escuro) |
| Grafite | `#161513` | Superfícies, cards sobre Breu |
| Cal | `#F4F1E8` | Texto sobre escuro |
| Cinza-pedra | `#97928A` | Texto secundário sobre escuro |
| Papel | `#FBF9F4` | Fundo de documentos |
| Tinta | `#1A1915` | Texto sobre claro |

Acentos:

| Nome | Hex | Papel |
|---|---|---|
| Âmbar | `#E39A3B` | Acento principal sobre escuro: links, grifos, "*Itinerante*", cursor |
| Barro | `#C4693F` | Acento secundário, hovers |
| Dourado | `#EFC780` | Detalhes finos sobre escuro |
| Queimado | `#B85C2E` | O acento em fundo claro (documentos) — contraste AA em Papel |

Regra de proporção: em qualquer aplicação, os acentos ocupam pouco da área — a marca é preta/clara com pontos de calor, não uma marca laranja.

## Tipografia

| Papel | Família | Pesos | Uso |
|---|---|---|---|
| Display/títulos | **Archivo** | 500–700 | Headlines, wordmark, títulos de documento |
| Acento itálico | **Instrument Serif** (italic) | 400 | "*Itinerante*", palavras grifadas em headlines |
| Corpo | **Archivo** | 400–500 | Texto corrido |
| Rótulos/técnico | **IBM Plex Mono** | 400–500 | Eyebrows, hex, metadados de documento, detalhes dev |

Todas livres (Google Fonts / @fontsource), auto-hospedadas no site quando ele existir — mesmo padrão dos sites de cliente.

## Aplicação em documentos (fundo claro)

Modelo validado no mockup (seção 04):

- Fundo Papel, texto Tinta.
- Cabeçalho: wordmark à esquerda, tipo do documento em IBM Plex Mono caps (cor Queimado) à direita, régua de 2px em Queimado embaixo.
- Metadados (Para / Data / Validade) com rótulo em mono caps pequeno e valor em Archivo 600.
- Destaques no corpo em Queimado.

## Site do projeto (futuro — fora deste spec)

Decisões já tomadas que o site deverá respeitar: fundo Breu, hero tipográfico com itálico em Âmbar (headline de referência validada: "Sites para hostels, pagos em *noites*."), navegação enxuta, foto da autora única e abaixo da dobra, seções prováveis: O projeto / Sites feitos / Como funciona / Contato.

## Decisões descartadas (não reabrir sem motivo forte)

- **Direção A "elegante e contida"** (monocromática + glow): fria demais para o público de hostels.
- **Estrada 2 "Entardecer"** (Fraunces, terracota, gradiente de poente) e **Estrada 3 "Quilometragem"** (amarelo-sinal, tracejado, cantos retos): avaliadas em mockup e preteridas em favor da Estrada 1.
- Símbolo/monograma como logo principal: wordmark tipográfico puro venceu.

## Entregáveis (implementação, próxima etapa)

Pasta `marca/` na raiz do repo:

1. `paleta.md` — tabela acima, pronta para consulta.
2. Wordmark em SVG (fundo escuro, fundo claro, monocromático) com fontes convertidas em curvas.
3. Guia de uso curto (1 página): proporção de acento, tamanhos mínimos, o que não fazer.
4. Tokens CSS (`marca/tokens.css`) para o futuro site e eventuais materiais HTML.

O site do projeto é um projeto separado, com spec própria, quando chegar a hora.
