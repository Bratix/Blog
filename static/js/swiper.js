$(document).ready(function () {
  var mySwiper = new Swiper ('.swiper-container', {
    // Optional parameters
    direction: 'horizontal',
    loop: false,

    scrollbar: {
      el: '.swiper-scrollbar',
      draggable: true,
    },

    autoplay: {
      delay: 5000,
    },
    
  })
  mySwiper.autoplay.start();
});