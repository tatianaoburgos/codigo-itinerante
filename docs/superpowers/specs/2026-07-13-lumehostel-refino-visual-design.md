# LumeHostel — refino visual: tipografia, símbolo, fim das caixinhas, seção "A vibe"

Data: 2026-07-13. Aprovado pela autora em brainstorm. Sucede o redesign one-page
(`2026-07-13-lumehostel-onepage-design.md`), que continua valendo.

## Regras que continuam valendo

- Nenhuma informação inventada sobre o hostel: só Booking, Google e Instagram.
- Preços nunca no site; CTA sempre WhatsApp.
- Fotos do hostel só das presenças públicas do próprio estabelecimento;
  proveniência registrada em `clientes/lumehostel/fotos/FONTES.md`.

## 1. Tipografia — uma fonte só, geométrica

**Problema:** a tipografia varia pela página. O logotipo usa uma fonte geométrica e
angular (Ellograph CF, do MIV — vem em curvas dentro do SVG, não como fonte), e todo o
resto do site usa Fredoka, que é arredondada. São duas famílias visuais diferentes.

**Decisão:** a Ellograph CF é proprietária (Connary Fagen) e exigiria licença web paga.
Adotamos uma **fonte livre com o espírito do logotipo** — reta, geométrica, espessura
uniforme, cortes secos — aplicada ao site inteiro (títulos e corpo), substituindo a
Fredoka.

**Fonte escolhida pela autora (comparativo visual das três candidatas — Space Grotesk,
Poppins, Archivo — renderizadas no próprio site): Space Grotesk.** Cortes angulares; o
"S" e o "E" são os mais próximos dos do logotipo.

O tema `template/src/styles/temas/lumehostel.css` passa a usar Space Grotesk em
`--font-display` e `--font-corpo` (via `@fontsource-variable/space-grotesk`, self-hosted);
a Fredoka sai, junto com o pacote `@fontsource-variable/fredoka`.

Permanece em `PENDENCIAS.md` a nota ao Gabriel: ele pode comprar a licença web da
Ellograph CF se quiser a fonte original do MIV no site.

## 2. Símbolo da marca

**Problema:** `clientes/lumehostel/marca/simbolo-ambar.svg` contém **apenas a estrela**.
O símbolo real da marca é estrela **+ chama** (o triângulo abaixo) — como se vê no logo
completo. Por isso os divisores entre seções parecem um símbolo cortado. Além disso, o
hero tem uma barra âmbar decorativa solta (`h-1 w-16 bg-fitinha`) que não pertence à
marca e é o elemento desalinhado que a autora apontou.

**Decisão:**

- Criar `clientes/lumehostel/marca/simbolo-completo.svg` com os dois traçados
  (estrela + chama), extraídos do `logo-ambar.svg`, com viewBox ajustada para que o
  símbolo fique centrado e alinhado.
- `config.marca.simbolo` passa a apontar para ele — divisores e marca-d'água usam o
  símbolo inteiro.
- Remover a barra âmbar solta do `Hero.astro`.

## 3. Fim das caixinhas

**Problema:** comodidades, região e depoimentos são cards com fundo claro, borda,
sombra e cantos arredondados. A autora considerou o resultado deselegante, e o efeito
compete com a fotografia, que deve dominar.

**Decisão — "sem caixa":**

- **Comodidades e região:** a foto é o elemento (canto reto ou raio mínimo), com o texto
  solto logo abaixo, direto sobre o fundo da seção. Sem borda, sem sombra, sem fundo de
  card.
- **Comodidade sem foto:** vira uma linha de lista fina (não uma caixa vazia).
- **Depoimentos:** a citação em tipo grande com uma barra fina lateral; sem moldura.
- Ajustar as regras de contraste em `lumehostel.css` que hoje dependem de `.bg-white` /
  `.bg-sal` nos cards, para que o texto continue legível sobre o fundo das seções.

## 4. Hero até a borda de cima, menu flutuante

**Problema:** hoje o `Nav` é uma barra terracota sólida no topo, empurrando a foto do
hero para baixo. A autora quer a foto encostando na borda superior da tela.

**Decisão:**

- O `Nav` deixa de ocupar espaço no fluxo: passa a flutuar **sobre** o hero
  (`position: fixed`, fundo transparente, letras claras), e o hero começa no topo
  absoluto da página.
- A legibilidade do menu sobre a foto é garantida pelo degradê escuro que o hero já
  tem no topo (reforçá-lo se necessário) — não por um fundo sólido.
- Ao rolar para fora do hero, o menu ganha fundo sólido (terracota) e permanece fixo,
  para que as âncoras e o botão de WhatsApp continuem ao alcance. Implementação com
  `IntersectionObserver` sobre o hero (script mínimo, sem biblioteca) alternando uma
  classe no header.
- Sem JavaScript (ou antes de ele rodar), o menu deve ficar legível: o estado padrão é
  o transparente sobre o hero, que é onde a página começa.

## 5. Seção "A vibe do hostel"

Nova seção, **entre Comodidades e A região** — fecha o "como é ficar aqui" antes de
partir para "o que tem em volta".

- **Formato:** mosaico de fotos em alturas variadas (CSS columns/masonry), quase sem
  texto: um título curto e as imagens. Sem card, sem borda, sem legenda.
- **Fonte das fotos:** as 13 páginas do Google Maps salvas pela autora
  (`~/Downloads/lume hostel vibe *.htm`) — cada arquivo embute a URL
  `lh3.googleusercontent.com/gps-cs-s/...` da foto; baixar com sufixo `=w1600`.
  Mais a foto do coworking (`lume hostel coworking.url`) e as já baixadas
  (`patio externo.jpg` — pátio à noite com varal de luzes, `redário.jpg`).
- **Dados:** campo novo `vibe?: Foto[]` no schema (opcional). Seção não renderiza sem ele.
- Verificar visualmente cada foto baixada (rejeitar frames de vídeo com legenda queimada,
  imagens verticais de stories, fotos com rosto de hóspede identificável).

## 6. Fotos e conteúdo reais

- **Acomodações → 6 tipos** (os que o Booking publica), cada um com foto própria,
  acabando com a imagem repetida no carrossel: Dormitório Misto 6 camas, Misto 8 camas,
  Feminino 4 camas, Feminino 6 camas, Quarto Duplo, Suíte Standard. As fotos já estão
  em `~/Downloads/` com esses nomes.
- **Comodidades ilustradas:** redário (`redário.jpg`) passa a ilustrar "Espaço com
  redes"; pátio à noite (`patio externo.jpg`) ilustra o pátio; coworking ganha foto.
- **Distâncias da região corrigidas** pelas oficiais do Booking (seção "Proximidades da
  acomodação", print em `~/Downloads/lume hostel - informações importantes.png`):
  Manaíra 600 m, Bessa 750 m, Tambaú 2 km, Cabo Branco 3,1 km, Farol do Cabo Branco 8 km,
  Centro Cultural José Lins do Rego 4 km, aeroporto 17 km. As distâncias atuais do config
  (medidas de carro entre centroides) estão erradas e saem.

## Fora de escopo

- Domínio, sitemap, contato real (seguem pendentes do Gabriel).
- Qualquer mudança na estrutura one-page, já aprovada.
