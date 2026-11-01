import { useState, useMemo } from 'react';
import { Trophy, Search, Filter } from 'lucide-react';
import { mainAwards } from '../data/awards';

export default function MainAwards() {
  const [filterText, setFilterText] = useState('');
  const [selectedWinner, setSelectedWinner] = useState<string | null>(null);

  const filtered = useMemo(() => {
    const q = filterText.toLowerCase();
    return mainAwards.filter(
      (a) =>
        a.title.toLowerCase().includes(q) ||
        a.winner.name.toLowerCase().includes(q) ||
        a.description.toLowerCase().includes(q)
    );
  }, [filterText]);

  return (
    <section id="awards" className="relative py-24 md:py-36">
      <div className="max-w-6xl mx-auto px-5 md:px-8">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-gold/10 border border-gold/20 text-champagne-soft text-xs font-medium tracking-wider uppercase mb-6">
            <Trophy className="w-3.5 h-3.5" /> Main Awards
          </div>
          <h2 className="font-display text-4xl md:text-6xl font-bold text-ivory leading-tight mb-4">
            The Golden <span className="gold-gradient-text">Categories</span>
          </h2>
          <p className="text-ivory/50 font-editorial italic max-w-lg mx-auto">
            Three legendary awards. Three unforgettable stories. One kingdom that never forgets.
          </p>
        </div>

        {/* Search */}
        <div className="max-w-md mx-auto mb-12 relative">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-ivory/30" />
          <input
            type="text"
            placeholder="Search awards or winners..."
            value={filterText}
            onChange={(e) => setFilterText(e.target.value)}
            className="w-full pl-10 pr-4 py-3 rounded-2xl bg-deep-blue-light/60 border border-white/5 text-ivory placeholder:text-ivory/30 focus:outline-none focus:border-gold/30 focus:ring-1 focus:ring-gold/10 transition-all text-sm"
          />
        </div>

        {/* Awards grid */}
        <div className="grid md:grid-cols-3 gap-6">
          {filtered.length === 0 && (
            <div className="md:col-span-3 text-center py-12 text-ivory/30 font-editorial italic text-lg">
              No awards match your search. Try a different word.
            </div>
          )}
          {filtered.map((award) => (
            <article
              key={award.id}
              className="glass-card glass-card-hover rounded-3xl overflow-hidden transition-all duration-300 group"
            >
              <div className="p-6 md:p-8 flex flex-col h-full">
                <div className="flex items-start justify-between mb-5">
                  <span className="text-[10px] font-semibold tracking-[0.2em] uppercase text-gold-dim">
                    {award.tag}
                  </span>
                  <span className="text-xs text-ivory/20 font-editorial">{award.subtitle}</span>
                </div>

                <h3 className="font-display text-xl md:text-2xl font-bold text-champagne leading-snug mb-3 group-hover:text-gold transition-colors">
                  {award.title}
                </h3>
                <p className="text-sm text-ivory/60 leading-relaxed mb-6 font-editorial italic flex-grow">
                  {award.description}
                </p>

                <div className="gold-divider mb-5" />

                <button
                  onClick={() => setSelectedWinner(selectedWinner === award.winner.id ? null : award.winner.id)}
                  className="w-full text-left"
                >
                  <div className="flex items-center gap-4 p-4 rounded-2xl bg-white/[0.02] hover:bg-white/[0.06] border border-white/5 hover:border-gold/10 transition-all">
                    <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-gold/20 to-deep-blue flex items-center justify-center shrink-0 overflow-hidden border border-gold/10">
                      <span className="text-xl font-display font-bold text-gold/80">
                        {award.winner.name.split(' ')[0]?.[0] || 'C'}
                      </span>
                    </div>
                    <div className="min-w-0">
                      <h4 className="font-display font-semibold text-ivory text-base truncate">
                        {award.winner.name}
                      </h4>
                      <p className="text-xs text-champagne-soft">{award.winner.role}</p>
                    </div>
                  </div>
                </button>

                {/* Expanded detail */}
                <div
                  className={`overflow-hidden transition-all duration-300 ease-in-out ${
                    selectedWinner === award.winner.id ? 'max-h-64 opacity-100 mt-4' : 'max-h-0 opacity-0 mt-0'
                  }`}
                >
                  <div className="p-4 rounded-2xl bg-deep-blue-light border border-gold/10">
                    <p className="text-xs text-ivory/40 mb-2 font-editorial">Recognition</p>
                    <p className="text-sm text-ivory/80 font-editorial leading-relaxed">
                      {award.winner.recognition}
                    </p>
                    <p className="text-xs text-ivory/30 mt-3 font-editorial italic">
                      {award.winner.artworkPlaceholder}
                    </p>
                  </div>
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
