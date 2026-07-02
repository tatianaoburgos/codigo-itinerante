# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é este projeto

Sites institucionais para hostels/pousadas oferecidos em permuta por noites de hospedagem. Arquitetura "build once, reuse everywhere": um motor Astro reutilizável em `template/`, dados por cliente em `clientes/<hostel>/` (config.json + fotos). Monorepo privado; cada cliente vira um projeto separado na Vercel apontando para este repo, com variável de ambiente selecionando qual cliente buildar.

Contexto de negócio e decisões fechadas estão em `docs/projeto.md` e `docs/decisoes-tecnicas.md` — leia antes de propor mudanças de arquitetura; as decisões lá registradas (Astro + Tailwind, config.json sem CMS, monorepo, componentes compartilhados) já foram deliberadas e não devem ser reabertas sem motivo forte.

## Comandos

Tudo roda dentro de `template/`:

```
cd template
npm install
npm run dev       # servidor de desenvolvimento
npm run build     # build estática
npm run preview   # serve a build localmente
```

Não há testes nem linter configurados ainda.

## Arquitetura

- **Stack**: Astro 5 + Tailwind CSS 4 (via `@tailwindcss/vite`), site 100% estático, deploy Vercel free tier. Tailwind é importado em `src/styles/global.css`.
- **Dados por cliente**: cada cliente tem `clientes/<hostel>/config.json`, validado por schema Zod (`template/src/lib/schema.ts`) na build — a build falha com dados inválidos. O cliente ativo é escolhido pela variável de ambiente `CLIENTE` (padrão `demo`) em `template/src/lib/cliente.ts`. `clientes/demo/` é o hostel fictício de vitrine ("Hostel Maré Alta").
- **Componentização**: biblioteca única de componentes compartilhados (hero, galeria, card de acomodação, mapa, CTA WhatsApp, nav/footer). Cada uma das 3 variações de site = uma composição de página diferente + um tema visual. ~80% do código compartilhado. Variação 1 primeiro, completa de ponta a ponta; variações 2 e 3 depois.
- **Tema por variação**: tokens de cor e fontes vivem no bloco `@theme` de `template/src/styles/global.css` (variação 1 = tema "Maré") — é essa camada que as variações 2 e 3 trocam. Fontes variáveis auto-hospedadas via pacotes `@fontsource-variable/*`.
- **Imagens**: fotos versionadas na pasta do cliente; otimização na build via `astro:assets`; alt text vem do config.json. As fotos ficam fora da raiz do Vite (`template/`), liberadas por `vite.server.fs.allow` em `template/astro.config.mjs`.
- **Site institucional, não motor de reservas**: 4 abas (Acomodações, Sobre, Localização, Contato/WhatsApp). Sem checagem de disponibilidade, sem pagamento, sem integração com OTAs. Evitar a palavra isolada "Reservas" no menu. Evitar preço exato no conteúdo — preferir faixa de preços ou "consulte no WhatsApp".

## Convenções

- Idioma do projeto (docs, conteúdo, commits): português brasileiro. Sites gerados usam `lang="pt-BR"`.
- Não copiar código, textos ou imagens do site de referência (nomadssalvador.com) — apenas estrutura.
- Ao incorporar templates de terceiros, verificar a licença: preferir MIT/Apache 2.0, evitar GPL/copyleft.

## Estado atual

Variação 1 completa: 4 páginas (`/`, `/acomodacoes`, `/sobre`, `/localizacao`) compostas com a biblioteca de componentes em `template/src/components/`, JSON-LD LodgingBusiness no layout. A 4ª aba do menu é o botão wa.me direto (sem página de contato; email/Instagram ficam no footer). Convenção: todo cliente precisa de `fotos/capa.jpg` (imagem do hero, decorativa) — `template/src/lib/fotos.ts` derruba a build se uma foto do config não existir. Pendente: sitemap (depende de `site`/domínio por cliente), variações 2 e 3.
