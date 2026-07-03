/** Dados de contato e identidade da autora. Valores [PROVISORIO] são preenchidos na Task 9. */
export const dados = {
  nome: "Tatiana Burgos",
  /** Número no formato wa.me: DDI + DDD + número, só dígitos. [PROVISORIO] */
  whatsapp: "5500000000000",
  mensagemWhatsApp: "Oi! Tenho um hostel e quero saber mais sobre a permuta.",
  email: "[PROVISORIO]",
  linkedin: "[PROVISORIO]",
} as const;

/** Link wa.me com a mensagem pré-preenchida. */
export function linkWhatsApp(): string {
  return `https://wa.me/${dados.whatsapp}?text=${encodeURIComponent(dados.mensagemWhatsApp)}`;
}
