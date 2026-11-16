/* PureLily: Forever Together — Interactive JavaScript
   Features: mobile navigation, petal-bud memory opener, falling petals,
             community wall (localStorage only), smooth section nav
   Unofficial fan project — Cookie Run: Kingdom celebration
*/

document.addEventListener("DOMContentLoaded", () => {
  initMobileNav();
  initActiveNavLinks();
  initPetalBuds();
  initFallingPetals();
  initCommunityWall();
});

// --- Mobile Navigation ---
function initMobileNav() {
  const toggle = document.getElementById("nav-toggle");
  const links = document.getElementById("nav-links");

  if (!toggle || !links) return;

  toggle.addEventListener("click", () => {
    const isOpen = links.classList.toggle("open");
    toggle.classList.toggle("active");
    toggle.setAttribute("aria-expanded", isOpen);
    toggle.setAttribute("aria-label", isOpen ? "Close menu" : "Toggle menu");
  });

  links.querySelectorAll("a").forEach((anchor) => {
    anchor.addEventListener("click", () => {
      links.classList.remove("open");
      toggle.classList.remove("active");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Toggle menu");
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && links.classList.contains("open")) {
      links.classList.remove("open");
      toggle.classList.remove("active");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Toggle menu");
    }
  });
}

// --- Active Nav Link on Scroll ---
function initActiveNavLinks() {
  const links = document.querySelectorAll(".nav-links a[href^='#']");
  const sections = Array.from(links)
    .map((a) => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);

  if (!links.length || !sections.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          links.forEach((a) => a.classList.remove("active"));
          const active = document.querySelector(
            `.nav-links a[href="#${entry.target.id}"]`
          );
          if (active) active.classList.add("active");
        }
      });
    },
    { threshold: 0.25 }
  );

  sections.forEach((section) => observer.observe(section));
}

// --- Petal Buds: friendship memory opener ---
function initPetalBuds() {
  const triggers = document.querySelectorAll(".bud-trigger");
  const panels = document.querySelectorAll(".message-panel");

  triggers.forEach((trigger) => {
    const bud = trigger.querySelector(".bud");
    const targetId = trigger.getAttribute("data-target");
    const target = document.getElementById(targetId);

    trigger.addEventListener("click", () => {
      const isOpen = trigger.getAttribute("aria-expanded") === "true";

      // Close all other open buds/panels
      triggers.forEach((t) => {
        t.setAttribute("aria-expanded", "false");
        t.querySelector(".bud").classList.remove("open");
        const id = t.getAttribute("data-target");
        document.getElementById(id).hidden = true;
      });

      if (!isOpen) {
        trigger.setAttribute("aria-expanded", "true");
        bud.classList.add("open");
        target.hidden = false;
        target.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    });
  });

  document.querySelectorAll(".msg-close").forEach((btn) => {
    btn.addEventListener("click", () => {
      const panel = btn.closest(".message-panel");
      panel.hidden = true;
      const id = panel.id;
      const trigger = document.querySelector(`.bud-trigger[data-target="${id}"]`);
      if (trigger) {
        trigger.setAttribute("aria-expanded", "false");
        trigger.querySelector(".bud").classList.remove("open");
      }
    });
  });
}

// --- Falling petals (hero decoration) ---
function initFallingPetals() {
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (prefersReduced) return;

  const container = document.querySelector(".hero") || document.body;
  const count = 14;

  for (let i = 0; i < count; i++) {
    const petal = document.createElement("div");
    petal.className = "falling-petal";
    petal.style.left = Math.random() * 100 + "vw";
    petal.style.top = -(Math.random() * 30) + "vh";
    petal.style.animationDuration = (10 + Math.random() * 12) + "s";
    petal.style.animationDelay = (Math.random() * 8) + "s";
    petal.style.opacity = 0.35 + Math.random() * 0.45;
    container.appendChild(petal);
  }
}

// --- Community Wall (localStorage only, nothing sent anywhere) ---
function initCommunityWall() {
  const form = document.getElementById("wall-form");
  const list = document.getElementById("wall-list");
  const empty = document.getElementById("wall-empty");
  const nameInput = document.getElementById("wall-name");
  const noteInput = document.getElementById("wall-note");

  if (!form || !list || !empty || !nameInput || !noteInput) return;

  let notes = JSON.parse(localStorage.getItem("purelily_notes") || "[]");

  function render() {
    list.innerHTML = "";
    if (notes.length === 0) {
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    notes.slice().reverse().forEach((note) => {
      const el = document.createElement("article");
      el.className = "wall-note-item";
      el.innerHTML = `
        <span class="wall-note-author">${escapeHtml(note.name)}</span>
        <p class="wall-note-text">${escapeHtml(note.text)}</p>
        <time class="wall-note-time">${formatTime(note.at)}</time>
      `;
      list.appendChild(el);
    });
  }

  function escapeHtml(s) {
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  function formatTime(iso) {
    try {
      return new Date(iso).toLocaleString(undefined, {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch (e) {
      return "";
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const name = nameInput.value.trim();
    const text = noteInput.value.trim();
    if (!name || !text) return;

    notes.push({ name, text, at: new Date().toISOString() });
    localStorage.setItem("purelily_notes", JSON.stringify(notes));
    nameInput.value = "";
    noteInput.value = "";
    render();
  });

  render();
}
