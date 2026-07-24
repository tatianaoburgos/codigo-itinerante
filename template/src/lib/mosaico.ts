/** Aspect-ratio cíclico usado pelos mosaicos de fotos (Vibe, A região):
 * a cada 3 itens, alterna retrato / quadrado / paisagem para dar ritmo à grade. */
export function aspectMosaico(indice: number): string {
  return indice % 3 === 0 ? 'aspect-4/5' : indice % 3 === 1 ? 'aspect-square' : 'aspect-4/3';
}
