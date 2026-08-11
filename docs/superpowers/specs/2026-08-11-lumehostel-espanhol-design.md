# Espanhol no LumeHostel — motor generalizado para N idiomas (design)

## Contexto

O LumeHostel já está em produção com pt/en (spec `2026-07-31-lumehostel-i18n-design.md`, implementado e verificado em 2026-08-11). A autora pediu, na mesma conversa, duas coisas: espanhol no LumeHostel e, separadamente, versões pt/en/es no site da própria marca (`site/`). Este spec cobre só a primeira — o `site/` não tem nenhuma infraestrutura de idioma hoje (texto cravado direto em ~10 componentes, projeto Astro totalmente separado) e fica para um segundo ciclo de brainstorm depois que este projeto for implementado.

Levantamento no código mostrou que a implementação pt/en atual foi escrita para **exatamente 2 idiomas**, não para N idiomas — a suposição "são só dois" está espalhada em vários pontos:

- `lib/schema.ts`: `campoLocalizavel` é `string | {pt, en}`, objeto de 2 chaves ambas obrigatórias.
- `lib/i18n.ts`: `idiomaAtual()` só reconhece `'en'` explicitamente; qualquer outro valor cai pra `'pt'`.
- `lib/textos.ts`: dicionário com blocos `pt` e `en` só.
- `components/Nav.astro`: alternador escrito como dois blocos JSX fixos (PT, depois EN), não um loop sobre idiomas ativos.
- `layouts/Layout.astro`: variável chamada `bilingue`, mais `hrefAlternativaPt`/`hrefAlternativaEn` hardcoded para os `<link rel="alternate">`; `ogLocale`/`htmlLang` resolvidos por um `? :` binário.

Portanto este projeto não é "copiar o padrão do `en`" — é generalizar o motor de bilíngue para multilíngue (N idiomas, guardado por `idiomasDisponiveis` como já é hoje) e, com essa capacidade pronta, ativar espanhol no LumeHostel.

## Decisões fechadas nesta sessão

- **Escopo**: só o LumeHostel ganha espanhol nesta rodada. `demo` e `maravista` continuam sem `idiomasDisponiveis` (comportamento de hoje, inalterado). `site/` fica para um projeto separado.
- **Autoria da tradução**: Claude traduz o conteúdo do `config.json`, mesmo método usado para o inglês (commit `add339a`, sem revisor externo); a autora revisa por seção antes de publicar.
- **Schema de idiomas**: `campoLocalizavel` vira `string | {pt: obrigatório, en?: opcional, es?: opcional}` — `pt` é a única chave sempre exigida quando o campo usa a forma de objeto; `en` e `es` são independentes entre si (um cliente pode ativar só `es` sem precisar traduzir `en`, e vice-versa). Quando o idioma pedido não tem chave no objeto, cai para `pt` como fallback.
- **Variante regional do espanhol**: `es_ES` para `og:locale` (mesma lógica do `en_US` já usado — variante "padrão" reconhecida universalmente por crawlers/Open Graph, sem apostar em nacionalidade específica do hóspede). `htmlLang` usa `es` plano, mesmo padrão do `en` plano já usado hoje (só o `pt` tem sufixo, `pt-BR`).

## Design

### 1. Schema (`lib/schema.ts`)

```ts
export const idiomas = ['pt', 'en', 'es'] as const;

export const campoLocalizavel = z.union([
  z.string().min(1),
  z.object({
    pt: z.string().min(1),
    en: z.string().min(1).optional(),
    es: z.string().min(1).optional(),
  }),
]);
```

`idiomasDisponiveis` já é `z.array(z.enum(idiomas)).optional()` — passa a aceitar `'es'` automaticamente assim que `idiomas` incluir o valor, sem mudança adicional de schema. `campoLocalizavelComMax` recebe o mesmo tratamento (pt obrigatório, en/es opcionais).

### 2. Fallback de tradução (`lib/i18n.ts`)

```ts
export function t(campo: CampoLocalizavel, idioma: Idioma): string {
  if (typeof campo === 'string') return campo;
  return campo[idioma] ?? campo.pt;
}

export function idiomaAtual(currentLocale: string | undefined): Idioma {
  return currentLocale === 'en' || currentLocale === 'es' ? currentLocale : 'pt';
}
```

### 3. Texto fixo do motor (`lib/textos.ts`)

Bloco `es` novo, mesma forma dos blocos `pt`/`en` existentes (nav, footer, botão WhatsApp com mensagem em espanhol, títulos/eyebrows de seção, texto do mapa). `depoimentoTraduzido` em espanhol: "Traducido del portugués."

### 4. Roteamento

`astro.config.mjs`: `i18n.locales` vira `['pt', 'en', 'es']`. Nova rota `template/src/pages/es/index.astro`, mesmo padrão fino de `en/index.astro` — redireciona para `/` se `idiomasDisponiveis` do cliente ativo não incluir `'es'`.

### 5. `Nav.astro`: alternador generalizado

O bloco PT/EN hardcoded (dois `{idioma === 'x' ? <span> : <a>}` fixos) vira um loop sobre os idiomas ativos do cliente (`config.idiomasDisponiveis`), usando `getRelativeLocaleUrl(idioma)` para cada um. Renderiza como texto atual (`<span aria-current="page">`) para o idioma ativo e link para os demais, na ordem `pt → en → es`. Com os 3 ativos no LumeHostel, o alternador mostra "PT / EN / ES".

### 6. `Layout.astro`: generalização de bilíngue para N idiomas

- `bilingue` (boolean) vira a lista de idiomas ativos (`config.idiomasDisponiveis ?? ['pt']`), usada para decidir se emite tags de idioma alternativo.
- `hrefAlternativaPt`/`hrefAlternativaEn` hardcoded viram um loop que gera um `<link rel="alternate" hreflang="X">` por idioma ativo (incluindo `es` quando presente).
- `ogLocale`: mapa `{pt: 'pt_BR', en: 'en_US', es: 'es_ES'}`.
- `htmlLang`: mapa `{pt: 'pt-BR', en: 'en', es: 'es'}`.

### 7. Conteúdo do LumeHostel (`clientes/lumehostel/config.json`)

Tradução para espanhol dos mesmos campos que ganharam inglês no commit `add339a`: `slogan`, `acomodacoes` (nome/capacidade/comodidades), `comodidades` (nome/descrição), `regiao` (nome/descrição), `depoimentos` (texto), `localizacao` (resumo/comoChegar). `idiomasDisponiveis` passa de `["pt", "en"]` para `["pt", "en", "es"]`.

## Fora de escopo

- `demo`, `maravista` — nenhuma mudança de conteúdo ou comportamento; seguem sem `idiomasDisponiveis`.
- `site/` (site da marca) — projeto separado, brainstorm próprio depois deste.
- Revisão de espanhol por falante nativo terceirizado.
- Detecção automática de idioma do navegador (`Accept-Language`) — troca continua manual, via alternador no Nav.
- Domínio/subdomínio dedicado para a versão em espanhol.

## Critérios de conclusão

- `npm run check` passa em `template/`.
- `CLIENTE=demo npm run build` e `CLIENTE=maravista npm run build` continuam passando sem alteração de output; `/es/` nesses builds redireciona para `/` (igual `/en/` já faz).
- `CLIENTE=lumehostel npm run build` gera `dist/index.html` (pt), `dist/en/index.html` (en) e `dist/es/index.html` (es) com conteúdo traduzido, incluindo depoimentos com a nota "Traducido del portugués."
- Alternador "PT / EN / ES" visível no Nav do LumeHostel, ausente no `demo` e no `maravista`.
- `hreflang` presente nas três versões do LumeHostel; `og:locale`/`lang` corretos em cada uma (`pt_BR`/`pt-BR`, `en_US`/`en`, `es_ES`/`es`).
- Teste manual no navegador: alternar entre PT/EN/ES troca a página mantendo visual, conteúdo e metadados no idioma certo, sem voltar para `/` ao navegar pelo menu/logo estando em `/en/` ou `/es/`.
