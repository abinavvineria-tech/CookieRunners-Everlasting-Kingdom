/* ==========================================================================
   EVERLASTING HORIZON — Starfield particles
   A lightweight, mobile-friendly animated canvas background.
   Respects prefers-reduced-motion.
   ========================================================================== */
(function () {
  'use strict';

  var canvas = document.getElementById('starfield');
  if (!canvas) return;

  var ctx = canvas.getContext('2d');
  var particles = [];
  var width, height;
  var particleCount = 45;            // keep low for mobile performance
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var animationId;

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }

  function random(min, max) {
    return Math.random() * (max - min) + min;
  }

  function createParticle() {
    return {
      x: random(0, width),
      y: random(0, height),
      vx: random(-0.12, 0.12),
      vy: random(-0.12, 0.12),
      radius: random(0.5, 1.6),
      alpha: random(0.35, 0.9),
      alphaDir: random(0.003, 0.009),
      color: random() > 0.5 ? '#d4af37' : '#a78bfa', // gold or magical purple
    };
  }

  function initParticles() {
    particles = [];
    var count = reduced ? Math.floor(particleCount / 2) : particleCount;
    for (var i = 0; i < count; i++) {
      var p = createParticle();
      // scatter initial alpha so they don't all pulse together
      p.alpha = random(0.2, 1);
      particles.push(p);
    }
  }

  function draw() {
    if (reduced) {
      ctx.clearRect(0, 0, width, height);
      return;
    }
    ctx.clearRect(0, 0, width, height);

    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];
      p.x += p.vx;
      p.y += p.vy;

      // wrap around screen
      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      // gentle pulse
      p.alpha += p.alphaDir;
      if (p.alpha > 0.9) { p.alpha = 0.9; p.alphaDir = -Math.abs(p.alphaDir); }
      if (p.alpha < 0.25) { p.alpha = 0.25; p.alphaDir = Math.abs(p.alphaDir); }

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = p.alpha;
      ctx.fill();
      ctx.globalAlpha = 1;
    }

    animationId = requestAnimationFrame(draw);
  }

  window.addEventListener('resize', function () {
    resize();
    initParticles();
  });

  resize();
  initParticles();

  if (!reduced) {
    draw();
  }

  // Pause when tab is hidden to save battery on mobile
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) {
      cancelAnimationFrame(animationId);
    } else if (!reduced) {
      draw();
    }
  });
})();
