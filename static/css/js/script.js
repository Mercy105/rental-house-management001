// JavaScript for Hide-on-Scroll Navigation Bar
let lastScrollTop = 0;
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > lastScrollTop) {
        // Downscroll - hide the navbar
        navbar.style.top = '-80px'; // Adjust this value based on your navbar height
    } else {
        // Upscroll - show the navbar
        navbar.style.top = '0';
    }
    
    lastScrollTop = scrollTop;
});
