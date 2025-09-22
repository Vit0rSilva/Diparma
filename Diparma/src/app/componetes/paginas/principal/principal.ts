import { Component, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Footer } from '../../layout/footer/footer';
import { Header } from '../../layout/header/header';

import Swiper from 'swiper';
import 'swiper/css';

@Component({
  selector: 'app-principal',
  standalone: true,
  imports: [Footer, Header,CommonModule],
  templateUrl: './principal.html',
  styleUrls: ['./principal.scss']
})
export class Principal implements AfterViewInit {

  numeros:number = 1;

  ngAfterViewInit() {
    const swiper = new Swiper('.swiper-carrosel', {
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
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
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
