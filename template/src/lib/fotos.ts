import type { ImageMetadata } from 'astro';
import { clienteAtivo, config } from './cliente';

const modulos = import.meta.glob<{ default: ImageMetadata }>(
  '../../../clientes/*/fotos/*.{jpg,jpeg,png,webp,avif}',
  { eager: true },
);

/** Fotos do cliente ativo, indexadas pelo nome do arquivo dentro de `fotos/`. */
const fotosDoCliente = new Map<string, ImageMetadata>(
  Object.entries(modulos)
    .filter(([caminho]) => caminho.includes(`/clientes/${clienteAtivo}/fotos/`))
    .map(([caminho, modulo]) => [caminho.split('/').pop()!, modulo.default]),
);

/** Resolve um nome de arquivo do config.json para os metadados usados pelo `astro:assets`. */
export function foto(arquivo: string): ImageMetadata {
  const meta = fotosDoCliente.get(arquivo);
  if (!meta) {
    throw new Error(`Foto "${arquivo}" nao encontrada em clientes/${clienteAtivo}/fotos/`);
  }
  return meta;
}

const modulosMarca = import.meta.glob<{ default: ImageMetadata }>(
  '../../../clientes/*/marca/*.{svg,png}',
  { eager: true },
);

const marcaDoCliente = new Map<string, ImageMetadata>(
  Object.entries(modulosMarca)
    .filter(([caminho]) => caminho.includes(`/clientes/${clienteAtivo}/marca/`))
    .map(([caminho, modulo]) => [caminho.split('/').pop()!, modulo.default]),
);

/** Resolve um arquivo de `marca/` do cliente ativo (logo, favicon). */
export function marca(arquivo: string): ImageMetadata {
  const meta = marcaDoCliente.get(arquivo);
  if (!meta) {
    throw new Error(`Arquivo de marca "${arquivo}" nao encontrado em clientes/${clienteAtivo}/marca/`);
  }
  return meta;
}

/** Símbolo da marca do cliente (divisor de seção e marca-d'água), se houver. */
export function simboloMarca(): ImageMetadata | undefined {
  return config.marca?.simbolo ? marca(config.marca.simbolo) : undefined;
}
