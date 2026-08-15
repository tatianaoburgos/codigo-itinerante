// @ts-check
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://codigo-itinerante.vercel.app',
  i18n: {
    locales: ['pt', 'en', 'es'],
    defaultLocale: 'pt',
    routing: { prefixDefaultLocale: false },
  },
  integrations: [
    sitemap({
      // Sem isso, o sitemap só exclui a 404 raiz (`/404`) — `en/404` e `es/404`
      // não recebem o tratamento especial de página de erro do Astro (são
      // páginas comuns, ver Nav i18n) e vazariam pro sitemap como conteúdo.
      // Com `i18n` configurado, @astrojs/sitemap exclui `<locale>/404` também.
      i18n: {
        defaultLocale: 'pt',
        locales: { pt: 'pt-BR', en: 'en', es: 'es' },
      },
    }),
  ],
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
