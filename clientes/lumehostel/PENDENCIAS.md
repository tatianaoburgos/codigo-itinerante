# Pendências — LumeHostel

O MIV cobre só a marca (já recebido — ver `marca.md`). Todo o `config.json` atual é
**conteúdo provisório** (marcado com `[PROVISORIO]`) e as fotos são **placeholders**
gerados na cor da marca, só para o preview navegável. O site real só fecha quando o
Gabriel preencher o briefing.

## O que pedir ao cliente

Enviar `docs/briefing-cliente.md` (questionário completo). Como o MIV já foi entregue,
a seção 1 (identidade visual) pode ser marcada como concluída — falta só:

- [ ] **Fotos em alta resolução** — quartos, áreas comuns, fachada, arredores.
      Obrigatória uma `fotos/capa.jpg` (imagem do hero). Substituir os placeholders.
- [ ] **Acomodações** — por tipo: nome, capacidade, comodidades (seção 4 do briefing).
- [ ] **Sobre o hostel** — história / proposta / o que diferencia (seção 3).
- [ ] **Contato** — WhatsApp (com DDD), e-mail, endereço completo, Instagram, domínio (seção 7).
- [ ] **Localização** — endereço para o mapa (gerar `mapsEmbedUrl`) e "como chegar" (seção 6).
- [ ] **Atividades/serviços** — tours, café, coworking etc. (seção 8).
- [ ] **Acesso admin ao Perfil da Empresa no Google** (ver seção 8 de `docs/projeto.md` — pedido à parte, não está no briefing).

Preços: não pedir — política fixa é "consultar no WhatsApp" (ver seção 5 do briefing).

## Placeholders a substituir no `config.json`

- `nome`/`slogan`/`descricaoSeo` — slogan já é o do MIV; revisar SEO com dados reais.
- `sobre.historia` e `sobre.diferenciais` — texto `[PROVISORIO]`.
- `acomodacoes[*]` — nomes, capacidades, comodidades e fotos `[PROVISORIO]`.
- `localizacao` — `endereco`, `mapsEmbedUrl` (hoje aponta para "Brasil"), `comoChegar`.
- `contato.whatsapp` — hoje `5583999990000` (fake); `email` — hoje `@example.com`;
  `instagram` — confirmar handle real.
- `atividades` — lista `[PROVISORIO]`.
