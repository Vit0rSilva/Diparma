import Swiper from 'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.mjs';

// init Swiper:
const swiper = new Swiper(
    '.swiper-carrosel', {
      slidesPerView: 2,       // Quantos slides aparecem por vez
    spaceBetween: 30,       // Espaço entre os slides
    initialSlide: 4,        // Começa no último slide (base 0, então 4 é o 5º slide)
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
      
    }
);

const swiperCarrosel = new Swiper('.swiper-carrosel-pratos', {
  slidesPerView: 1.4,
  spaceBetween: 30,
  grid:{
    rows:2,
    fill:"row",
  },

  // Responsividade
  breakpoints: {
    540: {
      slidesPerView: 2.2,
      grid: {
        rows: 2,
      },
    },
    780: {
      slidesPerView: 2.6,
      grid: {
        rows: 2,
      },
    },
    998: {
      slidesPerView: 3.5,
      grid: {
        rows: 2,
      },
    },
    1194: {
      slidesPerView: 4.6,
      grid: {
        rows: 2,
      },
    },
  },
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },

});