# Diretrizes de design — regras globais dos sites

Regras permanentes para TODO site que produzimos, extraídas da análise de ~30 sites de hostels/pousadas (2026-07-14, planilha "Avaliação sites hostels.xlsx" + comentários da autora). O catálogo de referências visuais por site está em `preferencias-visuais.md`.

## Princípio central

**Todo site deve parecer caro de ser feito.** Elementos de design, beleza, profundidade e ritmo — nunca cara de "site pobre, que não foi muito cobrado para ser feito". O que muda por nicho é apenas o **tom** (texto, paleta, clima, ilustrações): hostel = descontraído, pousada de família = aconchegante. A estrutura, a qualidade da construção e a assinatura visual refletem sempre um site confiável e de alto padrão. Referência do contraste: Parador (rico) vs Parador Pôr do Sol (mesma região, site pobre) — mesmo uma hospedagem barata pode ter site belo.

## SEMPRE (em todo site)

- **Hero full-bleed**: imagem em tela cheia, colada nas bordas, sem moldura/borda. Sem exceção, em qualquer nicho.
- **One-page, rolagem só vertical**: nenhum elemento exige arrastar para o lado, em desktop ou mobile. Sem carrossel horizontal de conteúdo. (Sites grandes usam rolagem horizontal porque têm dezenas de quartos/eventos; nossos clientes não têm.)
- **Todas as informações na one-page**: pouco texto, muita foto (ref.: Discovery Hostel), mas sem esconder informação atrás de cliques — nunca "abrir um monte de página" (contra-ref.: Tetris).
- **Seções com foto em tela cheia** quando o material do cliente permitir (ref.: Baguá "Conforto/Refúgio/Natureza"; Quebra-Noz casamentos — foto tomando a página com texto por cima).
- **Ritmo de composição alternado**: a cada seção o layout muda — foto metade da tela/texto na outra metade (ref.: Toca da Coruja, Mango Tree), depois inverte, depois foto full-bleed, mosaico... A cada rolada algo diferente; é isso que dá dinamismo e cara de caro (ref.: Parador, Kenoa).
- **Movimento sem vídeo**, as três técnicas juntas:
  1. Imagem fixa que a página rola por cima até ela desaparecer (ref.: Pousada Arte Colonial, Discovery);
  2. Surgimento suave de textos/fotos conforme se rola (fade/deslize discreto);
  3. O próprio layout alternado.
- **Comodidades com símbolo + descrição breve** (ref.: Baguá "No Coração da Chapada"). Os símbolos devem ser **artísticos, desenhados sob medida (SVG feito pelo Claude)** — nunca ícones literais/genéricos de biblioteca (contra-ref.: Pé no Mato).
- **Profundidade no fundo**: detalhes gráficos pertinentes ao tema no background e nas bordas da página (ref.: ondas do Surfcamp Arara; a onda atrás do texto que faltou no Mango Tree). Nunca 100% flat/branco-hospital (contra-ref.: History Hostel).
- **Depoimentos com aspas grandes** (ref.: Mango Tree).
- **Mosaico de fotos para "a vibe"** do lugar (ref.: El Misti "O melhor jeito de curtir Ipanema").
- **Localização/atrações com desenhos e detalhes**, não lista seca (ref.: El Misti "Localização privilegiada"; Ponto de Luz "Atrações ao Ar Livre").
- **Toque artístico** onde possível, dentro do que o Claude produz em SVG (ref.: Ibiti "Hospedagens que encantam e inspiram"; Yoga Encantada).
- **Consistência de cor nas fotos**: dentro do possível com o material recebido, evitar mistura de tratamentos (contra-ref.: Yoga Encantada — fotos ora alaranjadas, ora esverdeadas).
- **Contato só por WhatsApp** (wa.me) — regra do negócio, ver `decisoes-tecnicas.md`.

## NUNCA

- **Vídeo** (hero ou seções) — os clientes não terão esse material; ver "Futuro" abaixo.
- **Rolagem/arraste horizontal** em qualquer elemento.
- **Carrossel/slideshow "PowerPoint"** — fotos passando sozinhas (contra-ref.: Mango Tree, Ponto de Luz).
- **Popups** (contra-ref.: We Hostel, Ibiti — "uó, irritante").
- **Mascote/balão fixo** acompanhando o scroll com "melhor preço aqui" (contra-ref.: Quebra-Noz, Rituaali) — "cafona e desesperado".
- **Título da aba piscando** ou trocando para "volte aqui" / "1 nova mensagem" quando o visitante sai da página.
- **Página-portão** antes do site ("fazer reserva ou ir pro site" — contra-ref.: Toca da Coruja; home isolada da Books). A hero é a abertura; nunca uma página separada.
- **Emojis** — nunca, em lugar nenhum do site.
- **Embed de vídeo do YouTube** no meio da página (contra-ref.: Parador).
- **Ícones literais/genéricos de biblioteca** para comodidades ou qualquer coisa.
- **Engine de reserva** — sem disponibilidade, sem pagamento, sem OTA; só wa.me.
- **Preço no site** — política fixa: "consultar no WhatsApp".

## Futuro (fora de escopo hoje)

- **Vídeos**: se um dia um cliente tiver material próprio em vídeo, as referências bonitas de uso são Quebra-Noz (hero), Parador, Kenoa, Awasi ("Bem Estar Ativo" — vídeo em tela cheia), UXUA ("o hero mais lindo que já vi").
- **Argumento comercial**: o Mango Tree tem site institucional + página de reservas separada. Pesquisar hostels que só têm página de reserva e montar o caso de "por que ter um site institucional além da página de reserva".
