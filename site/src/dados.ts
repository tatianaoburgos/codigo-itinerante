/** Dados de contato e identidade da autora. */
export const dados = {
  nome: "Tatiana Burgos",
  /** Número no formato wa.me: DDI + DDD + número, só dígitos. */
  whatsapp: "5581971127821",
  mensagemWhatsApp: "Oi! Tenho um hostel e quero saber mais sobre a permuta.",
  email: "tatianaoburgos@gmail.com",
  linkedin: "https://www.linkedin.com/in/tatianaoburgos/",
} as const;

/** Link wa.me com a mensagem pré-preenchida. */
export function linkWhatsApp(): string {
  return `https://wa.me/${dados.whatsapp}?text=${encodeURIComponent(dados.mensagemWhatsApp)}`;
}
