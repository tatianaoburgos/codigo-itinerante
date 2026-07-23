# Projeto Site — Permuta com Hostels

Documento de trabalho. Consolida as decisões e discussões iniciais. A partir daqui, seguir versionando neste repositório.

---

## 1. Modelo de negócio (resumo)

Construir um site institucional simples para hostels/pousadas e oferecê-lo em permuta por noites de hospedagem (não é venda em dinheiro). Oferecer três tipos de sites diferentes — todos iguais em conteúdo, mas variando o layout.

- **Arquitetura pretendida**: "build once, reuse everywhere" — um motor de código reutilizável, com dados trocados por cliente.
- **Objetivo estratégico duplo**: (a) gerar hospedagem via permuta enquanto viajo; (b) construir ativo de portfólio em dev/dados (coerente com a documentação pública da transição no LinkedIn/Medium).
- **Gargalo conhecido a vigiar**: acúmulo de manutenção. Todo o desenho de escopo abaixo é feito para blindar contra isso.

Caso gere manutenção, a manutenção é combinada com o cliente mediante pagamento (ver decisão registrada na seção 10 e em `decisoes-tecnicas.md`).

---

## 2. Referência de estrutura

Modelo de referência: <https://www.nomadssalvador.com/>

- Usar APENAS como referência de ESTRUTURA (quais abas, ordem das seções, hierarquia visual).
- Ignorar toda a parte de reservas. O Nomads usa Cloudbeds como motor de reservas real; nós NÃO faremos isso.
- Não copiar código, textos ou imagens do Nomads. Estrutura/layout é livre; conteúdo é protegido.
- Nomads não é alvo de permuta — só referência.

**Licenças de templates**: ao usar qualquer template de código, ler o LICENSE. Preferir MIT / Apache 2.0 (uso comercial livre). Evitar GPL/copyleft. CC-BY exige manter crédito.

---

## 3. Estrutura do site (abas)

1. **Acomodações** — como o Nomads, mas SEM o botão "verifique disponibilidade" (não há reserva).
2. **Sobre o hostel** — informações gerais, história, diferencial.
3. **Localização** — mapa incorporado (Google Maps embed) + como chegar.
4. **Reserve pelo WhatsApp / Fale conosco** — link direto para o WhatsApp e e-mail do hostel.
   - ⚠️ Evitar a palavra isolada "Reservas" no menu — cria expectativa de motor de reservas. Usar rótulo que já sinalize o canal (WhatsApp/contato).

---

## 4. Escopo — O QUE INCLUI

- Site institucional responsivo (desktop + mobile).
- As 4 abas acima.
- Copy dos textos, a partir do briefing preenchido pelo cliente.
- SEO on-page básico (title, meta description, headings, dados estruturados LodgingBusiness, alt text, sitemap).
- Mapa incorporado (Google Maps embed).
- Botão/link direto para WhatsApp e e-mail.
- Vinculação do site ao Perfil da Empresa no Google — condicionada a o cliente fornecer acesso de administrador (ver seção 8).
- Registro e configuração de 1 domínio para o cliente (custo do cliente — ver seção 7).
- 1 (uma) rodada de ajustes, dentro de [DEFINIR: 15–30] dias após a entrega.

---

## 5. Escopo — O QUE NÃO INCLUI (explícito no contrato)

- ❌ Não é motor de reservas. Não checa disponibilidade em tempo real, não bloqueia datas, não confirma reservas.
- ❌ Não processa pagamento. Nenhum dado de cartão passa pelo site.
- ❌ Não sincroniza com Booking / Airbnb / Hostelworld / OTAs (não é channel manager).
- ❌ Não inclui manutenção contínua além da rodada de ajustes. Qualquer alteração posterior = novo acordo.
- ❌ Não inclui produção de fotos/vídeo profissional. Usa-se exclusivamente o material fornecido pelo cliente.
- ❌ Não inclui tráfego pago, campanhas ou gestão de redes sociais.
- ❌ Não garante posição/ranking no Google. SEO on-page ≠ garantia de primeira página.
- ❌ Não inclui e-mail corporativo, blog nem produção de conteúdo recorrente.
- ❌ Recuperação de acesso ao Perfil da Empresa no Google (é responsabilidade do cliente — ver seção 8).

---

## 6. Inputs necessários do cliente

Questionário completo, pronto para enviar ao cliente: `docs/briefing-cliente.md`.

Resumo do que é pedido:

- [ ] **Identidade visual** — Manual de Identidade Visual (MIV), se houver; senão, logo/cores/estilo desejado.
- [ ] **Fotos em alta resolução** — quartos, áreas comuns, fachada, arredores. A qualidade do site depende diretamente da qualidade das fotos fornecidas.
- [ ] **Descrição das acomodações** — para cada tipo de quarto: nome, capacidade, comodidades.
- [ ] **Sobre o hostel** — breve história, proposta, o que o diferencia.
- [ ] **Dados de contato** — número de WhatsApp, e-mail, endereço completo, Instagram/redes, domínio (se já tiver).
- [ ] **Acesso de administrador ao Perfil da Empresa no Google** (ver seção 8).
- [ ] **Grade de atividades/serviços**, se houver (tours, café, coworking etc.).

**Valores**: não é mais pergunta ao cliente — política fixa é "consultar no WhatsApp" (sem faixa/preço publicado no site), para evitar custo de manutenção recorrente a cada reajuste. Comunicado como combinado, não como escolha, no briefing.

Observação: a construção só começa após o recebimento completo deste material.

---

## 7. Domínio e hospedagem

- **Domínio**: registrado e configurado por mim; administração a discutir com cada cliente. O cliente pode me contratar para seguir com a manutenção ou ficar com o domínio para fazer o que quiser.
- O custo do domínio é o ÚNICO gasto financeiro do cliente — deixar isso explícito na proposta.
- **Hospedagem**: free tier (Vercel) — decisão registrada em `decisoes-tecnicas.md`. Custo zero para o cliente.
- ⚠️ Prever no contrato uma cláusula de portabilidade/transferência: se o cliente solicitar, o domínio e/ou o site podem ser transferidos para ele, mediante [processo a definir]. Isso evita atrito futuro sobre "de quem é o site". **O site é dele.** Com o monorepo, a transferência se dá exportando a pasta do cliente + motor para um repositório próprio (ver seção 10).

---

## 8. Perfil da Empresa no Google (cláusula)

Distinção importante:

- **Perfil da Empresa no Google (Google Business Profile)** = a ficha que controla nome, fotos, horário e o link do site. É aqui que se altera o link.

Pergunta certa ao dono: *"Quem administra o Perfil da Empresa no Google? Você tem acesso de proprietário/administrador?"*

Cláusula para o contrato:

> "A vinculação do site ao Perfil da Empresa no Google depende de o cliente fornecer acesso de administrador. Caso o cliente não possua esse acesso, a recuperação/reivindicação junto ao Google é de responsabilidade exclusiva do cliente."

---

## 9. Argumentos de venda (ordem de força)

1. **Economia de comissão de OTA.** Booking/Hostelworld cobram ~15–30% por reserva. Cada hóspede que reserva direto pelo WhatsApp via site é comissão que fica no bolso do dono. Quanto mais cara a diária, mais pesa → hostels/pousadas de diária mais alta têm mais interesse.
2. **Presença digital própria.** Deixa de depender 100% de plataformas de terceiros.
3. **Controle da marca.** O site mostra o diferencial (atividades, ambiente, proposta) que a ficha do Booking achata.
4. **Vinculação ao Google.** Ao buscar o nome do hostel, aparece o site + WhatsApp, encurtando o caminho para a reserva direta.

---

## 10. Decisão técnica: CÓDIGO PRÓPRIO — implicações

Decisão tomada: construir em código próprio (não em builder tipo Wix).

### Vantagens

- Ativo de portfólio real e reutilizável (coerente com a documentação pública da transição).
- Arquitetura "build once, reuse everywhere": template fixo + dados por cliente.
- Custo marginal por cliente ≈ zero (free tiers).
- Controle total de design, SEO e performance.
- Escala por clonagem: template + trocar dados + apontar domínio.

### Riscos / passivos (mitigações registradas)

- **Dependência do cliente em mim** — passivo que vira ativo: se o cliente quiser manutenção, ele paga (por alteração avulsa — ver decisões técnicas).
- **Passivo de manutenção** — o principal risco, liga direto com o gargalo de não-finalização. Mitigação: entrega fechada + 1 rodada de ajustes; o resto é novo acordo (já no escopo).
- **Bus factor / portabilidade** — se eu paro, o hostel fica com site que ninguém mantém. Mitigação: código no GitHub + documentação mínima que permita outro dev assumir.
- **Centralização de hospedagem** — todos os clientes na minha conta Vercel = ponto único de falha. Decisão: conta única no início (aceitável); separação futura se a carteira crescer.
- **Domínio administrado por mim** — controle vs dependência. Resolvido com cláusula de transferência (seção 7). O controle é do cliente, para fazer o que quiser: contratar outro dev ou me pagar a manutenção.

### Decisões técnicas — FECHADAS em 2026-07-01

Detalhes e justificativas em [`decisoes-tecnicas.md`](decisoes-tecnicas.md).

- [x] **Stack**: Astro + Tailwind CSS, site estático, deploy Vercel (free tier).
- [x] **Fonte de dados por cliente**: `config.json` versionado, validado por schema na build. Sem CMS na v1; manutenção paga por alteração avulsa (R$ 50–150, valor exato no contrato).
- [x] **Estrutura do repo**: monorepo privado (motor + pasta por cliente), com cliente-demo fictício como vitrine.
- [x] **Estratégia de imagens**: otimização na build via `astro:assets`; fotos versionadas na pasta do cliente.
- [x] **Componentização**: hero, galeria, card de acomodação, mapa, CTA WhatsApp, nav/footer — biblioteca única compartilhada; cada variação de layout = composição de página + tema. Variação 1 primeiro; 2 e 3 depois, com feedback de cliente real.

---

## 11. Precificação e cálculo de noites (referência)

Valor de mercado do pacote (referência BR, escopo enxuto, sem motor/pagamento):

| Componente | Valor de referência |
|---|---|
| Site institucional (motor reutilizável) | R$ 1.000 – R$ 2.000 |
| Copywriting customizado | R$ 500 – R$ 1.000 |
| SEO on-page básico | incluso (baixo esforço marginal) |
| **Total do pacote** | **R$ 1.500 – R$ 3.000** |

**Fórmula de conversão em noites:**

> Nº de noites = Valor do pacote (R$) ÷ Diária do hostel específico (R$)

Exemplos com diária de R$ 100 (hostels/pousadas de diária mais alta, mais propensos a ter interesse):

| Cenário | Cálculo | Noites |
|---|---|---|
| Piso | 1.500 ÷ 100 | ~15 noites |
| Teto | 3.000 ÷ 100 | ~30 noites |

**Notas de negociação:**

- Usar a diária REAL do hostel específico, não média genérica.
- O custo real de um leito vazio para o dono é muito menor que a diária de tabela → há margem para negociar mais noites sem que pese no caixa dele.
- Travar, junto com o número de noites: janela de uso (ex.: baixa temporada) e antecedência de reserva, para não esbarrar em lotação.

**Manutenção pós-entrega (decisão registrada):** cobrada por alteração avulsa, R$ 50–150 por alteração simples (valor exato a fechar no contrato), anunciada na proposta desde o início. Pode ser aceita em noites, mantendo a lógica da permuta.

---

## 12. Estrutura do contrato de permuta

✅ **Texto redigido em 2026-07-23**: `docs/contrato-permuta.md` — modelo genérico com
placeholders, usando os valores fechados na entrevista dirigida da Fase 5
(`docs/superpowers/specs/2026-07-23-fase5-limites-permuta-design.md`). Pendente: revisão da
autora antes de usar em um contrato real.

Cláusulas cobertas:

- [x] **Objeto** — o que é entregue (remete à seção 4).
- [x] **Escopo detalhado** — INCLUI (seção 4) e NÃO INCLUI (seção 5), com os números
      atualizados pela Fase 5 (4 rodadas antes da entrega, não a "1 rodada [DEFINIR]" ainda
      escrita nas seções 4/5 abaixo — ver nota de desatualização lá).
- [x] **Contrapartida** — nº de noites, tipo de acomodação fixo, período/janela de uso,
      antecedência de reserva, prazo de validade.
- [x] **Prazo e processo de entrega** — regra dos 10 dias antes da chegada (Fase 5).
- [x] **Responsabilidades do cliente** — fornecer material (seção 6), custear domínio
      (seção 7), dar acesso ao Google (seção 8).
- [x] **Domínio e hospedagem** — quem registra, quem administra, quem paga (seção 7).
- [x] **Cláusula de portabilidade/transferência** (seção 7 + Fase 5: 30 dias, cópia isolada,
      sem revenda).
- [x] **Cláusula do Google Business Profile** (seção 8, texto reaproveitado quase verbatim).
- [x] **Rodadas de ajuste** — 4 antes da entrega; além disso, novo acordo (Fase 5).
- [x] **Saída se o cliente não gostar** — site entregue como está, noites continuam devidas
      (Fase 5, não previsto no checklist original).
- [x] **Manutenção pós-entrega** — 15 dias com 1 ajuste pequeno grátis; depois, novo acordo
      (Fase 5).
- [x] **Propriedade** — de quem é o código; uso como portfólio; preço da alteração avulsa
      fica fora do texto do contrato (ver `decisoes-tecnicas.md`, cobrança à parte).
- [x] **Formalização** — gov.br ou papel (Fase 5).

---

## 13. Próximos passos / questões em aberto

1. ~~Fechar as decisões técnicas da seção 10.~~ ✅ Fechadas em 2026-07-01 (ver `decisoes-tecnicas.md`).
2. ~~Construir o primeiro template (o motor)~~ ✅ Variação 1 completa com cliente-demo (2026-07-02): componentes compartilhados + 4 páginas (home, acomodações, sobre, localização), tema "Maré". Falta o deploy da vitrine na Vercel.
3. **Primeiro cliente real iniciado: LumeHostel (2026-07-02).** Cliente entregou só o MIV (marca). Criada a camada de **tema por cliente** (`template/src/styles/temas/<slug>.css` via alias `@tema`); aplicada a identidade do LumeHostel (cores/fontes do MIV, com fontes livres no lugar das pagas). Esqueleto navegável com conteúdo `[PROVISORIO]` e fotos placeholder. **Aguardando briefing** — pendências em `clientes/lumehostel/PENDENCIAS.md`; marca documentada em `clientes/lumehostel/marca.md`.
4. ~~Redigir documento do cliente (seção 6).~~ ✅ `docs/briefing-cliente.md` criado (2026-07-02): questionário reutilizável, com seção de identidade visual (MIV ou fallback) e política fixa de preços "consultar no WhatsApp".
5. **Site da marca construído em `site/` (2026-07-03).** Landing única para donos de hostel (manifesto → dor → proposta → escopo → como funciona → quem sou eu → CTA WhatsApp), identidade do MIV, textos aprovados pela autora. Spec: `docs/superpowers/specs/2026-07-03-site-codigo-itinerante-design.md`. **Pendente**: dados reais de contato e foto (`site/src/dados.ts`), deploy na Vercel, domínio.
6. Levantar 5–8 exemplos de sites de hostel (planilha): tem motor ou WhatsApp? quantas abas? diferencial mostrado?
   - Método: Google Maps reverso, Instagram (bio), Hostelworld/Booking, showcases de design.
7. Definir prazos e janelas (campos [DEFINIR] acima) — via entrevista dirigida, ver item 8.
8. **Estabelecer os limites de risco comercial da permuta antes de redigir** (levantado
   2026-07-20): entrevista dirigida, uma pergunta por vez, cobrindo preço/permuta, escopo,
   saída, manutenção, propriedade e formalização. Roteiro completo: Fase 5 em
   `docs/ideias-backlog.md`. Só depois disso redigir o contrato de permuta (seção 12).

### Estrutura do repositório (adotada)

```
codigo-itinerante/
├── README.md                    (índice do projeto)
├── docs/
│   ├── projeto.md               (este documento)
│   ├── decisoes-tecnicas.md     (decisões fechadas e justificativas)
│   ├── contrato-permuta.md      (a redigir)
│   └── briefing-cliente.md      (questionário para o cliente)
├── marca/                       (identidade visual: wordmark/monograma SVG, tokens.css; manual em docs/miv.md)
├── template/                    (o motor: projeto Astro reutilizável)
│   └── src/styles/temas/        (tema por cliente: <slug>.css, selecionado por CLIENTE)
└── clientes/
    ├── demo/                    (hostel fictício: config.json + fotos)
    └── lumehostel/             (1º cliente real: config.json + fotos + marca.md + PENDENCIAS.md)
```
