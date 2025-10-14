import { Prato } from "./prato.model";
import { Bebidas } from "./bebidas.model";
import { Extra } from "./extra.model";

export interface CarrinhoItem {
  id: number;
  prato?: Prato;
  bebida?: Bebidas;
  extra?: Extra;
  quantidade_prato: number;
  quantidade_bebida: number;
  quantidade_extra: number;
  preco_unitario: number;
  subtotal: number;
  criado_em: string;       // datetime → string
  atualizado_em: string;
}

export interface Carrinho {
  id?: string;
  usuario_id?: string;
  status?: string;
  itens: CarrinhoItem[];
  total?: number;
  total_itens?: number;
  criado_em?: string;
}

export interface CarrinhoRequest {
  prato_id?: string | null;
  bebida_id?: string | null;
  extra_id?: string | null;
  quantidade_prato?: number;
  quantidade_bebida?: number;
  quantidade_extra?: number;
}