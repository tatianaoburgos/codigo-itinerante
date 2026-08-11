# Espanhol no LumeHostel — motor multilingue — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dar ao motor (`template/`) capacidade de servir N idiomas (não só pt/en) e ativar espanhol no LumeHostel (`/es/`), com o alternador do Nav virando "PT / EN / ES".

**Architecture:** Generaliza a implementação bilíngue existente (pt/en, já em produção) para multilíngue. `campoLocalizavel` no schema Zod vira `string | {pt: obrigatório, en?: opcional, es?: opcional}` — cada campo pode ter pt+en, pt+es, ou os três, com fallback pro pt quando o idioma pedido não tem chave. Pontos que hoje assumem "exatamente 2 idiomas" (`Nav.astro`, `Layout.astro`) passam a iterar sobre uma lista de idiomas ativos (`config.idiomasDisponiveis`) em vez de blocos condicionais fixos. Roteamento continua no i18n nativo do Astro, só ganha um terceiro locale (`/es/`).

**Tech Stack:** Astro 7 (roteamento i18n nativo, `astro:i18n`), Zod (schema), TypeScript, Node 24. Comandos em PowerShell (`$env:CLIENTE = '<slug>'; npm run build`, a partir de `template/`).

## Global Constraints

- Spec de referência: `docs/superpowers/specs/2026-08-11-lumehostel-espanhol-design.md`.
- **Só o LumeHostel é ativado nesta rodada.** `demo`, `maravista` e `site/` não podem mudar de comportamento nem de output de build.
- `campoLocalizavel`: `pt` é a única chave sempre obrigatória no objeto; `en` e `es` são opcionais e independentes entre si. `t(campo, idioma)` cai pro `pt` quando o campo é objeto e não tem a chave do idioma pedido.
- Tradução do conteúdo do LumeHostel: Claude traduz (mesmo método já usado pro inglês, commit `add339a`), autora revisa antes de publicar. Sem revisor nativo de espanhol.
- Variantes regionais: `og:locale` usa `es_ES` (mesma lógica do `en_US` já usado); `html lang` usa `es` plano (mesmo padrão do `en` plano já usado, só `pt` tem sufixo `pt-BR`).
- Ordem fixa do alternador e de qualquer iteração sobre idiomas ativos: `pt → en → es` (ordem de `idiomas` em `schema.ts`, não a ordem em que aparecem no `idiomasDisponiveis` do config.json).
- Não existe framework de testes no projeto (`CLAUDE.md`: "Não há testes nem linter configurados ainda") — verificação usa `npm run check`, builds reais (`CLIENTE=<x> npm run build`) e inspeção do `dist/` gerado via `Select-String`. Para lógica pura (schema, helper `t()`) alguns passos usam um script descartável em `template/` executado com `node --experimental-strip-types` e apagado logo depois.

---

## Task 1: Schema — `idiomas` com `es` e `campoLocalizavel` com en/es opcionais

**Files:**
- Modify: `template/src/lib/schema.ts` (arquivo inteiro)

**Interfaces:**
- Produces: `idiomas` (`['pt', 'en', 'es'] as const`), `Idioma` (tipo inferido, `'pt' | 'en' | 'es'`), `campoLocalizavel` (Zod schema, `string | {pt: string; en?: string; es?: string}`), `CampoLocalizavel` (tipo inferido).
- Consumes: nada (task raiz).

- [ ] **Step 1: Escrever o schema novo**

Substituir o conteúdo inteiro de `template/src/lib/schema.ts` por:

```ts
import { z } from 'zod';

/** Foto de um cliente: nome do arquivo na pasta `fotos/` + texto alternativo (acessibilidade/SEO). */
export const fotoSchema = z.object({
  arquivo: z.string().min(1),
  alt: z.string().min(1),
});

/** Texto do cliente: string única (um idioma) ou objeto por idioma. `pt` é
 *  sempre obrigatório (idioma base); `en`/`es` são opcionais e independentes
 *  entre si — um cliente pode ativar só um dos dois sem precisar traduzir
 *  pro outro. */
export const campoLocalizavel = z.union([
  z.string().min(1),
  z.object({
    pt: z.string().min(1),
    en: z.string().min(1).optional(),
    es: z.string().min(1).optional(),
  }),
]);

/** Mesma regra de `campoLocalizavel`, com limite de caracteres (ex.: meta description de SEO). */
function campoLocalizavelComMax(max: number) {
  return z.union([
    z.string().min(1).max(max),
    z.object({
      pt: z.string().min(1).max(max),
      en: z.string().min(1).max(max).optional(),
      es: z.string().min(1).max(max).optional(),
    }),
  ]);
}

/** Um tipo de acomodação do hostel (quarto compartilhado, suíte etc.). */
export const acomodacaoSchema = z.object({
  nome: campoLocalizavel,
  capacidade: campoLocalizavel,
  comodidades: z.array(campoLocalizavel).min(1),
  fotos: z.array(fotoSchema).min(1),
});

/** Arquivos de marca do cliente (pasta `marca/`), todos opcionais. */
export const marcaSchema = z.object({
  logo: z.string().min(1).optional(),
  favicon: z.string().min(1).optional(),
  simbolo: z.string().min(1).optional(),
  /** Ícone raster (PNG) para Apple touch icon e fallback de favicon. */
  appleTouchIcon: z.string().min(1).optional(),
  faviconPng: z.string().min(1).optional(),
  /** Vídeo full-bleed do hero (mp4/webm), no lugar da foto capa.jpg. */
  heroVideo: z.string().min(1).optional(),
  /** Frame estático (jpg) usado como poster do vídeo e fallback sem motion. */
  heroVideoPoster: z.string().min(1).optional(),
  /** Quando true, o logo (raster) aparece só no menu; a hero usa o nome em texto.
   *  Para logos tipo selo/circular que não escalam bem em tamanho grande. */
  logoApenasNoMenu: z.boolean().optional(),
  /** Quando true, a hero usa a composição centralizada (nome grande no meio,
   *  frase + símbolo no canto inferior direito) em vez do bloco padrão
   *  ancorado embaixo à esquerda. */
  heroCentralizado: z.boolean().optional(),
  /** Versão da frase (slogan) com quebra de linha manual (\n), usada só na
   *  composição centralizada da hero. Se ausente, usa o slogan normal. */
  heroFraseQuebrada: z.string().optional(),
});

/** Símbolos artísticos disponíveis na biblioteca compartilhada (SimboloComodidade.astro). */
export const simbolosComodidade = [
  'cozinha',
  'patio',
  'cowork',
  'rede',
  'churrasqueira',
  'jogos',
  'bagagem',
  'acolhedor',
  'vista-mar',
  'ar-condicionado',
  'recepcao',
  'wifi',
] as const;

/** Comodidade do hostel, opcionalmente ilustrada com foto ou com símbolo artístico. */
export const comodidadeSchema = z.object({
  nome: campoLocalizavel,
  descricao: campoLocalizavel.optional(),
  foto: fotoSchema.optional(),
  simbolo: z.enum(simbolosComodidade).optional(),
});

/** Seção de destaque full-bleed: foto que fica fixa enquanto a página rola, com frase por cima. */
export const destaqueSchema = z.object({
  frase: campoLocalizavel,
  foto: fotoSchema,
});

/** Ponto de interesse da região, com distância a partir do hostel. */
export const pontoRegiaoSchema = z.object({
  nome: campoLocalizavel,
  descricao: campoLocalizavel,
  distancia: z.string().min(1),
  foto: fotoSchema,
  credito: z.string().min(1).optional(),
});

/** Depoimento público real (Booking/Google), validável pelo cliente. */
export const depoimentoSchema = z.object({
  texto: campoLocalizavel,
  nome: z.string().min(1),
  fonte: z.string().min(1),
});

/** Idiomas com suporte no motor. */
export const idiomas = ['pt', 'en', 'es'] as const;

/**
 * Schema do config.json de cada cliente (`clientes/<slug>/config.json`).
 * A build falha se o arquivo não obedecer a este contrato.
 */
export const configClienteSchema = z.object({
  nome: z.string().min(1),
  marca: marcaSchema.optional(),
  slogan: campoLocalizavel,
  descricaoSeo: campoLocalizavelComMax(160),
  /** Idiomas em que o site deste cliente está disponível. Ausente = só pt (padrão de hoje). */
  idiomasDisponiveis: z.array(z.enum(idiomas)).optional(),
  sobre: z
    .object({
      historia: campoLocalizavel,
      foto: fotoSchema.optional(),
    })
    .optional(),
  acomodacoes: z.array(acomodacaoSchema).min(1).optional(),
  localizacao: z.object({
    endereco: z.string().min(1),
    /** Campos estruturados (opcionais) usados no PostalAddress do JSON-LD. */
    logradouro: z.string().min(1).optional(),
    bairro: z.string().min(1).optional(),
    cidade: z.string().min(1).optional(),
    uf: z.string().min(1).optional(),
    cep: z.string().min(1).optional(),
    mapsEmbedUrl: z.url().optional(),
    comoChegar: z.array(campoLocalizavel).optional(),
    /** Frase curta opcional, exibida ao fim da seção Localização. */
    resumo: campoLocalizavel.optional(),
  }),
  contato: z.object({
    whatsapp: z.string().regex(/^\d{12,13}$/, 'somente dígitos, com DDI e DDD (ex.: 5571999998888)'),
    email: z.email(),
    instagram: z.string().optional(),
    tiktok: z.string().optional(),
    facebook: z.string().optional(),
  }),
  comodidades: z.array(comodidadeSchema).min(1).optional(),
  regiao: z.array(pontoRegiaoSchema).min(1).optional(),
  depoimentos: z.array(depoimentoSchema).min(1).optional(),
  vibe: z.array(fotoSchema).min(1).optional(),
  destaques: z.array(destaqueSchema).max(2).optional(),
  /** Rótulos de seções futuras exibidos no nav sem link (roadmap do site). */
  navFuturo: z.array(z.string().min(1)).optional(),
});

export type ConfigCliente = z.infer<typeof configClienteSchema>;
export type Acomodacao = z.infer<typeof acomodacaoSchema>;
export type Foto = z.infer<typeof fotoSchema>;
export type Comodidade = z.infer<typeof comodidadeSchema>;
export type PontoRegiao = z.infer<typeof pontoRegiaoSchema>;
export type Depoimento = z.infer<typeof depoimentoSchema>;
export type Destaque = z.infer<typeof destaqueSchema>;
export type SimboloComodidade = (typeof simbolosComodidade)[number];
export type CampoLocalizavel = z.infer<typeof campoLocalizavel>;
export type Idioma = (typeof idiomas)[number];
```

- [ ] **Step 2: Verificar com script descartável — string solta, objetos parciais e completos, objeto sem pt**

Criar `template/_verificar_schema.ts`:

```ts
import { configClienteSchema } from './src/lib/schema';

const base = {
  nome: 'Teste',
  slogan: 'Slogan em pt',
  descricaoSeo: 'Descrição de teste com até 160 caracteres, sem problema nenhum aqui.',
  localizacao: { endereco: 'Rua Teste, 123' },
  contato: { whatsapp: '5571999998888', email: 'teste@teste.com' },
};

const casos: Array<[string, unknown, boolean]> = [
  ['string solta (compat com demo/maravista)', base.slogan, true],
  ['objeto só com pt', { pt: 'Ola' }, true],
  ['objeto pt+en (sem es)', { pt: 'Ola', en: 'Hello' }, true],
  ['objeto pt+es (sem en)', { pt: 'Ola', es: 'Hola' }, true],
  ['objeto pt+en+es completo', { pt: 'Ola', en: 'Hello', es: 'Hola' }, true],
  ['objeto sem pt (só en)', { en: 'Hello' }, false],
];

let falhas = 0;
for (const [descricao, slogan, devePassar] of casos) {
  const resultado = configClienteSchema.safeParse({ ...base, slogan });
  if (resultado.success !== devePassar) {
    console.error(`FALHOU: "${descricao}" — esperado ${devePassar ? 'válido' : 'inválido'}, obteve ${resultado.success ? 'válido' : 'inválido'}`);
    falhas++;
  }
}

if (falhas > 0) {
  console.error(`${falhas} caso(s) falharam.`);
  process.exit(1);
}
console.log('Schema: todos os casos passaram.');
```

Run (a partir de `template/`): `node --experimental-strip-types _verificar_schema.ts`
Expected: `Schema: todos os casos passaram.`

Depois de confirmar, apagar o arquivo: `Remove-Item _verificar_schema.ts` (dentro de `template/`).

- [ ] **Step 3: Rodar `npm run check` e builds de regressão**

A partir de `template/`:
```
npm run check
$env:CLIENTE = 'demo'; npm run build
$env:CLIENTE = 'maravista'; npm run build
$env:CLIENTE = 'lumehostel'; npm run build
```
Expected: os três passam sem erro (mudança de schema é aditiva — nenhum config foi editado ainda).

- [ ] **Step 4: Commit**

```bash
git add template/src/lib/schema.ts
git commit -m "Generaliza campoLocalizavel para en/es opcionais e adiciona es a idiomas"
```

---

## Task 2: `lib/i18n.ts` — fallback pro pt e `idiomaAtual` reconhecendo `es`

**Files:**
- Modify: `template/src/lib/i18n.ts` (arquivo inteiro)

**Interfaces:**
- Consumes: `CampoLocalizavel`, `Idioma` de `template/src/lib/schema.ts` (Task 1).
- Produces: `t(campo: CampoLocalizavel, idioma: Idioma): string` (agora com fallback pro `pt` quando o campo é objeto e não tem a chave pedida), `idiomaAtual(currentLocale: string | undefined): Idioma` (reconhece `'en'` e `'es'`) — usados por todo componente que renderiza texto (Tasks 5-7 e componentes já existentes que não mudam nesta rodada: `Footer`, `BotaoWhatsApp`, `Mapa`, `Hero`, `Acomodacoes`, `FotoDestaque`).

- [ ] **Step 1: Substituir o arquivo inteiro**

```ts
import type { CampoLocalizavel, Idioma } from './schema';

/** Resolve um campo de texto do cliente (string única ou objeto por idioma) para
 *  o idioma pedido. Se o campo for objeto e não tiver a chave do idioma pedido
 *  (idioma ativado no cliente, mas esse campo específico ainda não foi
 *  traduzido pra ele), cai para `pt`. */
export function t(campo: CampoLocalizavel, idioma: Idioma): string {
  if (typeof campo === 'string') return campo;
  return campo[idioma] ?? campo.pt;
}

/** Normaliza `Astro.currentLocale` (pode vir undefined) para um Idioma válido, com pt como padrão. */
export function idiomaAtual(currentLocale: string | undefined): Idioma {
  return currentLocale === 'en' || currentLocale === 'es' ? currentLocale : 'pt';
}
```

- [ ] **Step 2: Verificar com script descartável**

Criar `template/_verificar_i18n.ts`:

```ts
import { idiomaAtual, t } from './src/lib/i18n';

const casos: Array<[Parameters<typeof t>[0], 'pt' | 'en' | 'es', string]> = [
  ['Ola', 'pt', 'Ola'],
  ['Ola', 'es', 'Ola'],
  [{ pt: 'Ola', en: 'Hello' }, 'pt', 'Ola'],
  [{ pt: 'Ola', en: 'Hello' }, 'en', 'Hello'],
  [{ pt: 'Ola', en: 'Hello' }, 'es', 'Ola'],
  [{ pt: 'Ola', es: 'Hola' }, 'es', 'Hola'],
  [{ pt: 'Ola', en: 'Hello', es: 'Hola' }, 'es', 'Hola'],
];

let falhas = 0;
for (const [campo, idioma, esperado] of casos) {
  const resultado = t(campo, idioma);
  if (resultado !== esperado) {
    console.error(`FALHOU: t(${JSON.stringify(campo)}, "${idioma}") = "${resultado}", esperado "${esperado}"`);
    falhas++;
  }
}

if (idiomaAtual(undefined) !== 'pt') { console.error('FALHOU: idiomaAtual(undefined) deveria ser pt'); falhas++; }
if (idiomaAtual('es') !== 'es') { console.error('FALHOU: idiomaAtual("es") deveria ser es'); falhas++; }
if (idiomaAtual('fr') !== 'pt') { console.error('FALHOU: idiomaAtual("fr") deveria cair para pt'); falhas++; }

if (falhas > 0) { console.error(`${falhas} caso(s) falharam.`); process.exit(1); }
console.log('i18n: todos os casos passaram.');
```

Run: `node --experimental-strip-types _verificar_i18n.ts`
Expected: `i18n: todos os casos passaram.`

Apagar depois: `Remove-Item _verificar_i18n.ts`.

- [ ] **Step 3: `npm run check`**

Run: `npm run check` (dentro de `template/`)
Expected: passa sem erro.

- [ ] **Step 4: Commit**

```bash
git add template/src/lib/i18n.ts
git commit -m "Adiciona fallback pro pt em t() e reconhece es em idiomaAtual()"
```

---

## Task 3: `lib/textos.ts` — bloco `es` do dicionário de textos fixos

**Files:**
- Modify: `template/src/lib/textos.ts` (adiciona bloco `es`, mesma forma dos blocos `pt`/`en` existentes)

**Interfaces:**
- Consumes: nada.
- Produces: `textos.es` (mesma forma de `textos.pt`/`textos.en`) — consumido por Tasks 5-7 e pelos componentes já existentes (`Footer`, `BotaoWhatsApp`, `Mapa`) que já leem `textos[idioma]` genericamente.

- [ ] **Step 1: Adicionar o bloco `es`, logo após o fechamento do bloco `en` e antes de `} as const;`**

No arquivo `template/src/lib/textos.ts`, localizar o final do bloco `en` (a linha `},` que fecha `mapa: { titulo: 'Map' },` seguida da linha `} as const;`) e inserir o bloco `es` entre elas:

```ts
  es: {
    nav: {
      oHostel: 'El Hostel',
      acomodacoes: 'Habitaciones',
      comodidades: 'Comodidades',
      vibe: 'El ambiente',
      regiao: 'La zona',
      depoimentos: 'Reseñas',
      localizacao: 'Ubicación',
      abrirMenu: 'Abrir menú',
      fecharMenu: 'Cerrar menú',
    },
    footer: {
      faleConosco: 'Contáctanos',
      sigaAGente: 'Síguenos',
    },
    botaoWhatsApp: {
      rotuloPadrao: 'Reserva por WhatsApp',
      mensagem: (nome: string) =>
        `¡Hola! Vi el sitio web de ${nome} y me gustaría saber precios y disponibilidad.`,
    },
    pagina: {
      acomodacoesEyebrow: 'Habitaciones',
      acomodacoesTitulo: 'Elige tu rincón',
      acomodacoesCta: 'Consultar disponibilidad por WhatsApp',
      casaTitulo: 'La casa',
      comodidadesEyebrow: 'Comodidades',
      comodidadesTitulo: 'La vida por aquí',
      vibeEyebrow: 'El ambiente',
      vibeTitulo: 'Cómo es estar aquí',
      regiaoEyebrow: 'La zona',
      regiaoTitulo: 'Explora los alrededores',
      comoChegarTitulo: 'Cómo llegar',
      depoimentosEyebrow: 'Reseñas',
      depoimentosTitulo: 'Quién ha pasado por aquí',
      depoimentoTraduzido: 'Traducido del portugués.',
      localizacaoEyebrow: 'Ubicación',
      localizacaoTitulo: 'Dónde estamos',
      fotoCredito: 'Foto:',
      ctaFinalTitulo: 'Reserva directo con nosotros',
      ctaFinalTexto:
        'Escríbenos por WhatsApp y organiza tu estadía directo con quienes cuidan la casa.',
    },
    mapa: {
      titulo: 'Mapa',
    },
  },
```

- [ ] **Step 2: `npm run check`**

Run: `npm run check` (dentro de `template/`)
Expected: passa sem erro (valida que `pt`, `en` e `es` têm exatamente as mesmas chaves — se uma faltar em `es`, o uso mais adiante com `textos[idioma].pagina.xyz` acusaria erro de tipo quando `idioma` inclui `'es'`).

- [ ] **Step 3: Commit**

```bash
git add template/src/lib/textos.ts
git commit -m "Adiciona bloco es ao dicionario de textos fixos do motor"
```

---

## Task 4: Roteamento — `astro.config.mjs`, `pages/es/index.astro`, ativação no LumeHostel

**Files:**
- Modify: `template/astro.config.mjs`
- Create: `template/src/pages/es/index.astro`
- Modify: `clientes/lumehostel/config.json` (`idiomasDisponiveis` ganha `"es"`)

**Interfaces:**
- Consumes: `config` de `template/src/lib/cliente.ts` (já existente); `PaginaInicial` de `template/src/components/PaginaInicial.astro` (já existente, sem mudança nesta task).
- Produces: rota `/es/` funcional (redireciona para `/` quando o cliente não tem `"es"` em `idiomasDisponiveis`; renderiza a página quando tem).

- [ ] **Step 1: Adicionar `'es'` a `i18n.locales` em `astro.config.mjs`**

Em `template/astro.config.mjs`, dentro de `export default defineConfig({ ... })`, trocar:

```js
  i18n: {
    locales: ['pt', 'en'],
    defaultLocale: 'pt',
    routing: { prefixDefaultLocale: false },
  },
```

por:

```js
  i18n: {
    locales: ['pt', 'en', 'es'],
    defaultLocale: 'pt',
    routing: { prefixDefaultLocale: false },
  },
```

- [ ] **Step 2: Criar `pages/es/index.astro` com a mesma guarda de `pages/en/index.astro`**

```astro
---
import Layout from '../../layouts/Layout.astro';
import PaginaInicial from '../../components/PaginaInicial.astro';
import { config } from '../../lib/cliente';

if (!config.idiomasDisponiveis?.includes('es')) {
  return Astro.redirect('/', 302);
}
---

<Layout>
  <PaginaInicial />
</Layout>
```

- [ ] **Step 3: Verificar a guarda ANTES de ativar o espanhol no LumeHostel (estado "desligado")**

A partir de `template/`:
```
$env:CLIENTE = 'lumehostel'; npm run build
Select-String -Path dist/es/index.html -Pattern 'http-equiv="refresh"'
```
Expected: encontra a linha do `<meta http-equiv="refresh" ...>` — confirma que, sem `"es"` em `idiomasDisponiveis`, `/es/` redireciona para `/`.

- [ ] **Step 4: Ativar `"es"` no LumeHostel e verificar o estado "ligado"**

Editar `clientes/lumehostel/config.json`, linha 3:

```json
  "idiomasDisponiveis": ["pt", "en", "es"],
```

Rebuild:
```
$env:CLIENTE = 'lumehostel'; npm run build
Select-String -Path dist/es/index.html -Pattern 'http-equiv="refresh"'
Select-String -Path dist/es/index.html -Pattern 'Seu porto seguro'
```
Expected: o primeiro `Select-String` não encontra nada (sem redirecionamento); o segundo encontra "Seu porto seguro" (esperado — o conteúdo do config ainda não tem tradução `es`, então `t()` cai pro `pt`; isso é corrigido na Task 8. O importante aqui é confirmar que `/es/` renderiza a página completa, não o redirect).

- [ ] **Step 5: Confirmar que `demo` e `maravista` continuam redirecionando `/es/`**

```
$env:CLIENTE = 'demo'; npm run build
Select-String -Path dist/es/index.html -Pattern 'http-equiv="refresh"'
$env:CLIENTE = 'maravista'; npm run build
Select-String -Path dist/es/index.html -Pattern 'http-equiv="refresh"'
```
Expected: os dois encontram a linha do meta-refresh (nenhum dos dois tem `idiomasDisponiveis`).

- [ ] **Step 6: `npm run check`**

Run: `npm run check`
Expected: passa sem erro.

- [ ] **Step 7: Commit**

```bash
git add template/astro.config.mjs template/src/pages/es/index.astro clientes/lumehostel/config.json
git commit -m "Adiciona rota /es/ com guarda por idiomasDisponiveis e ativa espanhol no LumeHostel"
```

---

## Task 5: `Nav.astro` — alternador generalizado para N idiomas

**Files:**
- Modify: `template/src/components/Nav.astro` (arquivo inteiro)

**Interfaces:**
- Consumes: `idiomaAtual` (Task 2); `textos` (Task 3); `idiomas` (Task 1); `config.idiomasDisponiveis`; `getRelativeLocaleUrl` de `astro:i18n`.
- Produces: nenhuma interface nova para outras tasks — componente-folha.

- [ ] **Step 1: Substituir o arquivo inteiro**

```astro
---
import { getRelativeLocaleUrl } from 'astro:i18n';
import { config } from '../lib/cliente';
import { marca } from '../lib/fotos';
import { idiomaAtual } from '../lib/i18n';
import { idiomas } from '../lib/schema';
import { textos } from '../lib/textos';
import BotaoWhatsApp from './BotaoWhatsApp.astro';

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].nav;

// Idiomas ativos deste cliente, na ordem fixa pt -> en -> es (não a ordem em
// que aparecem no config.json).
const idiomasAtivos = idiomas.filter((i) => config.idiomasDisponiveis?.includes(i));

// Base do link "home" pro idioma atual — usada tanto pelo logo quanto pelos
// itens de âncora do menu (abas), pra não levar quem está em /en/ ou /es/ de
// volta pra página em português.
const linkBase = getRelativeLocaleUrl(idioma);

const abas = [
  { href: `${linkBase}#sobre`, rotulo: txt.oHostel },
  { href: `${linkBase}#acomodacoes`, rotulo: txt.acomodacoes },
  { href: `${linkBase}#comodidades`, rotulo: txt.comodidades },
  { href: `${linkBase}#vibe`, rotulo: txt.vibe },
  { href: `${linkBase}#regiao`, rotulo: txt.regiao },
  { href: `${linkBase}#depoimentos`, rotulo: txt.depoimentos },
  { href: `${linkBase}#localizacao`, rotulo: txt.localizacao },
]
  .filter((aba) => aba.href !== `${linkBase}#sobre` || config.sobre)
  .filter((aba) => aba.href !== `${linkBase}#acomodacoes` || config.acomodacoes)
  .filter((aba) => aba.href !== `${linkBase}#comodidades` || config.comodidades)
  .filter((aba) => aba.href !== `${linkBase}#vibe` || config.vibe)
  .filter((aba) => aba.href !== `${linkBase}#regiao` || config.regiao)
  .filter((aba) => aba.href !== `${linkBase}#depoimentos` || config.depoimentos)
  .filter((aba) => aba.href !== `${linkBase}#localizacao` || config.localizacao.mapsEmbedUrl);

const logo = config.marca?.logo ? marca(config.marca.logo) : undefined;

const mostrarAlternador = idiomasAtivos.length > 1;
---

<header
  data-solido="false"
  class="group fixed inset-x-0 top-0 z-50 border-b border-transparent bg-transparent text-white transition-colors duration-300 data-[solido=true]:border-sal data-[solido=true]:bg-espuma data-[solido=true]:text-noite"
>
  <nav
    aria-label="Principal"
    class="mx-auto flex max-w-5xl items-center justify-between gap-4 px-4 py-4"
  >
    <a
      href={linkBase}
      class="font-display text-xl font-bold focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-azulejo"
    >
      {/* SVG vetorial: `<img>` cru é intencional — astro:assets otimiza raster, não SVG. */}
      {logo ? <img src={logo.src} alt={config.nome} class="h-12 w-auto" /> : config.nome}
    </a>
    <div class="flex items-center gap-3">
      {
        mostrarAlternador && (
          <div class="flex items-center gap-1 font-mono text-xs font-bold tracking-widest uppercase">
            {idiomasAtivos.map((idiomaItem, indice) => (
              <>
                {indice > 0 && <span aria-hidden="true">/</span>}
                {idioma === idiomaItem ? (
                  <span aria-current="page">{idiomaItem.toUpperCase()}</span>
                ) : (
                  <a
                    href={getRelativeLocaleUrl(idiomaItem)}
                    hreflang={idiomaItem}
                    class="transition hover:text-fitinha focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-azulejo"
                  >
                    {idiomaItem.toUpperCase()}
                  </a>
                )}
              </>
            ))}
          </div>
        )
      }
      <BotaoWhatsApp />
      <button
        id="botao-menu-nav"
        popovertarget="menu-nav"
        popovertargetaction="toggle"
        aria-label={txt.abrirMenu}
        aria-expanded="false"
        aria-controls="menu-nav"
        data-rotulo-abrir={txt.abrirMenu}
        data-rotulo-fechar={txt.fecharMenu}
        class="flex h-8 w-8 flex-col items-center justify-center gap-[5px] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-azulejo"
      >
        <span class="block h-0.5 w-6 rounded-full bg-current transition-transform duration-200 group-has-[#menu-nav:popover-open]:translate-y-[7px] group-has-[#menu-nav:popover-open]:rotate-45"></span>
        <span class="block h-0.5 w-6 rounded-full bg-current transition-opacity duration-200 group-has-[#menu-nav:popover-open]:opacity-0"></span>
        <span class="block h-0.5 w-6 rounded-full bg-current transition-transform duration-200 group-has-[#menu-nav:popover-open]:-translate-y-[7px] group-has-[#menu-nav:popover-open]:-rotate-45"></span>
      </button>
    </div>
  </nav>

  <div
    id="menu-nav"
    popover
    class="fixed top-[4.5rem] right-4 left-auto m-0 flex-col gap-1 rounded-2xl border-0 bg-sal p-2 text-noite shadow-xl [&:popover-open]:flex"
  >
    {
      abas.map((aba) => (
        <a
          href={aba.href}
          class="rounded-lg px-3 py-2 text-sm font-bold transition hover:bg-azulejo/10 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-azulejo"
        >
          {aba.rotulo}
        </a>
      ))
    }
    {
      config.navFuturo?.map((rotulo) => (
        <span class="px-3 py-2 text-sm font-bold" title="Em breve" aria-hidden="true">
          {rotulo}
        </span>
      ))
    }
  </div>
</header>

<script>
  const header = document.querySelector<HTMLElement>('header[data-solido]');
  const hero = document.getElementById('hero');
  if (header && hero) {
    const observer = new IntersectionObserver(([entry]) => {
      header.dataset.solido = entry.isIntersecting ? 'false' : 'true';
    });
    observer.observe(hero);
  }

  const botaoMenu = document.getElementById('botao-menu-nav');
  const menu = document.getElementById('menu-nav');
  if (botaoMenu && menu) {
    const rotuloAbrir = botaoMenu.dataset.rotuloAbrir ?? 'Abrir menu';
    const rotuloFechar = botaoMenu.dataset.rotuloFechar ?? 'Fechar menu';
    menu.addEventListener('toggle', (evento) => {
      const aberto = (evento as ToggleEvent).newState === 'open';
      botaoMenu.setAttribute('aria-expanded', String(aberto));
      botaoMenu.setAttribute('aria-label', aberto ? rotuloFechar : rotuloAbrir);
    });
  }
</script>
```

Nota: `linkBase = getRelativeLocaleUrl(idioma)` substitui o antigo `idioma === 'en' ? linkEn : linkPt` — é a mesma resolução, só generalizada pra qualquer idioma da lista (inclusive `es`), preservando o comportamento já corrigido de manter a navegação de menu/logo dentro do idioma atual (não voltar pra `/` estando em `/en/` ou `/es/`).

- [ ] **Step 2: Build e checagem**

```
npm run check
$env:CLIENTE = 'lumehostel'; npm run build
Select-String -Path dist/index.html -Pattern '>EN<|>ES<'
Select-String -Path dist/en/index.html -Pattern '>PT<|>ES<'
Select-String -Path dist/es/index.html -Pattern '>PT<|>EN<'
Select-String -Path dist/es/index.html -Pattern 'href="/es#acomodacoes"'
```
Expected: `dist/index.html` (pt) mostra os links "EN" e "ES"; `dist/en/index.html` mostra "PT" e "ES" como links (com "EN" seria o `aria-current`, não um link, então não aparece na busca por `>EN<` isolado — ok se essa linha não achar nada nele, o que importa é achar PT e ES); `dist/es/index.html` mostra "PT" e "EN" como links; o item de menu de `dist/es/index.html` aponta pra `/es#acomodacoes` (não `/#acomodacoes` puro), confirmando que navegar pelo menu estando em `/es/` não sai do idioma.

```
$env:CLIENTE = 'demo'; npm run build
Select-String -Path dist/index.html -Pattern '>PT<|>EN<|>ES<'
```
Expected: nenhuma ocorrência — `demo` não tem `idiomasDisponiveis`, o alternador não aparece.

- [ ] **Step 3: Commit**

```bash
git add template/src/components/Nav.astro
git commit -m "Generaliza alternador do Nav para N idiomas (PT/EN/ES)"
```

---

## Task 6: `Layout.astro` — hreflang, og:locale e html lang generalizados

**Files:**
- Modify: `template/src/layouts/Layout.astro` (arquivo inteiro)

**Interfaces:**
- Consumes: `idiomaAtual`, `t` (Task 2); `idiomas`, `Idioma` (Task 1); `getRelativeLocaleUrl` de `astro:i18n`.
- Produces: nenhuma interface nova para outras tasks — usado pelas páginas (`pages/index.astro`, `pages/en/index.astro`, `pages/es/index.astro`), sem props novas.

- [ ] **Step 1: Substituir o arquivo inteiro**

```astro
---
import '../styles/global.css';
import { getRelativeLocaleUrl } from 'astro:i18n';
import Nav from '../components/Nav.astro';
import Footer from '../components/Footer.astro';
import { config } from '../lib/cliente';
import { foto, marca } from '../lib/fotos';
import { idiomaAtual, t } from '../lib/i18n';
import { idiomas, type Idioma } from '../lib/schema';

interface Props {
  titulo?: string;
  descricao?: string;
}

const idioma = idiomaAtual(Astro.currentLocale);
const descricaoSeo = t(config.descricaoSeo, idioma);
const sloganTraduzido = t(config.slogan, idioma);

const { titulo, descricao = descricaoSeo } = Astro.props;
const tituloPagina = titulo ? `${titulo} — ${config.nome}` : `${config.nome} — ${sloganTraduzido}`;

const temFaviconProprio = Boolean(config.marca?.favicon) || Boolean(config.marca?.faviconPng);
const favicon = config.marca?.favicon
  ? marca(config.marca.favicon).src
  : temFaviconProprio
    ? undefined
    : '/favicon.svg';
const faviconPng = config.marca?.faviconPng ? marca(config.marca.faviconPng).src : undefined;
const appleTouchIcon = config.marca?.appleTouchIcon
  ? marca(config.marca.appleTouchIcon).src
  : undefined;

// `Astro.site` vem da env em astro.config (domínio de produção da Vercel).
// Ausente em dev/preview local: URLs absolutas caem para relativas (degrada suave).
const site = Astro.site;
const absoluta = (caminho: string): string => (site ? new URL(caminho, site).href : caminho);

const canonical = site ? new URL(Astro.url.pathname, site).href : undefined;
const ogImagemArquivo = config.marca?.heroVideoPoster ?? 'capa.jpg';
const ogImagem = absoluta(foto(ogImagemArquivo).src);

// Idiomas ativos deste cliente, na ordem fixa pt -> en -> es. Gera um <link
// rel="alternate"> por idioma ativo; lista vazia (sem tags) quando o cliente
// só tem um idioma.
const idiomasAtivos = idiomas.filter((i) => config.idiomasDisponiveis?.includes(i));
const hrefsAlternativos =
  idiomasAtivos.length > 1
    ? idiomasAtivos.map((i) => ({ idioma: i, href: absoluta(getRelativeLocaleUrl(i)) }))
    : [];

const ogLocalePorIdioma: Record<Idioma, string> = { pt: 'pt_BR', en: 'en_US', es: 'es_ES' };
const htmlLangPorIdioma: Record<Idioma, string> = { pt: 'pt-BR', en: 'en', es: 'es' };
const ogLocale = ogLocalePorIdioma[idioma];
const htmlLang = htmlLangPorIdioma[idioma];

const loc = config.localizacao;
const endereco = loc.cidade
  ? {
      '@type': 'PostalAddress',
      streetAddress: loc.logradouro,
      addressLocality: loc.cidade,
      addressRegion: loc.uf,
      postalCode: loc.cep,
      addressCountry: 'BR',
    }
  : loc.endereco;

const dadosEstruturados = {
  '@context': 'https://schema.org',
  '@type': 'LodgingBusiness',
  name: config.nome,
  description: descricaoSeo,
  address: endereco,
  telephone: `+${config.contato.whatsapp}`,
  email: config.contato.email,
  image: ogImagem,
  ...(canonical && { url: canonical }),
  ...(config.contato.instagram && {
    sameAs: [`https://instagram.com/${config.contato.instagram}`],
  }),
};
---

<!doctype html>
<html lang={htmlLang} class="scroll-smooth">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    {favicon && <link rel="icon" type="image/svg+xml" href={favicon} />}
    {faviconPng && <link rel="icon" type="image/png" sizes="32x32" href={faviconPng} />}
    {appleTouchIcon && <link rel="apple-touch-icon" href={appleTouchIcon} />}
    {canonical && <link rel="canonical" href={canonical} />}
    {hrefsAlternativos.map(({ idioma: idiomaAlternativo, href }) => (
      <link rel="alternate" hreflang={idiomaAlternativo} href={href} />
    ))}
    <title>{tituloPagina}</title>
    <meta name="description" content={descricao} />

    <meta property="og:type" content="website" />
    <meta property="og:site_name" content={config.nome} />
    <meta property="og:title" content={tituloPagina} />
    <meta property="og:description" content={descricao} />
    <meta property="og:image" content={ogImagem} />
    <meta property="og:locale" content={ogLocale} />
    {canonical && <meta property="og:url" content={canonical} />}
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={tituloPagina} />
    <meta name="twitter:description" content={descricao} />
    <meta name="twitter:image" content={ogImagem} />

    <script
      type="application/ld+json"
      is:inline
      set:html={JSON.stringify(dadosEstruturados).replace(/</g, '\\u003c')}
    />
  </head>
  <body class="flex min-h-screen flex-col bg-espuma font-corpo text-noite">
    <Nav />
    <main class="flex-1">
      <slot />
    </main>
    <Footer />
    <script>
      const revelaveis = document.querySelectorAll<HTMLElement>('.revela');
      const observador = new IntersectionObserver(
        (entradas) => {
          for (const entrada of entradas) {
            if (entrada.isIntersecting) {
              entrada.target.classList.add('visivel');
              observador.unobserve(entrada.target);
            }
          }
        },
        { rootMargin: '0px 0px -10% 0px' },
      );
      revelaveis.forEach((el) => observador.observe(el));
    </script>
  </body>
</html>
```

- [ ] **Step 2: Build e checagem**

```
npm run check
$env:CLIENTE = 'lumehostel'; npm run build
Select-String -Path dist/index.html -Pattern 'lang="pt-BR"'
Select-String -Path dist/en/index.html -Pattern 'lang="en"'
Select-String -Path dist/es/index.html -Pattern 'lang="es"'
Select-String -Path dist/es/index.html -Pattern 'og:locale.*es_ES'
Select-String -Path dist/es/index.html -Pattern 'hreflang="pt"'
Select-String -Path dist/es/index.html -Pattern 'hreflang="en"'
Select-String -Path dist/es/index.html -Pattern 'hreflang="es"'
```
Expected: `lang` correto em cada versão; `dist/es/index.html` tem `og:locale` com `es_ES` e as três tags `hreflang` (pt, en, es) apontando pras três versões.

```
$env:CLIENTE = 'demo'; npm run build
Select-String -Path dist/index.html -Pattern 'hreflang'
```
Expected: nenhuma ocorrência — `demo` tem só 1 idioma ativo (nenhum, na verdade — sem `idiomasDisponiveis`), `hrefsAlternativos` fica vazio.

- [ ] **Step 3: Commit**

```bash
git add template/src/layouts/Layout.astro
git commit -m "Generaliza hreflang, og:locale e html lang para N idiomas"
```

---

## Task 7: `PaginaInicial.astro` — corrige nota de tradução hardcoded pra `en`

**Files:**
- Modify: `template/src/components/PaginaInicial.astro:232`

**Interfaces:**
- Consumes: `idioma` (variável local já existente no componente, resolvida por `idiomaAtual` na Task 2).
- Produces: nenhuma interface nova.

**Contexto do bug**: a nota "Traduzido do português" abaixo de cada depoimento hoje só aparece quando `idioma === 'en'`. Isso foi escrito antes de existir um terceiro idioma — com `es` ativo, um depoimento traduzido pro espanhol (`{pt, en, es}` ou `{pt, es}`) nunca mostraria a nota, porque a condição só reconhece `'en'`. A correção troca `idioma === 'en'` por `idioma !== 'pt'`, que cobre qualquer idioma não-português.

- [ ] **Step 1: Trocar a condição**

Em `template/src/components/PaginaInicial.astro`, trocar:

```astro
              {idioma === 'en' && typeof depoimento.texto !== 'string' && (
                <p class="mt-2 text-xs opacity-60">{txt.depoimentoTraduzido}</p>
              )}
```

por:

```astro
              {idioma !== 'pt' && typeof depoimento.texto !== 'string' && (
                <p class="mt-2 text-xs opacity-60">{txt.depoimentoTraduzido}</p>
              )}
```

- [ ] **Step 2: Build e checagem**

```
npm run check
$env:CLIENTE = 'lumehostel'; npm run build
Select-String -Path dist/en/index.html -Pattern 'Translated from Portuguese'
Select-String -Path dist/es/index.html -Pattern 'Traducido del portugu'
```
Expected: a versão `en` continua mostrando a nota (regressão-zero). A versão `es` passa a mostrar a nota também — antes desta correção, não mostraria (a condição só reconhecia `'en'`). Isso já funciona nesta task mesmo antes da Task 8 traduzir `depoimentos[].texto`: a nota em si vem de `textos.es.pagina.depoimentoTraduzido` (Task 3, já existe), e a condição só depende de `idioma !== 'pt'` — não depende de o depoimento já ter uma chave `es`. O texto do depoimento exibido continua em português (fallback do `t()`) até a Task 8; só a nota abaixo dele já aparece corretamente em espanhol.

- [ ] **Step 3: Commit**

```bash
git add template/src/components/PaginaInicial.astro
git commit -m "Corrige nota de traducao dos depoimentos para reconhecer qualquer idioma nao-pt"
```

---

## Task 8: Conteúdo do LumeHostel — tradução completa para espanhol

**Files:**
- Modify: `clientes/lumehostel/config.json` (arquivo inteiro)

**Interfaces:**
- Consumes: schema da Task 1 (campos aceitam `es` opcional).
- Produces: conteúdo final em pt/en/es do LumeHostel — task terminal, nenhuma outra task consome isso.

**Tradução (Claude → revisão da autora)**: mesmos campos que já têm `en` (commit `add339a`) ganham `es`: `slogan`, `descricaoSeo`, `sobre.historia`, `acomodacoes[].nome/capacidade/comodidades`, `localizacao.comoChegar/resumo`, `comodidades[].nome/descricao`, `regiao[].nome/descricao`, `depoimentos[].texto`, `destaques[].frase`. Campos que continuam sem tradução (mesma regra do inglês): nome de arquivo, telefone, e-mail, endereço estruturado, `credito` de foto, `nome`/`fonte` de depoimento.

- [ ] **Step 1: Substituir o arquivo inteiro**

```json
{
  "nome": "LumeHostel",
  "idiomasDisponiveis": ["pt", "en", "es"],
  "marca": { "logo": "logo-ambar.svg", "favicon": "simbolo-completo-terracota.svg", "simbolo": "simbolo-completo.svg", "appleTouchIcon": "apple-touch-icon.png", "faviconPng": "favicon-32.png" },
  "slogan": {
    "pt": "Seu porto seguro para renovar energias e seguir explorando",
    "en": "Your safe harbor to recharge and keep exploring",
    "es": "Tu puerto seguro para recargar energías y seguir explorando"
  },
  "descricaoSeo": {
    "pt": "LumeHostel em Manaíra, João Pessoa: hostel pensado para nômades digitais, a poucos minutos da praia.",
    "en": "LumeHostel in Manaíra, João Pessoa: a hostel designed for digital nomads, minutes from the beach.",
    "es": "LumeHostel en Manaíra, João Pessoa: hostel pensado para nómadas digitales, a pocos minutos de la playa."
  },
  "sobre": {
    "historia": {
      "pt": "O LumeHostel fica em Manaíra, a poucos minutos a pé da praia, e nasce como ponto de orientação para quem viaja trabalhando. Aqui a ideia é simples: oferecer um porto seguro para renovar energias entre uma jornada e outra, com espaço pensado para quem precisa de foco durante o dia e descanso à noite. Um ambiente acolhedor para nômades digitais.",
      "en": "LumeHostel is in Manaíra, just a short walk from the beach, and was created as a landmark for people who travel while they work. The idea here is simple: offer a safe harbor to recharge between one journey and the next, with space designed for those who need focus during the day and rest at night. A welcoming environment for digital nomads.",
      "es": "LumeHostel está en Manaíra, a pocos minutos a pie de la playa, y nace como punto de referencia para quienes viajan trabajando. La idea aquí es simple: ofrecer un puerto seguro para recargar energías entre un viaje y otro, con un espacio pensado para quienes necesitan concentración durante el día y descanso por la noche. Un ambiente acogedor para nómadas digitales."
    }
  },
  "acomodacoes": [
    {
      "nome": { "pt": "Dormitório Misto — 8 camas", "en": "Mixed Dorm — 8 beds", "es": "Dormitorio Mixto — 8 camas" },
      "capacidade": { "pt": "Quarto misto com 8 camas (beliches)", "en": "Mixed room with 8 beds (bunks)", "es": "Habitación mixta con 8 camas (literas)" },
      "comodidades": [
        { "pt": "Ar-condicionado", "en": "Air conditioning", "es": "Aire acondicionado" },
        { "pt": "Locker individual", "en": "Individual locker", "es": "Casillero individual" },
        { "pt": "Tomada individual por cama", "en": "Individual power outlet per bed", "es": "Enchufe individual por cama" },
        { "pt": "Toalhas inclusas", "en": "Towels included", "es": "Toallas incluidas" }
      ],
      "fotos": [
        { "arquivo": "dormitorio-misto-8.jpg", "alt": "Dormitório misto amplo com cama de solteiro e beliches, armário branco e janela com persiana" }
      ]
    },
    {
      "nome": { "pt": "Dormitório Feminino — 4 camas", "en": "Female Dorm — 4 beds", "es": "Dormitorio Femenino — 4 camas" },
      "capacidade": { "pt": "Quarto feminino com 4 camas (beliches)", "en": "Female room with 4 beds (bunks)", "es": "Habitación femenina con 4 camas (literas)" },
      "comodidades": [
        { "pt": "Ar-condicionado", "en": "Air conditioning", "es": "Aire acondicionado" },
        { "pt": "Locker individual", "en": "Individual locker", "es": "Casillero individual" },
        { "pt": "Tomada individual por cama", "en": "Individual power outlet per bed", "es": "Enchufe individual por cama" },
        { "pt": "Toalhas inclusas", "en": "Towels included", "es": "Toallas incluidas" }
      ],
      "fotos": [
        { "arquivo": "dormitorio-feminino-4.jpg", "alt": "Dormitório feminino com dois beliches de metal preto, armário e janela com grade decorativa" }
      ]
    },
    {
      "nome": { "pt": "Suíte Standard", "en": "Standard Suite", "es": "Suite Estándar" },
      "capacidade": { "pt": "2 pessoas, 1 cama de casal", "en": "2 people, 1 double bed", "es": "2 personas, 1 cama matrimonial" },
      "comodidades": [
        { "pt": "Ar-condicionado", "en": "Air conditioning", "es": "Aire acondicionado" },
        { "pt": "Locker individual", "en": "Individual locker", "es": "Casillero individual" },
        { "pt": "Tomada individual", "en": "Individual power outlet", "es": "Enchufe individual" },
        { "pt": "Toalhas inclusas", "en": "Towels included", "es": "Toallas incluidas" }
      ],
      "fotos": [
        { "arquivo": "suite-standard.jpg", "alt": "Suíte privativa com cama de casal, mesa de madeira, cadeiras e espelho de corpo inteiro" }
      ]
    },
    {
      "nome": { "pt": "Dormitório Misto — 6 camas", "en": "Mixed Dorm — 6 beds", "es": "Dormitorio Mixto — 6 camas" },
      "capacidade": { "pt": "Quarto misto com 6 camas (beliches)", "en": "Mixed room with 6 beds (bunks)", "es": "Habitación mixta con 6 camas (literas)" },
      "comodidades": [
        { "pt": "Ar-condicionado", "en": "Air conditioning", "es": "Aire acondicionado" },
        { "pt": "Locker individual", "en": "Individual locker", "es": "Casillero individual" },
        { "pt": "Tomada individual por cama", "en": "Individual power outlet per bed", "es": "Enchufe individual por cama" },
        { "pt": "Toalhas inclusas", "en": "Towels included", "es": "Toallas incluidas" }
      ],
      "fotos": [
        { "arquivo": "dormitorio-misto-6.jpg", "alt": "Dormitório misto com três beliches de metal e cortinas separando as camas" }
      ]
    },
    {
      "nome": { "pt": "Dormitório Feminino — 6 camas", "en": "Female Dorm — 6 beds", "es": "Dormitorio Femenino — 6 camas" },
      "capacidade": { "pt": "Quarto feminino com 6 camas (beliches)", "en": "Female room with 6 beds (bunks)", "es": "Habitación femenina con 6 camas (literas)" },
      "comodidades": [
        { "pt": "Ar-condicionado", "en": "Air conditioning", "es": "Aire acondicionado" },
        { "pt": "Locker individual", "en": "Individual locker", "es": "Casillero individual" },
        { "pt": "Tomada individual por cama", "en": "Individual power outlet per bed", "es": "Enchufe individual por cama" },
        { "pt": "Toalhas inclusas", "en": "Towels included", "es": "Toallas incluidas" }
      ],
      "fotos": [
        { "arquivo": "dormitorio-feminino-6.jpg", "alt": "Dormitório feminino com beliches de metal preto, armário branco e piso de cerâmica" }
      ]
    },
    {
      "nome": { "pt": "Quarto Duplo", "en": "Double Room", "es": "Habitación Doble" },
      "capacidade": { "pt": "2 pessoas, 1 cama de casal", "en": "2 people, 1 double bed", "es": "2 personas, 1 cama matrimonial" },
      "comodidades": [
        { "pt": "Ar-condicionado", "en": "Air conditioning", "es": "Aire acondicionado" },
        { "pt": "Locker individual", "en": "Individual locker", "es": "Casillero individual" },
        { "pt": "Tomada individual", "en": "Individual power outlet", "es": "Enchufe individual" },
        { "pt": "Toalhas inclusas", "en": "Towels included", "es": "Toallas incluidas" }
      ],
      "fotos": [
        { "arquivo": "quarto-duplo.jpg", "alt": "Quarto privativo com cama de casal, cortinas marrons, quadros na parede e mesa com cadeiras" }
      ]
    }
  ],
  "localizacao": {
    "endereco": "Av. Pombal, 1745 - Manaíra, João Pessoa - PB, 58038-242",
    "logradouro": "Av. Pombal, 1745",
    "bairro": "Manaíra",
    "cidade": "João Pessoa",
    "uf": "PB",
    "cep": "58038-242",
    "mapsEmbedUrl": "https://www.google.com/maps?q=LumeHostel,+Av.+Pombal+1745,+Manaira,+Joao+Pessoa&output=embed",
    "comoChegar": [
      { "pt": "Aeroporto Internacional de João Pessoa a cerca de 18 km", "en": "João Pessoa International Airport about 18 km away", "es": "Aeropuerto Internacional de João Pessoa a unos 18 km" },
      { "pt": "Rodoviária de João Pessoa a cerca de 9 km", "en": "João Pessoa bus station about 9 km away", "es": "Terminal de autobuses de João Pessoa a unos 9 km" },
      { "pt": "Praia de Manaíra a cerca de 8 minutos a pé", "en": "Manaíra Beach about an 8-minute walk", "es": "Playa de Manaíra a unos 8 minutos a pie" }
    ],
    "resumo": {
      "pt": "A poucos minutos da praia de Manaíra, no coração de João Pessoa.",
      "en": "Just minutes from Manaíra Beach, in the heart of João Pessoa.",
      "es": "A pocos minutos de la playa de Manaíra, en el corazón de João Pessoa."
    }
  },
  "contato": {
    "whatsapp": "5583988411745",
    "email": "lumehostel@gmail.com",
    "instagram": "lumehostel",
    "tiktok": "lumehostel"
  },
  "comodidades": [
    {
      "nome": { "pt": "Cozinha compartilhada", "en": "Shared kitchen", "es": "Cocina compartida" },
      "descricao": { "pt": "Geladeira, micro-ondas, purificador de água e utensílios à disposição dos hóspedes", "en": "Fridge, microwave, water purifier and utensils available for guests", "es": "Nevera, microondas, purificador de agua y utensilios a disposición de los huéspedes" },
      "simbolo": "cozinha",
      "foto": { "arquivo": "cozinha.jpg", "alt": "Cozinha compartilhada do LumeHostel, com balcão e banquetas" }
    },
    {
      "nome": { "pt": "Pátio externo", "en": "Outdoor patio", "es": "Patio exterior" },
      "descricao": { "pt": "Espaço com mesas para refeições e convivência entre hóspedes", "en": "Space with tables for meals and time together with other guests", "es": "Espacio con mesas para comidas y convivencia entre huéspedes" },
      "simbolo": "patio",
      "foto": { "arquivo": "jardim.jpg", "alt": "Pátio de entrada do LumeHostel com mesas de madeira e a fachada com o logo ao fundo" }
    },
    {
      "nome": { "pt": "Coworking ergonômico", "en": "Ergonomic coworking space", "es": "Coworking ergonómico" },
      "descricao": { "pt": "Mesas amplas e cadeiras confortáveis para render no trabalho", "en": "Spacious desks and comfortable chairs to get work done", "es": "Mesas amplias y sillas cómodas para rendir en el trabajo" },
      "simbolo": "cowork",
      "foto": { "arquivo": "coworking.jpg", "alt": "Sala de coworking do LumeHostel com mesas, cadeiras ergonômicas e notebooks junto à janela" }
    },
    {
      "nome": { "pt": "Espaço com redes", "en": "Hammock area", "es": "Zona de hamacas" },
      "descricao": { "pt": "Redes para descansar entre as atividades do dia", "en": "Hammocks to rest between the day's activities", "es": "Hamacas para descansar entre las actividades del día" },
      "simbolo": "rede",
      "foto": { "arquivo": "redario.jpg", "alt": "Redário do LumeHostel, com redes amarelas no corredor externo entre os quartos" }
    },
    {
      "nome": { "pt": "Churrasqueira", "en": "Barbecue area", "es": "Zona de parrilla" },
      "descricao": { "pt": "Para reunir a galera em volta do fogo", "en": "For gathering everyone around the fire", "es": "Para reunir a todos alrededor del fuego" },
      "simbolo": "churrasqueira"
    },
    {
      "nome": { "pt": "Sala de jogos", "en": "Games room", "es": "Sala de juegos" },
      "descricao": { "pt": "Diversão garantida entre um passeio e outro", "en": "Guaranteed fun between outings", "es": "Diversión garantizada entre un paseo y otro" },
      "simbolo": "jogos"
    },
    {
      "nome": { "pt": "Depósito de bagagem", "en": "Luggage storage", "es": "Depósito de equipaje" },
      "descricao": { "pt": "Suas malas guardadas antes do check-in e depois do check-out", "en": "Keep your bags safe before check-in and after check-out", "es": "Tus maletas guardadas antes del check-in y después del check-out" },
      "simbolo": "bagagem"
    },
    {
      "nome": { "pt": "Ambiente acolhedor", "en": "Welcoming atmosphere", "es": "Ambiente acogedor" },
      "descricao": { "pt": "Elogiado pelos hóspedes pelo aconchego e pela organização", "en": "Praised by guests for its coziness and organization", "es": "Elogiado por los huéspedes por su calidez y organización" },
      "simbolo": "acolhedor"
    }
  ],
  "regiao": [
    {
      "nome": { "pt": "Praia de Manaíra", "en": "Manaíra Beach", "es": "Playa de Manaíra" },
      "descricao": { "pt": "Praia urbana em frente ao bairro, com orla de bares e restaurantes", "en": "Urban beach right by the neighborhood, with a waterfront strip of bars and restaurants", "es": "Playa urbana frente al barrio, con un paseo marítimo de bares y restaurantes" },
      "distancia": "600 m",
      "foto": { "arquivo": "regiao-praia-manaira.jpg", "alt": "Faixa de areia e calçadão da Praia de Manaíra, com a orla ao fundo, em João Pessoa"},
      "credito": "Patrick / CC BY-SA 3.0"
    },
    {
      "nome": { "pt": "Orla do Bessa", "en": "Bessa Waterfront", "es": "Costa del Bessa" },
      "descricao": { "pt": "Orla vizinha a Manaíra, com calçadão à beira-mar", "en": "Waterfront next to Manaíra, with a seaside boardwalk", "es": "Costa vecina a Manaíra, con un paseo peatonal junto al mar" },
      "distancia": "750 m",
      "foto": { "arquivo": "regiao-orla-bessa.jpg", "alt": "Orla da Praia do Bessa em João Pessoa" },
      "credito": "Matheus Jampa da Silva / CC BY-SA 4.0"
    },
    {
      "nome": { "pt": "Pôr do sol no Jacaré", "en": "Sunset at Jacaré Beach", "es": "Atardecer en Jacaré" },
      "descricao": { "pt": "Praia em Cabedelo, na foz do Rio Paraíba, conhecida pelo pôr do sol", "en": "Beach in Cabedelo, at the mouth of the Paraíba River, known for its sunset", "es": "Playa en Cabedelo, en la desembocadura del río Paraíba, conocida por sus atardeceres" },
      "distancia": "10 km",
      "foto": { "arquivo": "regiao-por-do-sol-jacare.jpg", "alt": "Pôr do sol na Praia do Jacaré, em João Pessoa" },
      "credito": "Marinelson Almeida / CC BY 2.0"
    },
    {
      "nome": { "pt": "Centro Histórico", "en": "Historic Center", "es": "Centro Histórico" },
      "descricao": { "pt": "Conjunto de prédios históricos do Centro/Varadouro de João Pessoa", "en": "Cluster of historic buildings in João Pessoa's Centro/Varadouro district", "es": "Conjunto de edificios históricos del Centro/Varadouro de João Pessoa" },
      "distancia": "4 km",
      "foto": { "arquivo": "regiao-centro-historico.jpg", "alt": "Vista do Centro Histórico de João Pessoa" },
      "credito": "Rogerio121402 / CC BY-SA 4.0"
    },
    {
      "nome": { "pt": "Farol do Cabo Branco", "en": "Cabo Branco Lighthouse", "es": "Faro de Cabo Branco" },
      "descricao": { "pt": "Farol no ponto mais oriental das Américas, no bairro Cabo Branco", "en": "Lighthouse at the easternmost point of the Americas, in the Cabo Branco neighborhood", "es": "Faro en el punto más oriental de las Américas, en el barrio Cabo Branco" },
      "distancia": "3,1 km",
      "foto": { "arquivo": "regiao-farol-cabo-branco.jpg", "alt": "Farol do Cabo Branco, em João Pessoa" }
    },
    {
      "nome": { "pt": "Estação Cabo Branco", "en": "Cabo Branco Station", "es": "Estación Cabo Branco" },
      "descricao": { "pt": "Estação Cabo Branco de Ciência, Cultura e Artes, museu projetado por Oscar Niemeyer", "en": "Cabo Branco Station of Science, Culture and Arts, a museum designed by Oscar Niemeyer", "es": "Estación Cabo Branco de Ciencia, Cultura y Artes, museo diseñado por Oscar Niemeyer" },
      "distancia": "9 km",
      "foto": { "arquivo": "regiao-estacao-cabo-branco.jpg", "alt": "Estação Cabo Branco de Ciência, Cultura e Artes, em João Pessoa" },
      "credito": "A. Júnior / CC BY 2.0"
    }
  ],
  "depoimentos": [
    {
      "texto": {
        "pt": "Superou muito as minhas expectativas. É uma das melhores estruturas de Hostel que já encontrei. Tudo muito organizado, limpo, e nota-se muito capricho em tudo. Mas o que mais me chamou atenção: a equipe. Voltaria mais vezes só pela atenção, respeito, carinho e educação com a qual fui tratado.",
        "en": "It far exceeded my expectations. It's one of the best hostel setups I've ever found. Everything very organized, clean, and you can tell a lot of care went into it. But what struck me most: the team. I'd come back just for the attention, respect, care and courtesy I was treated with.",
        "es": "Superó ampliamente mis expectativas. Es una de las mejores estructuras de hostel que he encontrado. Todo muy organizado, limpio, y se nota mucho esmero en cada detalle. Pero lo que más me llamó la atención fue el equipo. Volvería solo por la atención, el respeto, el cariño y la amabilidad con la que fui tratado."
      },
      "nome": "Gabriel B.",
      "fonte": "via Google"
    },
    {
      "texto": {
        "pt": "Eu amei a experiência, é um ambiente acolhedor, tranquilo, me senti em casa. Se você procura um espaço que respeite a sua tranquilidade, descanso e ainda assim sugira atividades diferentes para te acolher e te fazer não se sentir sozinho na sua viagem, você vai ao lugar certo.",
        "en": "I loved the experience — it's a welcoming, peaceful environment, I felt right at home. If you're looking for a place that respects your peace and rest while still offering different activities to welcome you and keep you from feeling alone on your trip, this is the right place.",
        "es": "Amé la experiencia, es un ambiente acogedor, tranquilo, me sentí como en casa. Si buscas un espacio que respete tu tranquilidad y tu descanso, y que además te proponga actividades distintas para acogerte y hacer que no te sientas solo en tu viaje, llegaste al lugar correcto."
      },
      "nome": "Camila C.",
      "fonte": "via Google"
    },
    {
      "texto": {
        "pt": "Um dos melhores hostels que já fiquei. Muito limpo. Tinha noite de tacos, bate-papo com histórias de viajantes e teve uma aula de forró muito massa que participei e depois dançamos quadrilha. Foi muito divertido!",
        "en": "One of the best hostels I've stayed at. Very clean. There was taco night, chats swapping travel stories, and a really fun forró class I joined, and afterwards we danced quadrilha. It was a blast!",
        "es": "Uno de los mejores hostels en los que me he quedado. Muy limpio. Hubo noche de tacos, charlas con historias de viajeros y una clase de forró buenísima en la que participé, después bailamos quadrilha. ¡Fue muy divertido!"
      },
      "nome": "Desirree",
      "fonte": "via Booking"
    },
    {
      "texto": {
        "pt": "Feito de viajante para viajante. Ambiente acolhedor e familiar. Tudo muito limpo. Cozinha equipada. Quartos com ar-condicionado. Cowork excelente. Internet rápida.",
        "en": "Made by a traveler, for travelers. Welcoming, homey atmosphere. Everything very clean. Fully equipped kitchen. Air-conditioned rooms. Excellent coworking space. Fast internet.",
        "es": "Hecho de viajero para viajero. Ambiente acogedor y familiar. Todo muy limpio. Cocina equipada. Habitaciones con aire acondicionado. Coworking excelente. Internet rápido."
      },
      "nome": "Rudá A.",
      "fonte": "via Google"
    }
  ],
  "destaques": [
    {
      "frase": { "pt": "Fique à vontade: a casa também é sua", "en": "Make yourself at home: this house is yours too", "es": "Siéntete como en casa: esta también es tu casa" },
      "foto": { "arquivo": "destaque-cozinha.jpg", "alt": "Copa do LumeHostel com paredes amarelas, mural ondulado terracota e mesa de vidro com banquinhos" }
    },
    {
      "frase": { "pt": "Um porto seguro entre uma jornada e outra", "en": "A safe harbor between one journey and the next", "es": "Un puerto seguro entre un viaje y otro" },
      "foto": { "arquivo": "destaque-recepcao.jpg", "alt": "Recepção do LumeHostel banhada de sol, com balcão de madeira e vista para o pátio pelo portão decorado" }
    }
  ],
  "vibe": [
    { "arquivo": "vibe-patio-noite.jpg", "alt": "Pátio do LumeHostel à noite, com mesa comunitária e varal de luzes" },
    { "arquivo": "vibe-patio-entrada.jpg", "alt": "Pátio externo do LumeHostel visto da entrada, com mesas de madeira e o nome do hostel pintado na parede" },
    { "arquivo": "vibe-corredor-cores.jpg", "alt": "Corredor interno do LumeHostel com paredes amarela e terracota, geladeira e balcão com banquinhos" },
    { "arquivo": "vibe-mural-recados.jpg", "alt": "Parede de recados do LumeHostel, com mensagens e desenhos deixados por hóspedes" },
    { "arquivo": "vibe-entrada-frase.jpg", "alt": "Espaço de estar próximo à entrada do LumeHostel, com almofadas amarelas e quadro com frase inspiracional" }
  ]
}
```

- [ ] **Step 2: `npm run check`**

Run: `npm run check` (dentro de `template/`)
Expected: passa sem erro (schema já aceita `es` desde a Task 1).

- [ ] **Step 3: Commit**

```bash
git add clientes/lumehostel/config.json
git commit -m "Traduz conteudo do LumeHostel para espanhol (slogan, acomodacoes, comodidades, regiao, depoimentos, localizacao, destaques)"
```

---

## Task 9: Verificação final — builds dos 3 clientes e checklist manual no navegador

**Files:** nenhum arquivo novo — task de verificação.

**Interfaces:** nenhuma — task terminal.

- [ ] **Step 1: `npm run check` e builds dos 3 clientes**

A partir de `template/`:
```
npm run check
$env:CLIENTE = 'demo'; npm run build
$env:CLIENTE = 'maravista'; npm run build
$env:CLIENTE = 'lumehostel'; npm run build
```
Expected: os três passam sem erro. `demo`/`maravista` não têm `/es/index.html` funcional (redirect); `lumehostel` tem `dist/index.html`, `dist/en/index.html` e `dist/es/index.html` com conteúdo próprio.

- [ ] **Step 2: Confirmar conteúdo traduzido no `dist/es/` do LumeHostel**

```
Select-String -Path dist/es/index.html -Pattern 'Tu puerto seguro'
Select-String -Path dist/es/index.html -Pattern 'Elige tu rincón'
Select-String -Path dist/es/index.html -Pattern 'Traducido del portugu'
Select-String -Path dist/es/index.html -Pattern 'Reserva por WhatsApp'
Select-String -Path dist/es/index.html -Pattern 'Síguenos'
```
Expected: todas encontram ocorrência — slogan, título de seção, nota de tradução dos depoimentos, botão de WhatsApp e rótulo do rodapé, todos em espanhol.

- [ ] **Step 3: Rodar o preview local e abrir no navegador**

A partir de `template/`:
```
$env:CLIENTE = 'lumehostel'; npm run build; npm run preview
```

Abrir `http://localhost:4321/` (ou a porta que o preview indicar) e conferir manualmente:
1. Alternador no Nav mostra "PT / EN / ES", nos três estados (pt, en, es) o idioma atual aparece como texto simples (não link) e os outros dois como links.
2. Clicar em "ES" abre `/es/` com a página inteira renderizada em espanhol (hero, acomodações, comodidades, região, depoimentos, localização, CTA final).
3. Estando em `/es/`, clicar no logo e em qualquer item do menu de seção permanece em `/es/` (não volta pra `/`).
4. Depoimentos em `/es/` mostram a nota "Traducido del portugués." abaixo da citação.
5. Botão de WhatsApp em `/es/` abre com mensagem em espanhol (conferir o texto do link gerado, ex. inspecionar o `href`).
6. Rodapé em `/es/` mostra "Contáctanos" e "Síguenos" (se o LumeHostel tiver redes sociais configuradas).
7. `<html lang="es">`, `<meta property="og:locale" content="es_ES">` e as três tags `<link rel="alternate" hreflang="...">` (pt, en, es) presentes no `<head>` de `/es/` (inspecionar via devtools).
8. Voltar pra `/` (idioma pt) e `/en/`: nada mudou visualmente em relação ao comportamento já em produção (regressão-zero).
9. `demo` e `maravista`: confirmar que `/es/` desses clientes redireciona pra `/` (não é preciso abrir no navegador — já verificado via build na Task 4; só reconfirmar aqui como parte do checklist final se houver dúvida).

- [ ] **Step 4: Reportar o resultado do checklist pra autora**

Sem commit nesta task — é só verificação. Se todos os itens do Step 3 passarem, o projeto está pronto pra revisão final da autora antes do deploy manual (`vercel deploy --project lumehostel --cwd template --prod --yes`, fora do escopo deste plano).

---

## Nota final para a autora

Duas correções de escopo em relação à spec original, encontradas ao investigar o código real antes de escrever este plano:

1. **Task 7** corrige um bug pré-existente: a nota "Traduzido do português" nos depoimentos só reconhecia `idioma === 'en'`, então depoimentos traduzidos pro espanhol nunca mostrariam a nota. Não é uma regressão desta rodada — já existia desde a implementação do inglês, só ficou visível agora que há um terceiro idioma.
2. A tradução do conteúdo (Task 8) foi escrita por mim como parte deste plano, não como um placeholder a preencher depois — está pronta pra revisão sua antes do deploy.
