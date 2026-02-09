(function () {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', mobileNavToogle);
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function (e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });
  

  
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Init typed.js
   */
  const selectTyped = document.querySelector('.typed');
  if (selectTyped) {
    let typed_strings = selectTyped.getAttribute('data-typed-items');
    typed_strings = typed_strings.split(',');
    new Typed('.typed', {
      strings: typed_strings,
      loop: true,
      typeSpeed: 100,
      backSpeed: 50,
      backDelay: 2000
    });
  }

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function (swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Frequently Asked Questions Toggle
   */
  document.addEventListener('DOMContentLoaded', function () {
    const faqToggles = document.querySelectorAll('.faq-toggle');

    faqToggles.forEach(toggle => {
      toggle.addEventListener('click', function () {
        const parentItem = this.closest('.faq-item');

        // Close all other FAQs
        document.querySelectorAll('.faq-item').forEach(item => {
          if (item !== parentItem) {
            item.classList.remove('faq-active');
            item.querySelector('.faq-toggle').classList.remove('bi-plus');
            item.querySelector('.faq-toggle').classList.add('bi-plus');
          }
        });

        // Toggle the clicked FAQ
        parentItem.classList.toggle('faq-active');

        // Change icon
        this.classList.toggle('bi-plus');
        this.classList.toggle('bi-plus');
      });
    });
  });

  /**
   * Correct scrolling position upon page load for URLs containing hash links.
   */
  window.addEventListener('load', function (e) {
    if (window.location.hash) {
      if (document.querySelector(window.location.hash)) {
        setTimeout(() => {
          let section = document.querySelector(window.location.hash);
          let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
          window.scrollTo({
            top: section.offsetTop - parseInt(scrollMarginTop),
            behavior: 'smooth'
          });
        }, 100);
      }
    }
  });

  /**
   * Navmenu Scrollspy
   */
  let navmenulinks = document.querySelectorAll('.navmenu a');

  function navmenuScrollspy() {
    navmenulinks.forEach(navmenulink => {
      if (!navmenulink.hash) return;
      let section = document.querySelector(navmenulink.hash);
      if (!section) return;
      let position = window.scrollY + 200;
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        document.querySelectorAll('.navmenu a.active').forEach(link => link.classList.remove('active'));
        navmenulink.classList.add('active');
      } else {
        navmenulink.classList.remove('active');
      }
    })
  }
  window.addEventListener('load', navmenuScrollspy);
  document.addEventListener('scroll', navmenuScrollspy);

})();

// navbar js 



const hamburger = document.querySelector('.hamburger');
const mobileMenu = document.querySelector('.mobile-menu');
const overlay = document.querySelector('.overlay');
const closeBtn = document.querySelector('.close-btn');

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('active');
  mobileMenu.classList.toggle('active');
  overlay.classList.toggle('active');
});

closeBtn.addEventListener('click', () => {
  hamburger.classList.remove('active');
  mobileMenu.classList.remove('active');
  overlay.classList.remove('active');
});

overlay.addEventListener('click', () => {
  hamburger.classList.remove('active');
  mobileMenu.classList.remove('active');
  overlay.classList.remove('active');
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();

    hamburger.classList.remove('active');
    mobileMenu.classList.remove('active');
    overlay.classList.remove('active');

    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});


// Mobile dropdown toggle
document.querySelectorAll('.mobile-dropdown-toggle').forEach(toggle => {
  toggle.addEventListener('click', function (e) {
    e.preventDefault();
    const dropdown = this.parentElement;
    dropdown.classList.toggle('active');

    // Close other open dropdowns
    document.querySelectorAll('.mobile-dropdown').forEach(dd => {
      if (dd !== dropdown) {
        dd.classList.remove('active');
      }
    });
  });
});





// portfolio
document.addEventListener('DOMContentLoaded', function () {
  const filterButtons = document.querySelectorAll('.filter-button-group button');
  const portfolioItems = document.querySelectorAll('.bgd-portfolio-item');
  const moreItems = document.querySelectorAll('.more-items');
  const toggleButton = document.getElementById('toggleProjects');
  let showingAll = false;

  // Only show toggle button if there are hidden items
  if (moreItems.length === 0) {
    toggleButton.style.display = 'none';
  }

  // Filter functionality
  filterButtons.forEach(button => {
    button.addEventListener('click', function () {
      // Remove active class from all buttons
      filterButtons.forEach(btn => btn.classList.remove('active'));

      // Add active class to clicked button
      this.classList.add('active');

      const filterValue = this.getAttribute('data-filter');

      // Show/hide items based on filter
      portfolioItems.forEach(item => {
        if (filterValue === '*' || item.classList.contains(filterValue.substring(1))) {
          item.style.display = 'block';
        } else {
          item.style.display = 'none';
        }
      });

      // Reset the toggle button state when filtering
      showingAll = false;
      toggleButton.querySelector('.view-more-text').textContent = 'View More Projects';

      // Hide button if filtered results don't have more items
      const filteredMoreItems = document.querySelectorAll(`.more-items:not([style*="display: none"])`);
      toggleButton.style.display = filteredMoreItems.length > 0 ? 'inline-block' : 'none';
    });
  });

  // Toggle more/less projects
  toggleButton.addEventListener('click', function (e) {
    e.preventDefault();

    showingAll = !showingAll;

    if (showingAll) {
      moreItems.forEach(item => {
        item.style.display = 'block';
      });
      toggleButton.querySelector('.view-more-text').textContent = 'View Less Projects';
    } else {
      moreItems.forEach(item => {
        item.style.display = 'none';
      });
      toggleButton.querySelector('.view-more-text').textContent = 'View More Projects';
    }
  });
});


var Tawk_API = Tawk_API || {}, Tawk_LoadStart = new Date();

// Hide widget when it's ready
Tawk_API.onLoad = function () {
  Tawk_API.hideWidget();
};

// Hide widget as soon as chat opens
Tawk_API.onChatMaximized = function () {
  setTimeout(function () {
    Tawk_API.hideWidget(); // hide the floating icon again
  }, 100); // slight delay to ensure chat popup shows
};

// Hide widget after minimizing or ending
Tawk_API.onChatMinimized = function () {
  Tawk_API.hideWidget();
};
Tawk_API.onChatEnded = function () {
  Tawk_API.hideWidget();
};

(function () {
  var s1 = document.createElement("script"), s0 = document.getElementsByTagName("script")[0];
  s1.async = true;
  s1.src = 'https://embed.tawk.to/6874e5bce5777f190f9b0393/1j04a2r5d';
  s1.charset = 'UTF-8';
  s1.setAttribute('crossorigin', '*');
  s0.parentNode.insertBefore(s1, s0);
})();