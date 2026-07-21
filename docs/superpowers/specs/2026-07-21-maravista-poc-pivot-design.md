# Mar à Vista — Pivô de escopo: POC com hero em vídeo (design)

## Contexto

O plano original (`docs/superpowers/specs/2026-07-20-maravista-poc-design.md` e
`docs/superpowers/plans/2026-07-20-maravista-poc.md`) construía o site completo
do Mar à Vista Hostel como POC pré-contato. Em 2026-07-21, com as Tasks 1-5 já
commitadas e revisadas (motor + marca + tema) e a Task 6 (fotos) em andamento,
a autora decidiu mudar de estratégia: chegar ao dono com um site **completo**
antes de qualquer contato pode passar a impressão de estar vendendo algo grande
demais antes de validar a ideia. A nova entrega é uma **POC visualmente
sofisticada** — hero muito bem acabado + uma seção complementar + navegação
que demonstra a arquitetura futura sem implementá-la — que comunique "isto é
uma amostra do que podemos construir", não "este site está incompleto".

Este documento registra o design dessa POC. **Não substitui** o plano de site
completo — ele fica pausado, preservado, e retomado depois. Ver seção "O que
fica preservado" abaixo.

## O que já existia e continua valendo

Branch `maravista-poc` / worktree `.worktrees/maravista-poc`, 5 commits já
revisados:

| Task | O que é | Papel na POC |
|---|---|---|
| 1 | `localizacao.resumo` no schema (tira hardcode de João Pessoa) | Dormente — POC não tem seção de Localização |
| 2 | Fallback de favicon (PNG sem SVG genérico) | Ativo — afeta toda página |
| 3 | 4 símbolos marítimos novos em `SimboloComodidade.astro` | Dormente — POC não tem seção de Comodidades |
| 4 | Logo recortado (`logo.png`, `icone.png`, favicons) | Ativo — marca do hero |
| 5 | Tema `maravista.css` (paleta + tipografia) | Ativo — usado em toda a POC |

Nenhuma dessas tasks precisa ser desfeita ou alterada. As dormentes (1 e 3)
simplesmente não são exercitadas até a seção correspondente existir — ficam
prontas para quando a Fase completa retomar.

6 fotos da região já processadas (`clientes/maravista/fotos/regiao-*.jpg`,
não commitadas) não entram nesta POC — permanecem no worktree como estão,
preservadas para a Task 6 original quando o site completo retomar.

## Novo material desta sessão

- **Vídeo de drone do Instagram** (`clientes/maravista/fotos/hero-video-original.mp4`,
  720×1280, 23,5s, H.264+AAC) — fornecido pela autora. Mostra a orla da Barra
  vista de cima; o casarão azul-claro do hostel aparece a partir de ~15s e
  segue visível até o fim. **Ainda sem autorização de uso do dono do hostel**
  — vale só para a POC (uso interno da autora); pendência de autorização
  registrada para quando o contato acontecer.
- **7 fotos do hostel** direto da galeria pública do Booking.com (IDs
  596545653, 180750680, 180750686, 185701159, 185700798, 185700807, 184402033,
  181318477, 180795966, entre outras) — cobrem fachada, lounge, quartos com
  vista do mar, banheiros. Usadas nesta fase só a do lounge (ver seção "O
  Hostel" abaixo); as demais ficam disponíveis para quando as seções de
  Acomodações/Comodidades forem retomadas.
- Confirmado ao vivo no Booking: nota **8,8 "Fabuloso"** (1.177 avaliações),
  localização 9,9/10 — substitui os números aproximados (~9,1-9,2) do
  levantamento anterior.

## Design

### 1. Hero — vídeo full-bleed

`Hero.astro` ganha suporte opcional a vídeo, sem quebrar o comportamento atual
(LumeHostel/demo continuam com foto estática):

- Novo campo opcional no schema: `marca.heroVideo` (nome do arquivo, mesma
  pasta `fotos/` dos demais assets) — quando ausente, comportamento idêntico
  ao de hoje (`foto('capa.jpg')`).
- Quando presente, `Hero.astro` renderiza `<video autoplay muted playsinline
  poster={posterSrc}>` no lugar do `<Image>`. **Sem `loop`** — o vídeo toca
  uma vez e, por comportamento nativo do elemento `<video>`, congela no
  último frame (que é exatamente o frame com o casarão), funcionando como
  foto depois de terminar.
- `poster` = frame extraído do próprio vídeo (praticamente o mesmo do fim),
  usado como imagem de carregamento e como fallback.
- `prefers-reduced-motion: reduce` → não autoplay o vídeo; mostra só o
  `poster` como imagem estática. Mesmo princípio já aplicado à classe
  `.revela` no `Layout.astro`.
- `object-position: 50% 42%` (não o padrão 50% 50%) para manter o casarão
  em quadro mesmo em telas muito largas e baixas — validado visualmente no
  mockup `mockups/maravista-hero-video.html` (o vídeo mantém a largura toda
  em qualquer tela, por ser mais estreito que alto; só corta em cima/embaixo).
- Vídeo processado: mudo, H.264, ~720px de largura, ~12,9 MB para os 23,5s.
  **Nota de performance**: pesado para produção real (carregamento inicial);
  aceitável para a POC, mas recomendo revisitar bitrate/resolução antes de
  qualquer publicação além de uso interno.

### 2. Motor — `acomodacoes` e `comodidades` viram opcionais

Hoje `template/src/lib/schema.ts` exige `acomodacoes` (`.min(1)`) e
`comodidades` (`.min(1)`), e `template/src/pages/index.astro` os usa sem
guarda condicional (`config.comodidades.filter(...)` na linha 18, seções sem
`{condição && ...}`). Isso impede buildar uma página só com hero + uma seção.

Mudança, no mesmo padrão já usado para `regiao`/`depoimentos`/`destaques`:

- Schema: `acomodacoes: z.array(acomodacaoSchema).min(1).optional()` e mesma
  troca para `comodidades`.
- `index.astro`: mover a derivação de `comodidadesComFoto`/`comodidadesSemFoto`
  para dentro de uma guarda (`config.comodidades &&`), e envolver as duas
  seções (`#acomodacoes`, `#comodidades`) em condicionais equivalentes às que
  `regiao`/`depoimentos` já têm.
- **Build de LumeHostel e demo precisam continuar passando sem alteração** —
  ambos já fornecem os dois campos, então o comportamento não muda para eles;
  a validação é regressão, não funcionalidade nova para esses clientes.

### 3. Nav — arquitetura futura sem navegação falsa

Lista alinhada às seções que o motor *de fato* tem hoje (evita prometer algo
que o engine não constrói): **Início, O Hostel, Acomodações, Comodidades, A
Região, Localização**.

- **Início** e **O Hostel** — âncoras reais (`#hero`, `#sobre`).
- Os demais itens — rótulo visual sem `href` funcional (ou `href="#"` com
  `aria-disabled`), opacidade reduzida, sem interação de clique. Comunicam
  "isto existe no roadmap" sem simular uma navegação que não leva a lugar
  nenhum.
- Botão wa.me do nav continua **totalmente funcional** — é a única ação real
  que a POC precisa oferecer.

### 4. Seção "O Hostel" (`#sobre`) — a única seção nova implementada

Layout de duas colunas (foto + texto), reaproveitando o padrão visual já
usado no motor para seções com uma foto de destaque:

- **Foto**: a do lounge com colunas de pedra expostas e janelas/venezianas
  abertas para a praia (`185700798`, já processada em
  `mockups/img/maravista-hero/opcao-a-lounge-pedra.jpg` durante a comparação
  do hero — reaproveitar o arquivo, redimensionar para o padrão do projeto
  ≤1600px, mover para `clientes/maravista/fotos/`).
- **Texto**: reescrito nesta sessão com dados verificados ao vivo no
  Booking (não o rascunho antigo com números aproximados):

  > O Mar à Vista fica na Barra, de frente para o mar, a poucos passos do
  > Farol. É um hostel de dormitórios compartilhados — todos com vista para
  > o mar — com cozinha e recepção 24 horas. Hóspedes descrevem a
  > localização como perfeita e a vista como inigualável; a nota no
  > Booking é 8,8 ("Fabuloso"), com 1.177 avaliações, e 9,9/10 para
  > localização.

  (texto final ajustável na implementação; ideia e dados-fonte já validados)

### 5. Fora de escopo desta POC

Para não evoluir "sem querer" para o site completo:

- Nenhuma outra seção (Acomodações, Comodidades, A Região, Depoimentos,
  Localização) ganha conteúdo real ou dados no `config.json` desta POC —
  ficam ausentes (o motor já lida bem com campos ausentes) e representadas
  só como rótulo no nav.
- Sem `config.json` "quase completo" com campos vazios/placeholder só para
  preencher — o que não existe, não entra no config.
- Sem deploy em produção nesta etapa (fica para quando a autora decidir
  mostrar à autora/dono) — POC roda local (`npm run dev`) ou em preview.
- Fotos do Booking além da do lounge ficam catalogadas mas não processadas/
  commitadas ainda — só a foto usada na seção "O Hostel" entra no repo.

## Critérios de conclusão da POC

- `CLIENTE=maravista npm run build` passa.
- `CLIENTE=lumehostel npm run build` e `CLIENTE=demo npm run build` continuam
  passando sem alteração de output (regressão do schema opcional).
- Hero em vídeo funcionando: autoplay mudo, congela no último frame, respeita
  `prefers-reduced-motion`, framing do casarão correto em pelo menos 3
  larguras de tela (mobile, tablet, desktop largo).
- Nav mostra os 6 itens; só 2 são clicáveis; botão WhatsApp funcional.
- Seção "O Hostel" renderizada com foto + texto.
- Nenhuma outra seção do one-page aparece (confirma que o schema opcional
  está de fato ausente do config, não vazio).
