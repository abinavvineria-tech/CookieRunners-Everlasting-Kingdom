/* ========================================================================
   Champions League Countdown Nexus — app.js
   Unofficial fan project. Vanilla JavaScript interactivity.
   ======================================================================== */

(function () {
  "use strict";

  // ------------------------------------------------------------------
  // Constants
  // ------------------------------------------------------------------
  const API_EVENT = "/api/event";
  const STORAGE_THEME = "clcn:theme";
  const STORAGE_NOTIFY = "clcn:notifications";
  const NOTIFY_PERMISSIONED_KEY = "clcn:notify_permissioned";

  // ------------------------------------------------------------------
  // DOM elements
  // ------------------------------------------------------------------
  const els = {
    loadingScreen: null,
    navToggle: document.getElementById("nav-toggle"),
    siteNav: document.getElementById("site-nav"),
    navLinks: document.querySelectorAll(".nav-link"),
    themeToggle: document.getElementById("theme-toggle"),
    themeToggleText: document.getElementById("theme-toggle-text"),
    shareBtn: document.getElementById("share-btn"),
    copyBtn: document.getElementById("copy-btn"),
    notifyBtn: document.getElementById("notify-btn"),
    notifyText: document.getElementById("notify-text"),
    copyDetailsBtn: document.getElementById("copy-details-btn"),
    backToTop: document.getElementById("back-to-top"),
    toast: document.getElementById("toast"),
    countdown: {
      days: document.getElementById("c-days"),
      hours: document.getElementById("c-hours"),
      minutes: document.getElementById("c-minutes"),
      seconds: document.getElementById("c-seconds"),
      state: document.getElementById("countdown-state"),
      meta: document.getElementById("countdown-meta"),
      label: document.querySelector(".countdown-label"),
      card: document.getElementById("countdown-card"),
    },
    event: {
      name: document.getElementById("ev-name"),
      datetime: document.getElementById("ev-datetime"),
      tz: document.getElementById("ev-tz"),
      status: document.getElementById("ev-status"),
      desc: document.getElementById("ev-desc"),
      note: document.getElementById("ev-note"),
    },
    overlay: document.getElementById("event-started-overlay"),
    closeOverlay: document.getElementById("close-overlay"),
    mainContent: document.getElementById("main-content"),
  };

  let intervalId = null;
  let launchedShown = false;

  // ------------------------------------------------------------------
  // Helpers
  // ------------------------------------------------------------------
  function pad(n) {
    return String(n).padStart(2, "0");
  }

  function setText(el, text) {
    if (!el) return;
    if (el.textContent !== text) el.textContent = text;
  }

  function showToast(msg, duration = 3000) {
    if (!els.toast) return;
    els.toast.textContent = msg;
    els.toast.classList.add("show");
    clearTimeout(els.toast._timer);
    els.toast._timer = setTimeout(() => {
      els.toast.classList.remove("show");
    }, duration);
  }

  function escapeHtml(str) {
    if (typeof str !== "string") return "";
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  // ------------------------------------------------------------------
  // Loading screen
  // ------------------------------------------------------------------
  function removeLoadingScreen() {
    if (!els.loadingScreen) return;
    window.addEventListener("load", () => {
      setTimeout(() => {
        els.loadingScreen.classList.add("loaded");
        setTimeout(() => els.loadingScreen.remove(), 500);
      }, 350);
    });
  }

  // ------------------------------------------------------------------
  // Theme toggle
  // ------------------------------------------------------------------
  function initTheme() {
    const saved = localStorage.getItem(STORAGE_THEME);
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const theme = saved || (prefersDark ? "dark" : "light");
    setTheme(theme, false);

    els.themeToggle.addEventListener("click", () => {
      const current = document.body.dataset.theme || "dark";
      const next = current === "dark" ? "light" : "dark";
      setTheme(next, true);
    });
  }

  function setTheme(theme, announce) {
    document.body.dataset.theme = theme;
    document.body.className = "theme-" + theme;
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
      meta.content = theme === "dark" ? "#0b1f16" : "#f0fdf4";
    }
    if (els.themeToggleText) {
      els.themeToggleText.textContent =
        theme === "dark" ? "Switch to light theme" : "Switch to dark theme";
    }
    localStorage.setItem(STORAGE_THEME, theme);
    if (announce) showToast("Theme: " + (theme === "dark" ? "Dark" : "Light"));
  }

  // ------------------------------------------------------------------
  // Navigation
  // ------------------------------------------------------------------
  function initNavigation() {
    if (els.navToggle && els.siteNav) {
      els.navToggle.addEventListener("click", () => {
        const expanded = els.navToggle.getAttribute("aria-expanded") === "true";
        els.navToggle.setAttribute("aria-expanded", String(!expanded));
        els.siteNav.classList.toggle("open", !expanded);
      });
    }

    els.navLinks.forEach((link) => {
      link.addEventListener("click", (e) => {
        const href = link.getAttribute("href");
        if (href && href.startsWith("#")) {
          e.preventDefault();
          const target = document.querySelector(href);
          if (target) {
            target.scrollIntoView({ behavior: "smooth", block: "start" });
            window.scrollBy(0, -70);
          }
          setActiveSection(link.dataset.section || href);
          els.siteNav.classList.remove("open");
          if (els.navToggle) els.navToggle.setAttribute("aria-expanded", "false");
        }
      });
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) setActiveSection(entry.target.id);
        });
      },
      { threshold: 0.25, rootMargin: "-100px 0% -60% 0%" }
    );
    document.querySelectorAll("section[id]").forEach((sec) => observer.observe(sec));
  }

  function setActiveSection(id) {
    els.navLinks.forEach((link) => {
      const linkHref = link.getAttribute("href");
      const isActive = linkHref === "#" + id || link.dataset.section === id;
      link.classList.toggle("active", isActive);
      link.setAttribute("aria-current", isActive ? "page" : "false");
    });
  }

  // ------------------------------------------------------------------
  // Countdown (Asia/Kolkata / IST, synchronized with system clock)
  // ------------------------------------------------------------------
  async function initCountdown() {
    const data = await fetchEventData();
    if (!data) return;
    renderEventInfo(data);

    function tick() {
      const now = new Date();
      // Use the server-provided now_iso to compute a consistent reference,
      // then advance by elapsed local time so the clock stays synchronized.
      const serverNow = data.now_iso ? new Date(data.now_iso) : now;
      const target = new Date(data.target_iso);
      const elapsed = now.getTime() - serverNow.getTime();
      const diffSeconds = Math.floor((target.getTime() - now.getTime()) / 1000) - Math.floor(elapsed / 1000) + Math.floor((target.getTime() - serverNow.getTime()) / 1000);

      // Simpler: recompute from target vs now directly (browser local time == system clock).
      const diff = target.getTime() - now.getTime();

      if (diff <= 0) {
        showLaunchedState(data);
        return;
      }

      const totalSeconds = Math.floor(diff / 1000);
      const days = Math.floor(totalSeconds / (24 * 3600));
      const hours = Math.floor((totalSeconds % (24 * 3600)) / 3600);
      const minutes = Math.floor((totalSeconds % 3600) / 60);
      const seconds = totalSeconds % 60;

      setText(els.countdown.days, pad(days));
      setText(els.countdown.hours, pad(hours));
      setText(els.countdown.minutes, pad(minutes));
      setText(els.countdown.seconds, pad(seconds));

      setText(
        els.countdown.state,
        "Launching soon — get ready for the Welcome Night"
      );
      els.countdown.state.className = "";
      setText(
        els.countdown.meta,
        data.target_label
          ? "Target: " + data.target_label + "  &#8226;  " + data.timezone
          : ""
      );
    }

    tick();
    intervalId = setInterval(tick, 1000);
  }

  async function fetchEventData() {
    try {
      const res = await fetch(API_EVENT, { cache: "no-store" });
      if (!res.ok) throw new Error("Failed to load event data");
      return await res.json();
    } catch (err) {
      console.error("Event data load error:", err);
      showToast("Using default event data.", 3000);
      return null;
    }
  }

  function renderEventInfo(data) {
    if (!data) return;
    const ev = data.event || {};
    setText(els.event.name, ev.name || "Champions League Welcome Night");
    setText(
      els.event.datetime,
      ev.kickoff_label || (ev.date + " " + ev.time)
    );
    setText(els.event.tz, ev.timezone || "Asia/Kolkata");
    setText(els.event.desc, ev.description || "");
    setText(els.event.note, ev.unofficial_note || "");

    const statusEl = els.event.status;
    if (data.launched) {
      setText(statusEl, "Launched");
      statusEl.className = "badge launched";
    } else {
      setText(statusEl, "Counting down");
      statusEl.className = "badge counting_down";
    }
  }

  function showLaunchedState(data) {
    if (launchedShown) return;
    launchedShown = true;
    clearInterval(intervalId);

    [els.countdown.days, els.countdown.hours, els.countdown.minutes, els.countdown.seconds].forEach(
      (el) => setText(el, "00")
    );
    setText(els.countdown.state, "LIVE — THE CHAMPIONSHIP HAS BEGUN!");
    els.countdown.state.className = "live";
    if (els.event.status) {
      setText(els.event.status, "Launched");
      els.event.status.className = "badge launched";
    }

    // Show the event-started overlay.
    if (els.overlay) els.overlay.classList.remove("hidden");

    showToast("The Championship is LIVE!");

    // Fire a one-time notification if permission was previously granted.
    if (
      localStorage.getItem(NOTIFY_PERMISSIONED_KEY) === "true" &&
      Notification.permission === "granted"
    ) {
      try {
        new Notification("Champions League Welcome Night", {
          body: "The Championship has begun! Welcome Night is now live.",
          icon: undefined,
        });
      } catch (_) {
        // Notifications failed silently — optional feature.
      }
    }
  }

  // ------------------------------------------------------------------
  // Browser notifications (consent-only)
  // ------------------------------------------------------------------
  async function initNotifications() {
    if (!els.notifyBtn || !els.notifyText) return;

    const alreadyPermissioned = localStorage.getItem(NOTIFY_PERMISSIONED_KEY) === "true";
    if (alreadyPermissioned && Notification.permission === "granted") {
      setNotifyUI(true);
      return;
    }

    els.notifyBtn.addEventListener("click", async () => {
      if (!("Notification" in window)) {
        showToast("Notifications not supported on this browser.");
        return;
      }

      if (Notification.permission === "granted") {
        setNotifyUI(true);
        showToast("Notifications enabled.");
        return;
      }

      if (Notification.permission === "denied") {
        showToast("Notifications are blocked in browser settings.");
        return;
      }

      // Request permission — consent only.
      const result = await Notification.requestPermission();
      if (result === "granted") {
        localStorage.setItem(NOTIFY_PERMISSIONED_KEY, "true");
        setNotifyUI(true);
        showToast("Notifications enabled.");
        // Schedule a reminder at event time if already launched data available.
        scheduleEventNotification();
      } else {
        showToast("Notification permission not granted.");
      }
    });
  }

  function setNotifyUI(enabled) {
    if (!els.notifyBtn || !els.notifyText) return;
    if (enabled) {
      els.notifyBtn.classList.add("notify-enabled");
      els.notifyBtn.setAttribute("aria-pressed", "true");
      setText(els.notifyText, "Notifications on");
    } else {
      els.notifyBtn.classList.remove("notify-enabled");
      els.notifyBtn.setAttribute("aria-pressed", "false");
      setText(els.notifyText, "Enable notifications");
    }
  }

  function scheduleEventNotification() {
    // One-time reminder when the countdown reaches zero, using the permission
    // already granted. Handled inside showLaunchedState().
  }

  // ------------------------------------------------------------------
  // Copy event details
  // ------------------------------------------------------------------
  function initCopyButtons() {
    const detailsText =
      "Champions League Countdown Nexus — Welcome Night\n" +
      "Event: Cookie Run Kingdom Champions League Welcome Night\n" +
      "Date: 11 November 2026\n" +
      "Kickoff: 8:30 PM IST (Asia/Kolkata)\n" +
      "Unofficial fan project — not an official Devsisters website.\n\n" +
      "LET THE CHAMPIONSHIP BEGIN!";

    function copyText(text, successMsg) {
      return navigator.clipboard
        .writeText(text)
        .then(() => {
          showToast(successMsg);
        })
        .catch(() => {
          showToast("Copy not supported on this browser.");
        });
    }

    function attach(btn) {
      if (!btn) return;
      btn.addEventListener("click", () => copyText(detailsText, "Event details copied to clipboard"));
    }
    attach(els.copyBtn);
    attach(els.copyDetailsBtn);
  }

  // ------------------------------------------------------------------
  // Share
  // ------------------------------------------------------------------
  function initShareButton() {
    if (!els.shareBtn) return;
    els.shareBtn.addEventListener("click", async () => {
      const data = {
        title: document.title,
        text: "Champions League Countdown Nexus — Welcome Night. 11 November 2026, 8:30 PM IST.",
        url: window.location.href,
      };
      try {
        if (navigator.share && navigator.canShare && navigator.canShare(data)) {
          await navigator.share(data);
          showToast("Event shared!");
        } else if (navigator.share) {
          await navigator.share(data);
          showToast("Event shared!");
        } else {
          await navigator.clipboard.writeText(window.location.href);
          showToast("Link copied to clipboard.");
        }
      } catch (err) {
        try {
          await navigator.clipboard.writeText(window.location.href);
          showToast("Link copied to clipboard.");
        } catch (_) {
          showToast("Sharing not supported on this browser.");
        }
      }
    });
  }

  // ------------------------------------------------------------------
  // Scroll effects
  // ------------------------------------------------------------------
  function initScrollEffects() {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add("is-visible");
        });
      },
      { threshold: 0.12 }
    );
    document.querySelectorAll(".section").forEach((sec) => observer.observe(sec));

    const header = document.getElementById("site-header");
    window.addEventListener("scroll", () => {
      if (header) {
        header.style.boxShadow = window.scrollY > 40 ? "var(--shadow)" : "none";
      }
    });
  }

  // ------------------------------------------------------------------
  // Back to top
  // ------------------------------------------------------------------
  function initBackToTop() {
    if (!els.backToTop) return;
    window.addEventListener("scroll", () => {
      if (window.scrollY > 300) els.backToTop.classList.add("visible");
      else els.backToTop.classList.remove("visible");
    });
    els.backToTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // ------------------------------------------------------------------
  // Overlay close
  // ------------------------------------------------------------------
  function initOverlay() {
    if (!els.closeOverlay || !els.overlay) return;
    els.closeOverlay.addEventListener("click", () => {
      els.overlay.classList.add("hidden");
    });
  }

  // ------------------------------------------------------------------
  // Boot
  // ------------------------------------------------------------------
  function init() {
    removeLoadingScreen();
    initTheme();
    initNavigation();
    initCountdown();
    initNotifications();
    initCopyButtons();
    initShareButton();
    initScrollEffects();
    initBackToTop();
    initOverlay();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
