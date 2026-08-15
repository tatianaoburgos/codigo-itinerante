# pt/en/es no site da marca (`site/`) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dar ao `site/` (landing page da própria Código Itinerante) as 3 páginas (`index`, `faq`, `404`) em português, inglês e espanhol, com alternador de idioma, `hreflang`/`og:locale`/`html lang` corretos e WhatsApp localizado — mesmo padrão já em produção no motor (`template/`), adaptado à ausência de `config.json` por cliente.

**Architecture:** Roteamento i18n nativo do Astro (`/en/`, `/es/`, `/` continua pt). Todo texto fixo migra para um dicionário único (`lib/textos.ts`, 3 blocos `pt`/`en`/`es`, sem `campoLocalizavel`/fallback — aqui não existe "campo ainda não traduzido"). Um helper mínimo (`lib/i18n.ts`) resolve `Astro.currentLocale` para `'pt' | 'en' | 'es'`. Cada componente com texto cravado passa a ler `idiomaAtual(Astro.currentLocale)` e buscar sua seção em `textos[idioma]`. Um componente novo (`AlternadorIdioma.astro`) replica o padrão visual "PT / EN / ES" do `Nav.astro` do motor, sem gate de idiomas ativos (aqui os 3 sempre existem).

**Tech Stack:** Astro 7 (roteamento i18n nativo, `astro:i18n`), TypeScript, Node ≥22.12. Comandos em PowerShell, a partir de `site/`.

**Spec:** `docs/superpowers/specs/2026-08-14-site-marca-i18n-design.md`

## Global Constraints

- Escopo: só `site/` — nunca tocar `template/` nem `clientes/`.
- As 3 páginas do `site/` — `index`, `faq`, `404` — ganham pt/en/es.
- Autoria da tradução: Claude traduz o conteúdo, a autora revisa antes de publicar (mesmo método já usado no LumeHostel).
- Alternador de idioma: no topo de cada página, perto do elemento de logo/wordmark já existente ali — não no rodapé, não fixo na tela.
- Sem gate de idiomas ativos: diferente do motor (`idiomasDisponiveis` por cliente), aqui os 3 idiomas estão sempre ativos.
- Registro do espanhol: informal "tú", vocabulário latino-americano neutro (mesma correção já aplicada ao LumeHostel: "Nevera" → "Refrigerador" — evitar termos regionais da Espanha).
- `hreflang`: sempre 3 `<link rel="alternate">` (pt/en/es), via `getRelativeLocaleUrl()` — sem gate, diferente do motor.
- `og:locale`/`html lang` por mapa fixo: `{ pt: 'pt_BR', en: 'en_US', es: 'es_ES' }` / `{ pt: 'pt-BR', en: 'en', es: 'es' }`.
- Alt texts de nome próprio (`alt="Código Itinerante"`) ficam hardcoded nos componentes, iguais nos 3 idiomas — não entram no dicionário. Alt texts descritivos (foto da Tatiana, screenshots do LumeHostel) entram no dicionário e são traduzidos.
- Nomes próprios de lugar/produto (ex. "LumeHostel — João Pessoa, PB") não mudam entre idiomas.
- `canonical` já funciona sem mudança (deriva de `Astro.url.pathname`); sitemap já pega rotas i18n automaticamente via `@astrojs/sitemap`, sem configuração extra (confirmado no motor).
- Sem framework de testes no projeto (`CLAUDE.md`: "Não há testes nem linter configurados ainda") — verificação usa `npm run check`, builds reais (`npm run build` dentro de `site/`) e inspeção do `dist/` gerado via `Select-String`. Comandos em PowerShell, a partir de `site/`.
- Fora de escopo (não implementar): detecção automática de idioma do navegador, domínio/subdomínio dedicado por idioma, revisão de espanhol/inglês por falante nativo terceirizado.

---

## Task 1: `lib/i18n.ts` — helper de idioma

**Files:**
- Create: `site/src/lib/i18n.ts`

**Interfaces:**
- Consumes: nada (task raiz).
- Produces: `idiomas` (`['pt', 'en', 'es'] as const`), `Idioma` (tipo `'pt' | 'en' | 'es'`), `idiomaAtual(currentLocale: string | undefined): Idioma` — usado por todo componente/página das Tasks 3-16.

- [x] **Step 1: Criar o arquivo**

```ts
export const idiomas = ['pt', 'en', 'es'] as const;
export type Idioma = (typeof idiomas)[number];

/** Normaliza `Astro.currentLocale` (pode vir undefined) para um Idioma válido, com pt como padrão. */
export function idiomaAtual(currentLocale: string | undefined): Idioma {
  return currentLocale !== undefined && (idiomas as readonly string[]).includes(currentLocale)
    ? (currentLocale as Idioma)
    : 'pt';
}
```

- [x] **Step 2: Verificar com script descartável**

Criar `site/_verificar_i18n.ts`:

```ts
import { idiomaAtual } from './src/lib/i18n';

let falhas = 0;
const casos: Array<[string | undefined, string]> = [
  [undefined, 'pt'],
  ['pt', 'pt'],
  ['en', 'en'],
  ['es', 'es'],
  ['fr', 'pt'],
];
for (const [entrada, esperado] of casos) {
  const resultado = idiomaAtual(entrada);
  if (resultado !== esperado) {
    console.error(`FALHOU: idiomaAtual(${JSON.stringify(entrada)}) = "${resultado}", esperado "${esperado}"`);
    falhas++;
  }
}
if (falhas > 0) { console.error(`${falhas} caso(s) falharam.`); process.exit(1); }
console.log('i18n: todos os casos passaram.');
```

Run (a partir de `site/`): `node --experimental-strip-types _verificar_i18n.ts`
Expected: `i18n: todos os casos passaram.`

Apagar depois: `Remove-Item _verificar_i18n.ts`.

- [x] **Step 3: `npm run check`**

Run (a partir de `site/`): `npm run check`
Expected: passa sem erro (arquivo novo, ainda sem consumidores — nada quebra).

- [x] **Step 4: Commit**

```bash
git add site/src/lib/i18n.ts
git commit -m "Adiciona helper de idioma ao site da marca"
```

---

## Task 2: `lib/textos.ts` — dicionário completo pt/en/es

**Files:**
- Create: `site/src/lib/textos.ts`

**Interfaces:**
- Consumes: nada.
- Produces: `textos.pt`/`textos.en`/`textos.es`, cada um com as chaves `layout`, `meta.{home,faq,pagina404}`, `botaoWhatsApp`, `hero`, `quemSouEu`, `provaDeTrabalho`, `comoFunciona`, `manifesto`, `dor`, `proposta`, `escopo`, `ctaFinal`, `faq`, `pagina404` — consumidas pelas Tasks 4-16.

- [x] **Step 1: Criar o arquivo**

```ts
export const textos = {
  pt: {
    layout: {
      descricaoNegocio:
        'Construção de sites institucionais para hostels e pousadas, pagos em noites de hospedagem.',
    },
    meta: {
      home: {
        titulo: 'Código Itinerante — sites para hostels, pagos em noites',
        descricao:
          'Construo o site institucional do seu hostel em troca de noites de hospedagem. Sem dinheiro envolvido. Reserva direta pelo WhatsApp, sem comissão de plataforma.',
      },
      faq: {
        titulo: 'Perguntas frequentes — Código Itinerante',
        descricao:
          'Quantas noites, o que acontece se você não gostar, quem paga o quê — as dúvidas mais comuns sobre o site em troca de hospedagem.',
      },
      pagina404: {
        titulo: 'Página não encontrada — Código Itinerante',
        descricao: 'Essa página não existe. Volte para a home do Código Itinerante.',
      },
    },
    botaoWhatsApp: {
      rotuloPadrao: 'Chamar no WhatsApp',
      mensagem: 'Oi! Tenho um hostel e quero saber mais sobre a permuta.',
    },
    hero: {
      tituloPre: 'Sites para hostels, pagos em ',
      tituloDestaque: 'noites',
      paragrafo:
        'Eu construo o site institucional do seu hostel — e você me hospeda por algumas noites. Sem dinheiro envolvido. O site é seu, pra sempre.',
    },
    quemSouEu: {
      eyebrowTexto: 'quem',
      eyebrowDestaque: 'sou eu',
      fotoAlt: 'Tatiana Burgos sorrindo em uma paisagem de gêiseres no altiplano',
      paragrafo:
        'Trabalho como especialista em Ciência de Dados no Ministério da Gestão e da Inovação e, ao mesmo tempo, viajo pelo Brasil me hospedando em hostels. Essa combinação me deixa ver os hostels pelos dois lados: como hóspede e como profissional que constrói soluções digitais.',
      citacao:
        'Eu não estou construindo um site para um hostel que conheci por uma reunião de vídeo. Eu provavelmente dormi em um lugar como o seu na semana passada — e vou dormir em outro na semana que vem. Conheço a jornada do hóspede porque ela também é a minha.',
      linkedinLabel: 'Me encontre no LinkedIn',
    },
    provaDeTrabalho: {
      eyebrowTexto: 'o',
      eyebrowDestaque: 'resultado',
      altDesktop: 'Primeira dobra do site do LumeHostel vista no computador',
      altMobile: 'O mesmo site do LumeHostel visto no celular',
      cardTitulo: 'LumeHostel — João Pessoa, PB',
      paragrafo:
        'O site completo do LumeHostel: acomodações, comodidades, a região, depoimentos e localização, com reserva direta pelo WhatsApp.',
      verSiteLabel: 'Ver o site no ar',
    },
    comoFunciona: {
      eyebrowTexto: 'como',
      eyebrowDestaque: 'funciona',
      passos: [
        { titulo: 'Conversamos no WhatsApp', texto: 'Você me conta do hostel e fechamos juntos o acordo de noites.' },
        {
          titulo: 'Briefing e fotos',
          texto:
            'Você preenche um formulário rápido sobre o hostel e me envia as fotos em alta qualidade. Quanto melhores as fotos, mais bonito o site fica.',
        },
        { titulo: 'Quinze dias de construção', texto: 'Eu escrevo os textos, monto o site e você acompanha.' },
        { titulo: 'Site no ar, tudo seu', texto: 'Domínio no seu nome, site sob seu controle total.' },
      ],
    },
    manifesto: {
      eyebrowTexto: 'o',
      eyebrowDestaque: 'manifesto',
      paragrafo1: 'Código Itinerante nasceu de uma troca simples.',
      paragrafo2:
        'Eu viajo o Brasil construindo soluções digitais para negócios reais — e recebo em troca o que preciso na estrada: um lugar pra ficar. Por onde minhas pernas andam, o projeto chega. Não quero só passar pelos lugares; quero fazer parte deles.',
      paragrafo3Pre: 'Começando por quem me recebe toda semana:',
      paragrafo3Destaque: 'hostels',
    },
    dor: {
      eyebrowTexto: 'o',
      eyebrowDestaque: 'problema',
      paragrafo:
        'Muitas vezes eu queria reservar diretamente com o hostel, pois sabia que ficaria mais barato para mim e melhor para o negócio. Procurava o WhatsApp, tentava encontrar fotos confiáveis, entender os quartos, confirmar a localização. As informações estavam espalhadas entre redes sociais, mapas e plataformas de reserva. Depois de um tempo procurando, eu desistia — e reservava pela plataforma.',
      boxPre: 'Isso é comissão: ',
      boxForte: 'de 10% a 25% por reserva',
      boxPos: ', direto do bolso do hostel. Cada hóspede que reserva pelo seu WhatsApp é comissão que fica com você.',
    },
    proposta: {
      eyebrowTexto: 'a',
      eyebrowDestaque: 'proposta',
      paragrafo1:
        'Eu construo o site institucional completo do seu hostel — páginas, textos, fotos organizadas, botão de reserva direta pelo WhatsApp — e você me paga em noites de hospedagem.',
      destaque: 'É uma troca temporária por um produto permanente.',
      paragrafo3: 'Sem dinheiro envolvido. O único custo é o registro do domínio — que é seu e fica com você.',
    },
    escopo: {
      eyebrowTexto: 'o que você',
      eyebrowDestaque: 'recebe',
      incluiTitulo: 'Está incluído',
      naoIncluiTitulo: 'Não está incluído',
      inclui: [
        'Site responsivo, bonito no celular e no computador',
        'Acomodações, sobre o hostel, localização com mapa e contato',
        'Textos escritos por mim a partir do seu briefing',
        'Botão de reserva direta pelo seu WhatsApp',
        'SEO básico: seu hostel bem apresentado no Google',
        'Vinculação ao Perfil da Empresa no Google',
        'Domínio registrado e configurado',
        'Quatro rodadas de ajuste durante a construção',
      ],
      naoInclui: [
        'Motor de reservas com calendário e disponibilidade',
        'Pagamento online',
        'Integração com plataformas de reserva',
        'Manutenção contínua (alterações futuras são combinadas à parte)',
        'Produção de fotos profissionais',
        'Tráfego pago e gestão de redes sociais',
      ],
      duvidasPre: 'Ainda com dúvidas? ',
      duvidasLink: 'Veja as perguntas frequentes →',
    },
    ctaFinal: {
      tituloPre: 'Tem um hostel? Vamos ',
      tituloDestaque: 'conversar',
      paragrafo: 'Me chama no WhatsApp e me conta do seu hostel. A conversa não custa nada — nem depois dela.',
    },
    faq: {
      tituloPre: 'Perguntas ',
      tituloDestaque: 'frequentes',
      naoAchou: 'Não achou sua dúvida?',
      perguntas: [
        {
          pergunta: 'Quantas noites custa o site?',
          resposta:
            'Depende da diária real do seu hostel. Calculamos juntos e fechamos esse número já na conversa inicial no WhatsApp, antes de qualquer trabalho começar.',
        },
        {
          pergunta: 'Preciso ter fotos profissionais?',
          resposta:
            'Não precisa ser produção profissional — mas o site fica exatamente tão bonito quanto as fotos e vídeos que você me manda. Não existe mágica que transforme material feio em site bonito. Se as fotos do seu hostel já são boas, mesmo tiradas com celular, isso já basta.',
        },
        {
          pergunta: 'E se eu não gostar do resultado?',
          resposta:
            'Você acompanha a construção e tem direito a quatro rodadas de revisão ao longo do processo — não é só uma olhada no fim. Depois que usarmos essas rodadas e o site for entregue, ele já reflete o que ajustamos juntos.',
        },
        {
          pergunta: 'Existe contrato?',
          resposta:
            'Sim. A gente assina um combinado simples, em linguagem clara — sem juridiquês — antes de eu começar a trabalhar. Ele deixa escrito o que cada lado faz, os prazos e o que acontece em cada situação. Pode ser assinado eletronicamente ou em papel, como você preferir.',
        },
        {
          pergunta: 'Quais são os meus custos, além das noites?',
          resposta:
            'Só um: o domínio .com.br do seu hostel (em torno de R$40 por ano) — que já nasce registrado em seu nome. Depois da entrega, você ainda tem 15 dias com direito a um ajuste pequeno gratuito — trocar uma foto, corrigir um texto. Mudanças maiores, ou depois desse prazo, combinamos à parte.',
        },
        {
          pergunta: 'De quem é o domínio e o código do site?',
          resposta:
            'O domínio é seu desde o início — você mesmo registra, com seu CPF ou CNPJ, seguindo minhas instruções. O código roda na minha hospedagem, mas o site é feito pra você: se um dia quiser levar pra outro desenvolvedor, eu preparo uma cópia independente do seu site pra isso, sem custo, dentro do prazo combinado no contrato.',
        },
        {
          pergunta: 'Até quando o site fica no ar?',
          resposta:
            'O site fica no ar sem prazo — mesmo que você ainda não tenha migrado pra um domínio próprio. Ele só sai do ar se você pedir, ou se eu pedir. E ele também aparece como case real no meu portfólio, aqui no codigoitinerante.com.br.',
        },
      ],
    },
    pagina404: {
      titulo: 'Essa página não existe.',
      texto: 'Talvez o endereço tenha mudado, ou você tenha digitado errado.',
      voltarLabel: 'Voltar para a home',
    },
  },
  en: {
    layout: {
      descricaoNegocio: 'Building institutional websites for hostels and guesthouses, paid in nights of lodging.',
    },
    meta: {
      home: {
        titulo: 'Código Itinerante — hostel websites, paid in nights',
        descricao:
          "I build your hostel's institutional website in exchange for nights of lodging. No money involved. Direct booking on WhatsApp, no platform commission.",
      },
      faq: {
        titulo: 'Frequently Asked Questions — Código Itinerante',
        descricao:
          "How many nights, what happens if you don't like it, who pays for what — the most common questions about the site-for-lodging trade.",
      },
      pagina404: {
        titulo: 'Page not found — Código Itinerante',
        descricao: "This page doesn't exist. Go back to Código Itinerante's homepage.",
      },
    },
    botaoWhatsApp: {
      rotuloPadrao: 'Message on WhatsApp',
      mensagem: "Hi! I have a hostel and I'd like to know more about the trade.",
    },
    hero: {
      tituloPre: 'Websites for hostels, paid in ',
      tituloDestaque: 'nights',
      paragrafo:
        "I build your hostel's website — and you host me for a few nights in return. No money involved. The site is yours, for good.",
    },
    quemSouEu: {
      eyebrowTexto: 'who',
      eyebrowDestaque: 'I am',
      fotoAlt: 'Tatiana Burgos smiling in a geyser landscape on the altiplano',
      paragrafo:
        "I work as a Data Science specialist at Brazil's Ministry of Management and Innovation, and at the same time I travel around Brazil staying in hostels. That combination lets me see hostels from both sides: as a guest, and as a professional who builds digital solutions.",
      citacao:
        "I'm not building a website for a hostel I met over a video call. I probably slept in a place like yours last week — and I'll sleep in another one next week. I know the guest's journey because it's also mine.",
      linkedinLabel: 'Find me on LinkedIn',
    },
    provaDeTrabalho: {
      eyebrowTexto: 'the',
      eyebrowDestaque: 'result',
      altDesktop: 'First screen of the LumeHostel website seen on a computer',
      altMobile: 'The same LumeHostel website seen on a phone',
      cardTitulo: 'LumeHostel — João Pessoa, PB',
      paragrafo:
        'The full LumeHostel website: rooms, amenities, the area, reviews, and location, with direct booking on WhatsApp.',
      verSiteLabel: 'See the live site',
    },
    comoFunciona: {
      eyebrowTexto: 'how',
      eyebrowDestaque: 'it works',
      passos: [
        { titulo: 'We talk on WhatsApp', texto: 'You tell me about your hostel and together we close the deal on nights.' },
        {
          titulo: 'Briefing and photos',
          texto:
            'You fill out a quick form about your hostel and send me high-quality photos. The better the photos, the better the site looks.',
        },
        { titulo: 'Fifteen days of building', texto: 'I write the copy, build the site, and you follow along.' },
        { titulo: 'Site live, all yours', texto: 'Domain in your name, site fully under your control.' },
      ],
    },
    manifesto: {
      eyebrowTexto: 'the',
      eyebrowDestaque: 'manifesto',
      paragrafo1: 'Código Itinerante was born from a simple trade.',
      paragrafo2:
        "I travel around Brazil building digital solutions for real businesses — and in exchange, I get what I need on the road: a place to stay. Wherever my legs take me, the project goes too. I don't just want to pass through places; I want to be part of them.",
      paragrafo3Pre: 'Starting with whoever hosts me every week:',
      paragrafo3Destaque: 'hostels',
    },
    dor: {
      eyebrowTexto: 'the',
      eyebrowDestaque: 'problem',
      paragrafo:
        "Many times I wanted to book directly with the hostel, because I knew it would be cheaper for me and better for the business. I'd look for a WhatsApp number, try to find trustworthy photos, understand the rooms, confirm the location. The information was scattered across social media, maps, and booking platforms. After a while of searching, I'd give up — and book through the platform.",
      boxPre: "That's commission: ",
      boxForte: '10% to 25% per booking',
      boxPos: ", straight out of the hostel's pocket. Every guest who books through your WhatsApp is commission that stays with you.",
    },
    proposta: {
      eyebrowTexto: 'the',
      eyebrowDestaque: 'proposal',
      paragrafo1:
        "I build your hostel's complete institutional website — pages, copy, organized photos, a direct WhatsApp booking button — and you pay me in nights of lodging.",
      destaque: "It's a temporary trade for a permanent product.",
      paragrafo3: 'No money involved. The only cost is the domain registration — which is yours to keep.',
    },
    escopo: {
      eyebrowTexto: 'what you',
      eyebrowDestaque: 'get',
      incluiTitulo: "What's included",
      naoIncluiTitulo: "What's not included",
      inclui: [
        'Responsive site, beautiful on phone and computer',
        'Rooms, about the hostel, location with map, and contact',
        'Copy written by me based on your briefing',
        'Direct booking button through your WhatsApp',
        'Basic SEO: your hostel well presented on Google',
        'Linked to your Google Business Profile',
        'Domain registered and configured',
        'Four rounds of adjustments during the build',
      ],
      naoInclui: [
        'Booking engine with calendar and availability',
        'Online payment',
        'Integration with booking platforms',
        'Ongoing maintenance (future changes are arranged separately)',
        'Professional photo production',
        'Paid traffic and social media management',
      ],
      duvidasPre: 'Still have questions? ',
      duvidasLink: 'See the FAQ →',
    },
    ctaFinal: {
      tituloPre: "Have a hostel? Let's ",
      tituloDestaque: 'talk',
      paragrafo: 'Message me on WhatsApp and tell me about your hostel. The conversation costs nothing — not even afterward.',
    },
    faq: {
      tituloPre: 'Frequently Asked ',
      tituloDestaque: 'Questions',
      naoAchou: "Didn't find your question?",
      perguntas: [
        {
          pergunta: 'How many nights does the site cost?',
          resposta:
            "It depends on your hostel's actual nightly rate. We work it out together and settle on that number right in our first WhatsApp conversation, before any work begins.",
        },
        {
          pergunta: 'Do I need professional photos?',
          resposta:
            "It doesn't have to be a professional production — but the site ends up exactly as good-looking as the photos and videos you send me. There's no magic that turns bad material into a beautiful site. If your hostel's photos are already good, even if shot on a phone, that's enough.",
        },
        {
          pergunta: "What if I don't like the result?",
          resposta:
            "You follow the build and get four rounds of revisions throughout the process — not just one look at the end. By the time we've used those rounds and the site is delivered, it already reflects what we adjusted together.",
        },
        {
          pergunta: 'Is there a contract?',
          resposta:
            'Yes. We sign a simple agreement, in plain language — no legalese — before I start working. It spells out what each side does, the timelines, and what happens in each situation. It can be signed electronically or on paper, whichever you prefer.',
        },
        {
          pergunta: 'What are my costs, besides the nights?',
          resposta:
            "Just one: your hostel's .com.br domain (around R$40 per year) — registered in your name from the start. After delivery, you still get 15 days with the right to one small free adjustment — swapping a photo, fixing some text. Bigger changes, or requests after that window, are arranged separately.",
        },
        {
          pergunta: "Who owns the domain and the site's code?",
          resposta:
            "The domain is yours from the start — you register it yourself, with your CPF or CNPJ (Brazilian tax ID), following my instructions. The code runs on my hosting, but the site is built for you: if you ever want to take it to another developer, I'll prepare an independent copy of your site for that, at no cost, within the timeframe set out in the contract.",
        },
        {
          pergunta: 'How long does the site stay online?',
          resposta:
            "The site stays online indefinitely — even if you haven't migrated to your own domain yet. It only comes down if you ask, or if I ask. And it also shows up as a real case study in my portfolio, here at codigoitinerante.com.br.",
        },
      ],
    },
    pagina404: {
      titulo: "This page doesn't exist.",
      texto: 'Maybe the address changed, or you typed it wrong.',
      voltarLabel: 'Back to the homepage',
    },
  },
  es: {
    layout: {
      descricaoNegocio:
        'Construcción de sitios web institucionales para hostels y posadas, pagados en noches de hospedaje.',
    },
    meta: {
      home: {
        titulo: 'Código Itinerante — sitios web para hostels, pagados en noches',
        descricao:
          'Construyo el sitio web institucional de tu hostel a cambio de noches de hospedaje. Sin dinero de por medio. Reserva directa por WhatsApp, sin comisión de plataforma.',
      },
      faq: {
        titulo: 'Preguntas frecuentes — Código Itinerante',
        descricao:
          'Cuántas noches, qué pasa si no te gusta, quién paga qué — las dudas más comunes sobre el sitio a cambio de hospedaje.',
      },
      pagina404: {
        titulo: 'Página no encontrada — Código Itinerante',
        descricao: 'Esta página no existe. Vuelve al inicio de Código Itinerante.',
      },
    },
    botaoWhatsApp: {
      rotuloPadrao: 'Escribir por WhatsApp',
      mensagem: '¡Hola! Tengo un hostel y quiero saber más sobre el intercambio.',
    },
    hero: {
      tituloPre: 'Sitios web para hostels, pagados en ',
      tituloDestaque: 'noches',
      paragrafo:
        'Yo construyo el sitio web institucional de tu hostel — y tú me hospedas por algunas noches. Sin dinero de por medio. El sitio es tuyo, para siempre.',
    },
    quemSouEu: {
      eyebrowTexto: 'quién',
      eyebrowDestaque: 'soy',
      fotoAlt: 'Tatiana Burgos sonriendo en un paisaje de géiseres en el altiplano',
      paragrafo:
        'Trabajo como especialista en Ciencia de Datos en el Ministerio de Gestión e Innovación de Brasil y, al mismo tiempo, viajo por Brasil hospedándome en hostels. Esa combinación me deja ver los hostels desde los dos lados: como huésped y como profesional que construye soluciones digitales.',
      citacao:
        'No estoy construyendo un sitio web para un hostel que conocí en una videollamada. Probablemente dormí en un lugar como el tuyo la semana pasada — y voy a dormir en otro la semana que viene. Conozco el recorrido del huésped porque también es el mío.',
      linkedinLabel: 'Encuéntrame en LinkedIn',
    },
    provaDeTrabalho: {
      eyebrowTexto: 'el',
      eyebrowDestaque: 'resultado',
      altDesktop: 'Primera pantalla del sitio de LumeHostel vista en la computadora',
      altMobile: 'El mismo sitio de LumeHostel visto en el celular',
      cardTitulo: 'LumeHostel — João Pessoa, PB',
      paragrafo:
        'El sitio completo de LumeHostel: habitaciones, comodidades, la zona, reseñas y ubicación, con reserva directa por WhatsApp.',
      verSiteLabel: 'Ver el sitio en vivo',
    },
    comoFunciona: {
      eyebrowTexto: 'cómo',
      eyebrowDestaque: 'funciona',
      passos: [
        { titulo: 'Conversamos por WhatsApp', texto: 'Me cuentas sobre tu hostel y juntos cerramos el acuerdo de noches.' },
        {
          titulo: 'Brief y fotos',
          texto:
            'Completas un formulario rápido sobre tu hostel y me envías las fotos en alta calidad. Cuanto mejores las fotos, más bonito queda el sitio.',
        },
        { titulo: 'Quince días de construcción', texto: 'Yo escribo los textos, armo el sitio y tú lo vas siguiendo.' },
        { titulo: 'Sitio en línea, todo tuyo', texto: 'Dominio a tu nombre, sitio bajo tu control total.' },
      ],
    },
    manifesto: {
      eyebrowTexto: 'el',
      eyebrowDestaque: 'manifiesto',
      paragrafo1: 'Código Itinerante nació de un intercambio simple.',
      paragrafo2:
        'Viajo por Brasil construyendo soluciones digitales para negocios reales — y a cambio recibo lo que necesito en el camino: un lugar donde quedarme. A donde van mis piernas, llega el proyecto. No quiero solo pasar por los lugares; quiero ser parte de ellos.',
      paragrafo3Pre: 'Empezando por quienes me reciben cada semana:',
      paragrafo3Destaque: 'hostels',
    },
    dor: {
      eyebrowTexto: 'el',
      eyebrowDestaque: 'problema',
      paragrafo:
        'Muchas veces quise reservar directamente con el hostel, porque sabía que sería más barato para mí y mejor para el negocio. Buscaba el WhatsApp, trataba de encontrar fotos confiables, entender las habitaciones, confirmar la ubicación. La información estaba dispersa entre redes sociales, mapas y plataformas de reserva. Después de un rato buscando, me rendía — y reservaba por la plataforma.',
      boxPre: 'Eso es comisión: ',
      boxForte: 'de 10% a 25% por reserva',
      boxPos: ', directo del bolsillo del hostel. Cada huésped que reserva por tu WhatsApp es comisión que se queda contigo.',
    },
    proposta: {
      eyebrowTexto: 'la',
      eyebrowDestaque: 'propuesta',
      paragrafo1:
        'Yo construyo el sitio web institucional completo de tu hostel — páginas, textos, fotos organizadas, botón de reserva directa por WhatsApp — y tú me pagas en noches de hospedaje.',
      destaque: 'Es un intercambio temporal por un producto permanente.',
      paragrafo3: 'Sin dinero de por medio. El único costo es el registro del dominio — que es tuyo y se queda contigo.',
    },
    escopo: {
      eyebrowTexto: 'lo que',
      eyebrowDestaque: 'recibes',
      incluiTitulo: 'Qué incluye',
      naoIncluiTitulo: 'Qué no incluye',
      inclui: [
        'Sitio responsivo, bonito en el celular y en la computadora',
        'Habitaciones, sobre el hostel, ubicación con mapa y contacto',
        'Textos escritos por mí a partir de tu briefing',
        'Botón de reserva directa por tu WhatsApp',
        'SEO básico: tu hostel bien presentado en Google',
        'Vinculación con el Perfil de Empresa en Google',
        'Dominio registrado y configurado',
        'Cuatro rondas de ajustes durante la construcción',
      ],
      naoInclui: [
        'Motor de reservas con calendario y disponibilidad',
        'Pago en línea',
        'Integración con plataformas de reserva',
        'Mantenimiento continuo (los cambios futuros se acuerdan aparte)',
        'Producción de fotos profesionales',
        'Tráfico pago y gestión de redes sociales',
      ],
      duvidasPre: '¿Todavía tienes dudas? ',
      duvidasLink: 'Ver las preguntas frecuentes →',
    },
    ctaFinal: {
      tituloPre: '¿Tienes un hostel? Vamos a ',
      tituloDestaque: 'conversar',
      paragrafo: 'Escríbeme por WhatsApp y cuéntame sobre tu hostel. La conversación no cuesta nada — ni siquiera después.',
    },
    faq: {
      tituloPre: 'Preguntas ',
      tituloDestaque: 'frecuentes',
      naoAchou: '¿No encontraste tu duda?',
      perguntas: [
        {
          pergunta: '¿Cuántas noches cuesta el sitio?',
          resposta:
            'Depende de la tarifa real por noche de tu hostel. Lo calculamos juntos y cerramos ese número ya en la primera conversación por WhatsApp, antes de que empiece cualquier trabajo.',
        },
        {
          pergunta: '¿Necesito tener fotos profesionales?',
          resposta:
            'No hace falta que sea una producción profesional — pero el sitio queda exactamente tan bonito como las fotos y videos que me envíes. No existe magia que convierta material feo en un sitio bonito. Si las fotos de tu hostel ya son buenas, aunque sean tomadas con el celular, eso ya es suficiente.',
        },
        {
          pergunta: '¿Y si no me gusta el resultado?',
          resposta:
            'Tú sigues la construcción y tienes derecho a cuatro rondas de revisión a lo largo del proceso — no es solo un vistazo al final. Cuando ya hayamos usado esas rondas y el sitio sea entregado, este ya refleja lo que ajustamos juntos.',
        },
        {
          pergunta: '¿Existe un contrato?',
          resposta:
            'Sí. Firmamos un acuerdo simple, en lenguaje claro — sin tecnicismos legales — antes de que yo empiece a trabajar. Deja por escrito qué hace cada parte, los plazos y qué pasa en cada situación. Puede firmarse electrónicamente o en papel, como prefieras.',
        },
        {
          pergunta: '¿Cuáles son mis costos, además de las noches?',
          resposta:
            'Solo uno: el dominio .com.br de tu hostel (alrededor de R$40 por año) — que ya nace registrado a tu nombre. Después de la entrega, todavía tienes 15 días con derecho a un ajuste pequeño gratuito — cambiar una foto, corregir un texto. Cambios más grandes, o después de ese plazo, se acuerdan aparte.',
        },
        {
          pergunta: '¿De quién es el dominio y el código del sitio?',
          resposta:
            'El dominio es tuyo desde el principio — tú mismo lo registras, con tu CPF o CNPJ (identificación fiscal brasileña), siguiendo mis instrucciones. El código corre en mi hosting, pero el sitio está hecho para ti: si algún día quieres llevarlo a otro desarrollador, preparo una copia independiente de tu sitio para eso, sin costo, dentro del plazo acordado en el contrato.',
        },
        {
          pergunta: '¿Hasta cuándo el sitio queda en línea?',
          resposta:
            'El sitio queda en línea sin plazo — incluso si todavía no migraste a un dominio propio. Solo sale de línea si tú lo pides, o si yo lo pido. Y también aparece como caso real en mi portafolio, aquí en codigoitinerante.com.br.',
        },
      ],
    },
    pagina404: {
      titulo: 'Esta página no existe.',
      texto: 'Tal vez la dirección cambió, o la escribiste mal.',
      voltarLabel: 'Volver al inicio',
    },
  },
} as const;
```

- [x] **Step 2: Verificar paridade de chaves entre pt/en/es com script descartável**

Criar `site/_verificar_textos.ts`:

```ts
import { textos } from './src/lib/textos';

function caminhos(valor: unknown, prefixo = ''): string[] {
  if (Array.isArray(valor)) {
    const lista = [`${prefixo}[length=${valor.length}]`];
    valor.forEach((item, indice) => {
      lista.push(...caminhos(item, `${prefixo}[${indice}]`));
    });
    return lista;
  }
  if (valor !== null && typeof valor === 'object') {
    return Object.keys(valor)
      .sort()
      .flatMap((chave) => caminhos((valor as Record<string, unknown>)[chave], `${prefixo}.${chave}`));
  }
  return [prefixo];
}

const pt = new Set(caminhos(textos.pt));
const en = new Set(caminhos(textos.en));
const es = new Set(caminhos(textos.es));

let falhas = 0;
for (const [nome, conjunto] of [['en', en], ['es', es]] as const) {
  for (const caminho of pt) {
    if (!conjunto.has(caminho)) {
      console.error(`FALTA em ${nome}: ${caminho}`);
      falhas++;
    }
  }
  for (const caminho of conjunto) {
    if (!pt.has(caminho)) {
      console.error(`SOBRA em ${nome} (não existe em pt): ${caminho}`);
      falhas++;
    }
  }
}

if (falhas > 0) {
  console.error(`${falhas} diferença(s) de estrutura encontradas.`);
  process.exit(1);
}
console.log('textos: pt/en/es com a mesma estrutura de chaves.');
```

Run (a partir de `site/`): `node --experimental-strip-types _verificar_textos.ts`
Expected: `textos: pt/en/es com a mesma estrutura de chaves.`

Apagar depois: `Remove-Item _verificar_textos.ts`.

- [x] **Step 3: `npm run check`**

Run: `npm run check`
Expected: passa sem erro.

- [x] **Step 4: Commit**

```bash
git add site/src/lib/textos.ts
git commit -m "Adiciona dicionario pt/en/es de textos fixos ao site da marca"
```

---

## Task 3: Roteamento i18n + páginas `index` localizadas (meta apenas)

**Files:**
- Modify: `site/astro.config.mjs`
- Modify: `site/src/pages/index.astro`
- Create: `site/src/pages/en/index.astro`
- Create: `site/src/pages/es/index.astro`

**Interfaces:**
- Consumes: `idiomaAtual` (Task 1); `textos` (Task 2).
- Produces: rotas `/`, `/en/`, `/es/` funcionais, com `<title>`/meta description traduzidos. **Estado esperado ao fim desta task**: o corpo da página (Hero, QuemSouEu, etc.) continua em português nas 3 rotas — os componentes só são traduzidos nas Tasks 6-14. Isso é esperado, não é regressão.

- [x] **Step 1: Substituir o arquivo inteiro, adicionando o bloco `i18n`**

```js
// @ts-check
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://codigo-itinerante.vercel.app',
  i18n: {
    locales: ['pt', 'en', 'es'],
    defaultLocale: 'pt',
    routing: { prefixDefaultLocale: false },
  },
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
    server: {
      fs: {
        allow: [fileURLToPath(new URL('..', import.meta.url))],
      },
    },
  },
});
```

- [x] **Step 2: Atualizar `site/src/pages/index.astro` para ler idioma**

```astro
---
import Layout from "../layouts/Layout.astro";
import Hero from "../components/Hero.astro";
import Manifesto from "../components/Manifesto.astro";
import Dor from "../components/Dor.astro";
import Proposta from "../components/Proposta.astro";
import Escopo from "../components/Escopo.astro";
import ComoFunciona from "../components/ComoFunciona.astro";
import QuemSouEu from "../components/QuemSouEu.astro";
import ProvaDeTrabalho from "../components/ProvaDeTrabalho.astro";
import CtaFinal from "../components/CtaFinal.astro";
import { idiomaAtual } from "../lib/i18n";
import { textos } from "../lib/textos";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].meta.home;
---

<Layout titulo={txt.titulo} descricao={txt.descricao}>
  <Hero />
  <QuemSouEu />
  <ProvaDeTrabalho />
  <ComoFunciona />
  <Manifesto />
  <Dor />
  <Proposta />
  <Escopo />
  <CtaFinal />
</Layout>
```

- [x] **Step 3: Criar `site/src/pages/en/index.astro`**

```astro
---
import Layout from "../../layouts/Layout.astro";
import Hero from "../../components/Hero.astro";
import Manifesto from "../../components/Manifesto.astro";
import Dor from "../../components/Dor.astro";
import Proposta from "../../components/Proposta.astro";
import Escopo from "../../components/Escopo.astro";
import ComoFunciona from "../../components/ComoFunciona.astro";
import QuemSouEu from "../../components/QuemSouEu.astro";
import ProvaDeTrabalho from "../../components/ProvaDeTrabalho.astro";
import CtaFinal from "../../components/CtaFinal.astro";
import { idiomaAtual } from "../../lib/i18n";
import { textos } from "../../lib/textos";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].meta.home;
---

<Layout titulo={txt.titulo} descricao={txt.descricao}>
  <Hero />
  <QuemSouEu />
  <ProvaDeTrabalho />
  <ComoFunciona />
  <Manifesto />
  <Dor />
  <Proposta />
  <Escopo />
  <CtaFinal />
</Layout>
```

- [x] **Step 4: Criar `site/src/pages/es/index.astro`** (idêntico ao de `en/`, mesmos caminhos relativos)

```astro
---
import Layout from "../../layouts/Layout.astro";
import Hero from "../../components/Hero.astro";
import Manifesto from "../../components/Manifesto.astro";
import Dor from "../../components/Dor.astro";
import Proposta from "../../components/Proposta.astro";
import Escopo from "../../components/Escopo.astro";
import ComoFunciona from "../../components/ComoFunciona.astro";
import QuemSouEu from "../../components/QuemSouEu.astro";
import ProvaDeTrabalho from "../../components/ProvaDeTrabalho.astro";
import CtaFinal from "../../components/CtaFinal.astro";
import { idiomaAtual } from "../../lib/i18n";
import { textos } from "../../lib/textos";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].meta.home;
---

<Layout titulo={txt.titulo} descricao={txt.descricao}>
  <Hero />
  <QuemSouEu />
  <ProvaDeTrabalho />
  <ComoFunciona />
  <Manifesto />
  <Dor />
  <Proposta />
  <Escopo />
  <CtaFinal />
</Layout>
```

- [x] **Step 5: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/index.html -Pattern '<title>Código Itinerante — sites para hostels, pagos em noites</title>'
Select-String -Path dist/en/index.html -Pattern '<title>Código Itinerante — hostel websites, paid in nights</title>'
Select-String -Path dist/es/index.html -Pattern '<title>Código Itinerante — sitios web para hostels, pagados en noches</title>'
Select-String -Path dist/en/index.html -Pattern 'Sites para hostels, pagos em'
```
Expected: os 3 `<title>` corretos por idioma; a última busca **encontra** "Sites para hostels, pagos em" dentro de `dist/en/index.html` — confirma o estado esperado (Hero ainda não traduzido, corrigido na Task 6).

- [x] **Step 6: Commit**

```bash
git add site/astro.config.mjs site/src/pages/index.astro site/src/pages/en/index.astro site/src/pages/es/index.astro
git commit -m "Adiciona roteamento i18n e paginas index localizadas (meta) ao site da marca"
```

---

## Task 4: WhatsApp localizado (`dados.ts` + `BotaoWhatsApp.astro`)

**Files:**
- Modify: `site/src/dados.ts`
- Modify: `site/src/components/BotaoWhatsApp.astro`

**Interfaces:**
- Consumes: `idiomaAtual` (Task 1); `textos[idioma].botaoWhatsApp` (Task 2).
- Produces: `linkWhatsApp(mensagem: string): string` (assinatura mudou — antes não tinha parâmetro) — usado só por `BotaoWhatsApp.astro`, nenhum outro consumidor no repo.

- [x] **Step 1: Remover `mensagemWhatsApp` de `dados.ts` e parametrizar `linkWhatsApp`**

```ts
/** Dados de contato e identidade da autora. */
export const dados = {
  nome: "Tatiana Burgos",
  /** Número no formato wa.me: DDI + DDD + número, só dígitos. */
  whatsapp: "5581971127821",
  email: "tatianaoburgos@gmail.com",
  linkedin: "https://www.linkedin.com/in/tatianaoburgos/",
} as const;

/** Link wa.me com a mensagem pré-preenchida (localizada por idioma, ver lib/textos.ts). */
export function linkWhatsApp(mensagem: string): string {
  return `https://wa.me/${dados.whatsapp}?text=${encodeURIComponent(mensagem)}`;
}
```

- [x] **Step 2: `BotaoWhatsApp.astro` lê idioma e resolve rótulo/mensagem**

```astro
---
import { linkWhatsApp } from "../dados";
import { idiomaAtual } from "../lib/i18n";
import { textos } from "../lib/textos";

interface Props {
  rotulo?: string;
  invertido?: boolean;
}

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].botaoWhatsApp;
const { rotulo = txt.rotuloPadrao, invertido = false } = Astro.props;
---

<a
  href={linkWhatsApp(txt.mensagem)}
  target="_blank"
  rel="noopener noreferrer"
  class:list={[
    "inline-block rounded-full px-7 py-3 font-medium transition-colors",
    invertido ? "bg-breu text-ambar hover:bg-grafite" : "bg-ambar text-breu hover:bg-barro",
  ]}
>
  {rotulo}
</a>
```

- [x] **Step 3: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/index.html -Pattern 'Chamar no WhatsApp'
Select-String -Path dist/en/index.html -Pattern 'Message on WhatsApp'
Select-String -Path dist/es/index.html -Pattern 'Escribir por WhatsApp'
```
Expected: cada rota mostra o rótulo do botão no idioma certo (o botão da Hero não passa `rotulo` explícito, então usa sempre `rotuloPadrao`).

- [x] **Step 4: Commit**

```bash
git add site/src/dados.ts site/src/components/BotaoWhatsApp.astro
git commit -m "Localiza rotulo e mensagem do botao de WhatsApp no site da marca"
```

---

## Task 5: `Layout.astro` — hreflang, og:locale, html lang e JSON-LD traduzidos

**Files:**
- Modify: `site/src/layouts/Layout.astro`

**Interfaces:**
- Consumes: `idiomaAtual`, `idiomas`, `Idioma` (Task 1); `textos[idioma].layout.descricaoNegocio` (Task 2); `getRelativeLocaleUrl` de `astro:i18n`.
- Produces: nenhuma interface nova — `titulo`/`descricao`/`jsonLd` continuam props explícitas, como antes.

- [x] **Step 1: Substituir o arquivo inteiro**

```astro
---
import "../styles/global.css";
import { getRelativeLocaleUrl } from "astro:i18n";
import { dados } from "../dados";
import { idiomaAtual, idiomas, type Idioma } from "../lib/i18n";
import { textos } from "../lib/textos";

interface Props {
  titulo: string;
  descricao: string;
  /** JSON-LD adicional específico da página (ex.: FAQPage), somado ao Organization padrão. */
  jsonLd?: Record<string, unknown>;
}

const { titulo, descricao, jsonLd } = Astro.props;
const idioma = idiomaAtual(Astro.currentLocale);

const ogImage = new URL("og.png", Astro.site ?? Astro.url);
const canonical = new URL(Astro.url.pathname, Astro.site ?? Astro.url).href;

// Os 3 idiomas do site sempre estão ativos (sem gate de idiomasDisponiveis,
// diferente do motor) — sempre 3 tags <link rel="alternate">.
const hrefsAlternativos = idiomas.map((i) => ({
  idioma: i,
  href: new URL(getRelativeLocaleUrl(i), Astro.site ?? Astro.url).href,
}));

const ogLocalePorIdioma: Record<Idioma, string> = { pt: "pt_BR", en: "en_US", es: "es_ES" };
const htmlLangPorIdioma: Record<Idioma, string> = { pt: "pt-BR", en: "en", es: "es" };
const ogLocale = ogLocalePorIdioma[idioma];
const htmlLang = htmlLangPorIdioma[idioma];

const jsonLdOrganizacao = {
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  name: "Código Itinerante",
  description: textos[idioma].layout.descricaoNegocio,
  url: (Astro.site ?? Astro.url).href,
  email: dados.email,
  sameAs: [dados.linkedin],
};

const blocosJsonLd = [jsonLdOrganizacao, ...(jsonLd ? [jsonLd] : [])];
---

<!doctype html>
<html lang={htmlLang}>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png" />
    <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
    <link rel="canonical" href={canonical} />
    {hrefsAlternativos.map(({ idioma: idiomaAlternativo, href }) => (
      <link rel="alternate" hreflang={idiomaAlternativo} href={href} />
    ))}
    <title>{titulo}</title>
    <meta name="description" content={descricao} />

    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Código Itinerante" />
    <meta property="og:title" content={titulo} />
    <meta property="og:description" content={descricao} />
    <meta property="og:image" content={ogImage} />
    <meta property="og:url" content={canonical} />
    <meta property="og:locale" content={ogLocale} />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={titulo} />
    <meta name="twitter:description" content={descricao} />
    <meta name="twitter:image" content={ogImage} />

    {
      blocosJsonLd.map((bloco) => (
        <script
          type="application/ld+json"
          is:inline
          set:html={JSON.stringify(bloco).replace(/</g, "\\u003c")}
        />
      ))
    }
  </head>
  <body class="bg-ambar font-sans text-cal antialiased">
    <div class="pagina-degrade">
      <slot />
    </div>
  </body>
</html>
```

- [x] **Step 2: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/index.html -Pattern 'lang="pt-BR"'
Select-String -Path dist/en/index.html -Pattern 'lang="en"'
Select-String -Path dist/es/index.html -Pattern 'lang="es"'
Select-String -Path dist/index.html -Pattern 'og:locale.*pt_BR'
Select-String -Path dist/en/index.html -Pattern 'og:locale.*en_US'
Select-String -Path dist/es/index.html -Pattern 'og:locale.*es_ES'
Select-String -Path dist/index.html -Pattern 'hreflang="en"'
Select-String -Path dist/index.html -Pattern 'hreflang="es"'
Select-String -Path dist/en/index.html -Pattern 'hreflang="pt"'
Select-String -Path dist/es/index.html -Pattern 'hreflang="pt"'
Select-String -Path dist/en/index.html -Pattern 'Building institutional websites for hostels'
Select-String -Path dist/es/index.html -Pattern 'Construcción de sitios web institucionales'
```
Expected: `lang`/`og:locale` corretos por rota; `dist/index.html` tem `hreflang="en"` e `hreflang="es"` (as 3 tags sempre presentes, sem gate); a descrição do JSON-LD aparece traduzida em `en`/`es`.

- [x] **Step 3: Commit**

```bash
git add site/src/layouts/Layout.astro
git commit -m "Traduz hreflang, og:locale, html lang e JSON-LD do site da marca"
```

---

## Task 6: `AlternadorIdioma.astro` (novo) + `Hero.astro` localizado

**Files:**
- Create: `site/src/components/AlternadorIdioma.astro`
- Modify: `site/src/components/Hero.astro`

**Interfaces:**
- Consumes: `idiomas`, `Idioma`, `idiomaAtual` (Task 1); `textos[idioma].hero` (Task 2); `getRelativeLocaleUrl` de `astro:i18n`.
- Produces: `AlternadorIdioma` (props: `idioma: Idioma`, `class?: string`) — reusado nas Tasks 15 e 16.

- [x] **Step 1: Criar `AlternadorIdioma.astro`**

Réplica do padrão visual "PT / EN / ES" do `Nav.astro` do motor (`template/src/components/Nav.astro`), sem gate de idiomas ativos — aqui os 3 sempre aparecem.

```astro
---
import { getRelativeLocaleUrl } from "astro:i18n";
import { idiomas, type Idioma } from "../lib/i18n";

interface Props {
  idioma: Idioma;
  class?: string;
}

const { idioma, class: className } = Astro.props;
---

<div class:list={["flex items-center gap-1 font-mono text-xs font-bold tracking-widest uppercase", className]}>
  {
    idiomas.map((idiomaItem, indice) => (
      <>
        {indice > 0 && <span aria-hidden="true">/</span>}
        {idioma === idiomaItem ? (
          <span aria-current="page">{idiomaItem.toUpperCase()}</span>
        ) : (
          <a href={getRelativeLocaleUrl(idiomaItem)} hreflang={idiomaItem} class="transition hover:text-ambar">
            {idiomaItem.toUpperCase()}
          </a>
        )}
      </>
    ))
  }
</div>
```

- [x] **Step 2: `Hero.astro` lê idioma e usa o alternador**

```astro
---
import BotaoWhatsApp from "./BotaoWhatsApp.astro";
import AlternadorIdioma from "./AlternadorIdioma.astro";
import { idiomaAtual } from "../lib/i18n";
import { textos } from "../lib/textos";
import wordmark from "../../../marca/wordmark-escuro.svg";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].hero;
---

<header class="mx-auto flex min-h-dvh w-full max-w-3xl flex-col justify-center px-6 py-10 md:min-h-[78vh] md:py-12">
  <div class="flex justify-end">
    <AlternadorIdioma idioma={idioma} />
  </div>
  <img src={wordmark.src} alt="Código Itinerante" class="mt-4 -ml-[4.5%] w-[108%]" />
  <h1 class="mt-10 text-4xl font-bold leading-[1.05] tracking-[-0.035em] md:text-6xl">
    {txt.tituloPre}<em class="font-serifa font-normal text-ambar">{txt.tituloDestaque}</em>
  </h1>
  <p class="mt-6 max-w-xl text-base leading-relaxed text-pedra">
    {txt.paragrafo}
  </p>
  <div class="mt-8">
    <BotaoWhatsApp />
  </div>
</header>
```

- [x] **Step 3: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/index.html -Pattern 'Sites para hostels, pagos em'
Select-String -Path dist/en/index.html -Pattern 'Websites for hostels, paid in'
Select-String -Path dist/es/index.html -Pattern 'Sitios web para hostels, pagados en'
Select-String -Path dist/index.html -Pattern 'href="/en/"'
Select-String -Path dist/index.html -Pattern 'href="/es/"'
Select-String -Path dist/en/index.html -Pattern 'href="/"'
Select-String -Path dist/es/index.html -Pattern 'href="/"'
```
Expected: Hero traduzida em cada rota; alternador da home (`/`) linka para `/en/` e `/es/` **(com barra final — confirmado no build real do LumeHostel, `template/dist/index.html`: `getRelativeLocaleUrl` sempre adiciona `/` no fim para locales não-default, porque `trailingSlash` é `'ignore'` e `build.format` é `'directory'`, combinação que resolve para "sempre com barra"; só o locale padrão sem `path` retorna `/` puro)**; alternadores de `/en/` e `/es/` linkam de volta pra `/` (pt, sem barra dupla).

- [x] **Step 4: Commit**

```bash
git add site/src/components/AlternadorIdioma.astro site/src/components/Hero.astro
git commit -m "Adiciona alternador de idioma e localiza a Hero do site da marca"
```

---

## Task 7: `QuemSouEu.astro` localizado

**Files:**
- Modify: `site/src/components/QuemSouEu.astro`

**Interfaces:**
- Consumes: `idiomaAtual` (Task 1); `textos[idioma].quemSouEu` (Task 2).

- [x] **Step 1: Substituir o arquivo inteiro**

```astro
---
import { Image } from "astro:assets";
import Eyebrow from "./Eyebrow.astro";
import Secao from "./Secao.astro";
import BotaoContorno from "./BotaoContorno.astro";
import { dados } from "../dados";
import { idiomaAtual } from "../lib/i18n";
import { textos } from "../lib/textos";
import foto from "../assets/tatiana.jpg";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].quemSouEu;
---

<Secao>
  <Eyebrow texto={txt.eyebrowTexto} destaque={txt.eyebrowDestaque} />
  <div class="mt-7 grid items-start gap-7 md:grid-cols-[200px_1fr]">
    <Image
      src={foto}
      alt={txt.fotoAlt}
      widths={[200, 400, 800]}
      sizes="(min-width: 768px) 200px, 100vw"
      class="aspect-square w-full rounded-xl object-cover"
    />
    <div class="space-y-5 leading-relaxed">
      <p class="text-xl font-semibold">{dados.nome}</p>
      <p>{txt.paragrafo}</p>
      <blockquote class="border-l-2 border-ambar pl-5 text-lg">
        {txt.citacao}
      </blockquote>
      <p>
        <BotaoContorno href={dados.linkedin}>{txt.linkedinLabel}</BotaoContorno>
      </p>
    </div>
  </div>
</Secao>
```

- [x] **Step 2: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/index.html -Pattern 'Trabalho como especialista em Ciência de Dados'
Select-String -Path dist/en/index.html -Pattern 'I work as a Data Science specialist'
Select-String -Path dist/es/index.html -Pattern 'Trabajo como especialista en Ciencia de Datos'
```
Expected: as 3 rotas mostram o parágrafo no idioma correto.

- [x] **Step 3: Commit**

```bash
git add site/src/components/QuemSouEu.astro
git commit -m "Localiza a secao Quem sou eu do site da marca"
```

---

## Task 8: `ProvaDeTrabalho.astro` localizado

**Files:**
- Modify: `site/src/components/ProvaDeTrabalho.astro`

**Interfaces:**
- Consumes: `idiomaAtual` (Task 1); `textos[idioma].provaDeTrabalho` (Task 2).

- [x] **Step 1: Substituir o arquivo inteiro**

```astro
---
import { Image } from "astro:assets";
import Eyebrow from "./Eyebrow.astro";
import Secao from "./Secao.astro";
import BotaoContorno from "./BotaoContorno.astro";
import { idiomaAtual } from "../lib/i18n";
import { textos } from "../lib/textos";
import printDesktop from "../assets/portfolio/lumehostel-desktop.png";
import printMobile from "../assets/portfolio/lumehostel-mobile.png";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].provaDeTrabalho;
const url = "https://lumehostel.vercel.app";
---

<Secao>
  <Eyebrow texto={txt.eyebrowTexto} destaque={txt.eyebrowDestaque} />

  <div class="relative mt-7">
    <a
      href={url}
      target="_blank"
      rel="noopener"
      class="block overflow-hidden rounded-xl border border-pedra/20 shadow-2xl transition-transform hover:-translate-y-1"
    >
      <div class="flex items-center gap-2 bg-grafite px-4 py-3">
        <span class="h-2.5 w-2.5 rounded-full bg-pedra/40"></span>
        <span class="h-2.5 w-2.5 rounded-full bg-pedra/40"></span>
        <span class="h-2.5 w-2.5 rounded-full bg-pedra/40"></span>
        <span class="ml-3 font-mono text-xs text-pedra">lumehostel.vercel.app</span>
      </div>
      <Image
        src={printDesktop}
        alt={txt.altDesktop}
        widths={[480, 900, 1440]}
        sizes="(min-width: 768px) 720px, 100vw"
        class="w-full"
      />
    </a>

    <div
      class="pointer-events-none absolute -bottom-6 right-6 hidden w-[130px] overflow-hidden rounded-[1.5rem] border-4 border-grafite shadow-2xl md:block"
    >
      <Image
        src={printMobile}
        alt={txt.altMobile}
        widths={[130, 260, 390]}
        sizes="130px"
        class="w-full"
      />
    </div>
  </div>

  <div class="mt-10 space-y-5 leading-relaxed md:mt-16">
    <h3 class="text-xl font-semibold">{txt.cardTitulo}</h3>
    <p>{txt.paragrafo}</p>
    <p>
      <BotaoContorno href={url}>{txt.verSiteLabel}</BotaoContorno>
    </p>
  </div>
</Secao>
```

- [x] **Step 2: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/index.html -Pattern 'O site completo do LumeHostel'
Select-String -Path dist/en/index.html -Pattern 'The full LumeHostel website'
Select-String -Path dist/es/index.html -Pattern 'El sitio completo de LumeHostel'
```

- [x] **Step 3: Commit**

```bash
git add site/src/components/ProvaDeTrabalho.astro
git commit -m "Localiza a secao Prova de trabalho do site da marca"
```

---

## Task 9: `ComoFunciona.astro` localizado

**Files:**
- Modify: `site/src/components/ComoFunciona.astro`

**Interfaces:**
- Consumes: `idiomaAtual` (Task 1); `textos[idioma].comoFunciona` (Task 2).

- [x] **Step 1: Substituir o arquivo inteiro**

```astro
---
import Eyebrow from "./Eyebrow.astro";
import Secao from "./Secao.astro";
import { idiomaAtual } from "../lib/i18n";
import { textos } from "../lib/textos";
import iconeContato from "../../../marca/icones/icone-contato-cheio-breu.svg";
import iconeHostel from "../../../marca/icones/icone-hostel-cheio-breu.svg";
import iconeSiteProprio from "../../../marca/icones/icone-site-proprio-cheio-breu.svg";
import iconeEstrada from "../../../marca/icones/icone-estrada-cheio-breu.svg";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].comoFunciona;

const icones = [iconeContato, iconeHostel, iconeSiteProprio, iconeEstrada];
const passos = txt.passos.map((passo, indice) => ({ ...passo, icone: icones[indice] }));
---

<Secao>
  <Eyebrow texto={txt.eyebrowTexto} destaque={txt.eyebrowDestaque} />
  <ol class="mt-7 space-y-8">
    {
      passos.map((passo) => (
        <li class="flex gap-6">
          <img src={passo.icone.src} alt="" class="w-[72px] flex-none" />
          <div>
            <h3 class="text-xl font-semibold">{passo.titulo}</h3>
            <p class="mt-1 leading-relaxed text-pedra">{passo.texto}</p>
          </div>
        </li>
      ))
    }
  </ol>
</Secao>
```

- [x] **Step 2: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/index.html -Pattern 'Conversamos no WhatsApp'
Select-String -Path dist/en/index.html -Pattern 'We talk on WhatsApp'
Select-String -Path dist/es/index.html -Pattern 'Conversamos por WhatsApp'
```

- [x] **Step 3: Commit**

```bash
git add site/src/components/ComoFunciona.astro
git commit -m "Localiza a secao Como funciona do site da marca"
```

---

## Task 10: `Manifesto.astro` localizado

**Files:**
- Modify: `site/src/components/Manifesto.astro`

**Interfaces:**
- Consumes: `idiomaAtual` (Task 1); `textos[idioma].manifesto` (Task 2).

- [x] **Step 1: Substituir o arquivo inteiro**

```astro
---
import Eyebrow from "./Eyebrow.astro";
import Secao from "./Secao.astro";
import { idiomaAtual } from "../lib/i18n";
import { textos } from "../lib/textos";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].manifesto;
---

<Secao>
  <Eyebrow texto={txt.eyebrowTexto} destaque={txt.eyebrowDestaque} />
  <div class="mt-6 space-y-5 text-lg leading-relaxed">
    <p>{txt.paragrafo1}</p>
    <p>{txt.paragrafo2}</p>
    <p>
      {txt.paragrafo3Pre}
      <em class="font-serifa text-2xl font-bold text-ambar">{txt.paragrafo3Destaque}</em>.
    </p>
  </div>
</Secao>
```

- [x] **Step 2: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/index.html -Pattern 'nasceu de uma troca simples'
Select-String -Path dist/en/index.html -Pattern 'was born from a simple trade'
Select-String -Path dist/es/index.html -Pattern 'nació de un intercambio simple'
```

- [x] **Step 3: Commit**

```bash
git add site/src/components/Manifesto.astro
git commit -m "Localiza a secao Manifesto do site da marca"
```

---

## Task 11: `Dor.astro` localizado

**Files:**
- Modify: `site/src/components/Dor.astro`

**Interfaces:**
- Consumes: `idiomaAtual` (Task 1); `textos[idioma].dor` (Task 2).

- [x] **Step 1: Substituir o arquivo inteiro**

```astro
---
import Eyebrow from "./Eyebrow.astro";
import Secao from "./Secao.astro";
import { idiomaAtual } from "../lib/i18n";
import { textos } from "../lib/textos";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].dor;
---

<Secao>
  <Eyebrow texto={txt.eyebrowTexto} destaque={txt.eyebrowDestaque} />
  <div class="mt-6 space-y-5 text-lg leading-relaxed">
    <p>{txt.paragrafo}</p>
  </div>
  <div class="mt-8 rounded-xl border border-cal/10 bg-grafite/70 p-6 backdrop-blur-sm md:p-7">
    <p class="text-xl leading-relaxed">
      {txt.boxPre}<strong class="text-ambar">{txt.boxForte}</strong>{txt.boxPos}
    </p>
  </div>
</Secao>
```

- [x] **Step 2: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/index.html -Pattern 'de 10% a 25% por reserva'
Select-String -Path dist/en/index.html -Pattern '10% to 25% per booking'
Select-String -Path dist/es/index.html -Pattern 'de 10% a 25% por reserva'
```

- [x] **Step 3: Commit**

```bash
git add site/src/components/Dor.astro
git commit -m "Localiza a secao O problema do site da marca"
```

---

## Task 12: `Proposta.astro` localizado

**Files:**
- Modify: `site/src/components/Proposta.astro`

**Interfaces:**
- Consumes: `idiomaAtual` (Task 1); `textos[idioma].proposta` (Task 2).

- [x] **Step 1: Substituir o arquivo inteiro**

```astro
---
import Eyebrow from "./Eyebrow.astro";
import Secao from "./Secao.astro";
import { idiomaAtual } from "../lib/i18n";
import { textos } from "../lib/textos";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].proposta;
---

<Secao>
  <Eyebrow texto={txt.eyebrowTexto} destaque={txt.eyebrowDestaque} />
  <div class="mt-6 space-y-5 text-lg leading-relaxed">
    <p>{txt.paragrafo1}</p>
    <p class="font-serifa italic text-3xl leading-snug text-ambar md:text-4xl">
      {txt.destaque}
    </p>
    <p>{txt.paragrafo3}</p>
  </div>
</Secao>
```

- [x] **Step 2: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/index.html -Pattern 'É uma troca temporária por um produto permanente'
Select-String -Path dist/en/index.html -Pattern 'a temporary trade for a permanent product'
Select-String -Path dist/es/index.html -Pattern 'un intercambio temporal por un producto permanente'
```

- [x] **Step 3: Commit**

```bash
git add site/src/components/Proposta.astro
git commit -m "Localiza a secao A proposta do site da marca"
```

---

## Task 13: `Escopo.astro` localizado (link para FAQ ganha idioma)

**Files:**
- Modify: `site/src/components/Escopo.astro`

**Interfaces:**
- Consumes: `idiomaAtual` (Task 1); `textos[idioma].escopo` (Task 2); `getRelativeLocaleUrl` de `astro:i18n`.

- [x] **Step 1: Substituir o arquivo inteiro**

```astro
---
import { getRelativeLocaleUrl } from "astro:i18n";
import Eyebrow from "./Eyebrow.astro";
import Secao from "./Secao.astro";
import { idiomaAtual } from "../lib/i18n";
import { textos } from "../lib/textos";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].escopo;
---

<Secao>
  <Eyebrow texto={txt.eyebrowTexto} destaque={txt.eyebrowDestaque} />
  <div class="mt-6 grid gap-6 md:grid-cols-2">
    <div class="rounded-xl border border-cal/10 bg-grafite/70 p-6 backdrop-blur-sm md:p-7">
      <h3 class="font-mono text-sm font-medium uppercase tracking-[0.12em] text-ambar">{txt.incluiTitulo}</h3>
      <ul class="mt-5 space-y-3 leading-relaxed">
        {txt.inclui.map((item) => <li>{item}</li>)}
      </ul>
    </div>
    <div class="rounded-xl border border-cal/10 bg-grafite/70 p-6 backdrop-blur-sm md:p-7">
      <h3 class="font-mono text-sm font-medium uppercase tracking-[0.12em] text-cal/75">{txt.naoIncluiTitulo}</h3>
      <ul class="mt-5 space-y-3 leading-relaxed text-cal/75">
        {txt.naoInclui.map((item) => <li>{item}</li>)}
      </ul>
    </div>
  </div>
  <p class="mt-6 text-sm text-cal/75">
    {txt.duvidasPre}
    <a
      href={getRelativeLocaleUrl(idioma, "faq")}
      class="text-cal underline decoration-cal/40 underline-offset-4 hover:decoration-cal"
    >
      {txt.duvidasLink}
    </a>
  </p>
</Secao>
```

- [x] **Step 2: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/index.html -Pattern 'href="/faq/"'
Select-String -Path dist/en/index.html -Pattern 'href="/en/faq/"'
Select-String -Path dist/es/index.html -Pattern 'href="/es/faq/"'
Select-String -Path dist/en/index.html -Pattern 'Responsive site, beautiful on phone and computer'
Select-String -Path dist/es/index.html -Pattern 'Qué incluye'
```
Expected: o link para o FAQ é relativo ao idioma atual em cada rota, **sempre com barra final** (`getRelativeLocaleUrl(idioma, "faq")` retorna `/faq/`, `/en/faq/`, `/es/faq/` — qualquer chamada com `path` sempre fecha em `/`, mesmo para o locale padrão; confirma que `getRelativeLocaleUrl(idioma, "faq")` resolve corretamente — as rotas `/en/faq` e `/es/faq` só existem a partir da Task 15, mas o `href` gerado já é o caminho certo).

**Nota sobre apóstrofo em `Select-String`**: evite padrões com contração (ex. `"What's included"`) — o Astro renderiza apóstrofo de texto como entidade HTML `&#39;` no HTML final (confirmado ao rodar: o texto-fonte `What's included` sai como `What&#39;s included` no `dist/`), então o apóstrofo literal nunca bate contra o HTML gerado. Prefira um trecho sem contração, como acima.

- [x] **Step 3: Commit**

```bash
git add site/src/components/Escopo.astro
git commit -m "Localiza a secao O que voce recebe do site da marca"
```

---

## Task 14: `CtaFinal.astro` localizado

**Files:**
- Modify: `site/src/components/CtaFinal.astro`

**Interfaces:**
- Consumes: `idiomaAtual` (Task 1); `textos[idioma].ctaFinal` (Task 2).

- [x] **Step 1: Substituir o arquivo inteiro**

```astro
---
import BotaoWhatsApp from "./BotaoWhatsApp.astro";
import { dados } from "../dados";
import { idiomaAtual } from "../lib/i18n";
import { textos } from "../lib/textos";
import iconeContato from "../../../marca/icones/icone-contato-cheio-papel.svg";
import monograma from "../../../marca/monograma-claro.svg";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].ctaFinal;
---

<section class="mx-auto w-full max-w-3xl px-6 pb-6 pt-10 text-breu md:pt-12">
  <img src={iconeContato.src} alt="" class="h-[88px]" />
  <h2 class="mt-6 text-4xl font-bold tracking-[-0.035em] md:text-5xl">
    {txt.tituloPre}<em class="font-serifa font-normal">{txt.tituloDestaque}</em>.
  </h2>
  <p class="mt-4 max-w-md text-lg leading-relaxed text-breu/70">
    {txt.paragrafo}
  </p>
  <div class="mt-7">
    <BotaoWhatsApp invertido />
  </div>
  <footer class="mt-12 flex items-center justify-between border-t border-breu/25 pt-6 text-sm text-breu/70">
    <img src={monograma.src} alt="Código Itinerante" class="h-8" />
    <div class="flex gap-6">
      <a href={`mailto:${dados.email}`} class="hover:text-breu">{dados.email}</a>
      <a href={dados.linkedin} class="hover:text-breu">LinkedIn</a>
    </div>
  </footer>
</section>
```

- [x] **Step 2: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/index.html -Pattern 'Vamos <em class="font-serifa font-normal">conversar</em>'
Select-String -Path dist/en/index.html -Pattern 'Have a hostel\? Let'
Select-String -Path dist/en/index.html -Pattern '<em class="font-serifa font-normal">talk</em>'
Select-String -Path dist/es/index.html -Pattern 'Vamos a <em class="font-serifa font-normal">conversar</em>'
```
Expected: cada rota mostra o título de fechamento no idioma certo.

- [x] **Step 3: Commit**

```bash
git add site/src/components/CtaFinal.astro
git commit -m "Localiza a secao final de CTA do site da marca"
```

---

## Task 15: FAQ localizada (`faq.astro` + `en/faq.astro` + `es/faq.astro`)

**Files:**
- Modify: `site/src/pages/faq.astro`
- Create: `site/src/pages/en/faq.astro`
- Create: `site/src/pages/es/faq.astro`

**Interfaces:**
- Consumes: `idiomaAtual` (Task 1); `textos[idioma].faq`, `textos[idioma].meta.faq` (Task 2); `AlternadorIdioma` (Task 6); `getRelativeLocaleUrl` de `astro:i18n`.

- [x] **Step 1: Substituir `site/src/pages/faq.astro`**

```astro
---
import { getRelativeLocaleUrl } from "astro:i18n";
import Layout from "../layouts/Layout.astro";
import BotaoWhatsApp from "../components/BotaoWhatsApp.astro";
import AlternadorIdioma from "../components/AlternadorIdioma.astro";
import Secao from "../components/Secao.astro";
import { dados } from "../dados";
import { idiomaAtual } from "../lib/i18n";
import { textos } from "../lib/textos";
import monograma from "../../../marca/monograma-claro.svg";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].faq;
const txtMeta = textos[idioma].meta.faq;

const jsonLdFaq = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: txt.perguntas.map((p) => ({
    "@type": "Question",
    name: p.pergunta,
    acceptedAnswer: { "@type": "Answer", text: p.resposta },
  })),
};
---

<Layout titulo={txtMeta.titulo} descricao={txtMeta.descricao} jsonLd={jsonLdFaq}>
  <div class="min-h-dvh bg-ambar text-breu">
    <Secao>
      <div class="flex items-center justify-between gap-4">
        <a
          href={getRelativeLocaleUrl(idioma)}
          class="inline-flex items-center gap-2 text-sm text-breu/70 transition-colors hover:text-breu"
        >
          <img src={monograma.src} alt="" class="h-6" />
          Código Itinerante
        </a>
        <AlternadorIdioma idioma={idioma} />
      </div>
      <h1 class="mt-8 text-4xl font-bold tracking-[-0.035em] md:text-5xl">
        {txt.tituloPre}<em class="font-serifa font-normal">{txt.tituloDestaque}</em>
      </h1>
      <div class="mt-10 space-y-8">
        {
          txt.perguntas.map((p) => (
            <div>
              <h2 class="text-lg font-semibold">{p.pergunta}</h2>
              <p class="mt-2 leading-relaxed text-breu/80">{p.resposta}</p>
            </div>
          ))
        }
      </div>
      <div class="mt-14 border-t border-breu/20 pt-8">
        <p class="text-lg">{txt.naoAchou}</p>
        <div class="mt-4">
          <BotaoWhatsApp invertido />
        </div>
      </div>
      <footer class="mt-12 flex items-center justify-between border-t border-breu/20 pt-6 text-sm text-breu/70">
        <img src={monograma.src} alt="Código Itinerante" class="h-6" />
        <div class="flex gap-6">
          <a href={`mailto:${dados.email}`} class="hover:text-breu">{dados.email}</a>
          <a href={dados.linkedin} class="hover:text-breu">LinkedIn</a>
        </div>
      </footer>
    </Secao>
  </div>
</Layout>
```

- [x] **Step 2: Criar `site/src/pages/en/faq.astro`** (mesmo conteúdo, um nível a mais de `../`)

```astro
---
import { getRelativeLocaleUrl } from "astro:i18n";
import Layout from "../../layouts/Layout.astro";
import BotaoWhatsApp from "../../components/BotaoWhatsApp.astro";
import AlternadorIdioma from "../../components/AlternadorIdioma.astro";
import Secao from "../../components/Secao.astro";
import { dados } from "../../dados";
import { idiomaAtual } from "../../lib/i18n";
import { textos } from "../../lib/textos";
import monograma from "../../../../marca/monograma-claro.svg";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].faq;
const txtMeta = textos[idioma].meta.faq;

const jsonLdFaq = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: txt.perguntas.map((p) => ({
    "@type": "Question",
    name: p.pergunta,
    acceptedAnswer: { "@type": "Answer", text: p.resposta },
  })),
};
---

<Layout titulo={txtMeta.titulo} descricao={txtMeta.descricao} jsonLd={jsonLdFaq}>
  <div class="min-h-dvh bg-ambar text-breu">
    <Secao>
      <div class="flex items-center justify-between gap-4">
        <a
          href={getRelativeLocaleUrl(idioma)}
          class="inline-flex items-center gap-2 text-sm text-breu/70 transition-colors hover:text-breu"
        >
          <img src={monograma.src} alt="" class="h-6" />
          Código Itinerante
        </a>
        <AlternadorIdioma idioma={idioma} />
      </div>
      <h1 class="mt-8 text-4xl font-bold tracking-[-0.035em] md:text-5xl">
        {txt.tituloPre}<em class="font-serifa font-normal">{txt.tituloDestaque}</em>
      </h1>
      <div class="mt-10 space-y-8">
        {
          txt.perguntas.map((p) => (
            <div>
              <h2 class="text-lg font-semibold">{p.pergunta}</h2>
              <p class="mt-2 leading-relaxed text-breu/80">{p.resposta}</p>
            </div>
          ))
        }
      </div>
      <div class="mt-14 border-t border-breu/20 pt-8">
        <p class="text-lg">{txt.naoAchou}</p>
        <div class="mt-4">
          <BotaoWhatsApp invertido />
        </div>
      </div>
      <footer class="mt-12 flex items-center justify-between border-t border-breu/20 pt-6 text-sm text-breu/70">
        <img src={monograma.src} alt="Código Itinerante" class="h-6" />
        <div class="flex gap-6">
          <a href={`mailto:${dados.email}`} class="hover:text-breu">{dados.email}</a>
          <a href={dados.linkedin} class="hover:text-breu">LinkedIn</a>
        </div>
      </footer>
    </Secao>
  </div>
</Layout>
```

- [x] **Step 3: Criar `site/src/pages/es/faq.astro`** (idêntico ao de `en/`, mesmos caminhos relativos)

```astro
---
import { getRelativeLocaleUrl } from "astro:i18n";
import Layout from "../../layouts/Layout.astro";
import BotaoWhatsApp from "../../components/BotaoWhatsApp.astro";
import AlternadorIdioma from "../../components/AlternadorIdioma.astro";
import Secao from "../../components/Secao.astro";
import { dados } from "../../dados";
import { idiomaAtual } from "../../lib/i18n";
import { textos } from "../../lib/textos";
import monograma from "../../../../marca/monograma-claro.svg";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].faq;
const txtMeta = textos[idioma].meta.faq;

const jsonLdFaq = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: txt.perguntas.map((p) => ({
    "@type": "Question",
    name: p.pergunta,
    acceptedAnswer: { "@type": "Answer", text: p.resposta },
  })),
};
---

<Layout titulo={txtMeta.titulo} descricao={txtMeta.descricao} jsonLd={jsonLdFaq}>
  <div class="min-h-dvh bg-ambar text-breu">
    <Secao>
      <div class="flex items-center justify-between gap-4">
        <a
          href={getRelativeLocaleUrl(idioma)}
          class="inline-flex items-center gap-2 text-sm text-breu/70 transition-colors hover:text-breu"
        >
          <img src={monograma.src} alt="" class="h-6" />
          Código Itinerante
        </a>
        <AlternadorIdioma idioma={idioma} />
      </div>
      <h1 class="mt-8 text-4xl font-bold tracking-[-0.035em] md:text-5xl">
        {txt.tituloPre}<em class="font-serifa font-normal">{txt.tituloDestaque}</em>
      </h1>
      <div class="mt-10 space-y-8">
        {
          txt.perguntas.map((p) => (
            <div>
              <h2 class="text-lg font-semibold">{p.pergunta}</h2>
              <p class="mt-2 leading-relaxed text-breu/80">{p.resposta}</p>
            </div>
          ))
        }
      </div>
      <div class="mt-14 border-t border-breu/20 pt-8">
        <p class="text-lg">{txt.naoAchou}</p>
        <div class="mt-4">
          <BotaoWhatsApp invertido />
        </div>
      </div>
      <footer class="mt-12 flex items-center justify-between border-t border-breu/20 pt-6 text-sm text-breu/70">
        <img src={monograma.src} alt="Código Itinerante" class="h-6" />
        <div class="flex gap-6">
          <a href={`mailto:${dados.email}`} class="hover:text-breu">{dados.email}</a>
          <a href={dados.linkedin} class="hover:text-breu">LinkedIn</a>
        </div>
      </footer>
    </Secao>
  </div>
</Layout>
```

- [x] **Step 4: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/faq/index.html -Pattern 'Quantas noites custa o site'
Select-String -Path dist/en/faq/index.html -Pattern 'How many nights does the site cost'
Select-String -Path dist/es/faq/index.html -Pattern 'Cuántas noches cuesta el sitio'
Select-String -Path dist/en/faq/index.html -Pattern 'href="/en/"'
Select-String -Path dist/es/faq/index.html -Pattern 'href="/es/"'
```
Expected: as 3 rotas do FAQ existem, com as perguntas traduzidas; o link do logo/monograma em `/en/faq` aponta para `/en/` e em `/es/faq` para `/es/` — a home **daquele idioma**, não a raiz `/` em português. `getRelativeLocaleUrl(idioma)` sem segundo argumento sempre resolve pra home do idioma atual da página (com barra final, exceto quando esse idioma é o padrão pt).

- [x] **Step 5: Commit**

```bash
git add site/src/pages/faq.astro site/src/pages/en/faq.astro site/src/pages/es/faq.astro
git commit -m "Localiza a pagina de FAQ do site da marca em pt/en/es"
```

---

## Task 16: 404 localizada (`404.astro` + `en/404.astro` + `es/404.astro`)

**Files:**
- Modify: `site/src/pages/404.astro`
- Create: `site/src/pages/en/404.astro`
- Create: `site/src/pages/es/404.astro`

**Interfaces:**
- Consumes: `idiomaAtual` (Task 1); `textos[idioma].pagina404`, `textos[idioma].meta.pagina404` (Task 2); `AlternadorIdioma` (Task 6); `getRelativeLocaleUrl` de `astro:i18n`.

- [x] **Step 1: Substituir `site/src/pages/404.astro`**

```astro
---
import { getRelativeLocaleUrl } from "astro:i18n";
import Layout from "../layouts/Layout.astro";
import BotaoContorno from "../components/BotaoContorno.astro";
import AlternadorIdioma from "../components/AlternadorIdioma.astro";
import { idiomaAtual } from "../lib/i18n";
import { textos } from "../lib/textos";
import wordmark from "../../../marca/wordmark-escuro.svg";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].pagina404;
const txtMeta = textos[idioma].meta.pagina404;
---

<Layout titulo={txtMeta.titulo} descricao={txtMeta.descricao}>
  <div class="flex min-h-dvh flex-col items-center justify-center bg-breu px-6 py-10 text-center text-cal">
    <AlternadorIdioma idioma={idioma} class="mb-4" />
    <img src={wordmark.src} alt="Código Itinerante" class="w-64 max-w-full" />
    <p class="mt-8 text-2xl font-bold tracking-[-0.02em]">{txt.titulo}</p>
    <p class="mt-3 max-w-sm text-pedra">
      {txt.texto}
    </p>
    <div class="mt-8">
      <BotaoContorno href={getRelativeLocaleUrl(idioma)} externo={false}>{txt.voltarLabel}</BotaoContorno>
    </div>
  </div>
</Layout>
```

- [x] **Step 2: Criar `site/src/pages/en/404.astro`** (mesmo conteúdo, um nível a mais de `../`)

```astro
---
import { getRelativeLocaleUrl } from "astro:i18n";
import Layout from "../../layouts/Layout.astro";
import BotaoContorno from "../../components/BotaoContorno.astro";
import AlternadorIdioma from "../../components/AlternadorIdioma.astro";
import { idiomaAtual } from "../../lib/i18n";
import { textos } from "../../lib/textos";
import wordmark from "../../../../marca/wordmark-escuro.svg";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].pagina404;
const txtMeta = textos[idioma].meta.pagina404;
---

<Layout titulo={txtMeta.titulo} descricao={txtMeta.descricao}>
  <div class="flex min-h-dvh flex-col items-center justify-center bg-breu px-6 py-10 text-center text-cal">
    <AlternadorIdioma idioma={idioma} class="mb-4" />
    <img src={wordmark.src} alt="Código Itinerante" class="w-64 max-w-full" />
    <p class="mt-8 text-2xl font-bold tracking-[-0.02em]">{txt.titulo}</p>
    <p class="mt-3 max-w-sm text-pedra">
      {txt.texto}
    </p>
    <div class="mt-8">
      <BotaoContorno href={getRelativeLocaleUrl(idioma)} externo={false}>{txt.voltarLabel}</BotaoContorno>
    </div>
  </div>
</Layout>
```

- [x] **Step 3: Criar `site/src/pages/es/404.astro`** (idêntico ao de `en/`, mesmos caminhos relativos)

```astro
---
import { getRelativeLocaleUrl } from "astro:i18n";
import Layout from "../../layouts/Layout.astro";
import BotaoContorno from "../../components/BotaoContorno.astro";
import AlternadorIdioma from "../../components/AlternadorIdioma.astro";
import { idiomaAtual } from "../../lib/i18n";
import { textos } from "../../lib/textos";
import wordmark from "../../../../marca/wordmark-escuro.svg";

const idioma = idiomaAtual(Astro.currentLocale);
const txt = textos[idioma].pagina404;
const txtMeta = textos[idioma].meta.pagina404;
---

<Layout titulo={txtMeta.titulo} descricao={txtMeta.descricao}>
  <div class="flex min-h-dvh flex-col items-center justify-center bg-breu px-6 py-10 text-center text-cal">
    <AlternadorIdioma idioma={idioma} class="mb-4" />
    <img src={wordmark.src} alt="Código Itinerante" class="w-64 max-w-full" />
    <p class="mt-8 text-2xl font-bold tracking-[-0.02em]">{txt.titulo}</p>
    <p class="mt-3 max-w-sm text-pedra">
      {txt.texto}
    </p>
    <div class="mt-8">
      <BotaoContorno href={getRelativeLocaleUrl(idioma)} externo={false}>{txt.voltarLabel}</BotaoContorno>
    </div>
  </div>
</Layout>
```

- [x] **Step 4: Build e checagem**

A partir de `site/`:
```
npm run check
npm run build
Select-String -Path dist/404.html -Pattern 'Essa página não existe'
Select-String -Path dist/en/404/index.html -Pattern 'This page'
Select-String -Path dist/es/404/index.html -Pattern 'Esta página no existe'
Select-String -Path dist/en/404/index.html -Pattern 'href="/en/"'
Select-String -Path dist/es/404/index.html -Pattern 'href="/es/"'
```
Expected: as 3 versões da 404 existem, com o texto traduzido; o botão "voltar pra home" aponta pra `/en/` em `dist/en/404/index.html` e `/es/` em `dist/es/404/index.html` (home do próprio idioma atual, não a raiz `/` em português) — `getRelativeLocaleUrl(idioma)` sem `path`.

**Caminho de saída real, diferente do assumido originalmente** (confirmado rodando o build): só `src/pages/404.astro` (raiz, sem prefixo de idioma) recebe o tratamento especial do Astro que gera `dist/404.html` direto, sem subpasta — porque a rota dele bate exatamente com o padrão reservado `/404` que o Astro trata como página de erro (`ROUTE404_RE` em `node_modules/astro/dist/core/routing/internal/route-errors.js`). `src/pages/en/404.astro` e `src/pages/es/404.astro` têm rota `/en/404` e `/es/404` — não batem com esse padrão reservado — então o Astro as trata como páginas comuns, no formato `directory` padrão: saem em `dist/en/404/index.html` e `dist/es/404/index.html` (com subpasta), não em `dist/en/404.html`.

**Limitação conhecida, fora do controle deste código** (ver revisão crítica antes da execução): essas páginas `en/404.astro`/`es/404.astro` são páginas comuns, sem nenhum vínculo com o mecanismo de erro do Astro — só são alcançadas se alguém navegar direto pra `/en/404` ou `/es/404`. Elas **não** são servidas automaticamente quando o visitante acerta uma URL quebrada de verdade sob `/en/*` ou `/es/*` — nem no `astro preview` (o servidor de preview do Astro serve sempre `dist/404.html`, hardcoded, sem olhar pra subpastas — confirmado lendo `node_modules/astro/dist/core/preview/vite-plugin-astro-preview.js`), nem, muito provavelmente, em produção na Vercel (hospedagem estática da Vercel não documenta suporte a `404.html` aninhado por diretório — confirmado na documentação oficial e em relatos da comunidade). Um link quebrado sob `/en/algumacoisa` mostra a 404 em português. As páginas continuam valendo a pena como conteúdo alcançável por link direto, mas não resolvem "404 traduzida para quem cai numa URL quebrada" — ver decisão registrada na revisão crítica do plano.

- [x] **Step 5: Commit**

```bash
git add site/src/pages/404.astro site/src/pages/en/404.astro site/src/pages/es/404.astro
git commit -m "Localiza a pagina 404 do site da marca em pt/en/es"
```

---

## Task 17: Verificação final — build completo, regressão e checklist manual no navegador

**Files:** nenhum (task de verificação, sem mudança de código).

**Interfaces:**
- Consumes: build final de todas as Tasks 1-16.

- [x] **Step 1: Build e `check` limpos**

A partir de `site/`:
```
npm run check
npm run build
```
Expected: ambos passam sem erro. Confirma o critério de conclusão "npm run check e npm run build limpos em site/".

- [x] **Step 2: Confirmar as 9 rotas existem no `dist/`**

```
Get-ChildItem dist/index.html, dist/en/index.html, dist/es/index.html, dist/faq/index.html, dist/en/faq/index.html, dist/es/faq/index.html, dist/404.html, dist/en/404/index.html, dist/es/404/index.html
```
Expected: os 9 arquivos existem (critério de conclusão "gera dist/index.html, dist/en/index.html, dist/es/index.html — e o mesmo trio pra faq e 404"). **Nota**: só a 404 raiz (`dist/404.html`) recebe o nome de arquivo especial sem subpasta — `en/404.astro` e `es/404.astro` saem como página comum, em `dist/en/404/index.html` e `dist/es/404/index.html` (confirmado rodando o build; ver nota na Task 16).

- [x] **Step 3: Regressão consolidada de `hreflang`/`og:locale`/`lang` nas 3 páginas**

```
Select-String -Path dist/index.html, dist/faq/index.html, dist/404.html -Pattern 'lang="pt-BR"'
Select-String -Path dist/en/index.html, dist/en/faq/index.html, dist/en/404/index.html -Pattern 'lang="en"'
Select-String -Path dist/es/index.html, dist/es/faq/index.html, dist/es/404/index.html -Pattern 'lang="es"'
Select-String -Path dist/faq/index.html -Pattern 'hreflang="en"|hreflang="es"'
Select-String -Path dist/404.html -Pattern 'hreflang="en"|hreflang="es"'
```
Expected: `lang` correto nas 9 páginas; `hreflang` presente também nas páginas de FAQ e 404 (o `Layout.astro` gera as 3 tags sempre, independente da página).

- [x] **Step 4: Rodar `npm run preview` e verificar manualmente no navegador (9 combinações)**

A partir de `site/`: `npm run build` (se ainda não rodou) seguido de `npm run preview`, depois abrir no navegador e conferir, para cada uma das 3 páginas (`/`, `/faq`, `/en/404`/`/es/404` — navegando **direto** pra essas URLs, não digitando uma rota quebrada qualquer, já que uma URL inválida de verdade sob `/en/` ou `/es/` mostra a 404 em português, não a traduzida — ver limitação registrada na Task 16) nos 3 idiomas (`pt`, `en`, `es`):

- [ ] Alternador PT/EN/ES visível e funcional, sem levar de volta pra `/` estando em `/en/` ou `/es/`.
- [ ] Conteúdo da página (título, parágrafos, botões) no idioma certo.
- [ ] Botão do WhatsApp abre com a mensagem certa no idioma da página.
- [ ] Link "Veja as perguntas frequentes" (Escopo, na home) leva pro FAQ no idioma atual.
- [ ] `view-source:` confirma `<html lang>`, `hreflang` e `og:locale` corretos.

Usar as ferramentas de navegador (`claude-in-chrome`) para navegar e conferir cada uma das 9 combinações; reportar qualquer divergência antes de considerar a task concluída.

- [x] **Step 5: Commit final (se sobrar algum ajuste do checklist manual)**

Se o Step 4 não apontar nenhum ajuste, esta task não gera commit novo — as Tasks 1-16 já cobrem todo o código. Se algo precisar de correção, aplicar, re-rodar Steps 1-3 e commitar normalmente.
