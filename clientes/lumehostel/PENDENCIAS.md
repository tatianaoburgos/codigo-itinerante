# Pendências — LumeHostel

O MIV cobre a marca (recebido — ver `marca.md`). O `config.json` foi preenchido com
dados reais levantados em fontes públicas (Booking/agregadores e Google Maps, em
2026-07-12): endereço, acomodações, sobre, atividades e mapa. Contato (WhatsApp/e-mail)
segue com dados fake e as fotos ainda são placeholders — ambos dependem do Gabriel.

## Feito

- [x] Endereço e mapa (`localizacao.endereco`, `mapsEmbedUrl`, `comoChegar`)
- [x] Acomodações (4 tipos: Dormitório Misto, Dormitório Feminino, Quarto Duplo, Suíte Standard)
- [x] Sobre (história e diferenciais, com base no conceito do MIV)
- [x] Atividades/comodidades gerais
- [x] Marca (logo/favicon, seção já concluída na Task 3)

## Pendente do Gabriel

- [ ] **Confirmação de capacidade dos quartos privativos** — assumimos 2 pessoas para Quarto Duplo e Suíte Standard (validar com hostel)
- [ ] **Contato real** — WhatsApp (com DDD), e-mail e confirmação do Instagram (hoje fake/placeholder)
- [ ] **Domínio** do site
- [ ] **Confirmação dos textos** — validar se história/diferenciais/dados de acomodações batem com a realidade do hostel
- [ ] **Fotos em alta resolução** — quartos, áreas comuns, fachada, arredores. Obrigatória uma
      `fotos/capa.jpg` (imagem do hero). Substituir os placeholders atuais
      (`quarto-1.jpg` reaproveitada nos dois dormitórios, `suite-1.jpg` no duplo/suíte)
- [ ] **Autorização de uso** das fotos hoje usadas como referência (Booking/Google Maps), caso
      alguma delas venha a ser aproveitada além do placeholder
- [ ] **Acesso admin ao Perfil da Empresa no Google** (ver seção 8 de `docs/projeto.md`)

Preços: não pedir — política fixa é "consultar no WhatsApp" (já aplicada, `precos.politica: "consultar"`).
