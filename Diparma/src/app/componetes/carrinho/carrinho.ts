import { Component } from '@angular/core';
import {CarrinhoService} from './service/carrinho';
import { Api } from '../../core/service/api';
import { Endereco } from '../../models/endereco.model';

@Component({
  selector: 'app-carrinho',
  imports: [],
  templateUrl: './carrinho.html',
  styleUrl: './carrinho.scss'
})
export class Carrinho {
  carrinhoAberto: boolean = false;
  enderecos: Endereco[] = [];
  enderecoTodosNullPrincipal: boolean = false;

  constructor ( private carrinhoService: CarrinhoService, private api: Api) { }

  ngOnInit() {
    this.carrinhoService.carrinhoAberto$.subscribe(status => {
      this.carrinhoAberto = status;

      if (this.carrinhoAberto) {
        document.body.style.overflow = 'hidden'; // Desabilita o scroll do body
      }
      else {
        document.body.style.overflow = 'auto'; // Habilita o scroll do body
      }
    });
    this.api.getEnderecoUsuario(1).subscribe({
      next: (enderecos) => {
        this.enderecos = enderecos;

        let contadorEnderecosNull: number = 0;
        this.enderecos.forEach(endereco => {
          endereco.principal === false || endereco.principal === null  ? contadorEnderecosNull++ : null;
        });

        if (contadorEnderecosNull === this.enderecos.length) {
          this.enderecoTodosNullPrincipal = true;
        }
      },
      error: (err) => {
        console.error('Erro ao buscar endereços do usuário', err);
      }
    });

  }



  fecharCarrinho() {
    this.carrinhoService.fecharCarrinho();
  }
}
