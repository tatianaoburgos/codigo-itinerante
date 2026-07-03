# Site da marca Código Itinerante — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Landing page única do projeto Código Itinerante, dirigida a donos de hostel, com narrativa manifesto → dor → proposta → escopo → processo → autora → CTA WhatsApp.

**Architecture:** Novo projeto Astro mínimo em `site/` na raiz do monorepo (separado do motor `template/`), 1 página estática composta por componentes de seção, identidade do MIV (`docs/miv.md`), reaproveitando os SVGs de `marca/` via import direto (com `fs.allow` no Vite, mesmo padrão do template).

**Tech Stack:** Astro 5, Tailwind CSS 4 (`@tailwindcss/vite`), fontes via `@fontsource`, sharp (só para gerar a imagem OG).

**Spec:** `docs/superpowers/specs/2026-07-03-site-codigo-itinerante-design.md` — ler antes de começar.

## Global Constraints

- Todo conteúdo em português brasileiro; `lang="pt-BR"`.
- **Nunca citar Booking, Airbnb, Hostelworld ou qualquer OTA nominalmente** — dizer "plataformas de reserva". Dados de comissão: **de 10% a 25% por reserva, média histórica ~15%**.
- Regra do acento (MIV §1): Âmbar em fração pequena da página — itálico de headline, grifos, links, botão. Nunca página laranja. Preto `#000` e branco `#FFF` puros são proibidos — usar Breu e Cal.
- Itálico serifado (Instrument Serif) é tempero: **uma palavra ou expressão por título**, nunca frases inteiras.
- Sem JavaScript no cliente. Sem emojis em código. Página 100% estática.
- **CHECKPOINT DE TEXTO**: toda tarefa de seção termina mostrando o texto à autora ANTES do commit — nenhum texto entra sem aprovação dela. Textos abaixo são rascunhos de partida (a partir do material dela), não versões finais.
- Valores `[PROVISORIO]` em `dados.ts` (WhatsApp, e-mail, LinkedIn, nome, foto) são preenchidos na Task 9 com dados reais da autora.
- Não publicar números de noites nem valores em reais.
- Não há test runner no repo; o ciclo de verificação é `npm run build` (exit 0) + verificação visual no `npm run dev`.

---

### Task 1: Scaffold do projeto `site/`

**Files:**
- Create: `site/package.json`
- Create: `site/astro.config.mjs`
- Create: `site/tsconfig.json`
- Create: `site/src/styles/global.css`
- Create: `site/src/pages/index.astro` (provisório, substituído na Task 8)

**Interfaces:**
- Produces: tokens Tailwind `bg-breu`, `bg-grafite`, `text-cal`, `text-pedra`, `text-ambar`, `bg-ambar`, `hover:bg-barro`, `text-dourado`; fontes `font-sans` (Archivo), `font-serifa` (Instrument Serif), `font-mono` (IBM Plex Mono). Todas as tasks seguintes usam essas classes.

- [ ] **Step 1: Criar `site/package.json`**

```json
{
  "name": "site-codigo-itinerante",
  "type": "module",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview"
  },
  "dependencies": {
    "@fontsource-variable/archivo": "^5.2.0",
    "@fontsource/ibm-plex-mono": "^5.2.0",
    "@fontsource/instrument-serif": "^5.2.0",
    "@tailwindcss/vite": "^4.1.0",
    "astro": "^5.10.0",
    "tailwindcss": "^4.1.0"
  }
}
```

- [ ] **Step 2: Criar `site/astro.config.mjs`**

```js
// @ts-check
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// `site` fica indefinido até o deploy (Task 11); a imagem OG usa Astro.url como fallback.
export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
    server: {
      fs: {
        // Os SVGs da marca vivem fora da raiz do Vite (../marca); libera o monorepo.
        allow: [fileURLToPath(new URL('..', import.meta.url))],
      },
    },
  },
});
```

- [ ] **Step 3: Criar `site/tsconfig.json`**

```json
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "**/*"],
  "exclude": ["dist"]
}
```

- [ ] **Step 4: Criar `site/src/styles/global.css`**

Paleta e detalhes vêm de `marca/tokens.css` / MIV §3–4 (só o que o site escuro usa; Papel/Tinta/Queimado são de documentos claros — YAGNI aqui).

```css
/* Tema do site da marca Código Itinerante. Fonte de verdade: docs/miv.md + marca/tokens.css. */
@import "@fontsource-variable/archivo";
@import "@fontsource/instrument-serif/400-italic.css";
@import "@fontsource/ibm-plex-mono/400.css";
@import "@fontsource/ibm-plex-mono/500.css";
@import "tailwindcss";

@theme {
  --color-breu: #0a0a09;
  --color-grafite: #161513;
  --color-cal: #f4f1e8;
  --color-pedra: #97928a;
  --color-ambar: #e39a3b;
  --color-barro: #c4693f;
  --color-dourado: #efc780;

  --font-sans: "Archivo Variable", sans-serif;
  --font-serifa: "Instrument Serif", serif;
  --font-mono: "IBM Plex Mono", monospace;
}
```

- [ ] **Step 5: Criar `site/src/pages/index.astro` provisório**

```astro
---
import "../styles/global.css";
---
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <title>Código Itinerante</title>
  </head>
  <body class="bg-breu font-sans text-cal">
    <h1 class="p-8 text-2xl">scaffold ok — <em class="font-serifa italic text-ambar">noites</em></h1>
  </body>
</html>
```

- [ ] **Step 6: Instalar e verificar build**

Run (PowerShell): `cd site; npm install; npm run build`
Expected: instalação sem erros e build com exit 0 (`1 page(s) built`).

- [ ] **Step 7: Verificação visual**

Run: `cd site; npm run dev` e abrir `http://localhost:4321`.
Expected: fundo quase preto (Breu), texto claro em Archivo, palavra "noites" em serifa itálica âmbar. Isso prova tokens + as três fontes funcionando.

- [ ] **Step 8: Commit**

```powershell
git add site/package.json site/astro.config.mjs site/tsconfig.json site/src/ site/package-lock.json
git commit -m "Scaffold do site da marca em site/ (Astro + Tailwind + tokens do MIV)"
```

---

### Task 2: Layout com SEO, favicon e easter egg

**Files:**
- Create: `site/src/layouts/Layout.astro`
- Create: `site/public/favicon.svg` (cópia de `marca/monograma-claro.svg`)
- Modify: `site/src/pages/index.astro` (usar o Layout)

**Interfaces:**
- Produces: `Layout.astro` com `interface Props { titulo: string; descricao: string }`, slot único para o conteúdo. Todas as seções renderizam dentro dele.

- [ ] **Step 1: Copiar o favicon**

Run (PowerShell): `Copy-Item marca/monograma-claro.svg site/public/favicon.svg`
(Versão clara: legível na aba clara do navegador, o caso mais comum.)

- [ ] **Step 2: Criar `site/src/layouts/Layout.astro`**

O comentário HTML é o easter egg do spec — texto da autora, não alterar sem ela.

```astro
---
import "../styles/global.css";

interface Props {
  titulo: string;
  descricao: string;
}

const { titulo, descricao } = Astro.props;
const ogImage = new URL("og.png", Astro.site ?? Astro.url);
---

<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{titulo}</title>
    <meta name="description" content={descricao} />
    <meta property="og:title" content={titulo} />
    <meta property="og:description" content={descricao} />
    <meta property="og:image" content={ogImage} />
    <meta property="og:type" content="website" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <!--
      Qual é a ideia que você está tentando provar ao mundo?

      Que conhecimento se compartilha construindo soluções reais para
      pessoas reais. Que dá pra se conectar às pessoas e aos lugares,
      não apenas passar por eles.
    -->
  </head>
  <body class="bg-breu font-sans text-cal antialiased">
    <slot />
  </body>
</html>
```

- [ ] **Step 3: Reescrever `site/src/pages/index.astro` usando o Layout**

```astro
---
import Layout from "../layouts/Layout.astro";
---

<Layout
  titulo="Código Itinerante — sites para hostels, pagos em noites"
  descricao="Construo o site institucional do seu hostel em troca de noites de hospedagem. Sem dinheiro envolvido. Reserva direta pelo WhatsApp, sem comissão de plataforma."
>
  <h1 class="p-8 text-2xl">layout ok</h1>
</Layout>
```

- [ ] **Step 4: Verificar**

Run: `cd site; npm run build`
Expected: exit 0. Depois `npm run dev`, abrir a página, `Ctrl+U` (código-fonte):
o comentário do easter egg aparece no `<head>`, favicon do monograma na aba, metas OG presentes.

- [ ] **Step 5: Commit**

```powershell
git add site/src/layouts/Layout.astro site/public/favicon.svg site/src/pages/index.astro
git commit -m "Layout do site da marca: SEO, OG, favicon monograma e easter egg"
```

---

### Task 3: Dados de contato + componentes base (Eyebrow, BotaoWhatsApp)

**Files:**
- Create: `site/src/dados.ts`
- Create: `site/src/components/Eyebrow.astro`
- Create: `site/src/components/BotaoWhatsApp.astro`

**Interfaces:**
- Produces: `dados` (objeto com `nome`, `whatsapp`, `mensagemWhatsApp`, `email`, `linkedin`), `linkWhatsApp(): string`; `<Eyebrow texto destaque?>`; `<BotaoWhatsApp rotulo?>`. Usados pelas Tasks 4–8.

- [ ] **Step 1: Criar `site/src/dados.ts`**

```ts
/** Dados de contato e identidade da autora. Valores [PROVISORIO] são preenchidos na Task 9. */
export const dados = {
  nome: "Tatiana Burgos",
  /** Número no formato wa.me: DDI + DDD + número, só dígitos. [PROVISORIO] */
  whatsapp: "5500000000000",
  mensagemWhatsApp: "Oi! Tenho um hostel e quero saber mais sobre a permuta.",
  email: "[PROVISORIO]",
  linkedin: "[PROVISORIO]",
} as const;

/** Link wa.me com a mensagem pré-preenchida. */
export function linkWhatsApp(): string {
  return `https://wa.me/${dados.whatsapp}?text=${encodeURIComponent(dados.mensagemWhatsApp)}`;
}
```

- [ ] **Step 2: Criar `site/src/components/Eyebrow.astro`**

Rótulo de seção do MIV: mono caps, tracking largo, Cinza-pedra com destaque Âmbar.

```astro
---
interface Props {
  texto: string;
  destaque?: string;
}

const { texto, destaque } = Astro.props;
---

<p class="font-mono text-xs font-medium uppercase tracking-[0.12em] text-pedra">
  {texto}{destaque && <span class="text-ambar"> {destaque}</span>}
</p>
```

- [ ] **Step 3: Criar `site/src/components/BotaoWhatsApp.astro`**

Botão primário do MIV §5: pílula Âmbar, texto Breu, hover Barro.

```astro
---
import { linkWhatsApp } from "../dados";

interface Props {
  rotulo?: string;
}

const { rotulo = "Chamar no WhatsApp" } = Astro.props;
---

<a
  href={linkWhatsApp()}
  class="inline-block rounded-full bg-ambar px-7 py-3 font-medium text-breu transition-colors hover:bg-barro"
>
  {rotulo}
</a>
```

- [ ] **Step 4: Verificar**

Adicionar temporariamente ao `<Layout>` em `index.astro` (remover em seguida — a Task 4 substitui a página):

```astro
<Eyebrow texto="o" destaque="manifesto" />
<BotaoWhatsApp />
```

com os imports correspondentes. Run: `cd site; npm run build` → exit 0; no dev, o botão pílula âmbar leva para `wa.me/5500000000000` com a mensagem pré-preenchida.

- [ ] **Step 5: Commit**

```powershell
git add site/src/dados.ts site/src/components/
git commit -m "Dados de contato e componentes base do site da marca"
```

---

### Task 4: Hero

**Files:**
- Create: `site/src/components/Hero.astro`
- Modify: `site/src/pages/index.astro`

**Interfaces:**
- Consumes: `BotaoWhatsApp` (Task 3), `marca/wordmark-escuro.svg` (import de fora da raiz — habilitado pelo `fs.allow` da Task 1).
- Produces: `<Hero />` sem props.

- [ ] **Step 1: Criar `site/src/components/Hero.astro`**

Headline de referência validada no MIV §5. Hierarquia MIV: Archivo 700, tracking −0.035em, line-height ~1.05, itálico âmbar na palavra-chave.

```astro
---
import BotaoWhatsApp from "./BotaoWhatsApp.astro";
import wordmark from "../../../marca/wordmark-escuro.svg";
---

<header class="mx-auto flex min-h-screen w-full max-w-3xl flex-col justify-center px-6 py-16">
  <img src={wordmark.src} alt="Código Itinerante" class="w-56 md:w-72" />
  <h1 class="mt-14 text-4xl font-bold leading-[1.05] tracking-[-0.035em] md:text-6xl">
    Sites para hostels, pagos em <em class="font-serifa font-normal text-ambar">noites</em>.
  </h1>
  <p class="mt-6 max-w-xl text-lg leading-relaxed text-pedra">
    Eu construo o site institucional do seu hostel — e você me hospeda por
    algumas noites. Sem dinheiro envolvido. O site é seu, pra sempre.
  </p>
  <div class="mt-10">
    <BotaoWhatsApp />
  </div>
</header>
```

- [ ] **Step 2: Reescrever `site/src/pages/index.astro`**

Estrutura final da página; as seções das Tasks 5–8 são adicionadas aqui quando criadas.

```astro
---
import Layout from "../layouts/Layout.astro";
import Hero from "../components/Hero.astro";
---

<Layout
  titulo="Código Itinerante — sites para hostels, pagos em noites"
  descricao="Construo o site institucional do seu hostel em troca de noites de hospedagem. Sem dinheiro envolvido. Reserva direta pelo WhatsApp, sem comissão de plataforma."
>
  <Hero />
</Layout>
```

- [ ] **Step 3: Verificar**

Run: `cd site; npm run build` → exit 0. No dev: wordmark renderizado, headline com "noites" em itálico âmbar, botão funcional. Testar largura de celular (DevTools, 375px): sem estouro horizontal.

- [ ] **Step 4: CHECKPOINT DE TEXTO — mostrar headline e subtítulo à autora**

Apresentar o texto renderizado e ajustar até ela aprovar. Só então:

- [ ] **Step 5: Commit**

```powershell
git add site/src/components/Hero.astro site/src/pages/index.astro
git commit -m "Hero do site da marca com wordmark e headline do MIV"
```

---

### Task 5: Manifesto + Dor

**Files:**
- Create: `site/src/components/Manifesto.astro`
- Create: `site/src/components/Dor.astro`
- Modify: `site/src/pages/index.astro` (adicionar `<Manifesto />` e `<Dor />` após `<Hero />`)

**Interfaces:**
- Consumes: `Eyebrow` (Task 3).
- Produces: `<Manifesto />`, `<Dor />` sem props.

- [ ] **Step 1: Criar `site/src/components/Manifesto.astro`**

Rascunho a partir do texto da autora (2026-07-03): tecnologia sem gatekeepers, dádiva, "por onde minhas pernas andam".

```astro
---
import Eyebrow from "./Eyebrow.astro";
---

<section class="mx-auto w-full max-w-3xl px-6 py-20">
  <Eyebrow texto="o" destaque="manifesto" />
  <div class="mt-6 space-y-5 text-lg leading-relaxed">
    <p>
      Código Itinerante é um manifesto. Durante muito tempo, criar soluções
      digitais foi privilégio de quem tinha os instrumentos certos. Isso acabou.
    </p>
    <p>
      Eu viajo o Brasil construindo essas soluções para negócios reais — e
      recebo em troca o que preciso na estrada: um lugar pra ficar. Por onde
      minhas pernas andam, o projeto chega. Não quero só passar pelos lugares;
      quero fazer parte deles.
    </p>
    <p>
      Começando por quem me recebe toda semana:
      <em class="font-serifa text-ambar">hostels</em>.
    </p>
  </div>
</section>
```

- [ ] **Step 2: Criar `site/src/components/Dor.astro`**

Cena da autora quase intocada. **Sem nome de plataforma.** Único dado numérico da página.

```astro
---
import Eyebrow from "./Eyebrow.astro";
---

<section class="mx-auto w-full max-w-3xl px-6 py-20">
  <Eyebrow texto="o" destaque="problema" />
  <div class="mt-6 space-y-5 text-lg leading-relaxed">
    <p>
      Muitas vezes eu queria reservar diretamente com o hostel. Procurava o
      WhatsApp, tentava encontrar fotos confiáveis, entender os quartos,
      confirmar a localização. As informações estavam espalhadas entre redes
      sociais, mapas e plataformas de reserva. Depois de alguns minutos
      procurando, eu desistia — e reservava pela plataforma.
    </p>
    <p>
      O hostel perdia parte da diária em comissão. E eu perdia a chance de
      falar direto com quem ia me receber.
    </p>
  </div>
  <div class="mt-10 rounded-xl bg-grafite p-8">
    <p class="text-xl leading-relaxed">
      Plataformas de reserva cobram <strong class="text-ambar">de 10% a 25%
      de comissão</strong> por reserva — na média, cerca de 15%. Cada hóspede
      que reserva direto pelo seu WhatsApp é comissão que fica com você.
    </p>
  </div>
</section>
```

- [ ] **Step 3: Adicionar as seções em `index.astro`**

```astro
import Manifesto from "../components/Manifesto.astro";
import Dor from "../components/Dor.astro";
```

e, no corpo, após `<Hero />`:

```astro
<Manifesto />
<Dor />
```

- [ ] **Step 4: Verificar**

Run: `cd site; npm run build` → exit 0. No dev: as duas seções após o hero, card Grafite com o dado da comissão em destaque, nada de nome de OTA na página.

- [ ] **Step 5: CHECKPOINT DE TEXTO — aprovar manifesto e dor com a autora**

- [ ] **Step 6: Commit**

```powershell
git add site/src/components/Manifesto.astro site/src/components/Dor.astro site/src/pages/index.astro
git commit -m "Secoes manifesto e problema no site da marca"
```

---

### Task 6: Proposta + Escopo (recebe / não recebe)

**Files:**
- Create: `site/src/components/Proposta.astro`
- Create: `site/src/components/Escopo.astro`
- Modify: `site/src/pages/index.astro` (adicionar após `<Dor />`)

**Interfaces:**
- Consumes: `Eyebrow` (Task 3).
- Produces: `<Proposta />`, `<Escopo />` sem props.

- [ ] **Step 1: Criar `site/src/components/Proposta.astro`**

Frase-síntese em destaque com grifo âmbar (regra do acento: é O destaque da seção).

```astro
---
import Eyebrow from "./Eyebrow.astro";
---

<section class="mx-auto w-full max-w-3xl px-6 py-20">
  <Eyebrow texto="a" destaque="proposta" />
  <div class="mt-6 space-y-5 text-lg leading-relaxed">
    <p>
      Eu construo o site institucional completo do seu hostel — páginas, textos,
      fotos organizadas, botão de reserva direta pelo WhatsApp — e você me paga
      em noites de hospedagem.
    </p>
    <p class="font-serifa text-3xl leading-snug text-ambar md:text-4xl">
      É uma troca temporária por um produto permanente.
    </p>
    <p>
      Sem dinheiro envolvido. O único custo é o registro do domínio — que é
      seu e fica com você.
    </p>
  </div>
</section>
```

- [ ] **Step 2: Criar `site/src/components/Escopo.astro`**

Listas derivadas de `docs/projeto.md` §4–5 (espelhadas no spec §2.5). A coluna "não inclui" é deliberada — não suavizar.

```astro
---
import Eyebrow from "./Eyebrow.astro";

const inclui: string[] = [
  "Site responsivo, bonito no celular e no computador",
  "Acomodações, sobre o hostel, localização com mapa e contato",
  "Textos escritos por mim a partir do seu briefing",
  "Botão de reserva direta pelo seu WhatsApp",
  "SEO básico: seu hostel bem apresentado no Google",
  "Vinculação ao Perfil da Empresa no Google",
  "Domínio registrado e configurado",
  "Uma rodada de ajustes após a entrega",
];

const naoInclui: string[] = [
  "Motor de reservas com calendário e disponibilidade",
  "Pagamento online",
  "Integração com plataformas de reserva",
  "Manutenção contínua (alterações futuras são combinadas à parte)",
  "Produção de fotos profissionais",
  "Tráfego pago e gestão de redes sociais",
];
---

<section class="mx-auto w-full max-w-3xl px-6 py-20">
  <Eyebrow texto="o que você" destaque="recebe" />
  <div class="mt-6 grid gap-6 md:grid-cols-2">
    <div class="rounded-xl bg-grafite p-8">
      <h2 class="font-mono text-sm font-medium uppercase tracking-[0.12em] text-ambar">Está incluído</h2>
      <ul class="mt-5 space-y-3 leading-relaxed">
        {inclui.map((item) => <li>{item}</li>)}
      </ul>
    </div>
    <div class="rounded-xl border border-grafite p-8">
      <h2 class="font-mono text-sm font-medium uppercase tracking-[0.12em] text-pedra">Não está incluído</h2>
      <ul class="mt-5 space-y-3 leading-relaxed text-pedra">
        {naoInclui.map((item) => <li>{item}</li>)}
      </ul>
    </div>
  </div>
  <p class="mt-6 text-pedra">
    Prefiro te contar os limites agora do que te surpreender depois.
  </p>
</section>
```

- [ ] **Step 3: Adicionar em `index.astro`** (imports + `<Proposta /><Escopo />` após `<Dor />`)

- [ ] **Step 4: Verificar**

Run: `cd site; npm run build` → exit 0. No dev: frase-síntese grande em serifa âmbar; duas colunas viram uma no celular (375px).

- [ ] **Step 5: CHECKPOINT DE TEXTO — aprovar proposta e listas de escopo com a autora**

- [ ] **Step 6: Commit**

```powershell
git add site/src/components/Proposta.astro site/src/components/Escopo.astro site/src/pages/index.astro
git commit -m "Secoes proposta e escopo no site da marca"
```

---

### Task 7: Como funciona + Quem sou eu

**Files:**
- Create: `site/src/components/ComoFunciona.astro`
- Create: `site/src/components/QuemSouEu.astro`
- Modify: `site/src/pages/index.astro` (adicionar após `<Escopo />`)

**Interfaces:**
- Consumes: `Eyebrow` (Task 3), `dados` (Task 3).
- Produces: `<ComoFunciona />`, `<QuemSouEu />` sem props. A foto real entra na Task 9; até lá, bloco Grafite com aviso.

- [ ] **Step 1: Criar `site/src/components/ComoFunciona.astro`**

4 passos do spec §2.6. Sem números de noites/valores.

```astro
---
import Eyebrow from "./Eyebrow.astro";

const passos: { titulo: string; texto: string }[] = [
  { titulo: "Conversamos no WhatsApp", texto: "Você me conta do hostel e fechamos juntos o acordo de noites." },
  { titulo: "Você preenche o briefing", texto: "Um formulário com as informações do hostel, mais suas fotos em alta qualidade." },
  { titulo: "Quinze dias de construção", texto: "Eu escrevo os textos, monto o site e você acompanha." },
  { titulo: "Site no ar, controle seu", texto: "Domínio no seu nome, site sob seu controle total." },
];
---

<section class="mx-auto w-full max-w-3xl px-6 py-20">
  <Eyebrow texto="como" destaque="funciona" />
  <ol class="mt-8 space-y-8">
    {
      passos.map((passo, i) => (
        <li class="flex gap-6">
          <span class="font-mono text-2xl text-ambar">{i + 1}</span>
          <div>
            <h2 class="text-xl font-semibold">{passo.titulo}</h2>
            <p class="mt-1 leading-relaxed text-pedra">{passo.texto}</p>
          </div>
        </li>
      ))
    }
  </ol>
</section>
```

- [ ] **Step 2: Criar `site/src/components/QuemSouEu.astro`**

Dois pilares do spec §2.7: a estrada (citação dela) + a profissão. Foto única e abaixo da dobra (MIV §5).

```astro
---
import Eyebrow from "./Eyebrow.astro";
import { dados } from "../dados";
---

<section class="mx-auto w-full max-w-3xl px-6 py-20">
  <Eyebrow texto="quem" destaque="sou eu" />
  <div class="mt-8 grid items-start gap-8 md:grid-cols-[200px_1fr]">
    <div class="flex aspect-square items-center justify-center rounded-xl bg-grafite text-sm text-pedra">
      [PROVISORIO] foto
    </div>
    <div class="space-y-5 leading-relaxed">
      <p class="text-xl font-semibold">{dados.nome}</p>
      <p>
        Viajo pelo Brasil me hospedando em hostels e, ao mesmo tempo, trabalho
        como especialista em Ciência de Dados no Ministério da Gestão e da
        Inovação. Essa combinação me deixa ver os hostels pelos dois lados:
        como hóspede e como profissional que constrói soluções digitais.
      </p>
      <blockquote class="border-l-2 border-ambar pl-5 text-lg">
        Eu não estou construindo um site para um hostel que conheci por uma
        reunião de vídeo. Eu provavelmente dormi em um lugar como o seu na
        semana passada — e vou dormir em outro na semana que vem. Conheço a
        jornada do hóspede porque ela também é a minha.
      </blockquote>
      <p>
        <a href={dados.linkedin} class="text-ambar underline underline-offset-4 hover:text-barro">LinkedIn</a>
      </p>
    </div>
  </div>
</section>
```

- [ ] **Step 3: Adicionar em `index.astro`** (imports + `<ComoFunciona /><QuemSouEu />` após `<Escopo />`)

- [ ] **Step 4: Verificar**

Run: `cd site; npm run build` → exit 0. No dev: passos numerados em mono âmbar; citação com borda âmbar; grid vira coluna no celular.

- [ ] **Step 5: CHECKPOINT DE TEXTO — aprovar passos e "quem sou eu" com a autora**

- [ ] **Step 6: Commit**

```powershell
git add site/src/components/ComoFunciona.astro site/src/components/QuemSouEu.astro site/src/pages/index.astro
git commit -m "Secoes como funciona e quem sou eu no site da marca"
```

---

### Task 8: CTA final + footer

**Files:**
- Create: `site/src/components/CtaFinal.astro`
- Modify: `site/src/pages/index.astro` (adicionar após `<QuemSouEu />` — página completa)

**Interfaces:**
- Consumes: `BotaoWhatsApp`, `dados` (Task 3), `marca/monograma-escuro.svg`.
- Produces: `<CtaFinal />` sem props (inclui o footer).

- [ ] **Step 1: Criar `site/src/components/CtaFinal.astro`**

```astro
---
import BotaoWhatsApp from "./BotaoWhatsApp.astro";
import { dados } from "../dados";
import monograma from "../../../marca/monograma-escuro.svg";
---

<section class="mx-auto w-full max-w-3xl px-6 pb-10 pt-20">
  <div class="rounded-xl bg-grafite px-8 py-16 text-center">
    <h2 class="text-3xl font-bold tracking-[-0.035em] md:text-4xl">
      Tem um hostel? Vamos <em class="font-serifa font-normal text-ambar">conversar</em>.
    </h2>
    <p class="mx-auto mt-4 max-w-md leading-relaxed text-pedra">
      Me chama no WhatsApp e me conta do seu hostel. A conversa não custa
      nada — nem depois dela.
    </p>
    <div class="mt-8">
      <BotaoWhatsApp />
    </div>
  </div>
  <footer class="mt-16 flex items-center justify-between border-t border-grafite pt-8 text-sm text-pedra">
    <img src={monograma.src} alt="Código Itinerante" class="h-8" />
    <div class="flex gap-6">
      <a href={`mailto:${dados.email}`} class="hover:text-cal">{dados.email}</a>
      <a href={dados.linkedin} class="hover:text-cal">LinkedIn</a>
    </div>
  </footer>
</section>
```

- [ ] **Step 2: Adicionar em `index.astro`** — página completa:

```astro
---
import Layout from "../layouts/Layout.astro";
import Hero from "../components/Hero.astro";
import Manifesto from "../components/Manifesto.astro";
import Dor from "../components/Dor.astro";
import Proposta from "../components/Proposta.astro";
import Escopo from "../components/Escopo.astro";
import ComoFunciona from "../components/ComoFunciona.astro";
import QuemSouEu from "../components/QuemSouEu.astro";
import CtaFinal from "../components/CtaFinal.astro";
---

<Layout
  titulo="Código Itinerante — sites para hostels, pagos em noites"
  descricao="Construo o site institucional do seu hostel em troca de noites de hospedagem. Sem dinheiro envolvido. Reserva direta pelo WhatsApp, sem comissão de plataforma."
>
  <Hero />
  <Manifesto />
  <Dor />
  <Proposta />
  <Escopo />
  <ComoFunciona />
  <QuemSouEu />
  <CtaFinal />
</Layout>
```

- [ ] **Step 3: Verificar a página inteira**

Run: `cd site; npm run build` → exit 0. No dev, rolar do topo ao fim em desktop e 375px:
narrativa completa na ordem do spec, dois CTAs (hero e final), footer com monograma.

- [ ] **Step 4: CHECKPOINT DE TEXTO — aprovar CTA final e footer com a autora**

- [ ] **Step 5: Commit**

```powershell
git add site/src/components/CtaFinal.astro site/src/pages/index.astro
git commit -m "CTA final e footer: pagina completa do site da marca"
```

---

### Task 9: Dados reais da autora (contato + foto)

**Files:**
- Modify: `site/src/dados.ts`
- Create: `site/src/assets/tatiana.jpg` (foto fornecida pela autora)
- Modify: `site/src/components/QuemSouEu.astro` (trocar placeholder pela foto)

**Interfaces:**
- Consumes: `dados.ts` (Task 3), `QuemSouEu.astro` (Task 7).

- [ ] **Step 1: Pedir à autora**: número de WhatsApp comercial (DDI+DDD), e-mail de contato, URL do LinkedIn, confirmação do nome como aparece no site, e a foto (contexto estrada/hostel).

- [ ] **Step 2: Preencher `site/src/dados.ts`** com os valores reais (remover todos os `[PROVISORIO]`).

- [ ] **Step 3: Salvar a foto** em `site/src/assets/tatiana.jpg` e trocar o placeholder em `QuemSouEu.astro`:

```astro
---
import { Image } from "astro:assets";
import Eyebrow from "./Eyebrow.astro";
import { dados } from "../dados";
import foto from "../assets/tatiana.jpg";
---
```

e no lugar da `<div>` placeholder:

```astro
<Image src={foto} alt={`Foto de ${dados.nome}`} width="400" class="aspect-square rounded-xl object-cover" />
```

- [ ] **Step 4: Verificar**

Run: `cd site; npm run build` → exit 0 e `Select-String -Path site/src/dados.ts -Pattern "PROVISORIO"` → sem resultado. No dev: foto renderizada, botão WhatsApp abre o número real com a mensagem.

- [ ] **Step 5: Commit**

```powershell
git add site/src/dados.ts site/src/assets/tatiana.jpg site/src/components/QuemSouEu.astro
git commit -m "Dados reais de contato e foto da autora"
```

---

### Task 10: Imagem Open Graph

**Files:**
- Create: `site/scripts/gera-og.mjs`
- Create: `site/public/og.png` (gerado)
- Modify: `site/package.json` (devDependency `sharp` + script `og`)

**Interfaces:**
- Consumes: `marca/wordmark-escuro.svg`. O `Layout.astro` (Task 2) já aponta para `/og.png`.

- [ ] **Step 1: Instalar sharp e registrar o script**

Run: `cd site; npm install --save-dev sharp`
Em `site/package.json`, adicionar em `scripts`: `"og": "node scripts/gera-og.mjs"`.

- [ ] **Step 2: Criar `site/scripts/gera-og.mjs`**

```js
/** Gera public/og.png (1200x630): wordmark da marca centrado sobre fundo Breu. */
import sharp from "sharp";

const wordmark = await sharp("../marca/wordmark-escuro.svg", { density: 300 })
  .resize({ width: 840 })
  .png()
  .toBuffer();

await sharp({
  create: { width: 1200, height: 630, channels: 4, background: "#0a0a09" },
})
  .composite([{ input: wordmark, gravity: "center" }])
  .png()
  .toFile("public/og.png");

console.log("public/og.png gerado");
```

- [ ] **Step 3: Gerar e verificar**

Run: `cd site; npm run og`
Expected: `public/og.png gerado`. Abrir o arquivo: wordmark legível, centrado, fundo Breu, 1200×630.

- [ ] **Step 4: Verificar que a build serve a imagem**

Run: `cd site; npm run build` → exit 0 e `Test-Path site/dist/og.png` → `True`.

- [ ] **Step 5: Commit**

```powershell
git add site/scripts/gera-og.mjs site/public/og.png site/package.json site/package-lock.json
git commit -m "Imagem Open Graph gerada do wordmark para preview no WhatsApp"
```

---

### Task 11: Verificação final + docs + deploy

**Files:**
- Modify: `CLAUDE.md` (seção "Estado atual")
- Modify: `docs/projeto.md` (§13 Próximos passos)
- Modify: `site/astro.config.mjs` (campo `site`, após o deploy)

- [ ] **Step 1: Checklist dos critérios de sucesso do spec (§6)**

No `npm run preview` (build de produção), desktop e 375px:
- Rolando a página inteira, dá pra responder: o que é a permuta? o que recebo? o que não recebo? como começa? quem é a pessoa? — sem nenhum clique.
- Nenhuma menção nominal a OTA; dado de comissão correto (10–25%, ~15%).
- Âmbar em fração pequena da página (regra do acento).
- Sem erro no console do navegador; sem scroll horizontal no celular.

- [ ] **Step 2: Atualizar docs**

Em `CLAUDE.md` ("Estado atual") e `docs/projeto.md` (§13), registrar: site da marca construído em `site/` (landing única, spec de 2026-07-03), deploy na Vercel [status], domínio pendente.

- [ ] **Step 3: Commit dos docs**

```powershell
git add CLAUDE.md docs/projeto.md
git commit -m "Registra o site da marca em site/ nos docs do projeto"
```

- [ ] **Step 4: Deploy na Vercel (manual, pela autora)**

Novo projeto na Vercel apontando para este repo com **Root Directory = `site`** (framework Astro é autodetectado). Alternativa por CLI (a autora roda, prefixo `!`):

```
! cd site; npx vercel --prod
```

- [ ] **Step 5: Registrar a URL no config e regerar OG**

Com a URL do deploy (ex.: `https://codigo-itinerante.vercel.app`), adicionar em `site/astro.config.mjs`:

```js
export default defineConfig({
  site: "https://codigo-itinerante.vercel.app",
  // ... resto igual
});
```

Rebuild + redeploy. Testar mandando o link num chat do WhatsApp: preview com título, descrição e a imagem OG.

- [ ] **Step 6: Commit final**

```powershell
git add site/astro.config.mjs
git commit -m "Configura site URL do deploy para OG absoluto"
```

---

## Self-review (executado na escrita do plano)

- **Cobertura do spec**: 8 seções → Tasks 4–8; easter egg + SEO/OG → Task 2 e 10; identidade MIV → Task 1 (tokens) e componentes; `site/` separado + fs.allow → Task 1; dados reais → Task 9; critérios de sucesso → Task 11; domínio segue `[DEFINIR]` (Task 11 registra pendência). Sem lacunas.
- **Tipos/nomes consistentes**: `dados`, `linkWhatsApp()`, `Eyebrow {texto, destaque?}`, `BotaoWhatsApp {rotulo?}`, `Layout {titulo, descricao}` — conferidos entre tasks.
- **Placeholders**: os `[PROVISORIO]` são valores de dados a preencher na Task 9 (convenção do repo), não lacunas do plano.
