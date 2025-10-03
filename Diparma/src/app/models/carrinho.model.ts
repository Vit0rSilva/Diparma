import { Prato } from "./prato.model";
import { Bebidas } from "./bebidas.model";
import { Extra } from "./extra.model";
export interface ItemCarrinho {
    prato?: Prato;
    bebida?: Bebidas;
    extra?: Extra[];
    quantidade?: number;
    subtotal?: number;
}

export interface Carrinho{
    id:number;
    idUsuario:number;
    itens: ItemCarrinho[];
    total: number;
}