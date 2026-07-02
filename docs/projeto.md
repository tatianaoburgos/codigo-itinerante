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
- SEO on-page básico (title, meta description, headings, dados estruturados LocalBusiness, alt text, sitemap).
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

(esta seção vai no documento entregue AO CLIENTE, junto com a proposta/contrato)

Para construir o site, preciso que você me envie:

- [ ] **Fotos em alta resolução** — quartos, áreas comuns, fachada, arredores. A qualidade do site depende diretamente da qualidade das fotos fornecidas.
- [ ] **Descrição das acomodações** — para cada tipo de quarto: nome, capacidade, comodidades.
- [ ] **Sobre o hostel** — breve história, proposta, o que o diferencia.
- [ ] **Logo e cores da marca** (se houver).
- [ ] **Dados de contato** — número de WhatsApp, e-mail, endereço completo, Instagram/redes.
- [ ] **Valores** — faixa de preços a exibir (ou indicar se prefere "consultar valores"). Colocar como pergunta para o cliente.
- [ ] **Acesso de administrador ao Perfil da Empresa no Google** (ver seção 8).
- [ ] **Grade de atividades/serviços**, se houver (tours, café, coworking etc.) — montar lista pronta para o cliente só marcar com X, algo que facilite a vida dele.

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

## 12. Estrutura do contrato de permuta (a redigir)

Cláusulas previstas:

- [ ] **Objeto** — o que é entregue (remeter à seção 4).
- [ ] **Escopo detalhado** — INCLUI (seção 4) e NÃO INCLUI (seção 5).
- [ ] **Contrapartida** — nº de noites, período/janela de uso, antecedência de reserva, prazo de validade.
- [ ] **Prazo de entrega** — [DEFINIR].
- [ ] **Responsabilidades do cliente** — fornecer material (seção 6), custear domínio (seção 7), dar acesso ao Google (seção 8).
- [ ] **Domínio e hospedagem** — quem registra, quem administra, quem paga (seção 7).
- [ ] **Cláusula de portabilidade/transferência** (seção 7).
- [ ] **Cláusula do Google Business Profile** (seção 8).
- [ ] **Rodadas de revisão** — 1 inclusa; além disso, novo acordo.
- [ ] **Propriedade e manutenção** — de quem é o código; o que acontece após entrega; preço da alteração avulsa.

---

## 13. Próximos passos / questões em aberto

1. ~~Fechar as decisões técnicas da seção 10.~~ ✅ Fechadas em 2026-07-01 (ver `decisoes-tecnicas.md`).
2. **Construir o primeiro template (o motor)** — variação 1 completa, com cliente-demo fictício. Em andamento.
3. Levantar 5–8 exemplos de sites de hostel (planilha): tem motor ou WhatsApp? quantas abas? diferencial mostrado?
   - Método: Google Maps reverso, Instagram (bio), Hostelworld/Booking, showcases de design.
4. Definir prazos e janelas (campos [DEFINIR] acima).
5. Redigir contrato de permuta (seção 12) + documento do cliente (seção 6).

### Estrutura do repositório (adotada)

```
codigo-itinerante/
├── README.md                    (índice do projeto)
├── docs/
│   ├── projeto.md               (este documento)
│   ├── decisoes-tecnicas.md     (decisões fechadas e justificativas)
│   ├── contrato-permuta.md      (a redigir)
│   └── inputs-cliente.md        (a redigir)
├── template/                    (o motor: projeto Astro reutilizável)
└── clientes/
    └── demo/                    (hostel fictício: config.json + fotos)
```
