# Nav com Hambúrguer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Trocar o padrão de menu do motor (logo + links inline) por logo à esquerda / botão WhatsApp + hambúrguer à direita sempre na mesma linha, com os links num menu suspenso — novo padrão para todo cliente, aplicado agora em LumeHostel e Mar à Vista.

**Architecture:** `Nav.astro` vira layout único (sem branch por `logoFixoEsquerda`), usando a **Popover API nativa do HTML** (`popover` attribute) para o menu suspenso — dá dismiss automático (clique fora / Esc) sem JS extra. A animação do ícone de hambúrguer usa só Tailwind (`group-has-[#menu-nav:popover-open]:...`), sem `<style>` custom (o projeto não usa CSS solto em `.astro`, só utilitário). `BotaoWhatsApp.astro` ganha um prop `icone` pra virar ícone-só no mobile.

**Tech Stack:** Astro 5, Tailwind CSS 4, Zod (schema.ts). Sem framework de teste — verificação é `astro check`, `astro build` e checagem visual via dev server.

## Global Constraints

- Não usar `<style>` solto em `.astro` — só classes Tailwind (padrão já seguido em todo `template/src/components/`).
- `BotaoWhatsApp` com `icone` não pode alterar o comportamento das 2 chamadas existentes em `index.astro` (`rotulo="Consultar disponibilidade..."` e `tamanho="grande"`) — `icone` default `false`.
- Layout novo do `Nav.astro` é único (sem condicional) — remove de vez o branch por `logoFixoEsquerda`.
- Idioma de commits/docs: português.

---

### Task 1: `BotaoWhatsApp` com variante ícone-só (mobile)

**Files:**
- Modify: `template/src/components/BotaoWhatsApp.astro`

**Interfaces:**
- Produces: prop `icone?: boolean` (default `false`) em `BotaoWhatsApp`. Quando `true`, renderiza ícone do WhatsApp + texto escondido abaixo do breakpoint `sm` (Tailwind `hidden sm:inline`), com `aria-label` no `<a>` garantindo o rótulo acessível.

- [ ] **Step 1: Reescrever o componente com o novo prop**

Substituir o conteúdo de `template/src/components/BotaoWhatsApp.astro` por:

```astro
---
import { config } from '../lib/cliente';

interface Props {
  rotulo?: string;
  tamanho?: 'medio' | 'grande';
  icone?: boolean;
}

const { rotulo = 'Reserve pelo WhatsApp', tamanho = 'medio', icone = false } = Astro.props;

const mensagem = encodeURIComponent(
  `Ola! Vi o site do ${config.nome} e quero saber valores e disponibilidade.`,
);
const href = `https://wa.me/${config.contato.whatsapp}?text=${mensagem}`;

const tamanhos = {
  medio: 'px-4 py-2 text-sm',
  grande: 'px-6 py-3 text-base',
};
---

<a
  href={href}
  target="_blank"
  rel="noopener noreferrer"
  aria-label={icone ? rotulo : undefined}
  class:list={[
    'inline-flex items-center justify-center gap-2 rounded-full bg-zap font-corpo font-bold text-noite transition hover:brightness-110 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-azulejo',
    icone ? 'p-2.5 sm:px-4 sm:py-2' : tamanhos[tamanho],
  ]}
>
  {
    icone && (
      <svg viewBox="0 0 24 24" class="h-5 w-5 shrink-0 fill-current" aria-hidden="true">
        <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.006c.106.005.249-.04.39.298.144.347.491 1.2.534 1.287.043.087.072.188.014.304-.058.116-.087.188-.173.289l-.26.304c-.087.086-.177.18-.076.354.101.174.449.741.964 1.201.662.591 1.221.774 1.394.86s.274.072.376-.043c.101-.116.433-.506.549-.68.116-.173.231-.145.39-.087s1.011.477 1.184.564.289.13.332.202c.045.072.045.419-.1.824zM12.014 21.785h-.005c-1.762 0-3.49-.474-4.998-1.371l-.359-.213-3.719.976.992-3.623-.233-.372a9.945 9.945 0 0 1-1.522-5.32c.002-5.514 4.491-10.002 10.008-10.002 2.672 0 5.181 1.042 7.07 2.933a9.94 9.94 0 0 1 2.924 7.078c-.002 5.514-4.491 10-10.006 10.002z" />
      </svg>
    )
  }
  <span class:list={[icone && 'hidden sm:inline']}>{rotulo}</span>
</a>
```

- [ ] **Step 2: Checar tipos**

Run: `cd template && npm run check`
Expected: `0 errors` (o novo prop `icone?` é opcional e compatível com as 2 chamadas existentes que não o passam).

- [ ] **Step 3: Commit**

```bash
git add template/src/components/BotaoWhatsApp.astro
git commit -m "Botao WhatsApp ganha variante icone-so, pra caber ao lado do hamburguer no mobile"
```

---

### Task 2: `Nav.astro` — layout único com menu suspenso (Popover API)

**Files:**
- Modify: `template/src/components/Nav.astro`

**Interfaces:**
- Consumes: `BotaoWhatsApp` com `icone` (Task 1).
- Produces: nav sempre em uma linha (logo esquerda, botão+hambúrguer direita); menu suspenso `#menu-nav` com os links de `abas` + itens inertes de `config.navFuturo`.

- [ ] **Step 1: Reescrever `Nav.astro`**

Substituir o conteúdo de `template/src/components/Nav.astro` por:

```astro
---
import { config } from '../lib/cliente';
import { marca } from '../lib/fotos';
import BotaoWhatsApp from './BotaoWhatsApp.astro';

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

const logo = config.marca?.logo ? marca(config.marca.logo) : undefined;
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
      href="/"
      class="font-display text-xl font-bold focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-azulejo"
    >
      {/* SVG vetorial: `<img>` cru é intencional — astro:assets otimiza raster, não SVG. */}
      {logo ? <img src={logo.src} alt={config.nome} class="h-9 w-auto" /> : config.nome}
    </a>
    <div class="flex items-center gap-3">
      <BotaoWhatsApp icone />
      <button
        popovertarget="menu-nav"
        popovertargetaction="toggle"
        aria-label="Abrir menu"
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
    class="fixed top-[4.5rem] right-4 m-0 flex flex-col gap-1 rounded-2xl border-0 bg-sal p-2 text-noite shadow-xl"
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
</script>
```

Note: `logoFixoEsquerda` deixou de ser lido aqui de propósito — a Task 3 remove o campo do schema/config.

- [ ] **Step 2: Checar tipos**

Run: `cd template && npm run check`
Expected: `0 errors`.

- [ ] **Step 3: Commit**

```bash
git add template/src/components/Nav.astro
git commit -m "Nav.astro: layout unico com hamburguer (Popover API), logo esquerda + botao/hamburguer direita sempre na mesma linha"
```

---

### Task 3: Remover `logoFixoEsquerda` do schema e do config do Mar à Vista

**Files:**
- Modify: `template/src/lib/schema.ts`
- Modify: `clientes/maravista/config.json`

**Interfaces:**
- Consumes: nada (campo já não é lido por nenhum componente após a Task 2).
- Produces: `marcaSchema` sem o campo `logoFixoEsquerda`.

- [ ] **Step 1: Remover o campo do schema**

Em `template/src/lib/schema.ts`, dentro de `marcaSchema`, remover estas linhas:

```ts
  /** Quando true, o logo do menu fica sempre alinhado à esquerda, mesmo no
   *  layout mobile empilhado (padrão: centralizado). */
  logoFixoEsquerda: z.boolean().optional(),
```

- [ ] **Step 2: Remover a chave do config do Mar à Vista**

Em `clientes/maravista/config.json`, dentro de `"marca"`, remover:

```json
    "logoFixoEsquerda": true,
```

(cuidado para não deixar vírgula sobrando antes da chave seguinte, `"logoApenasNoMenu"`.)

- [ ] **Step 3: Checar tipos e build dos dois clientes**

Run: `cd template && npm run check`
Expected: `0 errors`.

Run: `cd template && CLIENTE=maravista npm run build`
Expected: build termina sem erro do Zod (config ainda válido sem o campo removido).

Run: `cd template && CLIENTE=lumehostel npm run build`
Expected: build termina sem erro (LumeHostel nunca usou o campo).

- [ ] **Step 4: Commit**

```bash
git add template/src/lib/schema.ts clientes/maravista/config.json
git commit -m "Remove logoFixoEsquerda: layout do Nav agora e unico, campo ficou sem funcao"
```

---

### Task 4: Verificação visual — LumeHostel e Mar à Vista, mobile e desktop

**Files:** nenhum (só verificação, sem mudança de código).

- [ ] **Step 1: Subir o dev server do LumeHostel**

Run (background): `cd template && CLIENTE=lumehostel npm run dev`
Expected: `astro v5.x ready` em `http://localhost:4321/`.

- [ ] **Step 2: Verificar em largura desktop (~1280px)**

Abrir `http://localhost:4321/` no navegador em ~1280px de largura. Confirmar:
- Logo à esquerda, botão "Reserve pelo WhatsApp" (com texto) + hambúrguer à direita, tudo numa linha só.
- Clicar no hambúrguer abre a lista (O Hostel, Acomodações, Comodidades, A vibe, A região, Localização) perto do canto superior direito, sem sobrepor nem deixar vão grande em relação à barra.
- Clicar fora do menu (ou Esc) fecha.
- Hero mostra só "LUME HOSTEL" + a frase, sem botão duplicado, perto do rodapé da hero.

- [ ] **Step 3: Verificar em largura mobile (~375px)**

Redimensionar para ~375px. Confirmar:
- Mesma linha única (logo | ícone do WhatsApp | hambúrguer), sem quebrar.
- Botão do WhatsApp mostra só o ícone (sem o texto "Reserve pelo WhatsApp" visível).
- Menu abre/fecha igual ao desktop.

- [ ] **Step 4: Repetir para o Mar à Vista**

Parar o dev server do LumeHostel (Ctrl+C no processo em background) e rodar:

Run (background): `cd template && CLIENTE=maravista npm run dev`

Repetir as verificações dos Steps 2 e 3 em `http://localhost:4321/`, e adicionalmente confirmar que o menu suspenso mostra "O Hostel" como link real e os 4 itens de `navFuturo` (Acomodações, Comodidades, A região, Localização) como texto não clicável, na mesma cor dos links reais.

- [ ] **Step 5: Ajustar `top-[4.5rem]` se necessário**

Se houver vão visível ou sobreposição entre a barra e o menu suspenso em qualquer um dos dois clientes, ajustar o valor arbitrário `top-[4.5rem]` em `template/src/components/Nav.astro` até encostar certinho, e repetir Steps 2–4.

- [ ] **Step 6: Commit se houve ajuste no Step 5**

```bash
git add template/src/components/Nav.astro
git commit -m "Ajusta posicao vertical do menu suspenso do Nav"
```

---

### Task 5: Redeploy de produção — LumeHostel e Mar à Vista

**Files:** nenhum (só deploy).

**Interfaces:**
- Consumes: projetos Vercel `lumehostel` e `maravista` já configurados (Root Directory `.`, build `cd template && npm run build`) — ver receita em `CLAUDE.md`, seção Comandos.

- [ ] **Step 1: Push do que foi commitado nas Tasks 1–4**

Run: `git push`
Expected: `master -> master` sem erro.

- [ ] **Step 2: Redeploy do LumeHostel**

Run: `vercel deploy --prod --cwd template --project lumehostel`
Expected: saída `"readyState": "READY"`, `"target": "production"`.

- [ ] **Step 3: Redeploy do Mar à Vista**

Run: `vercel deploy --prod --cwd template --project maravista`
Expected: saída `"readyState": "READY"`, `"target": "production"`.

- [ ] **Step 4: Conferir as duas URLs de produção**

Run: `curl -s -o /dev/null -w "%{http_code}\n" https://lumehostel.vercel.app` → esperado `200`.
Run: `curl -s -o /dev/null -w "%{http_code}\n" https://maravista-plum.vercel.app` → esperado `200`.

- [ ] **Step 5: Atualizar `CLAUDE.md`**

Adicionar uma linha ao final da seção "Estado atual" registrando: nav com hambúrguer virou padrão do motor (2026-07-23), LumeHostel e Mar à Vista redeployados com o nav novo e a hero do Lume sem o botão duplicado.

- [ ] **Step 6: Commit e push**

```bash
git add CLAUDE.md
git commit -m "docs: registra o novo padrao de nav (hamburguer) e o redeploy dos dois clientes"
git push
```

---

## Self-Review

- **Cobertura do spec:** ordem botão-depois-hambúrguer (Task 2, `grupo-direita` = `BotaoWhatsApp` antes do `<button>`) ✓; uma linha sempre (Task 2, `flex items-center justify-between` sem breakpoint condicional) ✓; ícone-só no mobile (Task 1) ✓; Popover API nativa (Task 2) ✓; `navFuturo` mesma cor, não clicável (Task 2) ✓; remover `logoFixoEsquerda` (Task 3) ✓; hero do Lume sem código extra, só redeploy (Task 5) ✓; redeploy dos dois clientes (Task 5) ✓.
- **Placeholders:** nenhum — todo step tem código ou comando exato.
- **Consistência de nomes:** prop `icone` (Task 1) usado igual em `<BotaoWhatsApp icone />` (Task 2); `id="menu-nav"` usado igual no `popovertarget` do botão e no `has-[#menu-nav:popover-open]` (Task 2).
