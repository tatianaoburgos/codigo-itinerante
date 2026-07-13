# Pendências — LumeHostel

O MIV cobre a marca (recebido — ver `marca.md`). O `config.json` foi preenchido com
dados reais levantados em fontes públicas (Booking/agregadores e Google Maps, em
2026-07-12/13): endereço, acomodações, sobre, comodidades, região, depoimentos e mapa.
Contato (WhatsApp/e-mail) segue com dados fake e depende do Gabriel. As fotos do hostel
são reais, extraídas das presenças públicas do próprio estabelecimento (Google Maps,
aba "Do proprietário", e Booking) — proveniência de cada arquivo em `fotos/FONTES.md`;
falta a autorização formal de uso.

Desde 2026-07-13 o site é uma **one-page com âncoras** (hero → acomodações em carrossel →
comodidades → a região → depoimentos → localização → CTA).

## Feito

- [x] Endereço e mapa (`localizacao.endereco`, `mapsEmbedUrl`, `comoChegar`)
- [x] Acomodações (4 tipos: Dormitório Misto, Dormitório Feminino, Quarto Duplo, Suíte Standard)
- [x] Sobre (história, com base no conceito do MIV)
- [x] Comodidades (as antigas "diferenciais" foram absorvidas aqui, agora ilustradas onde há foto)
- [x] Seção "A região" — 6 pontos de João Pessoa com distância real e foto de licença livre
- [x] Depoimentos — 4 avaliações públicas reais do Booking
- [x] Marca (logo/favicon/símbolo; símbolo usado como divisor de seções e marca-d'água)
- [x] Fotos reais em uso: `capa.jpg`, `quarto-1.jpg`, `suite-1.jpg`, `cozinha.jpg`, `jardim.jpg`

## Pendente do Gabriel — decisões

- [ ] **Manter a seção de depoimentos?** É uma área importante do site (prova social:
      são as avaliações reais dos hóspedes, e convertem). Mas é também uma área que
      **demandaria manutenção no futuro**: trocar, acrescentar ou remover um depoimento
      exige editar os dados do site e publicar de novo — não é algo que o Gabriel muda
      sozinho. Perguntar se ele quer manter a seção sabendo disso.
- [ ] **Fonte do site.** A fonte auxiliar do MIV dele (**Arial Rounded MT Bold**) é
      proprietária da Monotype e não pode ser hospedada num site sem licença web paga.
      Escolhemos a **Fredoka** — gratuita, de código aberto e fiel ao espírito
      arredondado e amigável do manual — e ela é usada no site inteiro (títulos e corpo),
      de forma que todos os visitantes vejam exatamente a mesma coisa. Informar isso ao
      Gabriel e registrar que ele **tem a opção de comprar a licença web da fonte do MIV**
      se quiser a original no site.

## Pendente do Gabriel — conteúdo

- [ ] **Contato real** — WhatsApp (com DDD), e-mail e confirmação do Instagram (hoje fake/placeholder)
- [ ] **Domínio** do site
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

O site é dominado por fotografia, e hoje faltam fotos para ilustrar:

- [ ] **Coworking** — nenhuma foto encontrada nas fontes públicas; hoje a comodidade
      aparece sem imagem, apesar de ser o diferencial central para o público nômade digital
- [ ] **Espaço com redes** — a foto `jardim.jpg` mostra o pátio com mesas, não as redes
- [ ] **Churrasqueira**
- [ ] **Sala de jogos**
- [ ] **Dormitório Feminino** — hoje usa a mesma foto do Dormitório Misto, e no carrossel
      os dois cards ficam lado a lado com a imagem repetida
- [ ] **Quarto Duplo e Suíte Standard** — hoje compartilham a mesma foto, pelo mesmo motivo

Preços: não pedir — política fixa é "consultar no WhatsApp" (já aplicada, `precos.politica: "consultar"`).
