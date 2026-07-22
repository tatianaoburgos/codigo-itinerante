# Mar à Vista — POC com Hero em Vídeo — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir a POC do Mar à Vista Hostel definida em
`docs/superpowers/specs/2026-07-21-maravista-poc-pivot-design.md`: hero
full-bleed em vídeo (congela no último frame), nav com a arquitetura futura
do site (só 2 itens reais), e uma única seção nova implementada ("O Hostel").

**Architecture:** Continua sendo o motor real (`template/`), não uma página
avulsa — as seções que a POC não usa (Acomodações, Comodidades, Região,
Depoimentos) simplesmente não aparecem porque o `config.json` não define os
campos correspondentes, mesmo mecanismo já usado para `regiao`/`depoimentos`.
Isso exige tornar `acomodacoes` e `comodidades` opcionais no schema (hoje são
obrigatórios) e separar o texto `sobre.historia` — hoje embutido dentro da
seção de Comodidades — em uma seção própria (`#sobre`) que sempre renderiza,
já que `sobre` continua obrigatório. `Hero.astro` ganha suporte a vídeo
opcional, reaproveitável por clientes futuros.

**Tech Stack:** Astro 5, Tailwind CSS 4, Zod, `astro:assets`, Vite
`import.meta.glob` (novo uso: resolver vídeo via `query: '?url'`, já que
`astro:assets` só otimiza imagem). Processamento de vídeo via `ffmpeg`
(instalado nesta sessão via `winget install --id Gyan.FFmpeg`).

## Global Constraints

- **Nenhuma informação inventada sobre o hostel** — conteúdo já verificado
  ao vivo no Booking.com nesta sessão (nota 8,8 "Fabuloso", 1.177
  avaliações, localização 9,9/10).
- **O vídeo do hero (Instagram Reels) ainda não tem autorização de uso do
  dono do hostel** — é uso interno da autora para avaliar o conceito; não
  publicar/enviar ao dono sem essa autorização (registrar como pendência).
- Preços: nunca no site; política fixa `"consultar"`.
- Idioma: português brasileiro em conteúdo, docs e commits. Sem emojis em
  código.
- Comandos de build rodam dentro de `template/` (PowerShell):
  `$env:CLIENTE = 'maravista'; npm run build`.
- Toda task que mexe em arquivo compartilhado do motor termina com as builds
  de `demo`, `lumehostel` **e** `maravista` passando (a de `maravista` só é
  possível a partir da Task 6, quando o `config.json` existir — até lá,
  validar `demo` + `lumehostel`).
- **Mudança visível no LumeHostel (site já publicado)**: a Task 1 move o
  texto `sobre.historia` de dentro da seção "Comodidades" para uma seção
  própria "O Hostel" logo depois de "Acomodações". Isso é intencional (ver
  spec), mas exige checagem visual do LumeHostel, não só build passando.
- Trabalho no worktree `.worktrees/maravista-poc` (branch `maravista-poc`),
  criado e aprovado no início da sessão. Specs/plans deste pivô vivem no
  `master` (mesmo padrão já usado para o plano anterior); só os commits de
  código/conteúdo vão para a branch do cliente.

---

### Task 1: Motor — seção `#sobre` própria (extraída de dentro de Comodidades)

**Contexto:** Hoje `config.sobre.historia` é renderizado como um parágrafo
dentro da seção `#comodidades` (`template/src/pages/index.astro:44`), sem
título próprio. Como `comodidades` vai virar opcional na Task 2, esse texto
precisa de uma seção independente que sempre renderiza (já que `sobre`
continua obrigatório no schema).

**Files:**
- Modify: `template/src/lib/schema.ts` (objeto `sobre`)
- Modify: `template/src/pages/index.astro:18-44`

**Interfaces:**
- Produces: `configClienteSchema.sobre.foto?: FotoSchema` — foto opcional
  que acompanha o texto na nova seção `#sobre`.

- [x] **Step 1: Adicionar `foto` opcional ao objeto `sobre` do schema**

Em `template/src/lib/schema.ts`, trocar:

```ts
  sobre: z.object({
    historia: z.string().min(1),
  }),
```

por:

```ts
  sobre: z.object({
    historia: z.string().min(1),
    foto: fotoSchema.optional(),
  }),
```

- [x] **Step 2: Criar a seção `#sobre`, remover o texto de dentro de Comodidades**

Em `template/src/pages/index.astro`, o arquivo atual tem (linhas 26-90,
resumido):

```astro
  <section id="acomodacoes" ...>
    ...
  </section>

  <DivisorSimbolo />

  <section id="comodidades" class="scroll-mt-36 sm:scroll-mt-20 bg-sal">
    <div class="mx-auto max-w-5xl px-4 py-14">
      <TituloSecao eyebrow="Comodidades">A vida por aqui</TituloSecao>
      <p class="revela mt-6 max-w-2xl text-lg leading-relaxed">{config.sobre.historia}</p>
      {/* ... resto do grid de comodidades ... */}
```

Trocar por (nova seção `#sobre` entre Acomodações e Comodidades; parágrafo
de `sobre.historia` removido de dentro de Comodidades):

```astro
  <section id="acomodacoes" ...>
    ...
  </section>

  <DivisorSimbolo />

  <section id="sobre" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden">
    <CascataOndas />
    <div class="mx-auto max-w-5xl px-4 py-14">
      <TituloSecao eyebrow="O Hostel">A casa</TituloSecao>
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

  <DivisorSimbolo />

  <section id="comodidades" class="scroll-mt-36 sm:scroll-mt-20 bg-sal">
    <div class="mx-auto max-w-5xl px-4 py-14">
      <TituloSecao eyebrow="Comodidades">A vida por aqui</TituloSecao>
      {/* ... resto do grid de comodidades, sem alteracao ... */}
```

Note que agora existem **dois** `<DivisorSimbolo />` (um antes e um depois de
`#sobre`) onde antes havia um só entre Acomodações e Comodidades.

- [x] **Step 3: Validar as duas builds**

Run: `cd template; $env:CLIENTE = 'lumehostel'; npm run build`
Expected: PASS. Grep `dist/index.html` por `>O Hostel<` (novo eyebrow) e
confirme que o texto da história do LumeHostel (comece com as primeiras
palavras do `historia` em `clientes/lumehostel/config.json`) aparece **fora**
do bloco de comodidades — abra `dist/index.html` e confirme visualmente a
ordem: `id="acomodacoes"` → `id="sobre"` → `id="comodidades"`.

Run: `cd template; $env:CLIENTE = 'demo'; npm run build`
Expected: PASS, mesma checagem.

- [x] **Step 4: Checagem visual do LumeHostel (site já publicado)**

Run: `cd template; $env:CLIENTE = 'lumehostel'; npm run dev`
Abrir no navegador, rolar até a nova seção "O Hostel" entre Acomodações e
Comodidades. Confirmar que o título "A casa" + texto ficam legíveis e bem
espaçados (o `CascataOndas` não deve conflitar visualmente com o degradê já
usado em Acomodações logo acima). Isso é uma mudança real no site publicado
— se o resultado não ficar bom, reportar como concern em vez de seguir.

- [x] **Step 5: Commit**

```bash
git add template/src/lib/schema.ts template/src/pages/index.astro
git commit -m "Motor: secao O Hostel separada de Comodidades (sobre.foto opcional)"
```

---

### Task 2: Motor — `acomodacoes`, `comodidades` e a seção de Localização viram opcionais

**Contexto:** Hoje `acomodacoes`/`comodidades` são obrigatórios (`.min(1)`,
sem `.optional()`) e usados sem guarda em `index.astro`. A seção visual de
Localização (`#localizacao`) também renderiza sem guarda nenhuma hoje — mas
os campos `endereco`/`logradouro`/`cidade`/`uf` (usados só no JSON-LD do
`Layout.astro`) continuam obrigatórios mesmo sem a seção visual, porque são
dados reais e simples (o endereço do hostel) que não têm o mesmo risco de
"conteúdo forçado" que `acomodacoes`/`comodidades` têm — por isso só
`mapsEmbedUrl` e `comoChegar` (os dois campos usados exclusivamente pela
seção visual, nunca pelo JSON-LD) viram opcionais, e é a presença de
`mapsEmbedUrl` que decide se a seção aparece. Sem essa mudança a build do
Mar à Vista (que não vai ter nenhum desses três campos na POC) quebra na
validação do Zod. O padrão a seguir é o mesmo já usado para
`regiao`/`depoimentos`/`destaques`.

**Files:**
- Modify: `template/src/lib/schema.ts` (`acomodacoes`, `comodidades`,
  `localizacao.mapsEmbedUrl`, `localizacao.comoChegar`)
- Modify: `template/src/pages/index.astro` (derivação + três seções)
- Modify: `template/src/components/Nav.astro` (filtro dos itens de nav)

**Interfaces:**
- Produces: `configClienteSchema.acomodacoes?: Acomodacao[]`,
  `configClienteSchema.comodidades?: Comodidade[]`,
  `configClienteSchema.localizacao.mapsEmbedUrl?: string`,
  `configClienteSchema.localizacao.comoChegar?: string[]` — todos opcionais
  agora.

- [x] **Step 1: Tornar os dois campos opcionais no schema**

Em `template/src/lib/schema.ts`, trocar:

```ts
  acomodacoes: z.array(acomodacaoSchema).min(1),
```

por:

```ts
  acomodacoes: z.array(acomodacaoSchema).min(1).optional(),
```

E trocar:

```ts
  comodidades: z.array(comodidadeSchema).min(1),
```

por:

```ts
  comodidades: z.array(comodidadeSchema).min(1).optional(),
```

E, dentro do objeto `localizacao`, trocar:

```ts
    mapsEmbedUrl: z.url(),
    comoChegar: z.array(z.string().min(1)),
```

por:

```ts
    mapsEmbedUrl: z.url().optional(),
    comoChegar: z.array(z.string().min(1)).optional(),
```

- [x] **Step 2: Guardar a derivação e as duas seções em `index.astro`**

Trocar a linha (hoje no topo do frontmatter, depois da Task 1 ainda como
estava):

```ts
const comodidadesComFoto = config.comodidades.filter((c) => c.foto);
const comodidadesSemFoto = config.comodidades.filter((c) => !c.foto);
```

por:

```ts
const comodidadesComFoto = config.comodidades?.filter((c) => c.foto) ?? [];
const comodidadesSemFoto = config.comodidades?.filter((c) => !c.foto) ?? [];
```

Envolver a seção `#acomodacoes` (incluindo o `<DivisorSimbolo />` que já vem
logo depois dela) em uma condicional:

```astro
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
```

E envolver o par `<DivisorSimbolo />` + `#comodidades` (o que vem **antes**
da seção, não depois — ver Task 1) em outra condicional:

```astro
  {
    config.comodidades && (
      <>
        <DivisorSimbolo />

        <section id="comodidades" class="scroll-mt-36 sm:scroll-mt-20 bg-sal">
          <div class="mx-auto max-w-5xl px-4 py-14">
            <TituloSecao eyebrow="Comodidades">A vida por aqui</TituloSecao>
            {/* ... grid de comodidadesComFoto/comodidadesSemFoto, sem alteracao ... */}
          </div>
        </section>
      </>
    )
  }
```

A seção `#sobre` (Task 1) fica **fora** dessas duas condicionais — sempre
renderiza entre elas.

- [x] **Step 3: Guardar a seção `#localizacao` em `index.astro`**

O arquivo hoje tem (o bloco `resumo` já existe, da Task 1 do plano
anterior):

```astro
  <section id="localizacao" class="relative isolate scroll-mt-36 sm:scroll-mt-20 overflow-hidden">
    <CascataOndas />
    <div class="mx-auto max-w-5xl px-4 py-14">
    <TituloSecao eyebrow="Localização">Onde estamos</TituloSecao>
    <p class="mt-4 text-lg">{config.localizacao.endereco}</p>
    <div class="revela mt-8">
      <Mapa />
    </div>
    {
      config.localizacao.comoChegar.length > 0 && (
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
```

Trocar por (seção inteira envolvida em `{config.localizacao.mapsEmbedUrl &&
(...)}`; a checagem de `comoChegar` ganha um `?.` porque o campo agora é
opcional):

```astro
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
```

- [x] **Step 4: Atualizar os filtros de `Nav.astro`**

Em `template/src/components/Nav.astro`, trocar:

```ts
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

por:

```ts
const abas = [
  { href: '/#acomodacoes', rotulo: 'Acomodações' },
  { href: '/#comodidades', rotulo: 'Comodidades' },
  { href: '/#vibe', rotulo: 'A vibe' },
  { href: '/#regiao', rotulo: 'A região' },
  { href: '/#localizacao', rotulo: 'Localização' },
]
  .filter((aba) => aba.href !== '/#acomodacoes' || config.acomodacoes)
  .filter((aba) => aba.href !== '/#comodidades' || config.comodidades)
  .filter((aba) => aba.href !== '/#vibe' || config.vibe)
  .filter((aba) => aba.href !== '/#regiao' || config.regiao)
  .filter((aba) => aba.href !== '/#localizacao' || config.localizacao.mapsEmbedUrl);
```

(A Task 3 mexe de novo nesse array para adicionar "O Hostel" e os itens
futuros inertes — não precisa reler este arquivo inteiro agora, só aplicar
o diff acima.)

- [x] **Step 5: Validar as duas builds (regressão)**

Run: `cd template; $env:CLIENTE = 'lumehostel'; npm run build`
Expected: PASS, output idêntico ao anterior (LumeHostel define
`mapsEmbedUrl`/`comoChegar`/`acomodacoes`/`comodidades`, então nada muda
visualmente aqui — só no LumeHostel a Task 1 muda algo, esta task não).

Run: `cd template; $env:CLIENTE = 'demo'; npm run build`
Expected: PASS, mesma checagem — `demo` também define os três campos.

O caminho "campo ausente" só é exercitado de verdade na Task 6, quando o
`config.json` do `maravista` existir sem `acomodacoes`, `comodidades`,
`mapsEmbedUrl` nem `comoChegar`.

- [x] **Step 6: Commit**

```bash
git add template/src/lib/schema.ts template/src/pages/index.astro template/src/components/Nav.astro
git commit -m "Motor: acomodacoes, comodidades e secao de localizacao viram opcionais"
```

---

### Task 3: Motor — Nav com "O Hostel" real + itens futuros inertes

**Contexto:** A POC precisa mostrar a arquitetura do site completo no menu
sem fingir navegação para seções que não existem ainda. "O Hostel" (Task 1)
sempre existe, então vira item real e incondicional. As demais seções que a
POC não implementa aparecem como rótulo sem link, via um novo campo opcional
`navFuturo` — não muda o comportamento de nenhum cliente existente (LumeHostel
e demo não vão definir esse campo).

**Files:**
- Modify: `template/src/lib/schema.ts` (novo campo `navFuturo`)
- Modify: `template/src/components/Nav.astro`

**Interfaces:**
- Produces: `configClienteSchema.navFuturo?: string[]` — rótulos exibidos no
  nav como texto inerte (sem link), depois dos itens reais.

- [x] **Step 1: Adicionar `navFuturo` ao schema**

Em `template/src/lib/schema.ts`, dentro de `configClienteSchema`, logo depois
do campo `destaques` (antes do `});` de fechamento):

```ts
  destaques: z.array(destaqueSchema).max(2).optional(),
  /** Rótulos de seções futuras exibidos no nav sem link (roadmap do site). */
  navFuturo: z.array(z.string().min(1)).optional(),
```

- [x] **Step 2: "O Hostel" vira item incondicional do nav**

Em `template/src/components/Nav.astro`, adicionar `{ href: '/#sobre', rotulo:
'O Hostel' }` como primeiro item do array `abas` (resultado do diff da
Task 2, Step 4):

```ts
const abas = [
  { href: '/#sobre', rotulo: 'O Hostel' },
  { href: '/#acomodacoes', rotulo: 'Acomodações' },
  { href: '/#comodidades', rotulo: 'Comodidades' },
  { href: '/#vibe', rotulo: 'A vibe' },
  { href: '/#regiao', rotulo: 'A região' },
  { href: '/#localizacao', rotulo: 'Localização' },
]
  .filter((aba) => aba.href !== '/#acomodacoes' || config.acomodacoes)
  .filter((aba) => aba.href !== '/#comodidades' || config.comodidades)
  .filter((aba) => aba.href !== '/#vibe' || config.vibe)
  .filter((aba) => aba.href !== '/#regiao' || config.regiao)
  .filter((aba) => aba.href !== '/#localizacao' || config.localizacao.mapsEmbedUrl);
```

- [x] **Step 3: Renderizar os itens inertes de `navFuturo`**

No mesmo arquivo, trocar o bloco que mapeia `abas`:

```astro
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
```

por (adiciona o `.map` de `config.navFuturo` logo depois do de `abas`, antes
do botão do WhatsApp):

```astro
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
      {
        config.navFuturo?.map((rotulo) => (
          <span class="pb-0.5 text-sm font-bold opacity-40" title="Em breve" aria-hidden="true">
            {rotulo}
          </span>
        ))
      }
      <BotaoWhatsApp />
    </div>
```

- [x] **Step 4: Validar as duas builds**

Run: `cd template; $env:CLIENTE = 'lumehostel'; npm run build`
Expected: PASS. `dist/index.html` contém um link novo `href="/#sobre"` com
texto "O Hostel" antes de "Acomodações" no nav. Nenhum `<span>` de
`navFuturo` aparece (LumeHostel não define esse campo).

Run: `cd template; $env:CLIENTE = 'demo'; npm run build`
Expected: PASS, mesma checagem.

- [x] **Step 5: Commit**

```bash
git add template/src/lib/schema.ts template/src/components/Nav.astro
git commit -m "Motor: nav ganha O Hostel real e suporte a itens futuros inertes"
```

---

### Task 4: Motor — `Hero.astro` ganha suporte a vídeo opcional

**Contexto:** Hoje o hero só aceita foto estática (`foto('capa.jpg')` via
`astro:assets`). Esta task adiciona um caminho opcional de vídeo — usado
pelo Mar à Vista, disponível para qualquer cliente futuro. Comportamento:
autoplay mudo, toca uma vez (sem `loop` — trava no último frame por
comportamento nativo do `<video>`), poster como imagem de carregamento e
fallback, e o vídeo só é ativado via JS quando `prefers-reduced-motion` não
estiver setado — caso contrário fica só o poster (mesma foto estática de
hoje, visualmente).

**Files:**
- Modify: `template/src/lib/fotos.ts` (novo helper `video`)
- Modify: `template/src/lib/schema.ts` (`marca.heroVideo`, `marca.heroVideoPoster`)
- Modify: `template/src/components/Hero.astro`

**Interfaces:**
- Produces: `video(arquivo: string): string` — resolve um `.mp4`/`.webm` de
  `clientes/<cliente>/fotos/` para a URL que o Vite gera (não passa por
  `astro:assets`, que só otimiza imagem).
- Produces: `configClienteSchema.marca.heroVideo?: string`,
  `configClienteSchema.marca.heroVideoPoster?: string`.

- [x] **Step 1: Helper `video()` em `fotos.ts`**

Em `template/src/lib/fotos.ts`, adicionar depois do bloco de `modulosMarca`/
`marcaDoCliente`/`marca()` (antes de `simboloMarca`):

```ts
const modulosVideo = import.meta.glob<string>('../../../clientes/*/fotos/*.{mp4,webm}', {
  eager: true,
  query: '?url',
  import: 'default',
});

const videosDoCliente = new Map<string, string>(
  Object.entries(modulosVideo)
    .filter(([caminho]) => caminho.includes(`/clientes/${clienteAtivo}/fotos/`))
    .map(([caminho, url]) => [caminho.split('/').pop()!, url]),
);

/** Resolve um arquivo de vídeo do cliente ativo (hero em vídeo). Não passa
 * por `astro:assets` — vídeo não é otimizado como imagem, só copiado. */
export function video(arquivo: string): string {
  const url = videosDoCliente.get(arquivo);
  if (!url) {
    throw new Error(`Video "${arquivo}" nao encontrado em clientes/${clienteAtivo}/fotos/`);
  }
  return url;
}
```

- [x] **Step 2: Campos novos no schema**

Em `template/src/lib/schema.ts`, dentro de `marcaSchema`, depois de
`faviconPng`:

```ts
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
});
```

- [x] **Step 3: `Hero.astro` — vídeo condicional**

Substituir o conteúdo de `template/src/components/Hero.astro` por:

```astro
---
import { Image } from 'astro:assets';
import { config } from '../lib/cliente';
import { foto, marca, video } from '../lib/fotos';
import BotaoWhatsApp from './BotaoWhatsApp.astro';
import MarcaDagua from './MarcaDagua.astro';

const logo = config.marca?.logo ? marca(config.marca.logo) : undefined;
const heroVideo = config.marca?.heroVideo ? video(config.marca.heroVideo) : undefined;
const heroVideoPoster = config.marca?.heroVideoPoster
  ? foto(config.marca.heroVideoPoster)
  : undefined;
---

<section id="hero" class="relative isolate flex min-h-svh items-end overflow-hidden bg-noite">
  <MarcaDagua />
  {
    heroVideo ? (
      <>
        {heroVideoPoster && (
          <Image
            src={heroVideoPoster}
            alt=""
            widths={[640, 1024, 1600]}
            sizes="100vw"
            loading="eager"
            class="absolute inset-0 -z-10 h-full w-full object-cover object-[50%_42%]"
          />
        )}
        <video
          class="hero-video absolute inset-0 -z-10 hidden h-full w-full object-cover object-[50%_42%]"
          data-src={heroVideo}
          muted
          playsinline
        />
      </>
    ) : (
      <Image
        src={foto('capa.jpg')}
        alt=""
        widths={[640, 1024, 1600]}
        sizes="100vw"
        loading="eager"
        class="absolute inset-0 -z-10 h-full w-full object-cover"
      />
    )
  }
  <div
    class="absolute inset-0 -z-10 bg-gradient-to-t from-noite/90 via-noite/50 to-noite/20"
    aria-hidden="true"
  >
  </div>
  <div class="mx-auto w-full max-w-5xl px-4 pt-32 pb-14">
    <h1 class="max-w-2xl">
      {/* SVG vetorial: `<img>` cru é intencional — astro:assets otimiza raster, não SVG. */}
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

{
  heroVideo && (
    <script>
      const video = document.querySelector<HTMLVideoElement>('.hero-video');
      if (video && window.matchMedia('(prefers-reduced-motion: no-preference)').matches) {
        video.src = video.dataset.src!;
        video.classList.remove('hidden');
        video.play().catch(() => {});
      }
    </script>
  )
}
```

Notas sobre o comportamento:
- Sem `loop` e sem `autoplay` no HTML: o script só atribui `src` e chama
  `.play()` depois de checar `prefers-reduced-motion`, evitando baixar o
  vídeo à toa para quem prefere sem movimento.
- Sem `loop`, ao terminar o `<video>` mantém o último frame renderizado —
  comportamento nativo do elemento, não precisa de código extra para
  "congelar".
- `object-[50%_42%]` (Tailwind arbitrary value) é o enquadramento validado
  no mockup `mockups/maravista-hero-video.html` — mantém o casarão em quadro.

- [x] **Step 4: Validar as duas builds (regressão)**

Run: `cd template; $env:CLIENTE = 'lumehostel'; npm run build`
Expected: PASS, `dist/index.html` continua com `<img>`/`<picture>` da
`capa.jpg` no hero (LumeHostel não define `marca.heroVideo`), nenhum
`<video>` no output.

Run: `cd template; $env:CLIENTE = 'demo'; npm run build`
Expected: PASS, mesma checagem.

Run: `cd template; npx astro check`
Expected: PASS, sem erros de tipo (confirma que `video()` e os campos novos
do schema estão bem tipados).

- [x] **Step 5: Commit**

```bash
git add template/src/lib/fotos.ts template/src/lib/schema.ts template/src/components/Hero.astro
git commit -m "Motor: Hero.astro ganha suporte opcional a video full-bleed"
```

---

### Task 5: Conteúdo — processar vídeo do hero e foto da seção "O Hostel"

**Contexto:** Task de mídia, não de código. Gera os arquivos finais que a
Task 6 vai referenciar no `config.json`. `ffmpeg` já foi instalado nesta
sessão (`winget install --id Gyan.FFmpeg`) — se rodar em uma sessão nova,
reinstalar ou localizar o binário via
`Get-ChildItem -Recurse -Filter ffmpeg.exe "$env:LOCALAPPDATA\Microsoft\WinGet\Packages"`.

**Files:**
- Create: `clientes/maravista/fotos/hero.mp4`
- Create: `clientes/maravista/fotos/hero-poster.jpg`
- Create: `clientes/maravista/fotos/sobre-lounge.jpg`
- Create: `clientes/maravista/fotos/FONTES.md`

**Interfaces:**
- Consumes: `clientes/maravista/fotos/hero-video-original.mp4` (já no
  repositório, fornecido pela autora).

- [x] **Step 1: Vídeo do hero — mudo, comprimido, sem cortar**

```bash
FFMPEG="/c/Users/tatia/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.2-full_build/bin/ffmpeg.exe"
SRC="clientes/maravista/fotos/hero-video-original.mp4"
"$FFMPEG" -y -i "$SRC" -an -vf "scale=720:-2" -c:v libx264 -crf 26 -preset slow -movflags +faststart clientes/maravista/fotos/hero.mp4
```

Expected: cria `clientes/maravista/fotos/hero.mp4` (~13 MB, 23,5s, sem
áudio). Se o caminho do `ffmpeg.exe` tiver mudado (reinstalação), ajustar a
variável `FFMPEG` antes de rodar.

- [x] **Step 2: Poster — último frame do vídeo**

```bash
"$FFMPEG" -y -ss 23.3 -i "$SRC" -frames:v 1 -q:v 2 clientes/maravista/fotos/hero-poster.jpg
```

Expected: cria `clientes/maravista/fotos/hero-poster.jpg`, mostrando o
casarão azul-claro (mesmo frame usado no mockup validado com a autora).
Abrir o arquivo e conferir visualmente.

- [x] **Step 3: Foto da seção "O Hostel"**

A foto do lounge com colunas de pedra já foi baixada da galeria pública do
Booking.com durante o brainstorm e está em
`mockups/img/maravista-hero/opcao-a-lounge-pedra.jpg` (1024×576, já dentro
do limite de 1600px do projeto). Copiar para o lugar definitivo:

```bash
cp mockups/img/maravista-hero/opcao-a-lounge-pedra.jpg clientes/maravista/fotos/sobre-lounge.jpg
```

- [x] **Step 4: Registrar proveniência**

Create `clientes/maravista/fotos/FONTES.md`:

```markdown
# Fontes das fotos e vídeo — Mar à Vista (POC)

## `sobre-lounge.jpg`

Galeria pública do Booking.com (perfil do Mar à Vista Hostel), foto do
lounge/área comum com colunas de pedra expostas e janelas abertas para a
praia. Foto publicada pelo próprio estabelecimento — não é foto de hóspede.

## `hero.mp4` / `hero-poster.jpg`

Recorte (mudo, recomprimido) de um vídeo de drone publicado no Instagram do
Mar à Vista Hostel (reels `DWBbxn7DtNW`), fornecido pela autora a partir de
cópia própria salva do Reels público. **Uso só para esta POC — ainda sem
autorização de uso do dono do hostel.** Pendência: pedir autorização (e,
idealmente, o arquivo original em resolução maior) quando o contato com o
dono acontecer.
```

- [x] **Step 5: Commit**

```bash
git add clientes/maravista/fotos/hero.mp4 clientes/maravista/fotos/hero-poster.jpg clientes/maravista/fotos/sobre-lounge.jpg clientes/maravista/fotos/FONTES.md
git commit -m "Conteudo Mar a Vista: video do hero processado e foto da secao O Hostel"
```

---

### Task 6: Conteúdo — `clientes/maravista/config.json` (POC enxuta)

**Files:**
- Create: `clientes/maravista/config.json`

**Interfaces:**
- Consumes: schema das Tasks 1, 2, 3, 4; assets das Tasks 4 (marca, já
  commitados antes deste pivô) e 5 (vídeo/foto).

- [x] **Step 1: Escrever o `config.json`**

```json
{
  "nome": "Mar à Vista Hostel",
  "marca": {
    "logo": "logo.png",
    "faviconPng": "favicon-32.png",
    "appleTouchIcon": "apple-touch-icon.png",
    "simbolo": "icone.png",
    "heroVideo": "hero.mp4",
    "heroVideoPoster": "hero-poster.jpg"
  },
  "slogan": "Mar à vista em todos os quartos",
  "descricaoSeo": "Mar à Vista Hostel, na Barra (Salvador): todos os quartos com vista pro mar, a 300 m do Farol da Barra. Reserve direto pelo WhatsApp.",
  "sobre": {
    "historia": "O Mar à Vista fica na Barra, de frente para o mar, a poucos passos do Farol. É um hostel de dormitórios compartilhados — todos com vista para o mar — com cozinha e recepção 24 horas. Hóspedes descrevem a localização como perfeita e a vista como inigualável; a nota no Booking é 8,8 (\"Fabuloso\"), com 1.177 avaliações, e 9,9/10 para localização.",
    "foto": { "arquivo": "sobre-lounge.jpg", "alt": "Lounge do Mar à Vista Hostel, com colunas de pedra e janelas abertas para a praia" }
  },
  "precos": {
    "politica": "consultar"
  },
  "localizacao": {
    "endereco": "Av. Oceânica, 171 — Barra, Salvador/BA",
    "logradouro": "Av. Oceânica, 171",
    "bairro": "Barra",
    "cidade": "Salvador",
    "uf": "BA"
  },
  "contato": {
    "whatsapp": "5571999838184",
    "email": "contato@maravistahostel.example.com",
    "instagram": "maravistahostel"
  },
  "navFuturo": ["Acomodações", "Comodidades", "A região", "Localização"]
}
```

Note o que **não está** aqui, intencionalmente: `acomodacoes`, `comodidades`
e, dentro de `localizacao`, `mapsEmbedUrl`/`comoChegar` — todos opcionais
desde a Task 2. `endereco`/`logradouro`/`bairro`/`cidade`/`uf` continuam
presentes porque são obrigatórios (usados no JSON-LD do `Layout.astro`,
independente de a seção visual `#localizacao` aparecer ou não) e são dados
reais e simples, sem risco de "conteúdo forçado". Sem `mapsEmbedUrl`, a Task
2 garante que nem a seção `#localizacao` nem o item "Localização" do nav
aparecem — é por isso que "Localização" está em `navFuturo` (o único jeito
dela aparecer é como rótulo inerte).

- [x] **Step 2: Validar a build**

Run: `cd template; $env:CLIENTE = 'maravista'; npm run build`
Expected: PASS. Se falhar por causa de algum campo obrigatório ausente,
conferir contra `template/src/lib/schema.ts` e completar o campo que
faltou — não pular validação do schema.

Run: `cd template; $env:CLIENTE = 'maravista'; npm run dev`
Conferir no navegador:
- Hero em vídeo tocando, casarão em quadro, para no último frame ao terminar
  (esperar os ~23s).
- Nav com 6 itens: só "O Hostel" é link real (âncora funcional); os outros
  5 ("Acomodações", "Comodidades", "A região", "Localização" — vindos de
  `navFuturo` — e note que "A vibe" nem aparece, porque `config.vibe` está
  ausente e o array `abas` já filtra isso) aparecem como texto sem link,
  com opacidade reduzida. Confirmar que "Localização" aparece **uma única
  vez** (só via `navFuturo` — o item fixo do array `abas` não deve aparecer,
  já que `config.localizacao.mapsEmbedUrl` está ausente).
- Seção "O Hostel" com foto + texto.
- Nenhuma outra seção (`#acomodacoes`, `#comodidades`, `#localizacao`)
  aparece.
- Botão WhatsApp abre `wa.me/5571999838184`.

- [x] **Step 3: Commit**

```bash
git add clientes/maravista/config.json
git commit -m "Conteudo Mar a Vista: config.json da POC (hero video + secao O Hostel)"
```

---

### Task 7: Verificação final

**Files:**
- Modify: `CLAUDE.md` (seção "Estado atual")

- [x] **Step 1: Build dos três clientes lado a lado**

Run: `cd template; $env:CLIENTE = 'maravista'; npm run build` — PASS.
Run: `cd template; $env:CLIENTE = 'lumehostel'; npm run build` — PASS.
Run: `cd template; $env:CLIENTE = 'demo'; npm run build` — PASS.
Run: `cd template; npx astro check` — PASS, sem erros de tipo.

- [x] **Step 2: Checklist contra os critérios de conclusão da spec**

Abrir `docs/superpowers/specs/2026-07-21-maravista-poc-pivot-design.md`,
seção "Critérios de conclusão", e confirmar cada item com
`$env:CLIENTE = 'maravista'; npm run dev`: hero em vídeo (autoplay mudo,
congela no fim, respeita `prefers-reduced-motion` — testar via DevTools
"Emulate CSS prefers-reduced-motion: reduce"), nav com 2 itens reais + 4
inertes, seção "O Hostel" com foto+texto, nenhuma outra seção do one-page.

- [x] **Step 3: Atualizar `CLAUDE.md`**

Na seção "Estado atual", registrar: pivô de escopo do Mar à Vista para POC
(hero em vídeo + seção "O Hostel" + nav com arquitetura futura), motivo
(evitar a impressão de "vender site grande demais" antes do contato com o
dono), link para a spec (`docs/superpowers/specs/2026-07-21-maravista-poc-pivot-design.md`)
e este plano; nota de que o plano de site completo
(`docs/superpowers/plans/2026-07-20-maravista-poc.md`) fica preservado e
pausado, não descartado; lembrete de que o vídeo do hero não tem autorização
de uso do dono ainda.

- [x] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: registra a POC do Mar a Vista (hero em video) e o pivo de escopo"
```
