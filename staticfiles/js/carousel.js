/*
  carousel.js - Implements a custom image carousel (slider).
  This script provides functionality for automatic and manual navigation
  between slides using plain JavaScript.
*/

document.addEventListener('DOMContentLoaded', function () {
    const carousel = document.querySelector('.carousel');
    const prevBtn = document.querySelector('.carousel-control-prev');
    const nextBtn = document.querySelector('.carousel-control-next');
    const slides = document.querySelectorAll('.carousel-item');
    let currentIndex = 0;

        // Function to show the current slide by adding 'active' class.
        function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.remove('active');
            if (i === index) {
                slide.classList.add('active');
            }
        });
    }

    // Event listener for the previous button click.
    prevBtn.addEventListener('click', function () {
        currentIndex = (currentIndex === 0) ? slides.length - 1 : currentIndex - 1;
        showSlide(currentIndex);
    });

    // Event listener for the next button click.
    nextBtn.addEventListener('click', function () {
        currentIndex = (currentIndex === slides.length - 1) ? 0 : currentIndex + 1;
        showSlide(currentIndex);
    });

    // Automatically advance to the next slide every 4 seconds.
    setInterval(function () {
        currentIndex = (currentIndex === slides.length - 1) ? 0 : currentIndex + 1;
        showSlide(currentIndex);
    }, 4000);
});
