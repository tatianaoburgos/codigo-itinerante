# Fase 5 — Limites comerciais da permuta (entrevista dirigida)

**Data**: 2026-07-23 · **Status**: aprovado pela autora

## O que é

Resultado da entrevista dirigida (uma pergunta por vez, com opções +
recomendação) prevista na Fase 5 de `docs/ideias-backlog.md`: as linhas que a
autora está disposta a seguir no modelo de permuta (site por noites),
cobrindo preço, escopo, saída, manutenção, propriedade e formalização. Fecha
as lacunas de `docs/projeto.md` §11-§12 com valores reais e é a base para
redigir o contrato de permuta (ainda não escrito) e o texto de risco no site
da marca (ainda não escrito).

## Decisões

### 1. Contrapartida (estadia da autora)

Durante o período de permuta, o hostel não pode remanejar a autora de
quarto em quarto ou de cama em cama — acomodação fixa (tipo de quarto/cama
especificado no contrato) pelo período combinado.

### 2. Preço/permuta (noites)

- Valor de referência do site fixado em **R$3.000** (substitui a faixa
  R$1.500–3.000 de `docs/projeto.md` §11) — **parâmetro interno, não aparece
  no texto do contrato entregue ao cliente**; só o número de noites
  resultante aparece.
- Fórmula: nº de noites = R$3.000 ÷ diária real do hostel.
- Piso de segurança: **20 noites**, mesmo com diária muito alta.
- Critérios de recusa: cálculo abaixo do piso, ou hostel sem fotos/material
  mínimo decente. *Descartado*: nota mínima de avaliação (Google/Booking)
  como critério fixo — a autora prefere não travar isso, decide caso a caso.

### 3. Escopo — rodadas de ajuste (antes da entrega)

**4 rodadas** de revisão sobre o rascunho, distintas da manutenção
pós-entrega (item 6). *Descartado*: controlar por prazo/calendário em vez de
contagem de rodadas.

### 4. Processo e prazos (sincronizados com a viagem)

- Se o cliente enviar fotos/material até **10 dias antes da chegada** da
  autora no hostel: ela entrega uma **prévia do site antes de chegar**, e os
  ajustes continuam durante a estadia.
- Se o cliente perder esse prazo: a autora viaja mesmo assim (a estadia já
  está combinada e ela depende dela para a própria logística de viagem); o
  trabalho passa a contar a partir de quando o material chegar, mesmo que
  seja durante a estadia. *Descartado*: adiar a estadia até o material
  chegar — depende de flexibilidade de agenda que a autora não quer travar
  contratualmente.

### 5. Saída — se o cliente não gostar do resultado final

Esgotadas as 4 rodadas, o site fica como entregue e **as noites continuam
devidas** — as rodadas já são o mecanismo de "não gostar"; uma vez
esgotadas, o acordo se cumpre dos dois lados. *Descartado*: renegociar
noites para baixo (abre negociação subjetiva a cada caso), ou tirar o site
do ar sem contrapartida (deixaria o trabalho da autora sem garantia de
retorno).

### 6. Manutenção pós-entrega

- 15 dias após a entrega: **1 manutenção/mudança pequena grátis**.
- Critério de "pequena": trocar texto/foto pontual, ajustar um dado.
  "Grande" (seção nova, mudança de layout, página nova) é **sempre**
  cobrança/novo acordo, mesmo dentro dos 15 dias. *Descartado*: limite por
  tempo gasto — mais preciso, mas gera atrito de medir e justificar tempo.
- Depois dos 15 dias: qualquer mudança é novo acordo — o cliente contrata a
  autora (paga) ou contrata outra pessoa.

### 7. Propriedade

- **Domínio**: o próprio cliente registra no registro.br, com o CPF/CNPJ
  dele — titular desde o início, sem transferência de titularidade
  posterior.
- **Site/código/hospedagem**: permanece no projeto Vercel da autora. A
  arquitetura de monorepo compartilhado entre clientes não permite
  transferir o projeto inteiro sem expor dados de outros clientes (ver
  `docs/projeto.md` §10).
- **Portabilidade**: grátis, uma vez, dentro de **30 dias a partir da data
  em que a autora for embora do hostel**. Mecanismo: exportar a pasta do
  cliente + o motor para um repositório novo e isolado (já registrado em
  `docs/projeto.md` §10); o cliente ou o dev dele sobe isso numa conta
  Vercel própria (import direto, sem transferência formal de projeto).
- **Restrição de uso**: o código exportado é para uso no site do próprio
  cliente — não pode ser revendido/reusado como motor para outros clientes
  (protege o negócio da autora).
- Fotos/conteúdo fornecidos pelo cliente continuam sendo dele, usados
  exclusivamente no site dele.
- Se o domínio não for comprado, o site continua no domínio da autora
  (subdomínio `vercel.app`).

### 8. Formalização

Documento simples, linguagem clara (sem juridiquês), assinado via
**assinatura eletrônica gov.br**, ou **contrato físico em papel** se o
cliente preferir (ex.: no momento em que a autora chega no hostel).

## Entregável desta fase: questionário de intake

`docs/gera_questionario_contrato.py` → `docs/questionario-contrato.docx`:
lista de perguntas que a autora responde antes de redigir cada contrato
real, separando o que é fixo (as cláusulas acima, listadas só como
referência, sem pergunta) do que muda por cliente — identificação, diária
usada no cálculo e nº de noites resultante, tipo de acomodação, janela de
uso e datas, prazos do site, domínio pretendido, formalização e
observações. Objetivo: a autora informa tudo de uma vez numa conversa
futura, sem reabrir a entrevista dirigida inteira a cada cliente novo.
Gerador em Python (`python-docx`), seguindo o mesmo padrão de fonte de
verdade em código já usado em `marca/gera_wordmark.py` e
`marca/gera_template_word.py` — mas sem aplicar o sistema visual da marca
(cabeçalho/rodapé/fontes do MIV §5), por ser um documento de uso interno,
não client-facing.

## Fora de escopo (fica para depois)

- Texto real do contrato de permuta (`docs/projeto.md` §12) — depende do
  template Word da Fase 2 e é a próxima etapa natural, usando as respostas
  do questionário desta fase.
- Texto de risco no site da marca (FAQ ou seção nova) — previsto na Fase 5
  original, ainda não escrito.
- Preenchimento do questionário para um cliente real (LumeHostel, Mar à
  Vista ou futuro) — esta fase entrega só o instrumento vazio.

## Referências

- `docs/ideias-backlog.md` Fase 5.
- `docs/projeto.md` §5, §11, §12.
- Memória `projeto-risco-comercial-permuta`.
