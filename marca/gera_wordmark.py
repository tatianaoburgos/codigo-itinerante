"""Gera os SVGs do wordmark e monograma do Código Itinerante com fontes em curvas.

Wordmark W2 (MIV §2): "Código" (Archivo 600, tracking -0.03em) + "Itinerante"
(Instrument Serif Italic, corpo 10% maior), na mesma baseline.
Monograma M4 (MIV §2): "C" e "I" ambos em Archivo 600, com o I inclinado 12°
e na cor de acento.

Uso:
    pip install fonttools
    curl -sL -o archivo.ttf "https://github.com/google/fonts/raw/main/ofl/archivo/Archivo%5Bwdth%2Cwght%5D.ttf"
    curl -sL -o instrumentserif-italic.ttf "https://github.com/google/fonts/raw/main/ofl/instrumentserif/InstrumentSerif-Italic.ttf"
    python gera_wordmark.py

Os .ttf ficam ao lado do script e não precisam ser versionados.
Saída: wordmark-{escuro,claro,mono}.svg e monograma-{escuro,claro,mono}.svg
"""

from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

AQUI = Path(__file__).parent

CODIGO_SIZE = 100.0
ITINERANTE_SIZE = 110.0  # ~10% maior, conforme MIV
TRACKING_EM = -0.03      # só no "Código"
WORD_GAP = 30.0
PAD = 12.0

CORES = {
    "escuro": ("#F4F1E8", "#E39A3B"),  # Cal / Âmbar — para fundo Breu
    "claro": ("#1A1915", "#B85C2E"),   # Tinta / Queimado — para fundo Papel
    "mono": ("currentColor", "currentColor"),
}


def carregar_archivo_600() -> TTFont:
    font = TTFont(AQUI / "archivo.ttf")
    instantiateVariableFont(font, {"wght": 600, "wdth": 100}, inplace=True)
    return font


def render_texto(font: TTFont, texto: str, size: float, tracking_em: float,
                 x0: float, slant_tan: float = 0.0) -> tuple[str, float, float, float, float]:
    """Desenha `texto` a partir de x0 na baseline y=0, com inclinação opcional.

    Retorna (path_d, x_final, y_min, y_max, x_max) em coordenadas SVG (y para baixo).
    """
    upm = font["head"].unitsPerEm
    scale = size / upm
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    hmtx = font["hmtx"]

    pen = SVGPathPen(glyph_set)
    x = x0
    y_min, y_max = 0.0, 0.0
    x_max = x0
    for ch in texto:
        nome = cmap[ord(ch)]
        glifo = glyph_set[nome]
        # y invertido: fontes têm y para cima, SVG para baixo;
        # yx inclina o glifo (topo para a direita) quando slant_tan > 0
        glifo.draw(TransformPen(pen, (scale, 0, slant_tan * scale, -scale, x, 0)))
        bp = BoundsPen(glyph_set)
        glifo.draw(bp)
        if bp.bounds is not None:
            b_xmin, b_ymin, b_xmax, b_ymax = bp.bounds
            y_min = min(y_min, -b_ymax * scale)
            y_max = max(y_max, -b_ymin * scale)
            cantos_x = [
                x + (bx + slant_tan * by) * scale
                for bx in (b_xmin, b_xmax) for by in (b_ymin, b_ymax)
            ]
            x_max = max(x_max, *cantos_x)
        avanco, _ = hmtx[nome]
        x += avanco * scale + tracking_em * size
    x -= tracking_em * size  # sem tracking depois do último glifo
    return pen.getCommands(), x, y_min, y_max, x_max


def svg(paths: list[tuple[str, str]], largura: float, y_min: float,
        y_max: float, titulo: str) -> str:
    w = largura + 2 * PAD
    h = (y_max - y_min) + 2 * PAD
    corpo = "\n".join(
        f'  <path fill="{cor}" transform="translate({PAD} {PAD - y_min})" d="{d}"/>'
        for d, cor in paths
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" '
        f'role="img" aria-label="{titulo}">\n'
        f"  <title>{titulo}</title>\n{corpo}\n</svg>\n"
    )


def gerar(arq_saida: str, partes: list[tuple[TTFont, str, float, float, float]],
          gap: float, titulo: str) -> None:
    for variante, (cor_sans, cor_italico) in CORES.items():
        cores = [cor_sans, cor_italico]
        paths: list[tuple[str, str]] = []
        x = 0.0
        y_min, y_max = 0.0, 0.0
        largura = 0.0
        for i, (font, texto, size, tracking, slant) in enumerate(partes):
            d, x, p_ymin, p_ymax, p_xmax = render_texto(font, texto, size, tracking, x, slant)
            paths.append((d, cores[i]))
            y_min = min(y_min, p_ymin)
            y_max = max(y_max, p_ymax)
            largura = max(largura, x, p_xmax)
            if i < len(partes) - 1:
                x += gap
        conteudo = svg(paths, largura, y_min, y_max, titulo)
        destino = AQUI / f"{arq_saida}-{variante}.svg"
        destino.write_text(conteudo, encoding="utf-8")
        print(f"gerado: {destino}")


def main() -> None:
    archivo = carregar_archivo_600()
    instrument = TTFont(AQUI / "instrumentserif-italic.ttf")

    gerar(
        "wordmark",
        [
            (archivo, "Código", CODIGO_SIZE, TRACKING_EM, 0.0),
            (instrument, "Itinerante", ITINERANTE_SIZE, 0.0, 0.0),
        ],
        WORD_GAP,
        "Código Itinerante",
    )
    # Monograma M4: dupla sans no mesmo peso, movimento só na inclinação do I
    gerar(
        "monograma",
        [
            (archivo, "C", CODIGO_SIZE, 0.0, 0.0),
            (archivo, "I", CODIGO_SIZE, 0.0, 0.2126),  # tan(12°)
        ],
        4.0,
        "Código Itinerante",
    )


if __name__ == "__main__":
    main()
