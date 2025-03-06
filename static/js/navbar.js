const navbarToggler = document.querySelector('.navbar-toggler-button');
const navbarCloseBtn = document.querySelector('.navbar-toggler-button.close');
const navbarCollapse = document.querySelector('.navbar-collapse');

navbarToggler.addEventListener('click', () => {
    navbarCollapse.classList.toggle('collapsed');
    navbarToggler.classList.toggle('close');
});

navbarCloseBtn.addEventListener('click', () => {
    navbarCollapse.classList.toggle('collapsed');
    navbarToggler.classList.toggle('close');
});
