# Fontes das fotos

Proveniência de cada arquivo de foto do LumeHostel. Fotos do hostel (`capa.jpg`, `cozinha.jpg`,
`jardim.jpg`) vêm das fotos públicas do próprio estabelecimento no
Google Maps (categoria "Do proprietário" / fotos publicadas pelo perfil do negócio) — nenhuma é
foto de hóspede nem de banco de imagens. Fotos da região (`regiao-*.jpg`) vêm do Wikimedia
Commons, com licença livre conferida e atribuição anotada abaixo.

## Fotos do hostel (Google Maps, perfil do LumeHostel)

| Arquivo | Origem | Autor | Licença | Atribuição exigida? |
|---|---|---|---|---|
| `capa.jpg` | Google Maps (perfil LumeHostel) — já existia antes desta task | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `cozinha.jpg` | Google Maps (perfil LumeHostel), galeria "Fotos e vídeos" | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `jardim.jpg` | Booking.com (galeria de fotos do LumeHostel), foto 3/55 — mostra o pátio de entrada com mesas/cadeiras e a fachada com o logo | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `dormitorio-misto-6.jpg` | Enviada pela autora, foto real do quarto correspondente no hostel | LumeHostel | Foto própria do hostel | Não |
| `dormitorio-misto-8.jpg` | Enviada pela autora, foto real do quarto correspondente no hostel | LumeHostel | Foto própria do hostel | Não |
| `dormitorio-feminino-4.jpg` | Enviada pela autora, foto real do quarto correspondente no hostel | LumeHostel | Foto própria do hostel | Não |
| `dormitorio-feminino-6.jpg` | Enviada pela autora, foto real do quarto correspondente no hostel | LumeHostel | Foto própria do hostel | Não |
| `quarto-duplo.jpg` | Enviada pela autora, foto real do quarto correspondente no hostel | LumeHostel | Foto própria do hostel | Não |
| `suite-standard.jpg` | Enviada pela autora, foto real do quarto correspondente no hostel | LumeHostel | Foto própria do hostel | Não |
| `vibe-patio-noite.jpg` | Enviada pela autora, foto real do estabelecimento — pátio à noite, com mesa comunitária e varal de luzes | LumeHostel | Foto própria do hostel | Não |
| `coworking.jpg` | Google Maps (galeria pública do LumeHostel), URL indicada pela autora em 2026-07-14 — sala de coworking com mesas e cadeiras ergonômicas | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `redario.jpg` | Booking.com (galeria do LumeHostel, foto 685884944), URL indicada pela autora em 2026-07-14 — redário no corredor externo | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `destaque-cozinha.jpg` | Booking.com (galeria do LumeHostel, foto 685884933), URL indicada pela autora em 2026-07-14 — copa amarela com mural terracota | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `destaque-recepcao.jpg` | Booking.com (galeria do LumeHostel, foto 685884930), URL indicada pela autora em 2026-07-14 — recepção ensolarada | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `vibe-patio-entrada.jpg` | Google Maps ou Booking, galeria pública do próprio estabelecimento LumeHostel | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `vibe-patio-trabalho.jpg` | Google Maps ou Booking, galeria pública do próprio estabelecimento LumeHostel | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `vibe-cozinha-bar.jpg` | Google Maps ou Booking, galeria pública do próprio estabelecimento LumeHostel | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `vibe-corredor-cores.jpg` | Google Maps ou Booking, galeria pública do próprio estabelecimento LumeHostel | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `vibe-recepcao.jpg` | Google Maps ou Booking, galeria pública do próprio estabelecimento LumeHostel | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `vibe-mural-recados.jpg` | Google Maps ou Booking, galeria pública do próprio estabelecimento LumeHostel | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `vibe-entrada-frase.jpg` | Google Maps ou Booking, galeria pública do próprio estabelecimento LumeHostel | LumeHostel | Foto publicada pelo estabelecimento | Não |
| `vibe-cozinha-corredor.jpg` | Google Maps, galeria pública do próprio estabelecimento LumeHostel (foto de visualização específica) | LumeHostel | Foto publicada pelo estabelecimento | Não |

Observação (2026-07-13): a versão anterior de `jardim.jpg` (baixada do Google Maps) era na
verdade um frame de vídeo/reel — formato vertical (720x1280) com legenda queimada na imagem
("Quando sua casa") — e foi descartada por não ser publicável. Frames de vídeo com texto
sobreposto não servem como foto do site, mesmo quando aparecem misturados às fotos normais na
galeria. A foto atual vem da galeria de fotos do Booking.com (não do Google Maps), é horizontal e
sem nenhum texto sobreposto.

Observação: não foi encontrada, na galeria pública do Google Maps nem na galeria do Booking.com,
nenhuma foto claramente identificável como coworking, churrasqueira, sala de jogos ou jardim com
redes — essas comodidades do config ficam **sem foto** (o schema trata `comodidade.foto` como
opcional). A galeria do Booking tem fotos de uma sala de estar com sofá e TV, mas a única limpa o
suficiente para uso mostra um hóspede com o rosto visível — descartada por privacidade. Para não
representar algo que não é, optei por não forçar nenhuma foto genérica com esses rótulos.

Observação (2026-07-13): revisitando as galerias para ampliar o mosaico "A vibe", também não foi
encontrada nenhuma foto de espaço de coworking dedicado — `vibe-patio-trabalho.jpg` mostra apenas
um notebook sobre a mesa comunitária do pátio, e não uma sala de trabalho. Por isso a comodidade
"Coworking ergonômico" continua sem foto no config.

Observação (2026-07-14): removidos `vibe-redario.jpg`, `vibe-recepcao.jpg`, `vibe-cozinha-bar.jpg`
e `vibe-cozinha-corredor.jpg` — mostravam as mesmas cenas das fotos novas (`redario.jpg`,
`destaque-recepcao.jpg`, `destaque-cozinha.jpg`) e de `cozinha.jpg`, gerando repetição entre
seções. A foto anterior do Farol do Cabo Branco (uma placa comemorativa, autor Ridiculopathy/CC0)
foi substituída pela vista cênica do Cácio Murilo.

Observação (2026-07-13): o arquivo baixado como `vibe-mural-entrada.jpg` era, na verdade, um
duplicado byte a byte de `capa.jpg` (mesmo hash SHA-256) — provavelmente a mesma foto salva duas
vezes durante a curadoria. Foi descartado (arquivo removido e entrada retirada do `vibe` do
config) para não repetir a mesma imagem duas vezes no mosaico.

## Fotos da região (Wikimedia Commons)

| Arquivo | Ponto | Origem (URL) | Autor | Licença | Atribuição exigida? |
|---|---|---|---|---|---|
| `regiao-praia-manaira.jpg` | Praia de Manaíra (mostra também a Praia do Bessa ao fundo) | https://commons.wikimedia.org/wiki/File:João-Pessoa-Praia-Manaíra-Bessa.jpg | Patrick | CC BY-SA 3.0 | Sim |
| `regiao-orla-bessa.jpg` | Orla do Bessa | https://commons.wikimedia.org/wiki/File:Praia_do_bessa_joao_pessoa.png | Matheus Jampa da Silva | CC BY-SA 4.0 | Sim |
| `regiao-por-do-sol-jacare.jpg` | Pôr do sol no Jacaré | https://commons.wikimedia.org/wiki/File:Por_do_Sol_na_Praia_do_Jacaré_em_João_Pessoa_-_Pb_-_Brasil_(8624763746).jpg | Marinelson Almeida | CC BY 2.0 | Sim |
| `regiao-centro-historico.jpg` | Centro Histórico de João Pessoa | https://commons.wikimedia.org/wiki/File:Vista_do_Centro_Histórico_de_João_Pessoa_PB_BR.jpg | Rogerio121402 | CC BY-SA 4.0 | Sim |
| `regiao-farol-cabo-branco.jpg` | Farol do Cabo Branco | https://commons.wikimedia.org/wiki/File:CacioMurilo_FarolCaboBranco_JoãoPessoa_PB_(39994462855).jpg | Cácio Murilo / MTur Destinos | Domínio público (Public Domain Mark, Flickr) | Não |
| `regiao-estacao-cabo-branco.jpg` | Estação Cabo Branco de Ciência, Cultura e Artes | https://commons.wikimedia.org/wiki/File:Estação_Cabo_Branco_de_Ciência,_Cultura_e_Artes_-_João_Pessoa,_Paraíba,_Brasil.jpg | A. Júnior | CC BY 2.0 | Sim |

Todas as fotos da região foram baixadas em resolução original via Wikimedia Commons
(`Special:FilePath`) e redimensionadas (lado maior <= 1600px, JPEG qualidade ~85-90) com `sharp`
antes de entrar no repositório. Onde a licença exige atribuição (todas exceto CC0), o crédito ao
autor deve constar em algum lugar do site (por exemplo, no rodapé da página ou em texto alt/legend
da imagem) — a implementação exata fica para a Task 6.
