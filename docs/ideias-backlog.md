# Backlog de ideias e roteiro incremental — marca e site Código Itinerante

Ideias da autora registradas em 2026-07-15, ordenadas num roteiro incremental. Quando ela perguntar "qual o próximo passo?", consultar este roteiro e propor a próxima fase não concluída. Referências visuais que embasam tudo: seção "Referências para o site da própria marca" em `docs/preferencias-visuais.md`.

## Princípio de ordenação

Identidade primeiro, aplicações depois. O MIV expandido é a fundação: iconografia e estilo de ilustração definidos lá alimentam o site, a animação da hero e o template Word. Fazer aplicações antes da identidade geraria retrabalho.

## Roteiro

### Fase 1 — Expandir o MIV (identidade além do wordmark) — EM ANDAMENTO
O `docs/miv.md` já existe (wordmark, monograma, paleta, regra do acento — aprovado 2026-07-02). Falta a camada que as novas ideias exigem:
1. **Estilo de ilustração/arte autoral**: definir a linguagem dos desenhos. É pré-requisito da iconografia, da viajante e de qualquer arte no site.
2. **Iconografia**: conjunto de ícones/símbolos da marca no estilo definido acima.
   ✅ **Concluída em 2026-07-19**: 6 conceitos do negócio em dois pesos (cheio/miúdo) e
   dois fundos — `marca/icones/`, seção 6 do `docs/miv.md`, spec
   `docs/superpowers/specs/2026-07-19-iconografia-design.md`.
3. **A personagem viajante**: design estático primeiro — vira ativo da marca antes de virar animação.
4. Registrar tudo como novas seções do `docs/miv.md`.

**Decisões parciais do brainstorm (2026-07-17, spec ainda não escrito):**
- Estilo-mãe: **linha solta e quente (Monge/McFetridge) com flat generoso**. Plano B: cena pintada estilo Maggie Appleton/Zelda BOTW.
- Limite: playful sem perder credibilidade com o dono de hostel.
- Cenários seguem as cores da marca (mescla âmbar → barro → ferrugem em camadas, aprovada). Paleta estendida "empoeirada" foi rejeitada — o mundo da viajante é vivo.
- **A viajante é a única livre da regra de cores**: mochila verde, calça azul, blusa vermelha, bota de trilha marrom, gorro amarelo com pompom de outra cor. Cabelo cacheado longo. **Nunca mostrar o rosto de perto** — só sugestão de rosto. Dois registros (de longe nas cenas / figurinha geométrica de corpo inteiro).
- Filminho da hero — roteiro fechado (2026-07-18): cidade **pequena** NitW, cinza/empoeirada de propósito (os hotéis "HOTEL" de 2–3 andares = as plataformas Booking/Airbnb); a viajante colorida caminha à noite sob céu estrelado, rosto parcialmente iluminado pelo celular; encontra a **casinha colorida com jardim** (o hostel com site próprio), o sol nasce em laranja Firewatch e ela entra. **Wordmark no céu o tempo todo**, mudando de cor (dentro da paleta) conforme noite/amanhecer. O final "para e segue o mouse" foi removido.
- Mockups: `mockups/estilo-ilustracao.html`, `mockups/paleta-estendida-cena.html`, `mockups/viajante-dois-registros.html`, `mockups/viajante-silhuetas.html`.
- **Execução pausada em 2026-07-18 no portão da Task 1** (plano `docs/superpowers/plans/2026-07-17-fase1-viajante-ilustracao.md`): silhueta preferida parcial S2·P2, mas o design da personagem aguarda a autora — ela vai trazer a personagem da cabeça dela (rabisco fotografado, entrevista dirigida, Figma ou ilustrador contratado; caminhos detalhados no plano). Retomar dali.

### Fase 2 — Template Word com a assinatura da marca — CONCLUÍDA (2026-07-20)
- `marca/template-documento.docx`, gerado por `marca/gera_template_word.py`. Fontes
  Archivo + Martian Mono (Instrument Serif não é usada em documentos, só no site);
  disponibilidade/fallback no Word resolvidos instalando faces próprias
  ("Archivo Doc"/"Martian Mono Doc") via `marca/prepara_fontes_documento.py`.
- Escopo desta fase é só o sistema visual — texto real de proposta/briefing/contrato
  fica para uma conversa futura com a autora sobre os tipos de documento.

### Fase 3 — Splashs de cor e arte no site da marca — DIREÇÃO FECHADA (2026-07-19)
- Direção aprovada: **degradê contínuo breu → âmbar** na página inteira, final nas versões de papel do MIV, iconografia em escala grande, tipografia maior. Spec: `docs/superpowers/specs/2026-07-19-site-degrade-fase3-design.md`; mockup aprovado: `mockups/site-splash-cor.html`.
- *Rejeitados no processo*: final de página em cor sólida (Set Studio), mancha de tinta e halo difuso.
- Movimento sem vídeo (desenhos que reagem à rolagem, Rauno) ficou para a Fase 4.

### Fase 4 — Animação da hero: a viajante
- Roteiro fechado em 2026-07-18 (spec da Fase 1, §5): noite na cidade cinza das plataformas → descoberta da casinha colorida → amanhecer Firewatch e ela entra; wordmark no céu mudando de cor. (A ideia original "contorno laranja, anda estilo Mario, cabeça segue o mouse" foi substituída.)
- Depois, adicionar mais elementos incrementalmente.
- Depende da Fase 1 (design da personagem) e idealmente da Fase 3 (site já com a linguagem de arte).

### Fase 5 — Reduzir o risco comercial da permuta (site + documentos) — EM ANDAMENTO

**O problema (levantado em 2026-07-20):** o modelo de permuta (site em troca de noites) é
incomum o bastante para gerar perguntas que o texto atual não responde. A seção "O que você
recebe" cobre o **escopo técnico**; o que trava a decisão do dono de hostel é o **risco
comercial**, e disso o site não fala.

**Entrevista dirigida concluída em 2026-07-23** — spec com os 8 eixos fechados (contrapartida
da estadia, preço/noites, rodadas de ajuste, processo/prazos, saída, manutenção, propriedade,
formalização) em
`docs/superpowers/specs/2026-07-23-fase5-limites-permuta-design.md`. Também saiu dessa sessão
o instrumento pra aplicar isso em cada cliente: `docs/gera_questionario_contrato.py` →
`docs/questionario-contrato.docx`, questionário de intake com as perguntas que mudam por
contrato (o valor de R$3.000 usado na fórmula de noites é parâmetro interno — não aparece no
contrato do cliente, só o número de noites resultante).

**FAQ da marca publicado, mesmo dia (2026-07-23)** — página nova `site/faq.astro` (fora da
rolagem única, link "Veja as perguntas frequentes" em `Escopo.astro`), 7 perguntas cobrindo as
5 originais da Fase 5 mais duas que surgiram na sessão (fotos/material mínimo, propriedade de
domínio/código). Corrigida junto uma linha desatualizada em `Escopo.astro` ("uma rodada de
ajustes após a entrega" → "quatro rodadas... durante a construção").

**Ainda falta** o texto real do contrato de permuta (usa `docs/projeto.md` §12 + o template
Word da Fase 2 + as respostas do questionário de intake).

### Ideias soltas (encaixar quando fizer sentido)
- "Artezinha" ao lado do nome na aba do navegador (Sara Soueidan) — favicon já existe? avaliar se o monograma CI cumpre isso ou se a viajante/ícone cabe.
- Voz autoral clara com toque de humor (Maggie Appleton, Lynn Fisher) — revisitar os textos do site quando a identidade estiver madura.
- Site que cria "ambiente/sentimento", não só uma página.

## Status

- [ ] Fase 1 — MIV expandido (ilustração, iconografia, viajante)
- [x] Fase 2 — Template Word (2026-07-20): só o sistema visual, sem texto
  comercial real — isso fica para uma conversa futura sobre os tipos de
  documento. Spec `docs/superpowers/specs/2026-07-20-fase2-template-word-design.md`.
- [x] Fase 3 — Degradê breu → âmbar + iconografia no site (2026-07-19)
- [ ] Fase 4 — Animação da hero
- [ ] Fase 5 — Risco comercial da permuta (entrevista de limites → textos e documentos):
  entrevista concluída, spec + questionário de intake + FAQ do site prontos (2026-07-23);
  falta só o texto do contrato
