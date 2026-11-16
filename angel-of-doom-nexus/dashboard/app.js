/* ============================================================================
   ANGEL OF DOOM — Hermes Agent Dashboard
   Application logic: panel navigation, sidebar toggle, live clock, logs.
   Unofficial fan project — not affiliated with or endorsed by Devsisters.
   ============================================================================ */

(function () {
  "use strict";

  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("topbar-toggle");
  const navItems = document.querySelectorAll(".nav-item");
  const panels = document.querySelectorAll(".panel");
  const logConsole = document.getElementById("log-console");

  // ── Toggle sidebar (mobile) ──
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener("click", () => {
      const isOpen = sidebar.classList.toggle("open");
      toggleBtn.setAttribute("aria-expanded", isOpen);
    });
  }

  // ── Close sidebar when clicking a nav item (mobile) ──
  navItems.forEach((item) => {
    item.addEventListener("click", (e) => {
      // Only handle anchor-style navigation within this SPA
      const target = item.getAttribute("data-panel");
      if (!target) return;

      e.preventDefault();

      // Update active nav item
      navItems.forEach((n) => {
        n.classList.remove("active");
        n.removeAttribute("aria-current");
      });
      item.classList.add("active");
      item.setAttribute("aria-current", "page");

      // Switch panels
      panels.forEach((p) => {
        p.classList.add("hidden");
      });
      const targetPanel = document.getElementById("panel-" + target);
      if (targetPanel) {
        targetPanel.classList.remove("hidden");
      }

      // Close sidebar on mobile
      if (sidebar && sidebar.classList.contains("open")) {
        sidebar.classList.remove("open");
        if (toggleBtn) toggleBtn.setAttribute("aria-expanded", "false");
      }

      log(`Navigated to panel: ${target}`, "info");
    });
  });

  // ── Live clock in topbar status ──
  function updateClock() {
    const now = new Date();
    // Display in local time; user prefers IST (UTC+5:30) for Cookie Run updates
    const istOffset = 5 * 60 + 30; // minutes
    const ist = new Date(now.getTime() + istOffset * 60000);
    const timeStr = ist.toLocaleTimeString("en-IN", {
      hour12: false,
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      timeZone: "Asia/Kolkata",
    });
    const el = document.getElementById("topbar-clock");
    if (el) el.textContent = timeStr + " IST";
  }
  setInterval(updateClock, 1000);
  updateClock();

  // ── Log helper ──
  function log(message, level = "info") {
    if (!logConsole) return;
    const now = new Date();
    const istOffset = 5 * 60 + 30;
    const ist = new Date(now.getTime() + istOffset * 60000);
    const timeStr = ist.toLocaleTimeString("en-IN", {
      hour12: false,
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      timeZone: "Asia/Kolkata",
    });

    const line = document.createElement("div");
    line.className = "log-line";
    line.innerHTML = `
      <span class="log-time">[${timeStr}]</span>
      <span class="log-level log-${level}">${level.toUpperCase()}</span>
      <span class="log-message">${escapeHtml(message)}</span>
    `;
    logConsole.appendChild(line);
    logConsole.scrollTop = logConsole.scrollHeight;
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  // ── Initial log ──
  log("Angel of Doom Hermes Agent dashboard loaded.", "success");
  log("Visual identity palette applied from measured reference.", "info");
  log("Unofficial fan project — not affiliated with Devsisters.", "warn");

  // ── Settings form (no persistence; demonstration only) ──
  const saveBtn = document.querySelector(".btn-primary");
  if (saveBtn) {
    saveBtn.addEventListener("click", () => {
      log("Settings saved (session only).", "success");
    });
  }

})();
