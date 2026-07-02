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
- **Dados por cliente**: cada cliente terá `clientes/<hostel>/config.json`, validado por schema (Zod, via content collections do Astro) na build — a build deve falhar com dados inválidos. `clientes/demo/` é o hostel fictício de vitrine.
- **Componentização**: biblioteca única de componentes compartilhados (hero, galeria, card de acomodação, mapa, CTA WhatsApp, nav/footer). Cada uma das 3 variações de site = uma composição de página diferente + um tema visual. ~80% do código compartilhado. Variação 1 primeiro, completa de ponta a ponta; variações 2 e 3 depois.
- **Imagens**: fotos versionadas na pasta do cliente; otimização na build via `astro:assets`; alt text vem do config.json.
- **Site institucional, não motor de reservas**: 4 abas (Acomodações, Sobre, Localização, Contato/WhatsApp). Sem checagem de disponibilidade, sem pagamento, sem integração com OTAs. Evitar a palavra isolada "Reservas" no menu. Evitar preço exato no conteúdo — preferir faixa de preços ou "consulte no WhatsApp".

## Convenções

- Idioma do projeto (docs, conteúdo, commits): português brasileiro. Sites gerados usam `lang="pt-BR"`.
- Não copiar código, textos ou imagens do site de referência (nomadssalvador.com) — apenas estrutura.
- Ao incorporar templates de terceiros, verificar a licença: preferir MIT/Apache 2.0, evitar GPL/copyleft.

## Estado atual

Scaffold do motor no ar (`template/src/pages/index.astro` é placeholder). Próximo passo registrado: construir a variação 1 do motor com o cliente-demo (`clientes/demo/` ainda não existe).
