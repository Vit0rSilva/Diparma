import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormControl } from '@angular/forms';
import { Prato } from '../../models/prato.model';
import { CarrinhoService } from '../carrinho/service/carrinho';

@Component({
  selector: 'app-product-modal',
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './product-modal.html',
  styleUrls: ['./product-modal.scss']
})
export class ProductModalComponent {
  @Input() visible = false;
  @Input() prato?: Prato | null;

  @Output() close = new EventEmitter<void>();

  quantidade = new FormControl<number>(1);

  constructor(private carrinhoService: CarrinhoService) {}

  incrementar() {
    const v = this.quantidade.value ?? 1;
    this.quantidade.setValue(v + 1);
  }

  decrementar() {
    const v = this.quantidade.value ?? 1;
    if (v > 1) this.quantidade.setValue(v - 1);
  }

  onAdd() {
    if (!this.prato) return;
    const q = this.quantidade.value ?? 1;
    this.carrinhoService.adicionarItem({ prato_id: this.prato.id, quantidade_prato: q });
    this.close.emit();
    this.carrinhoService.abrirCarrinho(); // abre automaticamente
  }

  onClose() {
    this.close.emit();
  }
}
