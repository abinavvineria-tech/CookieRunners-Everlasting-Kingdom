// CookieVerse: Memory Oven — SQLite-backed CRUD
(function () {
  'use strict';

  const form = document.getElementById('memory-form');
  const list = document.getElementById('memories-list');
  const empty = document.getElementById('memories-empty');
  const loading = document.getElementById('memories-loading');
  const errorEl = document.getElementById('memory-error');
  const successEl = document.getElementById('memory-success');

  if (!form || !list) return;

  function showLoading(show) {
    if (loading) loading.style.display = show ? 'block' : 'none';
  }
  function showEmpty(show) {
    if (empty) empty.style.display = show ? 'block' : 'none';
    if (list) list.style.display = show ? 'none' : 'grid';
  }
  function showMsg(el, show, text) {
    if (!el) return;
    el.style.display = show ? 'block' : 'none';
    if (text) el.textContent = text;
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  async function loadMemories() {
    showLoading(true);
    showMsg(errorEl, false);
    try {
      const res = await window.cvFetch('/api/memories');
      if (!res.ok) throw new Error('Failed to load memories');
      const memories = await res.json();
      render(memories);
    } catch (err) {
      showMsg(errorEl, true, 'Could not load memories: ' + escapeHtml(err.message));
    } finally {
      showLoading(false);
    }
  }

  function render(memories) {
    list.innerHTML = '';
    if (!memories || memories.length === 0) {
      showEmpty(true);
      return;
    }
    showEmpty(false);
    memories.forEach(function (m) {
      const card = document.createElement('div');
      card.className = 'memory-card';
      card.innerHTML =
        '<h3>' + escapeHtml(m.title || 'Untitled Memory') + '</h3>' +
        '<p>' + escapeHtml(m.content) + '</p>' +
        (m.favorite_cookie ? '<p><strong>Favorite Cookie:</strong> ' + escapeHtml(m.favorite_cookie) + '</p>' : '') +
        '<div class="memory-meta">Baked ' + relativeTime(m.created_at) + '</div>' +
        '<div class="memory-actions">' +
        '<button type="button" class="btn btn--ghost btn--sm" data-id="' + m.id + '">Delete</button>' +
        '</div>';
      list.appendChild(card);
    });

    list.querySelectorAll('button[data-id]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const id = parseInt(this.getAttribute('data-id'), 10);
        if (confirm('Delete this memory? This cannot be undone.')) {
          deleteMemory(id);
        }
      });
    });
  }

  async function deleteMemory(id) {
    try {
      const res = await window.cvFetch('/api/memories/' + id, { method: 'DELETE' });
      if (!res.ok) throw new Error('Delete failed');
      loadMemories();
      showMsg(successEl, true, 'Memory deleted.');
      setTimeout(function () { showMsg(successEl, false); }, 2500);
    } catch (err) {
      showMsg(errorEl, true, 'Delete failed: ' + escapeHtml(err.message));
    }
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    showMsg(errorEl, false);
    showMsg(successEl, false);

    const title = document.getElementById('memory-title').value.trim();
    const content = document.getElementById('memory-content').value.trim();
    const favorite = document.getElementById('memory-favorite-cookie').value.trim();

    if (!content) {
      showMsg(errorEl, true, 'Please write a memory before baking.');
      return;
    }

    try {
      const res = await window.cvFetch('/api/memories', {
        method: 'POST',
        body: { title, content, favorite_cookie: favorite }
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || 'Failed to save memory');
      }
      form.reset();
      showMsg(successEl, true, 'Memory baked and saved!');
      setTimeout(function () { showMsg(successEl, false); }, 2500);
      loadMemories();
    } catch (err) {
      showMsg(errorEl, true, 'Save failed: ' + escapeHtml(err.message));
    }
  });

  // relative time helper
  function relativeTime(iso) {
    if (!iso) return 'just now';
    const d = new Date(iso);
    const now = new Date();
    const sec = Math.floor((now - d) / 1000);
    if (sec < 60) return 'just now';
    const min = Math.floor(sec / 60);
    if (min < 60) return min + ' minute(s) ago';
    const h = Math.floor(min / 60);
    if (h < 24) return h + ' hour(s) ago';
    return d.toLocaleDateString();
  }

  loadMemories();
})();
