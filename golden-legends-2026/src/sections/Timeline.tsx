import { Clock, Sparkles } from 'lucide-react';
import { timelineEvents } from '../data/awards';

export default function Timeline() {
  return (
    <section id="timeline" className="relative py-24 md:py-36">
      <div className="max-w-4xl mx-auto px-5 md:px-8">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-violet-soft/10 border border-violet-soft/20 text-violet-soft text-xs font-medium tracking-wider uppercase mb-6">
            <Clock className="w-3.5 h-3.5" /> Timeline
          </div>
          <h2 className="font-display text-4xl md:text-6xl font-bold text-ivory leading-tight mb-4">
            Ceremony <span className="gold-gradient-text">Timeline</span>
          </h2>
          <p className="text-ivory/50 font-editorial italic max-w-md mx-auto">
            Every ceremony has its moments. These are the ones written in gold.
          </p>
        </div>

        <div className="relative">
          {/* Vertical gold line */}
          <div className="absolute left-[19px] md:left-1/2 md:-translate-x-px top-2 bottom-2 w-px bg-gradient-to-b from-transparent via-gold/40 to-transparent md:ml-0" />

          <div className="space-y-10">
            {timelineEvents.map((event, idx) => (
              <div
                key={event.date}
                className={`relative flex gap-6 md:gap-12 items-start ${
                  idx % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse md:text-right'
                }`}
              >
                {/* Date bubble */}
                <div className="hidden md:flex w-1/2 justify-end md:pr-8 md:justify-end md:pr-8">
                  <div className={`glass-card rounded-2xl px-5 py-4 max-w-xs border-gold/10 ${idx % 2 === 1 ? 'md:ml-auto md:mr-0 md:pr-8' : ''}`}>
                    <p className="text-xs text-champagne-soft tracking-widest font-medium mb-1">{event.date}</p>
                    <h4 className="font-display text-lg font-bold text-ivory">{event.title}</h4>
                    <p className="text-sm text-ivory/50 font-editorial mt-1">{event.description}</p>
                  </div>
                </div>

                {/* Center dot */}
                <div className="absolute left-[15px] md:left-1/2 md:-translate-x-1/2 top-1 w-[9px] h-[9px] rounded-full bg-gradient-to-br from-gold to-champagne border-2 border-deep-blue shadow-[0_0_12px_rgba(212,175,55,0.35)] z-10 shrink-0" />

                {/* Mobile card */}
                <div className="md:hidden pl-10">
                  <div className="glass-card rounded-2xl px-5 py-4 border-gold/10">
                    <p className="text-xs text-champagne-soft tracking-widest font-medium mb-1">{event.date}</p>
                    <h4 className="font-display text-lg font-bold text-ivory mb-1">{event.title}</h4>
                    <p className="text-sm text-ivory/50 font-editorial">{event.description}</p>
                  </div>
                </div>

                {/* Desktop opposite side */}
                <div className="hidden md:block w-1/2 md:pl-8 md:w-1/2">
                  <div className={`glass-card rounded-2xl px-5 py-4 max-w-xs border-gold/10 ${idx % 2 === 0 ? 'md:mr-auto md:ml-0' : 'md:ml-auto md:mr-0'}`}>
                    <p className="text-xs text-champagne-soft tracking-widest font-medium mb-1">{event.date}</p>
                    <h4 className="font-display text-lg font-bold text-ivory">{event.title}</h4>
                    <p className="text-sm text-ivory/50 font-editorial mt-1">{event.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="text-center mt-14">
          <p className="text-xs text-ivory/20 tracking-[0.3em] uppercase font-editorial italic">
            March 11 — Remembrance · December 8 — Salute Night · October 31 — First Golden Legends
          </p>
        </div>
      </div>
    </section>
  );
}
