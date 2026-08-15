/** Dados de contato e identidade da autora. */
export const dados = {
  nome: "Tatiana Burgos",
  /** Número no formato wa.me: DDI + DDD + número, só dígitos. */
  whatsapp: "5581971127821",
  email: "tatianaoburgos@gmail.com",
  linkedin: "https://www.linkedin.com/in/tatianaoburgos/",
} as const;

/** Link wa.me com a mensagem pré-preenchida (localizada por idioma, ver lib/textos.ts). */
export function linkWhatsApp(mensagem: string): string {
  return `https://wa.me/${dados.whatsapp}?text=${encodeURIComponent(mensagem)}`;
}
