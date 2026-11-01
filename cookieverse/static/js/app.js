// Cookie Runners Golden Ballon d'Or — Interactive Ceremony

let confettiActive = false;
let soundEnabled = true;

function launchConfetti(count = 300) {
  for (let i = 0; i < count; i++) {
    const c = document.createElement('div');
    c.className = 'confetti';
    const colors = ['#c8a556', '#e6c970', '#f2e0b0', '#d4a8f7', '#a6d8f7', '#fff'];
    c.style.background = colors[Math.floor(Math.random() * colors.length)];
    c.style.left = Math.random() * 100 + 'vw';
    c.style.animationDuration = (2 + Math.random() * 3) + 's';
    c.style.animationDelay = (Math.random() * 2) + 's';
    c.style.width = (8 + Math.random() * 12) + 'px';
    c.style.height = (8 + Math.random() * 12) + 'px';
    document.body.appendChild(c);
    setTimeout(() => c.remove(), 6000);
  }
}

function toggleSound() {
  soundEnabled = !soundEnabled;
  const btn = document.getElementById('sound-toggle');
  if (btn) btn.textContent = soundEnabled ? 'Sound: On' : 'Sound: Off';
  if (!soundEnabled) {
    // Mute any audio elements
    document.querySelectorAll('audio').forEach(a => a.muted = true);
  } else {
    document.querySelectorAll('audio').forEach(a => a.muted = false);
  }
}

function startCeremony() {
  const stage = document.getElementById('ceremony-stage');
  if (!stage) return;
  stage.scrollIntoView({ behavior: 'smooth' });
  setTimeout(() => {
    launchConfetti(400);
    revealSequence();
  }, 500);
}

function revealSequence() {
  const reveals = [
    { msg: 'THE COOKIE RUNNERS GOLDEN BALLON D\'OR 2026', delay: 0 },
    { msg: 'OUR GOLDEN BALLON D\'OR CO-WINNERS', delay: 2000 },
    { msg: 'White Lily Cookie & Mogra Cookie', delay: 4500 },
    { msg: 'THE GOLDEN HEART AWARD', delay: 7000 },
    { msg: 'White Lily Cookie & Mogra Cookie', delay: 9500 },
    { msg: 'THE GOLDEN TEAMMATE AWARD', delay: 12000 },
    { msg: 'Pure Vanilla Cookie', delay: 14500 },
    { msg: 'THANK YOU, COOKIE RUNNERS!', delay: 17000 },
  ];
  reveals.forEach(r => {
    setTimeout(() => {
      const banner = document.createElement('div');
      banner.className = 'reveal-banner';
      banner.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:9999;background:rgba(6,6,6,0.92);border:2px solid var(--gold);border-radius:20px;padding:2.5rem 3rem;max-width:90vw;text-align:center;box-shadow:0 0 60px rgba(200,165,86,0.5);animation:fadeInUp 1s ease-out;';
      banner.innerHTML = '<h2 style="font-size:clamp(1.2rem,4vw,2.2rem);color:var(--gold-light);letter-spacing:0.1em;margin-bottom:0.5rem;">' + r.msg + '</h2>';
      document.body.appendChild(banner);
      launchConfetti(150);
      setTimeout(() => banner.remove(), 3500);
    }, r.delay);
  });
}

window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.btn-gold').forEach(btn => {
    btn.addEventListener('click', () => launchConfetti(200));
  });
});
