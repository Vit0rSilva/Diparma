// carrinho.service.ts
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Carrinho } from '../../../models/carrinho.model';
import { Api } from '../../../core/service/api';

@Injectable({ providedIn: 'root' })
export class CarrinhoService {
  private carrinhoSubject = new BehaviorSubject<Carrinho | null>(null);
  carrinho$ = this.carrinhoSubject.asObservable();

  carrinhoAberto$ = new BehaviorSubject<boolean>(false);

  constructor(private api: Api) {}

  abrirCarrinho() {
    this.carrinhoAberto$.next(true);
  }

  fecharCarrinho() {
    this.carrinhoAberto$.next(false);
  }

  /** 🔹 Carrega carrinho da API e emite nova versão */
  carregarCarrinho() {
    this.api.getCarrinhoUsuario().subscribe({
      next: (res) => {
        this.carrinhoSubject.next(res.data);
      },
      error: (err) => console.error('Erro ao carregar carrinho:', err),
    });
  }

  /** 🔹 Adiciona item e recarrega */
  adicionarItem(payload: { prato_id?: string; quantidade_prato: number }) {
    this.api.addToCart(payload).subscribe({
      next: () => this.carregarCarrinho(),
      error: (err) => console.error('Erro ao adicionar item:', err),
    });
  }

  /** 🔹 Exclui item e recarrega */
  excluirItem(id: number) {
    this.api.deletItemCarrinho(id).subscribe({
      next: () => this.carregarCarrinho(),
      error: (err) => console.error('Erro ao excluir item:', err),
    });
  }
}
