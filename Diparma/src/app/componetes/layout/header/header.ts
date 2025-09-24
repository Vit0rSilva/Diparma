import { Component } from '@angular/core';
import { Carrinho } from '../../carrinho/carrinho';
import {CarrinhoService} from '../../carrinho/service/carrinho';

@Component({
  selector: 'app-header',
  imports: [],
  templateUrl: './header.html',
  styleUrl: './header.scss'
})
export class Header {
  constructor(private carrinhoService: CarrinhoService) { }

  abrirCarrinho(){
    this.carrinhoService.abrirCarrinho();
  }
}
