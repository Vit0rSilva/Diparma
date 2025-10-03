import { Carrinho } from "../componetes/carrinho/carrinho";
import { Endereco } from "./endereco.model";

export class Usuario{
    id?: number;
    nome?: string;
    email?: string;
    senha?: string;
    telefone?: string;
    cpf?: string;
    img?: string;
    token?: string;
    enderecos?: Endereco[];
    carrinho?: Carrinho[];
}