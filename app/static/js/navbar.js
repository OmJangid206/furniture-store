/*
  navbar.js - Toggles the navigation bar's collapsed state.
  This script handles the functionality to expand and collapse the navigation bar
  on mobile devices using a toggle button.
*/

// Select the navbar toggle button, close button, and collapse element.
const navbarToggler = document.querySelector('.navbar-toggler-button');
const navbarCloseBtn = document.querySelector('.navbar-toggler-button.close');
const navbarCollapse = document.querySelector('.navbar-collapse');

// Event listener for the toggle button click.
navbarToggler.addEventListener('click', () => {
    // Toggle the 'collapsed' class on the collapse element.
    navbarCollapse.classList.toggle('collapsed');
    // Toggle the 'close' class on the toggle button.
    navbarToggler.classList.toggle('close');
});

// Event listener for the close button click.
navbarCloseBtn.addEventListener('click', () => {
    // Toggle the 'collapsed' class on the collapse element.
    navbarCollapse.classList.toggle('collapsed');
    // Toggle the 'close' class on the toggle button.
    navbarToggler.classList.toggle('close');
});
