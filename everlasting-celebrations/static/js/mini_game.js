// CookieVerse: Jelly Rush Mini Game — canvas, touch & keyboard, high score via localStorage
(function () {
  'use strict';

  const canvas = document.getElementById('game-canvas');
  const ctx = canvas && canvas.getContext('2d');
  const scoreEl = document.getElementById('game-score');
  const bestEl = document.getElementById('game-best');
  const startBtn = document.getElementById('game-start');
  const pauseBtn = document.getElementById('game-pause');
  const restartBtn = document.getElementById('game-restart');
  const jumpBtn = document.getElementById('touch-jump');
  const slideBtn = document.getElementById('touch-slide');
  const victory = document.getElementById('victory-message');

  if (!canvas || !ctx) return;

  const GRAVITY = 0.6;
  const SPEED = 4;
  const JUMP_FORCE = -13;
  const WIN_SCORE = 50;

  function resize() {
    canvas.width = canvas.parentElement.clientWidth || 480;
    canvas.height = canvas.parentElement.clientHeight || 270;
  }
  resize();
  window.addEventListener('resize', resize);

  let active = false;
  let paused = false;
  let score = 0;
  let best = parseInt(localStorage.getItem('cv-jelly-best') || '0', 10);
  if (bestEl) bestEl.textContent = best;

  const player = {
    x: 60,
    y: 0,
    w: 34,
    h: 34,
    vy: 0,
    grounded: false,
    sliding: false,
    groundY: 0
  };

  const obstacles = [];
  const jellies = [];
  let frame = 0;
  let spawnTimer = 0;
  let spawnInterval = 90;
  let animId = null;

  const keys = {};
  window.addEventListener('keydown', function (e) {
    keys[e.code] = true;
    if (e.code === 'Space') {
      e.preventDefault();
      if (active && !paused) jump();
    }
    if (e.code === 'ArrowDown') {
      if (active && !paused) startSlide();
    }
  });
  window.addEventListener('keyup', function (e) {
    if (e.code === 'ArrowDown') endSlide();
  });

  if (startBtn) startBtn.addEventListener('click', startGame);
  if (pauseBtn) pauseBtn.addEventListener('click', function () {
    paused = !paused;
    pauseBtn.textContent = paused ? 'Resume' : 'Pause';
  });
  if (restartBtn) restartBtn.addEventListener('click', startGame);
  if (jumpBtn) jumpBtn.addEventListener('touchstart', function (e) {
    e.preventDefault();
    if (active && !paused) jump();
  });
  if (slideBtn) {
    slideBtn.addEventListener('touchstart', function (e) {
      e.preventDefault();
      if (active && !paused) startSlide();
    });
    slideBtn.addEventListener('touchend', endSlide);
  }

  function jump() {
    if (player.grounded && !player.sliding) {
      player.vy = JUMP_FORCE;
      player.grounded = false;
    }
  }

  function startSlide() {
    if (!player.sliding && player.grounded) {
      player.sliding = true;
      player.h = 20;
      player.y = player.groundY - player.h;
    }
  }

  function endSlide() {
    if (player.sliding) {
      player.sliding = false;
      player.h = 34;
      player.y = player.groundY - player.h;
    }
  }

  function startGame() {
    active = true;
    paused = false;
    score = 0;
    if (scoreEl) scoreEl.textContent = '0';
    if (victory) victory.style.display = 'none';
    player.x = 60;
    player.y = canvas.height - 90;
    player.vy = 0;
    player.grounded = true;
    player.sliding = false;
    player.h = 34;
    player.groundY = canvas.height - 50;
    obstacles.length = 0;
    jellies.length = 0;
    frame = 0;
    spawnTimer = 0;
    spawnInterval = 90;
    canvas.focus();
    if (!animId) loop();
  }

  function spawn() {
    const roll = Math.random();
    const size = 24 + Math.random() * 18;
    const groundY = canvas.height - 50;
    const item = {
      x: canvas.width + 40,
      y: groundY - size,
      w: size,
      h: size,
      type: roll > 0.72 ? 'jelly' : 'crumb'
    };
    if (item.type === 'jelly') jellies.push(item);
    else obstacles.push(item);
  }

  function loop() {
    if (!active) {
      animId = null;
      return;
    }
    if (!paused) {
      update();
    }
    draw();
    animId = requestAnimationFrame(loop);
  }

  function update() {
    frame++;
    spawnTimer++;
    if (spawnTimer >= spawnInterval) {
      spawn();
      spawnTimer = 0;
      spawnInterval = Math.max(55, 90 - Math.floor(score / 5) * 4);
    }

    player.vy += GRAVITY;
    player.y += player.vy;
    if (player.y > player.groundY - player.h) {
      player.y = player.groundY - player.h;
      player.vy = 0;
      player.grounded = true;
    }

    obstacles.forEach(function (o) { o.x -= SPEED; });
    jellies.forEach(function (j) { j.x -= SPEED; });

    while (obstacles.length && obstacles[0].x + obstacles[0].w < 0) obstacles.shift();
    while (jellies.length && jellies[0].x + jellies[0].w < 0) jellies.shift();

    obstacles.forEach(function (o) {
      if (rectIntersect(player, o)) {
        gameOver();
      }
    });

    jellies.forEach(function (j, idx) {
      if (rectIntersect(player, j)) {
        score += 10;
        if (scoreEl) scoreEl.textContent = String(score);
        jellies.splice(idx, 1);
        if (score >= WIN_SCORE) {
          winGame();
        }
      }
    });
  }

  function rectIntersect(a, b) {
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
    grad.addColorStop(0, '#b3e5fc');
    grad.addColorStop(1, '#81d4fa');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#8bc34a';
    ctx.fillRect(0, canvas.height - 50, canvas.width, 50);

    ctx.fillStyle = '#ffeb3b';
    ctx.beginPath();
    ctx.arc(player.x + player.w / 2, player.y + player.h / 2, player.w / 2, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#3e2723';
    ctx.beginPath();
    ctx.arc(player.x + player.w / 2 - 6, player.y + player.h / 2 - 5, 3, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(player.x + player.w / 2 + 6, player.y + player.h / 2 - 5, 3, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#8d6e63';
    obstacles.forEach(function (o) {
      ctx.beginPath();
      ctx.moveTo(o.x + o.w / 2, o.y);
      ctx.lineTo(o.x, o.y + o.h);
      ctx.lineTo(o.x + o.w, o.y + o.h);
      ctx.closePath();
      ctx.fill();
    });

    ctx.fillStyle = '#ffee93';
    jellies.forEach(function (j) {
      ctx.beginPath();
      ctx.ellipse(j.x + j.w / 2, j.y + j.h / 2, j.w / 2, j.h / 2, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#ffd60a';
      ctx.lineWidth = 2;
      ctx.stroke();
    });
  }

  function gameOver() {
    active = false;
    cancelAnimationFrame(animId);
    if (score > best) {
      best = score;
      localStorage.setItem('cv-jelly-best', String(best));
      if (bestEl) bestEl.textContent = String(best);
    }
    alert('Game Over! Jellies collected: ' + score);
  }

  function winGame() {
    active = false;
    cancelAnimationFrame(animId);
    if (victory) victory.style.display = 'block';
    if (score > best) {
      best = score;
      localStorage.setItem('cv-jelly-best', String(best));
      if (bestEl) bestEl.textContent = String(best);
    }
  }

})();
