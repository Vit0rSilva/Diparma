import { Carrinho } from "./carrinho.model";
import { Endereco } from "./endereco.model";

export class Usuario{
    id?: number;
    nome?: string;
    email?: string;
    senha?: string;
    telefone?: string;
    cpf?: string;
    img?: string;
    enderecos?: Endereco[];
    carrinho?: Carrinho[];
}

export interface UsuarioCreate {
  nome: string;
  cpf: string;
  email: string;
  telefone: string;
  senha: string;
}

export interface UsuarioResponse {
  id: number;
  nome: string;
  email: string;
  // demais campos que sua API retorna...
}

export interface EnderecoCreate {
  rua: string;
  numero: string;
  bairro: string;
  cidade: string;
  complemento?: string;
  endereco_principal: boolean;
  cep: string;
  lat?: string;
  lng?: string;
  usuario_id?: number; // será setado no frontend após criar usuário
}
