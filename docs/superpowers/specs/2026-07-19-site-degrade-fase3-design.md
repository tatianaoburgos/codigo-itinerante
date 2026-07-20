# Fase 3 — Degradê de cor e iconografia no site da marca

**Data**: 2026-07-19 · **Status**: aprovado pela autora (mockup `mockups/site-splash-cor.html`)

## O que é

Redesenho visual do `site/` (landing da marca Código Itinerante): o fundo deixa de ser
breu chapado e vira um **degradê contínuo breu → âmbar** ao longo da página inteira,
revelado pela rolagem. A iconografia da marca (concluída em 2026-07-19, `marca/icones/`)
entra em escala grande ancorando seções. Sem mudanças de conteúdo ou de estrutura de
seções — é uma camada visual sobre o site existente.

## Decisões (com o que foi rejeitado)

1. **Fundo**: degradê `linear-gradient(180deg)` do breu `#0a0a09` até o âmbar `#e39a3b`,
   aplicado ao wrapper da página inteira (não por seção). Os primeiros ~40% permanecem
   praticamente pretos; a cor entra devagar pelo meio (tons de transição
   `#14100c → #241812 → #4a2a17 → #8a4a24 → #c4693f`) e o final chega no âmbar cheio.
   Rampa de referência validada no mockup:
   `0% e 22% breu · 38% #14100c · 52% #241812 · 68% #4a2a17 · 82% #8a4a24 · 91% barro · 100% âmbar`.
   - *Rejeitado*: última seção em cor sólida (Set Studio) — a autora não quis fundo
     chapado de cor; corrigir a linha correspondente do `docs/ideias-backlog.md`.
   - *Rejeitado*: mancha de tinta (feTurbulence) e halo difuso de luz — testados no
     mockup e descartados ("horrorosa"). Não reintroduzir.

2. **Exceção deliberada à regra do acento do MIV**: o site termina numa área grande de
   âmbar, flexibilizando o "nunca é uma marca laranja". Leitura registrada: o degradê é
   a lâmpada acendendo ao longo da rolagem; o âmbar é ponto de chegada, não tom geral.
   Registrar esta exceção no `docs/miv.md` quando a implementação fechar.

3. **Final em versão de papel**: quando o fundo clareia, os elementos trocam para as
   versões de fundo claro do MIV — texto em breu, ícone `-papel`, monograma claro,
   botão invertido (fundo breu, texto âmbar), links/rodapé em breu translúcido.
   A troca é estática (o final está sempre na zona clara), não precisa de JS.

4. **Iconografia em escala grande**: ícones `cheio-breu` a 72px nos três passos de
   "Como funciona" (casinha, site próprio, noites) e `icone-contato-cheio-papel` a
   88px abrindo a seção final.

5. **Menos texto, tipografia maior**: h1 até `clamp(2.6rem, 8vw, 4.5rem)`, h2 até
   `3rem`, lead `1.2rem` com `max-width` em `ch`. Cortes de texto pontuais podem
   acontecer na implementação, mas reescrita de conteúdo está fora de escopo
   (os textos foram aprovados seção por seção em 2026-07-03).

6. **Cards sobre o degradê**: fundo translúcido `rgba(22,21,19,0.72)` com borda
   `rgba(244,241,232,0.07)` em vez de grafite sólido, para o degradê respirar atrás.

## Escopo de implementação

- Tudo em `site/` (projeto Astro separado do motor): `global.css`, `Layout.astro` e os
  componentes de seção existentes. Nenhuma mudança em `template/`.
- A ordem das seções não muda (`Hero → QuemSouEu → ComoFunciona → Manifesto → Dor →
  Proposta → Escopo → CtaFinal`). O mockup mostra só 4 seções; na implementação o
  degradê cobre as 8, mantendo a mesma lógica: escuro até ~metade, âmbar só no fim.
  Ajustar a rampa a olho para que apenas `CtaFinal` (e no máximo o fim de `Escopo`)
  fique na zona clara.
- Seções intermediárias que hoje usam `bg-grafite`/`border-grafite` passam para os
  fundos translúcidos do item 6.
- Onde as seções intermediárias pedirem ícone (ex.: `ComoFunciona`), usar a biblioteca
  `marca/icones/` nas versões `-breu`.
- Verificação: build local + conferência visual em viewport desktop e mobile;
  contraste do texto na zona de transição (meio do degradê) checado a olho —
  o texto `pedra` sobre os marrons intermediários é o ponto frágil.

## Fora de escopo

- Personagem viajante, cenas ilustradas, animação da hero (Fases 1 e 4).
- Reescrita dos textos e voz autoral (ideia solta do backlog).
- Movimento reagindo à rolagem (Rauno) — fica para a Fase 4, junto da animação.
- Domínio próprio.

## Referências

- Mockup aprovado: `mockups/site-splash-cor.html` (iterações anteriores:
  `mockups/site-final-cor-cheia.html`, rejeitado).
- Backlog: `docs/ideias-backlog.md` Fase 3 · MIV: `docs/miv.md`.
