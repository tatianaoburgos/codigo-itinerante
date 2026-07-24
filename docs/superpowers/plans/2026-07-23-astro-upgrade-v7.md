# Upgrade do Astro (template/ e site/) para v7 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Atualizar o Astro de `^5.10.0` para a versão mais recente (7.1.3+) em `template/` e em `site/`, eliminando as 3 vulnerabilidades de dependência que sobraram depois do `npm audit fix` de 2026-07-23 (astro, esbuild e o `sharp` embutido no astro — todas resolvidas só na v7.1.3), sem quebrar nenhum dos 3 builds de cliente (`demo`, `lumehostel`, `maravista`) nem o site da marca.

**Architecture:** Upgrade mecânico via ferramenta oficial `npx @astrojs/upgrade` (atualiza Astro + integrações oficiais juntas e aplica os codemods documentados), rodado separadamente em cada projeto — são dois `package.json`/`node_modules` independentes, sem código compartilhado entre eles. Trabalho numa branch isolada, com verificação por `astro check` + `astro build` dos 3 clientes + `site/`, `npm audit` para confirmar a resolução, e smoke test visual antes de decidir se e quando mesclar em `master` (que é de onde a Vercel builda os dois sites em produção).

**Tech Stack:** Astro `5.10.0` → `7.1.3+`; Vite 8 (Astro 7 sobe de Vite 6 para Vite 8 internamente — ponto de atenção real, ver Task 1/2); `@tailwindcss/vite`; `@astrojs/sitemap`; `@astrojs/check`; TypeScript.

## Global Constraints

- Não alterar comportamento visual/funcional dos sites — só a versão do Astro/Vite e o que os codemods oficiais tocarem.
- `template/` builda para 3 clientes (`demo`, `lumehostel`, `maravista`) — os 3 precisam continuar de pé, com `astro check` e `astro build` limpos.
- Trabalhar numa branch isolada (`deps/astro-upgrade-v7`); **não mesclar em `master` nem dar push sem aprovação explícita da autora** depois da verificação completa — os dois sites em produção (LumeHostel, Mar à Vista) buildam a partir de `master` na Vercel.
- Preferir a ferramenta oficial (`npx @astrojs/upgrade`) a editar o número de versão manualmente no `package.json` — ela aplica os codemods documentados nos guias oficiais.
- Ler os guias oficiais antes de mexer, não confiar só em conhecimento memorizado (a documentação do Astro muda rápido): <https://docs.astro.build/en/guides/upgrade-to/v6/> e <https://docs.astro.build/en/guides/upgrade-to/v7/>. A própria Astro recomenda isso explicitamente até para agentes de código.
- Se algo quebrar de um jeito que não dá pra resolver rápido, reverter a branch e voltar ao Astro 5 — `master` continua intocado e os sites em produção não são afetados enquanto o upgrade não for mesclado.
- Não há suíte de testes automatizada neste repositório (`astro check` + `astro build` + smoke test visual são a verificação real, mesmo padrão usado na auditoria de 2026-07-23).

## O que já se sabe sobre as breaking changes (via Context7, docs oficiais)

Levantado antes de escrever este plano, pra não promover suposição a fato:

- **`Astro.glob()` foi removido no v6** → substituído por `import.meta.glob(..., { eager: true })`. Não deve afetar nenhum dos dois projetos: `template/src/lib/fotos.ts` já usa `import.meta.glob` diretamente, nenhum uso de `Astro.glob()` encontrado na auditoria de 2026-07-23.
- **Content Collections legado (`type: 'content'`/`'data'`, flag `legacy.collections`) removidas no v6** — precisam da Content Layer API com loader. Não deve afetar nenhum projeto: nenhum dos dois usa Content Collections (`config.json` é lido via `node:fs` puro, decisão registrada em `docs/decisoes-tecnicas.md`).
- **Config de output do Rollup** (`entryFileNames`/`chunkFileNames`/`assetFileNames`) precisa migrar para `vite.environments.client.build.rollupOptions.output` no v6. Não deve afetar nenhum projeto: nenhum dos dois `astro.config.mjs` configura Rollup output hoje.
- **Flags experimentais** (`experimental.logger`/`cache`/`routeRules`) viraram config estável no v7. Não deve afetar nenhum projeto: nenhum `astro.config.mjs` usa bloco `experimental`.
- **Astro v7 sobe para Vite 8** internamente — "principalmente uma breaking change para integrações/plugins que dependem de internals do Vite". **Isso afeta os dois projetos de verdade**: `template/package.json` e `site/package.json` têm `"overrides": { "@tailwindcss/vite": { "vite": "^6.4.3" } }`, um workaround adicionado hoje (2026-07-23) porque o `@tailwindcss/vite` vinha com uma versão de Vite diferente da que o Astro usa internamente, causando erro de tipo em `astro.config.mjs` (`Type 'Plugin<any>[]' is not assignable to type 'PluginOption'`). Com Astro 7 usando Vite 8, esse pin em `^6.4.3` fica desatualizado e provavelmente reintroduz o mesmo erro — precisa ser atualizado (ver Task 1/Step 3 e Task 2/Step 3).
- Nenhuma mudança encontrada em `astro:assets`/`<Image>` (`widths`/`sizes`/`srcset`) que afete o uso atual — a API que os dois projetos já usam continua a mesma na documentação atual.
- O Squoosh image service (removido no v5) não é usado por nenhum dos dois projetos — N/A.

Isso reduz o risco esperado a: rodar a ferramenta, corrigir o pin do Vite se necessário, e conferir que nada mais aparece. Mas os greps dos Steps abaixo confirmam isso de novo, na hora — não é pra pular essa confirmação achando que já é sabido.

---

### Task 0: Preparar o terreno

**Files:** nenhum arquivo de código — só operações de git.

- [ ] **Step 1: Conferir se há mudanças pendentes no working tree**

  Run: `git status --short`

  Se aparecer qualquer arquivo modificado ou não versionado (por exemplo, sobras de outra sessão), **parar e perguntar à autora** se quer commitar ou revisar aquilo antes de criar a branch nova. Não misturar o upgrade com mudanças não relacionadas no mesmo diff — isso dificulta reverter só o upgrade se algo der errado.

- [ ] **Step 2: Criar a branch de trabalho**

  Run: `git checkout -b deps/astro-upgrade-v7`

  Expected: branch nova criada a partir de `master` limpo, confirmada por `git status` (working tree limpo, branch `deps/astro-upgrade-v7`).

---

### Task 1: Upgrade do `template/`

**Files:**
- Modify: `template/package.json`, `template/package-lock.json` (via ferramenta — não editar o número de versão à mão)
- Modify (condicional, só se o Step 3 pedir): `template/package.json` (campo `overrides`)
- Não deve precisar tocar: `template/astro.config.mjs`, `template/src/**` (nenhum breaking change conhecido bate no que o motor usa — ver seção acima). Se a ferramenta de upgrade aplicar um codemod em algum desses arquivos, revisar o diff antes de aceitar.

- [ ] **Step 1: Confirmar que não há uso dos padrões removidos, antes do upgrade**

  Run (dentro de `template/`):
  ```bash
  grep -rn "Astro.glob(" src/
  grep -rln "astro:content" src/
  grep -rln "defineCollection" src/
  grep -n "experimental" astro.config.mjs
  grep -n "rollupOptions" astro.config.mjs
  ```
  Expected: nenhum resultado em nenhum dos 5 comandos. Se algo aparecer, parar e ler a seção correspondente do guia oficial (v6 ou v7, ver links acima) antes de continuar — não corrigir "no escuro".

- [ ] **Step 2: Rodar a ferramenta oficial de upgrade**

  Run (dentro de `template/`): `npx @astrojs/upgrade`

  A ferramenta pergunta interativamente se deve prosseguir — confirmar. Ela atualiza `astro`, `@astrojs/sitemap` e `@astrojs/check` juntos, para as versões mais recentes compatíveis, e reporta no terminal quaisquer avisos de migração específicos do projeto. Ler essa saída com atenção antes de seguir pro próximo step.

- [ ] **Step 3: Checar se o pin de Vite em `overrides` ainda faz sentido**

  Run: `npm ls vite` (dentro de `template/`, depois do Step 2)

  Comparar a versão major reportada com o `^6.4.3` que está hoje em `template/package.json` → `overrides.@tailwindcss/vite.vite`. Se o Astro trouxe Vite 8 (esperado, ver seção acima), atualizar essa linha para o major correto (ex.: `"^8.0.0"`, ajustar pro que `npm ls vite` mostrar) e rodar `npm install` de novo pra aplicar o override.

- [ ] **Step 4: Rodar `astro check` nos 3 clientes**

  Run:
  ```bash
  CLIENTE=demo npm run check
  CLIENTE=lumehostel npm run check
  CLIENTE=maravista npm run check
  ```
  Expected: `0 errors / 0 warnings / 0 hints` nos três, igual estava antes do upgrade (confirmado em 2026-07-23). Qualquer erro novo: ler a mensagem completa, procurar a palavra-chave nos guias de upgrade v6/v7 antes de tentar corrigir.

- [ ] **Step 5: Rodar o build dos 3 clientes**

  Run:
  ```bash
  CLIENTE=demo npm run build
  CLIENTE=lumehostel npm run build
  CLIENTE=maravista npm run build
  ```
  Expected: os 3 completam sem erro, cada um gerando `dist/index.html` (mais os assets). Conferir na saída do build que as imagens continuam sendo emitidas em `.webp` (mesmo comportamento confirmado hoje, sem precisar de `format=` explícito nos componentes `<Image>`).

- [ ] **Step 6: Smoke test visual**

  Run (background): `CLIENTE=lumehostel npm run dev`

  Abrir `http://localhost:4321` no navegador e conferir visualmente: hero carrega com a foto/tema terracota, o menu hambúrguer abre e mostra o item "Depoimentos", a seção de acomodações renderiza as 6 fotos. Parar o dev server depois (`Ctrl+C` ou matar o processo).

- [ ] **Step 7: Confirmar que as vulnerabilidades sumiram**

  Run: `npm audit` (dentro de `template/`)

  Expected: as vulnerabilidades ligadas a `astro`, `esbuild` e ao `sharp` aninhado em `node_modules/astro` não aparecem mais. Se sobrar algum aviso novo e não relacionado, registrar mas não é bloqueante para este plano.

- [ ] **Step 8: Commit**

  Run:
  ```bash
  git add template/package.json template/package-lock.json
  git commit -m "Atualiza Astro do template/ para v7, resolve vulnerabilidades de dependencia"
  ```
  Se o Step 2 ou 3 tiver tocado outros arquivos (codemod em `astro.config.mjs` ou em `src/`), incluir esses arquivos no `git add` também, revisando o diff de cada um antes.

---

### Task 2: Upgrade do `site/`

**Files:**
- Modify: `site/package.json`, `site/package-lock.json` (via ferramenta)
- Modify (condicional): `site/package.json` (campo `overrides`)
- Não deve precisar tocar: `site/astro.config.mjs`, `site/src/**`.

- [ ] **Step 1: Confirmar que não há uso dos padrões removidos, antes do upgrade**

  Run (dentro de `site/`):
  ```bash
  grep -rn "Astro.glob(" src/
  grep -rln "astro:content" src/
  grep -rln "defineCollection" src/
  grep -n "experimental" astro.config.mjs
  grep -n "rollupOptions" astro.config.mjs
  ```
  Expected: nenhum resultado (confirmado na auditoria de 2026-07-23: `site/` não usa Content Collections, só componentes com dados hardcoded em `dados.ts`/arrays locais).

- [ ] **Step 2: Rodar a ferramenta oficial de upgrade**

  Run (dentro de `site/`): `npx @astrojs/upgrade`

  Mesmo procedimento do Task 1/Step 2: confirmar interativamente, ler a saída com atenção.

- [ ] **Step 3: Checar o pin de Vite em `overrides`**

  Run: `npm ls vite` (dentro de `site/`, depois do Step 2)

  `site/package.json` ganhou o mesmo `overrides.@tailwindcss/vite.vite: "^6.4.3"` hoje (2026-07-23), pelo mesmo motivo do `template/` (ver Task 1/Step 3 e a seção de breaking changes acima). Atualizar para o major de Vite que o Astro 7 trouxe, se `npm ls vite` mostrar Vite 8, e rodar `npm install` de novo.

- [ ] **Step 4: `astro check`**

  Run: `npm run check`

  Expected: `0 errors / 0 warnings / 0 hints` (23 arquivos, mesmo total de hoje).

- [ ] **Step 5: Build**

  Run: `npm run build`

  Expected: 3 páginas (`/`, `/faq`, `/404`) + `sitemap-index.xml`, sem erro. Conferir que as capturas de tela do portfólio (`ProvaDeTrabalho.astro`) e a foto da Tatiana (`QuemSouEu.astro`) continuam saindo em `.webp` com múltiplos tamanhos (`widths` responsivo, adicionado hoje).

- [ ] **Step 6: Smoke test visual**

  Run (background): `npm run dev`

  Abrir `http://localhost:4321`: conferir a home (degradê breu→âmbar, seções na ordem certa, portfólio com moldura de navegador) e `http://localhost:4321/faq` (os 7 cards de pergunta com heading, card "Não está incluído" com o mesmo fundo escuro do card irmão — é o fix de contraste de hoje, confirmar que não regrediu). Parar o dev server depois.

- [ ] **Step 7: Confirmar vulnerabilidades resolvidas**

  Run: `npm audit` (dentro de `site/`)

- [ ] **Step 8: Commit**

  Run:
  ```bash
  git add site/package.json site/package-lock.json
  git commit -m "Atualiza Astro do site/ para v7, resolve vulnerabilidades de dependencia"
  ```
  Mesma ressalva do Task 1/Step 8 sobre incluir outros arquivos se algum codemod tiver tocado neles.

---

### Task 3: Verificação final e decisão de merge

**Files:** nenhum — revisão e comunicação.

- [ ] **Step 1: Rodar `npm audit` nos dois projetos lado a lado**

  Run: `cd template && npm audit && cd ../site && npm audit`

  Expected: nenhuma vulnerabilidade relacionada a `astro`/`esbuild`/`sharp` em nenhum dos dois. Anotar o que sobrar (se sobrar) pra reportar.

- [ ] **Step 2: Revisar o diff completo da branch**

  Run: `git diff master --stat`

  Conferir que só os arquivos esperados mudaram (os dois `package.json`, os dois `package-lock.json`, e qualquer `astro.config.mjs`/arquivo de `src/` que algum codemod tenha tocado, já revisado individualmente nos Tasks 1-2). Nenhuma mudança de conteúdo/visual não intencional deve aparecer aqui.

- [ ] **Step 3: Reportar para a autora e aguardar decisão de merge**

  Resumir: o que mudou (versões antes/depois), resultado de cada `check`/`build`/smoke test, resultado do `npm audit` final. Perguntar explicitamente se ela quer:
  - (a) mesclar `deps/astro-upgrade-v7` em `master` agora — o que dispara redeploy automático do LumeHostel e do Mar à Vista na Vercel (os dois projetos apontam pra `master`), ou
  - (b) deixar a branch aberta pra revisão manual antes de mesclar.

  **Não mesclar nem dar push sem essa confirmação explícita** — é uma mudança de infraestrutura que afeta os dois sites em produção ao mesmo tempo.
