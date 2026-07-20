# Fase 3 — Degradê breu → âmbar no site da marca — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Aplicar ao `site/` a direção aprovada no spec `docs/superpowers/specs/2026-07-19-site-degrade-fase3-design.md`: fundo em degradê contínuo breu → âmbar, final nas versões de papel do MIV, iconografia da marca em escala grande e tipografia maior.

**Architecture:** Tudo é camada visual sobre os componentes existentes de `site/src/`. O degradê vive num wrapper único no `Layout.astro`; o final claro é estático (o `CtaFinal` está sempre na zona clara); os ícones vêm de `marca/icones/` por import relativo (mesmo padrão do wordmark no `Hero.astro`).

**Tech Stack:** Astro 5 + Tailwind CSS 4 (`@theme` em `site/src/styles/global.css`). Sem testes automatizados no projeto — verificação é `npm run build` + conferência visual com screenshot (Playwright ou navegador).

## Global Constraints

- Não mudar textos aprovados nem a ordem das seções (`Hero → QuemSouEu → ComoFunciona → Manifesto → Dor → Proposta → Escopo → CtaFinal`).
- Zona clara do degradê: apenas `CtaFinal` (no máximo o fim de `Escopo`). Rampa de referência do spec: `0% e 22% breu · 38% #14100c · 52% #241812 · 68% #4a2a17 · 82% #8a4a24 · 91% barro #c4693f · 100% âmbar #e39a3b` — ajustar percentuais a olho para as 8 seções.
- Mancha de tinta e halo difuso foram rejeitados — não reintroduzir.
- Sem emojis; idioma pt-BR; commits em português.
- Comandos rodam dentro de `site/` (`npm run dev` / `npm run build`).

---

### Task 1: Degradê no Layout

**Files:**
- Modify: `site/src/styles/global.css`
- Modify: `site/src/layouts/Layout.astro:33-35`

**Interfaces:**
- Produces: classe CSS `.pagina-degrade` aplicada a um wrapper dentro do `<body>`; todo o conteúdo do site rola sobre ela. Tasks seguintes assumem que o fundo atrás do `CtaFinal` é âmbar `#e39a3b` e atrás das seções 1–5 é praticamente breu.

- [ ] **Step 1: Adicionar a classe do degradê no global.css**

Acrescentar ao final de `site/src/styles/global.css`:

```css
/* Fase 3: o fundo da página é um degradê contínuo breu -> âmbar (a lâmpada
   acendendo ao longo da rolagem). Zona clara só no CtaFinal.
   Spec: docs/superpowers/specs/2026-07-19-site-degrade-fase3-design.md */
.pagina-degrade {
  min-height: 100vh;
  background: linear-gradient(
    180deg,
    #0a0a09 0%,
    #0a0a09 40%,
    #14100c 52%,
    #241812 62%,
    #4a2a17 74%,
    #8a4a24 84%,
    #c4693f 92%,
    #e39a3b 100%
  );
}
```

(Percentuais partem da rampa do spec, deslocados para baixo porque o site real tem 8 seções — a zona escura precisa cobrir até ~`Dor`/`Proposta`. Serão ajustados a olho na Task 6.)

- [ ] **Step 2: Envolver o slot no Layout**

Em `site/src/layouts/Layout.astro`, trocar:

```astro
  <body class="bg-breu font-sans text-cal antialiased">
    <slot />
  </body>
```

por:

```astro
  <body class="bg-ambar font-sans text-cal antialiased">
    <div class="pagina-degrade">
      <slot />
    </div>
  </body>
</html>
```

(`bg-ambar` no body: se o conteúdo acabar antes da viewport em telas muito altas, a sobra é âmbar — contínua com o fim do degradê — e não breu.)

- [ ] **Step 3: Verificar visualmente**

```
cd site
npm run dev
```

Abrir `http://localhost:4321`. Esperado: topo praticamente preto, cor entrando no meio, `CtaFinal` sobre âmbar. O texto do `CtaFinal` ainda estará ilegível (claro sobre claro) — é a Task 2.

- [ ] **Step 4: Commit**

```bash
git add site/src/styles/global.css site/src/layouts/Layout.astro
git commit -m "Fase 3: fundo do site em degrade continuo breu -> ambar"
```

---

### Task 2: CtaFinal na versão de papel

**Files:**
- Modify: `site/src/components/CtaFinal.astro` (arquivo inteiro)
- Modify: `site/src/components/BotaoWhatsApp.astro`

**Interfaces:**
- Consumes: fundo âmbar da Task 1 atrás da seção.
- Produces: prop `invertido?: boolean` em `BotaoWhatsApp.astro` (default `false`; `Hero` continua usando sem prop).

- [ ] **Step 1: Prop `invertido` no BotaoWhatsApp**

Em `site/src/components/BotaoWhatsApp.astro`, adicionar a prop e condicionar as classes. O elemento hoje usa `class="inline-block rounded-full bg-ambar px-7 py-3 font-medium text-breu transition-colors hover:bg-barro"`. Novo frontmatter e classe:

```astro
---
// (imports existentes permanecem)
interface Props {
  invertido?: boolean;
}
const { invertido = false } = Astro.props;
---
```

E no elemento, trocar o atributo `class` estático por:

```astro
  class:list={[
    "inline-block rounded-full px-7 py-3 font-medium transition-colors",
    invertido ? "bg-breu text-ambar hover:bg-grafite" : "bg-ambar text-breu hover:bg-barro",
  ]}
```

- [ ] **Step 2: Reescrever o CtaFinal para a zona clara**

Substituir o conteúdo de `site/src/components/CtaFinal.astro` por:

```astro
---
import BotaoWhatsApp from "./BotaoWhatsApp.astro";
import { dados } from "../dados";
import iconeContato from "../../../marca/icones/icone-contato-cheio-papel.svg";
import monograma from "../../../marca/monograma-claro.svg";
---

<section class="mx-auto w-full max-w-3xl px-6 pb-6 pt-10 text-breu md:pt-12">
  <img src={iconeContato.src} alt="" class="h-[88px]" />
  <h2 class="mt-6 text-4xl font-bold tracking-[-0.035em] md:text-5xl">
    Tem um hostel? Vamos <em class="font-serifa font-normal">conversar</em>.
  </h2>
  <p class="mt-4 max-w-md text-lg leading-relaxed text-breu/70">
    Me chama no WhatsApp e me conta do seu hostel. A conversa não custa
    nada — nem depois dela.
  </p>
  <div class="mt-7">
    <BotaoWhatsApp invertido />
  </div>
  <footer class="mt-12 flex items-center justify-between border-t border-breu/25 pt-6 text-sm text-breu/70">
    <img src={monograma.src} alt="Código Itinerante" class="h-8" />
    <div class="flex gap-6">
      <a href={`mailto:${dados.email}`} class="hover:text-breu">{dados.email}</a>
      <a href={dados.linkedin} class="hover:text-breu">LinkedIn</a>
    </div>
  </footer>
</section>
```

Mudanças em relação ao atual: sai o card grafite (o fundo agora é o âmbar do degradê), entra o ícone de contato 88px, texto/links em breu, `em` sem `text-ambar` (âmbar sobre âmbar sumiria), monograma na versão clara, botão invertido, alinhamento à esquerda como no mockup aprovado.

- [ ] **Step 3: Verificar visualmente**

Com `npm run dev` rodando, conferir o final da página: texto breu legível sobre âmbar, botão preto, monograma visível. Conferir também que o botão do `Hero` continua âmbar (prop default).

- [ ] **Step 4: Commit**

```bash
git add site/src/components/CtaFinal.astro site/src/components/BotaoWhatsApp.astro
git commit -m "Fase 3: CtaFinal na versao de papel com icone de contato e botao invertido"
```

---

### Task 3: Ícones da marca no ComoFunciona

**Files:**
- Modify: `site/src/components/ComoFunciona.astro` (arquivo inteiro)

**Interfaces:**
- Consumes: SVGs de `marca/icones/` (versões `cheio-breu`, fundo escuro nessa altura da página).

- [ ] **Step 1: Trocar os números pelos ícones**

Substituir o conteúdo de `site/src/components/ComoFunciona.astro` por:

```astro
---
import Eyebrow from "./Eyebrow.astro";
import iconeContato from "../../../marca/icones/icone-contato-cheio-breu.svg";
import iconeHostel from "../../../marca/icones/icone-hostel-cheio-breu.svg";
import iconeSiteProprio from "../../../marca/icones/icone-site-proprio-cheio-breu.svg";
import iconeEstrada from "../../../marca/icones/icone-estrada-cheio-breu.svg";

const passos: { icone: ImageMetadata; titulo: string; texto: string }[] = [
  { icone: iconeContato, titulo: "Conversamos no WhatsApp", texto: "Você me conta do hostel e fechamos juntos o acordo de noites." },
  { icone: iconeHostel, titulo: "Briefing e fotos", texto: "Você preenche um formulário rápido sobre o hostel e me envia as fotos em alta qualidade. Quanto melhores as fotos, mais bonito o site fica." },
  { icone: iconeSiteProprio, titulo: "Quinze dias de construção", texto: "Eu escrevo os textos, monto o site e você acompanha." },
  { icone: iconeEstrada, titulo: "Site no ar, controle seu", texto: "Domínio no seu nome, site sob seu controle total." },
];
---

<section class="mx-auto w-full max-w-3xl px-6 py-10 md:py-12">
  <Eyebrow texto="como" destaque="funciona" />
  <ol class="mt-7 space-y-8">
    {
      passos.map((passo) => (
        <li class="flex gap-6">
          <img src={passo.icone.src} alt="" class="w-[72px] flex-none" />
          <div>
            <h3 class="text-xl font-semibold">{passo.titulo}</h3>
            <p class="mt-1 leading-relaxed text-pedra">{passo.texto}</p>
          </div>
        </li>
      ))
    }
  </ol>
</section>
```

Mapeamento (para validação da autora na revisão final): contato → conversa no WhatsApp; hostel → briefing e fotos; site próprio → construção; estrada → site no ar. Os ícones são decorativos (`alt=""`), a numeração some — a `<ol>` mantém a semântica de sequência.

- [ ] **Step 2: Verificar visualmente**

Conferir a seção "como funciona": 4 ícones a 72px, traço cal com miolo âmbar, legíveis sobre o fundo ainda escuro dessa altura da página.

- [ ] **Step 3: Commit**

```bash
git add site/src/components/ComoFunciona.astro
git commit -m "Fase 3: icones da marca substituem numeros no ComoFunciona"
```

---

### Task 4: Cards translúcidos sobre o degradê

**Files:**
- Modify: `site/src/components/Dor.astro:21`
- Modify: `site/src/components/Escopo.astro:28,34`

**Interfaces:**
- Consumes: degradê da Task 1 (o fundo atrás desses cards é a zona de transição).

- [ ] **Step 1: Dor**

Em `site/src/components/Dor.astro`, trocar:

```astro
  <div class="mt-8 rounded-xl bg-grafite p-6 md:p-7">
```

por:

```astro
  <div class="mt-8 rounded-xl border border-cal/10 bg-grafite/70 p-6 backdrop-blur-sm md:p-7">
```

- [ ] **Step 2: Escopo**

Em `site/src/components/Escopo.astro`, trocar o card "Está incluído":

```astro
    <div class="rounded-xl bg-grafite p-6 md:p-7">
```

por:

```astro
    <div class="rounded-xl border border-cal/10 bg-grafite/70 p-6 backdrop-blur-sm md:p-7">
```

e o card "Não está incluído":

```astro
    <div class="rounded-xl border border-grafite p-6 md:p-7">
```

por:

```astro
    <div class="rounded-xl border border-cal/10 p-6 md:p-7">
```

- [ ] **Step 3: Verificar visualmente**

O degradê deve respirar atrás dos três cards; o texto interno (cal/pedra sobre grafite translúcido) continua legível.

- [ ] **Step 4: Commit**

```bash
git add site/src/components/Dor.astro site/src/components/Escopo.astro
git commit -m "Fase 3: cards translucidos deixam o degrade respirar"
```

---

### Task 5: Tipografia maior no Hero

**Files:**
- Modify: `site/src/components/Hero.astro:8`

- [ ] **Step 1: Subir a escala do h1**

Em `site/src/components/Hero.astro`, trocar:

```astro
  <h1 class="mt-10 text-4xl font-bold leading-[1.05] tracking-[-0.035em] md:text-6xl">
```

por:

```astro
  <h1 class="mt-10 text-5xl font-bold leading-[1.02] tracking-[-0.04em] md:text-7xl">
```

(`text-7xl` = 4.5rem, o teto do spec. O h2 do `CtaFinal` já subiu para `text-4xl md:text-5xl` na Task 2. Os demais títulos de seção são os eyebrows — ficam como estão; reescrita de hierarquia é fora de escopo.)

- [ ] **Step 2: Verificar visualmente**

Hero em desktop e mobile (~375px): o título não pode quebrar feio nem estourar. Se em mobile `text-5xl` apertar, recuar para `text-[2.6rem]`.

- [ ] **Step 3: Commit**

```bash
git add site/src/components/Hero.astro
git commit -m "Fase 3: tipografia do hero maior"
```

---

### Task 6: Ajuste fino da rampa, build e registro no MIV

**Files:**
- Modify: `site/src/styles/global.css` (percentuais da rampa, se necessário)
- Modify: `docs/miv.md` (nova subseção na seção de cores)
- Modify: `docs/ideias-backlog.md` (status da Fase 3)

- [ ] **Step 1: Conferência visual da página inteira**

Com `npm run dev`, rolar a página completa em desktop e mobile e checar:

1. Zona clara começa só depois de `Escopo` — `Proposta` ainda deve ler como escura. Se a cor subir cedo demais, aumentar os percentuais iniciais da rampa (ex.: breu até `45%`).
2. Ponto frágil apontado no spec: texto `pedra` (`#97928a`) sobre os marrons de transição (`#4a2a17`–`#8a4a24`), que no site real cobre `Dor`/`Proposta`/`Escopo`. Se estiver fraco, trocar `text-pedra` por `text-cal/80` nesses componentes.
3. `QuemSouEu`: botão outline âmbar e blockquote com borda âmbar ainda legíveis (estão na zona escura — devem estar ok).

Ajustar a rampa em `.pagina-degrade` até fechar; anotar os percentuais finais.

- [ ] **Step 2: Build de produção**

```
cd site
npm run build
```

Esperado: build sem erros. Rodar `npm run preview` e repetir a conferência rápida.

- [ ] **Step 3: Registrar a exceção no MIV**

Em `docs/miv.md`, na seção de cores (após a regra "Sobre escuro, nunca usar Queimado..."), acrescentar:

```markdown
**Exceção deliberada (site da marca, Fase 3 — 2026-07-19)**: o fundo do site
institucional é um degradê contínuo Breu → Âmbar revelado pela rolagem — a
lâmpada acendendo. O âmbar em área grande é o ponto de chegada da página, não
o tom geral da marca; a regra do acento segue valendo em todas as outras
aplicações. O trecho final (zona clara) usa as versões de papel: texto Tinta/
Breu, ícones `-papel`, monograma claro.
```

- [ ] **Step 4: Marcar a Fase 3 no backlog**

Em `docs/ideias-backlog.md`, seção Status, trocar:

```markdown
- [ ] Fase 3 — Splash de cor + arte no site
```

por:

```markdown
- [x] Fase 3 — Degradê breu → âmbar + iconografia no site (2026-07-19)
```

- [ ] **Step 5: Commit final**

```bash
git add site/src/styles/global.css docs/miv.md docs/ideias-backlog.md
git commit -m "Fase 3 concluida: rampa ajustada, excecao registrada no MIV"
```

---

## Self-review (feito na escrita)

- **Cobertura do spec**: degradê (T1), versão de papel no final (T2), iconografia grande (T2+T3), cards translúcidos (T4), tipografia maior (T5), rampa nas 8 seções + contraste + exceção no MIV (T6). Rejeitados (mancha/halo/cor sólida) listados nas Global Constraints como proibição.
- **Sem placeholders**: todo step de código mostra o código completo.
- **Consistência**: `invertido` definido na T2 e usado só lá; imports de ícones seguem o padrão `../../../marca/...` já usado pelo `Hero.astro` (T2, T3).
