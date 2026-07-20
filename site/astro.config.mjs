// @ts-check
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://codigo-itinerante.vercel.app',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
    server: {
      fs: {
        // Os SVGs da marca vivem fora da raiz do Vite (../marca); libera o monorepo.
        allow: [fileURLToPath(new URL('..', import.meta.url))],
      },
    },
  },
});
