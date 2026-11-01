// LilyVerse — main.js
// Responsive nav, theme toggle, reduced-motion respect, and form enhancements.

(function () {
  "use strict";

  // ---- Theme toggle (light/dark) ----
  const themeToggle = document.querySelector(".theme-toggle");
  const root = document.documentElement;

  function getSavedTheme() {
    try {
      return localStorage.getItem("lv-theme");
    } catch (e) {
      return null;
    }
  }

  function setTheme(theme) {
    if (theme === "dark") {
      root.setAttribute("data-theme", "dark");
      root.setAttribute("aria-label", "dark mode");
      if (themeToggle) {
        themeToggle.setAttribute("aria-checked", "true");
        themeToggle.textContent = "☀️";
      }
      try { localStorage.setItem("lv-theme", "dark"); } catch (e) {}
    } else {
      root.removeAttribute("data-theme");
      root.removeAttribute("aria-label");
      if (themeToggle) {
        themeToggle.setAttribute("aria-checked", "false");
        themeToggle.textContent = "🌙";
      }
      try { localStorage.setItem("lv-theme", "light"); } catch (e) {}
    }
  }

  // Respect system preference if no saved theme.
  const saved = getSavedTheme();
  if (saved) {
    setTheme(saved);
  } else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
    setTheme("dark");
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      const isDark = root.getAttribute("data-theme") === "dark";
      setTheme(isDark ? "light" : "dark");
    });
    themeToggle.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        this.click();
      }
    });
  }

  // ---- Responsive mobile nav ----
  const navToggle = document.querySelector(".nav-toggle");
  const navMenu = document.getElementById("nav-menu");

  if (navToggle && navMenu) {
    navToggle.addEventListener("click", function () {
      const open = navMenu.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", open);
    });

    // Close menu when a link is clicked.
    navMenu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navMenu.classList.remove("open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // ---- Confirm deletes inline (fallback for non-JS browsers the onsubmit covers) ----
  document.querySelectorAll("form.inline button[type='submit']").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      if (!confirm("Delete this milestone?")) {
        e.preventDefault();
      }
    });
  });

  // ---- Offer flower (AJAX) fallback already handled inline in template ----

  // ---- Announce flash messages to screen readers ----
  const flashes = document.querySelectorAll(".flash");
  flashes.forEach(function (flash) {
    if (!flash.getAttribute("role")) flash.setAttribute("role", "alert");
  });

})();
