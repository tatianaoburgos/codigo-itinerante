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
  simbolo: z.string().min(1).optional(),
  /** Ícone raster (PNG) para Apple touch icon e fallback de favicon. */
  appleTouchIcon: z.string().min(1).optional(),
  faviconPng: z.string().min(1).optional(),
  /** Vídeo full-bleed do hero (mp4/webm), no lugar da foto capa.jpg. */
  heroVideo: z.string().min(1).optional(),
  /** Frame estático (jpg) usado como poster do vídeo e fallback sem motion. */
  heroVideoPoster: z.string().min(1).optional(),
  /** Quando true, o logo do menu fica sempre alinhado à esquerda, mesmo no
   *  layout mobile empilhado (padrão: centralizado). */
  logoFixoEsquerda: z.boolean().optional(),
  /** Quando true, o logo (raster) aparece só no menu; a hero usa o nome em texto.
   *  Para logos tipo selo/circular que não escalam bem em tamanho grande. */
  logoApenasNoMenu: z.boolean().optional(),
  /** Quando true, a hero usa a composição centralizada (nome grande no meio,
   *  frase + símbolo no canto inferior direito) em vez do bloco padrão
   *  ancorado embaixo à esquerda. */
  heroCentralizado: z.boolean().optional(),
});

/** Símbolos artísticos disponíveis na biblioteca compartilhada (SimboloComodidade.astro). */
export const simbolosComodidade = [
  'cozinha',
  'patio',
  'cowork',
  'rede',
  'churrasqueira',
  'jogos',
  'bagagem',
  'acolhedor',
  'vista-mar',
  'ar-condicionado',
  'recepcao',
  'wifi',
] as const;

/** Comodidade do hostel, opcionalmente ilustrada com foto ou com símbolo artístico. */
export const comodidadeSchema = z.object({
  nome: z.string().min(1),
  descricao: z.string().min(1).optional(),
  foto: fotoSchema.optional(),
  simbolo: z.enum(simbolosComodidade).optional(),
});

/** Seção de destaque full-bleed: foto que fica fixa enquanto a página rola, com frase por cima. */
export const destaqueSchema = z.object({
  frase: z.string().min(1),
  foto: fotoSchema,
});

/** Ponto de interesse da região, com distância a partir do hostel. */
export const pontoRegiaoSchema = z.object({
  nome: z.string().min(1),
  descricao: z.string().min(1),
  distancia: z.string().min(1),
  foto: fotoSchema,
  credito: z.string().min(1).optional(),
});

/** Depoimento público real (Booking/Google), validável pelo cliente. */
export const depoimentoSchema = z.object({
  texto: z.string().min(1),
  nome: z.string().min(1),
  fonte: z.string().min(1),
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
    foto: fotoSchema.optional(),
  }),
  acomodacoes: z.array(acomodacaoSchema).min(1).optional(),
  precos: z.object({
    politica: z.enum(['faixa', 'consultar']),
    faixa: z.string().optional(),
  }),
  localizacao: z.object({
    endereco: z.string().min(1),
    /** Campos estruturados (opcionais) usados no PostalAddress do JSON-LD. */
    logradouro: z.string().min(1).optional(),
    bairro: z.string().min(1).optional(),
    cidade: z.string().min(1).optional(),
    uf: z.string().min(1).optional(),
    cep: z.string().min(1).optional(),
    mapsEmbedUrl: z.url().optional(),
    comoChegar: z.array(z.string().min(1)).optional(),
    /** Frase curta opcional, exibida ao fim da seção Localização. */
    resumo: z.string().min(1).optional(),
  }),
  contato: z.object({
    whatsapp: z.string().regex(/^\d{12,13}$/, 'somente dígitos, com DDI e DDD (ex.: 5571999998888)'),
    email: z.email(),
    instagram: z.string().optional(),
  }),
  comodidades: z.array(comodidadeSchema).min(1).optional(),
  regiao: z.array(pontoRegiaoSchema).min(1).optional(),
  depoimentos: z.array(depoimentoSchema).min(1).optional(),
  vibe: z.array(fotoSchema).min(1).optional(),
  destaques: z.array(destaqueSchema).max(2).optional(),
  /** Rótulos de seções futuras exibidos no nav sem link (roadmap do site). */
  navFuturo: z.array(z.string().min(1)).optional(),
});

export type ConfigCliente = z.infer<typeof configClienteSchema>;
export type Acomodacao = z.infer<typeof acomodacaoSchema>;
export type Foto = z.infer<typeof fotoSchema>;
export type Comodidade = z.infer<typeof comodidadeSchema>;
export type PontoRegiao = z.infer<typeof pontoRegiaoSchema>;
export type Depoimento = z.infer<typeof depoimentoSchema>;
export type Destaque = z.infer<typeof destaqueSchema>;
export type SimboloComodidade = (typeof simbolosComodidade)[number];
