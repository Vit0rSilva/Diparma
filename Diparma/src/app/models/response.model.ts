import { Endereco } from "./endereco.model";
import { Bebidas } from "./bebidas.model";
import { Extra } from "./extra.model";
import { Prato } from "./prato.model";

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}
