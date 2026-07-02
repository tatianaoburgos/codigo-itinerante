import { readFileSync } from 'node:fs';
import path from 'node:path';
import { configClienteSchema, type ConfigCliente } from './schema';

/** Slug do cliente ativo, definido pela variável de ambiente CLIENTE (padrão: demo). */
export const clienteAtivo: string = process.env.CLIENTE ?? 'demo';

/** Pasta do cliente ativo na raiz do monorepo (`clientes/<slug>/`). */
export const pastaCliente: string = path.resolve(process.cwd(), '..', 'clientes', clienteAtivo);

function carregarConfig(): ConfigCliente {
  const bruto = readFileSync(path.join(pastaCliente, 'config.json'), 'utf-8');
  return configClienteSchema.parse(JSON.parse(bruto));
}

/** Config validado do cliente ativo. Config inválido derruba a build com o erro do schema. */
export const config: ConfigCliente = carregarConfig();
