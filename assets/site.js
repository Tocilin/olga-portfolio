// Olga Tochilin — tiny progressive enhancements (all optional; the site works without JS)
(function () {
  var header = document.querySelector('.site-header');

  // Header turns into a floating pill once you scroll past the top
  function onScroll() { header.classList.toggle('is-stuck', window.scrollY > 40); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Reveal-on-scroll
  var els = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        // small stagger for siblings that enter together
        var delay = (en.target.dataset.i || 0) * 70;
        en.target.style.transitionDelay = delay + 'ms';
        en.target.classList.add('in');
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (el) {
      var sibs = el.parentElement.querySelectorAll(':scope > [data-reveal]');
      el.dataset.i = Math.min(Array.prototype.indexOf.call(sibs, el), 4);
      io.observe(el);
    });
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }
})();
