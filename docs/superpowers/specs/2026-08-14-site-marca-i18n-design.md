# pt/en/es no site da marca (`site/`) — design

## Contexto

O `site/` (landing page da própria Código Itinerante, projeto Astro separado do motor `template/`) não tem nenhuma infraestrutura de idioma hoje — texto cravado direto em ~10 componentes, 3 páginas (`index`, `faq`, `404`). O motor `template/` já resolveu multilíngue (pt/en/es) pro LumeHostel: roteamento i18n nativo do Astro, dicionário de textos por idioma (`lib/textos.ts`), helper de normalização de idioma (`lib/i18n.ts`), alternador no `Nav.astro`, `hreflang`/`og:locale`/`html lang` no `Layout.astro`. Esse projeto estende o mesmo padrão pro `site/`, adaptado à ausência de um `config.json` por cliente — aqui só existe um "cliente" (a própria marca), então todo o conteúdo é texto fixo, sem a distinção entre "campo do cliente" e "texto fixo do motor" que existe no `template/`.

Motivação: consistência com o produto vendido (o motor já oferece pt/en/es pros clientes), não prospecção ativa fora do Brasil.

## Decisões fechadas nesta sessão

- **Escopo de páginas**: as 3 páginas do `site/` — `index`, `faq`, `404` — ganham pt/en/es.
- **Autoria da tradução**: Claude traduz o conteúdo (mesmo método do LumeHostel), a autora revisa antes de publicar.
- **Alternador de idioma**: fica no topo de cada página, perto do elemento de logo/wordmark já existente ali (wordmark na Hero da home, o link do monograma na FAQ, a wordmark no 404) — não no rodapé nem fixo na tela. `site/` não tem `Nav.astro`/menu fixo como o motor; o alternador é um elemento pequeno e pontual em cada página, não um componente de navegação.
- **Sem gate de idiomas ativos**: diferente do motor (`idiomasDisponiveis` por cliente, com `demo`/`maravista` sem espanhol), aqui os 3 idiomas estão sempre ativos — não existe "cliente parcial".

## Design

### 1. Helpers de idioma (`site/src/lib/i18n.ts`, novo)

```ts
export const idiomas = ['pt', 'en', 'es'] as const;
export type Idioma = (typeof idiomas)[number];

export function idiomaAtual(currentLocale: string | undefined): Idioma {
  return currentLocale !== undefined && (idiomas as readonly string[]).includes(currentLocale)
    ? (currentLocale as Idioma)
    : 'pt';
}
```

Sem `t()`/`campoLocalizavel`: como todo o conteúdo é traduzido de uma vez (não há campo "ainda não traduzido" que precise cair pra `pt`), o dicionário já nasce com as 3 chaves resolvidas por seção.

### 2. Dicionário de textos (`site/src/lib/textos.ts`, novo)

```ts
export const textos = {
  pt: { hero: {...}, quemSouEu: {...}, provaDeTrabalho: {...}, comoFunciona: {...},
        manifesto: {...}, dor: {...}, proposta: {...}, escopo: {...}, ctaFinal: {...},
        faq: { perguntas: [...] }, pagina404: {...}, meta: { home: {...}, faq: {...}, pagina404: {...} },
        botaoWhatsApp: { rotuloPadrao: '...', mensagem: '...' } },
  en: { /* mesma forma */ },
  es: { /* mesma forma */ },
} as const;
```

Todo texto hoje cravado nos componentes migra pra cá, incluindo alt texts descritivos (foto da Tatiana, screenshots do LumeHostel em `ProvaDeTrabalho`). Alt texts que são nome próprio ("Código Itinerante") ficam iguais nos 3 idiomas.

### 3. Roteamento (`site/astro.config.mjs`)

```ts
i18n: {
  locales: ['pt', 'en', 'es'],
  defaultLocale: 'pt',
  routing: { prefixDefaultLocale: false },
},
```

`/` continua pt; `/en/` e `/es/` passam a existir.

### 4. Páginas novas (finas)

`src/pages/en/index.astro`, `src/pages/es/index.astro`, `src/pages/en/faq.astro`, `src/pages/es/faq.astro`, `src/pages/en/404.astro`, `src/pages/es/404.astro` — cada uma só monta os mesmos componentes de sempre (`Layout` + a composição existente), sem duplicar markup. `titulo`/`descricao` passados ao `Layout` vêm de `textos[idioma].meta.<pagina>`.

### 5. Componentes: leitura de idioma

Cada componente com texto cravado (`Hero`, `QuemSouEu`, `ProvaDeTrabalho`, `ComoFunciona`, `Manifesto`, `Dor`, `Proposta`, `Escopo`, `CtaFinal`, `BotaoWhatsApp`) ganha, no frontmatter:

```ts
import { idiomaAtual } from '../lib/i18n';
import { textos } from '../lib/textos';

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].<secao>;
```

E troca o texto literal por `txt.<campo>`.

### 6. Alternador de idioma

Réplica do padrão visual já usado no `Nav.astro` do motor: "PT / EN / ES", `getRelativeLocaleUrl()` de `astro:i18n`, `<span aria-current="page">` sem link pro idioma ativo, `<a hreflang>` pros outros dois. Sem gate de `idiomasDisponiveis` — sempre os 3.

Posicionamento por página:
- **Home**: perto da wordmark, no topo da Hero.
- **FAQ**: perto do link com o monograma, no topo da página.
- **404**: perto da wordmark central.

### 7. `Layout.astro`: meta multilíngue

- `idioma = idiomaAtual(Astro.currentLocale)`.
- `hreflang`: 3 `<link rel="alternate">` sempre presentes (pt/en/es), via `getRelativeLocaleUrl()` — sem gate, diferente do motor.
- `og:locale`/`html lang` por mapa fixo: `{ pt: 'pt_BR', en: 'en_US', es: 'es_ES' }` / `{ pt: 'pt-BR', en: 'en', es: 'es' }`.
- JSON-LD (`ProfessionalService` em toda página, `FAQPage` extra na FAQ): `description` e as perguntas/respostas da FAQ passam a vir de `textos[idioma]`.
- `canonical`: já funciona sem mudança (deriva de `Astro.url.pathname`).

### 8. WhatsApp localizado

`dados.mensagemWhatsApp` e o rótulo padrão do botão ("Chamar no WhatsApp") saem de `dados.ts` e viram `textos[idioma].botaoWhatsApp`. `BotaoWhatsApp.astro` lê o idioma e monta o link com a mensagem certa.

### 9. Sitemap

Automático via `@astrojs/sitemap`, sem configuração extra — já confirmado que pega rotas i18n no motor.

## Fora de escopo

- Detecção automática de idioma do navegador (`Accept-Language`) — troca continua manual, via alternador.
- Domínio/subdomínio dedicado pra versões em inglês/espanhol.
- Revisão de espanhol/inglês por falante nativo terceirizado.
- Qualquer mudança no motor `template/` ou em clientes (`clientes/`) — projeto isolado ao `site/`.

## Critérios de conclusão

- `npm run check` e `npm run build` limpos em `site/`.
- Build gera `dist/index.html`, `dist/en/index.html`, `dist/es/index.html` — e o mesmo trio pra `faq` e `404` — com conteúdo traduzido.
- Alternador PT/EN/ES funcional nas 3 páginas, sem levar de volta pra `/` ao navegar estando em `/en/` ou `/es/`.
- `hreflang`/`og:locale`/`lang` corretos nas 3 versões, nas 3 páginas.
- WhatsApp abre com mensagem no idioma da página atual.
- Teste manual no navegador cobrindo as 3 páginas × 3 idiomas (9 combinações).
