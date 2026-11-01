// EverLink SSH — vanilla JavaScript (no build step)

document.addEventListener("DOMContentLoaded", () => {
  // Confirm destructive actions on delete forms
  document.querySelectorAll("form[action*='/delete']").forEach((form) => {
    form.addEventListener("submit", (event) => {
      const btn = event.submitter;
      const name = btn ? btn.getAttribute("data-name") : null;
      const message = name
        ? `Delete profile "${name}"?`
        : "Are you sure you want to delete this profile?";
      if (!confirm(message)) {
        event.preventDefault();
      }
    });
  });

  // Auto-hide flash messages after 8 seconds
  setTimeout(() => {
    document.querySelectorAll(".flash").forEach((el) => {
      el.style.transition = "opacity 0.4s ease";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 400);
    });
  }, 8000);

  // Enhance connect buttons with a working-state label
  document.querySelectorAll("form[action*='/connect']").forEach((form) => {
    form.addEventListener("submit", () => {
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.textContent = "Connecting…";
        btn.disabled = true;
      }
    });
  });
});
