import type { CampoLocalizavel, Idioma } from './schema';

/** Resolve um campo de texto do cliente (string única ou par pt/en) para o idioma pedido. */
export function t(campo: CampoLocalizavel, idioma: Idioma): string {
  return typeof campo === 'string' ? campo : campo[idioma];
}

/** Normaliza `Astro.currentLocale` (pode vir undefined) para um Idioma válido, com pt como padrão. */
export function idiomaAtual(currentLocale: string | undefined): Idioma {
  return currentLocale === 'en' ? 'en' : 'pt';
}
