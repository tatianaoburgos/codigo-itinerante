// @ts-check
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// Cliente ativo (mesmo default de src/lib/cliente.ts). Seleciona o tema por cliente.
const cliente = process.env.CLIENTE ?? 'demo';

// Domínio de produção. Na Vercel vem automático (VERCEL_PROJECT_PRODUCTION_URL);
// `SITE_URL` permite sobrescrever. Ausente localmente: URLs absolutas degradam.
const site =
  process.env.SITE_URL ??
  (process.env.VERCEL_PROJECT_PRODUCTION_URL
    ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`
    : undefined);

export default defineConfig({
  site,
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
    resolve: {
      alias: {
        // @tema -> tokens/fontes do cliente ativo. Arquivo ausente derruba a build (fail-fast).
        '@tema': fileURLToPath(new URL(`./src/styles/temas/${cliente}.css`, import.meta.url)),
      },
    },
    server: {
      fs: {
        // Fotos dos clientes vivem fora da raiz do Vite (../clientes); libera o monorepo inteiro.
        allow: [fileURLToPath(new URL('..', import.meta.url))],
      },
    },
  },
});
