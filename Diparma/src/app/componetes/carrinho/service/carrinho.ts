import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CarrinhoService {
  private carrinhoAbertoSource = new BehaviorSubject<boolean>(false);
  carrinhoAberto$ = this.carrinhoAbertoSource.asObservable();

  abrirCarrinho(){
    this.carrinhoAbertoSource.next(true);
    
  }

  fecharCarrinho(){
    this.carrinhoAbertoSource.next(false);
  }
}
