// @ts-check
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// `site` fica indefinido até o deploy (Task 11); a imagem OG usa Astro.url como fallback.
export default defineConfig({
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
