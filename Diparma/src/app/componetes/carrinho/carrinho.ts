import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import {CarrinhoService} from './service/carrinho';
import { Api } from '../../core/service/api';
import { Endereco } from '../../models/endereco.model';

@Component({
  selector: 'app-carrinho',
  imports: [],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  templateUrl: './carrinho.html',
  styleUrl: './carrinho.scss'
})
export class Carrinho {
  carrinhoAberto: boolean = false;
  enderecos: Endereco[] = [];
  enderecoTodosNullPrincipal: boolean = false;
  etapaCesta: 'cesta' | 'pagamento' | 'confirmacao' = 'cesta';
  etapaPagamento: 'cartao' | 'pix' | 'dinheiro' = 'cartao';

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

  //-------------Fluxo de etapas do carrinho

  //Fluxo de etapa pagamento
  irParaPagamento(){
    this.etapaCesta = 'pagamento';
  }

  caixaCupom: 'aberto' | 'fechado' = 'fechado';
  cupomDesconto(opcao: string){
    if(opcao === 'fechado'){
      this.caixaCupom = 'fechado';
    }else{
      this.caixaCupom = 'aberto';
    }
  }

  //Fluxo de etapa confirmação
  tempo:number = 0;
  private intervalo: any;
  
  confirmarPedido(){
    this.tempo = 10;
    this.etapaCesta = 'confirmacao';

    this.intervalo = setInterval(() => {
      if (this.tempo > 0) {
        this.tempo--;
      } else {
        clearInterval(this.intervalo);
        console.log('Tempo acabou!');
        this.etapaCesta = 'cesta';
      }
    }, 1000);
  }

  voltarParaCesta(){
    this.etapaCesta = 'cesta';

    this.etapaPagamento = 'cartao';
  }

  //Fluxo de etapa pagamento
  selecionarCartao(){
    this.etapaPagamento = 'cartao';
  }
  selecionarPix(){
    this.etapaPagamento = 'pix';
  }
  selecionarDinheiro(){
    this.etapaPagamento = 'dinheiro';
  }

}
