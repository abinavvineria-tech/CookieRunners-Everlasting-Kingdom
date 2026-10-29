/* ==========================================================================
   CookieVerse Everlasting Bloom — The Everlasting Trinity (trinity.js)
   Interactive timeline controls for White Lily, Pure Vanilla, and the
   creator's Cookie Runner journey. All data loaded from a local config file.
   ========================================================================== */

(function () {
  "use strict";

  // ---------------- References ----------------
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  const lanes = {
    whitelily: $("#events-whitelily"),
    purevanilla: $("#events-purevanilla"),
    creator: $("#events-creator"),
  };

  const tabs = $$(".tab");
  const filterSelect = $("#filter-type");
  const sortSelect = $("#sort-order");
  const statusEl = $("#memoryStatus");
  const resetStatusEl = $("#resetStatus");

  // Config URL (served by Flask as static)
  const CONFIG_URL = "/static/data/trinity-timeline.json";

  // localStorage keys
  const STORAGE_KEY = "trinity_memories_v1";

  // ---------------- State ----------------
  let config = null;
  let userMemories = []; // entries added by the fan (saved locally)
  let activeTab = "all";
  let filterType = "all"; // all | official | personal
  let sortOrder = "asc"; // asc | desc

  // ---------------- Init ----------------
  async function init() {
    try {
      const response = await fetch(CONFIG_URL);
      if (!response.ok) throw new Error("Timeline config not available");
      config = await response.json();
    } catch (error) {
      console.error("Failed to load timeline config:", error);
      showStatus(statusEl, "Unable to load the timeline right now. Please refresh.", true);
      return;
    }

    loadUserMemories();
    bindControls();
    render();
  }

  // ---------------- Data helpers ----------------

  // Date sort key: iso string like "2021-01-21" or partial like "03-11" or "story-canon"
  function sortKey(event) {
    const iso = event.iso || "";
    // story-canon sorts last; partial month-day sorts after full dates but before story-canon
    if (iso === "story-canon") return "9999-99-99";
    if (/^\d{2}-\d{2}$/.test(iso)) return "0000-" + iso; // annual remembrance at start
    return iso || "9999-99-99";
  }

  function typeLabel(type) {
    return type === "official" ? "Official Lore" : "Personal Memory";
  }

  function passesFilter(event) {
    if (filterType === "all") return true;
    return event.type === filterType;
  }

  function matchesTab(eventTrack) {
    if (activeTab === "all") return true;
    if (activeTab === "purelily") return false; // PureLily chapter handled separately by section visibility
    return eventTrack === activeTab;
  }

  // Collect all timeline events across the three tracks, plus user memories
  function collectEvents() {
    const all = [];

    if (config && config.tracks) {
      ["whitelily", "purevanilla", "creator"].forEach((trackId) => {
        const track = config.tracks[trackId];
        if (!track || !track.events) return;
        track.events.forEach((event) => {
          all.push({
            ...event,
            track: trackId,
            trackName: track.name,
            trackTitle: track.title,
            trackColor: track.color,
            trackBadge: track.badge || trackId,
            sourceNote: event.source,
            isUser: false,
          });
        });
      });
    }

    // Append user memories (tagged by their chosen track)
    userMemories.forEach((m) => {
      all.push({
        id: m.id,
        date: m.date,
        iso: m.iso || "",
        headline: m.headline,
        body: m.body,
        type: m.type || "personal",
        source: "Your personal memory (saved in your browser)",
        tags: ["personal", "added-by-you"],
        track: m.track || "creator",
        trackName: m.trackName || "Your Memory",
        trackTitle: m.trackTitle || "",
        trackColor: null,
        trackBadge: "YOUR MEMORY",
        sourceNote: m.source || "Your personal memory",
        isUser: true,
      });
    });

    return all;
  }

  // ---------------- Rendering ----------------

  function render() {
    if (!config) return;

    // Update tab active states
    tabs.forEach((t) => {
      const active = t.dataset.tab === activeTab;
      t.classList.toggle("active", active);
      t.setAttribute("aria-selected", active);
    });

    // Show/hide PureLily chapter
    const purelilySection = $("#purelily-chapter");
    if (purelilySection) {
      purelilySection.style.display = activeTab === "purelily" ? "block" : "none";
    }

    // Show/hide creator profile on creator tab (context)
    const creatorProfile = $(".creator-profile-section");
    if (creatorProfile) {
      creatorProfile.style.display = activeTab === "creator" || activeTab === "all" ? "block" : "none";
    }

    // Clear lane containers
    Object.values(lanes).forEach((lane) => (lane.innerHTML = ""));

    const events = collectEvents()
      .filter((e) => passesFilter(e))
      .filter((e) => matchesTab(e.track))
      .sort((a, b) => {
        const ka = sortKey(a);
        const kb = sortKey(b);
        if (ka < kb) return sortOrder === "asc" ? -1 : 1;
        if (ka > kb) return sortOrder === "asc" ? 1 : -1;
        return 0;
      });

    if (events.length === 0) {
      Object.values(lanes).forEach((lane) => {
        lane.innerHTML = `<div class="empty-timeline">No milestones match your current filters.</div>`;
      });
      return;
    }

    // Group by track for lane rendering
    const byTrack = {};
    events.forEach((e) => {
      if (!byTrack[e.track]) byTrack[e.track] = [];
      byTrack[e.track].push(e);
    });

    ["whitelily", "purevanilla", "creator"].forEach((trackId) => {
      const lane = lanes[trackId];
      const trackEvents = byTrack[trackId] || [];
      if (activeTab !== "all" && activeTab !== trackId) {
        // When a single track tab is active, only that lane shows content
        if (activeTab !== trackId) lane.innerHTML = "";
      }
      trackEvents.forEach((event) => {
        lane.appendChild(createEventCard(event));
      });
    });
  }

  function createEventCard(event) {
    const card = document.createElement("article");
    card.className = "event-card";
    card.dataset.id = event.id;
    card.dataset.track = event.track;

    const color = event.trackColor || {};
    const markerClass =
      event.track === "purevanilla" ? "pv" : event.track === "creator" ? "cr" : "";
    const typeClass = event.type === "official" ? "official" : "personal";

    const iso = event.iso || "";
    const dateDisplay = event.date;
    const isAnnual = /^\d{2}-\d{2}$/.test(iso);

    const expanded = event.id === (card.dataset.expanded || "");

    card.innerHTML = `
      <div class="event-header" role="button" tabindex="0" aria-expanded="false" aria-label="Expand milestone: ${event.headline}">
        <div class="event-meta">
          <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
            <span class="event-date">${escapeHtml(dateDisplay)}${isAnnual ? " (annual)" : ""}</span>
            <span class="event-type ${typeClass}">${typeLabel(event.type)}</span>
          </div>
          <h3 class="event-headline">${escapeHtml(event.headline)}</h3>
          <p class="event-body">${escapeHtml(event.body)}</p>
          <div class="event-source">Source: ${escapeHtml(event.sourceNote || event.source)}</div>
        </div>
        <div class="expand-icon" aria-hidden="true">▼</div>
      </div>
      <div class="event-actions">
        <button class="event-btn" data-action="expand" aria-label="${expanded ? "Collapse" : "Expand"} milestone">${expanded ? "Show less" : "Show more"}</button>
      </div>
    `;

    const header = card.querySelector(".event-header");
    const expandBtn = card.querySelector('[data-action="expand"]');
    const expandIcon = card.querySelector(".expand-icon");

    function setExpanded(state) {
      card.classList.toggle("expanded", state);
      header.setAttribute("aria-expanded", state);
      expandBtn.textContent = state ? "Show less" : "Show more";
      expandBtn.setAttribute("aria-label", state ? "Collapse milestone" : "Expand milestone");
      expandIcon.textContent = state ? "▲" : "▼";
      card.dataset.expanded = state ? event.id : "";
    }

    function toggleExpanded() {
      setExpanded(!card.classList.contains("expanded"));
    }

    header.addEventListener("click", toggleExpanded);
    header.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        toggleExpanded();
      }
    });
    expandBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleExpanded();
    });

    return card;
  }

  // ---------------- Controls ----------------

  function bindControls() {
    // Tabs
    tabs.forEach((t) => {
      t.addEventListener("click", () => {
        activeTab = t.dataset.tab;
        render();
      });
      t.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          activeTab = t.dataset.tab;
          render();
        }
      });
    });

    // Filter
    filterSelect.addEventListener("change", () => {
      filterType = filterSelect.value;
      render();
    });

    // Sort
    sortSelect.addEventListener("change", () => {
      sortOrder = sortSelect.value;
      render();
    });
  }

  // ---------------- Add My Memory (localStorage) ----------------

  function loadUserMemories() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      userMemories = raw ? JSON.parse(raw) : [];
      if (!Array.isArray(userMemories)) userMemories = [];
    } catch (error) {
      console.error("Failed to read localStorage memories:", error);
      userMemories = [];
    }
  }

  function saveUserMemories() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(userMemories.slice(-100)));
    } catch (error) {
      console.error("Failed to save localStorage memories:", error);
      showStatus(statusEl, "Could not save to your browser storage. Private mode may block this.", true);
    }
  }

  const addForm = $("#addMemoryForm");
  const cancelBtn = $("#cancelMemory");

  if (addForm) {
    addForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const name = $("#memoryName").value.trim();
      const track = $("#memoryTrack").value;
      const date = $("#memoryDate").value.trim();
      const type = $("#memoryType").value;
      const headline = $("#memoryHeadline").value.trim();
      const body = $("#memoryBody").value.trim();

      if (!date || !headline || !body) {
        showStatus(statusEl, "Please fill in date, headline, and your memory.", true);
        return;
      }

      const trackInfo = getTrackInfo(track);

      const memory = {
        id: "user-" + Date.now(),
        date,
        iso: parseUserIso(date),
        headline,
        body,
        type,
        source: "Your personal memory",
        track,
        trackName: trackInfo.name,
        trackTitle: trackInfo.title,
        trackColor: trackInfo.color,
        trackBadge: "YOUR MEMORY",
        sourceNote: "Saved privately in your browser (localStorage)",
        createdAt: new Date().toISOString(),
        runnerName: name || "Cookie Runner",
      };

      userMemories.push(memory);
      saveUserMemories();
      render();

      addForm.reset();
      showStatus(statusEl, "Your memory has been saved privately in your browser.", false);
      setTimeout(() => showStatus(statusEl, "", false), 4000);
    });
  }

  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      addForm.reset();
      showStatus(statusEl, "", false);
    });
  }

  function getTrackInfo(trackId) {
    const map = {
      whitelily: { name: "White Lily Cookie", title: "The Legend of Truth", color: null },
      purevanilla: { name: "Pure Vanilla Cookie", title: "The Light of Hope", color: null },
      creator: { name: "The Cookie Runner", title: "The Keeper of Memories", color: null },
      purelily: { name: "PureLily", title: "Where Lily Meets Vanilla", color: null },
    };
    return map[trackId] || map.creator;
  }

  // Best-effort ISO parse from a free-text date; fallback to empty string
  function parseUserIso(dateStr) {
    if (!dateStr) return "";
    const parsed = Date.parse(dateStr);
    if (!isNaN(parsed)) {
      return new Date(parsed).toISOString().slice(0, 10);
    }
    // Handle "Month D, YYYY"
    const m = dateStr.match(/^(\w+)\s+(\d{1,2}),?\s+(\d{4})$/);
    if (m) {
      const parsed2 = Date.parse(dateStr);
      return !isNaN(parsed2) ? new Date(parsed2).toISOString().slice(0, 10) : "";
    }
    return "";
  }

  // ---------------- Reset with confirmation ----------------

  const resetBtn = $("#resetMemories");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      if (userMemories.length === 0) {
        showStatus(resetStatusEl, "No memories to reset.", false);
        return;
      }
      if (window.confirm("Reset all your saved memories? This cannot be undone and only affects your browser's local storage.")) {
        userMemories = [];
        saveUserMemories();
        render();
        showStatus(resetStatusEl, "Your memories have been reset.", false);
        setTimeout(() => showStatus(resetStatusEl, "", false), 4000);
      }
    });
  }

  // ---------------- Status helper ----------------

  function showStatus(el, message, isError) {
    if (!el) return;
    el.textContent = message;
    el.style.color = isError ? "#b04040" : "";
    el.setAttribute("aria-live", "polite");
  }

  // ---------------- Escape helper ----------------
  function escapeHtml(text) {
    if (text == null) return "";
    const div = document.createElement("div");
    div.textContent = String(text);
    return div.innerHTML;
  }

  // Kick off
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

})();
