import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Prato } from '../../models/prato.model';
import { Usuario } from '../../models/usuario.model'; 
import { User } from './user'; 
import { Endereco } from '../../models/endereco.model';
import { Carrinho, CarrinhoItem, CarrinhoRequest } from '../../models/carrinho.model';

import { ApiResponse } from '../../models/response.model';


@Injectable({
  providedIn: 'root'
})
export class Api {
  private usuario: Usuario[]  = [];
  private endereco: Endereco[] = [];
  private carrinho: Carrinho[] = [];
  apiUrl: string = "http://127.0.0.1:8000/";

  constructor(private http: HttpClient, private user: User){}

  //Observable - ele fica obserrvando quando os dados da api chegar
  getPratos(): Observable<Prato[]> {
    return new Observable<Prato[]>((observer) => {
      this.http.get<any>(this.apiUrl + 'pratos').subscribe({
        next: (res) => {
          observer.next(res.data || []); // devolve só o array
          observer.complete();
        },
        error: (err) => observer.error(err)
      });
    });
  }

  getEnderecosUsuario(): Observable<ApiResponse<Endereco[]>> {
    return this.http.get<ApiResponse<Endereco[]>>(this.apiUrl + 'usuarios/me/enderecos');
  }
  //carrinho
  getCarrinhoUsuario(): Observable<ApiResponse<Carrinho>> {
    return this.http.get<ApiResponse<Carrinho>>(this.apiUrl + 'carrinho');
  }


  addToCart(body: CarrinhoRequest): Observable<any> {
    // POST direto para /carrinho/ (ajuste caminho se for diferente)
    return this.http.post<any>(this.apiUrl + 'carrinho/', body);
  }

  deletItemCarrinho(id: number): Observable<any> {
    return this.http.delete(this.apiUrl + 'carrinho/' + id)
  }

  /*salvar(categoria: Categoria) : Observable<Categoria>{
    return this.http.post<Categoria>(this.apiUrl, categoria);
  }*/

}
