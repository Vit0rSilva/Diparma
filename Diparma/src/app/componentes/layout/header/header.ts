import { Component } from '@angular/core';
import { CarrinhoComponente } from '../../carrinho/carrinho';
import {CarrinhoService} from '../../carrinho/service/carrinho';
import { Router } from '@angular/router'


@Component({
  selector: 'app-header',
  imports: [],
  templateUrl: './header.html',
  styleUrl: './header.scss'
})
export class Header {
  constructor(private carrinhoService: CarrinhoService, private router: Router) { }

  abrirCarrinho(){
    this.carrinhoService.abrirCarrinho();
  }

  irParaLogin() {
    this.router.navigate(['/login']);
  }

  navegarPara(rota: string) {
    this.router.navigate([rota]);
  }

  navegarParaPedidos() {
    this.router.navigate(['/pedidos']);
  }

  navegarParaRegistro() {
    this.router.navigate(['/registro']);
  }
}
