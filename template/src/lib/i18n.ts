import type { CampoLocalizavel, Idioma } from './schema';

/** Resolve um campo de texto do cliente (string única ou objeto por idioma) para
 *  o idioma pedido. Se o campo for objeto e não tiver a chave do idioma pedido
 *  (idioma ativado no cliente, mas esse campo específico ainda não foi
 *  traduzido pra ele), cai para `pt`. */
export function t(campo: CampoLocalizavel, idioma: Idioma): string {
  if (typeof campo === 'string') return campo;
  return campo[idioma] ?? campo.pt;
}

/** Normaliza `Astro.currentLocale` (pode vir undefined) para um Idioma válido, com pt como padrão. */
export function idiomaAtual(currentLocale: string | undefined): Idioma {
  return currentLocale === 'en' || currentLocale === 'es' ? currentLocale : 'pt';
}
