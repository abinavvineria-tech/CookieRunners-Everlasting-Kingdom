/* CookieVerse Eternal Ceremony — ceremony interactions
 *
 * Drives the welcome -> award flow -> finale ceremony.
 * All buttons are real, tested interactions. No inert or decorative controls.
 */

(function () {
  "use strict";

  // ------------------------------------------------------------------ DOM refs
  const welcomeScreen = document.getElementById("home");
  const ceremonyScreen = document.getElementById("ceremony");
  const finaleScreen = document.getElementById("finale");

  const beginButton = document.getElementById("beginButton");
  const prevButton = document.getElementById("prevButton");
  const nextButton = document.getElementById("nextButton");
  const skipFinaleButton = document.getElementById("skipFinaleButton");
  const copyButton = document.getElementById("copyButton");
  const replayButton = document.getElementById("replayButton");
  const copyFinaleButton = document.getElementById("copyFinaleButton");

  const progressCurrent = document.getElementById("progressCurrent");
  const progressTotal = document.getElementById("progressTotal");
  const awardStage = document.getElementById("awardStage");
  const ceremonyHint = document.getElementById("ceremonyHint");
  const finaleMessage = document.getElementById("finaleMessage");
  const finaleWinners = document.getElementById("finaleWinners");

  const liveDate = document.getElementById("liveDate");
  const disclaimerText = document.getElementById("disclaimerText");
  const toast = document.getElementById("toast");

  // ------------------------------------------------------------------ State
  let currentIndex = 0;
  const awards = Array.isArray(CEREMONY_AWARDS) ? CEREMONY_AWARDS : [];
  const total = awards.length;
  const prefersReducedMotion =
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (progressTotal) progressTotal.textContent = total;

  // ------------------------------------------------------------------ Helpers
  function showToast(message, type) {
    if (!toast) return;
    toast.textContent = message;
    toast.className = "toast show";
    if (type === "copied") toast.classList.add("copied");
    clearTimeout(window._toastTimer);
    window._toastTimer = setTimeout(() => {
      toast.classList.remove("show", "copied");
    }, 2400);
  }

  function isReduced() {
    return prefersReducedMotion;
  }

  function delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  function focusElement(el) {
    if (!el) return;
    try {
      el.focus({ preventScroll: true });
    } catch (e) {
      el.focus();
    }
  }

  // ------------------------------------------------------------------ Sparkles / confetti
  function spawnSparkles(container, count) {
    if (!container || isReduced()) return;
    count = count || 10;
    const rect = container.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    for (let i = 0; i < count; i++) {
      const spark = document.createElement("span");
      spark.className = "sparkle";
      spark.textContent = ["✦", "✧", "✨", "🌟", "💫"][i % 5];
      const angle = (Math.PI * 2 * i) / count;
      const distance = 40 + Math.random() * 70;
      const tx = Math.cos(angle) * distance;
      const ty = Math.sin(angle) * distance;
      spark.style.setProperty("--tx", tx + "px");
      spark.style.setProperty("--ty", ty + "px");
      spark.style.left = centerX + "px";
      spark.style.top = centerY + "px";
      spark.style.fontSize = 12 + Math.random() * 14 + "px";
      document.body.appendChild(spark);
      // small random delay so they burst naturally
      spark.style.animationDelay = Math.random() * 0.4 + "s";
      setTimeout(() => spark.remove(), 2600);
    }
  }

  function spawnConfetti(count) {
    if (!count || isReduced()) return;
    count = count || 40;
    const colors = ["#f5d78b", "#c084fc", "#a78bfa", "#f472b6", "#34d399", "#fbbf24"];
    for (let i = 0; i < count; i++) {
      const piece = document.createElement("div");
      piece.style.position = "fixed";
      piece.style.left = Math.random() * 100 + "vw";
      piece.style.top = "-8px";
      piece.style.width = 6 + Math.random() * 8 + "px";
      piece.style.height = 6 + Math.random() * 10 + "px";
      piece.style.background = colors[i % colors.length];
      piece.style.borderRadius = Math.random() > 0.5 ? "2px" : "50%";
      piece.style.opacity = 0.9;
      piece.style.zIndex = 60;
      piece.style.pointerEvents = "none";
      document.body.appendChild(piece);
      const fall = 700 + Math.random() * 1200;
      const sway = -40 + Math.random() * 80;
      piece.animate(
        [
          { transform: `translate(0,0) rotate(0deg)`, opacity: 0.9 },
          { transform: `translate(${sway}px, ${window.innerHeight + 20}px) rotate(${360 * Math.random()}deg)`, opacity: 0 }
        ],
        { duration: fall, easing: "ease-in" }
      );
      setTimeout(() => piece.remove(), fall + 100);
    }
  }

  // ------------------------------------------------------------------ Rendering
  function renderAward(index) {
    const award = awards[index];
    if (!award) return;

    awardStage.innerHTML = "";

    const card = document.createElement("article");
    card.className = "award-card";
    card.setAttribute("role", "region");
    card.setAttribute("aria-label", "Award " + (index + 1) + " of " + total);

    const glow = document.createElement("div");
    glow.className = "award-glow";
    glow.style.setProperty("--card-color", award.color || "#f5d78b");

    const top = document.createElement("div");
    top.className = "award-top";
    const number = document.createElement("span");
    number.className = "award-number";
    number.textContent = String(index + 1).padStart(2, "0");
    const emoji = document.createElement("span");
    emoji.className = "award-emoji";
    emoji.textContent = award.emoji || "✦";
    emoji.setAttribute("aria-hidden", "true");
    top.append(number, emoji);

    const title = document.createElement("h2");
    title.className = "award-title reveal";
    title.textContent = award.title;

    const winnerWrap = document.createElement("div");
    winnerWrap.className = "winner-reveal";
    winnerWrap.setAttribute("aria-hidden", "true");

    if (award.anniversary) {
      const badge = document.createElement("div");
      badge.className = "anniversary-badge";
      badge.innerHTML =
        '<span class="badge-dot" aria-hidden="true"></span>' +
        award.release_date + " \u2013 " + award.anniversary_date +
        '<span class="winner-emoji" style="margin-left:8px;font-size:1.1em;">' +
        (award.winners_emoji || "") + "</span>";
      winnerWrap.appendChild(badge);
    }

    const winnerName = document.createElement("h3");
    winnerName.className = "award-winner";
    winnerName.innerHTML =
      award.winners +
      '<span class="winner-emoji" aria-hidden="true">' +
      (award.winners_emoji || "") + "</span>";

    const tribute = document.createElement("p");
    tribute.className = "award-tribute";
    tribute.textContent = award.tribute;

    const medal = document.createElement("span");
    medal.className = "medal";
    medal.textContent = award.medal || "✦";
    medal.setAttribute("aria-hidden", "true");

    winnerWrap.append(winnerName, tribute, medal);
    card.append(glow, top, title, winnerWrap);
    awardStage.appendChild(card);

    // Update progress + hint
    if (progressCurrent) progressCurrent.textContent = index + 1;
    if (ceremonyHint) {
      ceremonyHint.textContent =
        index === total - 1
          ? "Final award — tap Next Award to reach the finale."
          : "Tap Next Award to reveal the next legend.";
    }

    // Button states
    if (prevButton) prevButton.disabled = index === 0;
    if (nextButton) {
      nextButton.disabled = false;
      nextButton.textContent =
        index === total - 1 ? "Go to Finale \u2192" : "Next Award \u2192";
    }

    // Animate title in, then reveal winner content
    const titleDelay = isReduced() ? 0 : 700;
    const revealWinner = async () => {
      card.classList.add("glowing");
      winnerWrap.removeAttribute("aria-hidden");
      winnerWrap.classList.add("revealed");
      await delay(isReduced() ? 0 : 400);
      spawnSparkles(card, 10);
    };

    // Restart animation classes cleanly
    title.classList.remove("reveal");
    void title.offsetHeight; // force reflow
    title.classList.add("reveal");

    setTimeout(revealWinner, titleDelay);
  }

  function renderFinale() {
    if (finaleMessage) finaleMessage.textContent = CEREMONY_FINALE_MESSAGE || "";
    if (disclaimerText) disclaimerText.textContent = CEREMONY_DISCLAIMER || "";

    finaleWinners.innerHTML = "";
    awards.forEach((award) => {
      const item = document.createElement("article");
      item.className = "final-winner";
      const medal = award.medal || "✦";
      item.innerHTML =
        '<span class="win-medal" aria-hidden="true">' + medal + "</span>" +
        '<p class="win-title">' + escapeHtml(award.title) + "</p>" +
        '<p class="win-name">' + escapeHtml(award.winners) + "</p>";
      finaleWinners.appendChild(item);
    });

    spawnConfetti(44);
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  // ------------------------------------------------------------------ Navigation
  function showWelcome() {
    welcomeScreen.classList.remove("hidden");
    ceremonyScreen.classList.add("hidden");
    finaleScreen.classList.add("hidden");
    currentIndex = 0;
    focusElement(beginButton);
    spawnSparkles(welcomeScreen, 6);
  }

  function showCeremony(index) {
    if (index < 0) index = 0;
    if (index >= total) index = total - 1;
    currentIndex = index;
    welcomeScreen.classList.add("hidden");
    ceremonyScreen.classList.remove("hidden");
    finaleScreen.classList.add("hidden");
    renderAward(currentIndex);
    // Focus the primary forward control
    setTimeout(() => focusElement(nextButton), 50);
  }

  function showFinale() {
    welcomeScreen.classList.add("hidden");
    ceremonyScreen.classList.add("hidden");
    finaleScreen.classList.remove("hidden");
    renderFinale();
    focusElement(replayButton);
  }

  // ------------------------------------------------------------------ Copy summary
  function buildSummary() {
    const lines = [];
    lines.push("CookieVerse Eternal Ceremony \u2014 Fan Awards Summary");
    lines.push("================================================");
    lines.push("");
    awards.forEach((award, i) => {
      lines.push(
        (i + 1) +
        ". " +
        award.title +
        " \u2014 " +
        award.winners +
        (award.anniversary ? " (" + award.release_date + " \u2013 " + award.anniversary_date + ")" : "")
      );
    });
    lines.push("");
    lines.push("Finale message:");
    lines.push(CEREMONY_FINALE_MESSAGE || "");
    lines.push("");
    lines.push(CEREMONY_DISCLAIMER || "");
    return lines.join("\n");
  }

  async function copySummary() {
    const text = buildSummary();
    try {
      await navigator.clipboard.writeText(text);
      showToast("Ceremony summary copied!", "copied");
    } catch (err) {
      // Fallback for older browsers
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "absolute";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand("copy");
        showToast("Ceremony summary copied!", "copied");
      } catch (e) {
        showToast("Could not copy summary.", null);
      } finally {
        ta.remove();
      }
    }
  }

  // ------------------------------------------------------------------ Live date (Asia/Kolkata label only)
  function updateLiveDate() {
    if (!liveDate) return;
    liveDate.textContent = CEREMONY_NOW || "";
  }

  // ------------------------------------------------------------------ Event listeners
  beginButton.addEventListener("click", () => showCeremony(0));

  prevButton.addEventListener("click", () => {
    if (currentIndex > 0) showCeremony(currentIndex - 1);
  });

  nextButton.addEventListener("click", () => {
    if (currentIndex >= total - 1) {
      showFinale();
    } else {
      showCeremony(currentIndex + 1);
    }
  });

  skipFinaleButton.addEventListener("click", () => {
    showFinale();
  });

  copyButton.addEventListener("click", copySummary);

  replayButton.addEventListener("click", () => {
    showWelcome();
  });

  copyFinaleButton.addEventListener("click", copySummary);

  // ------------------------------------------------------------------ Init
  updateLiveDate();
  showWelcome();
})();
