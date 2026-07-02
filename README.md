# Código Itinerante

Sites institucionais para hostels/pousadas oferecidos em permuta por noites de hospedagem. Um motor reutilizável (Astro + Tailwind), dados trocados por cliente — "build once, reuse everywhere".

## Índice

- [`docs/projeto.md`](docs/projeto.md) — documento de negócio: modelo, escopo, precificação, contrato.
- [`docs/decisoes-tecnicas.md`](docs/decisoes-tecnicas.md) — decisões técnicas fechadas e justificativas.
- `template/` — o motor: projeto Astro reutilizável.
- `clientes/` — dados por cliente (`config.json` + fotos); `demo/` é o hostel fictício de vitrine.

## Estado atual

Variação 1 do motor completa (2026-07-02): 4 páginas (home, acomodações, sobre, localização) com componentes compartilhados, tema "Maré" e cliente-demo. Próximos passos: deploy da vitrine na Vercel, variações 2 e 3, contrato de permuta e documento de inputs do cliente.
