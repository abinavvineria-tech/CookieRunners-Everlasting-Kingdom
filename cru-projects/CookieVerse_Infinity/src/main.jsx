import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'

const divisions = [
  { number: '01', name: 'CookieVerse Central', label: 'Command centre', icon: '✦', description: 'Your gateway to every realm, milestone and announcement.' },
  { number: '02', name: 'CookieVerse Games', label: 'Explore & play', icon: '◈', description: 'Original fantasy worlds, quests, characters and stories.' },
  { number: '03', name: 'CookieVerse Intelligence', label: 'AI & technology', icon: '⌁', description: 'Hermes, Telegram and knowledge systems for the universe.' },
  { number: '04', name: 'CookieVerse Community', label: 'Gather together', icon: '♢', description: 'Events, achievements and a home for every fan.' },
  { number: '05', name: 'CookieVerse Archives', label: 'Remember & discover', icon: '▱', description: 'An evolving encyclopedia, timeline and memory vault.' },
]

const milestones = [
  ['Foundation', 'Central homepage and visual identity', 'Active'],
  ['Intelligence', 'Hermes and Telegram integration', 'Planned'],
  ['Exploration', 'Game concepts and lore systems', 'Planned'],
]

function App() {
  const [active, setActive] = useState('CookieVerse Central')
  const [menuOpen, setMenuOpen] = useState(false)
  const [notice, setNotice] = useState('')

  function navigate(name) {
    setActive(name)
    setMenuOpen(false)
    if (name !== 'CookieVerse Central') setNotice(`${name} is mapped for the next build phase.`)
    else setNotice('')
  }

  return (
    <div className="app-shell">
      <div className="stars" aria-hidden="true" />
      <header className="topbar">
        <button className="brand" onClick={() => navigate('CookieVerse Central')} aria-label="Go to CookieVerse Central">
          <span className="brand-mark">∞</span>
          <span><strong>COOKIEVERSE</strong><small>INFINITY</small></span>
        </button>
        <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)} aria-expanded={menuOpen}>☰</button>
        <nav className={menuOpen ? 'nav open' : 'nav'} aria-label="Main navigation">
          <button className="nav-active" onClick={() => navigate('CookieVerse Central')}>Central</button>
          <button onClick={() => navigate('CookieVerse Games')}>Games</button>
          <button onClick={() => navigate('CookieVerse Intelligence')}>Intelligence</button>
          <button onClick={() => navigate('CookieVerse Community')}>Community</button>
          <button onClick={() => navigate('CookieVerse Archives')}>Archives</button>
        </nav>
        <div className="status-pill"><span /> INFINITY ONLINE</div>
      </header>

      <main>
        <section className="hero">
          <div className="hero-copy">
            <p className="eyebrow">✧ ESTABLISHED 2026 · UNOFFICIAL FAN-MADE PROJECT</p>
            <h1>A universe<br /><em>without boundaries.</em></h1>
            <p className="hero-text">Welcome back, <strong>Captain Abinav.</strong> CookieVerse Infinity is an independent fantasy universe where imagination, community and technology run as one.</p>
            <div className="hero-actions"><button className="primary" onClick={() => document.getElementById('divisions').scrollIntoView({ behavior: 'smooth' })}>Enter the universe <span>→</span></button><button className="text-button" onClick={() => setNotice('Infinity is currently in Phase 1: Foundation.')}>View project status <span>↗</span></button></div>
          </div>
          <div className="hero-orbit" aria-hidden="true"><div className="orbit orbit-one" /><div className="orbit orbit-two" /><div className="crystal">✦</div><span className="orbit-dot dot-one" /><span className="orbit-dot dot-two" /><span className="orbit-dot dot-three" /></div>
        </section>

        <section className="stats" aria-label="Project statistics"><div><strong>05</strong><span>Core divisions</span></div><div><strong>∞</strong><span>Stories to discover</span></div><div><strong>01</strong><span>United vision</span></div><div className="motto"><span>ONE RUN.</span><span>ONE DREAM.</span><span>ONE UNITED.</span></div></section>

        <section id="divisions" className="section"><div className="section-heading"><div><p className="eyebrow">THE REALMS OF INFINITY</p><h2>Choose your <em>path.</em></h2></div><p>Five connected divisions. One shared universe.<br />Every journey begins at the Central.</p></div><div className="division-grid">{divisions.map((division) => <button className={active === division.name ? 'division-card selected' : 'division-card'} key={division.number} onClick={() => navigate(division.name)}><span className="card-number">{division.number}</span><span className="card-icon">{division.icon}</span><span className="card-label">{division.label}</span><h3>{division.name}</h3><p>{division.description}</p><span className="card-arrow">↗</span></button>)}</div></section>

        <section className="dashboard-section section"><div className="section-heading"><div><p className="eyebrow">CENTRAL COMMAND</p><h2>Project <em>pulse.</em></h2></div><span className="live-label"><i /> LIVE OVERVIEW</span></div><div className="dashboard-grid"><article className="panel progress-panel"><div className="panel-top"><span>DEVELOPMENT STATUS</span><strong>PHASE 01 <small>/ 05</small></strong></div><h3>The foundation is being laid.</h3><p>CookieVerse Central is taking shape. The gateway to the universe is open.</p><div className="progress-track"><span /></div><div className="progress-meta"><span>Foundation</span><span>20% complete</span></div></article><article className="panel announcement"><div className="panel-top"><span>LATEST TRANSMISSION</span><span>21 NOV 2026</span></div><div className="seal">✦</div><h3>Welcome to Infinity.</h3><p>The first chapter begins now. A fan-made universe built with creativity, care and Cookie Run spirit.</p><button onClick={() => setNotice('Announcement archive will be available in the Archives division.')}>Read announcement <span>→</span></button></article><article className="panel milestones"><div className="panel-top"><span>ROADMAP</span><span>2026 — 2027</span></div>{milestones.map(([title, detail, status]) => <div className="milestone" key={title}><span className={status === 'Active' ? 'milestone-dot active' : 'milestone-dot'} /> <div><strong>{title}</strong><small>{detail}</small></div><em>{status}</em></div>)}</article></div></section>
      </main>
      <footer><span>COOKIEVERSE INFINITY <b>∞</b></span><span>A fan-made project by Captain Abinav</span><span>ONE RUN. ONE DREAM. ONE UNITED. 🌸</span></footer>
      {notice && <button className="toast" onClick={() => setNotice('')} aria-label="Dismiss notification">✦ {notice} <b>×</b></button>}
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
