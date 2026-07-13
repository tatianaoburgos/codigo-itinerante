# LumeHostel — Redesign terracota/âmbar + conteúdo real — Plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Aplicar a identidade terracota/âmbar do MIV ao site do LumeHostel, com logo real, conteúdo real (Booking/Maps) e fotos do próprio hostel.

**Architecture:** Quase tudo vive no tema do cliente (`template/src/styles/temas/lumehostel.css`) e nos dados (`clientes/lumehostel/`). Única mudança no motor: suporte **opcional** a logo/favicon por cliente (campo novo no schema Zod + Nav + Layout), inerte para clientes sem o campo.

**Tech Stack:** Astro 5, Tailwind 4 (tokens `@theme`), Zod, PyMuPDF (extração do logo do PDF).

**Spec:** `docs/superpowers/specs/2026-07-12-lumehostel-redesign-conteudo-design.md`

## Global Constraints

- Não há testes/linter no projeto: a verificação é `CLIENTE=lumehostel npm run build` E `CLIENTE=demo npm run build` (regressão) dentro de `template/`, mais preview visual.
- Idioma de conteúdo/commits: português brasileiro. Sem emojis em código.
- Cores exatas: terracota `#c94520`, âmbar `#fcbe35`, texto escuro `#3a1509`, terracota profundo `#8f2d12`, creme `#fff3dc`. Verde WhatsApp `#25d366` não muda.
- Font stack começa com `"Arial Rounded MT Bold"` (não self-hostar — proprietária).
- Sem preço exato no conteúdo (`precos.politica: "consultar"`).
- WhatsApp/email reais ainda não existem: manter os placeholders atuais do config e o registro em `PENDENCIAS.md`.

---

### Task 1: Tema visual terracota/âmbar

**Files:**
- Modify: `template/src/styles/temas/lumehostel.css` (arquivo inteiro)

**Interfaces:**
- Produces: tokens `@theme` remapeados; nomes de token NÃO mudam (contrato com os componentes).

- [ ] **Step 1: Reescrever o tema**

Substituir o conteúdo de `template/src/styles/temas/lumehostel.css` por:

```css
/* Tema do cliente LumeHostel. Cores e conceito do Manual de Identidade Visual
   (Etna Comunicacao): terracota #c94520 dominante + ambar #fcbe35, como nas
   paginas do proprio MIV. Fonte auxiliar do MIV (Arial Rounded MT Bold,
   proprietaria) entra primeiro no stack; quem nao a tiver ve as substitutas
   livres arredondadas. Selecionado pela env CLIENTE via alias @tema. */
@import "@fontsource-variable/fredoka";
@import "@fontsource-variable/nunito";
@import "@fontsource-variable/spline-sans-mono";

@theme {
  --color-mare: #fcbe35;      /* blocos fortes (hero/CTA): ambar */
  --color-noite: #3a1509;     /* texto escuro: marrom profundo */
  --color-azulejo: #8f2d12;   /* links/realces sobre fundos claros */
  --color-sal: #fff3dc;       /* neutro claro: creme */
  --color-espuma: #c94520;    /* fundo geral: terracota */
  --color-fitinha: #fcbe35;   /* destaque: ambar */
  --color-zap: #25d366;       /* verde WhatsApp (fixo, funcional) */

  --font-display: "Arial Rounded MT Bold", "Fredoka Variable", ui-sans-serif, system-ui, sans-serif;
  --font-corpo: "Arial Rounded MT Bold", "Nunito Variable", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "Spline Sans Mono Variable", ui-monospace, monospace;
}

/* Ajustes exclusivos do LumeHostel: texto padrao branco sobre terracota;
   blocos ambar e cards claros voltam ao texto escuro. */
body {
  color: #ffffff;
}

.bg-mare,
.bg-sal,
.bg-white {
  color: var(--color-noite);
}

header.border-b {
  border-color: #8f2d1266;
  background: #c94520;
}

header.border-b a {
  color: #ffffff;
}

section.bg-mare {
  background: linear-gradient(135deg, #fcbe35 0%, #f0a81c 100%);
}

footer.bg-noite {
  background: #8f2d12;
  color: #ffffff;
}

.rounded-xl {
  border-radius: 1rem;
}

.bg-white {
  background: #fff3dc;
  border: 1px solid #8f2d1233;
}

.font-display {
  letter-spacing: -0.01em;
}
```

Observação: os componentes usam utilitárias como `text-noite`, `text-mare`,
`hover:text-azulejo` em lugares que agora ficam sobre terracota. Depois de
buildar, inspecionar o preview e ajustar NESTE arquivo (nunca nos componentes)
os casos ilegíveis — p.ex. `header.border-b a { color: #fff }` acima já cobre o
nav. É esperado iterar 2–3 vezes olhando o site.

- [ ] **Step 2: Buildar os dois clientes**

```bash
cd template
CLIENTE=lumehostel npm run build
CLIENTE=demo npm run build
```
Expected: ambos terminam sem erro.

- [ ] **Step 3: Conferir contraste no preview**

Dev server já roda em `http://localhost:4321/` (CLIENTE=lumehostel). Abrir as 4
páginas (`/`, `/acomodacoes`, `/sobre`, `/localizacao`) e verificar: nenhum
texto ilegível; branco sobre terracota; escuro sobre âmbar/creme. Ajustar
overrides conforme a observação do Step 1 até passar.

- [ ] **Step 4: Commit**

```bash
git add template/src/styles/temas/lumehostel.css
git commit -m "Tema LumeHostel: paleta terracota/ambar do MIV e stack com Arial Rounded"
```

---

### Task 2: Extrair o logo do PDF em SVG (âmbar e terracota)

**Files:**
- Create: `clientes/lumehostel/marca/logo-ambar.svg` (símbolo + wordmark, âmbar — para fundo terracota)
- Create: `clientes/lumehostel/marca/logo-terracota.svg` (idem, terracota — para fundo âmbar)
- Create: `clientes/lumehostel/marca/simbolo-ambar.svg` (só o símbolo "lume" — favicon)
- Fonte: `C:\Users\tatia\Downloads\lume.pdf` (página 3 tem as variantes em âmbar sobre terracota)

**Interfaces:**
- Produces: os 3 SVGs acima, com `viewBox` justo ao desenho e cor única de preenchimento. Task 3 e 4 referenciam esses nomes de arquivo.

- [ ] **Step 1: Instalar PyMuPDF e exportar a página 3 como SVG**

```bash
pip install pymupdf
python - <<'EOF'
import pymupdf
doc = pymupdf.open(r"C:\Users\tatia\Downloads\lume.pdf")
page = doc[2]  # pagina 3: variantes ambar sobre terracota
svg = page.get_svg_image()
open(r"C:\Users\tatia\codigo-itinerante\clientes\lumehostel\marca\pagina3.svg", "w", encoding="utf-8").write(svg)
print("ok", page.rect)
EOF
```
Expected: `ok Rect(...)` e o arquivo `pagina3.svg` criado. (Criar a pasta `clientes/lumehostel/marca/` antes.)

- [ ] **Step 2: Recortar o logo do SVG da página**

Abrir `pagina3.svg`, identificar o grupo de paths do logo horizontal grande
(símbolo + LUMEHOSTEL). Criar `logo-ambar.svg` contendo só esses paths, com
`viewBox` ajustado ao bounding box do desenho e `fill="#fcbe35"` em todos os
paths. Se os paths vierem como imagem rasterizada (sem vetores), cair no plano
B: renderizar a página em alta resolução e recortar PNG:

```python
pix = page.get_pixmap(dpi=600)
pix.save("pagina3.png")  # recortar o logo com PIL e salvar logo-ambar.png
```
(no plano B, os arquivos passam a ser .png e os passos seguintes usam .png)

- [ ] **Step 3: Gerar as variantes**

- `logo-terracota.svg`: cópia de `logo-ambar.svg` com `fill="#c94520"`.
- `simbolo-ambar.svg`: só os paths do símbolo (asterisco/lume), viewBox quadrado, `fill="#fcbe35"`.

- [ ] **Step 4: Verificar visualmente**

Abrir os 3 SVGs no navegador (`file:///...`) e comparar com a página 3 do PDF.
Expected: desenho idêntico, cor certa, sem restos da página.

- [ ] **Step 5: Commit**

```bash
git add clientes/lumehostel/marca/
git commit -m "Extrai logo e simbolo do LumeHostel do MIV em SVG (ambar e terracota)"
```

---

### Task 3: Motor — logo e favicon opcionais por cliente

**Files:**
- Modify: `template/src/lib/schema.ts` (acrescentar campo `marca` opcional)
- Modify: `template/src/lib/fotos.ts` (glob passa a cobrir `marca/*.svg`)
- Modify: `template/src/components/Nav.astro` (renderizar logo se houver)
- Modify: `template/src/layouts/Layout.astro:31` (favicon por cliente se houver)

**Interfaces:**
- Consumes: SVGs da Task 2.
- Produces: campo opcional no config:
  ```json
  "marca": { "logo": "logo-ambar.svg", "favicon": "simbolo-ambar.svg" }
  ```
  e helper `marca(arquivo: string): ImageMetadata` em `fotos.ts`.

- [ ] **Step 1: Schema — campo `marca` opcional**

Em `template/src/lib/schema.ts`, adicionar antes de `configClienteSchema`:

```ts
/** Arquivos de marca do cliente (pasta `marca/`), todos opcionais. */
export const marcaSchema = z.object({
  logo: z.string().min(1).optional(),
  favicon: z.string().min(1).optional(),
});
```

e dentro de `configClienteSchema`, após `nome`:

```ts
  marca: marcaSchema.optional(),
```

- [ ] **Step 2: fotos.ts — carregar também `marca/*.svg`**

Acrescentar em `template/src/lib/fotos.ts` (mesmo padrão do glob existente):

```ts
const modulosMarca = import.meta.glob<{ default: ImageMetadata }>(
  '../../../clientes/*/marca/*.svg',
  { eager: true },
);

const marcaDoCliente = new Map<string, ImageMetadata>(
  Object.entries(modulosMarca)
    .filter(([caminho]) => caminho.includes(`/clientes/${clienteAtivo}/marca/`))
    .map(([caminho, modulo]) => [caminho.split('/').pop()!, modulo.default]),
);

/** Resolve um arquivo de `marca/` do cliente ativo (logo, favicon). */
export function marca(arquivo: string): ImageMetadata {
  const meta = marcaDoCliente.get(arquivo);
  if (!meta) {
    throw new Error(`Arquivo de marca "${arquivo}" nao encontrado em clientes/${clienteAtivo}/marca/`);
  }
  return meta;
}
```

- [ ] **Step 3: Nav — logo no lugar do nome quando existir**

Em `template/src/components/Nav.astro`, no frontmatter:

```ts
import { marca } from '../lib/fotos';

const logo = config.marca?.logo ? marca(config.marca.logo) : undefined;
```

e trocar o conteúdo do `<a href="/">` (linhas 19–24) por:

```astro
    <a
      href="/"
      class="font-display text-xl font-bold text-mare focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-azulejo"
    >
      {logo ? <img src={logo.src} alt={config.nome} class="h-9 w-auto" /> : config.nome}
    </a>
```

- [ ] **Step 4: Layout — favicon por cliente**

Em `template/src/layouts/Layout.astro`, no frontmatter:

```ts
import { marca } from '../lib/fotos';

const favicon = config.marca?.favicon ? marca(config.marca.favicon).src : '/favicon.svg';
```

e a linha 31 vira:

```astro
    <link rel="icon" type="image/svg+xml" href={favicon} />
```

- [ ] **Step 5: Regressão — demo builda sem o campo**

```bash
cd template && CLIENTE=demo npm run build
```
Expected: PASS (demo não tem `marca`, caminho opcional inerte).

- [ ] **Step 6: Ativar no config do LumeHostel e buildar**

Em `clientes/lumehostel/config.json`, após `"nome"`:

```json
  "marca": { "logo": "logo-ambar.svg", "favicon": "simbolo-ambar.svg" },
```

```bash
CLIENTE=lumehostel npm run build
```
Expected: PASS. No preview, logo no header e favicon na aba.

- [ ] **Step 7: Commit**

```bash
git add template/src/lib/schema.ts template/src/lib/fotos.ts template/src/components/Nav.astro template/src/layouts/Layout.astro clientes/lumehostel/config.json
git commit -m "Motor: logo e favicon opcionais por cliente; ativa no LumeHostel"
```

---

### Task 4: Conteúdo real no config.json

**Files:**
- Modify: `clientes/lumehostel/config.json` (todo o conteúdo)
- Modify: `clientes/lumehostel/PENDENCIAS.md` (atualizar o que segue pendente)

**Interfaces:**
- Consumes: schema da Task 3 (campo `marca` já presente no arquivo).
- Produces: config sem `[PROVISORIO]`, exceto contato (WhatsApp/email fake mantidos).

- [ ] **Step 1: Reescrever o config com os dados levantados**

Dados de referência (Booking/agregadores, 2026-07-12): endereço Av. Pombal,
1745 — Manaíra, João Pessoa - PB, 58038-242; Praia de Manaíra a ~8 min a pé;
acomodações: dormitório feminino (4 e 6 camas), dormitório misto (6 e 8 camas),
quarto duplo, suíte standard — todos com ar-condicionado, lockers, tomadas
individuais e toalhas; comodidades gerais: coworking ergonômico, cozinha
compartilhada com café de cortesia, Wi-Fi, jardim com redes, churrasqueira,
sala de jogos, depósito de bagagem; sem café da manhã incluso; Instagram
`lumehostel`. Conceito do MIV para o "sobre": Segurança, Iluminação, Energia
Recarregada, Porto Seguro; tom acolhedor, para nômades digitais, sem clima de
festa. Estruturar em 4 acomodações (Dormitório Misto, Dormitório Feminino,
Quarto Duplo, Suíte Standard) reutilizando por ora as fotos existentes
(`quarto-1.jpg` nos dormitórios, `suite-1.jpg` no duplo/suíte — Task 5 troca).
`mapsEmbedUrl`: gerar embed de "LumeHostel, Av. Pombal 1745, Manaíra, João
Pessoa" (formato `https://www.google.com/maps?q=...&output=embed`).
`comoChegar`: aeroporto ~18 km, rodoviária ~9 km, praia de Manaíra a pé.
Manter `precos.politica: "consultar"` e o bloco `contato` atual (fake) — a
troca real é do Gabriel.

- [ ] **Step 2: Validar pelo build e conferir no preview**

```bash
cd template && CLIENTE=lumehostel npm run build
```
Expected: PASS (Zod valida). Conferir as 4 páginas no preview: nada de
`[PROVISORIO]` visível, mapa apontando para Manaíra.

- [ ] **Step 3: Atualizar PENDENCIAS.md**

Reescrever a lista: feito (endereço, acomodações, sobre, atividades, mapa,
marca); pendente do Gabriel (WhatsApp, email, domínio, confirmação dos textos,
fotos em alta / autorização de uso das fotos do Booking-Maps).

- [ ] **Step 4: Commit**

```bash
git add clientes/lumehostel/config.json clientes/lumehostel/PENDENCIAS.md
git commit -m "Conteudo real do LumeHostel a partir do Booking e Google Maps"
```

---

### Task 5: Fotos reais do hostel

**Files:**
- Modify: `clientes/lumehostel/fotos/capa.jpg`, `quarto-1.jpg`, `suite-1.jpg` (+ novas fotos por acomodação, se houver material)
- Modify: `clientes/lumehostel/config.json` (arquivos/alt das fotos novas)

**Interfaces:**
- Consumes: config da Task 4.

- [ ] **Step 1: Colher URLs das fotos públicas do hostel no Google Maps**

Via Claude in Chrome: abrir `https://www.google.com/maps/search/lume+hostel+joão+pessoa`,
entrar no perfil do hostel, abrir a galeria de fotos e extrair as URLs
`https://lh3.googleusercontent.com/p/...` (sem query string — o filtro da
extensão não bloqueia). Pedir tamanho grande trocando o sufixo por `=w1600`.

- [ ] **Step 2: Baixar e mapear**

```bash
curl -sL "<url>=w1600" -o clientes/lumehostel/fotos/capa.jpg
```
Mapear: fachada/área social → `capa.jpg`; dormitório → `quarto-1.jpg`;
quarto duplo/suíte → `suite-1.jpg`; extras boas → `dorm-feminino-1.jpg` etc.
Atualizar `fotos`/`alt` no config para descrever a foto real.

**Fallback** (se o Maps não tiver fotos utilizáveis): a usuária salva
manualmente as do Booking na pasta `fotos/`; último recurso, Unsplash/Pexels
temático (quarto com beliche, suíte, área social) conforme a spec.

- [ ] **Step 3: Buildar e conferir**

```bash
cd template && CLIENTE=lumehostel npm run build
```
Expected: PASS (`fotos.ts` derruba a build se algum arquivo do config faltar).
Preview: fotos reais nas 4 páginas, hero com a capa nova.

- [ ] **Step 4: Commit**

```bash
git add clientes/lumehostel/fotos/ clientes/lumehostel/config.json
git commit -m "Fotos reais do LumeHostel nas acomodacoes e na capa"
```

---

### Task 6: Verificação final e estado do projeto

**Files:**
- Modify: `CLAUDE.md` (parágrafo "Estado atual" sobre o LumeHostel)

- [ ] **Step 1: Verificação de ponta a ponta**

```bash
cd template
CLIENTE=lumehostel npm run build
CLIENTE=demo npm run build
```
Expected: ambos PASS. No preview do lumehostel, passar pelas 4 páginas:
paleta terracota/âmbar, logo no header, favicon, fotos reais, textos reais,
mapa certo, botão WhatsApp visível (ainda com número placeholder).

- [ ] **Step 2: Atualizar CLAUDE.md**

No parágrafo do LumeHostel em "Estado atual", trocar a descrição de "esqueleto
com conteúdo [PROVISORIO]" por: tema terracota/âmbar do MIV aplicado, logo real
extraído do PDF, conteúdo baseado nas presenças online (Booking/Maps); pendente
do Gabriel: WhatsApp/email reais, domínio e validação dos textos/fotos.

- [ ] **Step 3: Commit final**

```bash
git add CLAUDE.md
git commit -m "Atualiza estado do LumeHostel no CLAUDE.md"
```
