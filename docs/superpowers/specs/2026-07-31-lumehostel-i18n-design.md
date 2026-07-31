# Site bilíngue (pt/en) — motor + LumeHostel (design)

## Contexto

A autora pediu um site em inglês para o LumeHostel, com alternador de idioma
no Nav. Investimento pensado como **capacidade do motor** (`template/`),
reaproveitável por qualquer cliente futuro — mas **ativada nesta rodada só
para o LumeHostel**; `demo`, `maravista` e o site da marca (`site/`) não
mudam.

Levantamento no código confirmou que hoje não existe nenhuma infraestrutura
de idioma: `template/src/layouts/Layout.astro` tem `lang="pt-BR"` e
`og:locale` fixos, e o `config` do cliente ativo é carregado **uma vez**, no
import de `template/src/lib/cliente.ts`, e importado direto (sem prop) por
~9 componentes (`Hero`, `Nav`, `Footer`, `BotaoWhatsApp`, `Layout`,
`Acomodacoes`, `pages/index.astro`). Bilíngue de verdade exige traduzir dois
tipos de texto diferentes: o conteúdo do cliente (`config.json`) e o texto
fixo cravado nos componentes do motor (títulos de seção, rótulos de menu,
"Reserve pelo WhatsApp", `aria-label`s).

Precificação do escopo adicional (conversa em separado, não faz parte deste
spec): somar ao valor de referência de R$3.000 do modelo de permuta.

## Decisões fechadas nesta sessão

- **Depoimentos**: traduzidos, com nota discreta abaixo da citação ("Traduzido
  do português") — mantém a prova social sem fingir que o hóspede escreveu em
  inglês.
- **Autoria da tradução**: a autora (via Claude) traduz o conteúdo já aprovado
  em pt; ela revisa por seção antes de publicar. Não é conteúdo novo — é
  tradução fiel do que já existe.
- **Alternador de idioma no Nav**: texto simples "PT / EN", mesmo estilo
  tipográfico do resto do Nav (`font-mono`, como os eyebrows de seção). Sem
  bandeira — entraria em conflito direto com a diretriz do projeto de nunca
  usar ícone genérico/literal (`docs/diretrizes-design.md`), e bandeira dos
  EUA especificamente é uma escolha tecnicamente estranha pra representar
  "inglês".
- **URL**: `/en/` (prefixo de rota), não subdomínio — usa o roteamento i18n
  nativo do Astro, sem configuração extra de DNS.
- **Abordagem técnica**: união de tipos no schema (`string` **ou**
  `{ pt, en }`) dentro do próprio `config.json`, não um arquivo
  `config.en.json` separado — evita o risco de dois arquivos desalinharem
  (ex.: ordem diferente em `regiao`) e mantém a tradução ao lado do original
  no mesmo arquivo, mais fácil de revisar.

## Design

### 1. Roteamento (`astro.config.mjs`)

```js
i18n: {
  locales: ['pt', 'en'],
  defaultLocale: 'pt',
  routing: { prefixDefaultLocale: false },
}
```

`/` continua servindo pt sem prefixo (zero mudança de URL para os clientes
atuais); `/en/` serve inglês. O corpo da página, hoje inteiro em
`template/src/pages/index.astro`, é extraído para um componente
compartilhado `template/src/components/PaginaInicial.astro`, renderizado
tanto por `pages/index.astro` (pt) quanto por um novo `pages/en/index.astro`
— a estrutura da página não é duplicada, só a casca da rota. Dentro de
`PaginaInicial.astro`, `Astro.currentLocale` resolve o idioma da rota atual.

### 2. Ativação por cliente

Campo novo e opcional no schema, `idiomasDisponiveis: z.array(z.enum(['pt',
'en'])).optional()`. Ausente = comportamento de hoje (só pt), sem mudar
`demo` nem `maravista`. Só `clientes/lumehostel/config.json` ganha
`"idiomasDisponiveis": ["pt", "en"]`.

Em `pages/en/index.astro`: se o cliente ativo não tiver `"en"` na lista, a
rota redireciona para `/` (`Astro.redirect('/', 302)`). A rota `/en/`
portanto existe no build de qualquer cliente, mas só funciona para quem
declarou o campo. O alternador PT/EN no `Nav` só é renderizado quando
`idiomasDisponiveis` tem mais de um idioma.

### 3. Schema (`lib/schema.ts`)

Novo tipo:

```ts
const campoLocalizavel = z.union([
  z.string().min(1),
  z.object({ pt: z.string().min(1), en: z.string().min(1) }),
]);
```

Aplicado aos campos de prosa: `slogan`, `descricaoSeo`, `sobre.historia`,
`acomodacao.nome`/`capacidade`/`comodidades[]`, `comodidade.nome`/`descricao`,
`pontoRegiao.nome`/`descricao`, `depoimento.texto`,
`localizacao.comoChegar[]`/`resumo`. Ficam **fora** (seguem string simples):
nomes de arquivo, telefone, e-mail, CEP/UF/cidade/logradouro, `credito` de
foto, e `nome`/`fonte` do depoimento (nome de pessoa real não se traduz).

Como a união aceita string solta, **nenhum config existente muda de forma**
— `demo` e `maravista` continuam válidos sem qualquer edição. Um helper
`t(campo, locale)` (novo `template/src/lib/i18n.ts`) resolve o valor certo:
se o campo for string, retorna direto (mesmo valor nos dois idiomas); se for
`{pt, en}`, retorna a chave do locale atual.

### 4. Texto fixo do motor

Dicionário novo, `template/src/lib/textos.ts`, formato `{ pt: {...}, en:
{...} }`, cobrindo títulos/eyebrows de seção, rótulos do Nav, `aria-label`s
de abrir/fechar menu, "Fale conosco" do rodapé, rótulo padrão do
`BotaoWhatsApp` ("Reserve pelo WhatsApp"), texto do CTA final. Acessado via
`textoMotor(chave, locale)`, exportado do mesmo `lib/i18n.ts`. Ambos os
helpers (`t` e `textoMotor`) usam `Astro.currentLocale ?? 'pt'`.

### 5. Componentes tocados

`Hero`, `Nav`, `Footer`, `BotaoWhatsApp`, `Layout`, `Acomodacoes`,
`PaginaInicial` (novo, corpo extraído de `index.astro`).

- **Nav**: alternador "PT / EN" linkando raiz-a-raiz (`/` ↔ `/en/`) — sem
  tentar preservar âncora de rolagem, já que os IDs de seção (`#acomodacoes`
  etc.) não são traduzidos, são só identificadores internos.
- **Layout**: `lang` dinâmico (`pt-BR`/`en`), `og:locale` dinâmico
  (`pt_BR`/`en_US`), `<link rel="alternate" hreflang="...">` para as duas
  versões, JSON-LD (`description`) traduzido via `t()`.
- **Depoimentos** (dentro de `PaginaInicial`): nota "Traduzido do português"
  abaixo da citação, só na versão `/en/`.

### 6. Regra de erro

Se `idiomasDisponiveis` inclui `"en"`, todo campo que usar a forma `{pt,
en}` exige as duas chaves — o schema Zod não aceita objeto parcial, então a
build quebra se faltar uma tradução (mesmo princípio já usado hoje para foto
referenciada inexistente ou WhatsApp fora do formato). Um campo pode
continuar como string solta mesmo num cliente bilíngue, se a autora decidir
não traduzir aquele texto específico (ex.: endereço) — não é obrigatório
envolver tudo em `{pt, en}`.

## Fora de escopo

- `demo`, `maravista`, `site/` (site da marca) — nenhuma mudança de
  conteúdo ou comportamento.
- Tradução de IDs de âncora/seção (`#acomodacoes` etc.) — permanecem iguais
  nos dois idiomas.
- Qualquer forma de detecção automática de idioma do navegador
  (`Accept-Language`) — a troca é manual, via o alternador no Nav.
- Domínio/subdomínio dedicado para a versão em inglês.

## Critérios de conclusão

- `npm run check` passa em `template/`.
- `CLIENTE=demo npm run build` e `CLIENTE=maravista npm run build` continuam
  passando sem alteração de output; visitar `/en/` nesses builds redireciona
  para `/`.
- `CLIENTE=lumehostel npm run build` gera `dist/index.html` (pt) e
  `dist/en/index.html` (en) com conteúdo traduzido, incluindo depoimentos
  com a nota de tradução.
- Alternador "PT / EN" visível no Nav do LumeHostel, ausente no `demo` e no
  `maravista`.
- `hreflang` presente nas duas versões do LumeHostel.
- Teste manual no navegador: clicar o alternador troca de página mantendo o
  visual, conteúdo e metadados (title/description/JSON-LD) no idioma certo.
