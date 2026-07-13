import { z } from 'zod';

/** Foto de um cliente: nome do arquivo na pasta `fotos/` + texto alternativo (acessibilidade/SEO). */
export const fotoSchema = z.object({
  arquivo: z.string().min(1),
  alt: z.string().min(1),
});

/** Um tipo de acomodação do hostel (quarto compartilhado, suíte etc.). */
export const acomodacaoSchema = z.object({
  nome: z.string().min(1),
  capacidade: z.string().min(1),
  comodidades: z.array(z.string().min(1)).min(1),
  fotos: z.array(fotoSchema).min(1),
});

/** Arquivos de marca do cliente (pasta `marca/`), todos opcionais. */
export const marcaSchema = z.object({
  logo: z.string().min(1).optional(),
  favicon: z.string().min(1).optional(),
});

/**
 * Schema do config.json de cada cliente (`clientes/<slug>/config.json`).
 * A build falha se o arquivo não obedecer a este contrato.
 */
export const configClienteSchema = z.object({
  nome: z.string().min(1),
  marca: marcaSchema.optional(),
  slogan: z.string().min(1),
  descricaoSeo: z.string().min(1).max(160),
  sobre: z.object({
    historia: z.string().min(1),
    diferenciais: z.array(z.string().min(1)).min(1),
  }),
  acomodacoes: z.array(acomodacaoSchema).min(1),
  precos: z.object({
    politica: z.enum(['faixa', 'consultar']),
    faixa: z.string().optional(),
  }),
  localizacao: z.object({
    endereco: z.string().min(1),
    mapsEmbedUrl: z.url(),
    comoChegar: z.array(z.string().min(1)),
  }),
  contato: z.object({
    whatsapp: z.string().regex(/^\d{12,13}$/, 'somente dígitos, com DDI e DDD (ex.: 5571999998888)'),
    email: z.email(),
    instagram: z.string().optional(),
  }),
  atividades: z.array(z.string().min(1)),
});

export type ConfigCliente = z.infer<typeof configClienteSchema>;
export type Acomodacao = z.infer<typeof acomodacaoSchema>;
export type Foto = z.infer<typeof fotoSchema>;
