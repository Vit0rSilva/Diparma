import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CarrinhoService } from './service/carrinho';
import { Carrinho } from '../../models/carrinho.model';
import { Endereco } from '../../models/endereco.model';
import { Api } from '../../core/service/api';

@Component({
  selector: 'app-carrinho',
  imports: [],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  templateUrl: './carrinho.html',
  styleUrl: './carrinho.scss'
})
export class CarrinhoComponente {
  carrinho?: Carrinho;
  enderecos: Endereco[] = [];
  carrinhoAberto = false;
  carrinhoItens = false;
  totalComFrete = 8;
  enderecoTodosNullPrincipal: boolean = false;

  etapaCesta: 'cesta' | 'pagamento' | 'confirmacao' = 'cesta';
  etapaPagamento: 'cartao' | 'pix' | 'dinheiro' = 'cartao';

  constructor(private carrinhoService: CarrinhoService, private api: Api) {}

  ngOnInit() {
    // Escuta abertura
    this.carrinhoService.carrinhoAberto$.subscribe(status => {
      this.carrinhoAberto = status;
      document.body.style.overflow = status ? 'hidden' : 'auto';
    });

    // Escuta atualizações do carrinho
    this.carrinhoService.carrinho$.subscribe(carrinho => {
      this.carrinho = carrinho ?? { itens: [] } as Carrinho;
      this.carrinhoItens = !!carrinho && carrinho.itens.length > 0;
      this.totalComFrete = (carrinho?.total ?? 0) + 8;
    });

    // Carrega pela primeira vez
    this.carrinhoService.carregarCarrinho();

    // Endereços
    this.api.getEnderecosUsuario().subscribe({
      next: (enderecos) => this.enderecos = enderecos.data,
      error: (err) => console.error('Erro ao buscar endereços', err)
    });
  }

  excluirItens(id: number) {
    this.carrinhoService.excluirItem(id);
  }

  fecharCarrinho() {
    this.carrinhoService.fecharCarrinho();
  }

  caixaCupom: 'aberto' | 'fechado' = 'fechado';
  cupomDesconto(opcao: string){
    if(opcao === 'fechado'){
      this.caixaCupom = 'fechado';
    }else{
      this.caixaCupom = 'aberto';
    }
  }

  // etapas
  irParaPagamento() { this.etapaCesta = 'pagamento'; }
  voltarParaCesta() { this.etapaCesta = 'cesta'; this.etapaPagamento = 'cartao'; }
  selecionarCartao() { this.etapaPagamento = 'cartao'; }
  selecionarPix() { this.etapaPagamento = 'pix'; }
  selecionarDinheiro() { this.etapaPagamento = 'dinheiro'; }

  confirmarPedido() {
    this.etapaCesta = 'confirmacao';
    let tempo = 10;
    const timer = setInterval(() => {
      tempo--;
      if (tempo <= 0) {
        clearInterval(timer);
        this.etapaCesta = 'cesta';
      }
    }, 1000);
  }
}
