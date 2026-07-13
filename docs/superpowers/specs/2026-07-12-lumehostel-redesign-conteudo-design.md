# LumeHostel — redesign visual (MIV terracota/âmbar) + conteúdo real

Data: 2026-07-12. Design aprovado em conversa; substitui o esqueleto `[PROVISORIO]`
por identidade fiel ao MIV e conteúdo real extraído das presenças online do hostel.

## Contexto

O tema atual do LumeHostel usa a paleta azul e conteúdo provisório aguardando
briefing. A cliente decidiu antecipar: aplicar a dupla de cores do MIV
(terracota `#c94520` + âmbar `#fcbe35`, como nas páginas do manual `lume.pdf`),
usar a marca real e preencher o site com as informações que o hostel já publica
no Booking, Instagram e Google Maps.

## Escopo

Tudo acontece em `template/src/styles/temas/lumehostel.css`,
`clientes/lumehostel/config.json` e `clientes/lumehostel/fotos/` — nenhum
componente do motor muda.

### 1. Tema visual (aprovado)

Remapear os tokens compartilhados no `@theme` do tema do cliente:

| Token | Novo valor | Papel |
|---|---|---|
| `espuma` (fundo geral) | terracota `#c94520` | fundo dominante, texto branco |
| `mare` (blocos fortes) | âmbar `#fcbe35` | hero/CTA, texto marrom-escuro `#3a1509` |
| `noite` (footer/escuro) | terracota profundo `#8f2d12` | |
| `fitinha` e `azulejo` | âmbar `#fcbe35` | destaques e links sobre terracota |
| cards brancos | âmbar ou creme `#fff3dc` | decidir no ajuste fino olhando contraste |
| `zap` | verde WhatsApp (inalterado) | funcional |

Overrides existentes (gradientes azuis etc.) são reescritos para a nova paleta.

**Tipografia:** font stack `"Arial Rounded MT Bold", "Fredoka Variable", ...`
no display e corpo — a fonte proprietária aparece para quem a tem instalada
(macOS/iOS); os demais veem as substitutas livres já self-hostadas. Sem licença
webfont (custo recorrente descartado).

**Texto:** branco sobre terracota, marrom-escuro `#3a1509` sobre âmbar —
critério é beleza + contraste (WCAG AA no mínimo para corpo de texto).

### 2. Marca

Extrair o vetor do logo de `lume.pdf` (símbolo "lume" tipo asterisco + wordmark
LUMEHOSTEL) e gerar SVGs nas duas combinações: âmbar (para fundo terracota) e
terracota (para fundo âmbar). Guardar em `clientes/lumehostel/` (pasta de marca
do cliente). Usar no header e como favicon. Plano B se a extração vetorial
falhar: recorte PNG em alta da página 3 do PDF.

### 3. Conteúdo real (fontes: Booking, agregadores, Google Maps)

Dados já levantados:

- **Endereço:** Av. Pombal, 1745 — Manaíra, João Pessoa - PB, 58038-242.
  Praia de Manaíra a ~8 min a pé.
- **Posicionamento:** hostel para nômades digitais e viajantes que buscam
  organização e tranquilidade (não é hostel de festa). Nota 10/60 avaliações
  no agregador; destaque para limpeza, coworking e equipe.
- **Acomodações (Booking):** dormitório feminino (4 e 6 camas), dormitório
  misto (6 e 8 camas), Quarto Duplo, Suíte Standard. Todos com ar-condicionado,
  lockers individuais, tomadas na cama e toalhas.
- **Comodidades:** coworking com cadeiras ergonômicas, cozinha compartilhada
  (café/açúcar/temperos de cortesia), Wi-Fi grátis, jardim com redes,
  churrasqueira, sala de jogos, depósito de bagagem. Sem café da manhã incluso.
- **Instagram:** @lumehostel.

O `config.json` é reescrito com esses dados (removendo todos os `[PROVISORIO]`),
mantendo o conceito do MIV (Segurança, Iluminação, Energia Recarregada, Porto
Seguro) no texto de "sobre". `mapsEmbedUrl` passa a apontar para o endereço real.
WhatsApp/email seguem pendentes de confirmação do Gabriel (manter placeholder
sinalizado em `PENDENCIAS.md`).

### 4. Fotos reais

Preferência por fotos do próprio hostel (são dele, é o site oficial dele):

1. **Rota principal:** fotos públicas do perfil do hostel no Google Maps
   (CDN `lh3.googleusercontent.com`, sem assinatura de query) via navegador.
2. **Rota alternativa:** a usuária salva manualmente as fotos do Booking
   (o CDN `cf.bstatic.com` exige assinatura por URL e a extensão do Chrome
   bloqueia repassar URLs com query string — não contornar o filtro).
3. **Fallback:** banco gratuito (Unsplash/Pexels) temático — quarto com
   beliche, suíte de casal, capa — como aprovado antes desta extensão de escopo.

Mapear: `capa.jpg` (fachada/área social), `quarto-1.jpg` (dormitório),
`suite-1.jpg` (quarto duplo/suíte) + fotos extras por acomodação se a
qualidade permitir. Alt text descritivo no config.

## Verificação

- Build `CLIENTE=lumehostel` passa (schema Zod valida o config).
- Preview local nas 4 páginas: paleta terracota/âmbar aplicada, logo no header,
  fotos reais carregando, contraste legível em todos os blocos.
- Nenhuma regressão no cliente `demo` (build `CLIENTE=demo` continua passando).

## Fora do escopo

- Deploy na Vercel (decisão anterior: ainda não publicar).
- Mudanças em componentes do motor ou em outros clientes.
- Dados que só o Gabriel pode confirmar (WhatsApp, email, domínio).
