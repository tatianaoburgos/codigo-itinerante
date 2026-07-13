# LumeHostel one-page — redesign do motor e do site

Data: 2026-07-13. Aprovado pela autora em brainstorm.

## Objetivo

Transformar o site gerado pelo motor `template/` em uma **one-page com âncoras**,
dominada por fotografia, usando o LumeHostel como primeiro cliente do novo formato.
A one-page **substitui** a variação multipágina (decisão da autora): o motor passa a
gerar uma única página para todos os clientes.

## Regras de conteúdo (inegociáveis)

- **Nenhuma informação inventada sobre o hostel.** Só entra o que consta nas
  presenças públicas do LumeHostel: Booking, Google (Maps/avaliações) e Instagram.
- Fatos sobre a região (distâncias, nomes de pontos) devem ser verificáveis;
  sem opiniões atribuídas ao hostel.
- Política de preços inalterada: "consultar no WhatsApp", sem valores no site.

## Estrutura da página

Menu vira âncoras (`/#acomodacoes`, `/#comodidades`, `/#regiao`, `/#localizacao`)
+ botão WhatsApp (wa.me) no menu. Rotas `/acomodacoes`, `/sobre`, `/localizacao`
deixam de existir. Ordem de rolagem:

1. **Hero em tela cheia** — `capa.jpg` cobrindo a viewport; logo + slogan
   sobrepostos; marca-d'água grande e translúcida do símbolo ao fundo.
2. **Acomodações** — carrossel horizontal com CSS scroll-snap (sem biblioteca JS):
   cards de foto cheia com nome sobreposto na base e comodidades curtas do quarto.
3. **Comodidades** — evolução da seção "Diferenciais/Por que ficar aqui",
   expandida e ilustrada: cada comodidade com foto e 1–2 frases curtas.
   Itens (todos confirmados nas fontes públicas): coworking, cozinha compartilhada
   com café de cortesia, jardim com redes, churrasqueira, sala de jogos,
   depósito de bagagem, ar-condicionado + lockers.
4. **A região** — "Manaíra, João Pessoa" (inspiração estrutural:
   pousadacasadasflores.com.br/chapada-dos-veadeiros — só estrutura, sem copiar
   texto/imagem): ~5–6 pontos com foto e distância real do hostel — praia de
   Manaíra (~8 min a pé), orla/Bessa, pôr do sol no Jacaré, Centro Histórico,
   Farol do Cabo Branco, Estação Cabo Branco. Curadoria da Claude, cortável
   na revisão.
5. **Depoimentos** — 3–4 avaliações públicas reais (primeiro nome + origem,
   ex.: "via Booking"), estáticas no config.json.
6. **Localização** — mapa embed + "como chegar" (conteúdo já existente).
7. **CTA final** — bloco âmbar com marca-d'água do símbolo + botão WhatsApp.

Entre as seções: divisor com o símbolo do hostel pequeno e centralizado.

## Fotos

- **Do hostel**: extrair do Booking/Google Maps (fotos publicadas pelo próprio
  hostel; uso provisório até o Gabriel enviar originais em alta — registrar em
  PENDENCIAS.md com lista-guia do que fotografar).
- **Da região**: fotos com licença livre (Unsplash/Wikimedia), com crédito
  quando a licença exigir; crédito armazenado no config.json.

## Dados e motor

- Schema Zod (`template/src/lib/schema.ts`) ganha campos **opcionais** (para não
  quebrar o `demo`): `depoimentos[]` (texto, nome, fonte), `regiao[]` (nome,
  descrição curta, distância, foto, crédito), foto opcional por comodidade.
- As 4 páginas viram uma composição única em `index.astro`; componentes
  compartilhados continuam sendo a base (~80% reuso preservado).
- Seções sem dados no config (ex.: sem depoimentos) simplesmente não renderizam.

## Tema e tipografia

- `template/src/styles/temas/lumehostel.css`: **Fredoka Variable** em
  `--font-display` e `--font-corpo`. Arial Rounded MT Bold sai do stack —
  todos os visitantes veem o mesmo site.
- Símbolo âmbar mais presente: marca-d'água no hero e no CTA final,
  divisor entre seções.

## Notas para o Gabriel (PENDENCIAS.md)

1. **Depoimentos**: área importante do site, mas alterações futuras exigem
   manutenção (edição do config + novo deploy). Perguntar se ele quer manter.
2. **Fonte**: escolhemos a Fredoka por ser gratuita e fiel ao espírito
   arredondado do MIV; a Arial Rounded MT Bold é proprietária e ele tem a
   opção de comprar a licença web se quiser a fonte original no site.
3. **Fotos**: enviar originais em alta das áreas comuns (lista-guia incluída).

## Fora de escopo

- Sitemap, domínio, variações 2 e 3 (a decisão de substituir a variação 1
  pela one-page redefine o que "variações" significará; tratar depois).
- Qualquer integração de reservas/OTAs (decisão fechada do projeto).
