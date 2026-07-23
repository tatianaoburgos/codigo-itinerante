# Nav com hambúrguer — novo padrão de menu (2026-07-23)

## Contexto

A autora quer trocar o padrão de menu do motor: hoje o `Nav.astro` mostra logo + todos os links + botão do WhatsApp inline, quebrando em várias linhas no mobile (e, no caso do LumeHostel, até no desktop o botão cai numa segunda linha). O novo padrão, inspirado no header do Surfcamp Arara (referência visual trazida pela autora): logo sempre colada à esquerda; à direita, sempre na mesma linha do logo (nunca quebra), o botão "Reserve pelo WhatsApp" e, colado na borda, um ícone de hambúrguer que abre um menu com os links. **Este é o novo padrão-alvo para todo cliente futuro**, não só para os dois atuais.

Também aproveitando a mudança: o LumeHostel está com deploy de produção desatualizado (de 15/07), então o botão duplicado que hoje aparece dentro da hero (visível no site publicado) já não existe no código atual — só precisa de um redeploy.

Decisões já validadas com a autora (mockup interativo em `mockups/nav-hamburguer.html`):
- Ordem à direita: botão do WhatsApp primeiro, hambúrguer colado na borda.
- Uma linha só, sempre — nunca empilha, em nenhuma largura de tela.
- No mobile (abaixo do breakpoint `sm`, 640px), o botão do WhatsApp mostra só o ícone, sem texto (o texto completo não cabe ao lado do hambúrguer nessa largura).
- Campo `marcaSchema.logoFixoEsquerda` (hoje só usado pelo Mar à Vista) fica sem função com o layout único novo — remover do schema e do `config.json` do Mar à Vista.

## Arquitetura

**`Nav.astro`** — reescrito para layout único (sem mais a ramificação por `logoFixoEsquerda`):
- `<header>` com uma única `<nav>` em flex-row, `justify-between items-center`, sempre — logo à esquerda, grupo à direita.
- Grupo à direita: `<BotaoWhatsApp icone />` + `<button popovertarget="menu-nav" popovertargetaction="toggle" aria-label="Abrir menu">` com o ícone de 3 traços (span×3 via CSS, sem SVG).
- O menu (abas + `navFuturo`) sai da barra e vira o conteúdo de `<div id="menu-nav" popover>`, lista vertical, posicionado fixo abaixo do botão (`position: fixed; top; right`). Usa a **Popover API nativa** (`popover` attribute) — dá fechar ao clicar fora e com Esc de graça, sem JS extra.
- Ícone de hambúrguer anima para "X" com CSS puro via `:has(#menu-nav:popover-open)` no header (sem listener JS).
- Itens de `navFuturo` continuam não clicáveis (`<span title="Em breve">`), mesma cor dos links reais — só que agora dentro da lista vertical do popover em vez de inline.

**`BotaoWhatsApp.astro`** — novo prop opcional `icone?: boolean` (default `false`, não muda os 2 usos existentes em `index.astro`). Quando `true`: renderiza um ícone de WhatsApp (glifo padrão, SVG inline) + `<span class="hidden sm:inline">{rotulo}</span>` — texto escondido abaixo do breakpoint `sm`, ícone sempre visível. Padding vira circular (só ícone) no mobile e pill com texto a partir do `sm`. `aria-label` no `<a>` garante que o rótulo continue acessível quando o texto está oculto.

**`schema.ts`** — remove `logoFixoEsquerda` de `marcaSchema`.

**`clientes/maravista/config.json`** — remove a chave `"logoFixoEsquerda": true`.

**Sem mudança de código para a hero do LumeHostel** — o botão duplicado já não existe no `Hero.astro` atual; resolve com o redeploy.

## Deploy

Depois de mergeado: redeploy de produção dos dois clientes (`vercel deploy --prod --cwd template --project lumehostel` e `--project maravista`), pra o novo nav e a hero limpa do Lume irem ao ar nos dois.

## Verificação

- `CLIENTE=lumehostel npm run dev` e `CLIENTE=maravista npm run dev`: conferir visualmente em largura mobile (~375px) e desktop (~1280px) — logo à esquerda, botão+hambúrguer sempre na mesma linha à direita; clicar no hambúrguer abre a lista; clicar fora ou Esc fecha; no mobile o botão do WhatsApp mostra só o ícone, a partir do `sm` mostra ícone+texto.
- `npm run check` (astro check) depois de mexer no schema, pra garantir que a remoção de `logoFixoEsquerda` não quebra tipos.
- `npm run build` local pra cada cliente, confirmando que o Zod não rejeita o `config.json` do Mar à Vista sem o campo removido.
