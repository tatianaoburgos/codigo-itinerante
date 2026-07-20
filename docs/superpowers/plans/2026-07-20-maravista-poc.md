# Mar à Vista Hostel — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir o site completo do Mar à Vista Hostel (Barra, Salvador) como segundo cliente real do motor `template/`, com identidade derivada do logo existente (que não muda), para a autora abordar o dono e fechar uma permuta.

**Architecture:** Reaproveita o motor Astro one-page já existente (mesma composição de seções do LumeHostel). Duas correções pequenas e compartilhadas no motor (texto hardcoded de outro cliente; fallback de favicon para clientes sem SVG) + 4 símbolos artísticos novos na biblioteca compartilhada. Tudo o mais é específico do cliente: tema (`temas/maravista.css`), assets de marca derivados do PNG do logo (que não é vetorial — precisa de um recorte com chroma-key), fotos e `config.json`.

**Tech Stack:** Astro 5, Tailwind CSS 4, Zod, `astro:assets`, `@fontsource-variable/bricolage-grotesque` + `karla` (já instaladas). Processamento de imagem em Python + Pillow (já disponível no ambiente). Sem testes/linter no projeto — a validação de cada task é a build (`npm run build`) dos clientes `maravista` E `lumehostel` (garantir que a correção do motor não quebra o cliente existente) + conferência visual no dev server.

## Global Constraints

- **Nenhuma informação inventada sobre o hostel**: só conteúdo confirmado no Booking, Google Maps, TripAdvisor ou Instagram (`@maravistahostel`) do Mar à Vista.
- **O logo não muda.** Usado como está (`C:\Users\tatia\Downloads\marca mar a vista.png`); todo o resto (paleta, tipografia, símbolos) é derivado dele.
- Preços: nunca no site; política fixa `"consultar"`.
- Idioma: português brasileiro em conteúdo, docs e commits. Sem emojis em código.
- Comandos de build rodam dentro de `template/` (PowerShell): `$env:CLIENTE = 'maravista'; npm run build`.
- Toda task que mexe em arquivo compartilhado do motor termina com as builds de `maravista` E `lumehostel` passando.
- Sem contato ainda com o dono: WhatsApp de reservas já é real (`(71) 99983-8184` → `5571999838184`); e-mail usa placeholder óbvio (`@example.com`, mesmo padrão já usado em `clientes/demo/config.json`).

---

### Task 1: Motor — campo `localizacao.resumo` (remove o hardcode de João Pessoa)

**Files:**
- Modify: `template/src/lib/schema.ts:86-96` (bloco `localizacao`)
- Modify: `template/src/pages/index.astro:218-220`
- Modify: `clientes/lumehostel/config.json` (preserva o texto atual como dado, não como código)

**Interfaces:**
- Produces: `configClienteSchema.localizacao.resumo?: string` — frase curta opcional exibida ao fim da seção Localização.

- [ ] **Step 1: Adicionar o campo ao schema**

Em `template/src/lib/schema.ts`, dentro do objeto `localizacao` (depois de `comoChegar`, antes do `}),` de fechamento — linha 95-96 atual:

```ts
    comoChegar: z.array(z.string().min(1)),
    /** Frase curta opcional, exibida ao fim da seção Localização. */
    resumo: z.string().min(1).optional(),
  }),
```

- [ ] **Step 2: Trocar o texto fixo por `config.localizacao.resumo`**

Em `template/src/pages/index.astro`, substituir as linhas 218-220:

```astro
    <p class="mt-10 text-center text-lg">
      A poucos minutos da praia de Manaíra, no coração de João Pessoa.
    </p>
```

por:

```astro
    {
      config.localizacao.resumo && (
        <p class="mt-10 text-center text-lg">{config.localizacao.resumo}</p>
      )
    }
```

- [ ] **Step 3: Preservar o texto do LumeHostel como dado**

Em `clientes/lumehostel/config.json`, dentro do objeto `"localizacao"` (depois de `"comoChegar"`), adicionar:

```json
    "resumo": "A poucos minutos da praia de Manaíra, no coração de João Pessoa."
```

- [ ] **Step 4: Validar as duas builds**

Run: `cd template; $env:CLIENTE = 'lumehostel'; npm run build`
Expected: PASS, texto de João Pessoa continua no HTML gerado (`dist/index.html` contém "praia de Manaíra").

Run: `cd template; $env:CLIENTE = 'demo'; npm run build`
Expected: PASS (demo não tem `resumo` — o parágrafo simplesmente não aparece; campo é opcional).

- [ ] **Step 5: Commit**

```bash
git add template/src/lib/schema.ts template/src/pages/index.astro clientes/lumehostel/config.json
git commit -m "Motor: localizacao.resumo substitui texto hardcoded de Joao Pessoa"
```

---

### Task 2: Motor — favicon para clientes sem logo vetorial

**Contexto:** o Mar à Vista só tem um logo raster (PNG). `Layout.astro` hoje sempre emite um `<link rel="icon" type="image/svg+xml">` — usando o SVG do cliente se houver, senão o SVG genérico do motor (`/favicon.svg`) — mesmo quando o cliente só tem `faviconPng`. Isso faria o Mar à Vista mostrar o favicon genérico do motor ao lado do PNG correto, já que nunca terá `marca.favicon` (SVG).

**Files:**
- Modify: `template/src/layouts/Layout.astro:16` e `:63`

**Interfaces:**
- Consumes: `config.marca?.favicon`, `config.marca?.faviconPng` (schema já existente).

- [ ] **Step 1: Só cair no favicon genérico se o cliente não tiver NENHUM favicon próprio**

Em `template/src/layouts/Layout.astro`, trocar a linha 16:

```ts
const favicon = config.marca?.favicon ? marca(config.marca.favicon).src : '/favicon.svg';
```

por:

```ts
const temFaviconProprio = Boolean(config.marca?.favicon) || Boolean(config.marca?.faviconPng);
const favicon = config.marca?.favicon
  ? marca(config.marca.favicon).src
  : temFaviconProprio
    ? undefined
    : '/favicon.svg';
```

- [ ] **Step 2: Só renderizar o link SVG quando houver favicon a apontar**

Trocar a linha 63:

```astro
    <link rel="icon" type="image/svg+xml" href={favicon} />
```

por:

```astro
    {favicon && <link rel="icon" type="image/svg+xml" href={favicon} />}
```

- [ ] **Step 3: Validar que demo e lumehostel não mudam**

Run: `cd template; $env:CLIENTE = 'demo'; npm run build`
Expected: PASS. `dist/index.html` ainda contém `rel="icon" type="image/svg+xml" href="/favicon.svg"` (demo não define nem `favicon` nem `faviconPng` → cai no genérico, comportamento igual a antes).

Run: `cd template; $env:CLIENTE = 'lumehostel'; npm run build`
Expected: PASS. `dist/index.html` contém o link para `simbolo-completo-terracota.svg` (lumehostel define `marca.favicon` → primeiro branch, comportamento igual a antes).

- [ ] **Step 4: Commit**

```bash
git add template/src/layouts/Layout.astro
git commit -m "Motor: favicon PNG nao aciona mais o SVG generico quando cliente nao tem SVG proprio"
```

---

### Task 3: Motor — símbolos marítimos novos na biblioteca de comodidades

**Files:**
- Modify: `template/src/lib/schema.ts:28-37` (`simbolosComodidade`)
- Modify: `template/src/components/SimboloComodidade.astro:16-64` (`desenhos`)

**Interfaces:**
- Produces: `simbolosComodidade` ganha `'vista-mar' | 'ar-condicionado' | 'recepcao' | 'wifi'` além dos 8 existentes; `SimboloComodidade.astro` desenha os 4 novos no mesmo traço solto (viewBox 48x48, stroke, sem preenchimento exceto os pontinhos).

- [ ] **Step 1: Adicionar os 4 símbolos ao enum**

Em `template/src/lib/schema.ts`, trocar o array `simbolosComodidade` (linhas 28-37):

```ts
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
```

- [ ] **Step 2: Desenhar os 4 símbolos novos**

Em `template/src/components/SimboloComodidade.astro`, dentro do `Record<SimboloComodidade, string>` `desenhos`, adicionar (depois de `acolhedor`, antes do `};` de fechamento na linha 64):

```ts
  'vista-mar': `
    <circle cx="24" cy="18" r="7" />
    <path d="M24 7v3M13 18h3M35 18h3M16.5 10.5l2 2M31.5 10.5l-2 2" />
    <path d="M8 30c3-3 6-3 9 0s6 3 9 0 6-3 9 0 6 3 9 0" />
    <path d="M8 38c3-3 6-3 9 0s6 3 9 0 6-3 9 0 6 3 9 0" />`,
  'ar-condicionado': `
    <path d="M8 14c0-2.2 1.8-4 4-4h24c2.2 0 4 1.8 4 4v6c0 2.2-1.8 4-4 4H12c-2.2 0-4-1.8-4-4v-6Z" />
    <circle cx="14" cy="17" r="1.3" fill="currentColor" stroke="none" />
    <path d="M13 26c2 4 3 8 1 13M22 26c2 5 2.5 9 0 13M31 26c2 4 1.5 8-1 13" />`,
  recepcao: `
    <path d="M10 33h28" />
    <path d="M14 33c0-8 4.5-13 10-13s10 5 10 13" />
    <path d="M22 20v-4h4v4" />
    <circle cx="24" cy="14" r="1.6" fill="currentColor" stroke="none" />`,
  wifi: `
    <path d="M14 24c6-6 14-6 20 0" />
    <path d="M18.5 29.5c3.5-3.5 7.5-3.5 11 0" />
    <circle cx="24" cy="35" r="1.6" fill="currentColor" stroke="none" />`,
```

- [ ] **Step 3: Validar builds (símbolos ainda não usados em nenhum config)**

Run: `cd template; $env:CLIENTE = 'demo'; npm run build` — Expected: PASS.
Run: `cd template; $env:CLIENTE = 'lumehostel'; npm run build` — Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add template/src/lib/schema.ts template/src/components/SimboloComodidade.astro
git commit -m "Motor: simbolos maritimos novos (vista-mar, ar-condicionado, recepcao, wifi)"
```

---

### Task 4: Marca — recortar o logo raster (chroma-key + favicons)

**Contexto:** o único asset de marca é um PNG 240×251 com o emblema circular (aro branco, azul vivo, veleiro/gaivota) + a assinatura "Mar à Vista / Hostel / Salvador-Brasil" abaixo, tudo sobre um fundo sólido quase-preto opaco (RGB ≈ 12,16,20 — **não** é transparente). Medido diretamente no arquivo: aro branco entre y≈43 e y≈176, x≈37 e x≈220 (coluna central); o texto começa logo depois, em y≈177.

**Files:**
- Create: `clientes/maravista/marca/logo-original.png` (cópia intocada do arquivo recebido)
- Create: `clientes/maravista/marca/prepara_logo.py`
- Create (gerados pelo script): `clientes/maravista/marca/logo.png`, `icone.png`, `favicon-32.png`, `apple-touch-icon.png`

- [ ] **Step 1: Copiar o arquivo original para o repositório**

```bash
mkdir -p clientes/maravista/marca
cp "C:/Users/tatia/Downloads/marca mar a vista.png" "clientes/maravista/marca/logo-original.png"
```

- [ ] **Step 2: Escrever o script de recorte**

Create `clientes/maravista/marca/prepara_logo.py`:

```python
"""Recorta o logo raster do Mar a Vista (fundo solido opaco, sem alpha) em duas
pecas usaveis pelo motor: o lockup completo (circulo + assinatura) e o emblema
sozinho (para favicon/apple-touch-icon/divisor de secao). O fundo do arquivo
original e um quase-preto solido (RGB ~12,16,20) -- vira transparente por
chroma-key com transicao suave (evita halo duro na borda anti-aliased).

Uso: python prepara_logo.py (roda a partir desta pasta).
"""

from pathlib import Path

from PIL import Image

PASTA = Path(__file__).parent
ORIGINAL = PASTA / "logo-original.png"
COR_FUNDO = (12, 16, 20)
LIMITE_TRANSPARENTE = 25
LIMITE_OPACO = 55
# Caixa generosa em torno do aro branco (medido: x 37-220, y 43-176 no
# original 240x251), com margem de seguranca e parando antes do texto.
CAIXA_EMBLEMA = (20, 28, 232, 192)


def chroma_key(imagem: Image.Image) -> Image.Image:
    """Torna transparente todo pixel proximo de COR_FUNDO, com transicao suave."""
    rgba = imagem.convert("RGBA")
    pixels = rgba.load()
    largura, altura = rgba.size
    for y in range(altura):
        for x in range(largura):
            r, g, b, _ = pixels[x, y]
            distancia = (
                (r - COR_FUNDO[0]) ** 2 + (g - COR_FUNDO[1]) ** 2 + (b - COR_FUNDO[2]) ** 2
            ) ** 0.5
            if distancia <= LIMITE_TRANSPARENTE:
                alfa = 0
            elif distancia >= LIMITE_OPACO:
                alfa = 255
            else:
                alfa = round(
                    255 * (distancia - LIMITE_TRANSPARENTE) / (LIMITE_OPACO - LIMITE_TRANSPARENTE)
                )
            pixels[x, y] = (r, g, b, alfa)
    return rgba


def recortar_pelo_alfa(imagem: Image.Image) -> Image.Image:
    """Corta as margens totalmente transparentes."""
    caixa = imagem.getbbox()
    return imagem.crop(caixa) if caixa else imagem


def gerar_apple_touch_icon(emblema: Image.Image, tamanho: int, cor_fundo: str) -> Image.Image:
    """Compoe o emblema sobre um fundo solido quadrado (sem transparencia)."""
    fundo = Image.new("RGBA", (tamanho, tamanho), cor_fundo)
    reduzido = emblema.copy()
    reduzido.thumbnail((round(tamanho * 0.82), round(tamanho * 0.82)))
    x = (tamanho - reduzido.width) // 2
    y = (tamanho - reduzido.height) // 2
    fundo.paste(reduzido, (x, y), reduzido)
    return fundo.convert("RGB")


def main() -> None:
    original = Image.open(ORIGINAL)

    lockup = recortar_pelo_alfa(chroma_key(original))
    lockup.save(PASTA / "logo.png")

    emblema = recortar_pelo_alfa(chroma_key(original.crop(CAIXA_EMBLEMA)))
    emblema.save(PASTA / "icone.png")

    favicon = emblema.copy()
    favicon.thumbnail((32, 32))
    favicon.save(PASTA / "favicon-32.png")

    apple_touch_icon = gerar_apple_touch_icon(emblema, 180, "#0b2c55")
    apple_touch_icon.save(PASTA / "apple-touch-icon.png")

    print("Gerados: logo.png, icone.png, favicon-32.png, apple-touch-icon.png")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Rodar o script e conferir visualmente**

Run: `cd clientes/maravista/marca; python prepara_logo.py`
Expected: imprime a lista dos 4 arquivos gerados.

Abrir cada um dos 4 PNGs gerados (visualização de imagem) e confirmar:
- `logo.png`: círculo + veleiro/gaivota + assinatura completos, sem retângulo escuro ao redor, sem halo duro nas bordas.
- `icone.png`: só o emblema circular (sem nenhuma letra do texto "Mar à Vista/Hostel" cortada pela metade), fundo transparente.
- `favicon-32.png` e `apple-touch-icon.png`: emblema legível mesmo pequeno; o apple-touch-icon tem fundo azul-marinho sólido (sem transparência).

Se `icone.png` cortar uma borda do círculo ou pegar um pedaço do texto, ajustar `CAIXA_EMBLEMA` em `prepara_logo.py` e rodar de novo — os números acima são um ponto de partida medido, não o resultado final garantido.

- [ ] **Step 4: Commit**

```bash
git add clientes/maravista/marca
git commit -m "Marca Mar a Vista: recorte do logo raster (lockup + emblema + favicons)"
```

---

### Task 5: Tema `maravista.css`

**Contexto de cor:** amostrado diretamente do PNG do logo — azul vivo do círculo ≈ `rgb(2,108,218)`, azul-marinho da assinatura ≈ `rgb(2,42,94)`. O motor usa `--color-mare` tanto como cor de título (via `TituloSecao`, em quase toda seção) quanto como fundo forte (depoimentos + CTA final) — por isso `mare` precisa ser o azul **escuro** (marinho), não o vivo: um azul claro não teria contraste como texto de título sobre fundo claro. O azul vivo entra em `azulejo` (eyebrows/realces, texto pequeno, tolera mais saturação). `fitinha` (símbolos e destaques) usa um âmbar mais queimado que o dourado claro do LumeHostel, porque aqui o fundo é claro (creme/branco) e um dourado pastel teria pouco contraste — um problema que o `demo`/Lume não têm porque não usam essa cor para texto pequeno sobre fundo claro.

**Files:**
- Create: `template/src/styles/temas/maravista.css`

- [ ] **Step 1: Criar o arquivo do tema**

```css
/* Tema do cliente Mar a Vista Hostel. Paleta partindo do logo (que nao muda):
   azul-marinho da assinatura + azul vivo do circulo, sobre fundo claro
   (areia/branco) com acento em ambar queimado (sol do fim de tarde). Fontes:
   mesmo par de display/corpo do tema demo (Bricolage Grotesque + Karla), ja
   instaladas no projeto. Selecionado pela env CLIENTE via alias @tema. */
@import "@fontsource-variable/bricolage-grotesque";
@import "@fontsource-variable/karla";
@import "@fontsource-variable/spline-sans-mono";

@theme {
  --color-mare: #0b2c55;      /* azul-marinho do logo: titulos (TituloSecao) + blocos fortes (CTA/depoimentos) */
  --color-noite: #081120;     /* azul quase-preto: texto padrao do corpo e fundo do footer */
  --color-azulejo: #026cda;   /* azul vivo do circulo: eyebrows e realces sobre fundo claro */
  --color-sal: #ffffff;       /* branco: secao clara */
  --color-espuma: #fbf4e6;    /* areia: fundo geral da pagina */
  --color-fitinha: #c17f1b;   /* ambar queimado: simbolos e destaques (legivel sobre claro e escuro) */
  --color-zap: #25d366;       /* verde WhatsApp (fixo, funcional) */

  --font-display: "Bricolage Grotesque Variable", ui-sans-serif, system-ui, sans-serif;
  --font-corpo: "Karla Variable", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "Spline Sans Mono Variable", ui-monospace, monospace;
}

/* Depoimentos e CTA final (bg-mare = azul-marinho escuro): blockquote,
   figcaption e paragrafos do motor usam text-noite hardcoded (index.astro),
   que e ainda mais escuro que o mare e nao contrasta sobre ele. */
section.bg-mare .text-noite {
  color: var(--color-sal);
}
section.bg-mare .text-noite\/25 {
  color: rgb(255 255 255 / 0.25);
}
```

- [ ] **Step 2: Validar que a build do maravista roda** (ainda sem `config.json` — este passo só confirma que o CSS é sintaticamente válido; a build completa só passa depois da Task 7)

Run: `cd template; npx tsc --noEmit -p tsconfig.json 2>$null; echo done` — na verdade não há verificação isolada de CSS; pular a validação de build aqui e confirmar junto da Task 7.

- [ ] **Step 3: Commit**

```bash
git add template/src/styles/temas/maravista.css
git commit -m "Tema Mar a Vista: azul-marinho + azul vivo do logo, acento ambar queimado"
```

---

### Task 6: Conteúdo — fotos do hostel e da região

> Task de pesquisa/curadoria, não de código. Fonte de verdade: Booking, Google Maps, TripAdvisor e Instagram do Mar à Vista. NADA além disso — nenhuma foto de banco de imagens para o hostel em si.

**Files:**
- Create: `clientes/maravista/fotos/capa.jpg`, `dormitorio-misto.jpg`, `dormitorio-feminino.jpg`, `dormitorio-misto-6.jpg`
- Create: `clientes/maravista/fotos/regiao-farol-da-barra.jpg`, `regiao-porto-da-barra.jpg`, `regiao-praia-de-ondina.jpg`, `regiao-mam-bahia.jpg`, `regiao-elevador-lacerda.jpg`, `regiao-pelourinho.jpg`

- [ ] **Step 1: Fotos do hostel (Booking/Google Maps)**

Localizar "Mar à Vista Hostel" (Av. Oceânica, 171, Barra, Salvador) no Booking e no Google Maps. Baixar, das galerias publicadas pelo próprio estabelecimento (nunca foto de hóspede):

- `capa.jpg` — a melhor foto horizontal com vista do mar (fachada ou quarto com a janela/vista), para o hero em tela cheia.
- `dormitorio-misto.jpg` — foto do "Dormitório Misto".
- `dormitorio-feminino.jpg` — foto do "Dormitório Feminino".
- `dormitorio-misto-6.jpg` — foto do "Dormitório Misto — 6 Camas" (se não houver foto distinta desse quarto específico, reaproveitar a foto genérica do dormitório misto e anotar isso em `FONTES.md` — não inventar uma foto diferente).

Salvar como jpg, lado maior ≤ 1600px (redimensionar com Pillow se vier maior).

- [ ] **Step 2: Fotos livres da região (Wikimedia Commons)**

Para cada um dos 6 pontos abaixo, buscar no Wikimedia Commons, conferir licença livre (CC0/CC-BY/domínio público), baixar e salvar como `regiao-<slug>.jpg`:

| Arquivo | Ponto | Distância (TripAdvisor) |
|---|---|---|
| `regiao-farol-da-barra.jpg` | Farol da Barra | 300 m |
| `regiao-porto-da-barra.jpg` | Porto da Barra | 850 m |
| `regiao-praia-de-ondina.jpg` | Praia de Ondina | 2,4 km |
| `regiao-mam-bahia.jpg` | Museu de Arte Moderna da Bahia (Solar do Unhão) | 4,7 km |
| `regiao-elevador-lacerda.jpg` | Elevador Lacerda | 5 km |
| `regiao-pelourinho.jpg` | Pelourinho | 6 km |

- [ ] **Step 3: Registrar proveniência**

Anotar cada arquivo (origem, autor, licença, se exige atribuição) em `clientes/maravista/fotos/FONTES.md` — criado na Task 8, junto com os outros docs do cliente.

- [ ] **Step 4: Commit**

```bash
git add clientes/maravista/fotos
git commit -m "Fotos do Mar a Vista: hostel (Booking/Maps) e regiao (Wikimedia, licenca livre)"
```

---

### Task 7: Conteúdo — `config.json` completo do Mar à Vista

**Files:**
- Create: `clientes/maravista/config.json`

**Interfaces:**
- Consumes: schema da Task 1 e 3; fotos da Task 6; assets de marca da Task 4.

- [ ] **Step 1: Escrever o `config.json`**

```json
{
  "nome": "Mar à Vista Hostel",
  "marca": {
    "logo": "logo.png",
    "faviconPng": "favicon-32.png",
    "appleTouchIcon": "apple-touch-icon.png",
    "simbolo": "icone.png"
  },
  "slogan": "Mar à vista em todos os quartos",
  "descricaoSeo": "Mar à Vista Hostel, na Barra (Salvador): todos os quartos com vista pro mar, a 300 m do Farol da Barra. Reserve direto pelo WhatsApp.",
  "sobre": {
    "historia": "O Mar à Vista fica na Barra, em frente ao mar, a poucos passos do Farol e da praia do mesmo nome. É um hostel só para adultos, com dormitórios compartilhados com vista pro mar, ar-condicionado, e cozinha e recepção funcionando 24 horas. As avaliações públicas — 5,0 no TripAdvisor e cerca de 9,1 no Booking — destacam a localização, a limpeza e uma equipe que fala português, inglês e espanhol e está sempre pronta pra dar uma dica de passeio. É o tipo de lugar que também recebe bem grupos de amigos viajando juntos."
  },
  "acomodacoes": [
    {
      "nome": "Dormitório Misto",
      "capacidade": "Cama em beliche (dormitório compartilhado misto), 26 m²",
      "comodidades": ["Vista do mar", "Ar-condicionado", "Wi-Fi grátis", "Tomada perto da cama", "Banheiro compartilhado", "Jogos de tabuleiro/quebra-cabeças"],
      "fotos": [
        { "arquivo": "dormitorio-misto.jpg", "alt": "Dormitório misto do Mar à Vista Hostel" }
      ]
    },
    {
      "nome": "Dormitório Feminino",
      "capacidade": "Cama em beliche (dormitório compartilhado feminino), 24 m²",
      "comodidades": ["Vista do mar", "Ar-condicionado", "Banheiro privativo", "Wi-Fi grátis"],
      "fotos": [
        { "arquivo": "dormitorio-feminino.jpg", "alt": "Dormitório feminino do Mar à Vista Hostel" }
      ]
    },
    {
      "nome": "Dormitório Misto — 6 camas",
      "capacidade": "Dormitório misto com 6 camas em beliches",
      "comodidades": ["Vista do mar", "Ar-condicionado", "Wi-Fi grátis"],
      "fotos": [
        { "arquivo": "dormitorio-misto-6.jpg", "alt": "Dormitório misto de 6 camas do Mar à Vista Hostel" }
      ]
    }
  ],
  "precos": {
    "politica": "consultar"
  },
  "localizacao": {
    "endereco": "Av. Oceânica, 171 — Barra, Salvador/BA",
    "logradouro": "Av. Oceânica, 171",
    "bairro": "Barra",
    "cidade": "Salvador",
    "uf": "BA",
    "mapsEmbedUrl": "https://www.google.com/maps?q=Mar+a+Vista+Hostel,+Av+Oceanica+171,+Barra,+Salvador&output=embed",
    "comoChegar": [
      "Aeroporto Internacional de Salvador a cerca de 26 km",
      "Farol da Barra a 3 minutos a pé",
      "Praia do Farol da Barra a 300 m"
    ],
    "resumo": "A poucos passos do Farol da Barra, em Salvador."
  },
  "contato": {
    "whatsapp": "5571999838184",
    "email": "contato@maravistahostel.example.com",
    "instagram": "maravistahostel"
  },
  "comodidades": [
    { "nome": "Vista do mar em todos os quartos", "descricao": "Cada dormitório tem janela de frente para o mar da Barra.", "simbolo": "vista-mar" },
    { "nome": "Ar-condicionado", "descricao": "Em todos os dormitórios.", "simbolo": "ar-condicionado" },
    { "nome": "Recepção 24 horas", "simbolo": "recepcao" },
    { "nome": "Wi-Fi grátis", "descricao": "Sinal em toda a propriedade.", "simbolo": "wifi" },
    { "nome": "Cozinha compartilhada", "simbolo": "cozinha" },
    { "nome": "Jogos de tabuleiro e quebra-cabeças", "simbolo": "jogos" },
    { "nome": "Segurança 24 horas", "descricao": "Câmeras nas áreas comuns e extintores de incêndio." },
    { "nome": "Lounge e sala de TV compartilhados" }
  ],
  "regiao": [
    {
      "nome": "Farol da Barra",
      "descricao": "O farol mais famoso de Salvador, com museu náutico aberto à visitação.",
      "distancia": "300 m",
      "foto": { "arquivo": "regiao-farol-da-barra.jpg", "alt": "Farol da Barra, em Salvador" }
    },
    {
      "nome": "Porto da Barra",
      "descricao": "Praia urbana de águas calmas, uma das mais frequentadas de Salvador.",
      "distancia": "850 m",
      "foto": { "arquivo": "regiao-porto-da-barra.jpg", "alt": "Praia do Porto da Barra, em Salvador" }
    },
    {
      "nome": "Praia de Ondina",
      "descricao": "Orla urbana com vista para o Farol da Barra ao fundo.",
      "distancia": "2,4 km",
      "foto": { "arquivo": "regiao-praia-de-ondina.jpg", "alt": "Praia de Ondina, em Salvador" }
    },
    {
      "nome": "MAM Bahia",
      "descricao": "Museu de Arte Moderna, no Solar do Unhão, com vista para a Baía de Todos os Santos.",
      "distancia": "4,7 km",
      "foto": { "arquivo": "regiao-mam-bahia.jpg", "alt": "Museu de Arte Moderna da Bahia, no Solar do Unhão" }
    },
    {
      "nome": "Elevador Lacerda",
      "descricao": "Um dos cartões-postais de Salvador, liga a Cidade Alta à Cidade Baixa.",
      "distancia": "5 km",
      "foto": { "arquivo": "regiao-elevador-lacerda.jpg", "alt": "Elevador Lacerda, em Salvador" }
    },
    {
      "nome": "Pelourinho",
      "descricao": "Centro histórico de Salvador, tombado pela UNESCO como Patrimônio da Humanidade.",
      "distancia": "6 km",
      "foto": { "arquivo": "regiao-pelourinho.jpg", "alt": "Casario colorido do Pelourinho, em Salvador" }
    }
  ]
}
```

Preencher o `credito` de cada ponto de `regiao` (campo opcional) a partir do que for registrado em `fotos/FONTES.md` na Task 6, sempre que a licença da foto exigir atribuição — mesmo padrão do LumeHostel.

`depoimentos`, `destaques` e `vibe` ficam **de fora** desta primeira versão: são opcionais no schema, e ainda não temos avaliações com nome completo verificado nem fotos extras o bastante para sustentar essas seções com material real (ver `PENDENCIAS.md` na Task 8) — melhor não ter a seção do que forçar conteúdo fraco.

- [ ] **Step 2: Validar a build**

Run: `cd template; $env:CLIENTE = 'maravista'; npm run build`
Expected: PASS. Se falhar por foto ausente, conferir se todos os arquivos citados existem em `clientes/maravista/fotos/` (Task 6) e `clientes/maravista/marca/` (Task 4).

Run: `cd template; $env:CLIENTE = 'maravista'; npm run dev`
Conferir no navegador: hero com o logo e a vista do mar; as 3 acomodações; comodidades com os 4 símbolos novos + cozinha/jogos; seção "A região" com os 6 pontos; mapa; CTA final com o WhatsApp certo. Testar o botão do WhatsApp (deve abrir `wa.me/5571999838184`).

- [ ] **Step 3: Commit**

```bash
git add clientes/maravista/config.json
git commit -m "Conteudo completo do Mar a Vista: acomodacoes, comodidades e regiao"
```

---

### Task 8: Documentação do cliente

**Files:**
- Create: `clientes/maravista/marca.md`
- Create: `clientes/maravista/PENDENCIAS.md`
- Create: `clientes/maravista/fotos/FONTES.md`
- Create: `clientes/maravista/avaliacoes.md`

- [ ] **Step 1: `marca.md`**

```markdown
# Marca — Mar à Vista Hostel

Identidade visual do próprio hostel: **não recebemos um MIV**, só o arquivo
de logo (`marca/logo-original.png`, provavelmente exportado do Instagram ou
Google Maps). O logo **não é alterado** — usado como está; a paleta e a
tipografia do site são derivadas dele.

## Cores (amostradas diretamente do arquivo do logo)

| Papel | Hex | Uso no tema (`template/src/styles/temas/maravista.css`) |
|---|---|---|
| Azul-marinho (assinatura do logo) | `#0b2c55` (aprox.) | `--color-mare` |
| Azul quase-preto (derivado, mais escuro) | `#081120` | `--color-noite` |
| Azul vivo (círculo do logo) | `#026cda` (aprox.) | `--color-azulejo` |
| Âmbar queimado (escolha de paleta — sol do fim de tarde) | `#c17f1b` | `--color-fitinha` |

## Tipografia

Sem fonte própria no material recebido (logo usa lettering à mão, não uma
fonte digital). Escolhidas por decisão de design (brainstorm de 2026-07-20):

- Display (títulos): **Bricolage Grotesque Variable** — sans expressiva, mesma
  família já usada no tema `demo`.
- Corpo: **Karla Variable**.
- Mono (eyebrows/distâncias): **Spline Sans Mono Variable**.

## Assets derivados (`marca/`)

- `logo-original.png` — arquivo recebido, intocado.
- `logo.png` — lockup completo (círculo + assinatura), fundo transparente.
- `icone.png` — só o emblema circular, fundo transparente (divisor de seção,
  marca-d'água, fonte dos favicons).
- `favicon-32.png`, `apple-touch-icon.png` — gerados por `marca/prepara_logo.py`.
```

- [ ] **Step 2: `PENDENCIAS.md`**

```markdown
# Pendências — Mar à Vista Hostel

POC construída **sem contato ainda com o dono**, só com material público
(Booking, Google Maps, TripAdvisor, Instagram) — ver regra de ouro no
`CLAUDE.md`. Lista do que perguntar/pedir quando o contato acontecer.

## Pedir ao dono

- [ ] **Vídeo de drone** do Instagram (reels `DWBbxn7DtNW`) — pedir o arquivo
      com autorização de uso. Se vier, é candidato a hero em vídeo (hoje a
      hero é foto parada; vídeo é exceção à regra geral do motor, decisão da
      autora caso o material chegue).
- [ ] **Fotos em alta resolução** de quartos e áreas comuns — as fotos atuais
      vêm das galerias públicas do Booking/Google Maps, em baixa resolução.
- [ ] **E-mail de contato real** — hoje `contato@maravistahostel.example.com`
      (placeholder óbvio, mesmo padrão do `clientes/demo/config.json`).
- [ ] **Confirmar dados factuais**: os 3 tipos de dormitório e comodidades
      batem com a realidade atual do hostel? Política adults-only continua?
- [ ] **Avaliações com nome completo** para a seção de depoimentos — as
      avaliações públicas que encontramos (TripAdvisor) não tinham nome
      completo do autor; a seção ficou de fora desta versão por isso
      (ver `avaliacoes.md`).
- [ ] **Fotos extras** para uma seção "A vibe" (mosaico das áreas comuns) e
      até 2 destaques full-bleed — não incluídos nesta versão por falta de
      material distinto o bastante.

## Contexto sensível (não vai ao site — só para a autora saber antes de negociar)

Há reclamações públicas (Booking/TripAdvisor) sobre cobrança de day use e uso
do lobby antes do check-in. Não é um problema do site, mas vale saber antes
da conversa com o dono.
```

- [ ] **Step 3: `fotos/FONTES.md`**

Seguir exatamente o formato de `clientes/lumehostel/fotos/FONTES.md` (tabela
Arquivo/Origem/Autor/Licença/Atribuição exigida?), preenchendo com o que foi
de fato baixado na Task 6 — incluindo a observação, se aplicável, de que
`dormitorio-misto-6.jpg` reaproveita a foto do dormitório misto genérico por
falta de foto específica do quarto de 6 camas nas galerias públicas.

- [ ] **Step 4: `avaliacoes.md`**

```markdown
# Avaliações públicas do Mar à Vista Hostel

Levantamento em 2026-07-20 diretamente nas presenças públicas do hostel.

**Notas na data do levantamento:**

| Fonte | Nota | Volume |
|---|---|---|
| TripAdvisor | 5,0 (#26 de 204 hospedagens em Salvador) | 10 avaliações |
| Booking.com | ~9,1–9,2 | — |
| Booking.com (grupos) | 9,9 | — |

Duas avaliações do TripAdvisor foram encontradas no levantamento inicial, mas
**sem o nome completo do autor** (só descritor de data, ex. "visitante de
setembro de 2023") — por isso a seção de depoimentos ficou de fora desta
versão (schema exige `nome`). Trechos encontrados, para referência numa
próxima rodada de coleta (revisitar a aba de avaliações do TripAdvisor/Google
Maps para capturar o nome do autor):

1. "Passei 5 dias nesse hostel em Salvador e foi a melhor escolha que poderia
   ter feito."
2. "O hostel fica em frente ao mar da praia da Barra, apenas um quarteirão de
   distância do farol."

## Recomendação

Antes de adicionar a seção de depoimentos, revisitar TripAdvisor e Google Maps
coletando **nome + trecho + data** de 3-4 avaliações que cubram ângulos
distintos (localização, limpeza, atendimento, grupos) — mesmo padrão usado no
`avaliacoes.md` do LumeHostel.
```

- [ ] **Step 5: Commit**

```bash
git add clientes/maravista/marca.md clientes/maravista/PENDENCIAS.md clientes/maravista/fotos/FONTES.md clientes/maravista/avaliacoes.md
git commit -m "Docs do cliente Mar a Vista: marca, pendencias, fontes das fotos e avaliacoes"
```

---

### Task 9: Verificação final, deploy e atualização do CLAUDE.md

**Files:**
- Modify: `CLAUDE.md` (seção "Estado atual")

- [ ] **Step 1: Build dos dois clientes lado a lado**

Run: `cd template; $env:CLIENTE = 'maravista'; npm run build`
Expected: PASS.

Run: `cd template; $env:CLIENTE = 'lumehostel'; npm run build`
Expected: PASS (confirma que nenhuma das correções do motor quebrou o cliente existente).

Run: `cd template; npm run check`
Expected: PASS (sem erros de tipo).

- [ ] **Step 2: Conferência visual final no dev server**

Run: `cd template; $env:CLIENTE = 'maravista'; npm run dev`

Percorrer a página inteira e conferir contra `docs/diretrizes-design.md`: hero full-bleed, rolagem só vertical, nenhuma seção quebrada, símbolos com traço consistente, botão do WhatsApp funcionando, favicon do navegador mostrando o emblema do Mar à Vista (não o genérico do motor).

- [ ] **Step 3: Deploy — novo projeto Vercel**

Criar um projeto Vercel separado apontando para este repositório, com variável de ambiente `CLIENTE=maravista` (mesmo padrão do LumeHostel em produção). Confirmar a URL gerada (formato `maravista.vercel.app` ou similar) — é o link que a autora vai mandar para o dono do hostel.

- [ ] **Step 4: Atualizar `CLAUDE.md`**

Na seção "Estado atual", registrar: segundo cliente real (`clientes/maravista/`), construído como POC pré-contato a partir de material 100% público, com o logo do hostel mantido como recebido; link da spec (`docs/superpowers/specs/2026-07-20-maravista-poc-design.md`) e deste plano; URL de produção quando publicada; lembrete de que `PENDENCIAS.md` lista o que pedir ao dono quando o contato acontecer.

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: registra o Mar a Vista como segundo cliente real (POC pre-contato)"
```
