"""Prepara e instala as fontes usadas pelo template Word da marca.

Deriva duas faces estaticas ("Archivo Doc" Regular/Bold) a partir da fonte
variavel archivo.ttf, e uma face ("Martian Mono Doc" Regular) a partir da
martianmono.ttf — nomes proprios para nao colidir com um eventual Archivo/
Martian Mono "de verdade" instalado para outro fim. Instala por usuario no
Windows (sem precisar de admin).

Uso:
    pip install fonttools
    (arquivo.ttf ja deve existir ao lado, baixado para o gera_wordmark.py;
    se nao existir: curl -sL -o archivo.ttf
    "https://github.com/google/fonts/raw/main/ofl/archivo/Archivo%5Bwdth%2Cwght%5D.ttf")
    python prepara_fontes_documento.py

Rode uma vez por maquina. Reinicie o Word se estiver aberto.
"""

import os
import urllib.request
import winreg
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

AQUI = Path(__file__).parent
MARTIAN_MONO_URL = "https://github.com/google/fonts/raw/main/ofl/martianmono/MartianMono%5Bwdth%2Cwght%5D.ttf"


def baixar_martian_mono() -> Path:
    destino = AQUI / "martianmono.ttf"
    if not destino.exists():
        urllib.request.urlretrieve(MARTIAN_MONO_URL, destino)
        print(f"baixado: {destino}")
    return destino


def instancia_estatica(caminho: Path, wght: int, familia: str, subfamilia: str, negrito: bool) -> TTFont:
    """Extrai uma instancia estatica de uma fonte variavel, renomeada como fonte propria."""
    fonte = TTFont(caminho)
    instancia = instantiateVariableFont(fonte, {"wght": wght, "wdth": 100})
    nome_completo = familia if subfamilia == "Regular" else f"{familia} {subfamilia}"
    name_table = instancia["name"]
    for id_nome, valor in [
        (1, familia), (2, subfamilia), (4, nome_completo),
        (6, nome_completo.replace(" ", "-")), (16, familia), (17, subfamilia),
    ]:
        name_table.setName(valor, id_nome, 3, 1, 0x409)
        name_table.setName(valor, id_nome, 1, 0, 0)
    os2 = instancia["OS/2"]
    os2.usWeightClass = wght
    if negrito:
        os2.fsSelection = (os2.fsSelection & ~0b1000000) | 0b0100000
        instancia["head"].macStyle |= 0b01
    else:
        os2.fsSelection = (os2.fsSelection & ~0b0100000) | 0b1000000
        instancia["head"].macStyle &= ~0b01
    return instancia


def instalar_por_usuario(fonte: TTFont, nome_arquivo: str) -> None:
    """Copia a fonte para a pasta de fontes por usuario e registra no Windows."""
    pasta = Path(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts"))
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / nome_arquivo
    fonte.save(str(destino))
    nome_completo = fonte["name"].getDebugName(4)
    chave = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows NT\CurrentVersion\Fonts",
        0, winreg.KEY_SET_VALUE,
    )
    winreg.SetValueEx(chave, f"{nome_completo} (TrueType)", 0, winreg.REG_SZ, str(destino))
    winreg.CloseKey(chave)
    print(f"instalado: {nome_completo}")


def main() -> None:
    martian = baixar_martian_mono()
    instalar_por_usuario(
        instancia_estatica(AQUI / "archivo.ttf", 400, "Archivo Doc", "Regular", False),
        "archivo-doc-regular.ttf",
    )
    instalar_por_usuario(
        instancia_estatica(AQUI / "archivo.ttf", 700, "Archivo Doc", "Bold", True),
        "archivo-doc-bold.ttf",
    )
    instalar_por_usuario(
        instancia_estatica(martian, 400, "Martian Mono Doc", "Regular", False),
        "martianmono-doc-regular.ttf",
    )
    print("Fontes instaladas. Feche e reabra o Word se estiver aberto.")


if __name__ == "__main__":
    main()
