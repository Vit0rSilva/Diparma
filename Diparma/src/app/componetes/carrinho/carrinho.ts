import { Component } from '@angular/core';
import {CarrinhoService} from './service/carrinho';

@Component({
  selector: 'app-carrinho',
  imports: [],
  templateUrl: './carrinho.html',
  styleUrl: './carrinho.scss'
})
export class Carrinho {
  carrinhoAberto: boolean = false;

  constructor ( private carrinhoService: CarrinhoService) { }

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
  }

  fecharCarrinho() {
    this.carrinhoService.fecharCarrinho();
  }
}
