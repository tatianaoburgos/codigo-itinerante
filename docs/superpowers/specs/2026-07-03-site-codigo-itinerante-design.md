# Spec — Site da marca Código Itinerante

Design validado em 2026-07-03. Landing page do projeto, dirigida a donos de hostel/pousada,
com o objetivo único de **passar credibilidade e profissionalismo** para viabilizar a
permuta site-por-estadia. Sem portfólio na v1: **o capricho do próprio site é a prova de
qualidade** até o LumeHostel entrar como case real.

Identidade visual: seguir o MIV (`docs/miv.md`), em especial §5 "Site do projeto".
Fonte primária dos textos: material escrito pela autora em 2026-07-02/03 (respostas ao
questionário de marca — citações abaixo).

---

## 1. Decisões fechadas

| Decisão | Escolha |
|---|---|
| Formato | **Uma página corrida** (landing única, menu âncora opcional) |
| Ordem narrativa | **Manifesto abre a história** (hero → manifesto → dor → proposta → escopo → como funciona → quem sou eu → CTA) |
| CTA | **WhatsApp direto** — botão wa.me com mensagem pré-preenchida |
| Portfólio | **Ausente na v1**; LumeHostel entra como case real quando pronto |
| Presença pessoal | **Nome completo + foto + credenciais + LinkedIn** (foto única, abaixo da dobra — MIV §5) |
| Transparência da permuta | **Processo + escopo publicados; números não** (noites e valores ficam para a conversa) |
| Plataformas de reserva | **Nunca citar Booking ou outra OTA nominalmente** — dizer "plataformas de reserva". Dado oficial: comissão de **10% a 25%**, média histórica **~15%** |
| Textos | Cada seção terá o texto **lapidado junto com a autora** na implementação — nenhum texto entra sem aprovação dela |

## 2. As 8 seções

### 1. Hero
- Wordmark (SVG `marca/wordmark-escuro.svg`) + headline tipográfica.
- Headline candidata (referência validada no MIV §5): **"Sites para hostels, pagos em *noites*."**
  — Archivo 700, "*noites*" em Instrument Serif itálico Âmbar. Texto final a lapidar.
- Subtítulo de 1–2 frases apresentando o projeto e a oferta.
- Botão WhatsApp já visível (pílula Âmbar, texto Breu).

### 2. O manifesto
- Curto: 3–5 frases. Núcleo: tecnologia sem gatekeepers, troca de dádivas,
  "por onde minhas pernas andam, o projeto chega".
- Fecha com a ponte para o público: começando por quem me recebe — hostels.

### 3. A dor
- A cena real da autora como hóspede, em 1ª pessoa (texto dela, quase intocado):
  procurar o contato direto do hostel, informações fragmentadas entre redes sociais e
  mapas, desistir e reservar pela plataforma.
- **Sem citar plataforma nominalmente.** Fecho com o único dado numérico da página:
  plataformas de reserva cobram **de 10% a 25% de comissão por reserva (média ~15%)** —
  dinheiro que sai do bolso do dono.

### 4. A proposta
- A permuta em um parágrafo: site institucional completo em troca de noites de hospedagem.
- Frase-síntese em destaque visual (grifo Âmbar): **"É uma troca temporária por um produto permanente."**
- Explícito: sem dinheiro envolvido; o único custo é o registro do domínio — que é do
  cliente e fica com ele.

### 5. O que você recebe (e o que não)
Duas colunas honestas, derivadas do escopo fechado em `docs/projeto.md` §4–5:

- **Inclui**: site responsivo, 4 seções (acomodações, sobre, localização, contato/WhatsApp),
  textos escritos a partir do briefing, SEO on-page básico, mapa incorporado, botão de
  WhatsApp para reserva direta, vinculação ao Perfil da Empresa no Google, domínio
  registrado e configurado, 1 rodada de ajustes.
- **Não inclui**: motor de reservas, pagamento online, integração com plataformas de
  reserva, manutenção contínua, produção de fotos, tráfego pago.
- A coluna "não inclui" é deliberada: mostrar limites antes de fechar gera confiança.

### 6. Como funciona
4 passos numerados, sem números de noites/valores:
1. Conversa no WhatsApp e acordo das noites.
2. Cliente preenche o briefing e envia fotos.
3. 15 dias de construção.
4. Site no ar, sob controle total do cliente.

### 7. Quem sou eu
- Foto da autora (contexto estrada/hostel), nome completo, link para o LinkedIn.
- Dois pilares de credibilidade lado a lado:
  - **A estrada** — "Eu não estou construindo um site para um hostel que conheci por uma
    reunião no Zoom. Eu provavelmente dormi em um lugar como o seu na semana passada e
    dormirei em outro na semana que vem. Eu conheço a jornada do hóspede porque ela
    também é a minha."
  - **A profissão** — especialista em Ciência de Dados no Ministério da Gestão e Inovação.

### 8. CTA final + footer
- "Tem um hostel? Vamos conversar." + botão wa.me com mensagem pré-preenchida
  (ex.: "Oi! Tenho um hostel e quero saber mais sobre a permuta.").
- Footer mínimo: e-mail, LinkedIn, monograma.

### Easter egg
Comentário HTML no código-fonte com a pergunta "Qual é a ideia que você está tentando
provar ao mundo?" e a resposta da autora (compartilhar construindo soluções reais,
conectar-se aos lugares em vez de só passar por eles).

## 3. Identidade visual aplicada (MIV)

- Fundo **Breu** `#0A0A09`, texto **Cal** `#F4F1E8`, cards/superfícies **Grafite** `#161513`
  com raio ~12px.
- **Regra do acento**: Âmbar `#E39A3B` em fração pequena — itálico de headline, grifos,
  links, frase-síntese. Nunca página laranja.
- Eyebrows de seção em **IBM Plex Mono** caps, letter-spacing ~0.12em, Cinza-pedra com
  palavra de destaque em Âmbar (ex.: `O MANIFESTO`, `COMO FUNCIONA`).
- Tipografia: Archivo (display 500–700, corpo 400), Instrument Serif Italic (tempero de
  headline — uma palavra por título), IBM Plex Mono (rótulos). Autohospedadas via
  `@fontsource` / `@fontsource-variable`.
- Botão primário: pílula Âmbar com texto Breu. Secundário: contorno, texto Cal.
- Favicon: monograma (`marca/monograma-*.svg`).

## 4. Técnica

- **Novo diretório `site/` na raiz do monorepo** — projeto Astro 5 + Tailwind 4 próprio e
  mínimo: `index.astro` + componentes de seção. Fora do `template/` (o motor é dos
  clientes: multi-página, selecionado por env `CLIENTE`; o site da marca é 1 página com
  identidade própria — misturar complicaria os dois).
- **Reaproveita**: SVGs de `marca/` (wordmark, monograma) e a paleta de `marca/tokens.css`
  como fonte dos tokens do tema.
- **Deploy**: projeto separado na Vercel (free tier) apontando para `site/` — mesmo modelo
  dos clientes. Sobe primeiro no domínio `.vercel.app`.
- **Domínio**: `[DEFINIR]` (ex.: codigoitinerante.com.br). Não bloqueia a construção.
- **SEO/compartilhamento**: title/description, Open Graph com imagem (preview bonito no
  WhatsApp — canal principal de divulgação), `lang="pt-BR"`, favicon.
- Sem JS de framework no cliente (página estática); âncoras nativas se houver menu.

## 5. Fora de escopo (v1)

- Seção de portfólio/cases (entra com o LumeHostel pronto).
- Formulário de contato (CTA é WhatsApp).
- Blog, analytics, multi-idioma.

## 6. Critérios de sucesso

- Um dono de hostel que role a página inteira entende: o que é a permuta, o que recebe,
  o que não recebe, como começa, e quem é a pessoa — sem precisar clicar em nada.
- O site em si parece obra de quem ele contrataria: rápido, bonito no celular, preview
  correto quando o link é enviado por WhatsApp.
- Todos os textos aprovados pela autora, seção por seção.
