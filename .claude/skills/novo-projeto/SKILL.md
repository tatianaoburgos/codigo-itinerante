---
name: novo-projeto
description: Roteiro de entrevista para iniciar o site de um cliente novo — pesquisa as presenças online do hostel, confirma o que já foi respondido e pergunta o resto, sempre com opções + recomendação + referência visual.
---

# /novo-projeto — iniciar o site de um cliente novo

Roteiro para quando a autora anunciar um projeto novo. Antes de qualquer pergunta, leia:

1. `docs/diretrizes-design.md` — regras fixas (NUNCA perguntar sobre o que já é regra: hero full-bleed, one-page vertical, sem vídeo, sem carrossel, sem emojis, sem preço, só WhatsApp etc.).
2. `docs/preferencias-visuais.md` — catálogo de referências para montar as opções.
3. `docs/briefing-cliente.md` — questionário de onboarding do cliente (material, MIV, contato).

## Etapa 0 — Pesquisa (antes de perguntar qualquer coisa)

A autora fornece os links do hostel: **Google Maps, Instagram e Booking**. Pesquise-os primeiro e extraia tudo o que puder: nome, localização, tipos de acomodação, comodidades, avaliações e notas, clima/tom do lugar, identidade visual aparente (cores do logo/feed), fotos disponíveis.

**Regra de ouro do conteúdo**: tudo sobre o hostel vem exclusivamente dessas presenças online — nunca inventar informação.

**Perguntas já respondidas pela pesquisa não são perguntadas — são confirmadas.** ("Pelo Booking o hostel tem 4 tipos de quarto: X, Y, Z, W — confere?")

## Etapa 1 — Perguntas gerais (uma de cada vez)

Sempre **uma pergunta por vez**, das gerais para as específicas, para que as específicas já venham calibradas pelas respostas anteriores.

1. **Nicho / tipo de hospedagem** (provavelmente confirmável pela pesquisa): trilha/ecoturismo, praia surfista, urbano/casarão histórico, boutique urbano, festa, pousada de montanha, pousada de praia, wellness/retiro, sítio de família...
2. **Tom do site**: descontraído, aconchegante, sofisticado, artístico... (sugerir com base no nicho e no que a pesquisa mostrou do lugar). O tom muda texto, paleta e clima — nunca a qualidade estrutural.
3. **Material do cliente**: MIV? logo em que formato? fotos (quantas, de quê, qualidade)? vídeos (anotar para o futuro, sem usar agora)? Reaproveitar `docs/briefing-cliente.md`.

## Etapa 2 — Perguntas específicas (com opções + recomendação + referência visual)

Para cada uma: **2 a 4 opções, sempre com uma recomendação marcada**, pré-selecionadas a partir de `docs/preferencias-visuais.md` cruzado com nicho e tom já respondidos. **Citar sempre um site analisado como exemplo** ("como a hero do UXUA", "como o mosaico do El Misti") — ela precisa ver, não ler descrição abstrata.

4. **Paleta de cores** (partir do logo/MIV se houver; senão sugerir — lembrar que ela ama as cores da Pousada do Cais, mal executadas lá).
5. **Tipografia** (display + texto; atenção a licenças de fontes de MIV).
6. **Estilo dos símbolos/arte** (traço dos SVGs desenhados: orgânico, geométrico, temático — ref.: Baguá, Montanha Encantada, Ponto de Luz).
7. **Composição das seções** (quais seções, em que ordem, onde entram foto full-bleed, metade/metade, mosaico da vibe — em função do material fotográfico disponível).

**Quando a descrição não bastar**: oferecer **mockup HTML com toggle** para comparar as opções lado a lado — formato já aprovado por ela.

## Etapa 3 — Fechamento

Resumir as decisões num documento do cliente (`clientes/<slug>/` — seguir o padrão do LumeHostel: `marca.md`, `PENDENCIAS.md`, `fotos/FONTES.md`) e só então partir para spec/plano (brainstorming → writing-plans).
