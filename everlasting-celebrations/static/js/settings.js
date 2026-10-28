// CookieVerse: Settings — theme, reduced motion, sound
(function () {
  'use strict';

  const form = document.getElementById('save-settings-btn');
  const msg = document.getElementById('settings-msg');
  const htmlEl = document.documentElement;
  const reducedInput = document.getElementById('reduced-motion');
  const soundInput = document.getElementById('sound-enabled');

  const swatchLight = document.getElementById('swatch-light');
  const swatchDark = document.getElementById('swatch-dark');

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function setTheme(theme) {
    htmlEl.setAttribute('data-theme', theme);
    localStorage.setItem('cv-theme', theme);
    if (swatchLight) swatchLight.classList.toggle('swatch--active', theme === 'light');
    if (swatchDark) swatchDark.classList.toggle('swatch--active', theme === 'dark');
    if (swatchLight) swatchLight.setAttribute('aria-pressed', theme === 'light');
    if (swatchDark) swatchDark.setAttribute('aria-pressed', theme === 'dark');
  }

  // Theme swatch clicks
  if (swatchLight) {
    swatchLight.addEventListener('click', function () { setTheme('light'); });
  }
  if (swatchDark) {
    swatchDark.addEventListener('click', function () { setTheme('dark'); });
  }

  // Apply reduced motion class if enabled
  function applyReducedMotion(enabled) {
    if (enabled) {
      htmlEl.setAttribute('data-reduced-motion', 'true');
    } else {
      htmlEl.removeAttribute('data-reduced-motion');
    }
  }

  if (form && msg) {
    form.addEventListener('click', async function (e) {
      e.preventDefault();
      const payload = {
        theme: htmlEl.getAttribute('data-theme') || 'light',
        reduced_motion: reducedInput ? (reducedInput.checked ? 'true' : 'false') : 'false',
        sound_enabled: soundInput ? (soundInput.checked ? 'true' : 'false') : 'true'
      };
      try {
        const res = await window.cvFetch('/api/settings', {
          method: 'POST',
          body: payload
        });
        if (!res.ok) throw new Error('Failed to save settings');
        applyReducedMotion(payload.reduced_motion === 'true');
        msg.textContent = 'Settings saved.';
        msg.style.display = 'block';
        setTimeout(function () { msg.style.display = 'none'; }, 2500);
      } catch (err) {
        msg.textContent = 'Save failed: ' + escapeHtml(err.message);
        msg.style.color = 'var(--jelly-red)';
        msg.style.display = 'block';
      }
    });
  }

  // Immediate theme restore on load
  const saved = localStorage.getItem('cv-theme');
  if (saved) setTheme(saved);
  if (reducedInput && reducedInput.checked) applyReducedMotion(true);

})();
