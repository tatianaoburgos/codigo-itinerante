# Decisões técnicas — registro

Decisões fechadas em sessão de brainstorm em 2026-07-01. Resolvem os itens em aberto da seção 10 de [`projeto.md`](projeto.md).

## 1. Fonte de dados por cliente: `config.json` (sem CMS na v1)

**Decisão:** o conteúdo de cada cliente vive em `clientes/<hostel>/config.json`, versionado no repositório e validado por schema na build. Edição só pela desenvolvedora.

**Manutenção pós-entrega:** cobrada por alteração avulsa — R$ 50–150 por alteração simples (trocar texto, foto, preço), valor exato fechado no contrato e anunciado na proposta desde o início. Pode ser aceita em noites, mantendo a lógica da permuta.

**Justificativa:**
- Setup mais simples possível: nenhum serviço externo, nenhuma camada extra de aprendizado (relevante: experiência front-end iniciante).
- Elimina o suporte não remunerado de "cliente enrolado no painel do CMS".
- Transforma o passivo de manutenção em receita, como previsto na seção 10 do projeto.
- Para minimizar pedidos de alteração, evitar preço exato no site — preferir faixa de preços ou "consulte no WhatsApp" (o que muda com frequência num hostel é preço).
- Não fecha a porta do CMS: se a demanda real de edição aparecer, o conteúdo do JSON migra para um CMS headless com a mesma estrutura de dados.

## 2. Stack: Astro + Tailwind CSS, deploy Vercel (free tier)

**Decisão:** motor construído com Astro e Tailwind CSS, gerando site 100% estático. Deploy no free tier da Vercel.

**Justificativa:**
- Astro é feito para sites de conteúdo estático: componentes com sintaxe próxima de HTML (curva de aprendizado suave), HTML puro por padrão (performance e SEO excelentes).
- Content collections nativas validam o `config.json` de cada cliente com schema tipado (Zod) — a build falha com dados inválidos, avisando cedo.
- Alternativa considerada: Next.js (App Router). Descartada porque a curva React + App Router seria paga sem usar a interatividade que a justifica, alongando o caminho até a primeira entrega — e o risco nº 1 do projeto é não finalizar.
- Habilidades transferíveis (componentes, Tailwind, build estática, SEO) são as mesmas; Astro é respeitado como item de portfólio.

## 3. Variações de layout: componentes compartilhados + composições

**Decisão:** biblioteca única de componentes (hero, galeria, card de acomodação, mapa, CTA WhatsApp, nav/footer). Cada uma das 3 variações de site = uma composição de página diferente + um tema visual próprio. ~80% do código compartilhado; correção num componente beneficia as 3 variações.

**Sequência:** construir a variação 1 completa primeiro (de ponta a ponta, no ar como vitrine). Variações 2 e 3 nascem depois, idealmente com feedback de cliente real. Não é preciso ter as 3 prontas para começar a vender.

**Alternativas descartadas:** 3 temas cosméticos sobre o mesmo layout (diferenciação fraca demais); 3 templates independentes (triplica manutenção, contradiz o "build once, reuse everywhere").

## 4. Estrutura do repositório: monorepo privado

**Decisão:** um único repositório privado com o motor em `template/` e os dados de cada cliente em `clientes/<hostel>/` (config.json + fotos). Cada cliente vira um projeto separado na Vercel apontando para o mesmo repo, com variável de ambiente selecionando qual cliente buildar.

**Justificativa:**
- Uma correção no motor beneficia todos os clientes no próximo build — conserta-se uma vez, não N vezes. Alinha com o modelo de manutenção paga por alteração.
- Repo privado protege fotos e dados dos clientes. A vitrine pública do portfólio é o cliente-demo (conteúdo fictício) + os sites reais no ar.
- Portabilidade (cláusula de transferência): se um cliente pedir, exporta-se a pasta dele + o motor para um repositório próprio, sob demanda.
- Alternativa descartada: um repo por cliente — isolamento máximo, mas cada melhoria do motor teria que ser propagada manualmente repo a repo (multiplicador de manutenção).

## 5. Imagens

**Decisão:** fotos versionadas na pasta do cliente; otimização (redimensionamento, formatos modernos) na build via `astro:assets`. Alt text vem do config.json.
