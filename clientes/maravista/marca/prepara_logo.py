"""Recorta o logo raster do Mar a Vista (fundo solido opaco, sem alpha) em duas
pecas usaveis pelo motor: o lockup completo (circulo + assinatura) e o emblema
sozinho (para favicon/apple-touch-icon/divisor de secao). O fundo do arquivo
original e um quase-preto solido (RGB ~12,16,20) -- vira transparente por
chroma-key com transicao suave (evita halo duro na borda anti-aliased).

Uso: python prepara_logo.py (roda a partir desta pasta).
"""

from pathlib import Path

from PIL import Image

PASTA = Path(__file__).parent
ORIGINAL = PASTA / "logo-original.png"
COR_FUNDO = (12, 16, 20)
LIMITE_TRANSPARENTE = 25
LIMITE_OPACO = 55
# Caixa generosa em torno do aro branco (medido: x 37-220, y 43-176 no
# original 240x251), com margem de seguranca e parando antes do texto.
# Nota: o selo original e um unico circulo continuo (nao um circulo separado
# do texto) -- a franja branca sob o disco azul emenda direto no fundo branco
# onde a assinatura "Mar a Vista" fica escrita, sem faixa preta entre os dois.
# Por isso o limite inferior precisou ser medido pelo primeiro pixel de texto
# (varredura por cor: comeca em y=169) em vez do y=176 estimado no brief --
# 192 cortava letras da assinatura. 168 fica dentro da franja branca do
# circulo, com folga de seguranca antes do texto.
CAIXA_EMBLEMA = (20, 28, 232, 168)


def chroma_key(imagem: Image.Image) -> Image.Image:
    """Torna transparente todo pixel proximo de COR_FUNDO, com transicao suave."""
    rgba = imagem.convert("RGBA")
    pixels = rgba.load()
    largura, altura = rgba.size
    for y in range(altura):
        for x in range(largura):
            r, g, b, _ = pixels[x, y]
            distancia = (
                (r - COR_FUNDO[0]) ** 2 + (g - COR_FUNDO[1]) ** 2 + (b - COR_FUNDO[2]) ** 2
            ) ** 0.5
            if distancia <= LIMITE_TRANSPARENTE:
                alfa = 0
            elif distancia >= LIMITE_OPACO:
                alfa = 255
            else:
                alfa = round(
                    255 * (distancia - LIMITE_TRANSPARENTE) / (LIMITE_OPACO - LIMITE_TRANSPARENTE)
                )
            pixels[x, y] = (r, g, b, alfa)
    return rgba


def recortar_pelo_alfa(imagem: Image.Image) -> Image.Image:
    """Corta as margens totalmente transparentes."""
    caixa = imagem.getbbox()
    return imagem.crop(caixa) if caixa else imagem


def gerar_apple_touch_icon(emblema: Image.Image, tamanho: int, cor_fundo: str) -> Image.Image:
    """Compoe o emblema sobre um fundo solido quadrado (sem transparencia)."""
    fundo = Image.new("RGBA", (tamanho, tamanho), cor_fundo)
    reduzido = emblema.copy()
    reduzido.thumbnail((round(tamanho * 0.82), round(tamanho * 0.82)))
    x = (tamanho - reduzido.width) // 2
    y = (tamanho - reduzido.height) // 2
    fundo.paste(reduzido, (x, y), reduzido)
    return fundo.convert("RGB")


def main() -> None:
    original = Image.open(ORIGINAL)

    lockup = recortar_pelo_alfa(chroma_key(original))
    lockup.save(PASTA / "logo.png")

    emblema = recortar_pelo_alfa(chroma_key(original.crop(CAIXA_EMBLEMA)))
    emblema.save(PASTA / "icone.png")

    favicon = emblema.copy()
    favicon.thumbnail((32, 32))
    favicon.save(PASTA / "favicon-32.png")

    apple_touch_icon = gerar_apple_touch_icon(emblema, 180, "#0b2c55")
    apple_touch_icon.save(PASTA / "apple-touch-icon.png")

    print("Gerados: logo.png, icone.png, favicon-32.png, apple-touch-icon.png")


if __name__ == "__main__":
    main()
