# Ícones de redes sociais no rodapé — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rodapé do motor de cliente (`template/`) ganha um bloco "Siga a
gente" com ícones de Instagram/TikTok/Facebook, só quando o cliente tiver
pelo menos uma dessas redes preenchida no `config.json`; LumeHostel ganha
Instagram (já tinha) e TikTok.

**Architecture:** Dois campos novos opcionais no schema Zod
(`contato.tiktok`, `contato.facebook`); um componente novo,
`IconeRedeSocial.astro`, biblioteca de 3 ícones desenhados à mão em SVG
(mesmo padrão de `SimboloComodidade.astro`); `Footer.astro` monta as URLs,
remove o Instagram da lista "Fale conosco" e renderiza o bloco de ícones
condicionalmente, expandindo o grid pra 3 colunas quando há rede social.

**Tech Stack:** Astro 7, Zod (schema), Tailwind 4 (`class:list`).

## Global Constraints

- Ícones são SVG desenhados sob medida (viewBox 0 0 48 48, traço
  `currentColor`) — nunca ícones literais de biblioteca de terceiros
  (`docs/diretrizes-design.md`).
- Cor do ícone vem do tema do cliente (`fitinha`), nunca hardcoded.
- Escopo fechado: só `template/` (não `site/`); só Instagram, TikTok,
  Facebook — sem campo genérico de "redes futuras".
- Cada campo de rede social é opcional; ausência de todos os três mantém o
  rodapé exatamente como hoje (2 colunas, sem bloco novo).
- Sem emoji em nenhum texto/comentário.

---

### Task 1: Schema + componente de ícone + integração no rodapé

**Files:**
- Modify: `template/src/lib/schema.ts` (bloco `contato`, por volta da linha 116-120)
- Create: `template/src/components/IconeRedeSocial.astro`
- Modify: `template/src/components/Footer.astro` (arquivo inteiro, 47 linhas hoje)

**Interfaces:**
- Produces: `contato.tiktok?: string`, `contato.facebook?: string` no tipo
  `ConfigCliente` (schema.ts).
- Produces: componente `IconeRedeSocial` — props `{ rede: 'instagram' |
  'tiktok' | 'facebook'; class?: string }`, renderiza um `<svg
  aria-hidden="true">` com o desenho da rede pedida.
- Consumes: `config.contato` (de `template/src/lib/cliente.ts`, já
  importado por `Footer.astro`).

- [x] **Step 1: Adicionar os campos no schema**

Em `template/src/lib/schema.ts`, dentro do `contato: z.object({...})`
(linhas 116-120), depois de `instagram`:

```ts
  contato: z.object({
    whatsapp: z.string().regex(/^\d{12,13}$/, 'somente dígitos, com DDI e DDD (ex.: 5571999998888)'),
    email: z.email(),
    instagram: z.string().optional(),
    tiktok: z.string().optional(),
    facebook: z.string().optional(),
  }),
```

- [x] **Step 2: Rodar o check do Astro pra confirmar que o schema ainda é válido**

Run: `cd template && npm run check`
Expected: passa sem erros (campos novos são opcionais, nenhum config
existente muda de forma).

- [x] **Step 3: Criar a biblioteca de ícones `IconeRedeSocial.astro`**

Criar `template/src/components/IconeRedeSocial.astro`:

```astro
---
export type RedeSocial = 'instagram' | 'tiktok' | 'facebook';

interface Props {
  rede: RedeSocial;
  class?: string;
}

const { rede, class: classe } = Astro.props;

/**
 * Ícones de redes sociais desenhados à mão (traço grosso, viewBox 48),
 * mesmo espírito da biblioteca de símbolos de comodidade
 * (SimboloComodidade.astro) — nunca ícones literais de biblioteca de
 * terceiros. Ver diretrizes-design.md.
 */
const desenhos: Record<RedeSocial, string> = {
  instagram: `
    <rect x="6" y="6" width="36" height="36" rx="12" />
    <circle cx="24" cy="24" r="8" />
    <circle cx="34" cy="14" r="1.2" fill="currentColor" stroke="none" />`,
  tiktok: `
    <path d="M32 7c1 4.6 4 7.4 9.2 8v5.4c-3.2 0-6.2-.8-9.2-2.8v12.8a10 10 0 1 1-10-10c.6 0 1.2 0 1.8.2" />`,
  facebook: `
    <path d="M28 41v-14h4.6l.8-5.6H28V17.2c0-1.6.4-2.6 2.6-2.6H34V9c-.6 0-2.4-.2-4.4-.2-4.4 0-7.2 2.6-7.2 7.4v5.2H17.4v5.6h5v14" />`,
};
---

<svg
  viewBox="0 0 48 48"
  fill="none"
  stroke="currentColor"
  stroke-width="4"
  stroke-linecap="round"
  stroke-linejoin="round"
  aria-hidden="true"
  class={classe}
  set:html={desenhos[rede]}
/>
```

(`stroke-width="4"` é mais grosso que os `2` de `SimboloComodidade` — foi a
espessura aprovada pela autora no mockup comparativo pra esse conjunto de
ícones especificamente.)

- [x] **Step 4: Reescrever `Footer.astro`**

Substituir o conteúdo inteiro de `template/src/components/Footer.astro`
por:

```astro
---
import { config } from '../lib/cliente';
import IconeRedeSocial from './IconeRedeSocial.astro';

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
      <p class="mt-1 max-w-xs text-sm">{config.slogan}</p>
      <p class="mt-4 text-sm">{config.localizacao.endereco}</p>
    </div>
    <div class="text-sm sm:justify-self-end lg:justify-self-start">
      <p class="font-mono text-xs tracking-widest text-espuma uppercase">Fale conosco</p>
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
          <p class="font-mono text-xs tracking-widest text-espuma uppercase">Siga a gente</p>
          <div class="mt-3 flex gap-4">
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

Nota: no `sm` (2 colunas), com `temRedeSocial` o bloco "Siga a gente" some
pra linha de baixo ocupando a coluna esquerda — só vira 3 colunas lado a
lado a partir do `lg`. É a mesma resposiva já usada em outros grids do
projeto (`sm`→`lg` como próximo salto), sem breakpoint novo.

- [x] **Step 5: Rodar o check de novo**

Run: `cd template && npm run check`
Expected: passa sem erros de tipo (import do componente novo, props
corretas).

- [x] **Step 6: Build dos 3 clientes existentes, nenhum deve quebrar**

Run:
```
cd template
CLIENTE=demo npm run build
CLIENTE=maravista npm run build
CLIENTE=lumehostel npm run build
```
(No PowerShell: `$env:CLIENTE = 'demo'; npm run build`, repetir por
cliente.)

Expected: os 3 builds passam. `demo` e `maravista` (que só têm Instagram)
devem gerar rodapé com o bloco "Siga a gente" contendo só o ícone de
Instagram (o campo já existe nos dois — ver `clientes/demo/config.json` e
`clientes/maravista/config.json`).

- [x] **Step 7: Commit**

```bash
git add template/src/lib/schema.ts template/src/components/IconeRedeSocial.astro template/src/components/Footer.astro
git commit -m "Adiciona bloco de redes sociais (Instagram/TikTok/Facebook) ao rodape"
```

---

### Task 2: Dados do LumeHostel e verificação visual

**Files:**
- Modify: `clientes/lumehostel/config.json` (bloco `contato`, linhas 74-78)

**Interfaces:**
- Consumes: `contato.tiktok` (definido na Task 1).

- [x] **Step 1: Adicionar o TikTok ao config do LumeHostel**

Em `clientes/lumehostel/config.json`, dentro de `"contato"`:

```json
  "contato": {
    "whatsapp": "5583988411745",
    "email": "lumehostel@gmail.com",
    "instagram": "lumehostel",
    "tiktok": "lumehostel"
  },
```

(Sem `facebook` — o Gabriel não tem. `instagram` já era `"lumehostel"`,
confere com `https://www.instagram.com/lumehostel/`; `tiktok` novo, a
partir de `https://www.tiktok.com/@lumehostel`.)

- [x] **Step 2: Build do LumeHostel**

Run: `cd template && CLIENTE=lumehostel npm run build`
Expected: passa sem erros.

- [x] **Step 3: Checagem visual no navegador**

Run: `cd template && CLIENTE=lumehostel npm run dev` (PowerShell:
`$env:CLIENTE = 'lumehostel'; npm run dev`), abrir a home no navegador e
rolar até o rodapé.

Expected: rodapé em 3 colunas (nome/endereço, Fale conosco, Siga a gente);
bloco "Siga a gente" com 2 ícones (Instagram, TikTok — traço grosso âmbar);
cada ícone abre a URL certa em nova aba (`instagram.com/lumehostel`,
`tiktok.com/@lumehostel`); em largura de mobile as 3 colunas empilham.

- [x] **Step 4: Parar o servidor de dev**

Run: `npx astro dev stop` (Astro 7 usa daemon persistente — ver nota no
`CLAUDE.md` sobre `astro dev stop`/`status`/`logs` substituindo
`Ctrl+C`).

- [x] **Step 5: Commit**

```bash
git add clientes/lumehostel/config.json
git commit -m "Adiciona TikTok do LumeHostel ao rodape"
```

## Critérios de conclusão do plano

- `npm run check` limpo em `template/`.
- Build de `demo`, `maravista` e `lumehostel` passando.
- Rodapé do LumeHostel confirmado visualmente com Instagram + TikTok,
  3 colunas, ícones com o traço grosso aprovado.
- `demo`/`maravista` continuam buildando com Instagram (agora como ícone,
  não mais texto) e sem TikTok/Facebook.
