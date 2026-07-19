# Plano — Iconografia da marca Código Itinerante

> **CONCLUÍDO em 2026-07-19.** Rodadas 1/1B/1C/1D fecharam o conjunto (1B1, 2A, 3B,
> 4L sem nuvem, 5A, 6A); rodada 2 aprovada com ajustes (setas simétricas por rotação,
> raios no miúdo da estrada). SVGs em `marca/icones/` via `marca/gera_icones.py`;
> seção 6 do `docs/miv.md`.

## Contexto

Fase 1 do MIV, item 2. A parte da personagem/cidade/hero está pausada por decisão da autora; a iconografia não depende dela. Spec aprovada e commitada: `docs/superpowers/specs/2026-07-19-iconografia-design.md` — 6 conceitos do negócio, estilo linha solta + flat (herdado da spec 2026-07-17, §1/§2/§6), dois pesos (cheio/miúdo), cores por fundo (Papel: Tinta+Queimado; Breu: Cal+Âmbar/Dourado), regra do acento (máx. 1 mancha de acento por ícone).

Fluxo obrigatório do projeto: mockup HTML com variantes → aprovação humana explícita → SVG definitivo. Nenhuma task avança sem aprovação. Plano B registrado: se os SVGs não convencerem, cai no fluxo da viajante (autora vetoriza fora).

Ao aprovar este plano, salvá-lo também em `docs/superpowers/plans/2026-07-19-iconografia.md` (convenção do projeto, checkboxes marcam progresso) e commitar.

## Task 1 — Mockup rodada 1: propostas de desenho por conceito

Criar `mockups/icones-propostas.html`, seguindo o formato dos mockups existentes (base: `mockups/estilo-ilustracao.html` — mesmos tokens inline, eyebrow/h1/cartão/rótulo, SVGs desenhados à mão no arquivo; toggle claro/escuro para ver cada proposta sobre Breu e sobre Papel).

- 6 conceitos × 2–3 propostas de desenho cada, no peso **cheio** (linha solta + flat generoso):
  - **Site próprio**: casinha + cursor / casinha dentro de janela de navegador
  - **Permuta**: setas circulares soltas / aperto de mãos estilizado / casinha⇄lua
  - **Noites**: lâmpada de hostel acesa / lua + cama / lua sobre casinha
  - **Hostel/pousada**: casinha com jardim (variações de traço)
  - **Estrada/viagem**: estrada ao horizonte / placa de estrada
  - **Contato**: balão de conversa no traço da marca (variações)
- Traço: linha imperfeita de propósito, `stroke-linecap="round"`, uma ideia por ícone.
- Grade consistente (viewBox 64×64) para todos.

**PORTÃO**: autora abre o mockup e escolhe 1 desenho por conceito (ou pede nova rodada). Não seguir sem escolha explícita.

## Task 2 — Mockup rodada 2: refino, pesos e tamanhos reais

Criar `mockups/icones-refino.html` com os 6 desenhos escolhidos:

- Cada ícone nos **dois pesos** (cheio e miúdo — o miúdo é a destilação: linha simplificada + máx. 1 mancha).
- Cada peso nos **dois fundos** (Breu e Papel) com as cores da spec.
- Régua de tamanhos reais: 16 / 24 / 32 / 64 px, para validar legibilidade do miúdo no tamanho do Word.

**PORTÃO**: aprovação final por conceito. Se algum ícone "não convencer", acionar o plano B para esse ícone.

## Task 3 — SVGs definitivos

- Criar `marca/icones/` com os aprovados: `icone-<conceito>-<peso>-<fundo>.svg` (até 6 × 2 pesos × 2 fundos = 24 arquivos; slugs: `site-proprio`, `permuta`, `noites`, `hostel`, `estrada`, `contato`).
- SVGs limpos: viewBox 64×64, cores hard-coded conforme fundo (mesmo padrão dos SVGs de `marca/`), sem dependência de fonte, `aria-label` não é necessário em arquivo — decorativos por padrão.
- Verificação: abrir uma página de conferência rápida (ou os próprios arquivos) e comparar com o mockup aprovado.

## Task 4 — Registro no MIV e fechamento

- Nova seção "Iconografia" em `docs/miv.md`: inventário dos 6 conceitos, regra dos dois pesos, cores por fundo, regra do acento, proibições (nunca logo oficial do WhatsApp em documentos; ícones nunca em tema de cliente).
- Atualizar `docs/ideias-backlog.md` (item 2 da Fase 1 concluído) e o "Estado atual" do `CLAUDE.md`.
- Commit final.

## Verificação end-to-end

- Mockups abertos no navegador da autora em cada portão (Task 1 e 2) — a aprovação dela é o teste.
- Task 3: os SVGs renderizam idênticos ao mockup aprovado, nos dois fundos, legíveis a 16px no peso miúdo.
