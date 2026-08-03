# Ícones de redes sociais no rodapé (design)

## Contexto

A autora pediu uma seção "Siga nossas redes sociais" com ícones de
Instagram, TikTok e Facebook, pra usar em qualquer cliente que tiver essas
redes. Hoje o Instagram já existe no schema (`config.contato.instagram`),
mas só aparece como link de texto (`@handle`) dentro da lista "Fale
conosco" do rodapé; TikTok e Facebook não existem no schema.

Decisão pensada como **capacidade do motor** (`template/`), reaproveitável
por qualquer cliente — não é exclusiva do LumeHostel. `site/` (site da
própria marca) fica fora desta rodada.

## Decisões fechadas (brainstorming com companheiro visual)

- **Escopo**: só `template/`; só as 3 redes pedidas (Instagram, TikTok,
  Facebook) — sem generalizar pra lista aberta de redes, sem caso de uso
  real pra isso ainda.
- **Estilo do ícone**: traço grosso arredondado, "desenhado à mão" — mesmo
  espírito visual dos símbolos de comodidade (`SimboloComodidade.astro`),
  não um ícone de biblioteca genérica. Cor: `fitinha` (acento âmbar/laranja
  do tema do cliente), sem fundo/badge.
- **Posição**: bloco novo "Siga a gente" no rodapé, separado de "Fale
  conosco". O rodapé ganha uma 3ª coluna **só quando existe pelo menos uma
  rede social preenchida**; sem nenhuma rede, o rodapé continua com as 2
  colunas de hoje. Em mobile todas as colunas empilham, como já acontece.
- Instagram sai da lista de texto "Fale conosco" e passa a viver só no
  bloco de ícones, junto com TikTok/Facebook.

## Design

### 1. Schema (`template/src/lib/schema.ts`)

Dentro de `contato`, dois campos novos opcionais, mesmo padrão do
`instagram` que já existe (guardam só o handle, não a URL inteira):

```ts
contato: z.object({
  whatsapp: z.string().regex(/^\d{12,13}$/, '...'),
  email: z.email(),
  instagram: z.string().optional(),
  tiktok: z.string().optional(),
  facebook: z.string().optional(),
}),
```

### 2. Footer (`template/src/components/Footer.astro`)

- Monta as 3 URLs a partir do handle, só se o campo existir:
  `https://instagram.com/{handle}`, `https://www.tiktok.com/@{handle}`,
  `https://www.facebook.com/{handle}`.
- `temRedeSocial = Boolean(linkInstagram || linkTiktok || linkFacebook)`.
- Grid do rodapé: `sm:grid-cols-2`, mais `lg:grid-cols-3` quando
  `temRedeSocial` for `true`.
- Novo bloco condicional "Siga a gente": rótulo (mesmo estilo do "Fale
  conosco", `font-mono text-xs tracking-widest uppercase`) + linha de
  ícones (só os presentes, na ordem Instagram → TikTok → Facebook), cada
  um um `<a>` com `target="_blank" rel="noopener noreferrer"` e
  `aria-label` (“Instagram”, “TikTok”, “Facebook” — não tem texto visível
  ao lado do ícone).

### 3. Ícones (SVG inline em `Footer.astro`)

Três SVGs customizados (`viewBox="0 0 24 24"`, `stroke-width` ~2.2,
`stroke-linecap`/`stroke-linejoin: round`, `fill: none`, cor via classe
`text-fitinha` + `stroke-current`), desenhados no mesmo espírito artístico
dos símbolos de comodidade — não copiados de uma biblioteca de ícones de
terceiros. Tamanho ~22-24px. Foco visível
(`focus-visible:outline-2 focus-visible:outline-offset-2
focus-visible:outline-fitinha`), mesmo padrão dos links de texto do
rodapé.

### 4. Dados do LumeHostel

`clientes/lumehostel/config.json` → `contato`:
- `instagram`: já existe (`"lumehostel"`) — confirmado contra
  `https://www.instagram.com/lumehostel/`, sem mudança.
- `tiktok`: novo, `"lumehostel"` (a partir de
  `https://www.tiktok.com/@lumehostel`).
- `facebook`: **não adicionado** — o Gabriel não tem Facebook.

`demo` e `maravista` não mudam (nenhum tem TikTok/Facebook hoje; o
Instagram de ambos continua funcionando, só muda de lugar/estilo no
rodapé).

## Fora de escopo

- `site/` (site da própria marca).
- Qualquer rede além de Instagram/TikTok/Facebook.
- Ícones de rede social em outro lugar do site além do rodapé (nav, hero,
  etc.).

## Critérios de conclusão

- `npm run check` passa em `template/`.
- `CLIENTE=demo` e `CLIENTE=maravista` buildam normalmente; rodapé continua
  em 2 colunas (só Instagram, sem TikTok/Facebook — mas note que o
  Instagram deles também migra pro bloco de ícones).
- `CLIENTE=lumehostel` builda com o rodapé em 3 colunas, bloco "Siga a
  gente" mostrando ícone de Instagram e TikTok (sem Facebook), linkando
  pras URLs corretas.
- Teste visual manual (`npm run dev`) confirmando o estilo do ícone e o
  layout responsivo (mobile empilhado, desktop 3 colunas).
