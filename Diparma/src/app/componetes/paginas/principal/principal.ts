import { Component, AfterViewInit, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Footer } from '../../layout/footer/footer';
import { Header } from '../../layout/header/header';
import { Carrinho } from '../../carrinho/carrinho';

import { Prato } from '../../../models/prato.model';
import { Api } from '../../../core/service/api';

import Swiper from 'swiper';
import { Grid, Pagination, Navigation } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/grid';
import 'swiper/css/pagination';
import 'swiper/css/navigation';

Swiper.use([Grid, Pagination, Navigation]);

@Component({
  selector: 'app-principal',
  standalone: true,
  imports: [Footer, Header,CommonModule,Carrinho],
  templateUrl: './principal.html',
  styleUrls: ['./principal.scss']
})
export class Principal implements OnInit {

  pratos: Prato[] = [];

  constructor(private api: Api){}

  ngOnInit(){
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

  private initSwiper(){

    const swiper = new Swiper('.swiper-carrosel', {
      modules: [Grid, Pagination, Navigation],
      slidesPerView: 2,
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
  }

}
