# Spec — Iconografia da marca Código Itinerante

Data: 2026-07-19. Executa o item 2 da Fase 1 do backlog (`docs/ideias-backlog.md`),
herdando as regras da spec `2026-07-17-miv-ilustracao-viajante-design.md` (§1 estilo-mãe,
§2 regime de cor, §6 iconografia). A parte da personagem/cidade/hero segue pausada —
esta spec cobre somente os ícones.

## Por quê

A iconografia é o pré-requisito da Fase 2 (template Word) e alimenta a Fase 3 (arte no
site) e materiais de divulgação. Não depende do design final da viajante.

## 1. Usos-alvo

Em ordem de prioridade:

1. **Template Word (Fase 2)** — proposta, briefing, contrato. Fundo Papel, tamanhos
   pequenos (~16–24px).
2. **Redes e apresentações** — Instagram, slides, materiais de divulgação. Fundos Papel
   ou Breu, tamanhos generosos.

Fora de escopo: sites dos clientes (identidade da Código Itinerante não se mistura com
tema de cliente).

## 2. O conjunto — 6 conceitos do negócio

| Conceito | Ideia do desenho (a fechar no mockup) |
|---|---|
| Site próprio | Casinha com cursor/janela de navegador — o hostel dono da própria presença |
| Permuta | A troca: setas circulares ou aperto de mãos estilizado |
| Noites de hospedagem | Lua/cama ou a lâmpada de hostel acesa (narrativa da marca) |
| Hostel/pousada | A casinha com jardim (a mesma do universo da viajante, em versão ícone) |
| Estrada/viagem | Estrada sumindo no horizonte ou placa de estrada |
| Contato/WhatsApp | Balão de conversa no traço da marca — nunca o logo oficial do WhatsApp em documentos |

O desenho exato de cada conceito é decidido no mockup: 2–3 propostas por conceito,
escolha visual da autora.

## 3. Estilo e cor

- **Traço**: linha solta e quente, imperfeição de propósito, uma ideia por ícone
  (estilo-mãe Monge/McFetridge da Fase 1).
- **Cor por fundo**:
  - Fundo Papel: linha em Tinta `#1A1915`, acento em Queimado `#B85C2E`.
  - Fundo Breu: linha em Cal `#F4F1E8`, acento em Âmbar `#E39A3B` ou Dourado `#EFC780`.
- **Regra do acento aplicada**: no máximo uma mancha de acento por ícone; o ícone nunca
  é inteiramente colorido. Cores de ilustração nunca tocam texto/botão/link/fundo.

## 4. Dois pesos por ícone

| Peso | Tratamento | Uso |
|---|---|---|
| **Cheio** | Linha + flat generoso | Apresentações, redes, tamanhos ≥ 32px |
| **Miúdo** | Linha simplificada + no máximo 1 mancha | Word, ~16–24px |

Mesmo DNA visual nos dois pesos — o miúdo é a destilação do cheio, não outro desenho.

## 5. Execução e entrega

1. Mockup HTML com variantes em `mockups/` (formato de comparação com toggle já
   aprovado pela autora), mostrando cada conceito nos dois pesos e nos dois fundos.
2. **Aprovação humana explícita** por conceito — nada vira definitivo sem ela.
3. SVGs definitivos em `marca/icones/`, nomeados
   `icone-<conceito>-<peso>-<fundo>.svg` (ex.: `icone-permuta-cheio-papel.svg`).
4. Nova seção "Iconografia" no `docs/miv.md` com as regras e o inventário.

**Quem desenha**: Claude desenha os SVGs diretamente (ícones são geométricos, diferente
da personagem). **Plano B**: se o resultado não convencer a autora, cai no fluxo da
viajante — ela vetoriza fora, Claude limpa e integra.

## Fora de escopo

- Personagem, cidade e filme da hero (pausados por decisão da autora em 2026-07-19).
- Ícones utilitários de documento (seção, checklist, prazo) — avaliar na Fase 2 se
  necessários.
- Template Word em si — Fase 2.
