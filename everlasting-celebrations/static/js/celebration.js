// CookieVerse: Celebration activation + confetti + sparkles
(function () {
  'use strict';

  const celebrateBtn = document.getElementById('celebrate-btn');
  const confettiBtn = document.getElementById('confetti-btn');
  const successPanel = document.getElementById('celebration-success');
  const celebrationMessage = document.getElementById('celebration-message');
  const sparklesContainer = document.getElementById('sparkles');
  const reducedMotion = document.documentElement.getAttribute('data-reduced-motion') === 'true' ||
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- Sparkle particles on hero ----
  function createSparks(count) {
    if (reducedMotion || !sparklesContainer) return;
    for (let i = 0; i < count; i++) {
      const spark = document.createElement('div');
      spark.className = 'sparkle';
      const left = Math.random() * 100;
      const top = Math.random() * 100;
      const size = 4 + Math.random() * 6;
      const delay = Math.random() * 4;
      const dur = 2 + Math.random() * 3;
      spark.style.left = left + '%';
      spark.style.top = top + '%';
      spark.style.width = size + 'px';
      spark.style.height = size + 'px';
      spark.style.opacity = 0.4 + Math.random() * 0.6;
      spark.style.animationDelay = delay + 's';
      spark.style.animationDuration = dur + 's';
      sparklesContainer.appendChild(spark);
    }
  }
  createSparks(24);

  // ---- Confetti cannon ----
  function launchConfetti() {
    const canvas = document.createElement('canvas');
    canvas.className = 'confetti';
    document.body.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    const pieces = [];
    const colors = ['#ffd60a', '#ff6b6b', '#ffee93', '#6bcf72', '#4fc3f7', '#a29bfe', '#ff7675'];

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    for (let i = 0; i < 120; i++) {
      pieces.push({
        x: window.innerWidth / 2,
        y: window.innerHeight / 2,
        w: 6 + Math.random() * 10,
        h: 6 + Math.random() * 10,
        vx: (Math.random() - 0.5) * 18,
        vy: (Math.random() - 0.5) * 18 - 12,
        gravity: 0.5,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotate: Math.random() * 360,
        vrot: (Math.random() - 0.5) * 20,
        alpha: 1
      });
    }

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      let alive = 0;
      pieces.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += p.gravity;
        p.rotate += p.vrot;
        p.alpha -= 0.015;
        if (p.alpha > 0) {
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate(p.rotate * Math.PI / 180);
          ctx.globalAlpha = p.alpha;
          ctx.fillStyle = p.color;
          ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
          ctx.restore();
          alive++;
        }
      });
      if (alive > 0) {
        requestAnimationFrame(animate);
      } else {
        document.body.removeChild(canvas);
      }
    }
    animate();
  }

  // ---- Celebration activation ----
  if (celebrateBtn && successPanel) {
    celebrateBtn.addEventListener('click', function () {
      const already = successPanel.classList.contains('celebration-success--visible');
      if (!already) {
        successPanel.classList.add('celebration-success--visible');
        successPanel.style.display = 'block';
        launchConfetti();
        if (celebrationMessage) {
          celebrationMessage.textContent = 'Joy unlocked — thank you for celebrating with us! &#127873;';
        }
        celebrateBtn.textContent = 'Celebration Active! &#127881;';
        celebrateBtn.classList.add('btn--jelly');
        celebrateBtn.classList.remove('btn--primary');
      }
    });
  }

  if (confettiBtn) {
    confettiBtn.addEventListener('click', launchConfetti);
  }

})();
