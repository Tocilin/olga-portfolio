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
  // Pixel-mosaic reveal: elements marked [data-pixel] are covered by a mosaic made from
  // the image's own colours. When scrolled into view it churns briefly, then dissolves
  // away to reveal the real image. Plays once; skipped for reduced motion; no libraries.
  (function pixelReveal() {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var COLS = 36, CHURN = 450, DISSOLVE = 1000;

    document.querySelectorAll('[data-pixel]').forEach(function (host) {
      var img = host.querySelector('img');
      if (!img) return;
      var canvas = document.createElement('canvas');
      canvas.className = 'px-canvas';
      canvas.setAttribute('aria-hidden', 'true');
      host.appendChild(canvas);
      var ctx = canvas.getContext('2d');
      var st = null, done = false, started = false;

      function cleanup() { done = true; canvas.remove(); }

      function setup() {
        var r = host.getBoundingClientRect();
        if (!r.width || !r.height) return null;
        var dpr = 1;                // blocks are large, so 1x is plenty and keeps tall images light
        canvas.width = Math.round(r.width * dpr);
        canvas.height = Math.round(r.height * dpr);
        var rad = getComputedStyle(host).borderRadius;
        if (!parseFloat(rad)) rad = getComputedStyle(img).borderRadius;
        canvas.style.borderRadius = rad;
        var cell = r.width / COLS, rows = Math.ceil(r.height / cell);
        var colors = new Array(COLS * rows).fill(null);
        try {                       // sample the image's colours, one per cell
          var off = document.createElement('canvas');
          off.width = COLS; off.height = rows;
          var o = off.getContext('2d');
          o.imageSmoothingQuality = 'high';
          o.drawImage(img, 0, 0, COLS, rows);
          var d = o.getImageData(0, 0, COLS, rows).data;
          for (var i = 0; i < COLS * rows; i++) colors[i] = [d[i * 4], d[i * 4 + 1], d[i * 4 + 2]];
        } catch (e) { /* tainted/unavailable: fall back to neutral grey cells */ }
        var thresh = [];             // dissolve order: random, biased to sweep top-left → bottom-right
        for (var y = 0; y < rows; y++) for (var x = 0; x < COLS; x++)
          thresh.push(0.6 * Math.random() + 0.4 * (x + y) / (COLS + rows));
        return { dpr: dpr, cell: cell, rows: rows, colors: colors, thresh: thresh, w: r.width, h: r.height };
      }

      function draw(progress, churn) {
        var s = st;
        ctx.setTransform(s.dpr, 0, 0, s.dpr, 0, 0);
        ctx.clearRect(0, 0, s.w, s.h);
        for (var y = 0; y < s.rows; y++) for (var x = 0; x < COLS; x++) {
          var i = y * COLS + x;
          // cell alpha: stays 1 until its turn, then fades out over ~30% of the dissolve
          var a = progress <= 0 ? 1 : Math.max(0, Math.min(1, 1 - (progress * 1.35 - s.thresh[i]) / 0.3));
          if (a <= 0) continue;
          var c = s.colors[i] || [236, 236, 236];
          var k = churn ? 0.86 + Math.random() * 0.28 : 1;
          ctx.fillStyle = 'rgba(' + Math.min(255, c[0] * k | 0) + ',' + Math.min(255, c[1] * k | 0) + ',' + Math.min(255, c[2] * k | 0) + ',' + a + ')';
          ctx.fillRect(x * s.cell, y * s.cell, s.cell + 0.6, s.cell + 0.6);
        }
      }

      function ready(cb) {
        if (img.complete && img.naturalWidth) return cb();
        img.addEventListener('load', cb, { once: true });
        img.addEventListener('error', cleanup, { once: true });
        setTimeout(function () { if (!started && !done && !(img.complete && img.naturalWidth)) cleanup(); }, 6000);
      }

      function play() {
        if (started || done) return;
        started = true;
        ready(function () {
          st = setup();
          if (!st) return cleanup();
          var t0 = performance.now(), lastChurn = 0;
          (function frame(now) {
            if (done) return;
            var t = now - t0;
            if (t < CHURN) {
              if (now - lastChurn > 80) { draw(0, true); lastChurn = now; }
            } else {
              var p = (t - CHURN) / DISSOLVE;
              if (p >= 1) return cleanup();
              var e = 1 - Math.pow(1 - p, 2);          // ease-out
              draw(e, true);
            }
            requestAnimationFrame(frame);
          })(t0);
        });
      }

      // static mosaic cover until the element is visible, so the sharp image never flashes first
      ready(function () {
        if (started || done) return;
        var s0 = setup();
        if (s0) { st = s0; draw(0, false); }
      });

      if ('IntersectionObserver' in window) {
        var io2 = new IntersectionObserver(function (entries) {
          if (entries.some(function (en) { return en.isIntersecting; })) { io2.disconnect(); play(); }
        }, { threshold: 0, rootMargin: '0px 0px -15% 0px' });   // fire once the top edge is on screen (works for very tall images)
        io2.observe(host);
      } else { cleanup(); }
    });
  })();

})();
