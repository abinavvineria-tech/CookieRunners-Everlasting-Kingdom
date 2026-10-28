// CookieVerse: Anniversary Countdown — user-selectable date + OvenBreak reference
(function () {
  'use strict';

  const form = document.getElementById('countdown-form');
  const display = document.getElementById('countdown-display');
  const message = document.getElementById('countdown-message');
  const result = document.getElementById('countdown-result');
  const refBtn = document.getElementById('ovenbreak-ref-btn');
  const refResult = document.getElementById('ovenbreak-ref-result');

  if (!form || !display) return;

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function fmt(n) { return String(n).padStart(2, '0'); }

  function renderResult(data) {
    result.style.display = 'block';
    let html = '';
    if (data.status === 'past') {
      html += '<p style="color:var(--jelly-red); font-weight:600;">' + escapeHtml(data.message) + '</p>';
      html += '<p style="font-size:0.9rem; color:var(--text-muted);">' + data.days_passed + ' day(s) have passed since ' + escapeHtml(data.target_date) + '.</p>';
    } else if (data.status === 'today') {
      html += '<p style="color:var(--gold-dark); font-weight:600;">' + escapeHtml(data.message) + '</p>';
    } else {
      html += '<div class="countdown-display" style="justify-content:center; font-size:1.5rem; gap:0.4rem;">';
      html += '<span>' + data.days + 'd</span> <span>' + data.hours + 'h</span> <span>' + data.minutes + 'm</span> <span>' + data.seconds + 's</span>';
      html += '</div>';
      html += '<p style="color:var(--text-secondary); font-weight:600; margin-top:0.5rem;">' + escapeHtml(data.message) + '</p>';
    }
    result.innerHTML = html;
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const target = document.getElementById('countdown-target').value.trim();
    if (!target) {
      message.textContent = 'Please pick a date.';
      return;
    }
    try {
      const res = await window.cvFetch('/api/countdown', {
        method: 'POST',
        body: { target_date: target }
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || 'Countdown failed');
      }
      const data = await res.json();
      renderResult(data);
      message.textContent = '';
    } catch (err) {
      message.textContent = 'Countdown error: ' + escapeHtml(err.message);
      message.style.color = 'var(--jelly-red)';
    }
  });

  // ---- OvenBreak reference countdown ----
  if (refBtn && refResult) {
    refBtn.addEventListener('click', async function () {
      try {
        const res = await window.cvFetch('/api/countdown/ovenbreak');
        if (!res.ok) throw new Error('Reference countdown failed');
        const data = await res.json();
        let html = '<h4 style="margin:0 0 0.5rem; color:var(--text-primary);">OvenBreak 10th Anniversary Reference</h4>';
        html += '<p style="font-size:0.85rem; color:var(--text-muted); margin:0 0 0.5rem;">' + escapeHtml(data.reference_date) + '</p>';
        html += '<p style="font-size:0.8rem; color:var(--text-muted); margin:0 0 0.75rem;"><strong>Note:</strong> ' + escapeHtml(data.label) + '</p>';
        if (data.status === 'future') {
          html += '<div class="countdown-display" style="justify-content:center; font-size:1.5rem; gap:0.4rem;">';
          html += '<span>' + data.days + 'd</span> <span>' + data.hours + 'h</span> <span>' + data.minutes + 'm</span> <span>' + data.seconds + 's</span>';
          html += '</div>';
        } else if (data.status === 'today') {
          html += '<p style="color:var(--gold-dark); font-weight:600;">' + escapeHtml(data.message) + '</p>';
        } else {
          html += '<p style="color:var(--jelly-red); font-weight:600;">' + escapeHtml(data.message) + '</p>';
        }
        refResult.innerHTML = html;
        refResult.style.display = 'block';
      } catch (err) {
        refResult.innerHTML = '<p style="color:var(--jelly-red);">Reference load failed: ' + escapeHtml(err.message) + '</p>';
        refResult.style.display = 'block';
      }
    });
  }

})();
