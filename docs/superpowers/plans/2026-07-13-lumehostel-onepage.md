# LumeHostel One-Page — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformar o motor `template/` em gerador de one-page com âncoras (substituindo as 4 páginas), com o LumeHostel como primeiro cliente: fotos dominantes, comodidades ilustradas, seção da região, depoimentos, símbolo da marca presente e fonte única Fredoka.

**Architecture:** O `index.astro` passa a compor todas as seções (hero tela cheia → acomodações em carrossel → comodidades ilustradas → região → depoimentos → localização → CTA); as rotas `/acomodacoes`, `/sobre`, `/localizacao` são removidas e o menu vira âncoras. Schema Zod ganha campos novos (opcionais onde o `demo` não os tem). Conteúdo novo do LumeHostel entra no `config.json` a partir SOMENTE das presenças públicas do hostel (Booking/Google/Instagram).

**Tech Stack:** Astro 5, Tailwind CSS 4, Zod, `astro:assets`, `@fontsource-variable/fredoka`. Sem testes/linter no projeto — a validação de cada task é a build (`npm run build`) dos DOIS clientes (`lumehostel` e `demo`) + conferência visual no dev server.

## Global Constraints

- **Nenhuma informação inventada sobre o hostel**: só conteúdo presente no Booking, Google (Maps/avaliações) ou Instagram do LumeHostel.
- Preços: nunca no site; política "consultar no WhatsApp".
- Idioma: português brasileiro em código de conteúdo, docs e commits. Sem emojis em código.
- Não copiar texto/imagem de sites de referência (nomadssalvador.com, pousadacasadasflores.com.br) — só estrutura.
- Comandos de build rodam dentro de `template/` com env `CLIENTE` (usar Bash tool: `cd template && CLIENTE=lumehostel npm run build`).
- Toda task termina com as builds de `lumehostel` E `demo` passando.

---

### Task 1: Schema — novos campos de dados

**Files:**
- Modify: `template/src/lib/schema.ts`
- Modify: `clientes/demo/config.json` (migração `atividades` → `comodidades`)
- Modify: `clientes/lumehostel/config.json` (idem, mínimo para a build passar)

**Interfaces:**
- Produces: `configClienteSchema` com: `comodidades: {nome, descricao?, foto?}[]` (substitui `atividades`); `regiao?: {nome, descricao, distancia, foto, credito?}[]`; `depoimentos?: {texto, nome, fonte}[]`; `marca.simbolo?: string`. Tipos exportados `Comodidade`, `PontoRegiao`, `Depoimento`.

- [ ] **Step 1: Editar o schema**

Em `template/src/lib/schema.ts`, substituir a linha `atividades: z.array(z.string().min(1)),` e adicionar os schemas novos:

```ts
/** Comodidade do hostel, opcionalmente ilustrada com foto. */
export const comodidadeSchema = z.object({
  nome: z.string().min(1),
  descricao: z.string().min(1).optional(),
  foto: fotoSchema.optional(),
});

/** Ponto de interesse da região, com distância a partir do hostel. */
export const pontoRegiaoSchema = z.object({
  nome: z.string().min(1),
  descricao: z.string().min(1),
  distancia: z.string().min(1),
  foto: fotoSchema,
  credito: z.string().min(1).optional(),
});

/** Depoimento público real (Booking/Google), validável pelo cliente. */
export const depoimentoSchema = z.object({
  texto: z.string().min(1),
  nome: z.string().min(1),
  fonte: z.string().min(1),
});
```

No `marcaSchema`, adicionar `simbolo: z.string().min(1).optional(),`.

No `configClienteSchema`: trocar `atividades: ...` por
`comodidades: z.array(comodidadeSchema).min(1),` e adicionar
`regiao: z.array(pontoRegiaoSchema).optional(),` e
`depoimentos: z.array(depoimentoSchema).optional(),`.

Nos exports de tipos, adicionar:

```ts
export type Comodidade = z.infer<typeof comodidadeSchema>;
export type PontoRegiao = z.infer<typeof pontoRegiaoSchema>;
export type Depoimento = z.infer<typeof depoimentoSchema>;
```

- [ ] **Step 2: Migrar os dois config.json**

Em `clientes/demo/config.json` e `clientes/lumehostel/config.json`, renomear a chave `"atividades"` para `"comodidades"` e converter cada string em objeto. Exemplo (lumehostel):

```json
"comodidades": [
  { "nome": "Coworking ergonômico" },
  { "nome": "Cozinha compartilhada com café de cortesia" },
  { "nome": "Jardim com redes" },
  { "nome": "Churrasqueira" },
  { "nome": "Sala de jogos" },
  { "nome": "Depósito de bagagem" }
]
```

No lumehostel, adicionar em `"marca"`: `"simbolo": "simbolo-ambar.svg"`.

- [ ] **Step 3: Ajustar o consumidor atual**

`template/src/pages/index.astro` referencia `config.atividades` (linha ~57). Trocar por `config.comodidades` e renderizar `comodidade.nome` (ajuste mínimo — a seção será reescrita na Task 3).

- [ ] **Step 4: Validar builds**

Run: `cd template && CLIENTE=lumehostel npm run build && CLIENTE=demo npm run build`
Expected: ambas passam (schema valida os dois configs).

- [ ] **Step 5: Commit**

```bash
git add template/src clientes
git commit -m "Schema: comodidades ilustradas, regiao, depoimentos e simbolo de marca"
```

---

### Task 2: Componentes novos — divisor de símbolo, marca-d'água e carrossel

**Files:**
- Create: `template/src/components/DivisorSimbolo.astro`
- Create: `template/src/components/MarcaDagua.astro`
- Create: `template/src/components/CarrosselAcomodacoes.astro`

**Interfaces:**
- Consumes: `config.marca?.simbolo`, `marca()` de `lib/fotos.ts`, `foto()` de `lib/fotos.ts`, tipo `Acomodacao`.
- Produces: `<DivisorSimbolo />` (sem props); `<MarcaDagua />` (sem props; absoluto, pai precisa de `relative`); `<CarrosselAcomodacoes />` (sem props, lê `config.acomodacoes`).

- [ ] **Step 1: DivisorSimbolo.astro**

Símbolo pequeno centralizado entre seções; sem símbolo configurado, vira traço discreto:

```astro
---
import { config } from '../lib/cliente';
import { marca } from '../lib/fotos';

const simbolo = config.marca?.simbolo ? marca(config.marca.simbolo) : undefined;
---

<div class="flex justify-center py-2" aria-hidden="true">
  {
    simbolo ? (
      <img src={simbolo.src} alt="" class="h-8 w-auto opacity-70" />
    ) : (
      <span class="h-0.5 w-10 bg-fitinha" />
    )
  }
</div>
```

- [ ] **Step 2: MarcaDagua.astro**

Símbolo grande e translúcido ao fundo (hero e CTA final); sem símbolo, não renderiza nada:

```astro
---
import { config } from '../lib/cliente';
import { marca } from '../lib/fotos';

const simbolo = config.marca?.simbolo ? marca(config.marca.simbolo) : undefined;
---

{
  simbolo && (
    <img
      src={simbolo.src}
      alt=""
      aria-hidden="true"
      class="pointer-events-none absolute -right-16 -bottom-16 -z-10 h-[60%] w-auto opacity-10 select-none"
    />
  )
}
```

- [ ] **Step 3: CarrosselAcomodacoes.astro**

Carrossel horizontal com scroll-snap, foto cheia e nome sobreposto:

```astro
---
import { Image } from 'astro:assets';
import { config } from '../lib/cliente';
import { foto } from '../lib/fotos';
---

<div class="-mx-4 flex snap-x snap-mandatory gap-4 overflow-x-auto px-4 pb-4">
  {
    config.acomodacoes.map((acomodacao) => (
      <article class="relative w-[85vw] max-w-md shrink-0 snap-center overflow-hidden rounded-xl">
        <Image
          src={foto(acomodacao.fotos[0].arquivo)}
          alt={acomodacao.fotos[0].alt}
          widths={[480, 900]}
          sizes="(min-width: 640px) 448px, 85vw"
          class="aspect-3/4 w-full object-cover"
        />
        <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-noite/85 to-transparent p-5 pt-16">
          <h3 class="font-display text-2xl font-bold text-white">{acomodacao.nome}</h3>
          <p class="mt-1 text-sm text-sal">{acomodacao.capacidade}</p>
          <p class="mt-2 text-xs text-sal/90">{acomodacao.comodidades.join(' · ')}</p>
        </div>
      </article>
    ))
  }
</div>
```

- [ ] **Step 4: Validar builds** (componentes ainda não usados; garante que compilam via checagem do Astro)

Run: `cd template && CLIENTE=lumehostel npm run build && CLIENTE=demo npm run build`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add template/src/components
git commit -m "Componentes: divisor de simbolo, marca-d'agua e carrossel de acomodacoes"
```

---

### Task 3: One-page — index.astro composto, páginas antigas removidas, Nav com âncoras

**Files:**
- Modify: `template/src/pages/index.astro` (reescrita completa)
- Modify: `template/src/components/Nav.astro`
- Modify: `template/src/components/Hero.astro`
- Delete: `template/src/pages/acomodacoes.astro`, `template/src/pages/sobre.astro`, `template/src/pages/localizacao.astro`

**Interfaces:**
- Consumes: `DivisorSimbolo`, `MarcaDagua`, `CarrosselAcomodacoes` (Task 2); `Mapa`, `TituloSecao`, `BotaoWhatsApp`, `Layout` existentes; `config.comodidades/regiao/depoimentos` (Task 1).
- Produces: âncoras `#acomodacoes`, `#comodidades`, `#regiao`, `#depoimentos`, `#localizacao` na página única.

- [ ] **Step 1: Hero em tela cheia com marca-d'água**

Em `Hero.astro`: trocar `min-h-[70vh]` por `min-h-svh`, adicionar `overflow-hidden` na section e `<MarcaDagua />` como primeiro filho (importar de `./MarcaDagua.astro`). Se houver logo (`config.marca?.logo`), exibi-lo acima do `<h1>`:

```astro
{logo && <img src={logo.src} alt="" class="h-16 w-auto" />}
```

(com `const logo = config.marca?.logo ? marca(config.marca.logo) : undefined;` no frontmatter, importando `marca` de `../lib/fotos`).

- [ ] **Step 2: Nav com âncoras**

Em `Nav.astro`, substituir `abas` e remover a lógica de `caminhoAtual`/`aria-current`:

```ts
const abas = [
  { href: '/#acomodacoes', rotulo: 'Acomodações' },
  { href: '/#comodidades', rotulo: 'Comodidades' },
  { href: '/#regiao', rotulo: 'A região' },
  { href: '/#localizacao', rotulo: 'Localização' },
];
```

Classe dos links perde `border-b-2 pb-0.5` condicional (usar `border-transparent` fixo). Adicionar `scroll-behavior: smooth` via classe `scroll-smooth` no `<html>` de `Layout.astro`.

- [ ] **Step 3: Reescrever index.astro**

```astro
---
import { Image } from 'astro:assets';
import Layout from '../layouts/Layout.astro';
import Hero from '../components/Hero.astro';
import TituloSecao from '../components/TituloSecao.astro';
import BotaoWhatsApp from '../components/BotaoWhatsApp.astro';
import Mapa from '../components/Mapa.astro';
import DivisorSimbolo from '../components/DivisorSimbolo.astro';
import MarcaDagua from '../components/MarcaDagua.astro';
import CarrosselAcomodacoes from '../components/CarrosselAcomodacoes.astro';
import { config } from '../lib/cliente';
import { foto } from '../lib/fotos';
---

<Layout>
  <Hero />

  <section id="acomodacoes" class="mx-auto max-w-5xl scroll-mt-20 px-4 py-14">
    <TituloSecao eyebrow="Acomodações">Escolha seu canto</TituloSecao>
    <div class="mt-8">
      <CarrosselAcomodacoes />
    </div>
    <div class="mt-6 text-center">
      <BotaoWhatsApp rotulo="Consultar disponibilidade no WhatsApp" />
    </div>
  </section>

  <DivisorSimbolo />

  <section id="comodidades" class="scroll-mt-20 bg-sal">
    <div class="mx-auto max-w-5xl px-4 py-14">
      <TituloSecao eyebrow="Comodidades">A vida por aqui</TituloSecao>
      <p class="mt-6 max-w-2xl text-lg leading-relaxed">{config.sobre.historia}</p>
      <div class="mt-8 grid gap-6 sm:grid-cols-2">
        {
          config.comodidades.map((comodidade) => (
            <div class="overflow-hidden rounded-xl bg-white shadow-sm">
              {comodidade.foto && (
                <Image
                  src={foto(comodidade.foto.arquivo)}
                  alt={comodidade.foto.alt}
                  widths={[480, 900]}
                  sizes="(min-width: 640px) 480px, 100vw"
                  class="aspect-video w-full object-cover"
                />
              )}
              <div class="p-4">
                <h3 class="font-display text-lg font-bold text-mare">{comodidade.nome}</h3>
                {comodidade.descricao && <p class="mt-1 text-sm">{comodidade.descricao}</p>}
              </div>
            </div>
          ))
        }
      </div>
    </div>
  </section>

  <DivisorSimbolo />

  {
    config.regiao && (
      <section id="regiao" class="mx-auto max-w-5xl scroll-mt-20 px-4 py-14">
        <TituloSecao eyebrow="A região">Explore os arredores</TituloSecao>
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
      </section>
    )
  }

  {config.regiao && <DivisorSimbolo />}

  {
    config.depoimentos && (
      <section id="depoimentos" class="scroll-mt-20 bg-mare">
        <div class="mx-auto max-w-5xl px-4 py-14">
          <TituloSecao eyebrow="Depoimentos" claro>
            Quem passou por aqui
          </TituloSecao>
          <div class="mt-8 grid gap-6 sm:grid-cols-2">
            {config.depoimentos.map((depoimento) => (
              <figure class="rounded-xl bg-white p-6 shadow-sm">
                <blockquote class="leading-relaxed">“{depoimento.texto}”</blockquote>
                <figcaption class="mt-4 text-sm font-bold">
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

  <section id="localizacao" class="mx-auto max-w-5xl scroll-mt-20 px-4 py-14">
    <TituloSecao eyebrow="Localização">Onde estamos</TituloSecao>
    <p class="mt-4 text-lg">{config.localizacao.endereco}</p>
    <div class="mt-8">
      <Mapa />
    </div>
    {
      config.localizacao.comoChegar.length > 0 && (
        <div class="mt-10">
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
  </section>

  <section class="relative isolate overflow-hidden bg-mare">
    <MarcaDagua />
    <div class="mx-auto max-w-5xl px-4 py-14 text-center">
      <h2 class="font-display text-3xl font-bold text-noite">Reserve direto com a gente</h2>
      <p class="mx-auto mt-3 max-w-md text-noite">
        Sem comissão de plataforma: chame no WhatsApp e combine sua estadia direto com quem cuida
        da casa.
      </p>
      <div class="mt-6">
        <BotaoWhatsApp tamanho="grande" />
      </div>
    </div>
  </section>
</Layout>
```

- [ ] **Step 4: Apagar as páginas antigas**

```bash
git rm template/src/pages/acomodacoes.astro template/src/pages/sobre.astro template/src/pages/localizacao.astro
```

Verificar com Grep que nenhuma referência a `/acomodacoes`, `/sobre` ou `/localizacao` sobrou em `template/src` (Footer inclusive; se o Footer linkar rotas antigas, trocar por âncoras).

- [ ] **Step 5: Validar builds + conferência visual**

Run: `cd template && CLIENTE=lumehostel npm run build && CLIENTE=demo npm run build`
Expected: PASS, e `dist/` contém apenas `index.html`.
Subir `CLIENTE=lumehostel npm run dev` e conferir: âncoras do menu rolam para as seções; demo (sem `regiao`/`depoimentos`) não renderiza essas seções.

- [ ] **Step 6: Commit**

```bash
git add -A template/src
git commit -m "One-page com ancoras substitui as 4 paginas do motor"
```

---

### Task 4: Tema LumeHostel — Fredoka única

**Files:**
- Modify: `template/src/styles/temas/lumehostel.css`

- [ ] **Step 1: Unificar a fonte**

Remover `@import "@fontsource-variable/nunito";` e trocar os stacks (removendo a Arial Rounded, que é proprietária e variava entre máquinas):

```css
--font-display: "Fredoka Variable", ui-sans-serif, system-ui, sans-serif;
--font-corpo: "Fredoka Variable", ui-sans-serif, system-ui, sans-serif;
```

Atualizar o comentário do topo do arquivo: a fonte do MIV (Arial Rounded MT Bold) é proprietária; adotada a substituta livre Fredoka em todo o site para render idêntico em qualquer máquina.

- [ ] **Step 2: Validar build e visual**

Run: `cd template && CLIENTE=lumehostel npm run build`
Expected: PASS. No dev server, todo o texto (títulos e corpo) em Fredoka.

- [ ] **Step 3: Commit**

```bash
git add template/src/styles/temas/lumehostel.css
git commit -m "Tema LumeHostel: Fredoka unica em display e corpo"
```

---

### Task 5: Conteúdo — fotos do hostel (Booking/Google) e das regiões (licença livre)

> Task de pesquisa/curadoria, não de código. Fonte de verdade: Booking, Google Maps e Instagram do LumeHostel. NADA além disso.

**Files:**
- Create: `clientes/lumehostel/fotos/<novas fotos do hostel>.jpg` (nomes descritivos: `coworking.jpg`, `cozinha.jpg`, `jardim.jpg`, etc.)
- Create: `clientes/lumehostel/fotos/regiao-<ponto>.jpg` (~5-6 fotos livres)

- [ ] **Step 1: Baixar fotos do hostel das presenças públicas**

Localizar o LumeHostel (Av. Pombal, 1745, Manaíra, João Pessoa) no Booking e no Google Maps. Baixar as fotos publicadas pelo próprio hostel das áreas comuns que ilustram as comodidades (coworking, cozinha, jardim/redes, churrasqueira, sala de jogos). Salvar em `clientes/lumehostel/fotos/` com nomes descritivos, formato jpg, lado maior ≤ 1600px. Só usar fotos publicadas pelo estabelecimento (não de hóspedes). Se alguma comodidade não tiver foto, ela fica sem foto (o layout tolera).

- [ ] **Step 2: Baixar fotos livres da região**

Para cada ponto da curadoria (praia de Manaíra, orla do Bessa, pôr do sol no Jacaré, Centro Histórico, Farol do Cabo Branco, Estação Cabo Branco): buscar foto no Wikimedia Commons ou Unsplash, conferir a licença (CC0/CC-BY/Unsplash License), salvar como `regiao-<slug>.jpg` e anotar autor + licença para o campo `credito` quando a licença exigir atribuição.

- [ ] **Step 3: Commit**

```bash
git add clientes/lumehostel/fotos
git commit -m "Fotos provisorias do hostel (Booking/Maps) e fotos livres da regiao"
```

---

### Task 6: Conteúdo — config.json completo do LumeHostel

**Files:**
- Modify: `clientes/lumehostel/config.json`

**Interfaces:**
- Consumes: schema da Task 1; fotos da Task 5.

- [ ] **Step 1: Preencher comodidades com fotos e descrições curtas**

Para cada comodidade que ganhou foto na Task 5, adicionar `foto: {arquivo, alt}` e uma `descricao` de 1-2 frases derivada APENAS do que as fontes públicas afirmam (ex.: se o Booking lista "cozinha compartilhada", a descrição não pode prometer "café da manhã incluso" se isso não constar lá).

- [ ] **Step 2: Preencher `regiao`**

~5-6 entradas com `nome`, `descricao` (fato geográfico verificável, sem opinião em nome do hostel), `distancia` real a partir do endereço (conferir no Google Maps, ex.: "8 min a pé", "12 km"), `foto` e `credito` quando a licença exigir.

- [ ] **Step 3: Preencher `depoimentos`**

3-4 avaliações públicas reais do Booking/Google: `texto` (trecho fiel, pode encurtar sem alterar sentido), `nome` (primeiro nome apenas), `fonte` ("via Booking" / "via Google"). Escolher avaliações que citem pontos fortes distintos (limpeza, localização, coworking...).

- [ ] **Step 4: Validar build e visual**

Run: `cd template && CLIENTE=lumehostel npm run build`
Expected: PASS (schema valida; `fotos.ts` derruba a build se algum arquivo referido faltar). Conferir todas as seções no dev server.

- [ ] **Step 5: Commit**

```bash
git add clientes/lumehostel/config.json
git commit -m "Conteudo completo do LumeHostel: comodidades ilustradas, regiao e depoimentos"
```

---

### Task 7: Documentação — PENDENCIAS.md e CLAUDE.md

**Files:**
- Modify: `clientes/lumehostel/PENDENCIAS.md`
- Modify: `CLAUDE.md` (seções Arquitetura e Estado atual)

- [ ] **Step 1: Notas para o Gabriel em PENDENCIAS.md**

Adicionar três itens:

1. **Depoimentos** — seção importante do site (prova social), mas alterações futuras exigem manutenção (editar dados + novo deploy). Perguntar ao Gabriel se quer manter a seção.
2. **Fonte** — informar que escolhemos a Fredoka por ser gratuita e fiel ao espírito arredondado do MIV; a Arial Rounded MT Bold é proprietária e ele tem a opção de comprar a licença web se quiser a fonte original no site.
3. **Fotos em alta** — as fotos atuais das áreas comuns vieram do Booking/Google (provisórias); lista-guia do que fotografar: coworking, cozinha, jardim/redes, churrasqueira, sala de jogos, fachada, detalhes dos quartos.

- [ ] **Step 2: Atualizar CLAUDE.md**

Na seção Arquitetura: o motor gera one-page com âncoras (menu âncora + botão WhatsApp), não mais 4 páginas. Na seção Estado atual: registrar a mudança, os campos novos do schema e o estado do LumeHostel (conteúdo de fontes públicas, aguardando validação do Gabriel).

- [ ] **Step 3: Commit**

```bash
git add clientes/lumehostel/PENDENCIAS.md CLAUDE.md
git commit -m "Docs: pendencias do Gabriel (depoimentos, fonte, fotos) e CLAUDE.md do one-page"
```
