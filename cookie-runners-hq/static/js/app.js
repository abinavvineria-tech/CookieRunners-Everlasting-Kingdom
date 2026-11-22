/* =====================================================================
   Cookie Runners HQ — Application JavaScript
   ===================================================================== */

(function () {
  "use strict";

  // ---------- Theme ----------
  const THEME_KEY = "cr-theme";
  const html = document.documentElement;
  const themeToggle = document.getElementById("theme-toggle");

  function getSavedTheme() {
    try {
      return localStorage.getItem(THEME_KEY);
    } catch (e) {
      return null;
    }
  }

  function applyTheme(theme) {
    if (theme === "dark") {
      html.setAttribute("data-theme", "dark");
    } else {
      html.removeAttribute("data-theme");
    }
    if (themeToggle) {
      themeToggle.textContent = theme === "dark" ? "☀️" : "🌙";
      themeToggle.setAttribute("aria-pressed", theme === "dark");
    }
  }

  if (themeToggle) {
    const saved = getSavedTheme();
    applyTheme(saved || "light");
    themeToggle.addEventListener("click", function () {
      const isDark = html.hasAttribute("data-theme");
      applyTheme(isDark ? "light" : "dark");
      try {
        localStorage.setItem(THEME_KEY, isDark ? "light" : "dark");
      } catch (e) {
        // storage unavailable — ignore
      }
    });
  }

  // ---------- Mobile nav ----------
  const navToggle = document.getElementById("nav-toggle");
  const siteNav = document.getElementById("site-nav");
  if (navToggle && siteNav) {
    navToggle.addEventListener("click", function () {
      const open = siteNav.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", open);
    });
    // Close menu when a link is clicked
    siteNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        siteNav.classList.remove("open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // ---------- Flash dismiss ----------
  setTimeout(function () {
    document.querySelectorAll(".flash").forEach(function (flash) {
      flash.style.opacity = "0";
      setTimeout(function () {
        flash.remove();
      }, 300);
    });
  }, 5000);

  // ---------- Delete confirmations ----------
  document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      const message = form.getAttribute("data-confirm") || "Are you sure?";
      if (!confirm(message)) {
        event.preventDefault();
      }
    });
  });

  // ---------- Highlight current nav link ----------
  const currentPath = window.location.pathname;
  document.querySelectorAll(".site-nav a").forEach(function (link) {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    }
  });
})();
