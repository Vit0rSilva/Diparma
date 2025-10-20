import { Component, AfterViewInit, ElementRef, ViewChild, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Footer } from '../../layout/footer/footer';
import { Header } from '../../layout/header/header';
import { CarrinhoComponente } from '../../carrinho/carrinho';

import { ProductModalComponent } from '../../product-modal/product-modal';

import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { Prato } from '../../../models/prato.model';
import { Api } from '../../../core/service/api';

import Swiper from 'swiper';
import { Grid, Pagination, Navigation } from 'swiper/modules';

Swiper.use([Grid, Pagination, Navigation]);

@Component({
  selector: 'app-principal',
  standalone: true,
  imports: [Footer, Header, CommonModule, CarrinhoComponente, ProductModalComponent, HttpClientModule, FormsModule],
  templateUrl: './principal.html',
  styleUrls: ['./principal.scss']
})
export class Principal implements OnInit {

  pratos: Prato[] = [];

  modalVisible = false;
  selectedPrato: Prato | null = null;
  sending = false;
  feedback = '';

  @ViewChild('boxButton') boxButton!: ElementRef<HTMLDivElement>;

  constructor(private api: Api) { }

  ngOnInit() {
    //Pegar todos os pratos
    this.api.getPratos().subscribe({
      next: (dados) => {
        this.pratos = dados;
        console.log(dados)
        setTimeout(() => this.initSwiper())
        
      },
      error: (err) => {
        console.error('Error ao buscar pratos', err);
      }
    });

  }
  abrirModal(prato: Prato) {
    this.selectedPrato = prato;
    this.modalVisible = true;
  }

  fecharModal() {
    this.modalVisible = false;
    this.selectedPrato = null;
    this.feedback = '';
  }

  onAddToCart(payload: { prato_id?: string; quantidade_prato: number }) {
    if (!payload.prato_id) return;
    this.sending = true;
    this.feedback = '';

    const body = {
      prato_id: payload.prato_id,
      bebida_id: null,
      extra_id: null,
      quantidade_prato: payload.quantidade_prato,
      quantidade_bebida: 0,
      quantidade_extra: 0
    };

    this.api.addToCart(body).subscribe({
      next: (res) => {
        this.sending = false;
        this.feedback = '✅ Item adicionado ao carrinho';
        // opcional: emitir evento global / atualizar service do carrinho
        setTimeout(() => this.fecharModal(), 900);
      },
      error: (err) => {
        console.error('Erro ao adicionar ao carrinho', err);
        this.sending = false;
        this.feedback = '⚠️ Erro ao adicionar ao carrinho';
      }
    });
  }

  private initSwiper() {

    const swiper = new Swiper('.swiper-carrosel', {
      modules: [Grid, Pagination, Navigation],
      slidesPerView: 1,
      spaceBetween: 30,
      initialSlide: 4,
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
    });

    const swiperCarroselPratos = new Swiper('.swiper-carrosel-pratos', {
      modules: [Grid, Pagination, Navigation],
      slidesPerView: 1.4,
      spaceBetween: 30,
      grid: {
        rows: 2,
        fill: 'row',
      },
      breakpoints: {
        540: { slidesPerView: 2.2, grid: { rows: 2 } },
        780: { slidesPerView: 2.6, grid: { rows: 2 } },
        998: { slidesPerView: 3.5, grid: { rows: 2 } },
        1194: { slidesPerView: 4.6, grid: { rows: 2 } },
      },
      pagination: { el: '.swiper-pagination', clickable: true },
      navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
    });

    const swiperComentario = new Swiper('.swiper-comentario', {
      slidesPerView: 1.5,
      spaceBetween: 20,
      centeredSlides: true,
      breakpoints: {
        0: { slidesPerView: 1.5 },
        420: { slidesPerView: 1.5 },
        768: { slidesPerView: 2.5 },
        992: { slidesPerView: 3.5 },
        1200: { slidesPerView: 3.5 },
      },
    });

    swiperComentario.on('slideNextTransitionStart', () => {
      // Só esconder se o usuário estiver no primeiro slide indo pro próximo
      if (swiperComentario.previousIndex === 0) {
        this.boxButton.nativeElement.classList.remove('show');
        this.boxButton.nativeElement.classList.add('hide');
      }
    });

    swiperComentario.on('slideChange', () => {
      // Quando voltar para o primeiro slide, mostrar novamente
      if (swiperComentario.activeIndex === 0) {
        this.boxButton.nativeElement.classList.remove('hide');
        this.boxButton.nativeElement.classList.add('show');
      }
    });


  }

}
