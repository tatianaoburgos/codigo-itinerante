# Spec — Fase 1 do MIV expandido: estilo de ilustração e a viajante

Data: 2026-07-17. Brainstorm conduzido com a autora a partir de rodadas de referências
visuais (reações registradas em `docs/ideias-backlog.md` e na memória do projeto).
Complementa o `docs/miv.md` (identidade "Estrada 1 — Lâmpada de hostel").

## Por quê

O MIV cobre wordmark, monograma, paleta e tipografia — mas as ideias do backlog
(template Word, splashs de arte no site, animação da hero) exigem uma camada que ele
não tem: **estilo de ilustração, personagem e regra de cor para desenhos**. Fazer
aplicações sem essa fundação geraria retrabalho. Esta spec fecha a fundação.

## 1. Estilo-mãe da ilustração

**Linha solta e quente com preenchimento flat generoso** — referências: Quentin Monge,
Geoff McFetridge. Contorno a traço imperfeito de propósito, preenchimentos chapados,
uma ideia por desenho, sentimento acima de detalhe.

- Escolhido entre três tratamentos de cor (mockup `mockups/estilo-ilustracao.html`):
  só-linha, linha + uma mancha, e flat generoso — venceu o flat generoso.
- **Limite escrito**: playful e criativo até o ponto em que o dono de hostel ainda vê
  uma profissional. Na dúvida entre encantador e engraçadinho, escolher encantador.
- **Plano B registrado**: cena pintada estilo Maggie Appleton / Zelda Breath of the
  Wild (traço orgânico, cor aquarelada), caso a linha solta não conquiste a autora
  quando aplicada em peças reais.

## 2. Regra de cor da ilustração — dois regimes

### Cenários obedecem à marca
- Paisagens e cidades usam a paleta do MIV. Combinação aprovada para camadas de
  profundidade: **âmbar → barro → ferrugem profunda** (a "mescla de laranjas" estilo
  Firewatch). Fundo/céu sempre no território do Breu — a noite é da marca.
- Cores de apoio (céu de madrugada, vegetação) podem derivar da paleta, mas **vivas** —
  saturação franca. A proposta de paleta estendida empoeirada (verde-mata #6B8F71,
  azul-madrugada #4F6A8F, rosa-poente #BC7E8C; mockup
  `mockups/paleta-estendida-cena.html`) foi **rejeitada**: "o mundo da viajante não é
  feito de cores tão neutras e calmas".
- Cores de ilustração nunca tocam texto, botão, link ou fundo de interface.

### A viajante é a única livre
A personagem é o único elemento da marca que **não** obedece à regra de cores:
mochila **verde**, calça **azul**, blusa **vermelha**, bota de trilha **marrom**,
gorro **amarelo** com pompom **de outra cor**. Ela é o ponto multicolorido no mundo
monocromático-quente da marca — o que a torna imediatamente achável em qualquer cena.
Os tons exatos serão definidos no design final da personagem (etapa de execução),
calibrados para sentar sobre as cenas escuras.

## 3. A viajante

- **Silhueta**: gorro com pompom, cabelo cacheado **longo**, mochila de trilha,
  cachecol, bota de trilha. Esses elementos são o DNA — presentes em qualquer registro.
- **Rosto: nunca de perto.** A câmera não se aproxima do rosto; ele é no máximo
  sugerido (pontinhos, um traço) ou simplesmente não existe. O retrato frontal
  detalhado foi rejeitado (mockup `mockups/viajante-dois-registros.html`).
- **Dois registros, uma menina**:
  1. **De longe** — pequena nas cenas, formas arredondadas e macias, identificável
     pela silhueta e pelas cores livres. Referências: Alto (Alto's Odyssey), o velho
     de Old Man's Journey.
  2. **Figurinha geométrica de corpo inteiro** — espírito Everyhey (Hey Studio),
     para avatar, figurinha que passeia na página, futuros stickers. Corpo inteiro,
     nunca busto/retrato; rosto sugerido, não desenhado.

## 4. A cidade (cenário do filme da hero)

Construção **Night in the Woods**, integral: prédios como blocos simples com janelas
repetidas, cidade em **camadas de paralaxe**, silhuetas de telhados contra o céu.
Cores conforme o regime de cenário (§2). Influência secundária de luz: Pascal
Campion — janelas acesas e postes como pontos de emoção na cena, coerentes com a
narrativa da lâmpada de hostel do MIV.

## 5. O filme da hero (conceito registrado; spec próprio na Fase 4)

Tela cheia, fundo Breu, wordmark visível o tempo todo. A viajante atravessa a cidade
(estilo §4) em rolagem/tempo; a narrativa deve prender até o fim. No final, ela para
e a cabeça acompanha o mouse (referência: robbowen.digital). Sem vídeo — SVG/CSS/JS,
respeitando `prefers-reduced-motion` como todo movimento do projeto.

## 6. Iconografia

Herda o estilo-mãe (§1) e o regime de cor de cenário (§2): linha solta + flat nas
cores da marca, uma ideia por ícone. O desenho do conjunto é etapa de execução, com
estas regras prontas.

## Fora de escopo desta spec

- Desenho final da personagem (proporções, tons exatos das roupas) — execução.
- O filme da hero em si — Fase 4 do backlog.
- Template Word e splashs no site — Fases 2 e 3, dependem desta fundação.

## Registro no MIV

Ao executar, estas regras viram novas seções do `docs/miv.md` (§ ilustração,
§ personagem, § cidade), mantendo o manual como fonte única da identidade.
