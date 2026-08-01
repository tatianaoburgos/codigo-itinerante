// @ts-check
import { existsSync, readFileSync, createReadStream } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// Cliente ativo (mesmo default de src/lib/cliente.ts). Seleciona o tema por cliente.
const cliente = process.env.CLIENTE ?? 'demo';

// Pasta do cliente ativo (mesma regra de src/lib/cliente.ts: clientes/<slug>).
const pastaClienteAtivo = fileURLToPath(new URL(`../clientes/${cliente}/`, import.meta.url));

/** Nome do arquivo de vídeo do hero do cliente ativo, lido direto do config.json
 * (sem passar pelo schema Zod completo — aqui só precisamos desse campo).
 * @returns {string | undefined}
 */
function nomeVideoHero() {
  const caminhoConfig = path.join(pastaClienteAtivo, 'config.json');
  if (!existsSync(caminhoConfig)) return undefined;
  const config = JSON.parse(readFileSync(caminhoConfig, 'utf-8'));
  return config.marca?.heroVideo;
}

const arquivoVideoHero = nomeVideoHero();

/**
 * Serve (dev) e emite (build) o vídeo do hero do cliente ativo sem passar por
 * `import.meta.glob`. O glob precisaria do padrão literal `clientes/*\/fotos/*.mp4`
 * (Vite exige string estática, não dá pra parametrizar pelo cliente ativo em
 * tempo de build) e, com `query: '?url'`, isso copia pro dist o vídeo de TODOS
 * os clientes que tiverem um, não só do ativo — vazando vídeo sem autorização
 * de um cliente para o build publicado de outro. Aqui servimos/emitimos só o
 * arquivo exato referenciado em `marca.heroVideo` do cliente ativo.
 * @param {string} pastaFotos
 * @param {string | undefined} arquivo
 * @returns {import('vite').Plugin}
 */
function servirVideoDoCliente(pastaFotos, arquivo) {
  return {
    name: 'servir-video-cliente',
    configureServer(server) {
      if (!arquivo) return;
      server.middlewares.use((req, res, next) => {
        if (req.url !== `/video/${arquivo}`) return next();
        const caminho = path.join(pastaFotos, arquivo);
        if (!existsSync(caminho)) return next();
        res.setHeader('Content-Type', arquivo.endsWith('.webm') ? 'video/webm' : 'video/mp4');
        createReadStream(caminho).pipe(res);
      });
    },
    generateBundle() {
      if (!arquivo) return;
      const caminho = path.join(pastaFotos, arquivo);
      if (!existsSync(caminho)) return;
      this.emitFile({
        type: 'asset',
        fileName: `video/${arquivo}`,
        source: readFileSync(caminho),
      });
    },
  };
}

// Domínio de produção. Na Vercel vem automático (VERCEL_PROJECT_PRODUCTION_URL);
// `SITE_URL` permite sobrescrever. Ausente localmente: URLs absolutas degradam.
const site =
  process.env.SITE_URL ??
  (process.env.VERCEL_PROJECT_PRODUCTION_URL
    ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`
    : undefined);

export default defineConfig({
  site,
  i18n: {
    locales: ['pt', 'en'],
    defaultLocale: 'pt',
    routing: { prefixDefaultLocale: false },
  },
  integrations: [sitemap()],
  vite: {
    plugins: [
      tailwindcss(),
      servirVideoDoCliente(path.join(pastaClienteAtivo, 'fotos'), arquivoVideoHero),
    ],
    resolve: {
      alias: {
        // @tema -> tokens/fontes do cliente ativo. Arquivo ausente derruba a build (fail-fast).
        '@tema': fileURLToPath(new URL(`./src/styles/temas/${cliente}.css`, import.meta.url)),
      },
    },
    server: {
      fs: {
        // Fotos/config dos clientes e ativos da marca vivem fora da raiz do Vite
        // (../clientes, ../marca) — libera só essas duas pastas, não o monorepo inteiro.
        allow: [
          fileURLToPath(new URL('../clientes', import.meta.url)),
          fileURLToPath(new URL('../marca', import.meta.url)),
        ],
      },
    },
  },
});
