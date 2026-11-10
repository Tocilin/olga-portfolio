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
    var COLS = 120, CHURN = 450, DISSOLVE = 1000;

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

      // Mosaic is kept as a tiny COLS x rows image (one pixel per block) and scaled up with
      // nearest-neighbour smoothing off — one cheap drawImage per frame instead of thousands of fillRects.
      function setup() {
        var r = host.getBoundingClientRect();
        if (!r.width || !r.height) return null;
        if (st && st.w === r.width && st.h === r.height) return st;   // reuse sampling + dissolve order
        canvas.width = Math.round(r.width);
        canvas.height = Math.round(r.height);
        var rad = getComputedStyle(host).borderRadius;
        if (!parseFloat(rad)) rad = getComputedStyle(img).borderRadius;
        canvas.style.borderRadius = rad;
        var cell = r.width / COLS, rows = Math.ceil(r.height / cell), n = COLS * rows;
        var base = new Uint8ClampedArray(n * 3).fill(236);          // neutral grey fallback
        try {                                                        // sample the image's colours
          var off = document.createElement('canvas');
          off.width = COLS; off.height = rows;
          var o = off.getContext('2d');
          o.imageSmoothingQuality = 'high';
          o.drawImage(img, 0, 0, COLS, rows);
          var d = o.getImageData(0, 0, COLS, rows).data;
          for (var i = 0; i < n; i++) { base[i * 3] = d[i * 4]; base[i * 3 + 1] = d[i * 4 + 1]; base[i * 3 + 2] = d[i * 4 + 2]; }
        } catch (e) { /* unavailable: keep grey */ }
        var thresh = new Float32Array(n);   // dissolve order: random, biased to sweep top-left -> bottom-right
        for (var y = 0; y < rows; y++) for (var x = 0; x < COLS; x++)
          thresh[y * COLS + x] = 0.6 * Math.random() + 0.4 * (x + y) / (COLS + rows);
        var small = document.createElement('canvas');
        small.width = COLS; small.height = rows;
        var sctx = small.getContext('2d');
        return { cell: cell, rows: rows, n: n, base: base, thresh: thresh,
                 small: small, sctx: sctx, data: sctx.createImageData(COLS, rows), w: r.width, h: r.height };
      }

      function draw(progress, churn) {
        var s = st, data = s.data.data, base = s.base, th = s.thresh;
        for (var i = 0; i < s.n; i++) {
          // alpha: 1 until the block's turn, then fades out over ~30% of the dissolve
          var a = progress <= 0 ? 1 : 1 - (progress * 1.35 - th[i]) / 0.3;
          a = a < 0 ? 0 : a > 1 ? 1 : a;
          var k = churn ? 0.86 + Math.random() * 0.28 : 1, j = i * 4;
          data[j] = base[i * 3] * k; data[j + 1] = base[i * 3 + 1] * k; data[j + 2] = base[i * 3 + 2] * k;
          data[j + 3] = a * 255;
        }
        s.sctx.putImageData(s.data, 0, 0);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.imageSmoothingEnabled = false;
        ctx.drawImage(s.small, 0, 0, COLS, s.rows, 0, 0, COLS * s.cell, s.rows * s.cell);
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
