# Fase 2 — Template Word com a assinatura da marca

**Data**: 2026-07-20 · **Status**: aprovado pela autora

## O que é

Um gerador Python (`marca/gera_template_word.py`) que produz um único arquivo
`.docx` (`marca/template-documento.docx`) aplicando o sistema visual já
especificado em `docs/miv.md` §5 ("Documentos") a um documento-base genérico
com conteúdo placeholder. É o "arquivo-base" que a autora duplica e preenche
manualmente para gerar propostas, briefings ou contratos reais — não gera os
três documentos rotulados, e não inclui texto real de nenhum documento
comercial (essa decisão de escopo está registrada abaixo).

## Decisões (com o que foi descartado)

1. **Escopo — só o sistema visual, sem conteúdo comercial real.** O template
   traz apenas placeholders ilustrando cada estilo (título, corpo, destaque,
   metadados). *Adiado para o futuro, a pedido da autora*: definir os tipos
   de documento formais (proposta, briefing, contrato) e escrever o texto de
   cada um junto com ela — registrar isso como próxima conversa, não como
   parte desta fase.

2. **Um arquivo-base genérico, não os 3 documentos rotulados.** O rótulo do
   cabeçalho ("tipo do documento") fica como placeholder "DOCUMENTO"; a
   autora troca manualmente ao duplicar o arquivo para uso real. *Descartada*
   a opção de gerar `proposta.docx`/`briefing.docx`/`contrato.docx` já
   rotulados — decisão explícita da autora.

3. **Gerador Python (`python-docx`), não um `.docx`/`.dotx` montado à mão no
   Word.** Segue o mesmo padrão já estabelecido por `marca/gera_wordmark.py`
   e `marca/gera_icones.py`: fonte de verdade em código, regenerável,
   versionada no git. *Descartado*: montar o template manualmente na
   interface do Word — não seria reproduzível nem versionável, e quebraria o
   padrão do resto da pasta `marca/`.

4. **Fontes: instalar as famílias da marca no Windows + incorporar no
   arquivo.** *Correção sobre a aprovação inicial*: a estrutura do §5 do MIV
   (cabeçalho, metadados, corpo, rodapé) não usa itálico serifado em nenhum
   ponto — só Archivo e Martian Mono. Instrument Serif Italic fica de fora
   desta fase (seria instalada sem necessidade real; entra se um documento
   futuro pedir o acento itálico). Archivo já existe como `.ttf` em `marca/`
   (baixado para gerar os SVGs); falta baixar o `.ttf` da Martian Mono. As
   duas precisam ser instaladas no Windows para o Word renderizar
   corretamente, e o arquivo final tem as fontes incorporadas (Word suporta
   isso nativamente) para abrir igual em qualquer computador, mesmo sem as
   fontes instaladas. Como o Microsoft Word está instalado nesta máquina, a
   incorporação é automatizada via automação COM (`win32com`) ao final do
   script, sem passo manual na interface do Word. *Descartada*: usar fontes
   de sistema parecidas (ex. Trebuchet no lugar de Archivo) sem instalar
   nada — perderia fidelidade com a marca.

## Estrutura do documento (fonte: `docs/miv.md` §5)

- **Papel**: A4, fundo Papel (`#FBF9F4`), texto Tinta (`#1A1915`).
- **Cabeçalho**: wordmark claro (`marca/wordmark-claro.svg`) à esquerda; rótulo
  placeholder "DOCUMENTO" à direita, Martian Mono caps, cor Queimado
  (`#B85C2E`); régua de 2px Queimado fechando o cabeçalho embaixo.
- **Bloco de metadados**: linhas "Para / Data / Validade" — rótulo em Martian
  Mono caps 11px, cor Cinza-pedra (`#97928A`); valor em Archivo 600, Tinta.
- **Corpo**: um título de exemplo (Archivo 700), um parágrafo de texto corrido
  (Archivo 400, line-height ~1.6), e um trecho de destaque em Queimado
  negrito — todos com conteúdo placeholder que ilustra o estilo, não texto
  real de proposta/contrato.
- **Rodapé**: monograma CI (`marca/monograma-claro.svg`) à esquerda; site +
  contato ao centro; paginação "1 / 3" à direita — tudo em Martian Mono caps,
  corpo pequeno Cinza-pedra (`#97928A`), sobre régua fina de 0.5pt na mesma
  cor.

## Escopo de implementação

- Baixar o `.ttf` da Martian Mono (mesma fonte usada no site/MIV — Google
  Fonts) para `marca/`, ao lado de `archivo.ttf` já existente
  (`instrumentserif-italic.ttf` não é necessária nesta fase — ver item 4).
- Instalação das fontes automatizada por script (`marca/prepara_fontes_documento.py`),
  sem passo manual na interface do Windows/Word — deriva faces estáticas
  Regular/Bold nomeadas "Archivo Doc"/"Martian Mono Doc" a partir das fontes
  variáveis e instala por usuário.
- `marca/gera_template_word.py`: gera `marca/template-documento.docx` com a
  estrutura acima via `python-docx`, e ao final abre o arquivo via
  automação COM do Word para ativar "incorporar fontes" e resalvar.
- Registrar o entregável na seção 7 do `docs/miv.md` (que já lista o item 5
  como pendente) e marcar a Fase 2 como concluída em
  `docs/ideias-backlog.md`.
- Verificação: abrir o `.docx` gerado no Word e conferir visualmente
  cabeçalho, rodapé, réguas, cores e fontes; confirmar que o arquivo abre
  corretamente considerando as fontes incorporadas.

## Fora de escopo

- Texto real de proposta, briefing ou contrato (fase futura, com a autora).
- Os três arquivos rotulados separadamente (decisão explícita: só o
  arquivo-base).
- Qualquer automação de preenchimento (mala direta, campos dinâmicos) — é um
  documento estático que a autora edita manualmente.

## Referências

- `docs/miv.md` §5 "Documentos (proposta, briefing, contrato) — fundo claro"
  e §7 item 5 (pendência que esta fase resolve).
- Precedentes de geradores: `marca/gera_wordmark.py`, `marca/gera_icones.py`.
- Backlog: `docs/ideias-backlog.md` Fase 2.
