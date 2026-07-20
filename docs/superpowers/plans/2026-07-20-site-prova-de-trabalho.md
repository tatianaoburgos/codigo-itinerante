# Seção "prova de trabalho" — Plano de Implementação

> **Para trabalhadores agênticos:** SUB-SKILL OBRIGATÓRIA: use
> superpowers:subagent-driven-development (recomendado) ou
> superpowers:executing-plans para implementar tarefa a tarefa. Os passos usam
> caixas (`- [ ]`) para acompanhamento.

**Objetivo:** Adicionar ao site da marca uma seção de case único mostrando o site do
LumeHostel, entre "Quem sou eu" e "Como funciona", e recalibrar o degradê da página
para que a cor passe a entrar no ComoFunciona.

**Arquitetura:** Um componente Astro novo e autocontido (`ProvaDeTrabalho.astro`) com o
conteúdo do case escrito nele mesmo, mais duas capturas de tela reais servidas por
`astro:assets`. A moldura de navegador e o celular são markup + Tailwind, não imagem.
Por último, as paradas do gradiente em `global.css` são remedidas com a página nova
montada.

**Stack:** Astro 5, Tailwind CSS 4, `astro:assets`. Capturas feitas com o Playwright MCP.

**Spec:** `docs/superpowers/specs/2026-07-20-site-prova-de-trabalho-design.md`

## Restrições globais

- Todo o trabalho acontece em `site/`. Não tocar em `template/` nem em `clientes/`.
- Idioma de conteúdo, comentários e mensagens de commit: português brasileiro.
- **Sem emojis** em código, texto ou commits.
- **Este repositório não tem test runner nem linter.** A verificação de cada tarefa é
  `npm run build` passando + conferência visual no navegador. Não invente um framework
  de testes; não crie `tests/`.
- O texto do case é literal e já foi aprovado — não reescrever:
  - Título: `LumeHostel — João Pessoa, PB`
  - Corpo: `Site institucional completo: acomodações, comodidades, a região, depoimentos e localização. Reserva direta pelo WhatsApp. No ar desde julho de 2026.`
  - Botão: `Ver o site no ar`
- **Nunca afirmar** que houve permuta, noites pagas ou domínio próprio do cliente. Nada
  disso é verdade (ver spec, seção "O que a seção afirma").
- Cores só pelos tokens do tema (`breu`, `grafite`, `cal`, `pedra`, `ambar`, `barro`,
  `dourado`), definidos em `site/src/styles/global.css:8-20`.
- Comandos rodam no PowerShell (Windows). `VAR=x cmd` não funciona; use
  `$env:VAR = 'x'; cmd`.

---

### Task 1: Capturar os prints do LumeHostel

**Arquivos:**
- Criar: `site/src/assets/portfolio/lumehostel-desktop.png`
- Criar: `site/src/assets/portfolio/lumehostel-mobile.png`

**Interfaces:**
- Consome: nada.
- Produz: dois PNGs importáveis por `astro:assets`. A Task 2 os importa exatamente por
  esses caminhos. `lumehostel-desktop.png` tem 1440×900; `lumehostel-mobile.png` tem
  390×844.

- [ ] **Passo 1: Criar a pasta**

```powershell
New-Item -ItemType Directory -Force C:\Users\tatia\codigo-itinerante\site\src\assets\portfolio
```

- [ ] **Passo 2: Capturar a primeira dobra em desktop**

Carregue as ferramentas do Playwright MCP:

```
ToolSearch: select:mcp__plugin_playwright_playwright__browser_navigate,mcp__plugin_playwright_playwright__browser_resize,mcp__plugin_playwright_playwright__browser_take_screenshot,mcp__plugin_playwright_playwright__browser_evaluate,mcp__plugin_playwright_playwright__browser_close
```

Depois:

1. `browser_resize` com `width: 1440`, `height: 900`
2. `browser_navigate` para `https://lumehostel.vercel.app`
3. Aguarde as imagens carregarem — o site do LumeHostel é dominado por fotografia e o
   hero tem animação de surgimento (`.revela`). Rode `browser_evaluate`:

```js
async () => {
  await Promise.all(Array.from(document.images)
    .filter((img) => !img.complete)
    .map((img) => new Promise((r) => { img.onload = r; img.onerror = r; })));
  window.scrollTo(0, 0);
  return document.images.length;
}
```

4. `browser_take_screenshot` com
   `filename: "C:\\Users\\tatia\\codigo-itinerante\\site\\src\\assets\\portfolio\\lumehostel-desktop.png"`,
   `fullPage: false`, `type: "png"`

- [ ] **Passo 3: Capturar a primeira dobra em celular**

1. `browser_resize` com `width: 390`, `height: 844`
2. `browser_navigate` para `https://lumehostel.vercel.app` (recarrega no viewport novo;
   o hero usa `min-h-dvh` no mobile e precisa relayoutar)
3. Repita o `browser_evaluate` do Passo 2 para esperar as imagens
4. `browser_take_screenshot` com
   `filename: "C:\\Users\\tatia\\codigo-itinerante\\site\\src\\assets\\portfolio\\lumehostel-mobile.png"`,
   `fullPage: false`, `type: "png"`
5. `browser_close`

- [ ] **Passo 4: Verificar dimensões e conteúdo**

```powershell
Get-ChildItem C:\Users\tatia\codigo-itinerante\site\src\assets\portfolio\*.png | Select-Object Name, Length
```

Esperado: dois arquivos, ambos com `Length` maior que zero.

Agora **olhe as duas imagens** com a ferramenta Read. Elas precisam mostrar o hero do
LumeHostel com a foto de capa carregada. Se alguma vier com foto faltando, fundo
chapado ou texto invisível (a animação `.revela` não disparou), refaça a captura
correspondente rolando a página 1px antes do screenshot para forçar o
IntersectionObserver:

```js
() => { window.scrollTo(0, 1); window.scrollTo(0, 0); return true; }
```

- [ ] **Passo 5: Commit**

```powershell
cd C:\Users\tatia\codigo-itinerante
git add site/src/assets/portfolio/
git commit -m "Capturas do site do LumeHostel para a secao de portfolio"
```

---

### Task 2: Componente ProvaDeTrabalho e inserção na página

**Arquivos:**
- Criar: `site/src/components/ProvaDeTrabalho.astro`
- Modificar: `site/src/pages/index.astro` (import + posição entre `<QuemSouEu />` e `<ComoFunciona />`)

**Interfaces:**
- Consome: os dois PNGs da Task 1; `Eyebrow.astro` (props `texto: string`,
  `destaque?: string`).
- Produz: `<ProvaDeTrabalho />`, componente sem props. A Task 3 mede a posição desta
  seção na página, que é um `<section>` filho direto de `.pagina-degrade`.

- [ ] **Passo 1: Criar o componente**

Crie `site/src/components/ProvaDeTrabalho.astro` com exatamente este conteúdo:

```astro
---
import { Image } from "astro:assets";
import Eyebrow from "./Eyebrow.astro";
import printDesktop from "../assets/portfolio/lumehostel-desktop.png";
import printMobile from "../assets/portfolio/lumehostel-mobile.png";

const url = "https://lumehostel.vercel.app";
---

<section class="mx-auto w-full max-w-3xl px-6 py-10 md:py-12">
  <Eyebrow texto="prova de" destaque="trabalho" />

  <div class="relative mt-7">
    <a
      href={url}
      target="_blank"
      rel="noopener"
      class="block overflow-hidden rounded-xl border border-pedra/20 shadow-2xl transition-transform hover:-translate-y-1"
    >
      <div class="flex items-center gap-2 bg-grafite px-4 py-3">
        <span class="h-2.5 w-2.5 rounded-full bg-pedra/40"></span>
        <span class="h-2.5 w-2.5 rounded-full bg-pedra/40"></span>
        <span class="h-2.5 w-2.5 rounded-full bg-pedra/40"></span>
        <span class="ml-3 font-mono text-xs text-pedra">lumehostel.vercel.app</span>
      </div>
      <Image
        src={printDesktop}
        alt="Primeira dobra do site do LumeHostel vista no computador"
        width={1440}
        class="w-full"
      />
    </a>

    <div
      class="pointer-events-none absolute -bottom-6 right-6 hidden w-[130px] overflow-hidden rounded-[1.5rem] border-4 border-grafite shadow-2xl md:block"
    >
      <Image
        src={printMobile}
        alt="O mesmo site do LumeHostel visto no celular"
        width={390}
        class="w-full"
      />
    </div>
  </div>

  <div class="mt-10 space-y-5 leading-relaxed md:mt-16">
    <h3 class="text-xl font-semibold">LumeHostel — João Pessoa, PB</h3>
    <p>
      Site institucional completo: acomodações, comodidades, a região,
      depoimentos e localização. Reserva direta pelo WhatsApp. No ar desde
      julho de 2026.
    </p>
    <p>
      <a
        href={url}
        target="_blank"
        rel="noopener"
        class="inline-block rounded-full border border-ambar px-6 py-2.5 font-medium text-ambar transition-colors hover:bg-ambar hover:text-breu"
      >Ver o site no ar</a>
    </p>
  </div>
</section>
```

- [ ] **Passo 2: Inserir na página**

Em `site/src/pages/index.astro`, adicione o import depois da linha do `QuemSouEu`:

```astro
import QuemSouEu from "../components/QuemSouEu.astro";
import ProvaDeTrabalho from "../components/ProvaDeTrabalho.astro";
```

E o componente entre `<QuemSouEu />` e `<ComoFunciona />`:

```astro
  <Hero />
  <QuemSouEu />
  <ProvaDeTrabalho />
  <ComoFunciona />
```

- [ ] **Passo 3: Verificar que a build passa**

```powershell
cd C:\Users\tatia\codigo-itinerante\site
npm run build
```

Esperado: termina sem erro, com linha `Complete!`. Se falhar com erro de import de
imagem, confira que os PNGs da Task 1 existem nos caminhos exatos.

- [ ] **Passo 4: Conferir visualmente**

Suba o dev server em background:

```powershell
cd C:\Users\tatia\codigo-itinerante\site
npm run dev
```

Com o Playwright: `browser_resize` 1440×900, `browser_navigate` para
`http://localhost:4321`, role até a seção e tire um screenshot para olhar.

Confira, olhando a imagem:
- a moldura de navegador aparece com os três círculos e a URL legível;
- o celular está sobreposto no canto inferior direito, vazando um pouco da moldura;
- o celular **não** cobre o texto do case;
- o print está nítido, não esticado nem achatado.

Depois `browser_resize` para 390×844 e confira que **o celular sumiu** e a moldura de
navegador ocupa a largura toda sem estourar para os lados.

Se o celular colidir com o texto no desktop, aumente `md:mt-16` para `md:mt-20` no
bloco de texto — não mexa na posição do celular.

- [ ] **Passo 5: Commit**

```powershell
cd C:\Users\tatia\codigo-itinerante
git add site/src/components/ProvaDeTrabalho.astro site/src/pages/index.astro
git commit -m "Secao prova de trabalho: case do LumeHostel no site da marca"
```

---

### Task 3: Recalibrar o degradê da página

**Arquivos:**
- Modificar: `site/src/styles/global.css:22-41` (comentário e paradas de `.pagina-degrade`)

**Interfaces:**
- Consome: a página com a seção nova montada (Task 2).
- Produz: nada consumido por tarefas posteriores. É a última tarefa.

**Contexto:** hoje o breu sólido vai até 43% e a cor entra no Manifesto. Precisa passar
a cobrir Hero + QuemSouEu + ProvaDeTrabalho, com a cor entrando no **ComoFunciona**.
O âmbar cheio continua chegando pouco antes do `CtaFinal`. Os números atuais foram
medidos, não estimados — os novos também têm que ser.

- [ ] **Passo 1: Medir as posições das seções**

Com o dev server rodando, use `browser_resize` 1440×900, `browser_navigate` para
`http://localhost:4321` e rode `browser_evaluate`:

```js
() => {
  const total = document.documentElement.scrollHeight;
  const nomes = ["Hero", "QuemSouEu", "ProvaDeTrabalho", "ComoFunciona",
                 "Manifesto", "Dor", "Proposta", "Escopo", "CtaFinal"];
  return Array.from(document.querySelectorAll(".pagina-degrade > section"))
    .map((s, i) => ({
      secao: nomes[i] ?? `secao-${i}`,
      inicio: +(s.offsetTop / total * 100).toFixed(1),
    }));
}
```

Anote o resultado. Repita com `browser_resize` 390×844 — os percentuais mudam bastante
entre desktop e mobile.

- [ ] **Passo 2: Escolher as paradas**

Regras para converter as medidas em paradas:

- O breu sólido (`#0a0a09`) vai de `0%` até o **menor** valor de `inicio` do
  ComoFunciona entre desktop e mobile. Usar o menor garante que nenhum dos dois
  layouts comece a acender antes da hora.
- O âmbar cheio (`#e39a3b`) começa no **menor** `inicio` do CtaFinal, menos ~1 ponto,
  e vai até `100%`.
- As paradas intermediárias (`#241812`, `#4a2a17`, `#8a4a24`, `#c4693f`) se distribuem
  entre esses dois pontos mantendo o espaçamento proporcional que têm hoje (9, 10, 11,
  10, 7 pontos entre paradas consecutivas). Reescale proporcionalmente ao novo intervalo.

- [ ] **Passo 3: Reescrever o bloco**

Em `site/src/styles/global.css`, substitua o comentário e o bloco `.pagina-degrade`
pelos valores calculados. Mantenha o formato, trocando os `NN` pelos números medidos e
os nomes das seções pelos corretos:

```css
/* Fase 3: o fundo da página é um degradê contínuo breu -> âmbar (a lâmpada
   acendendo ao longo da rolagem). Breu solido cobre Hero + QuemSouEu +
   ProvaDeTrabalho; a cor começa a entrar exatamente no ComoFunciona
   (medido: NN% em desktop e NN% em mobile) e chega em âmbar cheio pouco
   antes do CtaFinal (~NN%), que fica na zona clara.
   Specs: docs/superpowers/specs/2026-07-19-site-degrade-fase3-design.md e
   docs/superpowers/specs/2026-07-20-site-prova-de-trabalho-design.md */
.pagina-degrade {
  min-height: 100vh;
  background: linear-gradient(
    180deg,
    #0a0a09 0%,
    #0a0a09 NN%,
    #241812 NN%,
    #4a2a17 NN%,
    #8a4a24 NN%,
    #c4693f NN%,
    #e39a3b NN%,
    #e39a3b 100%
  );
}
```

- [ ] **Passo 4: Conferir visualmente nos dois tamanhos**

Com o dev server rodando, em 1440×900 e depois em 390×844, tire screenshots em várias
alturas de rolagem (topo, meio, fim) e confirme, olhando:

- a seção "prova de trabalho" está inteira sobre breu sólido — nenhum tom de marrom
  aparecendo atrás do print;
- a cor começa a aparecer no ComoFunciona, não antes;
- o `CtaFinal` está inteiro na zona âmbar clara, com o texto em breu legível;
- não há faixa de cor visível "emendando" (transição dura entre duas paradas).

- [ ] **Passo 5: Verificar a build e commitar**

```powershell
cd C:\Users\tatia\codigo-itinerante\site
npm run build
```

Esperado: `Complete!` sem erros.

```powershell
cd C:\Users\tatia\codigo-itinerante
git add site/src/styles/global.css
git commit -m "Recalibra o degrade: cor passa a entrar no ComoFunciona"
```

---

## Verificação final

Depois das três tarefas, com o dev server rodando:

1. `npm run build` em `site/` termina com `Complete!`.
2. A página em 1440×900 mostra a seção nova entre "Quem sou eu" e "Como funciona", com
   moldura de navegador, celular sobreposto e botão âmbar.
3. A página em 390×844 mostra a mesma seção sem o celular e sem rolagem horizontal.
4. O link "Ver o site no ar" abre `https://lumehostel.vercel.app` em aba nova.
5. Nenhum texto da seção menciona permuta, noites ou domínio próprio.

Encerre o dev server em background quando terminar.
