# Mar à Vista Hostel (Barra, Salvador) — POC para fechar a permuta

Data: 2026-07-20. Aprovado pela autora em brainstorm.

## Objetivo

Construir o **site completo** do Mar à Vista Hostel como prova de trabalho, para
abordar o dono e fechar a permuta (site em troca de hospedagem). Ainda **não houve
contato**: a peça é montada só com material público e publicada numa URL da Vercel,
para a autora mandar o link. O dono vê o site *dele* pronto, não uma promessa; a
baixa resolução das fotos públicas vira o gancho ("quer ver com as suas fotos
boas? me manda").

Reaproveita integralmente o motor `template/` e o padrão de cliente do LumeHostel
(`clientes/lumehostel/`) — este é o **segundo cliente real**, nova identidade.

## Regras de conteúdo (inegociáveis)

- **Nenhuma informação inventada sobre o hostel.** Só entra o que consta nas
  presenças públicas: Booking, Google Maps, TripAdvisor e Instagram
  (`@maravistahostel`).
- Fatos da região (distâncias, nomes) verificáveis; sem opiniões atribuídas ao
  hostel.
- Preço: política fixa "consultar no WhatsApp", sem valores no site.
- **O logo não muda.** É a única identidade concreta disponível
  (`c:\Users\tatia\Downloads\marca mar a vista.png`): círculo azul-vivo, lettering
  script azul-marinho, veleiro e gaivota em negativo branco. Usado como está;
  âncora de toda a identidade derivada.

## Fatos confirmados (fontes públicas)

- **Local:** Av. Oceânica, 171 — Barra, Salvador/BA. Casarão de frente para a
  praia; Farol da Barra a ~300 m.
- **Perfil:** hostel urbano de praia, **adults only**, social (Booking dá nota
  **9,9 para grupos**). Recepção fala PT/EN/ES.
- **Notas:** TripAdvisor 5,0 · Booking ~9,1–9,2.
- **Acomodações** (detalhe por cama, via Booking): dormitório misto (~26 m²,
  banheiro **compartilhado**), dormitório feminino (~24 m², banheiro **privativo**)
  e dormitório misto de 6 camas — todos com vista do mar, ar-condicionado, wi-fi
  grátis, tomada perto da cama; roupa de cama e banho com custo adicional.
- **Comodidades:** cozinha compartilhada 24h, lounge/sala de TV, recepção 24h,
  wi-fi grátis, beira-mar, jogos de tabuleiro/quebra-cabeças, álcool gel, ferro de
  passar roupa, serviço de limpeza diário, segurança 24h/CCTV, máquinas de venda
  automática (lanches/bebidas). Sem estacionamento.
- **Elogios recorrentes:** localização, limpeza, equipe atenciosa que dá dicas,
  cozinha equipada, wi-fi bom.
- **Contato confirmado:** WhatsApp de reservas **(71) 99983-8184**; Instagram
  [@maravistahostel](https://www.instagram.com/maravistahostel/).

## Identidade visual (decisões do brainstorm)

- **Tom:** praia descolada com cara de caro (ref.: Surfcamp Arara + tipografia
  dos Books Hostel). Voz jovem-adulta, social, explorando com leveza o trocadilho
  de marinheiro "mar à vista!".
- **Paleta:** dois azuis do logo (vivo + marinho) + branco + neutro areia (creme)
  + acento sol/âmbar. Frio do mar + quente do fim de tarde é o que dá o "caro" e
  evita o azul chapado.
- **Tipografia:** títulos em **Bricolage Grotesque** (já no `package.json` do
  `template/`), corpo em sans neutra limpa. O script do logo não é usado em texto
  corrido.
- **Motivo gráfico:** marítimo — ondas/horizonte tom sobre tom no fundo (evolução
  do `CascataOndas.astro` do Lume) + **Farol da Barra** e veleiro/gaivota do logo
  como assinaturas pontuais. Símbolos das comodidades no mesmo traço marinho,
  desenhados sob medida (nunca ícone de biblioteca).

### Mapa de tokens (`template/src/styles/temas/maravista.css`)

Aproveita a lógica de **fundo claro** do motor — evita os muitos overrides de
contraste que o Lume precisou por ter fundo saturado. Cores exatas do azul serão
amostradas do PNG do logo na implementação.

| Token | Papel | Ponto de partida |
|---|---|---|
| `--color-espuma` | fundo geral da página | areia creme `#FBF4E6` |
| `--color-sal` | seção clara | branco `#FFFFFF` |
| `--color-mare` | blocos fortes (hero/CTA/depoimentos) | azul-vivo `~#1B84C4` |
| `--color-noite` | texto escuro / footer | azul-marinho `~#14314F` |
| `--color-azulejo` | links/realces sobre claro | azul-marinho/vivo |
| `--color-fitinha` | destaque (símbolos, filetes, eyebrows) | âmbar sol `~#F2A93B` |
| `--color-zap` | WhatsApp (fixo, funcional) | `#25D366` |
| `--font-display` / `--font-corpo` | Bricolage Grotesque / sans neutra | — |

## Estrutura da página (ordem do motor)

Seções opcionais só entram se o material público as sustentar honestamente.

1. **Hero** full-bleed — melhor vista do mar da Barra (`capa.jpg`) + logo + slogan
   com o trocadilho náutico.
2. **Acomodações** — dormitórios misto/feminino (e privativo, se houver), todos
   "vista pro mar".
3. **Comodidades** (fundo claro) — história curta + comodidades com símbolos
   marinhos: cozinha 24h, recepção 24h, vista pro mar, ar-condicionado, beira-mar,
   jogos de tabuleiro, wi-fi.
4. **Destaque full-bleed #1** — frase-âncora "vista pro mar de todos os quartos".
5. **A vibe** — mosaico das áreas comuns (só se houver fotos públicas distintas
   suficientes).
6. **A região** — Farol da Barra 300 m, Porto da Barra 850 m, Pelourinho 6 km,
   Elevador Lacerda 5 km, MAM 4,7 km, praias vizinhas — com distâncias e ilustração
   marítima.
7. **Destaque full-bleed #2** — sobre a Barra/localização (opcional).
8. **Depoimentos** (bloco azul-vivo) — avaliações reais 5,0 do TripAdvisor/Booking,
   com aspas grandes.
9. **Localização** — Av. Oceânica 171; mapa embed; como chegar (aeroporto ~25 km
   etc.).
10. **CTA final** — WhatsApp de reservas (71) 99983-8184.

Entre seções: divisor com assinatura marítima (veleiro/farol).

## Fotos

- **Do hostel:** galerias públicas do Booking/Google Maps (fotos publicadas pelo
  próprio hostel; uso provisório até o dono enviar originais em alta). Proveniência
  de cada arquivo em `clientes/maravista/fotos/FONTES.md`.
- **Da região:** licença livre (Wikimedia/Unsplash), com crédito quando a licença
  exigir; crédito no `config.json`.
- `capa.jpg` obrigatória (convenção do motor: Hero + OG image).

## Dados e motor

- `config.json` do cliente validado pelo schema Zod existente.
- **Símbolos marinhos faltantes** entram em `SimboloComodidade.astro` **e** no enum
  `simbolosComodidade` de `schema.ts` (as duas edições andam juntas). Reaproveitar
  o que couber da biblioteca atual (`cozinha`, `jogos`, `bagagem`, `acolhedor`).
- **Correção de dívida do motor:** `template/src/pages/index.astro` tem o texto de
  João Pessoa hardcoded ("A poucos minutos da praia de Manaíra…"). Vira campo do
  config (ex.: `localizacao.resumo`, opcional) ou é removido, senão o Mar à Vista
  herda texto do Lume. Ajustar `schema.ts` e o `config.json` do Lume junto.
- Seções sem dados no config não renderizam (comportamento atual preservado).

## Documentos do cliente (padrão LumeHostel)

`clientes/maravista/`: `config.json`, `marca.md` (identidade: logo, paleta
hex→token, tipografia), `PENDENCIAS.md`, `avaliacoes.md` (avaliações públicas reais
coletadas), `fotos/FONTES.md`, `fotos/`, `marca/` (logo como está + favicon
derivado do círculo/veleiro).

## Pendências do dono (PENDENCIAS.md, para quando houver contato)

1. **Vídeo de drone** do Instagram (reels `DWBbxn7DtNW`) — pedir o arquivo com
   autorização de uso; se vier, é candidato a hero em vídeo (exceção prevista na
   regra de design, decisão da autora).
2. **Fotos em alta resolução** de quartos e áreas comuns.
3. **E-mail de contato** — WhatsApp já confirmado ((71) 99983-8184, formato
   `5571999838184` no config); falta e-mail. Até lá, POC usa **placeholder
   claramente marcado**.
4. Confirmar dados factuais (tipos de quarto, comodidades, política adults-only).
5. **Contexto comercial sensível (não vai ao site):** há reclamações públicas
   sobre cobrança de day use / uso do lobby antes do check-in — a autora deve saber
   antes de negociar.

## Verificação

- `cd template; $env:CLIENTE = 'maravista'; npm run dev` — sobe sem erro; inspecionar
  cada seção.
- `npm run check` — tipos.
- `$env:CLIENTE = 'maravista'; npm run build` — build estática passa.
- Conferir que o **Lume continua buildando** após as mudanças no motor
  (`CLIENTE=lumehostel`).
- Publicar projeto Vercel separado (env `CLIENTE=maravista`) → URL para a autora.

## Fora de escopo

- Domínio próprio (fica para depois do dono topar).
- Depoimento textual do dono (não existe relação ainda).
- Qualquer integração de reservas/OTAs (decisão fechada do projeto).
- Redesenhar/estilizar o logo — usado exatamente como recebido.
