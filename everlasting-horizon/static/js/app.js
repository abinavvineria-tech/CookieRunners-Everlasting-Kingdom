/* ==========================================================================
   EVERLASTING HORIZON — Application JavaScript
   Mobile nav, flash dismiss, accessibility, and small interactions.
   ========================================================================== */
(function () {
  'use strict';

  // ---- Mobile navigation toggle ----
  var toggle = document.querySelector('.nav-toggle');
  var navLinks = document.querySelector('.nav-links');

  if (toggle && navLinks) {
    toggle.addEventListener('click', function () {
      var open = navLinks.classList.toggle('mobile-open');
      toggle.setAttribute('aria-expanded', open);
      toggle.textContent = open ? '✕' : '☰';
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });

    // Close mobile menu when a link is tapped
    var links = navLinks.querySelectorAll('a');
    links.forEach(function (link) {
      link.addEventListener('click', function () {
        navLinks.classList.remove('mobile-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.textContent = '☰';
        toggle.setAttribute('aria-label', 'Open menu');
      });
    });
  }

  // ---- Dismissible flash messages ----
  document.querySelectorAll('.flash').forEach(function (flash) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'btn-ghost btn-sm';
    btn.textContent = '✕';
    btn.setAttribute('aria-label', 'Dismiss message');
    btn.style.marginLeft = '10px';
    btn.style.padding = '4px 8px';
    btn.addEventListener('click', function () {
      flash.style.opacity = '0';
      setTimeout(function () { flash.remove(); }, 300);
    });
    flash.appendChild(btn);
  });

  // ---- Highlight the current page in navigation ----
  var currentPath = window.location.pathname;
  document.querySelectorAll('nav a').forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // ---- Confirm destructive actions ----
  document.querySelectorAll('form[data-confirm]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!confirm(form.getAttribute('data-confirm'))) {
        event.preventDefault();
      }
    });
  });
})();
