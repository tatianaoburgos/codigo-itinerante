import type { APIRoute } from 'astro';

/** robots.txt gerado na build; aponta o sitemap quando há domínio (`site`) definido. */
export const GET: APIRoute = ({ site }) => {
  const linhas = ['User-agent: *', 'Allow: /'];
  if (site) {
    linhas.push(`Sitemap: ${new URL('sitemap-index.xml', site).href}`);
  }
  return new Response(linhas.join('\n') + '\n', {
    headers: { 'Content-Type': 'text/plain' },
  });
};
