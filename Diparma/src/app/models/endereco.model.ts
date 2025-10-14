export interface Endereco {
  id: number;
  usuario_id: string;
  rua: string;
  numero: string;
  bairro: string;
  cidade: string;
  complemento?: string;
  endereco_principal?: boolean;
  cep: string;
  lat?: string;
  lng?: string;
}
