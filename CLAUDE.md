# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é este projeto

Sites institucionais para hostels/pousadas oferecidos em permuta por noites de hospedagem. Arquitetura "build once, reuse everywhere": um motor Astro reutilizável em `template/`, dados por cliente em `clientes/<hostel>/` (config.json + fotos). Monorepo privado; cada cliente vira um projeto separado na Vercel apontando para este repo, com variável de ambiente selecionando qual cliente buildar.

Contexto de negócio e decisões fechadas estão em `docs/projeto.md` e `docs/decisoes-tecnicas.md` — leia antes de propor mudanças de arquitetura; as decisões lá registradas (Astro + Tailwind, config.json sem CMS, monorepo, componentes compartilhados) já foram deliberadas e não devem ser reabertas sem motivo forte. A identidade visual da própria marca está em `docs/miv.md` (Manual de Identidade Visual) e o questionário reutilizável de onboarding de cliente em `docs/briefing-cliente.md`.

## Comandos

Há dois projetos Astro independentes, cada um com seu próprio `package.json` e `node_modules`:

**`template/`** — o motor dos sites de cliente (buildado por cliente via env `CLIENTE`):

```
cd template
npm install
CLIENTE=lumehostel npm run dev       # servidor de desenvolvimento (padrão: demo)
CLIENTE=lumehostel npm run build     # build estática
npm run preview                      # serve a build localmente
```

**`site/`** — o site da própria marca (landing page única, projeto separado):

```
cd site
npm install
npm run dev
npm run build
npm run og        # regenera a imagem Open Graph via sharp
```

Não há testes nem linter configurados ainda.

## Arquitetura

- **Stack**: Astro 5 + Tailwind CSS 4 (via `@tailwindcss/vite`), site 100% estático, deploy Vercel free tier. Tailwind é importado em `src/styles/global.css`.
- **Dados por cliente**: cada cliente tem `clientes/<hostel>/config.json`, validado por schema Zod (`template/src/lib/schema.ts`) na build — a build falha com dados inválidos. O cliente ativo é escolhido pela variável de ambiente `CLIENTE` (padrão `demo`) em `template/src/lib/cliente.ts`. `clientes/demo/` é o hostel fictício de vitrine ("Hostel Maré Alta").
- **Componentização**: biblioteca única de componentes compartilhados (hero, galeria, card de acomodação, mapa, CTA WhatsApp, nav/footer). Cada uma das 3 variações de site = uma composição de página diferente + um tema visual. ~80% do código compartilhado. Variação 1 primeiro, completa de ponta a ponta; variações 2 e 3 depois.
- **Tema por cliente**: cada cliente tem seu tema em `template/src/styles/temas/<slug>.css` (bloco `@theme` com tokens de cor + `--font-*`, e os `@import` das fontes daquele cliente). O `global.css` só faz `@import "@tema"` (antes do `@import "tailwindcss"`) + a base; o alias `@tema` é resolvido em `template/astro.config.mjs` a partir da env `CLIENTE` (arquivo ausente derruba a build). Os nomes de token são compartilhados (`mare`, `noite`, `azulejo`, `sal`, `espuma`, `fitinha`, `zap`) — funcionam como slots reaproveitados entre clientes; renomear para papéis neutros é follow-up. Fontes variáveis auto-hospedadas via `@fontsource-variable/*`.
- **Imagens**: fotos versionadas na pasta do cliente; otimização na build via `astro:assets`; alt text vem do config.json. As fotos ficam fora da raiz do Vite (`template/`), liberadas por `vite.server.fs.allow` em `template/astro.config.mjs`.
- **Marca do negócio (`marca/`)**: ativos da identidade visual da própria marca **Código Itinerante** (o negócio que revende os sites), distinta dos temas por cliente em `template/src/styles/temas/` — não confundir. Identidade "Estrada 1 — Lâmpada de hostel"; manual completo em `docs/miv.md`. Contém wordmark e monograma em SVG nas 3 variantes (`-escuro`/`-claro`/`-mono`, com as fontes convertidas em curvas — não dependem de fonte instalada), `tokens.css` (custom properties `--ci-*`) e o gerador `gera_wordmark.py`. Para regenerar os SVGs, as instruções (instalar `fonttools`, baixar Archivo + Instrument Serif Italic, rodar o script) estão na docstring de `marca/gera_wordmark.py`; os `.ttf` ficam ao lado e não são versionados.
- **Site institucional, não motor de reservas**: 4 abas (Acomodações, Sobre, Localização, Contato/WhatsApp). Sem checagem de disponibilidade, sem pagamento, sem integração com OTAs. Evitar a palavra isolada "Reservas" no menu. Evitar preço exato no conteúdo — preferir faixa de preços ou "consulte no WhatsApp".

## Convenções

- Idioma do projeto (docs, conteúdo, commits): português brasileiro. Sites gerados usam `lang="pt-BR"`.
- Não copiar código, textos ou imagens do site de referência (nomadssalvador.com) — apenas estrutura.
- Ao incorporar templates de terceiros, verificar a licença: preferir MIT/Apache 2.0, evitar GPL/copyleft.

## Estado atual

Variação 1 completa: 4 páginas (`/`, `/acomodacoes`, `/sobre`, `/localizacao`) compostas com a biblioteca de componentes em `template/src/components/`, JSON-LD LodgingBusiness no layout. A 4ª aba do menu é o botão wa.me direto (sem página de contato; email/Instagram ficam no footer). Convenção: todo cliente precisa de `fotos/capa.jpg` (imagem do hero, decorativa) — `template/src/lib/fotos.ts` derruba a build se uma foto do config não existir.

Primeiro cliente real em andamento: **LumeHostel** (`clientes/lumehostel/`), com tema terracota/âmbar do MIV aplicado (`template/src/styles/temas/lumehostel.css` — ver `clientes/lumehostel/marca.md`), logo real extraído do PDF (`clientes/lumehostel/marca/`) e conteúdo baseado nas presenças online do hostel (Booking/Maps). O motor `template/` ganhou suporte a logo/favicon opcionais por cliente via campo `marca` no config.json. Pendente do Gabriel (dono do LumeHostel): WhatsApp/email reais (hoje placeholder, registrado em `clientes/lumehostel/PENDENCIAS.md`), domínio e validação dos textos/fotos. Build/preview: `CLIENTE=lumehostel`.

Questionário de briefing para clientes (reutilizável): `docs/briefing-cliente.md`. Pergunta identidade visual primeiro (MIV ou fallback logo/cores/estilo); preço é política fixa comunicada como combinado ("consultar no WhatsApp", sem faixa/valor no site) — nunca pergunta ao cliente.

**Site da própria marca construído em `site/`** (2026-07-03): landing page única (spec em `docs/superpowers/specs/2026-07-03-site-codigo-itinerante-design.md`), projeto Astro separado do motor — comandos `npm run dev/build/preview` dentro de `site/`, mais `npm run og` (regenera a imagem Open Graph via sharp). Textos aprovados pela autora seção por seção; dados reais preenchidos e site publicado na Vercel (`https://codigo-itinerante.vercel.app`, definido em `site/astro.config.mjs`). Pendente no site da marca: domínio próprio.

Pendente: sitemap (depende de `site`/domínio por cliente), validação do LumeHostel pelo cliente (textos, fotos, contato real), variações 2 e 3.
