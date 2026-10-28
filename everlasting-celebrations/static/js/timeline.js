// CookieVerse: Anniversary Timeline — verified vs fan-created entries
(function () {
  'use strict';

  const list = document.getElementById('timeline-list');
  const empty = document.getElementById('timeline-empty');
  if (!list) return;

  // Seed data: verified = community-documented reference dates; fan = unofficial creations.
  const entries = [
    {
      year: '2016',
      title: 'Cookie Run: OvenBreak launches',
      desc: 'OvenBreak debuts with run-based gameplay, cookies, and jelly.',
      type: 'verified',
      typeLabel: 'Community reference'
    },
    {
      year: '2017',
      title: 'First anniversary events',
      desc: 'Early anniversary celebrations introduce limited-time cookies and jellies.',
      type: 'fan',
      typeLabel: 'Fan-created'
    },
    {
      year: '2018',
      title: 'New cookie batches arrive',
      desc: 'More legendary and ancient heroes join the roster.',
      type: 'verified',
      typeLabel: 'Community reference'
    },
    {
      year: '2019',
      title: 'Community milestones grow',
      desc: 'Fan events, art, and community runs flourish worldwide.',
      type: 'fan',
      typeLabel: 'Fan-created'
    },
    {
      year: '2020',
      title: 'Expanding the Oven',
      desc: 'New game modes and seasonal events keep runners racing.',
      type: 'verified',
      typeLabel: 'Community reference'
    },
    {
      year: '2021',
      title: 'Kingdom era expands',
      desc: 'Cookie Run: Kingdom brings kingdom-building to the franchise.',
      type: 'verified',
      typeLabel: 'Community reference'
    },
    {
      year: '2022',
      title: 'Fan celebration year',
      desc: 'Community-organized anniversary gatherings across regions.',
      type: 'fan',
      typeLabel: 'Fan-created'
    },
    {
      year: '2023',
      title: 'New legends & beasts',
      desc: 'Ancient heroes and beasts enrich the Cookie Run lore.',
      type: 'verified',
      typeLabel: 'Community reference'
    },
    {
      year: '2024',
      title: 'Community memories',
      desc: 'Runners share stories, friendships, and unforgettable runs.',
      type: 'fan',
      typeLabel: 'Fan-created'
    },
    {
      year: '2025',
      title: 'Approaching a decade',
      desc: 'The community prepares for the 10th anniversary milestone.',
      type: 'fan',
      typeLabel: 'Fan-created'
    },
    {
      year: '2026',
      title: '10th Anniversary (reference)',
      desc: 'October 27, 2026 marks ten years since OvenBreak launch — a fan-maintained reference date.',
      type: 'verified',
      typeLabel: 'Community reference'
    },
    {
      year: '2026',
      title: 'Everlasting Celebrations studio',
      desc: 'This fan project celebrates legends, memories, and milestones.',
      type: 'fan',
      typeLabel: 'Fan-created'
    }
  ];

  function render() {
    if (!entries || entries.length === 0) {
      if (empty) empty.style.display = 'block';
      if (list) list.style.display = 'none';
      return;
    }
    if (empty) empty.style.display = 'none';
    if (list) list.style.display = 'flex';

    list.innerHTML = '';
    entries.forEach(function (e) {
      const card = document.createElement('article');
      card.className = 'timeline-card ' + (e.type === 'fan' ? 'timeline-card--fan' : '');
      card.innerHTML =
        '<div class="timeline-meta">' +
        '<span class="timeline-year">' + escapeHtml(e.year) + '</span>' +
        '<span class="timeline-type">' + escapeHtml(e.typeLabel) + '</span>' +
        '</div>' +
        '<h3 class="timeline-title">' + escapeHtml(e.title) + '</h3>' +
        '<p class="timeline-desc">' + escapeHtml(e.desc) + '</p>';
      list.appendChild(card);
    });
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  render();
})();
