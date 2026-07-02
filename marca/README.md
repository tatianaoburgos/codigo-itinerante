# marca/ — ativos da identidade visual

Identidade **"Estrada 1 — Lâmpada de hostel"**. O manual completo (paleta, regras, aplicações) é o **[MIV](../docs/miv.md)**; este diretório guarda os arquivos prontos para uso.

## Arquivos

| Arquivo | Uso |
|---|---|
| `wordmark-escuro.svg` | Logo sobre fundo Breu/escuro (Cal + Âmbar) |
| `wordmark-claro.svg` | Logo sobre fundo Papel/claro (Tinta + Queimado) |
| `wordmark-mono.svg` | Fallback monocromático — herda a cor do contexto (`currentColor`) |
| `monograma-*.svg` | "C*I*" para favicon/avatar, mesmas três variantes |
| `tokens.css` | Paleta, fontes e detalhes como custom properties (`--ci-*`) |

Os SVGs têm as fontes **convertidas em curvas** — não dependem de fonte instalada e podem ir direto para documentos, e-mail ou impressão.

## Como foram gerados

Glifos extraídos de Archivo (instância wght 600) e Instrument Serif Italic com `fontTools`, seguindo a construção do MIV §2 (corpo do itálico 10% maior, tracking −0.03em no "Código"). Para regenerar (ex.: mudança de cor), use `gera_wordmark.py` — as instruções de uso estão na docstring do próprio script.
