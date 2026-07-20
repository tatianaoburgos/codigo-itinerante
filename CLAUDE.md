# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é este projeto

Sites institucionais para hostels/pousadas oferecidos em permuta por noites de hospedagem. Arquitetura "build once, reuse everywhere": um motor Astro reutilizável em `template/`, dados por cliente em `clientes/<hostel>/` (config.json + fotos). Monorepo privado; cada cliente vira um projeto separado na Vercel apontando para este repo, com variável de ambiente selecionando qual cliente buildar.

**Diretrizes de design obrigatórias em qualquer trabalho visual**: `docs/diretrizes-design.md` (o que todo site SEMPRE tem e o que NUNCA tem — ex.: hero full-bleed, rolagem só vertical, sem vídeos/carrosséis/popups/emojis) e `docs/preferencias-visuais.md` (catálogo de referências visuais por site analisado, para propor opções com exemplo que a autora consiga ver). Para iniciar site de cliente novo, usar a skill `/novo-projeto` (`.claude/skills/novo-projeto/SKILL.md`): pesquisa Maps/Instagram/Booking primeiro, confirma o que a pesquisa já respondeu, pergunta o resto uma pergunta por vez com opções + recomendação + referência visual.

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
npm run check                        # astro check (tipos, sem lint dedicado)
```

No PowerShell (Windows), a sintaxe `VAR=x cmd` não funciona — defina a env antes: `$env:CLIENTE = 'lumehostel'; npm run dev`.

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
- **Formato do site**: **one-page com âncoras** (desde 2026-07-13, substituiu a variação multipágina). Uma única rota `/` compõe, nesta ordem: hero em tela cheia → acomodações em grade (cards boutique, 2/3 colunas) → comodidades ilustradas → a região → depoimentos → localização → CTA final. O menu são âncoras + botão wa.me. Seções cujo campo não existe no config (`regiao`, `depoimentos`) simplesmente não renderizam, e o Nav esconde a aba correspondente.
- **Componentização**: biblioteca única de componentes compartilhados (hero, galeria, grade de acomodações, mapa, CTA WhatsApp, nav/footer, divisor de símbolo, marca-d'água). ~80% do código compartilhado entre clientes; cada cliente = mesma composição + tema visual próprio.
- **Tema por cliente**: cada cliente tem seu tema em `template/src/styles/temas/<slug>.css` (bloco `@theme` com tokens de cor + `--font-*`, e os `@import` das fontes daquele cliente). O `global.css` só faz `@import "@tema"` (antes do `@import "tailwindcss"`) + a base; o alias `@tema` é resolvido em `template/astro.config.mjs` a partir da env `CLIENTE` (arquivo ausente derruba a build). Os nomes de token são compartilhados (`mare`, `noite`, `azulejo`, `sal`, `espuma`, `fitinha`, `zap`) — funcionam como slots reaproveitados entre clientes; renomear para papéis neutros é follow-up. Fontes variáveis auto-hospedadas via `@fontsource-variable/*`.
- **Imagens**: fotos versionadas na pasta do cliente; otimização na build via `astro:assets`; alt text vem do config.json. As fotos ficam fora da raiz do Vite (`template/`), liberadas por `vite.server.fs.allow` em `template/astro.config.mjs`.
- **Marca do negócio (`marca/`)**: ativos da identidade visual da própria marca **Código Itinerante** (o negócio que revende os sites), distinta dos temas por cliente em `template/src/styles/temas/` — não confundir. Identidade "Estrada 1 — Lâmpada de hostel"; manual completo em `docs/miv.md`. Contém wordmark e monograma em SVG nas 3 variantes (`-escuro`/`-claro`/`-mono`, com as fontes convertidas em curvas — não dependem de fonte instalada), `tokens.css` (custom properties `--ci-*`) e o gerador `gera_wordmark.py`. Para regenerar os SVGs, as instruções (instalar `fonttools`, baixar Archivo + Instrument Serif Italic, rodar o script) estão na docstring de `marca/gera_wordmark.py`; os `.ttf` ficam ao lado e não são versionados. Versão navegável do manual em `marca/miv.html` (gerada a partir de `docs/miv.md`), com exportação em PDF em `marca/MIV-codigo-itinerante.pdf`.
- **Site institucional, não motor de reservas**: 4 abas (Acomodações, Sobre, Localização, Contato/WhatsApp). Sem checagem de disponibilidade, sem pagamento, sem integração com OTAs. Evitar a palavra isolada "Reservas" no menu. Evitar preço exato no conteúdo — preferir faixa de preços ou "consulte no WhatsApp".

## Convenções

- Idioma do projeto (docs, conteúdo, commits): português brasileiro. Sites gerados usam `lang="pt-BR"`.
- Não copiar código, textos ou imagens do site de referência (nomadssalvador.com) — apenas estrutura.
- Ao incorporar templates de terceiros, verificar a licença: preferir MIT/Apache 2.0, evitar GPL/copyleft.

## Estado atual

Motor completo como **one-page** (`/` apenas), JSON-LD LodgingBusiness no layout. Spec e plano do redesign: `docs/superpowers/specs/2026-07-13-lumehostel-onepage-design.md` e `docs/superpowers/plans/2026-07-13-lumehostel-onepage.md`. Convenção: todo cliente precisa de `fotos/capa.jpg` (imagem do hero, decorativa) — `template/src/lib/fotos.ts` derruba a build se uma foto do config não existir. Campos do config: `comodidades` (nome + descricao/foto/simbolo opcionais; `simbolo` referencia a biblioteca de SVGs artísticos em `SimboloComodidade.astro`), `regiao`, `depoimentos` e `destaques` (opcionais; `destaques` = até 2 seções full-bleed com foto fixa ao rolar + frase, técnica clip-path), `marca.simbolo` (divisor de seções e marca-d'água). Movimento sem vídeo: classe `.revela` (surgimento suave via IntersectionObserver no Layout, respeita `prefers-reduced-motion`).

Primeiro cliente real em andamento: **LumeHostel** (`clientes/lumehostel/`), com tema terracota/âmbar do MIV aplicado (`template/src/styles/temas/lumehostel.css` — ver `clientes/lumehostel/marca.md`), logo real extraído do PDF (`clientes/lumehostel/marca/`), favicon completo em terracota e conteúdo baseado **exclusivamente** nas presenças online do hostel (Booking/Maps/Instagram) — nunca inventar informação sobre o hostel. Fotos do hostel vêm das galerias públicas do próprio estabelecimento e as da região são de licença livre; proveniência de cada arquivo em `clientes/lumehostel/fotos/FONTES.md`. Coworking e redário já têm foto própria; churrasqueira e sala de jogos ainda não. Tipografia: Space Grotesk em todo o site (a Arial Rounded MT Bold do MIV é proprietária; ver pendência de licença abaixo — a Fredoka foi substituída). Fundo das seções usa o componente `CascataOndas.astro` (cascata tom sobre tom por seção) para evitar cor chapada; mosaicos de "A região" e "A vibe" alinhados em fileiras alternando foto grande/pequena. Publicado em produção na Vercel em `https://lumehostel.vercel.app` (2026-07-15); falta domínio próprio. Pendências do Gabriel em `clientes/lumehostel/PENDENCIAS.md` — inclui decidir se mantém a seção de depoimentos (custo de manutenção) e a opção de comprar a licença web da fonte do MIV. As 10 melhores avaliações públicas do hostel (Google Maps 5,0/52 e Booking 9,2/444) estão em `clientes/lumehostel/avaliacoes.md`; em 2026-07-14 o `config.json` já foi atualizado com depoimentos trocados a partir dessas avaliações do Google. Build/preview: `CLIENTE=lumehostel`.

Questionário de briefing para clientes (reutilizável): `docs/briefing-cliente.md`. Pergunta identidade visual primeiro (MIV ou fallback logo/cores/estilo); preço é política fixa comunicada como combinado ("consultar no WhatsApp", sem faixa/valor no site) — nunca pergunta ao cliente.

**Site da própria marca construído em `site/`** (2026-07-03): landing page única (spec em `docs/superpowers/specs/2026-07-03-site-codigo-itinerante-design.md`), projeto Astro separado do motor — comandos `npm run dev/build/preview` dentro de `site/`, mais `npm run og` (regenera a imagem Open Graph via sharp). Textos aprovados pela autora seção por seção; dados reais preenchidos e site publicado na Vercel (`https://codigo-itinerante.vercel.app`, definido em `site/astro.config.mjs`). SEO básico (sitemap.xml + robots.txt via `@astrojs/sitemap`, mesmo padrão do `template/`) adicionado em 2026-07-20. Pendente no site da marca: domínio próprio.

**Fase 3 do roteiro concluída em 2026-07-19** (splash de cor + iconografia no `site/`): fundo da página em degradê contínuo Breu → Âmbar (classe `.pagina-degrade` em `site/src/styles/global.css`), breu sólido cobrindo Hero + QuemSouEu + ComoFunciona e a cor entrando a partir do Manifesto, chegando em âmbar cheio pouco antes do CTA final. `CtaFinal` vive na zona clara (versão de papel: ícone/monograma claros, texto em Breu, botão invertido via nova prop `invertido` em `BotaoWhatsApp.astro`). Ícones de `marca/icones/` em escala grande no `ComoFunciona` (72px) e no `CtaFinal` (88px). `Hero` no mobile usa `min-h-dvh` (tela cheia) para a primeira dobra não revelar a seção seguinte — no desktop mantém `md:min-h-[78vh]`. Exceção à regra do acento registrada no `docs/miv.md`. Spec e plano: `docs/superpowers/specs/2026-07-19-site-degrade-fase3-design.md` e `docs/superpowers/plans/2026-07-19-site-degrade-fase3.md`.

**Fase 1 do MIV em andamento** (desde 2026-07-17): estilo de ilustração da marca e a personagem "viajante". Spec em `docs/superpowers/specs/2026-07-17-miv-ilustracao-viajante-design.md`, plano em `docs/superpowers/plans/2026-07-17-fase1-viajante-ilustracao.md` (checkboxes marcam o progresso). Fluxo: cada peça nasce como mockup HTML com variantes em `mockups/` (formato de comparação aprovado pela autora), passa por aprovação humana explícita e só então vira SVG definitivo em `marca/ilustracao/` — nenhuma task avança sem aprovação. Estado: Task 1 (silhuetas) pausada no portão de aprovação, com tendência parcial S2-P2 (`mockups/viajante-silhuetas.html`) que a autora considerou insuficiente. Em 2026-07-19 ela trouxe um desenho a lápis próprio (celular erguido, óculos escuros, cabelão cacheado, top cropped) e o vetorizou; o Claude coloriu por regiões em `mockups/viajante-colorida.svg` (fonte em `mockups/viajante-vetorizada-original.svg`) — aguardando a reação dela para promover a `marca/ilustracao/viajante.svg`. No mesmo dia ela pediu para deixar personagem/cidade/hero por último e seguir com o resto do roteiro. **Iconografia da marca concluída em 2026-07-19** (spec `docs/superpowers/specs/2026-07-19-iconografia-design.md`, plano `docs/superpowers/plans/2026-07-19-iconografia.md`): 6 conceitos do negócio em dois pesos e dois fundos, SVGs em `marca/icones/` gerados por `marca/gera_icones.py` (fonte de verdade do desenho: `mockups/icones-refino.html`), regras na seção 6 do `docs/miv.md`. Backlog de fases e ideias em `docs/ideias-backlog.md`.

Sitemap já integrado via `@astrojs/sitemap` em `template/astro.config.mjs` (+ `template/src/pages/robots.txt.ts`); a URL base ainda depende do domínio por cliente. Pendente: validação do LumeHostel pelo cliente (textos, fotos, contato real). As "variações 2 e 3" ficaram em aberto: a one-page substituiu a variação 1 para todos os clientes, então o que "variação" significa daqui pra frente precisa ser redefinido (provavelmente tema + composição, não estrutura de rotas).
