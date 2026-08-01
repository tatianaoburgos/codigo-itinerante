# Site bilíngue (pt/en) — motor + LumeHostel — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dar ao motor (`template/`) capacidade de servir um site em inglês (`/en/`) além do português (`/`), com alternador de idioma no Nav — ativada nesta rodada só para o LumeHostel (`idiomasDisponiveis` no `config.json`); `demo`, `maravista` e `site/` continuam exatamente como estão.

**Architecture:** Roteamento i18n nativo do Astro (`i18n` em `astro.config.mjs`, pasta `src/pages/en/`). Cada campo de texto do cliente vira `string` (um idioma) ou `{ pt, en }` (união no schema Zod) — resolvido em runtime de build por um helper `t()`. Texto fixo do motor (títulos de seção, rótulos de menu, mensagens de WhatsApp) vive num dicionário `pt`/`en` separado do `config.json`. `Astro.currentLocale`, disponível em qualquer `.astro` a partir da config de i18n, informa qual idioma renderizar.

**Tech Stack:** Astro 7 (roteamento i18n nativo, `astro:i18n`), Zod (schema), TypeScript, Node 24 (ambiente local — `--experimental-strip-types` usado só para scripts de verificação descartáveis, não entra no repo).

## Global Constraints

- Spec de referência: `docs/superpowers/specs/2026-07-31-lumehostel-i18n-design.md`.
- **Só o LumeHostel é ativado nesta rodada.** `demo`, `maravista` e `site/` não podem mudar de comportamento nem de output de build.
- Todo config existente (`demo`, `maravista`) deve continuar válido sem qualquer edição — a união de tipos aceita string solta.
- Alternador de idioma no Nav: texto simples "PT / EN" (duas letras clicáveis lado a lado, sem bandeira) — decisão já aprovada, não reabrir.
- URL da versão em inglês: `/en/` (prefixo de rota), não subdomínio.
- Depoimentos traduzidos vêm com nota "Traduzido do português." (pt) / "Translated from Portuguese." (en) abaixo da citação, só na versão en.
- Nomes de arquivo, telefone, e-mail, endereço (CEP/UF/cidade/logradouro/endereço completo), crédito de foto, nome e fonte de depoimento **não são traduzidos** — permanecem string simples mesmo no LumeHostel.
- Alt text de foto (`foto.alt`) **fica fora de escopo nesta rodada** — permanece só em português mesmo em `/en/` (limitação conhecida, não é esquecimento; ver nota na Task 11).
- Comandos de build usam `$env:CLIENTE = '<slug>'; npm run build` (PowerShell) a partir de `template/`.
- Não existe framework de testes no projeto (`CLAUDE.md`: "Não há testes nem linter configurados ainda") — verificação usa `npm run check`, builds reais (`CLIENTE=<x> npm run build`) e inspeção do `dist/` gerado. Para lógica pura (schema, helper `t()`) alguns passos usam um script descartável em `template/` executado com `node --experimental-strip-types` e apagado logo depois — não é um arquivo de teste permanente, é só uma forma barata de rodar o código antes de existir uma página real que o exercite.

---

## Task 1: Schema — campo bilíngue, `idiomasDisponiveis` e `destaque.frase`

**Files:**
- Modify: `template/src/lib/schema.ts` (arquivo inteiro — a mudança toca a maior parte dele)

**Interfaces:**
- Produces: `campoLocalizavel` (Zod schema, `string | { pt: string; en: string }`), `CampoLocalizavel` (tipo inferido), `idiomas` (`['pt', 'en'] as const`), `Idioma` (tipo inferido), campo `idiomasDisponiveis?: Idioma[]` em `ConfigCliente`.
- Consumes: nada (task raiz).

**Nota de escopo**: o spec (`docs/superpowers/specs/2026-07-31-lumehostel-i18n-design.md`, seção 3) lista os campos de prosa a tornar bilíngues, mas não incluiu `destaque.frase` — uma omissão da enumeração, não uma decisão deliberada (o LumeHostel usa `destaques` com 2 itens reais; sem tradução, a página em inglês mostraria a frase em português bem no meio de uma seção full-bleed). Esta task já inclui `destaque.frase` na lista, como correção de escopo. Avise a autora disso ao final do plano.

**Nota de dependência**: o bloco `contato` abaixo já inclui `tiktok`/`facebook` (strings simples, não traduzidas — são nomes de plataforma) porque o plano `docs/superpowers/plans/2026-07-31-redes-sociais-rodape.md` foi commitado antes deste (`6330f7b`, `713c212`) e já adicionou esses dois campos ao `schema.ts` real. Esta task parte desse estado — não reverte os campos.

- [ ] **Step 1: Escrever o schema novo**

Substituir o conteúdo inteiro de `template/src/lib/schema.ts** por:

```ts
import { z } from 'zod';

/** Foto de um cliente: nome do arquivo na pasta `fotos/` + texto alternativo (acessibilidade/SEO). */
export const fotoSchema = z.object({
  arquivo: z.string().min(1),
  alt: z.string().min(1),
});

/** Texto do cliente: string única (um idioma) ou par pt/en (cliente bilíngue). */
export const campoLocalizavel = z.union([
  z.string().min(1),
  z.object({ pt: z.string().min(1), en: z.string().min(1) }),
]);

/** Mesma regra de `campoLocalizavel`, com limite de caracteres (ex.: meta description de SEO). */
function campoLocalizavelComMax(max: number) {
  return z.union([
    z.string().min(1).max(max),
    z.object({ pt: z.string().min(1).max(max), en: z.string().min(1).max(max) }),
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
export const idiomas = ['pt', 'en'] as const;

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

- [ ] **Step 2: Verificar que configs existentes (string solta) continuam válidos e que par incompleto falha**

Criar um script descartável `template/_verificar_schema.ts`:

```ts
import { configClienteSchema } from './src/lib/schema';

const base = {
  nome: 'Teste',
  slogan: 'Slogan em pt',
  descricaoSeo: 'Descrição de teste com até 160 caracteres, sem problema nenhum aqui.',
  localizacao: { endereco: 'Rua Teste, 123' },
  contato: { whatsapp: '5571999998888', email: 'teste@teste.com' },
};

// 1. String solta continua válida (compatibilidade com demo/maravista)
const r1 = configClienteSchema.safeParse(base);
if (!r1.success) throw new Error('FALHOU: config com strings soltas deveria ser válido');

// 2. Par {pt, en} completo é válido
const r2 = configClienteSchema.safeParse({
  ...base,
  slogan: { pt: 'Slogan em pt', en: 'Slogan in en' },
  idiomasDisponiveis: ['pt', 'en'],
});
if (!r2.success) throw new Error('FALHOU: par {pt, en} completo deveria ser válido');

// 3. Par incompleto (falta en) FALHA
const r3 = configClienteSchema.safeParse({
  ...base,
  slogan: { pt: 'Slogan em pt' },
});
if (r3.success) throw new Error('FALHOU: par incompleto deveria ser rejeitado pelo schema');

console.log('Schema: os 3 casos passaram.');
```

Run (a partir de `template/`): `node --experimental-strip-types _verificar_schema.ts`
Expected: `Schema: os 3 casos passaram.`

Depois de confirmar, apagar o arquivo: `rm template/_verificar_schema.ts` (ou `Remove-Item` no PowerShell).

- [ ] **Step 3: Rodar `npm run check` e builds de regressão**

A partir de `template/`:
```
npm run check
$env:CLIENTE = 'demo'; npm run build
$env:CLIENTE = 'maravista'; npm run build
$env:CLIENTE = 'lumehostel'; npm run build
```
Expected: os três passam sem erro (nenhum config foi editado ainda — a mudança de schema é aditiva).

- [ ] **Step 4: Commit**

```bash
git add template/src/lib/schema.ts
git commit -m "Adiciona suporte a campo bilíngue (pt/en) e idiomasDisponiveis ao schema de cliente"
```

---

## Task 2: `lib/i18n.ts` — helpers `t()` e `idiomaAtual()`

**Files:**
- Create: `template/src/lib/i18n.ts`

**Interfaces:**
- Consumes: `CampoLocalizavel`, `Idioma` de `template/src/lib/schema.ts` (Task 1).
- Produces: `t(campo: CampoLocalizavel, idioma: Idioma): string`, `idiomaAtual(currentLocale: string | undefined): Idioma` — usados por todo componente que renderiza texto (Tasks 5-10).

- [ ] **Step 1: Criar o arquivo**

```ts
import type { CampoLocalizavel, Idioma } from './schema';

/** Resolve um campo de texto do cliente (string única ou par pt/en) para o idioma pedido. */
export function t(campo: CampoLocalizavel, idioma: Idioma): string {
  return typeof campo === 'string' ? campo : campo[idioma];
}

/** Normaliza `Astro.currentLocale` (pode vir undefined) para um Idioma válido, com pt como padrão. */
export function idiomaAtual(currentLocale: string | undefined): Idioma {
  return currentLocale === 'en' ? 'en' : 'pt';
}
```

- [ ] **Step 2: Verificar com script descartável**

Criar `template/_verificar_i18n.ts`:

```ts
import { idiomaAtual, t } from './src/lib/i18n';

const casos: Array<[Parameters<typeof t>[0], 'pt' | 'en', string]> = [
  ['Ola', 'pt', 'Ola'],
  ['Ola', 'en', 'Ola'],
  [{ pt: 'Ola', en: 'Hello' }, 'pt', 'Ola'],
  [{ pt: 'Ola', en: 'Hello' }, 'en', 'Hello'],
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
if (idiomaAtual('pt') !== 'pt') { console.error('FALHOU: idiomaAtual("pt") deveria ser pt'); falhas++; }
if (idiomaAtual('en') !== 'en') { console.error('FALHOU: idiomaAtual("en") deveria ser en'); falhas++; }
if (idiomaAtual('fr') !== 'pt') { console.error('FALHOU: idiomaAtual("fr") deveria cair para pt'); falhas++; }

if (falhas > 0) { console.error(`${falhas} caso(s) falharam.`); process.exit(1); }
console.log('i18n: todos os casos passaram.');
```

Run: `node --experimental-strip-types _verificar_i18n.ts`
Expected: `i18n: todos os casos passaram.`

Apagar depois: `rm template/_verificar_i18n.ts`.

- [ ] **Step 3: `npm run check`**

Run: `npm run check` (dentro de `template/`)
Expected: passa sem erro.

- [ ] **Step 4: Commit**

```bash
git add template/src/lib/i18n.ts
git commit -m "Adiciona helpers t() e idiomaAtual() para resolver texto por idioma"
```

---

## Task 3: `lib/textos.ts` — dicionário de textos fixos do motor

**Files:**
- Create: `template/src/lib/textos.ts`

**Interfaces:**
- Consumes: nada.
- Produces: `textos: { pt: {...}, en: {...} }` (const, tipo inferido) — namespaces `nav`, `footer`, `botaoWhatsApp`, `pagina`, `mapa`. Consumido por Tasks 5-10.

**Nota de dependência**: `footer.sigaAGente` foi adicionado à lista de chaves — é rótulo do bloco "Siga a gente" do rodapé (plano `redes-sociais-rodape.md`, commit `6330f7b`), texto de interface como `faleConosco`, não nome de marca/plataforma, então precisa de tradução como qualquer outro rótulo fixo do motor.

- [ ] **Step 1: Criar o arquivo**

```ts
export const textos = {
  pt: {
    nav: {
      oHostel: 'O Hostel',
      acomodacoes: 'Acomodações',
      comodidades: 'Comodidades',
      vibe: 'A vibe',
      regiao: 'A região',
      depoimentos: 'Depoimentos',
      localizacao: 'Localização',
      abrirMenu: 'Abrir menu',
      fecharMenu: 'Fechar menu',
    },
    footer: {
      faleConosco: 'Fale conosco',
      sigaAGente: 'Siga a gente',
    },
    botaoWhatsApp: {
      rotuloPadrao: 'Reserve pelo WhatsApp',
      mensagem: (nome: string) =>
        `Ola! Vi o site do ${nome} e quero saber valores e disponibilidade.`,
    },
    pagina: {
      acomodacoesEyebrow: 'Acomodações',
      acomodacoesTitulo: 'Escolha seu canto',
      acomodacoesCta: 'Consultar disponibilidade no WhatsApp',
      casaTitulo: 'A casa',
      comodidadesEyebrow: 'Comodidades',
      comodidadesTitulo: 'A vida por aqui',
      vibeEyebrow: 'A vibe',
      vibeTitulo: 'Como é ficar aqui',
      regiaoEyebrow: 'A região',
      regiaoTitulo: 'Explore os arredores',
      comoChegarTitulo: 'Como chegar',
      depoimentosEyebrow: 'Depoimentos',
      depoimentosTitulo: 'Quem passou por aqui',
      depoimentoTraduzido: 'Traduzido do português.',
      localizacaoEyebrow: 'Localização',
      localizacaoTitulo: 'Onde estamos',
      fotoCredito: 'Foto:',
      ctaFinalTitulo: 'Reserve direto com a gente',
      ctaFinalTexto: 'Chame no WhatsApp e combine sua estadia direto com quem cuida da casa.',
    },
    mapa: {
      titulo: 'Mapa',
    },
  },
  en: {
    nav: {
      oHostel: 'The Hostel',
      acomodacoes: 'Rooms',
      comodidades: 'Amenities',
      vibe: 'The vibe',
      regiao: 'The area',
      depoimentos: 'Reviews',
      localizacao: 'Location',
      abrirMenu: 'Open menu',
      fecharMenu: 'Close menu',
    },
    footer: {
      faleConosco: 'Get in touch',
      sigaAGente: 'Follow us',
    },
    botaoWhatsApp: {
      rotuloPadrao: 'Book on WhatsApp',
      mensagem: (nome: string) =>
        `Hi! I saw ${nome}'s website and I'd like to know prices and availability.`,
    },
    pagina: {
      acomodacoesEyebrow: 'Rooms',
      acomodacoesTitulo: 'Pick your corner',
      acomodacoesCta: 'Check availability on WhatsApp',
      casaTitulo: 'The house',
      comodidadesEyebrow: 'Amenities',
      comodidadesTitulo: 'Life around here',
      vibeEyebrow: 'The vibe',
      vibeTitulo: 'What it feels like here',
      regiaoEyebrow: 'The area',
      regiaoTitulo: 'Explore the surroundings',
      comoChegarTitulo: 'Getting here',
      depoimentosEyebrow: 'Reviews',
      depoimentosTitulo: 'Who has stayed here',
      depoimentoTraduzido: 'Translated from Portuguese.',
      localizacaoEyebrow: 'Location',
      localizacaoTitulo: 'Where we are',
      fotoCredito: 'Photo:',
      ctaFinalTitulo: 'Book directly with us',
      ctaFinalTexto:
        "Message us on WhatsApp and arrange your stay directly with the people who run the house.",
    },
    mapa: {
      titulo: 'Map',
    },
  },
} as const;
```

- [ ] **Step 2: `npm run check`**

Run: `npm run check` (dentro de `template/`)
Expected: passa sem erro (valida que `pt` e `en` têm exatamente as mesmas chaves — se uma faltar, o uso mais adiante com `textos[idioma].pagina.xyz` acusaria erro de tipo).

- [ ] **Step 3: Commit**

```bash
git add template/src/lib/textos.ts
git commit -m "Adiciona dicionario pt/en de textos fixos do motor (nav, rodape, botao WhatsApp, secoes)"
```

---

## Task 4: Roteamento — `astro.config.mjs`, `PaginaInicial.astro`, `pages/en/index.astro`

**Files:**
- Modify: `template/astro.config.mjs`
- Create: `template/src/components/PaginaInicial.astro` (corpo movido de `pages/index.astro`, sem alteração de conteúdo nesta task — só extração)
- Modify: `template/src/pages/index.astro` (vira casca fina)
- Create: `template/src/pages/en/index.astro`
- Modify: `clientes/lumehostel/config.json` (adiciona `idiomasDisponiveis`)

**Interfaces:**
- Consumes: `config` de `template/src/lib/cliente.ts` (já existente).
- Produces: rota `/en/` funcional (redireciona para `/` quando o cliente não tem `"en"` em `idiomasDisponiveis`; renderiza a página quando tem). Componente `PaginaInicial.astro` sem props, usado por `pages/index.astro` e `pages/en/index.astro`.

- [ ] **Step 1: Adicionar bloco `i18n` ao `astro.config.mjs`**

Modificar `template/astro.config.mjs`, dentro de `export default defineConfig({ ... })` — adicionar a chave `i18n` (pode ir logo após `site,`):

```js
export default defineConfig({
  site,
  i18n: {
    locales: ['pt', 'en'],
    defaultLocale: 'pt',
    routing: { prefixDefaultLocale: false },
  },
  integrations: [sitemap()],
  vite: {
    // ... resto do arquivo permanece idêntico
```

- [ ] **Step 2: Extrair `PaginaInicial.astro` (mover, sem alterar conteúdo)**

Criar `template/src/components/PaginaInicial.astro` com o conteúdo atual de `template/src/pages/index.astro`, removendo só a importação e o wrap de `Layout` (o resto — imports de componentes, frontmatter, todas as seções — é uma cópia literal):

```astro
---
import { Image } from 'astro:assets';
import Hero from './Hero.astro';
import TituloSecao from './TituloSecao.astro';
import BotaoWhatsApp from './BotaoWhatsApp.astro';
import Mapa from './Mapa.astro';
import DivisorSimbolo from './DivisorSimbolo.astro';
import MarcaDagua from './MarcaDagua.astro';
import Acomodacoes from './Acomodacoes.astro';
import FotoDestaque from './FotoDestaque.astro';
import SimboloComodidade from './SimboloComodidade.astro';
import Vibe from './Vibe.astro';
import CascataOndas from './CascataOndas.astro';
import { config } from '../lib/cliente';
import { foto } from '../lib/fotos';
import { aspectMosaico } from '../lib/mosaico';

const comodidadesComFoto = config.comodidades?.filter((c) => c.foto) ?? [];
const comodidadesSemFoto = config.comodidades?.filter((c) => !c.foto) ?? [];
const [destaqueUm, destaqueDois] = config.destaques ?? [];
---

<Hero />

{
  config.acomodacoes && (
    <>
      <section id="acomodacoes" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden">
        <CascataOndas />
        <div class="mx-auto max-w-5xl px-4 py-14">
          <TituloSecao eyebrow="Acomodações">Escolha seu canto</TituloSecao>
          <div class="revela mt-8">
            <Acomodacoes />
          </div>
          <div class="mt-6 text-center">
            <BotaoWhatsApp rotulo="Consultar disponibilidade no WhatsApp" />
          </div>
        </div>
      </section>

      <DivisorSimbolo />
    </>
  )
}

{
  config.sobre && (
    <section id="sobre" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden">
      <CascataOndas />
      <div class="mx-auto max-w-5xl px-4 py-14">
        <TituloSecao>A casa</TituloSecao>
        <div
          class:list={[
            'revela mt-8',
            config.sobre.foto && 'grid items-center gap-10 sm:grid-cols-2',
          ]}
        >
          {
            config.sobre.foto && (
              <Image
                src={foto(config.sobre.foto.arquivo)}
                alt={config.sobre.foto.alt}
                widths={[480, 900]}
                sizes="(min-width: 640px) 480px, 100vw"
                class="aspect-4/3 w-full object-cover"
              />
            )
          }
          <p class="max-w-2xl text-lg leading-relaxed">{config.sobre.historia}</p>
        </div>
      </div>
    </section>
  )
}

{
  config.comodidades && (
    <>
      <DivisorSimbolo />

      <section id="comodidades" class="scroll-mt-36 sm:scroll-mt-20 bg-sal">
        <div class="mx-auto max-w-5xl px-4 py-14">
          <TituloSecao eyebrow="Comodidades">A vida por aqui</TituloSecao>
          {
            comodidadesComFoto.length > 0 && (
              <div class="mt-12 space-y-12">
                {comodidadesComFoto.map((comodidade, indice) => (
                  <div class="revela grid items-center gap-6 sm:grid-cols-2 sm:gap-10">
                    <Image
                      src={foto(comodidade.foto!.arquivo)}
                      alt={comodidade.foto!.alt}
                      widths={[480, 900]}
                      sizes="(min-width: 640px) 480px, 100vw"
                      class:list={[
                        'aspect-4/3 w-full object-cover',
                        indice % 2 === 1 && 'sm:order-last',
                      ]}
                    />
                    <div>
                      {comodidade.simbolo && (
                        <SimboloComodidade
                          simbolo={comodidade.simbolo}
                          class="mb-4 h-12 w-12 text-fitinha"
                        />
                      )}
                      <h3 class="font-display text-2xl font-bold text-mare">{comodidade.nome}</h3>
                      {comodidade.descricao && (
                        <p class="mt-3 text-lg leading-relaxed">{comodidade.descricao}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )
          }
          {
            comodidadesSemFoto.length > 0 && (
              <ul class="revela mt-14 grid gap-x-8 gap-y-10 sm:grid-cols-2 lg:grid-cols-3">
                {comodidadesSemFoto.map((comodidade) => (
                  <li class="flex items-start gap-4">
                    {comodidade.simbolo ? (
                      <SimboloComodidade
                        simbolo={comodidade.simbolo}
                        class="h-12 w-12 shrink-0 text-fitinha"
                      />
                    ) : (
                      <span class="mt-3 h-0.5 w-6 shrink-0 bg-fitinha" aria-hidden="true" />
                    )}
                    <div>
                      <h3 class="font-display font-bold text-mare">{comodidade.nome}</h3>
                      {comodidade.descricao && <p class="mt-1 text-sm">{comodidade.descricao}</p>}
                    </div>
                  </li>
                ))}
              </ul>
            )
          }
        </div>
      </section>
    </>
  )
}

{destaqueUm ? <FotoDestaque destaque={destaqueUm} /> : config.vibe && <DivisorSimbolo />}

{
  config.vibe && (
    <section id="vibe" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden">
      <CascataOndas />
      <div class="mx-auto max-w-5xl px-4 py-14">
        <TituloSecao eyebrow="A vibe">Como é ficar aqui</TituloSecao>
        <div class="revela mt-8">
          <Vibe />
        </div>
      </div>
    </section>
  )
}

{config.vibe && <DivisorSimbolo />}

{
  config.regiao && (
    <section id="regiao" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden">
      <CascataOndas />
      <div class="mx-auto max-w-5xl px-4 py-14">
      <TituloSecao eyebrow="A região">Explore os arredores</TituloSecao>
      {/* Celular: mosaico em 2 colunas com alturas variadas. Computador: fileiras
          alinhadas na mesma altura, alternando foto grande + pequena (ritmo
          Parador/Kenoa) — display:grid desativa as columns no lg. */}
      <div class="revela mt-8 columns-2 gap-3 lg:grid lg:grid-cols-3 lg:gap-x-4 lg:gap-y-8">
        {config.regiao.map((ponto, indice) => (
          <figure class:list={[
            'group mb-4 break-inside-avoid lg:mb-0',
            [0, 3, 4].includes(indice % 6) && 'lg:col-span-2',
          ]}>
            <div class="overflow-hidden">
              <Image
                src={foto(ponto.foto.arquivo)}
                alt={ponto.foto.alt}
                widths={[400, 800, 1200]}
                sizes="(min-width: 1024px) 40vw, 50vw"
                class:list={[
                  'w-full object-cover transition duration-500 group-hover:scale-105 lg:aspect-auto lg:h-75',
                  aspectMosaico(indice),
                ]}
              />
            </div>
            <figcaption class="px-1 pt-3">
              <p class="font-mono text-xs tracking-widest text-fitinha uppercase">{ponto.distancia}</p>
              <h3 class="mt-1 font-display text-lg font-bold">{ponto.nome}</h3>
              <p class="mt-1 text-sm opacity-90">{ponto.descricao}</p>
              {ponto.credito && <p class="mt-1 text-xs opacity-60">Foto: {ponto.credito}</p>}
            </figcaption>
          </figure>
        ))}
      </div>
      </div>
    </section>
  )
}

{config.regiao && (destaqueDois ? <FotoDestaque destaque={destaqueDois} /> : <DivisorSimbolo />)}

{
  config.depoimentos && (
    <section id="depoimentos" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden bg-mare">
      <CascataOndas cor="var(--color-mare)" />
      <MarcaDagua />
      <div class="mx-auto max-w-5xl px-4 py-14">
        <TituloSecao eyebrow="Depoimentos" claro>
          Quem passou por aqui
        </TituloSecao>
        <div class="mt-10 grid gap-x-10 gap-y-12 sm:grid-cols-2">
          {config.depoimentos.map((depoimento) => (
            <figure class="revela relative pt-8 pl-2">
              <span
                class="pointer-events-none absolute -top-3 left-0 font-display text-8xl leading-none text-noite/25 select-none"
                aria-hidden="true"
              >
                &ldquo;
              </span>
              <blockquote class="text-lg leading-relaxed text-noite">{depoimento.texto}</blockquote>
              <figcaption class="mt-4 text-sm font-bold text-noite">
                {depoimento.nome} <span class="font-normal opacity-70">— {depoimento.fonte}</span>
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  )
}

{config.depoimentos && <DivisorSimbolo />}

{
  config.localizacao.mapsEmbedUrl && (
    <section id="localizacao" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden">
      <CascataOndas />
      <div class="mx-auto max-w-5xl px-4 py-14">
      <TituloSecao eyebrow="Localização">Onde estamos</TituloSecao>
      <p class="mt-4 text-lg">{config.localizacao.endereco}</p>
      <div class="revela mt-8">
        <Mapa />
      </div>
      {
        config.localizacao.comoChegar && config.localizacao.comoChegar.length > 0 && (
          <div class="revela mt-10">
            <h3 class="font-display text-xl font-bold text-mare">Como chegar</h3>
            <ul class="mt-4 max-w-2xl space-y-3">
              {config.localizacao.comoChegar.map((trecho) => (
                <li class="flex gap-3">
                  <span class="mt-2.5 h-0.5 w-4 shrink-0 bg-fitinha" aria-hidden="true" />
                  {trecho}
                </li>
              ))}
            </ul>
          </div>
        )
      }
      {
        config.localizacao.resumo && (
          <p class="mt-10 text-center text-lg">{config.localizacao.resumo}</p>
        )
      }
      </div>
    </section>
  )
}

<section class="relative isolate overflow-hidden bg-mare">
  <CascataOndas cor="var(--color-mare)" />
  <MarcaDagua />
  <div class="mx-auto max-w-5xl px-4 py-14 text-center">
    <h2 class="font-display text-3xl font-bold text-noite">Reserve direto com a gente</h2>
    <p class="mx-auto mt-3 max-w-md text-noite">
      Chame no WhatsApp e combine sua estadia direto com quem cuida da casa.
    </p>
    <div class="mt-6">
      <BotaoWhatsApp tamanho="grande" />
    </div>
  </div>
</section>
```

Note: os imports de componentes agora usam `./` em vez de `../components/` (o arquivo está dentro de `components/`); os imports de `lib/` continuam `../lib/`.

- [ ] **Step 3: `pages/index.astro` vira casca fina**

Substituir todo o conteúdo de `template/src/pages/index.astro` por:

```astro
---
import Layout from '../layouts/Layout.astro';
import PaginaInicial from '../components/PaginaInicial.astro';
---

<Layout>
  <PaginaInicial />
</Layout>
```

- [ ] **Step 4: Criar `pages/en/index.astro` com a guarda de redirecionamento**

```astro
---
import Layout from '../../layouts/Layout.astro';
import PaginaInicial from '../../components/PaginaInicial.astro';
import { config } from '../../lib/cliente';

if (!config.idiomasDisponiveis?.includes('en')) {
  return Astro.redirect('/', 302);
}
---

<Layout>
  <PaginaInicial />
</Layout>
```

- [ ] **Step 5: Verificar a guarda ANTES de ativar o LumeHostel (estado "desligado")**

A partir de `template/`:
```
$env:CLIENTE = 'lumehostel'; npm run build
Select-String -Path dist/en/index.html -Pattern 'http-equiv="refresh"'
```
Expected: encontra a linha do `<meta http-equiv="refresh" ...>` — confirma que, sem `idiomasDisponiveis` no config, `/en/` redireciona para `/` (comportamento padrão do Astro em build estático sem adaptador: `Astro.redirect()` vira uma página HTML com meta-refresh, não um 302 HTTP real — [confirmado na doc oficial do Astro]).

- [ ] **Step 6: Ativar `idiomasDisponiveis` no LumeHostel e verificar o estado "ligado"**

Editar `clientes/lumehostel/config.json`, adicionando a chave logo depois de `"nome"`:

```json
  "nome": "LumeHostel",
  "idiomasDisponiveis": ["pt", "en"],
  "marca": { ... },
```

Rebuild:
```
$env:CLIENTE = 'lumehostel'; npm run build
Select-String -Path dist/en/index.html -Pattern 'http-equiv="refresh"'
Select-String -Path dist/en/index.html -Pattern 'Reserve pelo WhatsApp'
```
Expected: o primeiro `Select-String` não encontra nada (sem redirecionamento); o segundo encontra `Reserve pelo WhatsApp` (esperado — os textos ainda estão em português, porque `Nav`/`Footer`/`BotaoWhatsApp`/`PaginaInicial` ainda não foram religados aos helpers; isso é corrigido nas próximas tasks). O importante aqui é confirmar que `/en/` renderiza a página completa, não o redirect.

- [ ] **Step 7: Confirmar que `demo` e `maravista` continuam redirecionando**

```
$env:CLIENTE = 'demo'; npm run build
Select-String -Path dist/en/index.html -Pattern 'http-equiv="refresh"'
$env:CLIENTE = 'maravista'; npm run build
Select-String -Path dist/en/index.html -Pattern 'http-equiv="refresh"'
```
Expected: os dois encontram a linha do meta-refresh (nenhum dos dois tem `idiomasDisponiveis`).

- [ ] **Step 8: `npm run check`**

Run: `npm run check`
Expected: passa sem erro.

- [ ] **Step 9: Commit**

```bash
git add template/astro.config.mjs template/src/components/PaginaInicial.astro template/src/pages/index.astro template/src/pages/en/index.astro clientes/lumehostel/config.json
git commit -m "Adiciona roteamento i18n do Astro e rota /en/ com guarda por idiomasDisponiveis"
```

---

## Task 5: `Nav.astro` — textos e alternador PT / EN

**Files:**
- Modify: `template/src/components/Nav.astro` (arquivo inteiro)

**Interfaces:**
- Consumes: `idiomaAtual`, `t` (Task 2); `textos` (Task 3); `config.idiomasDisponiveis` (Task 1); `getRelativeLocaleUrl` de `astro:i18n` (nativo do Astro, disponível a partir da Task 4).
- Produces: nenhuma interface nova para outras tasks — componente-folha.

- [ ] **Step 1: Substituir o arquivo inteiro**

```astro
---
import { getRelativeLocaleUrl } from 'astro:i18n';
import { config } from '../lib/cliente';
import { marca } from '../lib/fotos';
import { idiomaAtual } from '../lib/i18n';
import { textos } from '../lib/textos';
import BotaoWhatsApp from './BotaoWhatsApp.astro';

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].nav;

const linkPt = getRelativeLocaleUrl('pt');
const linkEn = getRelativeLocaleUrl('en');
// Base do link "home" pro idioma atual — usada tanto pelo logo quanto pelos
// itens de âncora do menu (abas), pra não levar quem está em /en/ de volta
// pra página em português. Só o alternador PT/EN em si (abaixo) precisa de
// linkPt/linkEn crus, sem esse prefixo.
const linkBase = idioma === 'en' ? linkEn : linkPt;

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

const mostrarAlternador = (config.idiomasDisponiveis?.length ?? 0) > 1;
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
            {idioma === 'pt' ? (
              <span aria-current="page">PT</span>
            ) : (
              <a
                href={linkPt}
                hreflang="pt"
                class="transition hover:text-fitinha focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-azulejo"
              >
                PT
              </a>
            )}
            <span aria-hidden="true">/</span>
            {idioma === 'en' ? (
              <span aria-current="page">EN</span>
            ) : (
              <a
                href={linkEn}
                hreflang="en"
                class="transition hover:text-fitinha focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-azulejo"
              >
                EN
              </a>
            )}
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

Nota: o `aria-label` de abrir/fechar menu é setado por um `<script>` que roda no navegador — não tem acesso a `Astro.currentLocale` (isso só existe em tempo de build/SSR). Por isso os rótulos traduzidos são passados via `data-rotulo-abrir`/`data-rotulo-fechar` no próprio botão, e o script lê `dataset` em vez de usar strings cravadas.

**Nota sobre `linkBase` (correção de bug encontrada na revisão do plano)**: numa
versão anterior deste plano, o link do logo e os `href` de `abas` ficavam
fixos em `/`/`/#acomodacoes` etc., iguais ao `Nav.astro` de hoje (que só
serve `/`, então "raiz" e "página atual" sempre coincidem). Com `/en/`
virando uma segunda página real que renderiza as mesmas seções, isso
quebraria: clicar no logo ou em qualquer item do menu de seção estando em
`/en/` levaria de volta pra `/` (página em português), abandonando o site em
inglês — só o alternador PT/EN em si (que já usava `linkPt`/`linkEn` via
`getRelativeLocaleUrl`) ficava correto. `linkBase` resolve isso: em `/`
gera exatamente os mesmos hrefs de hoje (`/#acomodacoes` etc., zero mudança
pra `demo`/`maravista`, que sempre resolvem `idioma === 'pt'`); em `/en/`
gera `/en#acomodacoes` etc., mantendo a navegação dentro do idioma atual.

- [ ] **Step 2: Build e checagem**

```
npm run check
$env:CLIENTE = 'lumehostel'; npm run build
Select-String -Path dist/index.html -Pattern 'Acomodações'
Select-String -Path dist/en/index.html -Pattern 'Rooms'
Select-String -Path dist/en/index.html -Pattern '>PT<'
Select-String -Path dist/index.html -Pattern '>EN<'
Select-String -Path dist/en/index.html -Pattern 'href="/en#acomodacoes"'
Select-String -Path dist/index.html -Pattern 'href="/#acomodacoes"'
```
Expected: `dist/index.html` (pt) mostra "Acomodações" e o link "EN"; `dist/en/index.html` mostra "Rooms" e o rótulo ativo "PT". Crucial: o item de menu "Acomodações"/"Rooms" e o link do logo em `dist/en/index.html` apontam pra `/en#acomodacoes` (não `/#acomodacoes` puro) — confirma que navegar pelo menu ou clicar no logo estando em `/en/` não manda de volta pra página em português; em `dist/index.html` o href continua `/#acomodacoes`, idêntico ao comportamento de hoje.

```
$env:CLIENTE = 'demo'; npm run build
Select-String -Path dist/index.html -Pattern '>PT<|>EN<'
Select-String -Path dist/index.html -Pattern 'href="/#acomodacoes"'
```
Expected: nenhuma ocorrência de `>PT<`/`>EN<` — `demo` não tem `idiomasDisponiveis`, o alternador não aparece; o href do menu de seção continua `/#acomodacoes` (comportamento inalterado, já que `demo` nunca resolve `idioma === 'en'`).

- [ ] **Step 3: Commit**

```bash
git add template/src/components/Nav.astro
git commit -m "Traduz rotulos do Nav e adiciona alternador PT/EN"
```

---

## Task 6: `Footer.astro` — textos

**Files:**
- Modify: `template/src/components/Footer.astro` (arquivo inteiro)

**Interfaces:**
- Consumes: `idiomaAtual`, `t` (Task 2); `textos` (Task 3).

**Nota de dependência**: o `Footer.astro` real já foi reescrito pelo plano
`redes-sociais-rodape.md` (commit `6330f7b`) para incluir o bloco "Siga a
gente" (`IconeRedeSocial`, `linkTiktok`, `linkFacebook`, `temRedeSocial`,
grid de 3 colunas condicional). O bloco abaixo parte **desse** arquivo real
e acrescenta só as mudanças de i18n por cima — não é mais uma reversão pro
estado de 2 colunas de antes da Task de redes sociais.

- [ ] **Step 1: Substituir o arquivo inteiro**

```astro
---
import { config } from '../lib/cliente';
import IconeRedeSocial from './IconeRedeSocial.astro';
import { idiomaAtual, t } from '../lib/i18n';
import { textos } from '../lib/textos';

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].footer;

const linkWhatsApp = `https://wa.me/${config.contato.whatsapp}`;
const linkInstagram = config.contato.instagram
  ? `https://instagram.com/${config.contato.instagram}`
  : undefined;
const linkTiktok = config.contato.tiktok ? `https://www.tiktok.com/@${config.contato.tiktok}` : undefined;
const linkFacebook = config.contato.facebook
  ? `https://www.facebook.com/${config.contato.facebook}`
  : undefined;
const temRedeSocial = Boolean(linkInstagram || linkTiktok || linkFacebook);

const estilosLink =
  'underline decoration-fitinha decoration-2 underline-offset-4 transition hover:text-fitinha focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-fitinha';
const estilosIcone =
  'transition hover:opacity-75 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-fitinha';
---

<footer class="relative isolate overflow-hidden bg-noite text-sal">
  {
    /* Textura de grade de pontos: o rodapé nunca fica com fundo chapado
       (decisão da autora, 2026-07-23). Cor neutra em branco translúcido
       funciona sobre o bg-noite de qualquer tema. */
  }
  <div
    class="pointer-events-none absolute inset-0"
    style="background-image: radial-gradient(circle, rgb(255 255 255 / 0.12) 1px, transparent 1.5px); background-size: 22px 22px; mask-image: radial-gradient(ellipse 90% 100% at 70% 30%, black 40%, transparent 90%);"
    aria-hidden="true"
  >
  </div>
  <div
    class:list={[
      'relative mx-auto grid max-w-5xl gap-8 px-4 py-10 sm:grid-cols-2',
      { 'lg:grid-cols-3': temRedeSocial },
    ]}
  >
    <div>
      <p class="font-display text-lg font-bold text-espuma">{config.nome}</p>
      <p class="mt-1 max-w-xs text-sm">{t(config.slogan, idioma)}</p>
      <p class="mt-4 text-sm">{config.localizacao.endereco}</p>
    </div>
    <div class="text-sm sm:justify-self-end lg:justify-self-start">
      <p class="font-mono text-xs tracking-widest text-espuma uppercase">{txt.faleConosco}</p>
      <ul class="mt-3 space-y-2">
        <li>
          <a href={linkWhatsApp} target="_blank" rel="noopener noreferrer" class={estilosLink}>WhatsApp</a>
        </li>
        <li>
          <a href={`mailto:${config.contato.email}`} class={estilosLink}>{config.contato.email}</a>
        </li>
      </ul>
    </div>
    {
      temRedeSocial && (
        <div class="text-sm sm:justify-self-end lg:justify-self-start">
          <p class="font-mono text-xs tracking-widest text-espuma uppercase">{txt.sigaAGente}</p>
          <div class="mt-3 flex justify-center gap-4">
            {linkInstagram && (
              <a href={linkInstagram} target="_blank" rel="noopener noreferrer" aria-label="Instagram" class={estilosIcone}>
                <IconeRedeSocial rede="instagram" class="h-6 w-6 text-fitinha" />
              </a>
            )}
            {linkTiktok && (
              <a href={linkTiktok} target="_blank" rel="noopener noreferrer" aria-label="TikTok" class={estilosIcone}>
                <IconeRedeSocial rede="tiktok" class="h-6 w-6 text-fitinha" />
              </a>
            )}
            {linkFacebook && (
              <a href={linkFacebook} target="_blank" rel="noopener noreferrer" aria-label="Facebook" class={estilosIcone}>
                <IconeRedeSocial rede="facebook" class="h-6 w-6 text-fitinha" />
              </a>
            )}
          </div>
        </div>
      )
    }
  </div>
</footer>
```

Nota: `aria-label="Instagram"`/`"TikTok"`/`"Facebook"` e os nomes dentro de
`IconeRedeSocial` continuam fixos nos dois idiomas — são nomes de
plataforma, mesma regra de não-tradução já usada pra nome/fonte de
depoimento e crédito de foto. Só `{txt.sigaAGente}` (rótulo da seção) é
traduzido, igual `{txt.faleConosco}`.

- [ ] **Step 2: Build e checagem**

```
npm run check
$env:CLIENTE = 'lumehostel'; npm run build
Select-String -Path dist/en/index.html -Pattern 'Get in touch'
Select-String -Path dist/index.html -Pattern 'Fale conosco'
Select-String -Path dist/en/index.html -Pattern 'Follow us'
Select-String -Path dist/index.html -Pattern 'Siga a gente'
Select-String -Path dist/en/index.html -Pattern 'tiktok.com/@lumehostel'
```
Expected: cada arquivo mostra a versão do seu próprio idioma (inclusive o
rótulo "Siga a gente"/"Follow us"); o bloco de redes sociais (Instagram +
TikTok do LumeHostel) continua presente nos dois idiomas.

- [ ] **Step 3: Commit**

```bash
git add template/src/components/Footer.astro
git commit -m "Traduz rodape (Fale conosco/Siga a gente e equivalentes em ingles, slogan)"
```

---

## Task 7: `BotaoWhatsApp.astro` — rótulo padrão e mensagem

**Files:**
- Modify: `template/src/components/BotaoWhatsApp.astro` (arquivo inteiro)

**Interfaces:**
- Consumes: `idiomaAtual` (Task 2); `textos` (Task 3).
- Produces: comportamento inalterado para quem já passa `rotulo` explícito (`PaginaInicial.astro`, Task 9, vai passar o texto traduzido via prop).

- [ ] **Step 1: Substituir o arquivo inteiro**

```astro
---
import { config } from '../lib/cliente';
import { idiomaAtual } from '../lib/i18n';
import { textos } from '../lib/textos';

interface Props {
  rotulo?: string;
  tamanho?: 'medio' | 'grande';
}

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].botaoWhatsApp;

const { rotulo = txt.rotuloPadrao, tamanho = 'medio' } = Astro.props;

const mensagem = encodeURIComponent(txt.mensagem(config.nome));
const href = `https://wa.me/${config.contato.whatsapp}?text=${mensagem}`;

const tamanhos = {
  medio: 'px-3 py-1.5 text-xs sm:px-4 sm:py-2 sm:text-sm',
  grande: 'px-6 py-3 text-base',
};
---

<a
  href={href}
  target="_blank"
  rel="noopener noreferrer"
  class:list={[
    'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-full bg-zap font-corpo font-bold text-noite transition hover:brightness-110 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-azulejo',
    tamanhos[tamanho],
  ]}
>
  {rotulo}
</a>
```

- [ ] **Step 2: Build e checagem**

```
npm run check
$env:CLIENTE = 'lumehostel'; npm run build
Select-String -Path dist/en/index.html -Pattern 'Book on WhatsApp'
Select-String -Path dist/index.html -Pattern 'Reserve pelo WhatsApp'
```
Expected: cada versão mostra o rótulo padrão no seu idioma (a versão com `rotulo` explícito — "Consultar disponibilidade" — ainda está em português nos dois idiomas até a Task 9).

- [ ] **Step 3: Commit**

```bash
git add template/src/components/BotaoWhatsApp.astro
git commit -m "Traduz rotulo padrao e mensagem do BotaoWhatsApp"
```

---

## Task 8: `Hero.astro` e `Acomodacoes.astro` — conteúdo do cliente

**Files:**
- Modify: `template/src/components/Hero.astro:1-14,96` (frontmatter + linha do slogan não-centralizado)
- Modify: `template/src/components/Acomodacoes.astro` (arquivo inteiro)

**Interfaces:**
- Consumes: `idiomaAtual`, `t` (Task 2).

- [ ] **Step 1: `Hero.astro` — atualizar frontmatter**

Modificar `template/src/components/Hero.astro`, linhas 1-13 (frontmatter):

```astro
---
import { Image } from 'astro:assets';
import { config } from '../lib/cliente';
import { foto, marca, video } from '../lib/fotos';
import { idiomaAtual, t } from '../lib/i18n';
import MarcaDagua from './MarcaDagua.astro';

const idioma = idiomaAtual(Astro.currentLocale);

const logo = config.marca?.logo && !config.marca.logoApenasNoMenu ? marca(config.marca.logo) : undefined;
const heroVideo = config.marca?.heroVideo ? video(config.marca.heroVideo) : undefined;
const heroVideoPoster = config.marca?.heroVideoPoster
  ? foto(config.marca.heroVideoPoster)
  : undefined;
const heroCentralizado = config.marca?.heroCentralizado ?? false;
const fraseHero = config.marca?.heroFraseQuebrada ?? t(config.slogan, idioma);
---
```

- [ ] **Step 2: `Hero.astro` — atualizar a linha do slogan no bloco não-centralizado**

Na mesma seção do template (bloco `else` do `heroCentralizado ? (...) : (...)`), trocar:

```astro
        <p class="hero-frase mt-4 max-w-xl text-base text-white">{config.slogan}</p>
```

por:

```astro
        <p class="hero-frase mt-4 max-w-xl text-base text-white">{t(config.slogan, idioma)}</p>
```

(O restante do arquivo — vídeo, poster, composição centralizada, script do vídeo — permanece idêntico; `fraseHero`, já resolvido no frontmatter, é usado sem mudança na composição centralizada.)

- [ ] **Step 3: `Acomodacoes.astro` — substituir o arquivo inteiro**

```astro
---
import { Image } from 'astro:assets';
import { config } from '../lib/cliente';
import { foto } from '../lib/fotos';
import { idiomaAtual, t } from '../lib/i18n';

const idioma = idiomaAtual(Astro.currentLocale);
---

{/* Cards estilo boutique (ref. Kenoa/Parador/Awasi): foto limpa sem véu escuro,
    legenda embaixo com a capacidade em eyebrow monospace. 2 colunas no celular
    para encurtar a rolagem. */}
{
  config.acomodacoes && (
    <div class="grid grid-cols-2 gap-x-3 gap-y-8 sm:gap-x-4 lg:grid-cols-3">
      {config.acomodacoes.map((acomodacao) => (
        <article>
          <div class="overflow-hidden rounded-xl">
            <Image
              src={foto(acomodacao.fotos[0].arquivo)}
              alt={acomodacao.fotos[0].alt}
              widths={[480, 900]}
              sizes="(min-width: 640px) 448px, 50vw"
              class="aspect-3/4 w-full object-cover"
            />
          </div>
          <p class="mt-3 font-mono text-xs tracking-widest text-fitinha uppercase">
            {t(acomodacao.capacidade, idioma)}
          </p>
          <h3 class="mt-1 font-display text-lg font-bold">{t(acomodacao.nome, idioma)}</h3>
          <p class="mt-1 text-sm opacity-75">
            {acomodacao.comodidades.map((c) => t(c, idioma)).join(' · ')}
          </p>
        </article>
      ))}
    </div>
  )
}
```

- [ ] **Step 4: `npm run check` (ainda sem tradução no config — output visual não muda)**

Run: `npm run check`
Expected: passa sem erro. (Sem tradução ainda no `config.json`, `t()` devolve a mesma string em pt e en — nenhuma regressão visual esperada nesta task.)

- [ ] **Step 5: Commit**

```bash
git add template/src/components/Hero.astro template/src/components/Acomodacoes.astro
git commit -m "Religa Hero e Acomodacoes ao helper t() para conteudo bilingue"
```

---

## Task 9: `PaginaInicial.astro`, `FotoDestaque.astro`, `Mapa.astro` — conteúdo e chrome de seção

**Files:**
- Modify: `template/src/components/PaginaInicial.astro` (arquivo inteiro — reescreve o extraído na Task 4)
- Modify: `template/src/components/FotoDestaque.astro` (arquivo inteiro)
- Modify: `template/src/components/Mapa.astro` (arquivo inteiro)

**Interfaces:**
- Consumes: `idiomaAtual`, `t` (Task 2); `textos` (Task 3); `Destaque` type (Task 1).

- [ ] **Step 1: `FotoDestaque.astro` — substituir o arquivo inteiro**

```astro
---
import { Image } from 'astro:assets';
import type { Destaque } from '../lib/schema';
import { foto } from '../lib/fotos';
import { idiomaAtual, t } from '../lib/i18n';

interface Props {
  destaque: Destaque;
}

const { destaque } = Astro.props;
const idioma = idiomaAtual(Astro.currentLocale);
---

{/* A imagem é position:fixed (parada em relação à janela) e o clip-path da
    seção a recorta: ao rolar, a página passa por cima da foto imóvel. */}
<section
  class="relative isolate flex min-h-[70svh] items-center justify-center overflow-hidden"
  style="clip-path: inset(0)"
>
  <Image
    src={foto(destaque.foto.arquivo)}
    alt={destaque.foto.alt}
    widths={[768, 1280, 1920]}
    sizes="100vw"
    class="fixed inset-0 -z-10 h-full w-full object-cover"
  />
  <div class="fixed inset-0 -z-10 bg-noite/45" aria-hidden="true"></div>
  <p
    class="revela max-w-3xl px-6 text-center font-display text-3xl font-bold text-white [text-shadow:0_1px_12px_rgb(0_0_0/0.35)] sm:text-5xl"
  >
    {t(destaque.frase, idioma)}
  </p>
</section>
```

- [ ] **Step 2: `Mapa.astro` — substituir o arquivo inteiro**

```astro
---
import { config } from '../lib/cliente';
import { idiomaAtual } from '../lib/i18n';
import { textos } from '../lib/textos';

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].mapa;
---

<iframe
  src={config.localizacao.mapsEmbedUrl}
  title={`${txt.titulo}: ${config.localizacao.endereco}`}
  loading="lazy"
  referrerpolicy="no-referrer-when-downgrade"
  sandbox="allow-scripts allow-same-origin allow-popups"
  class="aspect-video w-full rounded-xl border-0"></iframe>
```

- [ ] **Step 3: `PaginaInicial.astro` — substituir o arquivo inteiro**

```astro
---
import { Image } from 'astro:assets';
import Hero from './Hero.astro';
import TituloSecao from './TituloSecao.astro';
import BotaoWhatsApp from './BotaoWhatsApp.astro';
import Mapa from './Mapa.astro';
import DivisorSimbolo from './DivisorSimbolo.astro';
import MarcaDagua from './MarcaDagua.astro';
import Acomodacoes from './Acomodacoes.astro';
import FotoDestaque from './FotoDestaque.astro';
import SimboloComodidade from './SimboloComodidade.astro';
import Vibe from './Vibe.astro';
import CascataOndas from './CascataOndas.astro';
import { config } from '../lib/cliente';
import { foto } from '../lib/fotos';
import { aspectMosaico } from '../lib/mosaico';
import { idiomaAtual, t } from '../lib/i18n';
import { textos } from '../lib/textos';

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].pagina;

const comodidadesComFoto = config.comodidades?.filter((c) => c.foto) ?? [];
const comodidadesSemFoto = config.comodidades?.filter((c) => !c.foto) ?? [];
const [destaqueUm, destaqueDois] = config.destaques ?? [];
---

<Hero />

{
  config.acomodacoes && (
    <>
      <section id="acomodacoes" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden">
        <CascataOndas />
        <div class="mx-auto max-w-5xl px-4 py-14">
          <TituloSecao eyebrow={txt.acomodacoesEyebrow}>{txt.acomodacoesTitulo}</TituloSecao>
          <div class="revela mt-8">
            <Acomodacoes />
          </div>
          <div class="mt-6 text-center">
            <BotaoWhatsApp rotulo={txt.acomodacoesCta} />
          </div>
        </div>
      </section>

      <DivisorSimbolo />
    </>
  )
}

{
  config.sobre && (
    <section id="sobre" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden">
      <CascataOndas />
      <div class="mx-auto max-w-5xl px-4 py-14">
        <TituloSecao>{txt.casaTitulo}</TituloSecao>
        <div
          class:list={[
            'revela mt-8',
            config.sobre.foto && 'grid items-center gap-10 sm:grid-cols-2',
          ]}
        >
          {
            config.sobre.foto && (
              <Image
                src={foto(config.sobre.foto.arquivo)}
                alt={config.sobre.foto.alt}
                widths={[480, 900]}
                sizes="(min-width: 640px) 480px, 100vw"
                class="aspect-4/3 w-full object-cover"
              />
            )
          }
          <p class="max-w-2xl text-lg leading-relaxed">{t(config.sobre.historia, idioma)}</p>
        </div>
      </div>
    </section>
  )
}

{
  config.comodidades && (
    <>
      <DivisorSimbolo />

      <section id="comodidades" class="scroll-mt-36 sm:scroll-mt-20 bg-sal">
        <div class="mx-auto max-w-5xl px-4 py-14">
          <TituloSecao eyebrow={txt.comodidadesEyebrow}>{txt.comodidadesTitulo}</TituloSecao>
          {
            comodidadesComFoto.length > 0 && (
              <div class="mt-12 space-y-12">
                {comodidadesComFoto.map((comodidade, indice) => (
                  <div class="revela grid items-center gap-6 sm:grid-cols-2 sm:gap-10">
                    <Image
                      src={foto(comodidade.foto!.arquivo)}
                      alt={comodidade.foto!.alt}
                      widths={[480, 900]}
                      sizes="(min-width: 640px) 480px, 100vw"
                      class:list={[
                        'aspect-4/3 w-full object-cover',
                        indice % 2 === 1 && 'sm:order-last',
                      ]}
                    />
                    <div>
                      {comodidade.simbolo && (
                        <SimboloComodidade
                          simbolo={comodidade.simbolo}
                          class="mb-4 h-12 w-12 text-fitinha"
                        />
                      )}
                      <h3 class="font-display text-2xl font-bold text-mare">{t(comodidade.nome, idioma)}</h3>
                      {comodidade.descricao && (
                        <p class="mt-3 text-lg leading-relaxed">{t(comodidade.descricao, idioma)}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )
          }
          {
            comodidadesSemFoto.length > 0 && (
              <ul class="revela mt-14 grid gap-x-8 gap-y-10 sm:grid-cols-2 lg:grid-cols-3">
                {comodidadesSemFoto.map((comodidade) => (
                  <li class="flex items-start gap-4">
                    {comodidade.simbolo ? (
                      <SimboloComodidade
                        simbolo={comodidade.simbolo}
                        class="h-12 w-12 shrink-0 text-fitinha"
                      />
                    ) : (
                      <span class="mt-3 h-0.5 w-6 shrink-0 bg-fitinha" aria-hidden="true" />
                    )}
                    <div>
                      <h3 class="font-display font-bold text-mare">{t(comodidade.nome, idioma)}</h3>
                      {comodidade.descricao && <p class="mt-1 text-sm">{t(comodidade.descricao, idioma)}</p>}
                    </div>
                  </li>
                ))}
              </ul>
            )
          }
        </div>
      </section>
    </>
  )
}

{destaqueUm ? <FotoDestaque destaque={destaqueUm} /> : config.vibe && <DivisorSimbolo />}

{
  config.vibe && (
    <section id="vibe" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden">
      <CascataOndas />
      <div class="mx-auto max-w-5xl px-4 py-14">
        <TituloSecao eyebrow={txt.vibeEyebrow}>{txt.vibeTitulo}</TituloSecao>
        <div class="revela mt-8">
          <Vibe />
        </div>
      </div>
    </section>
  )
}

{config.vibe && <DivisorSimbolo />}

{
  config.regiao && (
    <section id="regiao" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden">
      <CascataOndas />
      <div class="mx-auto max-w-5xl px-4 py-14">
      <TituloSecao eyebrow={txt.regiaoEyebrow}>{txt.regiaoTitulo}</TituloSecao>
      {/* Celular: mosaico em 2 colunas com alturas variadas. Computador: fileiras
          alinhadas na mesma altura, alternando foto grande + pequena (ritmo
          Parador/Kenoa) — display:grid desativa as columns no lg. */}
      <div class="revela mt-8 columns-2 gap-3 lg:grid lg:grid-cols-3 lg:gap-x-4 lg:gap-y-8">
        {config.regiao.map((ponto, indice) => (
          <figure class:list={[
            'group mb-4 break-inside-avoid lg:mb-0',
            [0, 3, 4].includes(indice % 6) && 'lg:col-span-2',
          ]}>
            <div class="overflow-hidden">
              <Image
                src={foto(ponto.foto.arquivo)}
                alt={ponto.foto.alt}
                widths={[400, 800, 1200]}
                sizes="(min-width: 1024px) 40vw, 50vw"
                class:list={[
                  'w-full object-cover transition duration-500 group-hover:scale-105 lg:aspect-auto lg:h-75',
                  aspectMosaico(indice),
                ]}
              />
            </div>
            <figcaption class="px-1 pt-3">
              <p class="font-mono text-xs tracking-widest text-fitinha uppercase">{ponto.distancia}</p>
              <h3 class="mt-1 font-display text-lg font-bold">{t(ponto.nome, idioma)}</h3>
              <p class="mt-1 text-sm opacity-90">{t(ponto.descricao, idioma)}</p>
              {ponto.credito && <p class="mt-1 text-xs opacity-60">{txt.fotoCredito} {ponto.credito}</p>}
            </figcaption>
          </figure>
        ))}
      </div>
      </div>
    </section>
  )
}

{config.regiao && (destaqueDois ? <FotoDestaque destaque={destaqueDois} /> : <DivisorSimbolo />)}

{
  config.depoimentos && (
    <section id="depoimentos" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden bg-mare">
      <CascataOndas cor="var(--color-mare)" />
      <MarcaDagua />
      <div class="mx-auto max-w-5xl px-4 py-14">
        <TituloSecao eyebrow={txt.depoimentosEyebrow} claro>
          {txt.depoimentosTitulo}
        </TituloSecao>
        <div class="mt-10 grid gap-x-10 gap-y-12 sm:grid-cols-2">
          {config.depoimentos.map((depoimento) => (
            <figure class="revela relative pt-8 pl-2">
              <span
                class="pointer-events-none absolute -top-3 left-0 font-display text-8xl leading-none text-noite/25 select-none"
                aria-hidden="true"
              >
                &ldquo;
              </span>
              <blockquote class="text-lg leading-relaxed text-noite">{t(depoimento.texto, idioma)}</blockquote>
              <figcaption class="mt-4 text-sm font-bold text-noite">
                {depoimento.nome} <span class="font-normal opacity-70">— {depoimento.fonte}</span>
              </figcaption>
              {idioma === 'en' && typeof depoimento.texto !== 'string' && (
                <p class="mt-2 text-xs opacity-60">{txt.depoimentoTraduzido}</p>
              )}
            </figure>
          ))}
        </div>
      </div>
    </section>
  )
}

{config.depoimentos && <DivisorSimbolo />}

{
  config.localizacao.mapsEmbedUrl && (
    <section id="localizacao" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden">
      <CascataOndas />
      <div class="mx-auto max-w-5xl px-4 py-14">
      <TituloSecao eyebrow={txt.localizacaoEyebrow}>{txt.localizacaoTitulo}</TituloSecao>
      <p class="mt-4 text-lg">{config.localizacao.endereco}</p>
      <div class="revela mt-8">
        <Mapa />
      </div>
      {
        config.localizacao.comoChegar && config.localizacao.comoChegar.length > 0 && (
          <div class="revela mt-10">
            <h3 class="font-display text-xl font-bold text-mare">{txt.comoChegarTitulo}</h3>
            <ul class="mt-4 max-w-2xl space-y-3">
              {config.localizacao.comoChegar.map((trecho) => (
                <li class="flex gap-3">
                  <span class="mt-2.5 h-0.5 w-4 shrink-0 bg-fitinha" aria-hidden="true" />
                  {t(trecho, idioma)}
                </li>
              ))}
            </ul>
          </div>
        )
      }
      {
        config.localizacao.resumo && (
          <p class="mt-10 text-center text-lg">{t(config.localizacao.resumo, idioma)}</p>
        )
      }
      </div>
    </section>
  )
}

<section class="relative isolate overflow-hidden bg-mare">
  <CascataOndas cor="var(--color-mare)" />
  <MarcaDagua />
  <div class="mx-auto max-w-5xl px-4 py-14 text-center">
    <h2 class="font-display text-3xl font-bold text-noite">{txt.ctaFinalTitulo}</h2>
    <p class="mx-auto mt-3 max-w-md text-noite">
      {txt.ctaFinalTexto}
    </p>
    <div class="mt-6">
      <BotaoWhatsApp tamanho="grande" />
    </div>
  </div>
</section>
```

Nota sobre a nota "Traduzido do português": ela só aparece quando o depoimento **de fato** tem um par `{pt, en}` no config (`typeof depoimento.texto !== 'string'`) — um depoimento que ficasse só em português (string solta) num cliente bilíngue não ganharia a nota (não faria sentido, já que apareceria em português mesmo na página em inglês).

- [ ] **Step 4: `npm run check` e build**

```
npm run check
$env:CLIENTE = 'lumehostel'; npm run build
Select-String -Path dist/en/index.html -Pattern 'Pick your corner'
Select-String -Path dist/en/index.html -Pattern 'Life around here'
Select-String -Path dist/index.html -Pattern 'Escolha seu canto'
```
Expected: `dist/en/index.html` mostra os títulos em inglês; `dist/index.html` continua em português (conteúdo do `config.json` ainda não traduzido — só o chrome do motor mudou; isso é esperado até a Task 11).

```
$env:CLIENTE = 'demo'; npm run build
```
Expected: build passa; conteúdo de `demo` (site sem `idiomasDisponiveis`) idêntico ao anterior — `Astro.currentLocale` resolve pt tanto em `/` (rota default) quanto, se alguém acessasse `/en/` diretamente, redirecionaria antes de renderizar.

- [ ] **Step 5: Commit**

```bash
git add template/src/components/PaginaInicial.astro template/src/components/FotoDestaque.astro template/src/components/Mapa.astro
git commit -m "Traduz titulos/eyebrows de secao e religa conteudo do cliente ao helper t()"
```

---

## Task 10: `Layout.astro` — `lang`, `og:locale`, `hreflang`, JSON-LD

**Files:**
- Modify: `template/src/layouts/Layout.astro` (arquivo inteiro)

**Interfaces:**
- Consumes: `idiomaAtual`, `t` (Task 2); `getRelativeLocaleUrl` de `astro:i18n`.

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

const bilingue = (config.idiomasDisponiveis?.length ?? 0) > 1;
const hrefAlternativaPt = bilingue ? absoluta(getRelativeLocaleUrl('pt')) : undefined;
const hrefAlternativaEn = bilingue ? absoluta(getRelativeLocaleUrl('en')) : undefined;

const ogLocale = idioma === 'en' ? 'en_US' : 'pt_BR';
const htmlLang = idioma === 'en' ? 'en' : 'pt-BR';

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
    {hrefAlternativaPt && <link rel="alternate" hreflang="pt" href={hrefAlternativaPt} />}
    {hrefAlternativaEn && <link rel="alternate" hreflang="en" href={hrefAlternativaEn} />}
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

Nota: `descricao` (prop opcional do `Layout`, usada por páginas que não sejam a home — nenhuma existe hoje, mas a interface pública do componente é preservada) continua string simples — quem passar essa prop no futuro passa a string já resolvida no idioma certo.

- [ ] **Step 2: `npm run check` e build**

```
npm run check
$env:CLIENTE = 'lumehostel'; npm run build
Select-String -Path dist/index.html -Pattern 'lang="pt-BR"'
Select-String -Path dist/en/index.html -Pattern 'lang="en"'
Select-String -Path dist/en/index.html -Pattern 'hreflang="pt"'
Select-String -Path dist/index.html -Pattern 'hreflang="en"'
```
Expected: cada arquivo tem o `lang` certo e aponta, via `hreflang`, para a versão no outro idioma.

```
$env:CLIENTE = 'demo'; npm run build
Select-String -Path dist/index.html -Pattern 'hreflang'
```
Expected: nenhuma ocorrência (`demo` não é bilíngue, `bilingue` é `false`, nenhuma tag `hreflang` é gerada).

- [ ] **Step 3: Commit**

```bash
git add template/src/layouts/Layout.astro
git commit -m "Adiciona lang/og:locale dinamicos e hreflang ao Layout"
```

---

## Task 11: `clientes/lumehostel/config.json` — tradução completa

**Files:**
- Modify: `clientes/lumehostel/config.json` (arquivo inteiro)

**Interfaces:**
- Consumes: schema da Task 1 (todo campo `{pt, en}` precisa das duas chaves preenchidas, senão a build quebra).

**Nota de escopo conhecida**: `foto.alt` (texto alternativo de imagem) **não é traduzido nesta rodada** — permanece só em português mesmo em `/en/`. Isso é uma lacuna real de acessibilidade/SEO na versão em inglês (leitor de tela lerá a descrição em português), mas ficou fora do campo de campos aprovado no spec; registrar como pendência para a autora decidir se entra numa rodada futura.

**Nota de dependência**: o `contato.tiktok` abaixo já reflete o config real (commit `713c212`, plano `redes-sociais-rodape.md`) — não remover.

- [ ] **Step 1: Substituir o `config.json` inteiro**

```json
{
  "nome": "LumeHostel",
  "idiomasDisponiveis": ["pt", "en"],
  "marca": { "logo": "logo-ambar.svg", "favicon": "simbolo-completo-terracota.svg", "simbolo": "simbolo-completo.svg", "appleTouchIcon": "apple-touch-icon.png", "faviconPng": "favicon-32.png" },
  "slogan": {
    "pt": "Seu porto seguro para renovar energias e seguir explorando",
    "en": "Your safe harbor to recharge and keep exploring"
  },
  "descricaoSeo": {
    "pt": "LumeHostel em Manaíra, João Pessoa: hostel pensado para nômades digitais, a poucos minutos da praia.",
    "en": "LumeHostel in Manaíra, João Pessoa: a hostel designed for digital nomads, minutes from the beach."
  },
  "sobre": {
    "historia": {
      "pt": "O LumeHostel fica em Manaíra, a poucos minutos a pé da praia, e nasce como ponto de orientação para quem viaja trabalhando. Aqui a ideia é simples: oferecer um porto seguro para renovar energias entre uma jornada e outra, com espaço pensado para quem precisa de foco durante o dia e descanso à noite. Um ambiente acolhedor para nômades digitais.",
      "en": "LumeHostel is in Manaíra, just a short walk from the beach, and was created as a landmark for people who travel while they work. The idea here is simple: offer a safe harbor to recharge between one journey and the next, with space designed for those who need focus during the day and rest at night. A welcoming environment for digital nomads."
    }
  },
  "acomodacoes": [
    {
      "nome": { "pt": "Dormitório Misto — 8 camas", "en": "Mixed Dorm — 8 beds" },
      "capacidade": { "pt": "Quarto misto com 8 camas (beliches)", "en": "Mixed room with 8 beds (bunks)" },
      "comodidades": [
        { "pt": "Ar-condicionado", "en": "Air conditioning" },
        { "pt": "Locker individual", "en": "Individual locker" },
        { "pt": "Tomada individual por cama", "en": "Individual power outlet per bed" },
        { "pt": "Toalhas inclusas", "en": "Towels included" }
      ],
      "fotos": [
        { "arquivo": "dormitorio-misto-8.jpg", "alt": "Dormitório misto amplo com cama de solteiro e beliches, armário branco e janela com persiana" }
      ]
    },
    {
      "nome": { "pt": "Dormitório Feminino — 4 camas", "en": "Female Dorm — 4 beds" },
      "capacidade": { "pt": "Quarto feminino com 4 camas (beliches)", "en": "Female room with 4 beds (bunks)" },
      "comodidades": [
        { "pt": "Ar-condicionado", "en": "Air conditioning" },
        { "pt": "Locker individual", "en": "Individual locker" },
        { "pt": "Tomada individual por cama", "en": "Individual power outlet per bed" },
        { "pt": "Toalhas inclusas", "en": "Towels included" }
      ],
      "fotos": [
        { "arquivo": "dormitorio-feminino-4.jpg", "alt": "Dormitório feminino com dois beliches de metal preto, armário e janela com grade decorativa" }
      ]
    },
    {
      "nome": { "pt": "Suíte Standard", "en": "Standard Suite" },
      "capacidade": { "pt": "2 pessoas, 1 cama de casal", "en": "2 people, 1 double bed" },
      "comodidades": [
        { "pt": "Ar-condicionado", "en": "Air conditioning" },
        { "pt": "Locker individual", "en": "Individual locker" },
        { "pt": "Tomada individual", "en": "Individual power outlet" },
        { "pt": "Toalhas inclusas", "en": "Towels included" }
      ],
      "fotos": [
        { "arquivo": "suite-standard.jpg", "alt": "Suíte privativa com cama de casal, mesa de madeira, cadeiras e espelho de corpo inteiro" }
      ]
    },
    {
      "nome": { "pt": "Dormitório Misto — 6 camas", "en": "Mixed Dorm — 6 beds" },
      "capacidade": { "pt": "Quarto misto com 6 camas (beliches)", "en": "Mixed room with 6 beds (bunks)" },
      "comodidades": [
        { "pt": "Ar-condicionado", "en": "Air conditioning" },
        { "pt": "Locker individual", "en": "Individual locker" },
        { "pt": "Tomada individual por cama", "en": "Individual power outlet per bed" },
        { "pt": "Toalhas inclusas", "en": "Towels included" }
      ],
      "fotos": [
        { "arquivo": "dormitorio-misto-6.jpg", "alt": "Dormitório misto com três beliches de metal e cortinas separando as camas" }
      ]
    },
    {
      "nome": { "pt": "Dormitório Feminino — 6 camas", "en": "Female Dorm — 6 beds" },
      "capacidade": { "pt": "Quarto feminino com 6 camas (beliches)", "en": "Female room with 6 beds (bunks)" },
      "comodidades": [
        { "pt": "Ar-condicionado", "en": "Air conditioning" },
        { "pt": "Locker individual", "en": "Individual locker" },
        { "pt": "Tomada individual por cama", "en": "Individual power outlet per bed" },
        { "pt": "Toalhas inclusas", "en": "Towels included" }
      ],
      "fotos": [
        { "arquivo": "dormitorio-feminino-6.jpg", "alt": "Dormitório feminino com beliches de metal preto, armário branco e piso de cerâmica" }
      ]
    },
    {
      "nome": { "pt": "Quarto Duplo", "en": "Double Room" },
      "capacidade": { "pt": "2 pessoas, 1 cama de casal", "en": "2 people, 1 double bed" },
      "comodidades": [
        { "pt": "Ar-condicionado", "en": "Air conditioning" },
        { "pt": "Locker individual", "en": "Individual locker" },
        { "pt": "Tomada individual", "en": "Individual power outlet" },
        { "pt": "Toalhas inclusas", "en": "Towels included" }
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
      { "pt": "Aeroporto Internacional de João Pessoa a cerca de 18 km", "en": "João Pessoa International Airport about 18 km away" },
      { "pt": "Rodoviária de João Pessoa a cerca de 9 km", "en": "João Pessoa bus station about 9 km away" },
      { "pt": "Praia de Manaíra a cerca de 8 minutos a pé", "en": "Manaíra Beach about an 8-minute walk" }
    ],
    "resumo": {
      "pt": "A poucos minutos da praia de Manaíra, no coração de João Pessoa.",
      "en": "Just minutes from Manaíra Beach, in the heart of João Pessoa."
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
      "nome": { "pt": "Cozinha compartilhada", "en": "Shared kitchen" },
      "descricao": { "pt": "Geladeira, micro-ondas, purificador de água e utensílios à disposição dos hóspedes", "en": "Fridge, microwave, water purifier and utensils available for guests" },
      "simbolo": "cozinha",
      "foto": { "arquivo": "cozinha.jpg", "alt": "Cozinha compartilhada do LumeHostel, com balcão e banquetas" }
    },
    {
      "nome": { "pt": "Pátio externo", "en": "Outdoor patio" },
      "descricao": { "pt": "Espaço com mesas para refeições e convivência entre hóspedes", "en": "Space with tables for meals and time together with other guests" },
      "simbolo": "patio",
      "foto": { "arquivo": "jardim.jpg", "alt": "Pátio de entrada do LumeHostel com mesas de madeira e a fachada com o logo ao fundo" }
    },
    {
      "nome": { "pt": "Coworking ergonômico", "en": "Ergonomic coworking space" },
      "descricao": { "pt": "Mesas amplas e cadeiras confortáveis para render no trabalho", "en": "Spacious desks and comfortable chairs to get work done" },
      "simbolo": "cowork",
      "foto": { "arquivo": "coworking.jpg", "alt": "Sala de coworking do LumeHostel com mesas, cadeiras ergonômicas e notebooks junto à janela" }
    },
    {
      "nome": { "pt": "Espaço com redes", "en": "Hammock area" },
      "descricao": { "pt": "Redes para descansar entre as atividades do dia", "en": "Hammocks to rest between the day's activities" },
      "simbolo": "rede",
      "foto": { "arquivo": "redario.jpg", "alt": "Redário do LumeHostel, com redes amarelas no corredor externo entre os quartos" }
    },
    {
      "nome": { "pt": "Churrasqueira", "en": "Barbecue area" },
      "descricao": { "pt": "Para reunir a galera em volta do fogo", "en": "For gathering everyone around the fire" },
      "simbolo": "churrasqueira"
    },
    {
      "nome": { "pt": "Sala de jogos", "en": "Games room" },
      "descricao": { "pt": "Diversão garantida entre um passeio e outro", "en": "Guaranteed fun between outings" },
      "simbolo": "jogos"
    },
    {
      "nome": { "pt": "Depósito de bagagem", "en": "Luggage storage" },
      "descricao": { "pt": "Suas malas guardadas antes do check-in e depois do check-out", "en": "Keep your bags safe before check-in and after check-out" },
      "simbolo": "bagagem"
    },
    {
      "nome": { "pt": "Ambiente acolhedor", "en": "Welcoming atmosphere" },
      "descricao": { "pt": "Elogiado pelos hóspedes pelo aconchego e pela organização", "en": "Praised by guests for its coziness and organization" },
      "simbolo": "acolhedor"
    }
  ],
  "regiao": [
    {
      "nome": { "pt": "Praia de Manaíra", "en": "Manaíra Beach" },
      "descricao": { "pt": "Praia urbana em frente ao bairro, com orla de bares e restaurantes", "en": "Urban beach right by the neighborhood, with a waterfront strip of bars and restaurants" },
      "distancia": "600 m",
      "foto": { "arquivo": "regiao-praia-manaira.jpg", "alt": "Faixa de areia e calçadão da Praia de Manaíra, com a orla ao fundo, em João Pessoa"},
      "credito": "Patrick / CC BY-SA 3.0"
    },
    {
      "nome": { "pt": "Orla do Bessa", "en": "Bessa Waterfront" },
      "descricao": { "pt": "Orla vizinha a Manaíra, com calçadão à beira-mar", "en": "Waterfront next to Manaíra, with a seaside boardwalk" },
      "distancia": "750 m",
      "foto": { "arquivo": "regiao-orla-bessa.jpg", "alt": "Orla da Praia do Bessa em João Pessoa" },
      "credito": "Matheus Jampa da Silva / CC BY-SA 4.0"
    },
    {
      "nome": { "pt": "Pôr do sol no Jacaré", "en": "Sunset at Jacaré Beach" },
      "descricao": { "pt": "Praia em Cabedelo, na foz do Rio Paraíba, conhecida pelo pôr do sol", "en": "Beach in Cabedelo, at the mouth of the Paraíba River, known for its sunset" },
      "distancia": "10 km",
      "foto": { "arquivo": "regiao-por-do-sol-jacare.jpg", "alt": "Pôr do sol na Praia do Jacaré, em João Pessoa" },
      "credito": "Marinelson Almeida / CC BY 2.0"
    },
    {
      "nome": { "pt": "Centro Histórico", "en": "Historic Center" },
      "descricao": { "pt": "Conjunto de prédios históricos do Centro/Varadouro de João Pessoa", "en": "Cluster of historic buildings in João Pessoa's Centro/Varadouro district" },
      "distancia": "4 km",
      "foto": { "arquivo": "regiao-centro-historico.jpg", "alt": "Vista do Centro Histórico de João Pessoa" },
      "credito": "Rogerio121402 / CC BY-SA 4.0"
    },
    {
      "nome": { "pt": "Farol do Cabo Branco", "en": "Cabo Branco Lighthouse" },
      "descricao": { "pt": "Farol no ponto mais oriental das Américas, no bairro Cabo Branco", "en": "Lighthouse at the easternmost point of the Americas, in the Cabo Branco neighborhood" },
      "distancia": "3,1 km",
      "foto": { "arquivo": "regiao-farol-cabo-branco.jpg", "alt": "Farol do Cabo Branco, em João Pessoa" }
    },
    {
      "nome": { "pt": "Estação Cabo Branco", "en": "Cabo Branco Station" },
      "descricao": { "pt": "Estação Cabo Branco de Ciência, Cultura e Artes, museu projetado por Oscar Niemeyer", "en": "Cabo Branco Station of Science, Culture and Arts, a museum designed by Oscar Niemeyer" },
      "distancia": "9 km",
      "foto": { "arquivo": "regiao-estacao-cabo-branco.jpg", "alt": "Estação Cabo Branco de Ciência, Cultura e Artes, em João Pessoa" },
      "credito": "A. Júnior / CC BY 2.0"
    }
  ],
  "depoimentos": [
    {
      "texto": {
        "pt": "Superou muito as minhas expectativas. É uma das melhores estruturas de Hostel que já encontrei. Tudo muito organizado, limpo, e nota-se muito capricho em tudo. Mas o que mais me chamou atenção: a equipe. Voltaria mais vezes só pela atenção, respeito, carinho e educação com a qual fui tratado.",
        "en": "It far exceeded my expectations. It's one of the best hostel setups I've ever found. Everything very organized, clean, and you can tell a lot of care went into it. But what struck me most: the team. I'd come back just for the attention, respect, care and courtesy I was treated with."
      },
      "nome": "Gabriel B.",
      "fonte": "via Google"
    },
    {
      "texto": {
        "pt": "Eu amei a experiência, é um ambiente acolhedor, tranquilo, me senti em casa. Se você procura um espaço que respeite a sua tranquilidade, descanso e ainda assim sugira atividades diferentes para te acolher e te fazer não se sentir sozinho na sua viagem, você vai ao lugar certo.",
        "en": "I loved the experience — it's a welcoming, peaceful environment, I felt right at home. If you're looking for a place that respects your peace and rest while still offering different activities to welcome you and keep you from feeling alone on your trip, this is the right place."
      },
      "nome": "Camila C.",
      "fonte": "via Google"
    },
    {
      "texto": {
        "pt": "Um dos melhores hostels que já fiquei. Muito limpo. Tinha noite de tacos, bate-papo com histórias de viajantes e teve uma aula de forró muito massa que participei e depois dançamos quadrilha. Foi muito divertido!",
        "en": "One of the best hostels I've stayed at. Very clean. There was taco night, chats swapping travel stories, and a really fun forró class I joined, and afterwards we danced quadrilha. It was a blast!"
      },
      "nome": "Desirree",
      "fonte": "via Booking"
    },
    {
      "texto": {
        "pt": "Feito de viajante para viajante. Ambiente acolhedor e familiar. Tudo muito limpo. Cozinha equipada. Quartos com ar-condicionado. Cowork excelente. Internet rápida.",
        "en": "Made by a traveler, for travelers. Welcoming, homey atmosphere. Everything very clean. Fully equipped kitchen. Air-conditioned rooms. Excellent coworking space. Fast internet."
      },
      "nome": "Rudá A.",
      "fonte": "via Google"
    }
  ],
  "destaques": [
    {
      "frase": { "pt": "Fique à vontade: a casa também é sua", "en": "Make yourself at home: this house is yours too" },
      "foto": { "arquivo": "destaque-cozinha.jpg", "alt": "Copa do LumeHostel com paredes amarelas, mural ondulado terracota e mesa de vidro com banquinhos" }
    },
    {
      "frase": { "pt": "Um porto seguro entre uma jornada e outra", "en": "A safe harbor between one journey and the next" },
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

- [ ] **Step 2: `npm run check` e build final do LumeHostel**

```
npm run check
$env:CLIENTE = 'lumehostel'; npm run build
Select-String -Path dist/en/index.html -Pattern 'Your safe harbor to recharge'
Select-String -Path dist/en/index.html -Pattern 'Mixed Dorm — 8 beds'
Select-String -Path dist/en/index.html -Pattern 'Translated from Portuguese'
Select-String -Path dist/index.html -Pattern 'Seu porto seguro para renovar energias'
```
Expected: todas as buscas encontram a linha correspondente — `/en/` mostra conteúdo real em inglês (slogan, acomodações, nota de tradução nos depoimentos), `/` continua em português.

- [ ] **Step 3: Commit**

```bash
git add clientes/lumehostel/config.json
git commit -m "Traduz conteudo do LumeHostel para ingles (slogan, acomodacoes, comodidades, regiao, depoimentos, localizacao)"
```

---

## Task 12: Verificação final — os 3 clientes + checklist manual

**Files:** nenhum (task só de verificação).

**Interfaces:** nenhuma nova.

- [ ] **Step 1: Build limpo dos 3 clientes**

```
$env:CLIENTE = 'demo'; npm run build
$env:CLIENTE = 'maravista'; npm run build
$env:CLIENTE = 'lumehostel'; npm run build
```
Expected: os três terminam sem erro.

- [ ] **Step 2: Confirmar que `demo` e `maravista` redirecionam `/en/` e não mostram o alternador**

```
$env:CLIENTE = 'demo'; npm run build
Select-String -Path dist/en/index.html -Pattern 'http-equiv="refresh"'
Select-String -Path dist/index.html -Pattern '>PT<|>EN<'

$env:CLIENTE = 'maravista'; npm run build
Select-String -Path dist/en/index.html -Pattern 'http-equiv="refresh"'
Select-String -Path dist/index.html -Pattern '>PT<|>EN<'
```
Expected: os dois clientes mostram o meta-refresh em `/en/` e nenhuma ocorrência de `PT`/`EN` no Nav.

- [ ] **Step 3: `astro check` limpo**

```
npm run check
```
Expected: passa sem erro.

- [ ] **Step 4: Checklist manual no navegador (LumeHostel)**

```
$env:CLIENTE = 'lumehostel'; npm run dev
```

No navegador:
1. Abrir `http://localhost:4321/` — confirmar site em português, alternador "PT / EN" no Nav com "PT" ativo (não clicável) e "EN" como link.
2. Clicar em "EN" — confirmar navegação para `/en/`, conteúdo inteiro em inglês (nav, hero, seções, rodapé, botões de WhatsApp).
3. **(cobre o bug de locale do Nav corrigido nesta revisão)** Em `/en/`, abrir o menu hambúrguer e clicar num item de seção (ex. "Rooms" ou "Amenities") — confirmar que a URL continua começando com `/en` e a página rola até a seção, sem voltar pra `/` em português.
4. Em `/en/`, clicar no logo "LumeHostel" no canto esquerdo do Nav — confirmar que a URL continua `/en/` (não volta pra `/`).
5. Na seção Depoimentos em `/en/`, confirmar que cada citação tem a nota "Translated from Portuguese." abaixo.
6. Clicar em "PT" a partir de `/en/` — confirmar volta para `/` em português.
7. Testar o botão de WhatsApp em `/en/` — confirmar que a mensagem pré-preenchida está em inglês.
8. No rodapé em `/en/`, confirmar o rótulo "Follow us" (em vez de "Siga a gente") acima dos ícones de Instagram/TikTok.
9. Ver código-fonte da página (`Ctrl+U`) em `/en/` — confirmar `<html lang="en">`, `<link rel="alternate" hreflang="pt" ...>` e `<link rel="alternate" hreflang="en" ...>`, `og:locale` = `en_US`.
10. Repetir a checagem de `hreflang`/`lang`/`og:locale` em `/` (esperado: `lang="pt-BR"`, `og:locale` = `pt_BR`).

- [ ] **Step 5: Parar o servidor de dev**

```
npx astro dev stop
```
(Astro 7 usa daemon persistente — `Ctrl+C` não é suficiente, ver `CLAUDE.md`.)

- [ ] **Step 6: Commit final (se houver algum ajuste do checklist manual)**

Se o Step 4 revelar algum ajuste necessário, corrigir, re-rodar o checklist relevante, e:
```bash
git add -A
git commit -m "Ajustes finais da verificacao manual do site bilingue do LumeHostel"
```
Se nada precisar de ajuste, esta task não gera commit próprio.
