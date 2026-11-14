/* ======================================================================
   Cookie Runners Everlasting Kingdom — Landing Page Interactivity
   ======================================================================
   - Theme switcher (dark/light) with persisted preference
   - Animated nav bar on scroll
   - Mobile navigation menu
   - Smooth scrolling + active section highlighting
   - Scroll-reveal animations (respects prefers-reduced-motion)
   - Live GitHub repository statistics (public API, no tokens)
   - Back-to-top button
   - Toast notifications
   ====================================================================== */

(function () {
  'use strict';

  // ------------------------------------------------------------------
  // Selectors
  // ------------------------------------------------------------------
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');
  const navLinks = document.querySelectorAll('.nav-link');
  const topbar = document.querySelector('.topbar');
  const themeTrigger = document.getElementById('themeTrigger');
  const backToTop = document.getElementById('backToTop');

  const statStars = document.getElementById('statStars');
  const statForks = document.getElementById('statForks');
  const statIssues = document.getElementById('statIssues');
  const statContributors = document.getElementById('statContributors');

  const repoStars = document.getElementById('repoStars');
  const repoForks = document.getElementById('repoForks');
  const repoIssues = document.getElementById('repoIssues');
  const repoRelease = document.getElementById('repoRelease');
  const repoLicense = document.getElementById('repoLicense');
  const updatesList = document.getElementById('repoUpdates');
  const contributorsList = document.getElementById('contributorsList');
  const contributorsNote = document.getElementById('contributorsNote');

  const REPO_OWNER = 'abinavvineria-tech';
  const REPO_NAME = 'CookieRunners-Everlasting-Kingdom';

  // ------------------------------------------------------------------
  // Theme
  // ------------------------------------------------------------------
  const THEME_KEY = 'crk-theme';
  const savedTheme = localStorage.getItem(THEME_KEY);
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light');

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
    if (themeTrigger) themeTrigger.textContent = theme === 'dark' ? '🌙' : '☀️';
  }

  applyTheme(initialTheme);

  if (themeTrigger) {
    themeTrigger.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      applyTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  // ------------------------------------------------------------------
  // Toast
  // ------------------------------------------------------------------
  function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast show';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 450);
    }, 3000);
  }

  // ------------------------------------------------------------------
  // Nav: scroll effect + mobile menu + active link
  // ------------------------------------------------------------------
  function onScroll() {
    const y = window.scrollY;
    if (topbar) {
      if (y > 20) {
        topbar.style.padding = '0 clamp(18px, 5vw, 60px)';
        topbar.style.boxShadow = '0 8px 24px -10px rgba(0,0,0,0.45)';
      } else {
        topbar.style.padding = '0 clamp(18px, 5vw, 60px)';
        topbar.style.boxShadow = 'none';
      }
    }
    if (backToTop) {
      if (y > 400) backToTop.classList.add('visible');
      else backToTop.classList.remove('visible');
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (backToTop) {
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Mobile toggle
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      const open = navMenu.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', open);
    });

    // Close mobile menu on link click
    navLinks.forEach((link) => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Active section highlighting via IntersectionObserver
  const sections = document.querySelectorAll('section[id]');
  const observerOptions = { root: null, rootMargin: '-10% 0% -60% 0%', threshold: 0.1 };
  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navLinks.forEach((link) => {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + id) {
            link.classList.add('active');
          }
        });
      }
    });
  }, observerOptions);
  sections.forEach((sec) => sectionObserver.observe(sec));

  // ------------------------------------------------------------------
  // Scroll reveal
  // ------------------------------------------------------------------
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealEls = document.querySelectorAll(
    '.feature-card, .showcase-card, .tech-item, .update-card, .faq-item, .contributor-card, .link-card, .glass-card'
  );

  function reveal() {
    if (reduceMotion) {
      revealEls.forEach((el) => (el.style.opacity = '1'));
      return;
    }
    const triggerBottom = window.innerHeight * 0.88;
    revealEls.forEach((el) => {
      const top = el.getBoundingClientRect().top;
      if (top < triggerBottom) {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      }
    });
  }

  revealEls.forEach((el) => {
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    el.style.opacity = '0';
    el.style.transform = 'translateY(24px)';
  });

  window.addEventListener('scroll', reveal, { passive: true });
  window.addEventListener('load', reveal);
  reveal();

  // ------------------------------------------------------------------
  // GitHub API: repository statistics (public, no token)
  // ------------------------------------------------------------------
  async function fetchRepoStats() {
    async function getJSON(path) {
      try {
        const res = await fetch(`https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}${path}`, {
          headers: { Accept: 'application/vnd.github+json' },
        });
        if (!res.ok) return null;
        return await res.json();
      } catch (err) {
        console.warn('GitHub API fetch failed:', path, err);
        return null;
      }
    }

    const [repo, contributors, releases] = await Promise.all([
      getJSON(''),
      getJSON('/contributors?per_page=100'),
      getJSON('/releases?per_page=5'),
    ]);

    // Repository stats card (hero + updates)
    if (repo) {
      const set = (el, val) => { if (el) el.textContent = val; };
      set(statStars, repo.stargazers_count?.toLocaleString() || '—');
      set(statForks, repo.forks_count?.toLocaleString() || '—');
      set(statIssues, repo.open_issues_count?.toLocaleString() || '—');
      set(statContributors, (contributors && contributors.length) || 1);
      set(repoStars, repo.stargazers_count?.toLocaleString() || '—');
      set(repoForks, repo.forks_count?.toLocaleString() || '—');
      set(repoIssues, repo.open_issues_count?.toLocaleString() || '—');

      if (repoRelease) {
        if (releases && releases.length > 0) {
          const latest = releases[0];
          const published = latest.published_at ? new Date(latest.published_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' }) : '—';
          repoRelease.innerHTML = `<strong>${latest.tag_name || latest.name}</strong> · ${published}`;
        } else {
          repoRelease.textContent = 'No releases yet';
        }
      }

      if (repoLicense) {
        if (repo.license) {
          repoLicense.innerHTML = `<a href="${repo.license.html_url}" target="_blank" rel="noopener" style="color:var(--gold);">${repo.license.spdx_id || repo.license.name}</a>`;
        } else {
          repoLicense.textContent = 'None detected';
        }
      }
    }

    // Contributors
    if (contributorsList && contributors && contributors.length) {
      contributorsList.innerHTML = '';
      contributors.forEach((c) => {
        const card = document.createElement('article');
        card.className = 'contributor-card glass-card';
        card.innerHTML = `
          <img class="contributor-avatar" src="${c.avatar_url}" alt="${c.login}" width="64" height="64">
          <div class="contributor-info">
            <h3>${c.login}</h3>
            <p class="contributor-login">@${c.login}</p>
            <p class="contributor-contrib">${c.contributions} contribution${c.contributions !== 1 ? 's' : ''}</p>
          </div>
          <a class="contributor-link" href="${c.html_url}" target="_blank" rel="noopener">Profile →</a>
        `;
        contributorsList.appendChild(card);
      });
      if (contributorsNote) {
        contributorsNote.textContent = `Contributor data fetched live from GitHub. Repository currently has ${contributors.length} contributor${contributors.length !== 1 ? 's' : ''}.`;
      }
    }

    // Recent activity (use repo pushed_at as latest update, plus releases as events)
    if (updatesList && repo) {
      updatesList.innerHTML = '';
      const entries = [];

      if (releases && releases.length > 0) {
        releases.slice(0, 3).forEach((r) => {
          entries.push({
            actor: 'Cookie Runners',
            title: `Release ${r.tag_name || r.name}`,
            body: r.body ? r.body.split('\n')[0].slice(0, 120) : 'A new release is available.',
            time: r.published_at,
            html: r.html_url,
          });
        });
      }

      if (repo.pushed_at) {
        entries.unshift({
          actor: 'Cookie Runners',
          title: 'Repository updated',
          body: `Last push on ${new Date(repo.pushed_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}`,
          time: repo.pushed_at,
          html: `https://github.com/${REPO_OWNER}/${REPO_NAME}/commits/${repo.default_branch || 'main'}`,
        });
      }

      if (entries.length === 0) {
        updatesList.innerHTML = '<div class="update-empty"><span>✦</span>No recent activity to display.</div>';
        return;
      }

      entries.forEach((e) => {
        const card = document.createElement('article');
        card.className = 'update-card';
        const timeStr = e.time ? new Date(e.time).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' }) : '—';
        card.innerHTML = `
          <div class="update-avatar">✦</div>
          <div class="update-info">
            <h4>${e.title}</h4>
            <p>${e.body}</p>
            <time>${timeStr}</time>
          </div>
        `;
        card.addEventListener('click', () => { if (e.html) window.open(e.html, '_blank'); });
        card.style.cursor = 'pointer';
        updatesList.appendChild(card);
      });
    }
  }

  fetchRepoStats();

  // ------------------------------------------------------------------
  // Loading animation: fade out once hydrated
  // ------------------------------------------------------------------
  window.addEventListener('load', () => {
    document.body.classList.add('loaded');
  });
})();
