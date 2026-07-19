# Pendências — LumeHostel

O MIV cobre a marca (recebido — ver `marca.md`). O `config.json` foi preenchido com
dados reais levantados em fontes públicas (Booking/agregadores e Google Maps, em
2026-07-12/13): endereço, acomodações, sobre, comodidades, região, depoimentos e mapa.
O WhatsApp já é o número real (atualizado em 2026-07-14); e-mail e confirmação do
Instagram ainda dependem do Gabriel. As fotos do hostel
são reais, extraídas das presenças públicas do próprio estabelecimento (Google Maps,
aba "Do proprietário", e Booking) — proveniência de cada arquivo em `fotos/FONTES.md`;
falta a autorização formal de uso.

Desde 2026-07-13 o site é uma **one-page com âncoras** (hero → acomodações em grade →
comodidades → a região → depoimentos → localização → CTA).

## Feito

- [x] Endereço e mapa (`localizacao.endereco`, `mapsEmbedUrl`, `comoChegar`)
- [x] Acomodações — os 6 tipos reais do Booking (Dormitório Misto 6 e 8 camas, Dormitório
      Feminino 4 e 6 camas, Quarto Duplo, Suíte Standard), cada um com foto própria
- [x] Sobre (história, com base no conceito do MIV)
- [x] Comodidades (as antigas "diferenciais" foram absorvidas aqui, agora ilustradas onde há foto)
- [x] Seção "A vibe do hostel" — mosaico com 9 fotos reais do próprio estabelecimento
- [x] Seção "A região" — 6 pontos de João Pessoa com distância oficial do Booking e foto
      de licença livre
- [x] Depoimentos — 4 avaliações públicas reais do Booking (candidatas de troca levantadas
      no Google Maps e no Booking em `avaliacoes.md`, aguardando escolha)
- [x] Marca (logo/favicon/símbolo completo — estrela + chama; usado como divisor de
      seções e marca-d'água)
- [x] Tipografia única (Space Grotesk) em todo o site
- [x] Fotos reais em uso: `capa.jpg`, `cozinha.jpg`, `jardim.jpg`, as 6 fotos de
      acomodação e as 9 da seção "A vibe" (ver `fotos/FONTES.md`)

## Pendente do Gabriel — decisões

- [ ] **Manter a seção de depoimentos?** É uma área importante do site (prova social:
      são as avaliações reais dos hóspedes, e convertem). Mas é também uma área que
      **demandaria manutenção no futuro**: trocar, acrescentar ou remover um depoimento
      exige editar os dados do site e publicar de novo — não é algo que o Gabriel muda
      sozinho. Perguntar se ele quer manter a seção sabendo disso.
- [x] **Quais depoimentos entram no site.** Em 2026-07-14 foram levantadas as 10 melhores
      avaliações públicas (Google Maps e Booking) em `avaliacoes.md`; o `config.json` já
      foi atualizado com a troca (3 via Google, 1 via Booking). Falta confirmar com o
      Gabriel se os nomes devem aparecer completos ou só o primeiro nome.
- [ ] **Fonte do site.** A fonte auxiliar do MIV dele (**Arial Rounded MT Bold**) é
      proprietária da Monotype e não pode ser hospedada num site sem licença web paga.
      A autora comparou visualmente três substitutas livres e escolheu **Space Grotesk**
      — geométrica e angular, no espírito do logotipo (que usa a Ellograph CF, também
      proprietária) — usada no site inteiro (títulos e corpo). Informar isso ao Gabriel e
      registrar que ele **tem a opção de comprar a licença web de qualquer uma das duas
      fontes do MIV** se quiser a original no site.

## Pendente do Gabriel — conteúdo

- [x] **E-mail real** — atualizado para `lumehostel@gmail.com` (2026-07-15).
- [ ] **Confirmação do Instagram**. WhatsApp e e-mail já são os reais.
- [ ] **Domínio** do site — publicado em produção na Vercel em https://lumehostel.vercel.app (2026-07-15); falta domínio próprio
- [ ] **Confirmação dos textos** — validar se história, comodidades e dados das acomodações
      batem com a realidade do hostel
- [ ] **Confirmação de capacidade dos quartos privativos** — assumimos 2 pessoas para
      Quarto Duplo e Suíte Standard
- [ ] **Confirmar coworking e sala de jogos** — constam no config, mas não achamos
      confirmação de primeira mão nas fontes públicas nesta rodada
- [ ] **Autorização para uso das fotos** que vieram do Google Maps e do Booking
      (todas do perfil oficial do estabelecimento; nenhuma foto de hóspede foi usada —
      ver `fotos/FONTES.md`)
- [ ] **Acesso admin ao Perfil da Empresa no Google** (ver seção 8 de `docs/projeto.md`)

## Fotos que faltam (enviar em alta resolução)

O site é dominado por fotografia. Coworking (`coworking.jpg`) e redário (`redario.jpg`)
já têm foto própria (adicionadas em 2026-07-14). Ainda faltam:

- [ ] **Churrasqueira**
- [ ] **Sala de jogos**

Preços: não pedir — política fixa é "consultar no WhatsApp" (já aplicada, `precos.politica: "consultar"`).
