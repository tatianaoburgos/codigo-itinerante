export const idiomas = ['pt', 'en', 'es'] as const;
export type Idioma = (typeof idiomas)[number];

/** Normaliza `Astro.currentLocale` (pode vir undefined) para um Idioma válido, com pt como padrão. */
export function idiomaAtual(currentLocale: string | undefined): Idioma {
  return currentLocale !== undefined && (idiomas as readonly string[]).includes(currentLocale)
    ? (currentLocale as Idioma)
    : 'pt';
}
