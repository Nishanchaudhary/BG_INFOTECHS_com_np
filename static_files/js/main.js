// main.js - Completely clean version with NO navbar interference
(function () {
  "use strict";

  /**
   * Initialize AOS animations - Safe
   */
  function initAOS() {
    if (typeof AOS !== 'undefined') {
      AOS.init({
        duration: 600,
        easing: 'ease-in-out',
        once: true,
        mirror: false
      });
    }
  }

  /**
   * Initialize glightbox - Safe
   */
  function initGlightbox() {
    if (typeof GLightbox !== 'undefined') {
      const glightbox = GLightbox({
        selector: '.glightbox'
      });
    }
  }

  /**
   * Initialize Pure Counter - Safe
   */
  function initPureCounter() {
    if (typeof PureCounter !== 'undefined') {
      new PureCounter();
    }
  }

  /**
   * Initialize typed.js - Safe
   */
  function initTyped() {
    const selectTyped = document.querySelector('.typed');
    if (selectTyped && typeof Typed !== 'undefined') {
      let typed_strings = selectTyped.getAttribute('data-typed-items');
      if (typed_strings) {
        typed_strings = typed_strings.split(',');
        new Typed('.typed', {
          strings: typed_strings,
          loop: true,
          typeSpeed: 100,
          backSpeed: 50,
          backDelay: 2000
        });
      }
    }
  }

  /**
   * Initialize swiper sliders - Safe
   */
  function initSwipers() {
    if (typeof Swiper !== 'undefined') {
      document.querySelectorAll(".init-swiper").forEach(function (swiperElement) {
        // Only target swipers that are specifically marked for initialization
        if (swiperElement.classList.contains('init-swiper')) {
          let configElement = swiperElement.querySelector(".swiper-config");
          if (configElement) {
            try {
              let config = JSON.parse(configElement.innerHTML.trim());
              new Swiper(swiperElement, config);
            } catch (e) {
              console.log('Swiper config error:', e);
            }
          }
        }
      });
    }
  }

  /**
   * Initialize FAQ toggles - Safe (only for specific FAQ sections)
   */
  function initFAQs() {
    // Only target FAQ sections that are not in navigation
    const faqSections = document.querySelectorAll('.faq-section:not(header .faq-section):not(nav .faq-section):not(.mobile-menu .faq-section)');
    
    faqSections.forEach(section => {
      const faqToggles = section.querySelectorAll('.faq-toggle');
      
      faqToggles.forEach(toggle => {
        toggle.addEventListener('click', function (e) {
          e.preventDefault();
          e.stopPropagation();
          
          const parentItem = this.closest('.faq-item');
          if (!parentItem) return;
          
          // Close all other FAQs in this section only
          section.querySelectorAll('.faq-item').forEach(item => {
            if (item !== parentItem) {
              item.classList.remove('faq-active');
            }
          });
          
          // Toggle current FAQ
          parentItem.classList.toggle('faq-active');
        });
      });
    });
  }

  /**
   * Initialize portfolio filtering - Safe
   */
  function initPortfolio() {
    const portfolioSection = document.querySelector('#portfolio, .portfolio-section');
    if (!portfolioSection) return;

    const filterButtons = portfolioSection.querySelectorAll('.filter-button-group button');
    const portfolioItems = portfolioSection.querySelectorAll('.bgd-portfolio-item');
    const moreItems = portfolioSection.querySelectorAll('.more-items');
    const toggleButton = portfolioSection.querySelector('#toggleProjects');
    let showingAll = false;

    // Only show toggle button if there are hidden items
    if (moreItems.length === 0 && toggleButton) {
      toggleButton.style.display = 'none';
    }

    // Filter functionality
    filterButtons.forEach(button => {
      button.addEventListener('click', function (e) {
        e.stopPropagation();
        
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
        if (toggleButton) {
          toggleButton.querySelector('.view-more-text').textContent = 'View More Projects';
        }

        // Hide button if filtered results don't have more items
        const filteredMoreItems = portfolioSection.querySelectorAll(`.more-items:not([style*="display: none"])`);
        if (toggleButton) {
          toggleButton.style.display = filteredMoreItems.length > 0 ? 'inline-block' : 'none';
        }
      });
    });

    // Toggle more/less projects
    if (toggleButton) {
      toggleButton.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();

        showingAll = !showingAll;

        if (showingAll) {
          moreItems.forEach(item => {
            item.style.display = 'block';
          });
          this.querySelector('.view-more-text').textContent = 'View Less Projects';
        } else {
          moreItems.forEach(item => {
            item.style.display = 'none';
          });
          this.querySelector('.view-more-text').textContent = 'View More Projects';
        }
      });
    }
  }

  /**
   * Safe smooth scroll for hash links (explicitly excludes navigation)
   */
  function initSafeSmoothScroll() {
    // Only target hash links that are explicitly marked for smooth scroll
    document.querySelectorAll('a[href^="#"].smooth-scroll').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href && href !== '#') {
          const target = document.querySelector(href);
          if (target && !target.closest('header') && !target.closest('nav')) {
            e.preventDefault();
            const scrollMarginTop = getComputedStyle(target).scrollMarginTop || '0';
            window.scrollTo({
              top: target.offsetTop - parseInt(scrollMarginTop),
              behavior: 'smooth'
            });
          }
        }
      });
    });
  }

  /**
   * Safe scroll effect (only for body, no navbar interaction)
   */
  function initSafeScrollEffect() {
    window.addEventListener('scroll', function() {
      // Only add/remove scrolled class to body, no navbar manipulation
      if (window.scrollY > 100) {
        document.body.classList.add('scrolled');
      } else {
        document.body.classList.remove('scrolled');
      }
    });
  }

  /**
   * Initialize all safe components when DOM is ready
   */
  document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing safe components only...');
    
    // Initialize only safe components that don't touch navigation
    setTimeout(() => {
      initAOS();
      initGlightbox();
      initPureCounter();
      initTyped();
      initSwipers();
      initFAQs();
      initPortfolio();
      initSafeSmoothScroll();
      initSafeScrollEffect();
    }, 100);
  });

  /**
   * Final initialization after window load
   */
  window.addEventListener('load', function() {
    console.log('Page fully loaded - final safe initialization');
    // Re-run only safe initializations
    setTimeout(() => {
      initAOS();
      initSwipers();
    }, 200);
  });

})();