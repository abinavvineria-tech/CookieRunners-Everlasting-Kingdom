import { useState, useCallback } from 'react';
import { Sparkles, Play, Trophy } from 'lucide-react';
import Particles from '../components/Particles';

export default function Hero() {
  const [ceremonyStarted, setCeremonyStarted] = useState(false);
  const [replaying, setReplaying] = useState(false);

  const startCeremony = useCallback(() => {
    setCeremonyStarted(true);
  }, []);

  const replay = useCallback(() => {
    setReplaying(true);
    setTimeout(() => setReplaying(false), 2500);
  }, []);

  return (
    <section id="ceremony" className="relative min-h-[100dvh] flex flex-col items-center justify-center overflow-hidden">
      <Particles />
      <div className="absolute inset-0 bg-gradient-to-b from-midnight/40 via-deep-blue/20 to-deep-blue/80 z-[1]" />

      <div className="relative z-10 max-w-4xl mx-auto px-6 text-center pt-28 pb-16 flex flex-col items-center gap-8">
        {/* Emblem */}
        <div className="relative">
          <div className={`w-20 h-20 md:w-28 md:h-28 rounded-full border-2 border-gold/40 flex items-center justify-center gold-glow transition-all duration-700 ${ceremonyStarted ? 'scale-110 border-gold/70' : 'scale-100'}`}>
            <Trophy className={`w-10 h-10 md:w-14 md:h-14 text-gold transition-all duration-700 ${ceremonyStarted ? 'rotate-[360deg]' : 'rotate-0'}`} strokeWidth={1.5} />
          </div>
          <Sparkles className="absolute -top-2 -right-2 w-5 h-5 text-champagne animate-pulse" />
        </div>

        <div className="space-y-3">
          <p className="text-xs md:text-sm font-editorial italic text-champagne-soft tracking-[0.35em] uppercase">
            First Edition — 2026
          </p>
          <h1 className="hero-title font-display font-black text-[3rem] md:text-[5rem] lg:text-[6.5rem] leading-[0.92] tracking-tight gold-gradient-text">
            Cookie Runners<br />
            <span className="text-[0.55em] md:text-[0.5em] tracking-[0.15em] font-editorial font-light not-italic text-ivory/90">
              Golden Legends Awards
            </span>
          </h1>
        </div>

        <p className="text-sm md:text-base text-ivory/60 max-w-xl leading-relaxed font-editorial italic">
          ONE KINGDOM. MANY LEGENDS. ONE COOKIE RUNNER FAMILY.
        </p>

        <div className="gold-divider w-48" />

        <p className="text-xs md:text-sm text-ivory/50 tracking-widest uppercase font-medium">
          Unofficial Fan Project — A Celebration of the Community
        </p>

        {!ceremonyStarted ? (
          <button
            onClick={startCeremony}
            className="group flex items-center gap-3 px-8 py-4 rounded-full border border-gold/30 bg-gold/5 hover:bg-gold/15 text-champagne font-medium tracking-widest text-sm transition-all hover:border-gold/60 hover:scale-[1.03] hover:shadow-[0_0_30px_rgba(212,175,55,0.15)]"
          >
            <Play className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
            Start the Ceremony
          </button>
        ) : (
          <div className="flex flex-col items-center gap-4 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div className="flex items-center gap-2 text-champagne-soft text-sm tracking-wide">
              <Sparkles className="w-4 h-4" />
              Ceremony in progress
            </div>
            <button
              onClick={replay}
              className="flex items-center gap-3 px-6 py-3 rounded-full border border-gold/20 bg-white/5 hover:bg-gold/10 text-champagne/80 font-medium text-sm transition-all hover:border-gold/40"
            >
              <Play className="w-4 h-4" />
              Replay Introduction
            </button>
            {replaying && (
              <p className="text-xs text-champagne-soft animate-pulse">Celebrating the legends...</p>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
