import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'

const divisions = [
  { number: '01', name: 'CookieVerse Central', slug: 'central', label: 'Command centre', icon: '✦', description: 'Your gateway to every realm, milestone and announcement.', detail: 'Review the project pulse, roadmap and latest transmission from one command centre.' },
  { number: '02', name: 'CookieVerse Games', slug: 'games', label: 'Explore & play', icon: '◈', description: 'Original fantasy worlds, quests, characters and stories.', detail: 'Game concepts, kingdom exploration and interactive stories are planned for Phase 3.' },
  { number: '03', name: 'CookieVerse Intelligence', slug: 'intelligence', label: 'AI & technology', icon: '⌁', description: 'Hermes, Telegram and knowledge systems for the universe.', detail: 'Hermes, Telegram and knowledge retrieval will be connected after credentialed backend setup.' },
  { number: '04', name: 'CookieVerse Community', slug: 'community', label: 'Gather together', icon: '♢', description: 'Events, achievements and a home for every fan.', detail: 'Community profiles, events and competitions are planned for Phase 4.' },
  { number: '05', name: 'CookieVerse Archives', slug: 'archives', label: 'Remember & discover', icon: '▱', description: 'An evolving encyclopedia, timeline and memory vault.', detail: 'The encyclopedia, timeline and announcement archive will grow during the Exploration phase.' },
]

const milestones = [
  ['Foundation', 'Central homepage and visual identity', 'Active'],
  ['Intelligence', 'Hermes and Telegram integration', 'Planned'],
  ['Exploration', 'Game concepts and lore systems', 'Planned'],
]

function App() {
  const [active, setActive] = useState(() => getDivisionFromHash())
  const [menuOpen, setMenuOpen] = useState(false)
  const [notice, setNotice] = useState('')

  function getDivisionFromHash() {
    const slug = window.location.hash.replace('#/', '') || 'central'
    return divisions.find((division) => division.slug === slug)?.name || 'CookieVerse Central'
  }

  function navigate(name, destination = null) {
    const division = divisions.find((item) => item.name === name)
    const hash = destination || `#/${division?.slug || 'central'}`
    window.history.pushState({}, '', hash)
    setActive(name)
    setMenuOpen(false)
    setNotice(name === 'CookieVerse Central' ? '' : `${name} opened. This division is currently in planning.`)
    requestAnimationFrame(() => document.getElementById('division-detail')?.scrollIntoView({ behavior: 'smooth', block: 'start' }))
  }

  React.useEffect(() => {
    const handleHashChange = () => setActive(getDivisionFromHash())
    window.addEventListener('popstate', handleHashChange)
    window.addEventListener('hashchange', handleHashChange)
    return () => {
      window.removeEventListener('popstate', handleHashChange)
      window.removeEventListener('hashchange', handleHashChange)
    }
  }, [])

  const activeDivision = divisions.find((division) => division.name === active) || divisions[0]

  function enterUniverse() {
    if (active !== 'CookieVerse Central') navigate('CookieVerse Central')
    requestAnimationFrame(() => document.getElementById('divisions')?.scrollIntoView({ behavior: 'smooth' }))
  }

  function showStatus() {
    setNotice('Project status: Phase 1 — Foundation, 20% complete.')
    document.getElementById('project-pulse')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  return (
    <div className="app-shell">
      <div className="stars" aria-hidden="true" />
      <header className="topbar">
        <button className="brand" onClick={() => navigate('CookieVerse Central')} aria-label="Go to CookieVerse Central">
          <span className="brand-mark">∞</span>
          <span><strong>COOKIEVERSE</strong><small>INFINITY</small></span>
        </button>
        <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)} aria-expanded={menuOpen} aria-controls="main-navigation" aria-label={menuOpen ? 'Close navigation menu' : 'Open navigation menu'}>☰</button>
        <nav id="main-navigation" className={menuOpen ? 'nav open' : 'nav'} aria-label="Main navigation">
          {divisions.map((division) => <button className={active === division.name ? 'nav-active' : ''} key={division.slug} onClick={() => navigate(division.name)}>{division.name.replace('CookieVerse ', '')}</button>)}
        </nav>
        <div className="status-pill"><span /> INFINITY ONLINE</div>
      </header>

      <main>
        <section className="hero">
          <div className="hero-copy">
            <p className="eyebrow">✧ ESTABLISHED 2026 · UNOFFICIAL FAN-MADE PROJECT</p>
            <h1>A universe<br /><em>without boundaries.</em></h1>
            <p className="hero-text">Welcome back, <strong>Captain Abinav.</strong> CookieVerse Infinity is an independent fantasy universe where imagination, community and technology run as one.</p>
            <div className="hero-actions"><button className="primary" onClick={enterUniverse}>Enter the universe <span>→</span></button><button className="text-button" onClick={showStatus}>View project status <span>↗</span></button></div>
          </div>
          <div className="hero-orbit" aria-hidden="true"><div className="orbit orbit-one" /><div className="orbit orbit-two" /><div className="crystal">✦</div><span className="orbit-dot dot-one" /><span className="orbit-dot dot-two" /><span className="orbit-dot dot-three" /></div>
        </section>

        <section className="stats" aria-label="Project statistics"><div><strong>05</strong><span>Core divisions</span></div><div><strong>∞</strong><span>Stories to discover</span></div><div><strong>01</strong><span>United vision</span></div><div className="motto"><span>ONE RUN.</span><span>ONE DREAM.</span><span>ONE UNITED.</span></div></section>

        <section id="divisions" className="section"><div className="section-heading"><div><p className="eyebrow">THE REALMS OF INFINITY</p><h2>Choose your <em>path.</em></h2></div><p>Five connected divisions. One shared universe.<br />Every journey begins at the Central.</p></div><div className="division-grid">{divisions.map((division) => <button className={active === division.name ? 'division-card selected' : 'division-card'} key={division.number} onClick={() => navigate(division.name)}><span className="card-number">{division.number}</span><span className="card-icon">{division.icon}</span><span className="card-label">{division.label}</span><h3>{division.name}</h3><p>{division.description}</p><span className="card-arrow">↗</span></button>)}</div></section>
        <section id="division-detail" className="division-detail section" aria-live="polite"><div><p className="eyebrow">ACTIVE DIVISION · {activeDivision.number}</p><h2>{activeDivision.name}</h2><p>{activeDivision.detail}</p></div>{activeDivision.slug === 'central' ? <button className="secondary" onClick={showStatus}>Open project status <span>→</span></button> : <span className="planned-badge">PLANNED FEATURE</span>}</section>

        <section id="project-pulse" className="dashboard-section section"><div className="section-heading"><div><p className="eyebrow">CENTRAL COMMAND</p><h2>Project <em>pulse.</em></h2></div><span className="live-label"><i /> LIVE OVERVIEW</span></div><div className="dashboard-grid"><article className="panel progress-panel"><div className="panel-top"><span>DEVELOPMENT STATUS</span><strong>PHASE 01 <small>/ 05</small></strong></div><h3>The foundation is being laid.</h3><p>CookieVerse Central is taking shape. The gateway to the universe is open.</p><div className="progress-track"><span /></div><div className="progress-meta"><span>Foundation</span><span>20% complete</span></div></article><article className="panel announcement"><div className="panel-top"><span>LATEST TRANSMISSION</span><span>21 NOV 2026</span></div><div className="seal">✦</div><h3>Welcome to Infinity.</h3><p>The first chapter begins now. A fan-made universe built with creativity, care and Cookie Run spirit.</p><button onClick={() => navigate('CookieVerse Archives')}>Read announcement <span>→</span></button></article><article className="panel milestones"><div className="panel-top"><span>ROADMAP</span><span>2026 — 2027</span></div>{milestones.map(([title, detail, status]) => <div className="milestone" key={title}><span className={status === 'Active' ? 'milestone-dot active' : 'milestone-dot'} /> <div><strong>{title}</strong><small>{detail}</small></div><em>{status}</em></div>)}</article></div></section>
      </main>
      <footer><span>COOKIEVERSE INFINITY <b>∞</b></span><span>A fan-made project by Captain Abinav</span><span>ONE RUN. ONE DREAM. ONE UNITED. 🌸</span></footer>
      {notice && <button className="toast" onClick={() => setNotice('')} aria-label="Dismiss notification">✦ {notice} <b>×</b></button>}
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
