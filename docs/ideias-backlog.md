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

### Fase 2 — Template Word com a assinatura da marca — EM ANDAMENTO (desde 2026-07-20)
- Só o sistema visual (cabeçalho/rodapé/tipografia do MIV §5), sem texto comercial real —
  isso fica para uma conversa futura sobre os tipos de documento (ver Fase 5). Fontes: Archivo
  + Martian Mono (Instrument Serif não é usada em documentos, só no site); disponibilidade no
  Word resolvida instalando faces próprias ("Archivo Doc"/"Martian Mono Doc") via
  `marca/prepara_fontes_documento.py`.
- Spec `docs/superpowers/specs/2026-07-20-fase2-template-word-design.md`, plano
  `docs/superpowers/plans/2026-07-20-fase2-template-word.md` (5 tasks, subagent-driven).
- **Estado (2026-07-20): Task 1 concluída** (commit `182fcf5`) — fontes derivadas e
  instaladas por usuário no Windows, verificadas no registro. Faltam Tasks 2-5: gerador
  `marca/gera_template_word.py` (esqueleto/cabeçalho/rodapé, corpo, incorporação de fontes
  via automação COM do Word) e documentação final. Ledger de progresso em
  `.superpowers/sdd/progress.md`. **Retomar despachando a Task 2** (usar
  `scripts/task-brief` da skill subagent-driven-development sobre o plano acima).

### Fase 3 — Splashs de cor e arte no site da marca — DIREÇÃO FECHADA (2026-07-19)
- Direção aprovada: **degradê contínuo breu → âmbar** na página inteira, final nas versões de papel do MIV, iconografia em escala grande, tipografia maior. Spec: `docs/superpowers/specs/2026-07-19-site-degrade-fase3-design.md`; mockup aprovado: `mockups/site-splash-cor.html`.
- *Rejeitados no processo*: final de página em cor sólida (Set Studio), mancha de tinta e halo difuso.
- Movimento sem vídeo (desenhos que reagem à rolagem, Rauno) ficou para a Fase 4.

### Fase 4 — Animação da hero: a viajante
- Roteiro fechado em 2026-07-18 (spec da Fase 1, §5): noite na cidade cinza das plataformas → descoberta da casinha colorida → amanhecer Firewatch e ela entra; wordmark no céu mudando de cor. (A ideia original "contorno laranja, anda estilo Mario, cabeça segue o mouse" foi substituída.)
- Depois, adicionar mais elementos incrementalmente.
- Depende da Fase 1 (design da personagem) e idealmente da Fase 3 (site já com a linguagem de arte).

### Fase 5 — Reduzir o risco comercial da permuta (site + documentos) — A FAZER

**O problema (levantado em 2026-07-20):** o modelo de permuta (site em troca de noites) é
incomum o bastante para gerar perguntas que o texto atual não responde. A seção "O que você
recebe" cobre o **escopo técnico**; o que trava a decisão do dono de hostel é o **risco
comercial**, e disso o site não fala. Perguntas que ficam sem resposta hoje:

- Quantas noites, em média, para um hostel médio? (hoje só existe "consultar")
- O que acontece se o dono não gostar do resultado, além da "uma rodada de ajustes"?
- Existe combinado por escrito? Contrato, proposta, e-mail de aceite?
- Quem paga domínio, hospedagem, manutenção depois? Por quanto tempo?
- Até quando ela mantém o site no ar se a relação acabar?

**Já existe base em `docs/projeto.md`**: §11 tem a fórmula de conversão em noites (piso/teto por
diária real) e §5 já lista o que o escopo NÃO inclui (sem manutenção contínua além de 1 rodada
de ajustes). §12 tem o checklist de cláusulas do contrato, ainda sem os valores preenchidos.
Esta fase preenche essas lacunas — não recomeça do zero.

**Como conduzir (pedido explícito da autora, não pular):** antes de redigir qualquer texto
de site ou documento comercial, **estabelecer as linhas** — até onde ela vai e o que ela não
está disposta a fazer. O trabalho começa por uma **entrevista dirigida**, uma pergunta por
vez, com opções e recomendação (mesmo formato da skill `/novo-projeto`), para ela descobrir e
declarar os próprios limites. Só depois de as linhas estarem escritas é que se redige.

Eixos que a entrevista precisa cobrir (esboço — refinar na hora):
1. **Preço/permuta**: piso de noites, o que conta como "hostel médio", quando ela recusa.
2. **Escopo**: o que está incluso, o que é extra, quantas rodadas de ajuste de verdade.
3. **Saída**: e se ele não gostar? Devolve as noites? Fica com o site? Ela tira do ar?
4. **Manutenção**: o que ela mantém de graça, por quanto tempo, o que vira cobrança.
5. **Propriedade**: domínio, código, fotos, conteúdo — de quem fica o quê.
6. **Formalização**: até que ponto ela quer contrato (nada / e-mail de aceite / proposta
   assinada) — decisão dela, não default meu.

Entregáveis prováveis (definir depois da entrevista): um documento interno com as linhas
("minhas condições"), o texto de risco no site (provável seção nova ou FAQ curto) e o
modelo de proposta/combinado para o cliente. Depende da Fase 2 (template Word) para os
documentos saírem com a cara da marca.

### Ideias soltas (encaixar quando fizer sentido)
- "Artezinha" ao lado do nome na aba do navegador (Sara Soueidan) — favicon já existe? avaliar se o monograma CI cumpre isso ou se a viajante/ícone cabe.
- Voz autoral clara com toque de humor (Maggie Appleton, Lynn Fisher) — revisitar os textos do site quando a identidade estiver madura.
- Site que cria "ambiente/sentimento", não só uma página.

## Status

- [ ] Fase 1 — MIV expandido (ilustração, iconografia, viajante)
- [ ] Fase 2 — Template Word
- [x] Fase 3 — Degradê breu → âmbar + iconografia no site (2026-07-19)
- [ ] Fase 4 — Animação da hero
- [ ] Fase 5 — Risco comercial da permuta (entrevista de limites → textos e documentos)
