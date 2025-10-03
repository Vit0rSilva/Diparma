import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Prato } from '../../models/prato.model';
import { Usuario } from '../../models/usuario.model'; 
import { User } from './user'; 
import { Endereco } from '../../models/endereco.model';
import { Carrinho } from '../../models/carrinho.model';


@Injectable({
  providedIn: 'root'
})
export class Api {
  private usuario: Usuario[]  = [];
  private endereco: Endereco[] = [];
  private carrinho: Carrinho[] = [];
  apiUrl: string = "http://localhost:3001/";

  constructor(private http: HttpClient, private user: User){}

  //Observable - ele fica obserrvando quando os dados da api chegar
  getPratos(): Observable<Prato[]>{
    return this.http.get<Prato[]>(this.apiUrl + 'pratos');
  }

  getEnderecoUsuario(id: number): Observable<Endereco[]> {
    return new Observable<Endereco[]>((observer) => {
      this.user.getUsuarios(id).subscribe({
        next: (usuarios) => {
          if (usuarios.length === 0) {
            observer.next([]);
            observer.complete();
            return console.error('Nenhum usuário encontrado com o ID fornecido');
          }

          // Pega o primeiro usuário retornado
          const usuario = usuarios[0];

          // Aqui acessamos o array de endereços corretamente
          if (usuario.enderecos && usuario.enderecos.length > 0) {
            this.endereco = usuario.enderecos.map((endereco) => ({
              id: endereco.id,
              rua: endereco.rua,
              numero: endereco.numero,
              complemento: endereco.complemento,
              bairro: endereco.bairro,
              cidade: endereco.cidade,
              cep: endereco.cep,
              principal: endereco.principal
            }));

            observer.next(this.endereco);
          } else {
            observer.next([]); // Nenhum endereço
          }

          // Retorna os endereços
          observer.complete();
        },
        error: (err) => {
          console.error('Erro ao buscar usuário', err);
          observer.error(err);
        }
      });
    });
  }
  
  getCarrinhoUsuario(id: number): Observable<Carrinho[]> {
    return new Observable<Endereco[]>((observer) => {
      this.user.getUsuarios(id).subscribe({
        next: (usuarios) => {
          if (usuarios.length === 0) {
            observer.next([]);
            observer.complete();
            return console.error('Nenhum usuário encontrado com o ID fornecido');
          }

          // Pega o primeiro usuário retornado
          const usuario = usuarios[0];

          // Aqui acessamos o array de endereços corretamente
          if (usuario.carrinho && usuario.carrinho.length > 0) {
            this.carrinho = usuario.carrinho.map((carrinho) => ({
              id: carrinho.id,
              idUsuario: carrinho.idUsuario
              
            }));

            observer.next(this.endereco);
          } else {
            observer.next([]); // Nenhum endereço
          }

          // Retorna os endereços
          observer.complete();
        },
        error: (err) => {
          console.error('Erro ao buscar usuário', err);
          observer.error(err);
        }
      });
    });
  }

  /*salvar(categoria: Categoria) : Observable<Categoria>{
    return this.http.post<Categoria>(this.apiUrl, categoria);
  }*/

}
