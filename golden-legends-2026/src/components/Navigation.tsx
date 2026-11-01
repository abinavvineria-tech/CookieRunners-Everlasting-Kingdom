import { useState, useCallback } from 'react';
import { Menu, X, Award } from 'lucide-react';
import { navLinks } from '../data/navigation';

export default function Navigation() {
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleNav = useCallback((href: string) => {
    setMobileOpen(false);
    const el = document.querySelector(href);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, []);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass-card border-b-0 rounded-none bg-deep-blue/80 backdrop-blur-xl border-b border-gold/10">
      <div className="max-w-6xl mx-auto px-5 h-16 flex items-center justify-between">
        <a
          href="#"
          onClick={(e) => { e.preventDefault(); handleNav('#ceremony'); }}
          className="flex items-center gap-2.5 text-champagne hover:text-gold transition-colors"
        >
          <Award className="w-6 h-6 text-gold" strokeWidth={2} />
          <span className="font-display font-bold text-base tracking-wide hidden sm:inline">
            Golden Legends 2026
          </span>
          <span className="font-display font-bold text-base tracking-wide sm:hidden">
            GL 2026
          </span>
        </a>

        {/* Desktop links */}
        <div className="hidden md:flex items-center gap-1">
          {navLinks.map((link) => (
            <a
              key={link.sectionId}
              href={link.href}
              onClick={(e) => { e.preventDefault(); handleNav(link.href); }}
              className="px-3.5 py-2 rounded-lg text-sm font-medium text-ivory/70 hover:text-champagne hover:bg-white/5 transition-all tracking-wide"
            >
              {link.label}
            </a>
          ))}
        </div>

        {/* Mobile toggle */}
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="md:hidden p-2 rounded-xl text-ivory hover:bg-white/5 transition-colors"
          aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
        >
          {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile panel */}
      <div
        className={`md:hidden overflow-hidden transition-all duration-300 ease-in-out ${
          mobileOpen ? 'max-h-80 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="px-5 pb-5 pt-1 flex flex-col gap-1 border-t border-white/5">
          {navLinks.map((link) => (
            <a
              key={link.sectionId}
              href={link.href}
              onClick={(e) => { e.preventDefault(); handleNav(link.href); }}
              className="px-4 py-3 rounded-xl text-sm font-medium text-ivory/80 hover:text-champagne hover:bg-white/5 transition-all tracking-wide"
            >
              {link.label}
            </a>
          ))}
        </div>
      </div>
    </nav>
  );
}
