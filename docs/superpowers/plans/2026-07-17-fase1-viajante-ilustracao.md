# Fase 1 do MIV — Viajante e Ilustração — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformar a spec da Fase 1 (`docs/superpowers/specs/2026-07-17-miv-ilustracao-viajante-design.md`) em ativos concretos: a viajante desenhada nos dois registros, tons de roupa fechados, uma cena de cidade NitW de teste, a iconografia da marca e as novas seções do `docs/miv.md`.

**Architecture:** Trabalho de design iterativo com a autora: cada peça nasce como mockup HTML com variantes (formato aprovado por ela), passa por um portão de aprovação humana, e só então vira SVG definitivo versionado em `marca/ilustracao/`. O "teste" de cada task é a reação da autora — nenhuma task avança sem aprovação explícita.

**Tech Stack:** HTML/CSS/SVG puros nos mockups (padrão `mockups/*.html`, Google Fonts via link); SVGs finais autocontidos (sem fontes externas); tokens CSS em `marca/tokens.css`.

## Global Constraints

- Estilo-mãe: linha solta e quente (Monge/McFetridge) com flat generoso (spec §1).
- Limite: playful até onde o dono de hostel ainda vê uma profissional (spec §1).
- Cenários obedecem à paleta da marca; camadas âmbar `#E39A3B` → barro `#C4693F` → ferrugem profunda; fundo no território do Breu `#0A0A09` (spec §2). Cores vivas, nunca empoeiradas.
- A viajante é a única livre de regra de cor: mochila verde, calça azul, blusa vermelha, bota marrom, gorro amarelo com pompom de outra cor (spec §2).
- Viajante: cabelo cacheado longo; rosto nunca de perto, no máximo sugerido (spec §3).
- Cidade: construção Night in the Woods — blocos, janelas repetidas, paralaxe, silhueta de telhados (spec §4).
- Cores de ilustração nunca tocam texto, botão, link ou fundo de interface (spec §2).
- Sem emojis em código; idioma pt-BR; commits em português.
- Mockups seguem o padrão visual dos existentes (`mockups/miv-revisao.html`): fundo Breu, cartões Grafite, rótulos Martian Mono.

---

### Task 1: Silhuetas da viajante — registro de longe

**Files:**
- Create: `mockups/viajante-silhuetas.html`

**Interfaces:**
- Consumes: paleta e padrões de cartão de `mockups/viajante-dois-registros.html` (copiar o bloco `<style>` base).
- Produces: a silhueta aprovada (proporção + pose) e a combinação de tons de roupa aprovada — insumos das Tasks 2, 3 e 4.

- [ ] **Step 1: Montar o mockup com 4 propostas de silhueta × 2 paletas de roupa**

Estrutura do arquivo (mesmo esqueleto CSS dos mockups anteriores). Oito cartões em grade 4×2: cada coluna é uma silhueta (S1–S4), cada linha uma paleta de roupa (P1, P2). Cada célula mostra a viajante ~180px de altura sobre uma faixa de cena mínima (crista de morro barro sobre fundo Breu) para julgar a leitura à distância.

As 4 silhuetas variam um eixo por vez:
- **S1 — arredondada compacta** (base Alto): corpo em gota, cabeça grande, passada curta.
- **S2 — alongada macia** (base Old Man's Journey): corpo mais alto, pernas finas, passada larga.
- **S3 — triangular** : casaco/poncho abrindo em A, silhueta estável.
- **S4 — mochilão dominante**: a mochila maior que o torso, corpo inclinado pra frente (trilheira de verdade).

Elementos obrigatórios em todas (DNA da spec §3): gorro com pompom, **cabelo cacheado longo** (caindo abaixo dos ombros, cachos como cachos de círculos), mochila, cachecol ao vento, botas. Rosto: nenhum (de longe não se desenha rosto).

As 2 paletas de roupa (spec §2 — tons a calibrar sobre cena escura):
- **P1 — viva-clara**: mochila verde `#4E9B5E`, calça azul `#3E6FB0`, blusa vermelha `#D64545`, bota marrom `#7A4A2B`, gorro amarelo `#F0C24B`, pompom vermelho `#D64545`.
- **P2 — viva-profunda**: mochila verde `#3A7A4A`, calça azul `#2F5488`, blusa vermelha `#B93A3A`, bota marrom `#5F3A22`, gorro amarelo `#E8B93E`, pompom azul `#3E6FB0`.

Rótulo de cada célula: `S1 · P1` etc. Legenda final perguntando os dois eixos separados: qual corpo, qual paleta.

- [ ] **Step 2: Abrir no navegador e verificar**

Run: `start "" "C:\Users\tatia\codigo-itinerante\mockups\viajante-silhuetas.html"`
Verificar: 8 células renderizam, cabelo claramente longo em todas, nenhuma tem rosto, tons legíveis sobre o fundo escuro.

- [ ] **Step 3: Portão de aprovação da autora**

Apresentar pedindo reação nos dois eixos (silhueta e paleta) separadamente. Iterar o mockup até aprovação explícita de uma combinação (ex.: "S2 com P1, mas pompom azul"). Registrar a escolha no próprio arquivo (banner "APROVADO: ...") antes de seguir.

- [ ] **Step 4: Commit**

```bash
git add mockups/viajante-silhuetas.html
git commit -m "Fase 1: silhuetas da viajante (registro de longe) com escolha aprovada"
```

---

### Task 2: Tokens de cor da viajante

**Files:**
- Modify: `marca/tokens.css` (acrescentar bloco ao final do `:root`)

**Interfaces:**
- Consumes: paleta de roupa aprovada na Task 1.
- Produces: custom properties `--vj-*` usadas nos SVGs e mockups seguintes.

- [ ] **Step 1: Acrescentar o bloco de tokens**

Com os hex aprovados na Task 1 (os valores abaixo são os de P1; substituir pelos aprovados):

```css
  /* A viajante — a única fora da regra de cores (MIV § personagem).
     Estas cores são exclusivas da personagem: nunca em interface ou cenário. */
  --vj-mochila: #4e9b5e;
  --vj-calca: #3e6fb0;
  --vj-blusa: #d64545;
  --vj-bota: #7a4a2b;
  --vj-gorro: #f0c24b;
  --vj-pompom: #d64545;
  --vj-pele: #b97a52;
  --vj-cabelo: #2e1b12;
```

- [ ] **Step 2: Verificar consistência**

Conferir que nenhum hex colide com um token `--ci-*` existente (a viajante não usa cor da marca) e que os valores batem com o banner "APROVADO" da Task 1.

- [ ] **Step 3: Commit**

```bash
git add marca/tokens.css
git commit -m "Fase 1: tokens de cor da viajante"
```

---

### Task 3: Figurinha geométrica de corpo inteiro — registro de perto

**Files:**
- Create: `mockups/viajante-figurinha.html`

**Interfaces:**
- Consumes: silhueta e paleta aprovadas (Task 1), tokens `--vj-*` (Task 2).
- Produces: figurinha aprovada — insumo do SVG final (Task 5) e de avatar/stickers futuros.

- [ ] **Step 1: Montar o mockup com 3 propostas de figurinha**

Corpo inteiro sempre, ~320px de altura, espírito Everyhey (geometria de círculos e arcos) mas **derivada da silhueta aprovada** na Task 1. Três propostas variando só o grau de geometrização:
- **F1 — quase a silhueta**: a de longe ampliada com acabamento (mesmas formas, cantos mais precisos).
- **F2 — geometria média**: formas explícitas (cabeça círculo, corpo cápsula, cachos como coroa de bolhas longas), rosto sugerido por 2 pontinhos afastados OU nada — mostrar as duas.
- **F3 — geometria radical**: círculos/arcos puros estilo Everyhey, sem rosto nenhum.

Regra dura da spec §3 em banner no topo: corpo inteiro, nunca busto; rosto no máximo sugerido. Cada proposta sobre dois fundos (Breu e um cartão âmbar) para testar versatilidade de avatar.

- [ ] **Step 2: Abrir no navegador e verificar**

Run: `start "" "C:\Users\tatia\codigo-itinerante\mockups\viajante-figurinha.html"`
Verificar: nenhuma proposta é busto/retrato; cabelo longo presente; cores da Task 2.

- [ ] **Step 3: Portão de aprovação da autora**

Iterar até aprovação explícita (incluindo a decisão rosto-sugerido vs sem-rosto). Registrar banner "APROVADO" no arquivo.

- [ ] **Step 4: Commit**

```bash
git add mockups/viajante-figurinha.html
git commit -m "Fase 1: figurinha de corpo inteiro da viajante com escolha aprovada"
```

---

### Task 4: Cena-modelo do roteiro — cidade cinza, casinha colorida

**Files:**
- Create: `mockups/cidade-viajante.html`

**Interfaces:**
- Consumes: silhueta de longe aprovada (Task 1), tokens `--vj-*` (Task 2), roteiro do filme (spec §5).
- Produces: a cena-modelo da cidade e da casinha — gramática visual que a Fase 4 (filme da hero) reutilizará, incluindo os dois estados do céu e do wordmark.

- [ ] **Step 1: Montar a cena-modelo com os dois estados do céu**

Uma cena horizontal (~1200×500) que conta o roteiro numa imagem só — noite à esquerda, aurora à direita:
- **Cidade pequena NitW dessaturada** (esquerda/centro): 2–3 hotéis-bloco de 2–3 andares com letreiro "HOTEL" no topo, em cinzas quentes derivados do Breu/Grafite (ex. `#2A2724`, `#3A3733`, `#4A4540`); janelas repetidas em grade, luz fria/apagada. Camadas de paralaxe: telhados de fundo, fileira de prédios, rua na frente. O cinza é narrativo (mundo das plataformas — spec §2/§4), não estética da marca.
- **Céu noturno estrelado** sobre a cidade, com o **wordmark no céu** (versão noite: Código em Cal, Itinerante em Âmbar).
- **A viajante colorida** na rua, celular na mão com um cone/glow sutil iluminando rosto e peito (luz Campion) — o único elemento multicolorido do trecho noturno.
- **A casinha do hostel** na ponta direita: colorida (âmbar/barro/dourado + jardim verde vivo), sob o trecho do céu que **amanhece em degradê laranja Firewatch**; ali o wordmark aparece na versão amanhecer (cores da paleta com contraste sobre o céu claro).

- [ ] **Step 2: Abrir no navegador e verificar**

Run: `start "" "C:\Users\tatia\codigo-itinerante\mockups\cidade-viajante.html"`
Verificar: a cidade lê como "sem cor" ao lado da casinha; letreiros "HOTEL" legíveis; a viajante é o único elemento multicolorido na parte noturna; wordmark legível nos dois trechos de céu.

- [ ] **Step 3: Portão de aprovação da autora**

Iterar (densidade de prédios, quantidade de janelas acesas, altura das camadas) até aprovação. Banner "APROVADO" no arquivo.

- [ ] **Step 4: Commit**

```bash
git add mockups/cidade-viajante.html
git commit -m "Fase 1: cena de cidade estilo NitW com a viajante integrada"
```

---

### Task 5: SVGs definitivos em marca/

**Files:**
- Create: `marca/ilustracao/viajante-longe.svg`
- Create: `marca/ilustracao/viajante-figurinha.svg`
- Create: `marca/ilustracao/cidade-modelo.svg`
- Create: `marca/ilustracao/LEIA-ME.md`

**Interfaces:**
- Consumes: as versões aprovadas das Tasks 1, 3 e 4.
- Produces: ativos versionados reutilizáveis (documentos, site, Fase 4).

- [ ] **Step 1: Extrair cada SVG aprovado para arquivo próprio**

Copiar o SVG aprovado de cada mockup para o arquivo correspondente, autocontido: cores em hex literais (sem `var()` — os SVGs devem funcionar fora de contexto CSS), `viewBox` preservado, atributo `aria-label` descritivo, sem fontes externas.

- [ ] **Step 2: Criar o LEIA-ME**

`marca/ilustracao/LEIA-ME.md` com: o que é cada arquivo, de qual mockup veio, a regra de uso (viajante = única fora da paleta; cores dela nos tokens `--vj-*` de `marca/tokens.css`) e o aviso de nunca usar as cores dela em interface.

- [ ] **Step 3: Verificar renderização isolada**

Run: `start "" "C:\Users\tatia\codigo-itinerante\marca\ilustracao\viajante-longe.svg"` (e os outros dois)
Verificar: cada SVG abre sozinho no navegador com cores corretas.

- [ ] **Step 4: Commit**

```bash
git add marca/ilustracao/
git commit -m "Fase 1: SVGs definitivos da viajante e da cidade-modelo"
```

---

### Task 6: Iconografia da marca

**Files:**
- Create: `mockups/iconografia.html`
- Create: `marca/ilustracao/icones/` (um SVG por ícone aprovado)

**Interfaces:**
- Consumes: estilo-mãe (spec §1) e regime de cor de cenário (spec §2).
- Produces: conjunto inicial de ícones para documentos (Fase 2) e site (Fase 3).

- [ ] **Step 1: Montar o mockup do conjunto inicial de 8 ícones**

Conjunto proposto (um conceito por ícone, todos do mundo do negócio): **estrada**, **lâmpada de hostel**, **cama/noite**, **código** (chaves `{ }` desenhadas à mão), **mochila**, **pin de mapa**, **permuta** (setas em círculo), **carta/contato**. Estilo: linha solta cal `#F4F1E8` sobre Breu com **um** preenchimento âmbar por ícone (a versão flat completa fica para quando houver uso que a peça); versão papel: linha Tinta `#1A1915`, preenchimento Queimado `#B85C2E`. Grade 4×2, cada ícone em 3 tamanhos (64/32/20px) para testar redução.

- [ ] **Step 2: Abrir no navegador e verificar**

Run: `start "" "C:\Users\tatia\codigo-itinerante\mockups\iconografia.html"`
Verificar: os 8 legíveis a 20px; nenhum usa cor da viajante.

- [ ] **Step 3: Portão de aprovação da autora**

Iterar traço e metáforas até aprovação (ela pode cortar/trocar conceitos do conjunto). Banner "APROVADO".

- [ ] **Step 4: Extrair SVGs aprovados**

Um arquivo por ícone em `marca/ilustracao/icones/` (`estrada.svg`, `lampada.svg`, `cama.svg`, `codigo.svg`, `mochila.svg`, `pin.svg`, `permuta.svg`, `carta.svg`), autocontidos, `viewBox="0 0 64 64"`.

- [ ] **Step 5: Commit**

```bash
git add mockups/iconografia.html marca/ilustracao/icones/
git commit -m "Fase 1: iconografia inicial da marca (8 icones aprovados)"
```

---

### Task 7: Registrar tudo no MIV e fechar a fase

**Files:**
- Modify: `docs/miv.md` (novas seções após "§5 Aplicações")
- Modify: `docs/ideias-backlog.md` (status da Fase 1)
- Modify: `CLAUDE.md` (uma linha em "Estado atual" apontando os novos ativos)

**Interfaces:**
- Consumes: tudo que foi aprovado nas Tasks 1–6.
- Produces: `docs/miv.md` como fonte única da identidade expandida.

- [ ] **Step 1: Escrever as novas seções do MIV**

Três seções novas, condensando a spec + as escolhas concretas:
- **§ Ilustração**: estilo-mãe, limite de credibilidade, regime de cor de cenário (mescla âmbar→barro→ferrugem, cores vivas), regra "cores de ilustração nunca em interface", plano B (cena pintada) registrado como alternativa.
- **§ A viajante**: DNA (gorro+pompom, cabelo cacheado longo, mochila, cachecol, botas), a exceção de cor com os tokens `--vj-*` finais, a regra do rosto (nunca de perto, no máximo sugerido), os dois registros com ponteiro para os SVGs.
- **§ A cidade**: construção NitW (blocos, janelas repetidas, paralaxe, telhados), luz Campion, ponteiro para `cidade-modelo.svg`.

Atualizar também "§6 Entregáveis" com os novos arquivos de `marca/ilustracao/`.

- [ ] **Step 2: Marcar a Fase 1 no backlog**

Em `docs/ideias-backlog.md`: `- [x] Fase 1 — MIV expandido (ilustração, iconografia, viajante)` e remover o bloco "Decisões parciais" (agora vive no MIV). Em `CLAUDE.md`, acrescentar em "Estado atual": ativos de ilustração da marca em `marca/ilustracao/` (viajante, cidade-modelo, ícones), regras em `docs/miv.md`.

- [ ] **Step 3: Revisão da autora**

Pedir que ela leia as seções novas do MIV — é o documento canônico; nada fecha sem o ok dela.

- [ ] **Step 4: Commit**

```bash
git add docs/miv.md docs/ideias-backlog.md CLAUDE.md
git commit -m "Fase 1 concluida: MIV expandido com ilustracao, viajante e cidade"
```

---

## Self-review (feita na escrita)

- **Cobertura da spec**: §1→Tasks 1/6, §2→Tasks 1/2/4, §3→Tasks 1/3/5, §4→Task 4, §5→conceito fica registrado no MIV (Task 7; execução é Fase 4, fora de escopo), §6→Task 6, "Registro no MIV"→Task 7. Sem lacunas.
- **Sem placeholders**: cada task tem conteúdo executável; os hex de P1/P2 são propostas concretas a validar no portão da Task 1 (o plano marca explicitamente onde substituir).
- **Consistência de nomes**: `--vj-*` usado igualmente nas Tasks 2/3/4/7; caminhos `marca/ilustracao/` idênticos nas Tasks 5/6/7.
- **Natureza do trabalho**: aqui não há testes automatizados — o ciclo de cada task é mockup → navegador → aprovação da autora → commit. Os portões humanos substituem o passo "rodar testes".
