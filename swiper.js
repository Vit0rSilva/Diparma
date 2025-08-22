import Swiper from 'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.mjs';

// init Swiper:
const swiper = new Swiper(
    '.swiper', {
      slidesPerView: 3,       // Quantos slides aparecem por vez
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