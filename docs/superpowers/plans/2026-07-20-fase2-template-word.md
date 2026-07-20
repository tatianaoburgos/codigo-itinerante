# Fase 2 — Template Word Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Gerar `marca/template-documento.docx` — o arquivo-base com a assinatura visual da marca (cabeçalho, rodapé, cores, tipografia conforme `docs/miv.md` §5), pronto para a autora duplicar em propostas/briefings/contratos reais.

**Architecture:** Dois scripts Python em `marca/`, seguindo o padrão já usado por `gera_wordmark.py`/`gera_icones.py` (fonte de verdade em código, regenerável). `prepara_fontes_documento.py` roda uma vez por máquina: deriva faces estáticas Regular/Bold nomeadas "Archivo Doc"/"Martian Mono Doc" a partir das fontes variáveis já usadas no MIV, e instala por usuário no Windows. `gera_template_word.py` monta o `.docx` via `python-docx` (rasterizando wordmark/monograma para PNG só para embutir as imagens) e, ao final, abre o arquivo via automação COM do Word para incorporar as fontes.

**Tech Stack:** Python 3.12, `python-docx`, `fontTools` (já usado por `gera_wordmark.py`), `svglib`+`reportlab`+`rlPyCairo` (rasterização SVG→PNG), `pywin32` (automação COM do Word).

## Global Constraints

- Português brasileiro em nomes de função, comentários e mensagens; sem emojis.
- Type hints em todas as funções (parâmetros e retorno).
- Só o sistema visual — sem texto real de proposta/briefing/contrato (decisão da autora, spec §"Decisões" item 1). Todo conteúdo do corpo é placeholder entre colchetes, ex. `[Nome do cliente]`.
- Um único arquivo de saída genérico (`template-documento.docx`), rótulo do cabeçalho fica "DOCUMENTO" — não gerar proposta.docx/briefing.docx/contrato.docx separados (decisão da autora).
- Cores exatas do MIV: Papel `#FBF9F4`, Tinta `#1A1915`, Queimado `#B85C2E`, Cinza-pedra `#97928A`.
- Fontes derivadas ganham nomes próprios "Archivo Doc" / "Martian Mono Doc" — nunca "Archivo"/"Martian Mono" puro, para não colidir com uma eventual instalação futura das fontes completas.
- Instrument Serif **não** é necessária nesta fase (o §5 do MIV não usa itálico serifado em documentos) — não instalar, não referenciar. Se isso for cobrado depois, é uma correção de escopo consciente, não um esquecimento.

---

### Task 1: Preparar e instalar as fontes do documento

**Files:**
- Create: `marca/prepara_fontes_documento.py`

**Interfaces:**
- Produces: duas fontes TrueType instaladas por usuário no Windows, com nome completo (`name` ID 4) `"Archivo Doc"`, `"Archivo Doc Bold"` e `"Martian Mono Doc"`. As Tasks seguintes (`gera_template_word.py`) referenciam essas famílias pelos nomes-base `"Archivo Doc"` e `"Martian Mono Doc"` (constantes `FONTE_CORPO`/`FONTE_MONO`).

- [ ] **Step 1: Escrever o script**

Criar `marca/prepara_fontes_documento.py`:

```python
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
```

- [ ] **Step 2: Confirmar que `archivo.ttf` existe, instalar dependências e rodar**

```
ls marca/archivo.ttf
```
Se não existir, baixar primeiro (comando no docstring do Step 1). Depois:

```
pip install fonttools
python marca/prepara_fontes_documento.py
```

Esperado: baixa `marca/martianmono.ttf`, imprime três linhas `instalado: Archivo Doc` / `instalado: Archivo Doc Bold` / `instalado: Martian Mono Doc`, e a linha final de aviso.

- [ ] **Step 3: Verificar o registro no Windows**

```
python -c "
import winreg
chave = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows NT\CurrentVersion\Fonts')
i = 0
encontrados = []
while True:
    try:
        nome, _, _ = winreg.EnumValue(chave, i)
        if 'Doc' in nome:
            encontrados.append(nome)
        i += 1
    except OSError:
        break
print(sorted(encontrados))
"
```

Esperado: lista contendo `'Archivo Doc (TrueType)'`, `'Archivo Doc Bold (TrueType)'`, `'Martian Mono Doc (TrueType)'`.

- [ ] **Step 4: Commit**

```bash
git add marca/prepara_fontes_documento.py
git commit -m "Fase 2: script que deriva e instala as fontes do template Word"
```

(`marca/martianmono.ttf` não deve ser commitado — mesmo padrão de `archivo.ttf`/`instrumentserif-italic.ttf`, que já ficam de fora do git. Confirmar com `git status` que só o `.py` foi adicionado.)

---

### Task 2: Esqueleto do gerador — página, estilos, cabeçalho e rodapé

**Files:**
- Create: `marca/gera_template_word.py`

**Interfaces:**
- Consumes: `marca/wordmark-claro.svg`, `marca/monograma-claro.svg` (já existem); fontes `"Archivo Doc"`/`"Martian Mono Doc"` instaladas na Task 1 (referenciadas pelo nome — o script roda e salva independente de as fontes estarem instaladas, mas o Word só vai renderizar certo se estiverem).
- Produces: `marca/template-documento.docx` (com corpo placeholder de uma linha — Task 3 substitui). Funções reutilizadas pelas Tasks seguintes: `configurar_secao(documento) -> Emu`, `construir_corpo(documento) -> None` (Task 3 substitui o corpo desta função), `main()` (Task 4 acrescenta a chamada de incorporação de fontes ao final).

- [ ] **Step 1: Escrever o gerador**

Criar `marca/gera_template_word.py`:

```python
"""Gera o template Word (.docx) com a assinatura da marca Código Itinerante.

Sistema visual conforme docs/miv.md secao 5 ("Documentos"): cabecalho com
wordmark + tipo do documento, rodape com monograma + contato + paginacao,
fundo Papel, corpo em Archivo com destaques em Queimado. E o arquivo-base
generico que a autora duplica para propostas/briefings/contratos reais —
nao inclui texto comercial de verdade, so conteudo placeholder.

Uso:
    python prepara_fontes_documento.py   # uma vez, instala as fontes
    pip install python-docx svglib reportlab rlPyCairo pywin32
    python gera_template_word.py

Saida: template-documento.docx
"""

import tempfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Emu, Pt, RGBColor
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

AQUI = Path(__file__).parent

PAPEL = 0xFBF9F4
TINTA = RGBColor(0x1A, 0x19, 0x15)
QUEIMADO = RGBColor(0xB8, 0x5C, 0x2E)
CINZA_PEDRA = RGBColor(0x97, 0x92, 0x8A)

FONTE_CORPO = "Archivo Doc"
FONTE_MONO = "Martian Mono Doc"


def rasterizar_svg(caminho_svg: Path, destino_png: Path, dpi: int = 300) -> None:
    """Converte um SVG em PNG com fundo Papel, para embutir no docx."""
    desenho = svg2rlg(str(caminho_svg))
    renderPM.drawToFile(desenho, str(destino_png), fmt="PNG", bg=PAPEL, dpi=dpi)


def borda_paragrafo(paragrafo, lado: str, cor_hex: str, tamanho_oitavos_pt: int, espaco_pt: int) -> None:
    """Adiciona uma regua (borda simples) a um lado do paragrafo via OOXML."""
    pPr = paragrafo._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    borda = OxmlElement(f"w:{lado}")
    borda.set(qn("w:val"), "single")
    borda.set(qn("w:sz"), str(tamanho_oitavos_pt))
    borda.set(qn("w:space"), str(espaco_pt))
    borda.set(qn("w:color"), cor_hex)
    pBdr.append(borda)
    pPr.append(pBdr)


def campo_simples(paragrafo, instrucao: str, texto_cache: str) -> None:
    """Insere um campo de Word (ex.: PAGE, NUMPAGES) com um valor de cache exibido."""
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), instrucao)
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = texto_cache
    r.append(t)
    fld.append(r)
    paragrafo._p.append(fld)


def fundo_pagina(documento: Document, cor_hex: str) -> None:
    """Define a cor de fundo da pagina (elemento w:background, filho de w:document)."""
    fundo = OxmlElement("w:background")
    fundo.set(qn("w:color"), cor_hex)
    documento.element.insert(0, fundo)


def configurar_secao(documento: Document) -> Emu:
    """A4, margens de 2,5cm (2cm em cima/baixo). Retorna a largura util em EMU."""
    secao = documento.sections[0]
    secao.page_width = Cm(21)
    secao.page_height = Cm(29.7)
    secao.left_margin = secao.right_margin = Cm(2.5)
    secao.top_margin = secao.bottom_margin = Cm(2)
    return Emu(secao.page_width - secao.left_margin - secao.right_margin)


def configurar_estilos(documento: Document) -> None:
    normal = documento.styles["Normal"]
    normal.font.name = FONTE_CORPO
    normal.font.size = Pt(11)
    normal.font.color.rgb = TINTA
    normal.paragraph_format.space_after = Pt(10)
    normal.paragraph_format.line_spacing = 1.3


def construir_cabecalho(documento: Document, largura_util: Emu, wordmark_png: Path, rotulo: str) -> None:
    secao = documento.sections[0]
    p = secao.header.paragraphs[0]
    p.style = documento.styles["Normal"]
    p.paragraph_format.tab_stops.add_tab_stop(largura_util, WD_TAB_ALIGNMENT.RIGHT)
    p.add_run().add_picture(str(wordmark_png), height=Cm(0.9))
    r = p.add_run()
    r.add_tab()
    r.add_text(rotulo)
    r.font.name = FONTE_MONO
    r.font.size = Pt(10)
    r.font.color.rgb = QUEIMADO
    borda_paragrafo(p, "bottom", "B85C2E", 16, 6)


def construir_rodape(documento: Document, largura_util: Emu, monograma_png: Path, site: str) -> None:
    secao = documento.sections[0]
    p = secao.footer.paragraphs[0]
    p.style = documento.styles["Normal"]
    p.paragraph_format.tab_stops.add_tab_stop(Emu(largura_util // 2), WD_TAB_ALIGNMENT.CENTER)
    p.paragraph_format.tab_stops.add_tab_stop(largura_util, WD_TAB_ALIGNMENT.RIGHT)
    p.add_run().add_picture(str(monograma_png), height=Cm(0.6))

    r_site = p.add_run()
    r_site.add_tab()
    r_site.add_text(site)
    r_site.font.name = FONTE_MONO
    r_site.font.size = Pt(8)
    r_site.font.color.rgb = CINZA_PEDRA

    r_pag = p.add_run()
    r_pag.add_tab()
    r_pag.font.name = FONTE_MONO
    r_pag.font.size = Pt(8)
    r_pag.font.color.rgb = CINZA_PEDRA
    campo_simples(p, "PAGE", "1")

    r_barra = p.add_run(" / ")
    r_barra.font.name = FONTE_MONO
    r_barra.font.size = Pt(8)
    r_barra.font.color.rgb = CINZA_PEDRA
    campo_simples(p, "NUMPAGES", "1")

    borda_paragrafo(p, "top", "97928A", 4, 6)


def construir_corpo(documento: Document) -> None:
    documento.add_paragraph("(corpo em construcao)")


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        wordmark_png = tmp_path / "wordmark.png"
        monograma_png = tmp_path / "monograma.png"
        rasterizar_svg(AQUI / "wordmark-claro.svg", wordmark_png)
        rasterizar_svg(AQUI / "monograma-claro.svg", monograma_png)

        documento = Document()
        largura_util = configurar_secao(documento)
        configurar_estilos(documento)
        fundo_pagina(documento, "FBF9F4")
        construir_cabecalho(documento, largura_util, wordmark_png, "DOCUMENTO")
        construir_rodape(documento, largura_util, monograma_png, "codigoitinerante.com.br")
        construir_corpo(documento)

        destino = AQUI / "template-documento.docx"
        documento.save(str(destino))
        print(f"gerado: {destino}")


if __name__ == "__main__":
    main()
```

**Nota importante sobre os tab stops do cabeçalho/rodapé**: o estilo embutido do Word "Header"/"Footer" já vem com tab stops padrão (`center` a 234pt, `right` a 468pt, herdados do tamanho de página Letter). Se o parágrafo do cabeçalho/rodapé mantiver esse estilo, o Word **combina** esses tabs herdados com os que a gente adiciona via `add_tab_stop`, e o primeiro `\t` pode pular para o tab errado (herdado) em vez do nosso. Por isso `p.style = documento.styles["Normal"]` é obrigatório logo depois de pegar `secao.header.paragraphs[0]`/`secao.footer.paragraphs[0]`, **antes** de adicionar os tab stops — isso já está no código acima, não remover.

- [ ] **Step 2: Instalar dependências e rodar**

```
pip install python-docx svglib reportlab rlPyCairo pywin32
python marca/gera_template_word.py
```

Esperado: imprime `gerado: ...marca/template-documento.docx` sem erros. Se falhar em `import cairocffi`/`cairo`, o pacote errado foi instalado — confirmar que é `rlPyCairo` (traz `pycairo` com binário pré-compilado para Windows) e não `cairosvg` (depende de uma DLL nativa do Cairo que não vem instalada).

- [ ] **Step 3: Verificar a estrutura do arquivo gerado**

```
python -c "
from docx import Document
doc = Document('marca/template-documento.docx')
h = doc.sections[0].header.paragraphs[0]
f = doc.sections[0].footer.paragraphs[0]
print('header:', [r.text for r in h.runs])
print('footer:', [r.text for r in f.runs])
"
```

Esperado: `header: ['', '\tDOCUMENTO']` e `footer: ['', '\tcodigoitinerante.com.br', '\t', ' / ']` (o texto dos campos de página não aparece aqui — são elementos `w:fldSimple`, não `w:r` comuns; isso é esperado).

- [ ] **Step 4: Commit**

```bash
git add marca/gera_template_word.py
git commit -m "Fase 2: esqueleto do gerador do template Word (pagina, cabecalho, rodape)"
```

---

### Task 3: Corpo do documento — metadados, título, texto, destaque

**Files:**
- Modify: `marca/gera_template_word.py:142-143` (função `construir_corpo`)

**Interfaces:**
- Consumes: `TINTA`, `QUEIMADO`, `CINZA_PEDRA`, `FONTE_CORPO`, `FONTE_MONO` (constantes da Task 2).
- Produces: `construir_corpo(documento)` preenchida — nenhuma outra função muda de assinatura.

- [ ] **Step 1: Substituir a função placeholder**

Em `marca/gera_template_word.py`, localizar:

```python
def construir_corpo(documento: Document) -> None:
    documento.add_paragraph("(corpo em construcao)")
```

Substituir por:

```python
def construir_corpo(documento: Document) -> None:
    for rotulo, valor in [
        ("PARA", "[Nome do cliente]"),
        ("DATA", "[00/00/0000]"),
        ("VALIDADE", "[00/00/0000]"),
    ]:
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

    espaco = documento.add_paragraph()
    espaco.paragraph_format.space_after = Pt(6)

    titulo = documento.add_paragraph()
    titulo.paragraph_format.space_before = Pt(6)
    titulo.paragraph_format.space_after = Pt(12)
    r_titulo = titulo.add_run("[Título do documento]")
    r_titulo.font.name = FONTE_CORPO
    r_titulo.font.size = Pt(20)
    r_titulo.font.bold = True
    r_titulo.font.color.rgb = TINTA

    documento.add_paragraph(
        "[Texto do documento. Corpo em Archivo Regular, 11pt, entrelinha 1,3 "
        "— o padrão de leitura confortável em tela e impresso.]"
    )

    destaque = documento.add_paragraph()
    destaque.add_run("Um trecho de destaque, como ")
    r_destaque = destaque.add_run("uma cláusula importante ou um valor")
    r_destaque.font.color.rgb = QUEIMADO
    r_destaque.font.bold = True
    destaque.add_run(
        ", aparece em Queimado negrito — sempre um trecho, nunca o parágrafo inteiro."
    )
```

- [ ] **Step 2: Regenerar e verificar**

```
python marca/gera_template_word.py
python -c "
from docx import Document
doc = Document('marca/template-documento.docx')
for p in doc.paragraphs:
    print(repr(p.text))
"
```

Esperado: 3 linhas de metadados (`PARA  [Nome do cliente]` etc.), uma linha vazia, `[Título do documento]`, o parágrafo de corpo, e o parágrafo de destaque terminando em "...nunca o parágrafo inteiro." — 7 parágrafos no total.

- [ ] **Step 3: Commit**

```bash
git add marca/gera_template_word.py
git commit -m "Fase 2: corpo do template com metadados, titulo, texto e destaque"
```

---

### Task 4: Incorporar as fontes no arquivo final via automação COM

**Files:**
- Modify: `marca/gera_template_word.py:1-16` (imports/docstring — nenhuma mudança de conteúdo, só referência de linha para a próxima edição)
- Modify: `marca/gera_template_word.py` (adicionar função `incorporar_fontes` e chamá-la em `main()`)

**Interfaces:**
- Consumes: `Path` (já importado). `win32com.client` (novo import, só usado dentro da função nova).
- Produces: `incorporar_fontes(caminho_docx: Path) -> None`.

- [ ] **Step 1: Adicionar a função de incorporação**

Em `marca/gera_template_word.py`, logo acima de `def main() -> None:`, inserir:

```python
def incorporar_fontes(caminho_docx: Path) -> None:
    """Abre o docx no Word e resalva com as fontes incorporadas no arquivo."""
    import win32com.client as win32

    word = win32.gencache.EnsureDispatch("Word.Application")
    word.Visible = False
    try:
        word.Options.PrintBackgrounds = True
        doc = word.Documents.Open(str(caminho_docx))
        doc.EmbedTrueTypeFonts = True
        doc.Save()
        doc.Close()
    finally:
        word.Quit()


```

- [ ] **Step 2: Chamar a função ao final de `main()`**

Localizar, dentro de `main()`:

```python
        destino = AQUI / "template-documento.docx"
        documento.save(str(destino))
        print(f"gerado: {destino}")
```

Substituir por:

```python
        destino = AQUI / "template-documento.docx"
        documento.save(str(destino))

    incorporar_fontes(destino)
    print(f"gerado com fontes incorporadas: {destino}")
```

(Reparar na indentação: a chamada `incorporar_fontes(destino)` fica **fora** do bloco `with tempfile.TemporaryDirectory()`, já que só precisa do arquivo `.docx` salvo, não mais dos PNGs temporários.)

- [ ] **Step 3: Regenerar e verificar a incorporação**

```
python marca/gera_template_word.py
```

Esperado: imprime `gerado com fontes incorporadas: ...template-documento.docx`, sem janelas do Word visíveis na tela (roda com `Visible = False`).

```
python -c "
import zipfile
z = zipfile.ZipFile('marca/template-documento.docx')
fontes = [n for n in z.namelist() if 'font' in n.lower()]
print(fontes)
"
```

Esperado: lista contendo `word/fontTable.xml` e pelo menos um `word/fonts/fontN.odttf` (as fontes incorporadas, formato ofuscado do Word).

- [ ] **Step 4: Confirmar que nenhum processo do Word ficou aberto**

```
powershell -Command "Get-Process WINWORD -ErrorAction SilentlyContinue"
```

Esperado: nenhuma saída (nenhum processo `WINWORD.EXE` rodando). Se algum aparecer, encerrar com `taskkill /PID <pid> /F` antes de prosseguir — indica que o `word.Quit()` não rodou (provavelmente por uma exceção antes do `finally`); investigar a causa, não apenas matar o processo e seguir.

- [ ] **Step 5: Commit**

```bash
git add marca/gera_template_word.py
git commit -m "Fase 2: incorpora as fontes no docx final via automacao COM do Word"
```

---

### Task 5: Documentação — MIV, backlog e CLAUDE.md

**Files:**
- Modify: `docs/miv.md:195` (item pendente da seção 7)
- Modify: `docs/ideias-backlog.md` (status da Fase 2)
- Modify: `CLAUDE.md` (seção "Marca do negócio")

**Interfaces:** nenhuma — só documentação.

- [ ] **Step 1: Marcar a pendência do MIV como resolvida**

Em `docs/miv.md`, localizar (seção 7, "Entregáveis"):

```
5. Pendente: aplicar o cabeçalho padrão nos documentos comerciais quando forem redigidos (proposta, contrato).
```

Substituir por:

```
5. ✅ Template-base em `marca/template-documento.docx` (2026-07-20), gerado por
   `marca/gera_template_word.py` a partir de `marca/prepara_fontes_documento.py`
   (instala as fontes "Archivo Doc"/"Martian Mono Doc"). Aplica o cabeçalho/rodapé
   desta seção com conteúdo placeholder — o texto real de cada documento
   (proposta, briefing, contrato) fica para uma fase futura, a combinar.
```

- [ ] **Step 2: Marcar a Fase 2 no backlog**

Em `docs/ideias-backlog.md`, seção "Status", localizar:

```
- [ ] Fase 2 — Template Word
```

Substituir por:

```
- [x] Fase 2 — Template Word (2026-07-20): só o sistema visual, sem texto
  comercial real — isso fica para uma conversa futura sobre os tipos de
  documento. Spec `docs/superpowers/specs/2026-07-20-fase2-template-word-design.md`.
```

Também atualizar a linha da Fase 2 na seção "Roteiro" (mesmo arquivo), que hoje diz:

```
### Fase 2 — Template Word com a assinatura da marca
- Documento .docx padrão para todos os documentos do projeto: fontes da marca (Archivo + Instrument Serif — verificar disponibilidade/fallback no Word), cores do MIV, iconografia da Fase 1, cara extremamente profissional.
- Depende da Fase 1 (iconografia pronta).
```

Substituir por:

```
### Fase 2 — Template Word com a assinatura da marca — CONCLUÍDA (2026-07-20)
- `marca/template-documento.docx`, gerado por `marca/gera_template_word.py`. Fontes
  Archivo + Martian Mono (Instrument Serif não é usada em documentos, só no site);
  disponibilidade/fallback no Word resolvidos instalando faces próprias
  ("Archivo Doc"/"Martian Mono Doc") via `marca/prepara_fontes_documento.py`.
- Escopo desta fase é só o sistema visual — texto real de proposta/briefing/contrato
  fica para uma conversa futura com a autora sobre os tipos de documento.
```

- [ ] **Step 3: Atualizar o CLAUDE.md**

Em `CLAUDE.md`, na seção "Marca do negócio (`marca/`)", localizar a frase que termina em:

```
Versão navegável do manual em `marca/miv.html` (gerada a partir de `docs/miv.md`), com exportação em PDF em `marca/MIV-codigo-itinerante.pdf`.
```

Acrescentar logo depois, no mesmo parágrafo:

```
 Template Word em `marca/template-documento.docx` (Fase 2, 2026-07-20): gerado por
 `marca/gera_template_word.py`, aplica o cabeçalho/rodapé/tipografia de
 `docs/miv.md` §5 com conteúdo placeholder; `marca/prepara_fontes_documento.py`
 instala as fontes "Archivo Doc"/"Martian Mono Doc" (faces estáticas derivadas
 das variáveis, nomes próprios para não colidir com uma instalação futura das
 fontes completas) por usuário no Windows e roda uma vez por máquina.
```

- [ ] **Step 4: Commit**

```bash
git add docs/miv.md docs/ideias-backlog.md CLAUDE.md
git commit -m "Fase 2: documenta o template Word concluido no MIV, backlog e CLAUDE.md"
```

---

## Self-review (feito na escrita)

- **Cobertura do spec**: escopo só-visual (Task 3, conteúdo em colchetes), arquivo-base único rotulado "DOCUMENTO" (Task 2), fontes instaladas+incorporadas (Tasks 1 e 4), estrutura completa do §5 do MIV — cabeçalho/metadados/corpo/destaque/rodapé (Tasks 2-3), registro da pendência resolvida (Task 5).
- **Sem placeholders no plano**: todo código é o código real, já testado manualmente ponta-a-ponta (rasterização, tab stops, campos de página, incorporação de fontes) antes de escrever este plano — não é código hipotético.
- **Risco não-óbvio documentado inline**: a nota na Task 2 sobre `p.style = documento.styles["Normal"]` existe porque um bug real (tabs herdados do estilo "Header"/"Footer" do Word colidindo com os tabs adicionados) foi encontrado e corrigido durante a validação deste plano — sem essa linha, o cabeçalho/rodapé renderiza com o texto no lugar errado.
- **Consistência de tipos**: `Emu` usado consistentemente como tipo de retorno de `configurar_secao`/parâmetro de `construir_cabecalho`/`construir_rodape`; `Document`, `Path` conforme a assinatura de cada função em todas as tasks.
