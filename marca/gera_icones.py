"""Gera os SVGs definitivos da iconografia da marca em marca/icones/.

Fonte de verdade do desenho: mockups/icones-refino.html (rodada 2, aprovada em
2026-07-19). Conjunto: 1B1, 2A, 3B, 4L sem nuvem, 5A, 6A. Regras na secao
"Iconografia" do docs/miv.md.

Uso: python marca/gera_icones.py  (a partir da raiz do repositorio)
Gera 6 conceitos x 2 pesos (cheio/miudo) x 2 fundos (breu/papel) = 24 arquivos.
"""

from pathlib import Path

FUNDOS: dict[str, dict[str, str]] = {
    # linha (L), acento (A) e a cor do fundo (F) para os furos/vazados
    "breu": {"L": "#F4F1E8", "A": "#E39A3B", "F": "#0A0A09"},
    "papel": {"L": "#1A1915", "A": "#B85C2E", "F": "#FBF9F4"},
}

PESO_TRACO: dict[str, str] = {"cheio": "3.25", "miudo": "4.5"}

# Elementos por conceito e peso. Placeholders: {L} linha, {A} acento, {F} fundo.
ICONES: dict[str, dict[str, list[str]]] = {
    "site-proprio": {
        "cheio": [
            '<path d="M10 13 Q9 13 9 15 L9 49 Q9 51 11 51 L53 51 Q55 51 55 49 L55 15 Q55 13 53 13 Z"/>',
            '<path d="M9 23 L55 23"/>',
            '<circle cx="15.5" cy="18" r="1.8" fill="{L}" stroke="none"/>',
            '<circle cx="21.5" cy="18" r="1.8" fill="{L}" stroke="none"/>',
            '<path d="M21 42 L32 31 L43 42 Z" fill="{A}" stroke="none"/>',
            '<path d="M24 42 L24 47 L40 47 L40 42"/>',
        ],
        "miudo": [
            '<path d="M10 11 Q9 11 9 13 L9 51 Q9 53 11 53 L53 53 Q55 53 55 51 L55 13 Q55 11 53 11 Z"/>',
            '<path d="M9 22 L55 22"/>',
            '<path d="M20 44 L32 32 L44 44 Z" fill="{A}" stroke="none"/>',
            '<path d="M24 44 L24 49 L40 49 L40 44"/>',
        ],
    },
    "permuta": {
        # A seta de baixo e o mesmo desenho da de cima girado 180 graus.
        "cheio": [
            '<path d="M15 30 Q17 13 32 13 Q42 13 47 21"/>',
            '<path d="M45 13 L53 22 L42 26 Z" fill="{L}" stroke="none"/>',
            '<g transform="rotate(180 32 32)">'
            '<path stroke="{A}" d="M15 30 Q17 13 32 13 Q42 13 47 21"/>'
            '<path d="M45 13 L53 22 L42 26 Z" fill="{A}" stroke="none"/>'
            "</g>",
        ],
        "miudo": [
            '<path d="M15 30 Q17 13 32 13 Q42 13 47 21"/>',
            '<path d="M44 11 L54 22 L41 27 Z" fill="{L}" stroke="none"/>',
            '<g transform="rotate(180 32 32)">'
            '<path stroke="{A}" d="M15 30 Q17 13 32 13 Q42 13 47 21"/>'
            '<path d="M44 11 L54 22 L41 27 Z" fill="{A}" stroke="none"/>'
            "</g>",
        ],
    },
    "noites": {
        "cheio": [
            '<path d="M42 8 A9 9 0 1 0 50 20 A7 7 0 1 1 42 8 Z" fill="{A}" stroke="none"/>',
            '<path d="M12 30 L12 50"/>',
            '<path d="M12 44 L52 44 L52 50"/>',
            '<path d="M12 38 Q13 34 17 34 L24 34 Q28 34 28 38"/>',
            '<path d="M28 38 L52 38 L52 44"/>',
        ],
        "miudo": [
            '<path d="M41 6 A10 10 0 1 0 50 20 A8 8 0 1 1 41 6 Z" fill="{A}" stroke="none"/>',
            '<path d="M11 28 L11 52"/>',
            '<path d="M11 44 L53 44 L53 52"/>',
            '<path d="M11 36 L53 36 L53 44"/>',
        ],
    },
    "hostel": {
        "cheio": [
            '<path d="M16 32 Q31 16 33 17 L48 32"/>',
            '<path d="M20 32 L20 50 L44 50 L44 32"/>',
            '<circle cx="32" cy="27" r="4" stroke-width="2.25"/>',
            '<path d="M23 37 L28 37 L28 42 L23 42 Z" stroke-width="2.25"/>',
            '<path d="M36 37 L41 37 L41 42 L36 42 Z" stroke-width="2.25"/>',
            '<path d="M29 50 L29 44 Q29 41 32 41 Q35 41 35 44 L35 50 Z" fill="{A}" stroke="none"/>',
            '<path d="M26 50 L25 53 L39 53 L38 50" stroke-width="2.25"/>',
            '<path d="M10 53 L10 47"/>',
            '<circle cx="10" cy="43" r="4" fill="{L}" stroke="none"/>',
            '<path d="M54 53 L54 47"/>',
            '<circle cx="54" cy="43" r="4" fill="{L}" stroke="none"/>',
            '<path d="M6 53 L58 53"/>',
        ],
        "miudo": [
            '<path d="M15 30 Q31 14 33 15 L49 30"/>',
            '<path d="M19 30 L19 50 L45 50 L45 30"/>',
            '<path d="M27 50 L27 43 Q27 39 32 39 Q37 39 37 43 L37 50 Z" fill="{A}" stroke="none"/>',
            '<path d="M10 50 L10 46"/>',
            '<circle cx="10" cy="41.5" r="4.5" fill="{L}" stroke="none"/>',
            '<path d="M54 50 L54 46"/>',
            '<circle cx="54" cy="41.5" r="4.5" fill="{L}" stroke="none"/>',
            '<path d="M5 50 L59 50"/>',
        ],
    },
    "estrada": {
        "cheio": [
            '<path d="M18 33 A14 14 0 0 1 46 33 Z" fill="{A}" stroke="none"/>',
            '<path d="M32 10 L32 14" stroke-width="2.25"/>',
            '<path d="M15 19 L18 22" stroke-width="2.25"/>',
            '<path d="M49 19 L46 22" stroke-width="2.25"/>',
            '<path d="M4 33 L60 33"/>',
            '<path d="M16 56 L28 33"/>',
            '<path d="M48 56 L36 33"/>',
            '<path d="M32 52 L32 48" stroke-width="2.25"/>',
            '<path d="M32 42 L32 39" stroke-width="2.25"/>',
        ],
        "miudo": [
            '<path d="M17 33 A15 15 0 0 1 47 33 Z" fill="{A}" stroke="none"/>',
            '<path d="M32 8 L32 13"/>',
            '<path d="M14 17 L18 21"/>',
            '<path d="M50 17 L46 21"/>',
            '<path d="M4 33 L60 33"/>',
            '<path d="M15 57 L28 33"/>',
            '<path d="M49 57 L36 33"/>',
        ],
    },
    "contato": {
        "cheio": [
            '<path d="M17 12 Q11 12 11 19 L11 33 Q11 40 18 40 L21 40 L21 50 L31 40 L46 40 '
            'Q53 40 53 33 L53 19 Q53 12 47 12 Z" fill="{A}" stroke="none"/>',
            '<circle cx="24" cy="26" r="1" stroke="{F}" stroke-width="4"/>',
            '<circle cx="32" cy="26" r="1" stroke="{F}" stroke-width="4"/>',
            '<circle cx="40" cy="26" r="1" stroke="{F}" stroke-width="4"/>',
        ],
        "miudo": [
            '<path d="M16 10 Q9 10 9 18 L9 34 Q9 42 17 42 L20 42 L20 54 L32 42 L47 42 '
            'Q55 42 55 34 L55 18 Q55 10 48 10 Z" fill="{A}" stroke="none"/>',
            '<circle cx="23" cy="26" r="1.5" stroke="{F}" stroke-width="6"/>',
            '<circle cx="32" cy="26" r="1.5" stroke="{F}" stroke-width="6"/>',
            '<circle cx="41" cy="26" r="1.5" stroke="{F}" stroke-width="6"/>',
        ],
    },
}


def gera_svg(elementos: list[str], peso: str, cores: dict[str, str]) -> str:
    """Monta um SVG 64x64 com os atributos de traco no elemento raiz."""
    corpo = "\n  ".join(e.format(**cores) for e in elementos)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" '
        f'stroke="{cores["L"]}" stroke-width="{PESO_TRACO[peso]}" '
        'stroke-linecap="round" stroke-linejoin="round">\n'
        f"  {corpo}\n</svg>\n"
    )


def main() -> None:
    destino = Path(__file__).parent / "icones"
    destino.mkdir(exist_ok=True)
    for conceito, pesos in ICONES.items():
        for peso, elementos in pesos.items():
            for fundo, cores in FUNDOS.items():
                arquivo = destino / f"icone-{conceito}-{peso}-{fundo}.svg"
                arquivo.write_text(gera_svg(elementos, peso, cores), encoding="utf-8")
                print(f"gerado: {arquivo}")


if __name__ == "__main__":
    main()
