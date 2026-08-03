"""Gera a proposta (.docx) para o CasaMarelo, no sistema visual da marca.

Documento comercial real (CLAUDE.md - Convencoes): usa sempre o template Word
da marca (marca/gera_template_word.py, docs/miv.md secao 5) - nunca texto
puro. Reaproveita as funcoes de cabecalho/rodape/estilo de la; so o corpo e
especifico desta proposta.

Nao inclui numero de noites nem o valor de referencia interno (R$3.000) -
isso fica para o contrato, redigido depois (docs/contrato-permuta.md).

Uso:
    python gera_proposta_casamarelo.py

Saida: proposta-casamarelo.docx
"""

import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).parent
sys.path.insert(0, str(AQUI.parent / "marca"))

from docx import Document  # noqa: E402
from docx.shared import Pt  # noqa: E402
from gera_template_word import (  # noqa: E402
    FONTE_CORPO,
    FONTE_MONO,
    QUEIMADO,
    TINTA,
    CINZA_PEDRA,
    configurar_estilos,
    configurar_secao,
    construir_cabecalho,
    construir_rodape,
    fundo_pagina,
    incorporar_fontes,
    rasterizar_svg,
)

DATA = "02/08/2026"
VALIDADE = "17/08/2026"  # +15 dias -- ajustar se a autora combinar outro prazo


def paragrafo_meta(documento: Document, rotulo: str, valor: str) -> None:
    p = documento.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r_rotulo = p.add_run(rotulo + "  ")
    r_rotulo.font.name = FONTE_MONO
    r_rotulo.font.size = Pt(9)
    r_rotulo.font.color.rgb = CINZA_PEDRA
    r_valor = p.add_run(valor)
    r_valor.font.name = FONTE_CORPO
    r_valor.font.size = Pt(11)
    r_valor.font.color.rgb = TINTA
    r_valor.font.bold = True


def titulo_documento(documento: Document, texto: str) -> None:
    espaco = documento.add_paragraph()
    espaco.paragraph_format.space_after = Pt(6)

    p = documento.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(texto)
    r.font.name = FONTE_CORPO
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = TINTA


def subtitulo(documento: Document, texto: str) -> None:
    p = documento.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(texto)
    r.font.name = FONTE_CORPO
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = QUEIMADO


def paragrafo(documento: Document, texto: str) -> None:
    p = documento.add_paragraph(texto)
    p.paragraph_format.space_after = Pt(10)


def item(documento: Document, texto_normal: str, destaque: str = "", texto_apos: str = "") -> None:
    p = documento.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(texto_normal)
    r.font.name = FONTE_CORPO
    r.font.size = Pt(11)
    r.font.color.rgb = TINTA
    if destaque:
        r_destaque = p.add_run(destaque)
        r_destaque.font.name = FONTE_CORPO
        r_destaque.font.size = Pt(11)
        r_destaque.font.bold = True
        r_destaque.font.color.rgb = QUEIMADO
        if texto_apos:
            r_apos = p.add_run(texto_apos)
            r_apos.font.name = FONTE_CORPO
            r_apos.font.size = Pt(11)
            r_apos.font.color.rgb = TINTA


def item_ausente(documento: Document, texto: str) -> None:
    p = documento.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(texto)
    r.font.name = FONTE_CORPO
    r.font.size = Pt(11)
    r.font.color.rgb = CINZA_PEDRA
    r.font.italic = True


def construir_corpo(documento: Document) -> None:
    paragrafo_meta(documento, "PARA", "CasaMarelo")
    paragrafo_meta(documento, "DATA", DATA)
    paragrafo_meta(documento, "VALIDADE", VALIDADE)

    titulo_documento(documento, "O que muda no site do CasaMarelo")
    paragrafo(
        documento,
        "Fomos ao casamarelo.com e clicamos em cada botão, cada link, cada "
        "seção do menu. O que segue é o que encontramos — e o que entregamos "
        "no lugar.",
    )

    subtitulo(documento, "O que o site atual promete e não entrega")
    item(documento, "O seletor ", "\"BR · ES · EN\"", " não leva a nenhum conteúdo em inglês ou espanhol — os links não vão a lugar nenhum.")
    item(documento, "O item de menu ", "\"Avaliações\"", " abre uma seção sem nenhum depoimento.")
    item(documento, "O item de menu ", "\"CasAMARelo Cultural\"", " abre uma seção sem nenhum conteúdo.")
    item(documento, "Nenhum dos 5 ícones de rede social (Instagram, Facebook, TikTok) leva a um perfil real.")
    item(documento, "O site não tem dados estruturados nem SEO básico configurado para o Google.")

    subtitulo(documento, "O que a Código Itinerante entrega")
    item(documento, "Site institucional real em ", "três idiomas", ": português, inglês e espanhol.")
    item(documento, "Seção de ", "depoimentos reais", ", publicada a partir das avaliações do Google e do Booking.")
    item(documento, "Seções de ", "comodidades, região e como chegar", ", ilustradas e com fotos.")
    item(documento, "Redes sociais ", "linkadas de verdade", " no site.")
    item(documento, "Configuração completa de ", "SEO técnico", ": dados estruturados, sitemap, meta description.")
    item(documento, "Site ", "leve e rápido", ", pensado primeiro para celular.")
    item(documento, "Reserva simples e direta ", "pelo WhatsApp", ".")

    subtitulo(documento, "O que não está incluído")
    item_ausente(documento, "Sistema de reservas com checagem de disponibilidade.")
    item_ausente(documento, "Pagamento online.")
    item_ausente(documento, "Integração com Booking, Airbnb, Hostelworld ou outras plataformas.")
    item_ausente(documento, "Produção de fotos ou vídeos profissionais.")

    subtitulo(documento, "Próximo passo")
    paragrafo(
        documento,
        "O combinado completo — noites de hospedagem, prazos e forma de "
        "entrega — vem no contrato, a seguir.",
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        marca_dir = AQUI.parent / "marca"
        wordmark_png = tmp_path / "wordmark.png"
        monograma_png = tmp_path / "monograma.png"
        rasterizar_svg(marca_dir / "wordmark-claro.svg", wordmark_png)
        rasterizar_svg(marca_dir / "monograma-claro.svg", monograma_png)

        documento = Document()
        largura_util = configurar_secao(documento)
        configurar_estilos(documento)
        fundo_pagina(documento, "FBF9F4")
        construir_cabecalho(documento, largura_util, wordmark_png, "PROPOSTA")
        construir_rodape(documento, largura_util, monograma_png, "codigoitinerante.com.br")
        construir_corpo(documento)

        destino = AQUI / "proposta-casamarelo.docx"
        documento.save(str(destino))

    incorporar_fontes(destino)
    print(f"gerado com fontes incorporadas: {destino}")


if __name__ == "__main__":
    main()
