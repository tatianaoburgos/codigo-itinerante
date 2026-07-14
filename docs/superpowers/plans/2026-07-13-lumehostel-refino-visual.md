# LumeHostel — Refino Visual — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Unificar a tipografia do site do LumeHostel em Space Grotesk, corrigir o símbolo
da marca (hoje só a estrela, falta a chama), tirar as caixinhas com borda/sombra de
comodidades/região/depoimentos, levar a foto do hero até a borda de cima da tela com um
menu flutuante por cima, criar a seção "A vibe do hostel", e atualizar fotos/conteúdo com
material real trazido pela autora (6 tipos de quarto, redário, pátio à noite) e distâncias
oficiais do Booking.

**Architecture:** Segue a mesma composição one-page já existente (`template/src/pages/index.astro`).
As seções sem card ganham nova marcação (foto + texto solto, sem `bg-white`/`rounded-xl`);
o `Nav` deixa de ocupar espaço no fluxo (`position: fixed`) e alterna um atributo
`data-solido` via `IntersectionObserver` observando o `Hero`; a seção "A vibe" é um
componente novo (`Vibe.astro`) que renderiza um mosaico CSS multi-coluna a partir de um
campo opcional `vibe` no schema.

**Tech Stack:** Astro 5, Tailwind CSS 4, Zod, `astro:assets`, `@fontsource-variable/space-grotesk`.
Sem testes/linter no projeto — a validação de cada task é a build dos dois clientes
(`lumehostel` e `demo`) + conferência visual no navegador.

## Global Constraints

- **Nenhuma informação inventada sobre o hostel**: fotos e fatos só de Booking, Google
  (Maps/avaliações) e Instagram do LumeHostel; fatos sobre a região devem ser verificáveis.
- Preços nunca no site; CTA sempre WhatsApp.
- Português brasileiro em código/commits; sem emojis em código.
- Toda foto nova de área/comodidade do hostel precisa constar em
  `clientes/lumehostel/fotos/FONTES.md` com sua proveniência.
- Comandos de build rodam dentro de `template/` com env `CLIENTE`:
  `cd template && CLIENTE=lumehostel npm run build && CLIENTE=demo npm run build`.
  Ambas as builds devem passar ao final de toda task.
- Sem overengineering; sem programação defensiva.

---

### Task 1: Fonte única — Space Grotesk

**Files:**
- Modify: `template/package.json`
- Modify: `template/src/styles/temas/lumehostel.css`

**Interfaces:**
- Produces: `--font-display` e `--font-corpo` do tema lumehostel passam a resolver para
  `"Space Grotesk Variable"`.

- [ ] **Step 1: Instalar a fonte e remover a Fredoka**

```bash
cd template
npm install @fontsource-variable/space-grotesk
npm uninstall @fontsource-variable/fredoka
```

- [ ] **Step 2: Atualizar o tema**

Em `template/src/styles/temas/lumehostel.css`, trocar o import e os tokens de fonte:

```css
@import "@fontsource-variable/space-grotesk";
@import "@fontsource-variable/spline-sans-mono";

@theme {
  --color-mare: #fcbe35;
  --color-noite: #3a1509;
  --color-azulejo: #8f2d12;
  --color-sal: #fff3dc;
  --color-espuma: #c94520;
  --color-fitinha: #fcbe35;
  --color-zap: #25d366;

  --font-display: "Space Grotesk Variable", ui-sans-serif, system-ui, sans-serif;
  --font-corpo: "Space Grotesk Variable", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "Spline Sans Mono Variable", ui-monospace, monospace;
}
```

Atualizar o comentário no topo do arquivo: a fonte auxiliar do MIV (Arial Rounded MT
Bold) é proprietária; a substituta livre escolhida — Space Grotesk, geométrica e
angular, no espírito do logotipo — está em todo o site (display e corpo).

- [ ] **Step 3: Validar as duas builds**

Run: `cd template && CLIENTE=lumehostel npm run build && CLIENTE=demo npm run build`
Expected: PASS nas duas (demo não usa Fredoka, então não é afetado pela remoção do pacote).

- [ ] **Step 4: Commit**

```bash
git add template/package.json template/package-lock.json template/src/styles/temas/lumehostel.css
git commit -m "Tema LumeHostel: Space Grotesk substitui a Fredoka em todo o site"
```

---

### Task 2: Símbolo completo da marca (estrela + chama)

**Files:**
- Create: `clientes/lumehostel/marca/simbolo-completo.svg`
- Modify: `clientes/lumehostel/config.json`

**Interfaces:**
- Consumes: nenhuma mudança de código — `DivisorSimbolo.astro` e `MarcaDagua.astro` já
  leem `config.marca.simbolo` via `marca()` (`template/src/lib/fotos.ts`), sem alteração.
- Produces: `config.marca.simbolo` passa a apontar para o arquivo novo.

- [ ] **Step 1: Criar o SVG do símbolo completo**

O arquivo atual `clientes/lumehostel/marca/simbolo-ambar.svg` contém só a estrela (o
segundo `<path>` do logotipo). A chama é o primeiro `<path>` do logotipo completo
(`clientes/lumehostel/marca/logo-ambar.svg`). Criar
`clientes/lumehostel/marca/simbolo-completo.svg` com os dois traçados, viewBox ajustada
para cobrir ambos (chama: x 14.52–26.88, y 24.96–42.00; estrela: x 0–41.4, y 0–34.92 —
bbox combinado x:[0,41.4] y:[0,42], com 1 unidade de respiro):

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1.000 -1.000 43.400 44.000">
<path d="M 20.760 24.960 L 18.840 26.880 L 14.520 41.040 C 16.560 41.760 18.720 42.000 20.880 42.000 C 23.040 42.000 24.960 41.760 26.880 41.160 L 22.560 26.880 L 20.760 24.960 Z" fill="#fcbe35"/>
<path d="M 40.800 15.240 L 25.200 15.240 L 32.280 8.280 L 34.920 5.520 C 33.960 4.680 33.000 3.960 31.920 3.240 L 29.280 6.000 L 22.560 12.600 L 22.560 0.000 C 21.960 0.000 21.360 0.000 20.760 0.000 C 20.040 0.000 19.440 0.000 18.840 0.000 L 18.840 12.600 L 12.240 6.000 L 9.480 3.240 C 8.400 3.960 7.440 4.680 6.480 5.520 L 16.200 15.240 L 0.720 15.240 C 0.360 16.440 0.120 17.760 0.000 18.960 L 16.200 18.960 L 6.000 29.160 L 3.240 31.920 L 5.640 34.920 L 8.280 32.280 L 18.840 21.720 L 20.760 19.800 L 22.560 21.720 L 33.240 32.280 L 35.880 34.920 C 36.720 33.960 37.560 33.000 38.160 31.920 L 35.400 29.280 L 25.200 18.960 L 41.400 18.960 C 41.280 17.760 41.040 16.440 40.800 15.240 Z" fill="#fcbe35"/>
</svg>
```

- [ ] **Step 2: Apontar o config para o símbolo completo**

Em `clientes/lumehostel/config.json`, trocar a chave `simbolo` dentro de `marca`:

```json
"marca": { "logo": "logo-ambar.svg", "favicon": "simbolo-ambar.svg", "simbolo": "simbolo-completo.svg" },
```

(`favicon` continua com `simbolo-ambar.svg` — é usado minúsculo no ícone da aba, onde a
chama praticamente não apareceria; sem mudança aí.)

- [ ] **Step 3: Validar visualmente**

Run: `cd template && CLIENTE=lumehostel npm run build`
Expected: PASS. Abrir a build (`npm run preview` ou dev server) e conferir que os
divisores entre seções e a marca-d'água do hero/CTA mostram o símbolo completo
(estrela + chama), não só a estrela.

- [ ] **Step 4: Commit**

```bash
git add clientes/lumehostel/marca/simbolo-completo.svg clientes/lumehostel/config.json
git commit -m "Simbolo completo (estrela + chama) nos divisores e marca-d'agua"
```

---

### Task 3: Hero até a borda de cima, menu flutuante

**Files:**
- Modify: `template/src/components/Hero.astro`
- Modify: `template/src/components/Nav.astro`
- Modify: `template/src/styles/temas/lumehostel.css`

**Interfaces:**
- Produces: `<section id="hero">` em `Hero.astro` (usado pelo script do `Nav` para saber
  quando alternar o estado sólido). `<header data-solido="...">` em `Nav.astro`.

- [ ] **Step 1: Hero — remover a barra decorativa e marcar a seção**

Em `template/src/components/Hero.astro`, adicionar `id="hero"` à `<section>` e remover o
`<span>` decorativo (não pertence à marca):

```astro
---
import { Image } from 'astro:assets';
import { config } from '../lib/cliente';
import { foto, marca } from '../lib/fotos';
import BotaoWhatsApp from './BotaoWhatsApp.astro';
import MarcaDagua from './MarcaDagua.astro';

const logo = config.marca?.logo ? marca(config.marca.logo) : undefined;
---

<section id="hero" class="relative isolate flex min-h-svh items-end overflow-hidden bg-noite">
  <MarcaDagua />
  <Image
    src={foto('capa.jpg')}
    alt=""
    widths={[640, 1024, 1600]}
    sizes="100vw"
    loading="eager"
    class="absolute inset-0 -z-10 h-full w-full object-cover"
  />
  <div
    class="absolute inset-0 -z-10 bg-gradient-to-t from-noite/90 via-noite/50 to-noite/20"
    aria-hidden="true"
  >
  </div>
  <div class="mx-auto w-full max-w-5xl px-4 pt-32 pb-14">
    <h1 class="max-w-2xl">
      {
        logo ? (
          <img src={logo.src} alt={config.nome} class="h-14 w-auto sm:h-20" />
        ) : (
          <span class="font-display text-4xl font-bold text-white sm:text-6xl">{config.nome}</span>
        )
      }
    </h1>
    <p class="mt-4 max-w-xl text-lg text-white">{config.slogan}</p>
    <div class="mt-8">
      <BotaoWhatsApp tamanho="grande" />
    </div>
  </div>
</section>
```

(Só a linha `<span class="block h-1 w-16 bg-fitinha" aria-hidden="true"></span>` saiu, e
`id="hero"` entrou na section; o resto do arquivo é igual ao atual.)

- [ ] **Step 2: Nav — flutuante sobre o hero, sólido ao rolar**

Reescrever `template/src/components/Nav.astro` por completo:

```astro
---
import { config } from '../lib/cliente';
import { marca } from '../lib/fotos';
import BotaoWhatsApp from './BotaoWhatsApp.astro';

const abas = [
  { href: '/#acomodacoes', rotulo: 'Acomodações' },
  { href: '/#comodidades', rotulo: 'Comodidades' },
  { href: '/#regiao', rotulo: 'A região' },
  { href: '/#localizacao', rotulo: 'Localização' },
].filter((aba) => aba.href !== '/#regiao' || config.regiao);

const logo = config.marca?.logo ? marca(config.marca.logo) : undefined;
---

<header
  data-solido="false"
  class="fixed inset-x-0 top-0 z-50 border-b border-transparent bg-transparent text-white transition-colors duration-300 data-[solido=true]:border-sal data-[solido=true]:bg-espuma data-[solido=true]:text-noite"
>
  <nav
    aria-label="Principal"
    class="mx-auto flex max-w-5xl flex-col items-center gap-3 px-4 py-4 sm:flex-row sm:justify-between"
  >
    <a
      href="/"
      class="font-display text-xl font-bold text-mare focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-azulejo"
    >
      {logo ? <img src={logo.src} alt={config.nome} class="h-9 w-auto" /> : config.nome}
    </a>
    <div class="flex flex-wrap items-center justify-center gap-x-5 gap-y-2">
      {
        abas.map((aba) => (
          <a
            href={aba.href}
            class="border-b-2 border-transparent pb-0.5 text-sm font-bold transition hover:text-fitinha focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-azulejo"
          >
            {aba.rotulo}
          </a>
        ))
      }
      <BotaoWhatsApp />
    </div>
  </nav>
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
</script>
```

Note: os links das abas e o nome da marca não têm mais `text-noite` fixo — herdam a cor
do `<header>` (branco flutuando sobre o hero, `text-noite` quando sólido), exceto o nome
da marca que mantém `text-mare` (cor de destaque do tema) nos dois estados.

- [ ] **Step 3: Tema — texto branco no estado sólido do LumeHostel**

Em `template/src/styles/temas/lumehostel.css`, remover as duas regras antigas do header
(a classe `.border-b` não existe mais no `Nav`, então elas ficariam mortas):

```css
header.border-b {
  border-color: #8f2d1266;
  background: #c94520;
}

header.border-b a {
  color: #ffffff;
}
```

E acrescentar, no lugar delas, uma regra para o estado sólido: `bg-espuma` já resolve
para terracota no tema do LumeHostel, mas o texto padrão do estado sólido
(`text-noite`, marrom escuro) fica com contraste insuficiente sobre terracota — forçar
branco:

```css
/* Estado solido do menu flutuante (Nav.astro): bg-espuma ja e terracota neste tema,
   mas o text-noite padrao (marrom escuro) nao contrasta bem sobre terracota. */
header[data-solido="true"] {
  color: #ffffff;
}
```

- [ ] **Step 4: Validar as duas builds e conferir visualmente**

Run: `cd template && CLIENTE=lumehostel npm run build && CLIENTE=demo npm run build`
Expected: PASS nas duas.

No dev server (`CLIENTE=lumehostel npm run dev`), abrir no navegador e confirmar: a foto
do hero cobre até a borda de cima da tela (sem barra terracota atravessada); o menu
aparece transparente com texto branco sobre a foto; ao rolar para fora do hero, o menu
vira uma barra terracota sólida com o mesmo texto branco, permanecendo fixo no topo.

- [ ] **Step 5: Commit**

```bash
git add template/src/components/Hero.astro template/src/components/Nav.astro template/src/styles/temas/lumehostel.css
git commit -m "Hero ate a borda de cima; menu flutuante que fica solido ao rolar"
```

---

### Task 4: Fim das caixinhas — comodidades, região e depoimentos sem card

**Files:**
- Modify: `template/src/pages/index.astro`

**Interfaces:**
- Consumes: `config.comodidades` (`{nome, descricao?, foto?}[]`), `config.regiao`
  (`{nome, descricao, distancia, foto, credito?}[]`), `config.depoimentos`
  (`{texto, nome, fonte}[]`) — schemas inalterados nesta task.

- [ ] **Step 1: Comodidades — foto solta + lista fina para as sem foto**

Na seção `#comodidades` de `template/src/pages/index.astro`, separar as comodidades com
e sem foto no frontmatter, e trocar os cards por foto+texto direto (sem `bg-white`,
`rounded-xl`, `shadow-sm`):

No frontmatter do arquivo, acrescentar (depois dos imports):

```astro
const comodidadesComFoto = config.comodidades.filter((c) => c.foto);
const comodidadesSemFoto = config.comodidades.filter((c) => !c.foto);
```

Substituir o bloco atual da seção `#comodidades` (a `<div class="mt-8 grid items-start gap-6 sm:grid-cols-2">...</div>`) por:

```astro
      {
        comodidadesComFoto.length > 0 && (
          <div class="mt-8 grid gap-8 sm:grid-cols-2">
            {comodidadesComFoto.map((comodidade) => (
              <div>
                <Image
                  src={foto(comodidade.foto!.arquivo)}
                  alt={comodidade.foto!.alt}
                  widths={[480, 900]}
                  sizes="(min-width: 640px) 480px, 100vw"
                  class="aspect-video w-full object-cover"
                />
                <h3 class="mt-3 font-display text-lg font-bold text-mare">{comodidade.nome}</h3>
                {comodidade.descricao && <p class="mt-1 text-sm">{comodidade.descricao}</p>}
              </div>
            ))}
          </div>
        )
      }
      {
        comodidadesSemFoto.length > 0 && (
          <ul class="mt-8 grid gap-3 border-t border-sal/30 pt-6 sm:grid-cols-2">
            {comodidadesSemFoto.map((comodidade) => (
              <li class="flex gap-3">
                <span class="mt-2.5 h-0.5 w-4 shrink-0 bg-fitinha" aria-hidden="true" />
                <span>
                  <span class="font-bold">{comodidade.nome}</span>
                  {comodidade.descricao && <> — {comodidade.descricao}</>}
                </span>
              </li>
            ))}
          </ul>
        )
      }
```

- [ ] **Step 2: Região — foto solta, sem card**

Na seção `#regiao`, substituir:

```astro
<div class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
  {config.regiao.map((ponto) => (
    <article class="overflow-hidden rounded-xl bg-white shadow-sm">
      <Image
        src={foto(ponto.foto.arquivo)}
        alt={ponto.foto.alt}
        widths={[400, 800]}
        sizes="(min-width: 1024px) 320px, (min-width: 640px) 480px, 100vw"
        class="aspect-4/3 w-full object-cover"
      />
      <div class="p-4">
        <p class="font-mono text-xs tracking-widest text-azulejo uppercase">
          {ponto.distancia}
        </p>
        <h3 class="mt-1 font-display text-lg font-bold text-mare">{ponto.nome}</h3>
        <p class="mt-1 text-sm">{ponto.descricao}</p>
        {ponto.credito && <p class="mt-2 text-xs opacity-60">Foto: {ponto.credito}</p>}
      </div>
    </article>
  ))}
</div>
```

por:

```astro
<div class="mt-8 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
  {config.regiao.map((ponto) => (
    <article>
      <Image
        src={foto(ponto.foto.arquivo)}
        alt={ponto.foto.alt}
        widths={[400, 800]}
        sizes="(min-width: 1024px) 320px, (min-width: 640px) 480px, 100vw"
        class="aspect-4/3 w-full object-cover"
      />
      <p class="mt-3 font-mono text-xs tracking-widest text-azulejo uppercase">
        {ponto.distancia}
      </p>
      <h3 class="mt-1 font-display text-lg font-bold text-mare">{ponto.nome}</h3>
      <p class="mt-1 text-sm">{ponto.descricao}</p>
      {ponto.credito && <p class="mt-2 text-xs opacity-60">Foto: {ponto.credito}</p>}
    </article>
  ))}
</div>
```

- [ ] **Step 3: Depoimentos — citação grande com barra lateral, sem moldura**

Na seção `#depoimentos`, substituir:

```astro
<div class="mt-8 grid gap-6 sm:grid-cols-2">
  {config.depoimentos.map((depoimento) => (
    <figure class="rounded-xl bg-white p-6 shadow-sm">
      <blockquote class="leading-relaxed">"{depoimento.texto}"</blockquote>
      <figcaption class="mt-4 text-sm font-bold">
        {depoimento.nome} <span class="font-normal opacity-70">— {depoimento.fonte}</span>
      </figcaption>
    </figure>
  ))}
</div>
```

por:

```astro
<div class="mt-8 grid gap-8 sm:grid-cols-2">
  {config.depoimentos.map((depoimento) => (
    <figure class="border-l-4 border-noite pl-5">
      <blockquote class="text-lg leading-relaxed text-noite">“{depoimento.texto}”</blockquote>
      <figcaption class="mt-4 text-sm font-bold text-noite">
        {depoimento.nome} <span class="font-normal opacity-70">— {depoimento.fonte}</span>
      </figcaption>
    </figure>
  ))}
</div>
```

(A seção `#depoimentos` tem fundo `bg-mare` (âmbar); o texto explícito `text-noite` — marrom
escuro — garante contraste, já que o texto padrão do body é branco, invisível sobre âmbar.)

- [ ] **Step 4: Validar as duas builds e conferir visualmente**

Run: `cd template && CLIENTE=lumehostel npm run build && CLIENTE=demo npm run build`
Expected: PASS nas duas. No dev server, confirmar que nenhuma das três seções tem
card/borda/sombra — a foto e o texto ficam soltos sobre o fundo da seção.

- [ ] **Step 5: Commit**

```bash
git add template/src/pages/index.astro
git commit -m "Fim das caixinhas: comodidades, regiao e depoimentos sem card"
```

---

### Task 5: Seção "A vibe do hostel" — schema, componente e primeiras fotos

**Files:**
- Modify: `template/src/lib/schema.ts`
- Create: `template/src/components/Vibe.astro`
- Modify: `template/src/components/Nav.astro`
- Modify: `template/src/pages/index.astro`
- Modify: `clientes/lumehostel/config.json`
- Create: `clientes/lumehostel/fotos/vibe-patio-noite.jpg`
- Create: `clientes/lumehostel/fotos/vibe-redario.jpg`
- Modify: `clientes/lumehostel/fotos/FONTES.md`

**Interfaces:**
- Produces: `vibe?: Foto[]` em `ConfigCliente` (schema). `<Vibe />` (sem props, lê
  `config.vibe`).

- [ ] **Step 1: Schema — campo `vibe` opcional**

Em `template/src/lib/schema.ts`, no `configClienteSchema`, acrescentar depois de
`depoimentos`:

```ts
  depoimentos: z.array(depoimentoSchema).optional(),
  vibe: z.array(fotoSchema).optional(),
```

- [ ] **Step 2: Componente `Vibe.astro` — mosaico multi-coluna**

Criar `template/src/components/Vibe.astro`:

```astro
---
import { Image } from 'astro:assets';
import { config } from '../lib/cliente';
import { foto } from '../lib/fotos';
---

{
  config.vibe && (
    <div class="columns-2 gap-3 sm:columns-3">
      {config.vibe.map((imagem) => (
        <Image
          src={foto(imagem.arquivo)}
          alt={imagem.alt}
          widths={[300, 600]}
          sizes="(min-width: 640px) 33vw, 50vw"
          class="mb-3 w-full break-inside-avoid object-cover"
        />
      ))}
    </div>
  )
}
```

Cada foto mantém sua proporção original (sem `aspect-*` forçado), criando o efeito de
mosaico com alturas variadas — a coluna CSS (`columns-2`/`sm:columns-3`) distribui as
imagens automaticamente, e `break-inside-avoid` evita que uma imagem seja cortada entre
colunas.

- [ ] **Step 3: Copiar as duas fotos já disponíveis**

```powershell
Copy-Item "C:\Users\tatia\Downloads\patio externo.jpg" "clientes\lumehostel\fotos\vibe-patio-noite.jpg"
Copy-Item "C:\Users\tatia\Downloads\redário.jpg" "clientes\lumehostel\fotos\vibe-redario.jpg"
```

- [ ] **Step 4: Wire — inserir a seção entre Comodidades e A região, e no menu**

Em `template/src/components/Nav.astro`, acrescentar a aba condicional (o array `abas` já
tem o filtro de `/#regiao`; acrescentar o de `/#vibe` na mesma cadeia, na posição entre
Comodidades e A região):

```astro
const abas = [
  { href: '/#acomodacoes', rotulo: 'Acomodações' },
  { href: '/#comodidades', rotulo: 'Comodidades' },
  { href: '/#vibe', rotulo: 'A vibe' },
  { href: '/#regiao', rotulo: 'A região' },
  { href: '/#localizacao', rotulo: 'Localização' },
]
  .filter((aba) => aba.href !== '/#vibe' || config.vibe)
  .filter((aba) => aba.href !== '/#regiao' || config.regiao);
```

Em `template/src/pages/index.astro`, importar `Vibe` (junto dos outros imports de
componente) e inserir a nova seção depois do bloco de comodidades (depois do
`</section>` que fecha `#comodidades`, antes do `<DivisorSimbolo />` que antecede a
região):

```astro
import Vibe from '../components/Vibe.astro';
```

```astro
  <DivisorSimbolo />

  {
    config.vibe && (
      <section id="vibe" class="mx-auto max-w-5xl scroll-mt-20 px-4 py-14">
        <TituloSecao eyebrow="A vibe">Como é ficar aqui</TituloSecao>
        <div class="mt-8">
          <Vibe />
        </div>
      </section>
    )
  }

  {config.vibe && <DivisorSimbolo />}
```

(A `<DivisorSimbolo />` que já existia entre Comodidades e Região permanece onde estava,
imediatamente após a seção Comodidades — o bloco acima entra depois dela, e a região
segue com seu próprio par de divisores como já existe hoje.)


- [ ] **Step 5: Dados — adicionar `vibe` ao config do LumeHostel**

Em `clientes/lumehostel/config.json`, acrescentar depois de `depoimentos`:

```json
  "vibe": [
    { "arquivo": "vibe-patio-noite.jpg", "alt": "Pátio do LumeHostel à noite, com mesa comunitária e varal de luzes" },
    { "arquivo": "vibe-redario.jpg", "alt": "Redário do LumeHostel, com redes amarelas no corredor externo entre os quartos" }
  ]
```

- [ ] **Step 6: Registrar a proveniência**

Em `clientes/lumehostel/fotos/FONTES.md`, acrescentar as duas fotos: origem "enviada
pela autora, foto real do estabelecimento" (não são de banco de imagens nem de
terceiros — são fotos próprias do hostel).

- [ ] **Step 7: Validar as duas builds e conferir visualmente**

Run: `cd template && CLIENTE=lumehostel npm run build && CLIENTE=demo npm run build`
Expected: PASS nas duas (`demo` não tem `config.vibe`, então a seção não renderiza nele —
confirmar que o build do demo não quebra por isso).

No dev server, confirmar: a aba "A vibe" aparece no menu do LumeHostel; a seção mostra as
duas fotos em mosaico (colunas de alturas diferentes, sem card).

- [ ] **Step 8: Commit**

```bash
git add template/src/lib/schema.ts template/src/components/Vibe.astro template/src/components/Nav.astro template/src/pages/index.astro clientes/lumehostel/config.json clientes/lumehostel/fotos/vibe-patio-noite.jpg clientes/lumehostel/fotos/vibe-redario.jpg clientes/lumehostel/fotos/FONTES.md
git commit -m "Secao 'A vibe do hostel': schema, componente de mosaico e primeiras fotos"
```

---

### Task 6: Curadoria de mais fotos para "A vibe" e para o coworking

> Task de pesquisa/curadoria com navegador, não de código. Fonte de verdade: galerias
> públicas do LumeHostel no Google Maps e no Booking — fotos publicadas pelo próprio
> estabelecimento, nunca de hóspede/banco de imagens.

**Files:**
- Create: `clientes/lumehostel/fotos/vibe-<assunto>.jpg` (6 a 10 fotos)
- Create: `clientes/lumehostel/fotos/coworking.jpg` (se encontrada)
- Modify: `clientes/lumehostel/config.json` (`vibe` ampliado; `foto` da comodidade
  "Coworking ergonômico", se encontrada)
- Modify: `clientes/lumehostel/fotos/FONTES.md`

**Nota importante:** os 13 arquivos `lume hostel vibe *.htm` em `~/Downloads` (páginas do
Google Maps salvas pela autora) **não são utilizáveis por parsing** — todos embutem a
mesma URL genérica de foto de perfil do estabelecimento (a galeria de fotos do Maps é
renderizada via JavaScript depois do carregamento, então o HTML salvo não contém a foto
específica que a autora estava vendo). Não gastar tempo tentando extrair URLs deles.

O arquivo `lume hostel coworking.url`, por outro lado, **é utilizável**: é um atalho para
uma URL de visualização de foto específica do Google Maps, com o ID da foto embutido no
parâmetro `!1s...` (diferente da URL genérica). Abrir essa URL ao vivo no navegador deve
levar direto à foto que a autora queria indicar como o coworking.

- [ ] **Step 1: Tentar a foto do coworking pelo atalho**

Ler `C:\Users\tatia\Downloads\lume hostel coworking.url` para obter a URL, abrir no
Claude in Chrome (`navigate`), e usar `read_page`/`javascript_tool` para localizar a
`<img>` principal do visualizador de foto (mesma técnica que funcionou nas fotos de
cozinha/pátio da rodada anterior: ler os `src` das tags `<img>` direto do DOM quando o
modal de galeria não abre por clique). Se a imagem carregada mostrar claramente uma área
de coworking (mesas, cadeiras, ambiente de trabalho), baixar em alta resolução
(`curl -sL "<url>=w1600" -o clientes/lumehostel/fotos/coworking.jpg`) e confirmar
visualmente com a ferramenta Read antes de manter.

- [ ] **Step 2: Explorar a galeria pública do Google Maps e do Booking**

Abrir a listagem do LumeHostel no Google Maps
(`https://www.google.com/maps/search/lume+hostel+joão+pessoa`) e no Booking
(`https://www.booking.com/hotel/br/lumehostel.pt-br.html`), navegar pela galeria de
fotos publicada pelo próprio estabelecimento. Selecionar 6 a 10 fotos que transmitam "a
vibe" do hostel — ambientes sociais, entrada, mural, luzes, pátio em outros horários —
DISTINTAS das já em uso (`capa.jpg`, `cozinha.jpg`, `jardim.jpg`, `vibe-patio-noite.jpg`,
`vibe-redario.jpg`, e as fotos de quarto da Task 7). Baixar cada uma em alta resolução,
nomear descritivamente (`vibe-mural.jpg`, `vibe-entrada.jpg` etc.).

- [ ] **Step 3: Verificar visualmente cada foto antes de manter**

Usar a ferramenta Read em cada `.jpg` baixado. Rejeitar: frames de vídeo/reel com
legenda queimada na imagem, fotos verticais de stories, fotos com rosto de hóspede
identificável, fotos de baixa qualidade/desfocadas. Regra já aplicada com sucesso na
curadoria anterior do LumeHostel — não afrouxar aqui.

- [ ] **Step 4: Atualizar os dados**

Em `clientes/lumehostel/config.json`: ampliar o array `vibe` com as fotos aprovadas
(`arquivo` + `alt` descrevendo o que a foto realmente mostra). Se a foto de coworking foi
aprovada no Step 1, adicionar `foto: {arquivo: "coworking.jpg", alt: "..."}` à comodidade
`{ "nome": "Coworking ergonômico" }` (hoje sem foto).

- [ ] **Step 5: Registrar a proveniência**

Em `clientes/lumehostel/fotos/FONTES.md`, acrescentar uma linha por arquivo novo: origem
(Google Maps ou Booking, galeria do próprio estabelecimento), e observação de que
nenhuma foto de hóspede foi usada.

- [ ] **Step 6: Validar a build e conferir visualmente**

Run: `cd template && CLIENTE=lumehostel npm run build`
Expected: PASS. No dev server, confirmar que a seção "A vibe" tem um mosaico mais rico, e
que a comodidade "Coworking ergonômico" ganhou foto (se encontrada — senão, ela continua
como linha na lista sem foto, o que é aceitável).

- [ ] **Step 7: Commit**

```bash
git add clientes/lumehostel/fotos clientes/lumehostel/config.json
git commit -m "Mais fotos para 'A vibe' e foto do coworking, das galerias publicas do hostel"
```

---

### Task 7: Seis tipos de acomodação, cada um com sua própria foto

**Files:**
- Create: `clientes/lumehostel/fotos/dormitorio-misto-6.jpg`
- Create: `clientes/lumehostel/fotos/dormitorio-misto-8.jpg`
- Create: `clientes/lumehostel/fotos/dormitorio-feminino-4.jpg`
- Create: `clientes/lumehostel/fotos/dormitorio-feminino-6.jpg`
- Create: `clientes/lumehostel/fotos/quarto-duplo.jpg`
- Create: `clientes/lumehostel/fotos/suite-standard.jpg`
- Modify: `clientes/lumehostel/config.json`
- Modify: `clientes/lumehostel/fotos/FONTES.md`

**Interfaces:**
- Consumes: `acomodacaoSchema` (`{nome, capacidade, comodidades, fotos}[]`) —
  inalterado; esta task só muda dados, não schema.

O Booking lista 6 tipos de quarto (hoje o site agrupa em 4, com fotos repetidas entre
Dormitório Misto/Feminino e entre Quarto Duplo/Suíte). A autora já baixou a foto real de
cada um dos 6 tipos.

- [ ] **Step 1: Copiar e renomear as fotos**

```powershell
Copy-Item "C:\Users\tatia\Downloads\Cama em Dormitório Misto com 6 Camas.jpg" "clientes\lumehostel\fotos\dormitorio-misto-6.jpg"
Copy-Item "C:\Users\tatia\Downloads\Cama em Dormitório Misto com 8 Camas.jpg" "clientes\lumehostel\fotos\dormitorio-misto-8.jpg"
Copy-Item "C:\Users\tatia\Downloads\Cama em Dormitório Feminino com 4 Camas.jpg" "clientes\lumehostel\fotos\dormitorio-feminino-4.jpg"
Copy-Item "C:\Users\tatia\Downloads\Cama em Dormitório Feminino com 6 Camas.jpg" "clientes\lumehostel\fotos\dormitorio-feminino-6.jpg"
Copy-Item "C:\Users\tatia\Downloads\Quarto Duplo.jpg" "clientes\lumehostel\fotos\quarto-duplo.jpg"
Copy-Item "C:\Users\tatia\Downloads\Suíte Standard.jpg" "clientes\lumehostel\fotos\suite-standard.jpg"
```

- [ ] **Step 2: Substituir o array `acomodacoes` no config**

Em `clientes/lumehostel/config.json`, substituir o array `acomodacoes` inteiro por:

```json
  "acomodacoes": [
    {
      "nome": "Dormitório Misto",
      "capacidade": "Quarto misto com 6 camas (beliches)",
      "comodidades": ["Ar-condicionado", "Locker individual", "Tomada individual por cama", "Toalhas inclusas"],
      "fotos": [
        { "arquivo": "dormitorio-misto-6.jpg", "alt": "Dormitório misto com três beliches de metal e cortinas separando as camas" }
      ]
    },
    {
      "nome": "Dormitório Misto",
      "capacidade": "Quarto misto com 8 camas (beliches)",
      "comodidades": ["Ar-condicionado", "Locker individual", "Tomada individual por cama", "Toalhas inclusas"],
      "fotos": [
        { "arquivo": "dormitorio-misto-8.jpg", "alt": "Dormitório misto amplo com cama de solteiro e beliches, armário branco e janela com persiana" }
      ]
    },
    {
      "nome": "Dormitório Feminino",
      "capacidade": "Quarto feminino com 4 camas (beliches)",
      "comodidades": ["Ar-condicionado", "Locker individual", "Tomada individual por cama", "Toalhas inclusas"],
      "fotos": [
        { "arquivo": "dormitorio-feminino-4.jpg", "alt": "Dormitório feminino com dois beliches de metal preto, armário e janela com grade decorativa" }
      ]
    },
    {
      "nome": "Dormitório Feminino",
      "capacidade": "Quarto feminino com 6 camas (beliches)",
      "comodidades": ["Ar-condicionado", "Locker individual", "Tomada individual por cama", "Toalhas inclusas"],
      "fotos": [
        { "arquivo": "dormitorio-feminino-6.jpg", "alt": "Dormitório feminino com beliches de metal preto, armário branco e piso de cerâmica" }
      ]
    },
    {
      "nome": "Quarto Duplo",
      "capacidade": "2 pessoas, 1 cama de casal",
      "comodidades": ["Ar-condicionado", "Locker individual", "Tomada individual", "Toalhas inclusas"],
      "fotos": [
        { "arquivo": "quarto-duplo.jpg", "alt": "Quarto privativo com cama de casal, cortinas marrons, quadros na parede e mesa com cadeiras" }
      ]
    },
    {
      "nome": "Suíte Standard",
      "capacidade": "2 pessoas, 1 cama de casal",
      "comodidades": ["Ar-condicionado", "Locker individual", "Tomada individual", "Toalhas inclusas"],
      "fotos": [
        { "arquivo": "suite-standard.jpg", "alt": "Suíte privativa com cama de casal, mesa de madeira, cadeiras e espelho de corpo inteiro" }
      ]
    }
  ],
```

- [ ] **Step 3: Registrar a proveniência**

Em `clientes/lumehostel/fotos/FONTES.md`, acrescentar as 6 fotos com origem "enviada
pela autora, foto real do quarto correspondente no hostel".

- [ ] **Step 4: Validar a build e conferir visualmente**

Run: `cd template && CLIENTE=lumehostel npm run build`
Expected: PASS. No dev server, confirmar que o carrossel de acomodações mostra 6 cards,
cada um com foto própria (sem repetição).

- [ ] **Step 5: Commit**

```bash
git add clientes/lumehostel/fotos clientes/lumehostel/config.json
git commit -m "Seis tipos de acomodacao (Booking) com foto propria cada, sem repeticao"
```

---

### Task 8: Distâncias oficiais do Booking e atualização das pendências

**Files:**
- Modify: `clientes/lumehostel/config.json`
- Modify: `clientes/lumehostel/PENDENCIAS.md`

O Booking publica as distâncias oficiais do próprio hostel ("Proximidades da
acomodação"), diferentes (e mais confiáveis) das medidas atualmente no config, que
tinham sido calculadas por rota de carro entre centroides de bairro.

- [ ] **Step 1: Corrigir as distâncias em `regiao`**

Em `clientes/lumehostel/config.json`, atualizar o campo `distancia` de cada ponto
conforme o Booking (distâncias em linha reta/oficiais do estabelecimento):

```json
  "regiao": [
    {
      "nome": "Praia de Manaíra",
      "descricao": "Praia urbana em frente ao bairro, com orla de bares e restaurantes",
      "distancia": "600 m",
      "foto": { "arquivo": "regiao-praia-manaira.jpg", "alt": "Faixa de areia e calçadão da Praia de Manaíra, com a orla ao fundo, em João Pessoa"},
      "credito": "Patrick / CC BY-SA 3.0"
    },
    {
      "nome": "Orla do Bessa",
      "descricao": "Orla vizinha a Manaíra, com calçadão à beira-mar",
      "distancia": "750 m",
      "foto": { "arquivo": "regiao-orla-bessa.jpg", "alt": "Orla da Praia do Bessa em João Pessoa" },
      "credito": "Matheus Jampa da Silva / CC BY-SA 4.0"
    },
    {
      "nome": "Pôr do sol no Jacaré",
      "descricao": "Praia em Cabedelo, na foz do Rio Paraíba, conhecida pelo pôr do sol",
      "distancia": "10 km",
      "foto": { "arquivo": "regiao-por-do-sol-jacare.jpg", "alt": "Pôr do sol na Praia do Jacaré, em João Pessoa" },
      "credito": "Marinelson Almeida / CC BY 2.0"
    },
    {
      "nome": "Centro Histórico",
      "descricao": "Conjunto de prédios históricos do Centro/Varadouro de João Pessoa",
      "distancia": "4 km",
      "foto": { "arquivo": "regiao-centro-historico.jpg", "alt": "Vista do Centro Histórico de João Pessoa" },
      "credito": "Rogerio121402 / CC BY-SA 4.0"
    },
    {
      "nome": "Farol do Cabo Branco",
      "descricao": "Farol no ponto mais oriental das Américas, no bairro Cabo Branco",
      "distancia": "3,1 km",
      "foto": { "arquivo": "regiao-farol-cabo-branco.jpg", "alt": "Farol do Cabo Branco, em João Pessoa" }
    },
    {
      "nome": "Estação Cabo Branco",
      "descricao": "Estação Cabo Branco de Ciência, Cultura e Artes, museu projetado por Oscar Niemeyer",
      "distancia": "9 km",
      "foto": { "arquivo": "regiao-estacao-cabo-branco.jpg", "alt": "Estação Cabo Branco de Ciência, Cultura e Artes, em João Pessoa" },
      "credito": "A. Júnior / CC BY 2.0"
    }
  ],
```

Notas sobre os números: "Praia urbana" (Manaíra, 600 m) e "Orla do Bessa" (750 m) vêm
direto da tabela "Praias na vizinhança" do Booking. "Centro Histórico" passa a usar a
distância do "Cultural Center Jose Lins do Rego" (4 km, ponto do Centro Histórico listado
em "Principais atrações"). "Farol do Cabo Branco" usa a distância de "Cabo Branco Beach"
(3,1 km, a praia mais próxima do farol, já que o Booking não lista o farol em si).
"Pôr do sol no Jacaré" e "Estação Cabo Branco" não constam na lista do Booking — mantêm
a distância já calculada anteriormente (10 km e 9 km).

- [ ] **Step 2: Atualizar `PENDENCIAS.md`**

Em `clientes/lumehostel/PENDENCIAS.md`, na nota sobre fonte, atualizar de Fredoka para
Space Grotesk:

Trocar o parágrafo que menciona "Escolhemos a **Fredoka**" por:

```markdown
- [ ] **Fonte do site.** A fonte auxiliar do MIV dele (**Arial Rounded MT Bold**) é
      proprietária da Monotype e não pode ser hospedada num site sem licença web paga.
      A autora comparou visualmente três substitutas livres e escolheu **Space Grotesk**
      — geométrica e angular, no espírito do logotipo (que usa a Ellograph CF, também
      proprietária) — usada no site inteiro (títulos e corpo). Informar isso ao Gabriel e
      registrar que ele **tem a opção de comprar a licença web de qualquer uma das duas
      fontes do MIV** se quiser a original no site.
```

Acrescentar, na seção "Fotos que faltam", que coworking/redário/pátio à noite já foram
resolvidos por fotos reais trazidas pela autora (Tasks 5-6 deste plano) — remover essas
três linhas da lista de pendentes se a Task 6 encontrou foto para o coworking; mantê-las
se não encontrou.

- [ ] **Step 3: Validar a build final**

Run: `cd template && CLIENTE=lumehostel npm run build && CLIENTE=demo npm run build`
Expected: PASS nas duas.

- [ ] **Step 4: Commit**

```bash
git add clientes/lumehostel/config.json clientes/lumehostel/PENDENCIAS.md
git commit -m "Distancias da regiao conforme o Booking; pendencias atualizadas (fonte, fotos)"
```
