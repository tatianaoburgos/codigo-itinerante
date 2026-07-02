// @ts-check
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
    server: {
      fs: {
        // Fotos dos clientes vivem fora da raiz do Vite (../clientes); libera o monorepo inteiro.
        allow: [fileURLToPath(new URL('..', import.meta.url))],
      },
    },
  },
});
