// CookieVerse: Everlasting Celebrations — shared app logic
(function () {
  'use strict';

  // ---- Theme toggle ----
  const themeToggle = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  const htmlEl = document.documentElement;
  const savedTheme = localStorage.getItem('cv-theme') || 'light';

  function setTheme(theme) {
    htmlEl.setAttribute('data-theme', theme);
    localStorage.setItem('cv-theme', theme);
    if (themeIcon) {
      themeIcon.textContent = theme === 'dark' ? '&#127769;' : '&#127760;';
    }
    if (themeToggle) {
      themeToggle.setAttribute('aria-pressed', theme === 'dark');
    }
  }

  setTheme(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      const current = htmlEl.getAttribute('data-theme') || 'light';
      setTheme(current === 'light' ? 'dark' : 'light');
    });
  }

  // ---- Mobile nav toggle ----
  const navToggle = document.getElementById('nav-toggle');
  const mainNav = document.getElementById('main-nav');
  if (navToggle && mainNav) {
    navToggle.addEventListener('click', function () {
      const expanded = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', !expanded);
      mainNav.classList.toggle('active');
    });

    // Close nav when a link is clicked
    mainNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mainNav.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // ---- Global fetch helper with CSRF ----
  window.cvFetch = function (url, options) {
    options = options || {};
    const token = document.querySelector('meta[name="csrf-token"]')?.content ||
                  document.querySelector('input[name="csrf_token"]')?.value;
    const headers = options.headers || {};
    if (token) {
      headers['X-CSRFToken'] = token;
    }
    if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(options.body);
    }
    return fetch(url, Object.assign({}, options, { headers }));
  };

  // ---- Accessible button activation (Space/Enter) ----
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') {
      const target = e.target;
      if (target && target.matches('[role="button"]')) {
        e.preventDefault();
        target.click();
      }
    }
  });

})();
