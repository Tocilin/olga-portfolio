// Olga Tochilin — tiny progressive enhancements (all optional; the site works without JS)
(function () {
  var header = document.querySelector('.site-header');

  // Header turns into a floating pill once you scroll past the top
  function onScroll() { header.classList.toggle('is-stuck', window.scrollY > 40); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Images fade in only if they actually had to load. Already-loaded images, and ones that
  // come straight from the browser cache, simply appear. Text and cards never fade.
  document.querySelectorAll('.work-img img, .project figure img').forEach(function (img) {
    if (img.complete) return;                         // already loaded: leave it alone
    img.classList.add('img-pending');
    function show(instant) {
      if (instant) img.style.transition = 'none';
      img.classList.remove('img-pending');
      if (instant) { void img.offsetWidth; img.style.transition = ''; }
    }
    function fromCache() {                            // cached or near-instant: no need to fade
      try {
        var e = performance.getEntriesByName(img.currentSrc || img.src);
        e = e[e.length - 1];
        return !!e && (e.transferSize === 0 || e.duration < 80);
      } catch (err) { return false; }
    }
    img.addEventListener('load', function () { show(fromCache()); }, { once: true });
    img.addEventListener('error', function () { show(true); }, { once: true });
    if (img.complete) show(true);                     // finished between the check and the listener
  });

  // Interactive dot field: the dotted shapes on the "What I Do" cards become particles.
  // The cursor repels nearby dots (stronger when closer); springs with damping pull them
  // back home. Positions are read from the original SVG, so shape, size and spacing are
  // unchanged. Skipped for reduced motion (static SVG stays) and when JS is off.
  (function dotField() {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var PAD = 48;          // room around the shape so pushed dots are never clipped
    var RADIUS = 0.34;     // cursor influence radius, as a fraction of the shape width
    var REPEL = 1.15;      // repulsion strength (px / frame^2 at the cursor's centre)
    var SPRING = 0.06;     // pull back toward home
    var DAMP = 0.82;       // velocity kept per frame (lower = settles faster)
    var SWEEP = 0.10;      // how much cursor speed is passed on to nearby dots

    document.querySelectorAll('.what-card').forEach(function (card) {
      var svg = card.querySelector('svg.dots');
      var path = svg && svg.querySelector('path');
      if (!path) return;

      // read the dots (zero-length "M x y h0" segments) and their size from the SVG
      var pts = [], re = /M\s*([\d.]+)\s+([\d.]+)h0/g, m, d = path.getAttribute('d');
      while ((m = re.exec(d))) pts.push([+m[1], +m[2]]);
      if (!pts.length) return;
      var dotR = (parseFloat(path.getAttribute('stroke-width')) || 4) / 2;   // viewBox units
      var color = getComputedStyle(svg).color;

      var wrap = document.createElement('div');
      wrap.className = svg.getAttribute('class') + ' dots-field';
      var canvas = document.createElement('canvas');
      canvas.setAttribute('aria-hidden', 'true');
      wrap.appendChild(canvas);
      svg.replaceWith(wrap);
      var ctx = canvas.getContext('2d');

      var n = pts.length;
      var hx = new Float32Array(n), hy = new Float32Array(n);
      var x = new Float32Array(n), y = new Float32Array(n);
      var vx = new Float32Array(n), vy = new Float32Array(n);
      var scale = 1, r = 1, R = 80, dpr = 1, W = 0;
      var mx = 0, my = 0, cx = 0, cy = 0, pcx = 0, pcy = 0;
      var active = false, running = false, last = 0;

      function layout() {
        var w = wrap.clientWidth;
        if (!w || w === W) return;
        W = w; dpr = Math.min(window.devicePixelRatio || 1, 2);
        scale = w / 400; r = dotR * scale; R = w * RADIUS;
        var cw = w + PAD * 2, ch = w * 384 / 400 + PAD * 2;
        canvas.width = Math.round(cw * dpr); canvas.height = Math.round(ch * dpr);
        for (var i = 0; i < n; i++) {
          hx[i] = pts[i][0] * scale + PAD; hy[i] = pts[i][1] * scale + PAD;
          x[i] = hx[i]; y[i] = hy[i]; vx[i] = vy[i] = 0;
        }
        draw();
      }

      function draw() {
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.clearRect(0, 0, canvas.width / dpr, canvas.height / dpr);
        ctx.fillStyle = color;
        ctx.beginPath();
        for (var i = 0; i < n; i++) { ctx.moveTo(x[i] + r, y[i]); ctx.arc(x[i], y[i], r, 0, 6.2832); }
        ctx.fill();
      }

      function frame(now) {
        var dt = Math.min((now - last) / 16.667, 2.5); last = now;
        // smooth the cursor so forces change gradually; its speed drives the "sweep" push
        var sx = 0, sy = 0;
        if (active) {
          var k = Math.min(1, 0.4 * dt);
          cx += (mx - cx) * k; cy += (my - cy) * k;
          sx = (cx - pcx) / dt; sy = (cy - pcy) / dt;
          var sp = Math.hypot(sx, sy);
          if (sp > 24) { sx *= 24 / sp; sy *= 24 / sp; }     // cap the push from very fast flicks
          pcx = cx; pcy = cy;
        }
        var damp = Math.pow(DAMP, dt), energy = 0;
        for (var i = 0; i < n; i++) {
          var ax = (hx[i] - x[i]) * SPRING, ay = (hy[i] - y[i]) * SPRING;
          if (active) {
            var dx = x[i] - cx, dy = y[i] - cy, dist = Math.hypot(dx, dy);
            if (dist < R) {
              var tt = 1 - dist / R, f = REPEL * tt * tt;
              if (dist < 0.5) { dx = Math.random() - .5; dy = Math.random() - .5; dist = Math.hypot(dx, dy) || 1; }
              ax += dx / dist * f; ay += dy / dist * f;
              vx[i] += sx * SWEEP * tt * dt; vy[i] += sy * SWEEP * tt * dt;
            }
          }
          vx[i] = (vx[i] + ax * dt) * damp; vy[i] = (vy[i] + ay * dt) * damp;
          x[i] += vx[i] * dt; y[i] += vy[i] * dt;
          energy += Math.abs(x[i] - hx[i]) + Math.abs(y[i] - hy[i]) + Math.abs(vx[i]) + Math.abs(vy[i]);
        }
        draw();
        if (active || energy / n > 0.004) { requestAnimationFrame(frame); }
        else {                                   // settled: snap exactly home and stop
          for (var j = 0; j < n; j++) { x[j] = hx[j]; y[j] = hy[j]; vx[j] = vy[j] = 0; }
          draw(); running = false;
        }
      }
      function start() { if (!running) { running = true; last = performance.now(); requestAnimationFrame(frame); } }

      function track(e) {
        var b = canvas.getBoundingClientRect();
        mx = e.clientX - b.left; my = e.clientY - b.top;
        if (!active) { active = true; cx = pcx = mx; cy = pcy = my; }
        start();
      }
      card.addEventListener('pointermove', track);
      card.addEventListener('pointerenter', track);
      card.addEventListener('pointerleave', function () { active = false; start(); });
      card.addEventListener('pointercancel', function () { active = false; start(); });

      if ('ResizeObserver' in window) new ResizeObserver(layout).observe(wrap); else layout();
      layout();
    });
  })();

})();
