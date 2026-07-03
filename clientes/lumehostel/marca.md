# Marca — LumeHostel

Referência de identidade visual extraída do **Manual de Identidade Visual (MIV)**
entregue pelo cliente, produzido pela agência **Etna Comunicação**
(`etnacomunicacao@gmail.com`, `83 99925.6586` — contato **da agência**, não do hostel).
Gestor da marca: **Gabriel Lume**.

## Conceito / posicionamento

- "Seu porto seguro para renovar energias e seguir explorando"
- "Iluminando seu caminho, conectando sua jornada"
- Ativos intangíveis: **Segurança, Iluminação, Energia Recarregada, Porto Seguro**;
  também **Ponto de Orientação para viajantes**.
- Público-alvo declarado: **nômade digital** (trabalha remoto enquanto viaja).
- Tom: convidativo, simpático, simples, acolhedor.

## Cores (hexadecimal — sistema oficial pra web)

| Papel | Hex | Uso no tema (`template/src/styles/temas/lumehostel.css`) |
|---|---|---|
| Azul (primária / porto seguro) | `#1f3c8f` | `--color-mare` |
| Azul profundo | derivado `#0e1c42` | `--color-noite` |
| Azul vibrante (links) | derivado `#2f56c0` | `--color-azulejo` |
| Amarelo "lume" (luz / destaque) | `#fcbe35` | `--color-fitinha` |
| Verde (secundária) | `#3e8e40` | `--color-mata` (ainda não usada por componentes) |
| Terracota/laranja (secundária) | `#c94520` | `--color-terracota` (idem) |

## Tipografia

- MIV (pagas/proprietárias, não self-hostáveis):
  - Display/marca: **Ellograph CF** (Connary Fagen).
  - Auxiliar: **Arial Rounded MT Bold** (Monotype).
- Substitutas livres adotadas (self-host via `@fontsource-variable`, respeitando o
  espírito "arredondada, amigável, simples"):
  - Display: **Fredoka Variable** → `--font-display`.
  - Corpo: **Nunito Variable** → `--font-corpo`.
  - Mono: **Spline Sans Mono Variable** → `--font-mono`.
