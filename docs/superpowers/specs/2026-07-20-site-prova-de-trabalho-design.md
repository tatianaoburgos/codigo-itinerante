# Seção "prova de trabalho" no site da marca

Data: 2026-07-20
Escopo: `site/` (site da própria marca Código Itinerante), não o `template/`.

## Problema

O site da marca argumenta bem — explica a dor, a proposta, o escopo e quem faz — mas
não mostra nenhum trabalho pronto. Quem chega precisa acreditar na palavra. Existe um
site real no ar (LumeHostel, `https://lumehostel.vercel.app`), e ele não aparece em
lugar nenhum.

## O que a seção afirma (e o que não afirma)

A seção prova **ofício**: que a autora sabe construir o site de um hostel e que existe
um exemplar público disso. Ela **não** afirma que o modelo de permuta por noites já
rodou.

Isso é uma decisão de fato, não de tom: o site do LumeHostel foi feito de presente para
um amigo dono de hostel, justamente para formar portfólio. Não houve acordo de noites.
Qualquer frase sobre permuta, noites pagas ou domínio próprio no nome do cliente seria
falsa e está fora do escopo desta seção. O domínio próprio, aliás, segue pendente — o
site está num subdomínio da Vercel (`clientes/lumehostel/PENDENCIAS.md:56`).

O dono do hostel foi consultado e concorda com o site aparecendo no portfólio.

## Formato: um case, não uma grade

Com um único trabalho, uma grade de portfólio mostra um card e um buraco — comunica
falta. Um case único bem tratado comunica escolha. A estrutura vira grade quando
existir um segundo trabalho; não antes.

## Componente e posição

Novo `site/src/components/ProvaDeTrabalho.astro`, inserido em
`site/src/pages/index.astro` entre `<QuemSouEu />` e `<ComoFunciona />`.

Segue o padrão das outras seções:

- container `mx-auto w-full max-w-3xl px-6 py-10 md:py-12`
- `<Eyebrow texto="prova de" destaque="trabalho" />`

O conteúdo do case fica escrito no próprio componente, não em `site/src/dados.ts`.
É um case só; extrair para dado estruturado só se justifica com dois ou mais.

## A peça visual

Moldura de navegador construída em markup — não embutida na imagem. Razões: fica nítida
em qualquer densidade de tela, usa os tokens de cor da marca e mantém o PNG menor.

- Barra superior arredondada com três círculos e o texto `lumehostel.vercel.app` em
  `font-mono text-pedra`.
- Abaixo da barra, a captura desktop.
- Celular sobreposto no canto inferior direito, vazando um pouco da moldura, com borda
  arredondada grossa e a captura mobile dentro.
- Abaixo do breakpoint `md`, o celular não é renderizado: no espaço disponível ele
  viraria uma miniatura ilegível. Fica só a moldura de navegador.

O propósito do par desktop + celular é provar responsividade. A maioria dos hóspedes
chega pelo celular, então isso é argumento de venda, não enfeite.

### Capturas

Duas capturas reais de `https://lumehostel.vercel.app`, da primeira dobra:

- desktop: viewport 1440×900
- mobile: viewport 390×844

Salvas em `site/src/assets/portfolio/` e servidas via `astro:assets` (mesmo mecanismo
de `QuemSouEu.astro`, que usa `<Image>` sobre `src/assets/tatiana.jpg`).

## Texto

Título: `LumeHostel — João Pessoa, PB`

Corpo:

> Site institucional completo: acomodações, comodidades, a região, depoimentos e
> localização. Reserva direta pelo WhatsApp. No ar desde julho de 2026.

Botão: "Ver o site no ar", reusando o pill de borda âmbar do link do LinkedIn em
`site/src/components/QuemSouEu.astro:35`, com `target="_blank"` e `rel="noopener"`.

## Degradê da página

O fundo da página é um degradê contínuo breu → âmbar calibrado por percentual de
rolagem (`.pagina-degrade` em `site/src/styles/global.css:28`). Hoje o breu sólido vai
até 43% e a cor começa a entrar no Manifesto.

Com a seção nova, muda: **o breu sólido passa a cobrir Hero → QuemSouEu → prova de
trabalho, e a cor começa a entrar no ComoFunciona.** A seção nova cai em fundo breu,
o que favorece o print — o site do LumeHostel é claro e terracota, e contrasta.

O âmbar cheio continua chegando pouco antes do `CtaFinal`, que permanece na zona clara.

Os percentuais novos são **medidos, não estimados**: com a página montada, medir
`offsetTop / scrollHeight` de cada seção em desktop e em mobile e reescrever as paradas
do gradiente a partir dessas medidas. Foi assim que a Fase 3 chegou nos números atuais
(`docs/superpowers/specs/2026-07-19-site-degrade-fase3-design.md`).

## Riscos registrados

- **Fotos sem autorização formal.** As fotos do LumeHostel vieram das presenças públicas
  do próprio estabelecimento (Google Maps e Booking) e a autorização de uso segue
  pendente (`clientes/lumehostel/PENDENCIAS.md:63`). Elas aparecem no print. Isso não é
  um risco novo criado por esta seção — decorre de o site do LumeHostel já estar
  público — mas fica anotado.
- **Site ainda não validado pelo cliente.** Textos, dados das acomodações e contatos
  ainda aguardam confirmação (`clientes/lumehostel/PENDENCIAS.md:57`). Se ele pedir
  mudanças, o print desatualiza. Recapturar é barato; não é bloqueio.

## Fora de escopo

- Depoimento do dono do hostel no site da marca (decidido: fica para depois).
- Página dedicada de portfólio, ou rota `/portfolio`. O site é one-page.
- Estrutura de grade ou lista de cases. Entra quando existir um segundo trabalho.
