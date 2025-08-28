import Swiper from 'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.mjs';

// init Swiper:
const swiper = new Swiper(
    '.swiper', {
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
  
  slidesPerView: 4,
  spaceBetween: 30,
  grid:{
    rows:2,
    fill:"row",
  },

  // Responsividade
  breakpoints: {
    640: {
      slidesPerView: 2,
      grid: {
        rows: 2,
      },
    },
    768: {
      slidesPerView: 3,
      grid: {
        rows: 2,
      },
    },
    1024: {
      slidesPerView: 4,
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